"""Build the Methods Digest: locate cited passages, generate the appendix, compile.

Citations in the LaTeX sources use

    \\pc{key}{page}{exact snippet copied from the paper}

where ``page`` is the 1-based page of the appended copy. This script finds every
snippet on its page (tolerant to hyphenation, line breaks, ligatures and
punctuation), then writes ``generated/*.tex`` so that each citation links to a
named destination just above the passage, the passage is highlighted in the
appended full text, and the highlight links back to the citing sentence.

usage:  python build_digest.py            # locate, generate, compile, optimise
        python build_digest.py --check    # locate and report only
        python build_digest.py --no-pdf   # generate without compiling
        add --fix-pages to move a citation whose snippet occurs once on a nearby page to that page
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import statistics
import subprocess
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

import fitz  # PyMuPDF

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
GEN = HERE / "generated"
BUILD = HERE / "build"
SOURCES = ["sections/*.tex", "cards/*.tex"]
ONLY = None  # single stage letter when building a stage volume

PC_RE = re.compile(r"\\pc\{([^{}]+)\}\{([^{}]+)\}\{([^{}]+)\}")
PP_RE = re.compile(r"\\(?:pp|pa|pt)\{([^{}]+)\}")
STAGES = "SADWCILHR"
STAGE_NAMES = {
    "S": "Scope and definitions", "A": "App search and selection", "D": "Material capture",
    "W": "Walkthrough", "C": "Codebook and pilot", "I": "Two-coder comparison",
    "L": "LLM feasibility", "H": "Harm tree", "R": "Reporting",
}


# --------------------------------------------------------------------------- text helpers
def detok(s: str) -> str:
    """Mimic TeX's \\detokenize on a single-line argument (spaces collapsed)."""
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"(\\[A-Za-z]+)(?=[^A-Za-z ])", r"\1 ", s)
    return s


def anchor_hash(key: str, page: str, snippet: str) -> str:
    return hashlib.md5(detok(f"{key}|{page}|{snippet}").encode("utf-8")).hexdigest().upper()


def unescape(s: str) -> str:
    return re.sub(r"\\([%&_$#])", r"\1", s).replace("~", " ").replace("``", '"').replace("''", '"')


def norm_chars(s: str) -> str:
    s = unicodedata.normalize("NFKC", s).lower()
    s = s.replace("ß", "ss")
    return "".join(ch for ch in s if ch.isalnum())


def tex_escape(s: str) -> str:
    s = unicodedata.normalize("NFKC", s or "")
    rep = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
           "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
    s = "".join(rep.get(c, c) for c in s)
    for a, b in {"\u2010": "-", "\u2011": "-", "\u2012": "-", "\u2013": "--", "\u2014": "---",
                 "\u2018": "`", "\u2019": "'", "\u201c": "``", "\u201d": "''", "\u2026": "...",
                 "\u00a0": " ", "\u2212": "-", "\u2032": "'", "\u00b7": "$\\cdot$", "\u2192": "$\\rightarrow$"}.items():
        s = s.replace(a, b)
    return "".join(ch for ch in s if ord(ch) < 0x180)


def pdf_string(s: str) -> str:
    """Safe text for bookmarks (passed through hyperref's \\pdfstringdef)."""
    s = tex_escape(s)
    return s.replace("``", '"').replace("''", '"').replace("`", "'")


# --------------------------------------------------------------------------- registry
def load_registry() -> list[dict]:
    reg = json.loads((HERE / "registry.json").read_text(encoding="utf-8"))
    for e in reg:
        e["path"] = (ROOT / e["pdf"]) if e.get("pdf") else None
        if e["path"] and not e["path"].exists():
            print(f"WARNING missing file for {e['key']}: {e['pdf']}")
            e["path"] = None
    return sorted(reg, key=lambda e: e["num"])


def page_range(e: dict, doc: fitz.Document) -> list[int]:
    """0-based source page indices included in the appendix."""
    if e.get("pages"):
        a, b = e["pages"]
        return list(range(a - 1, b))
    return list(range(doc.page_count))


# --------------------------------------------------------------------------- locating
class PageIndex:
    def __init__(self, page: fitz.Page):
        self.page = page
        # content-stream order keeps columns intact (sorting interleaves two-column layouts)
        words = page.get_text("words", sort=False)
        self.words = words
        self.stream = []
        self.owner = []
        for i, w in enumerate(words):
            n = norm_chars(w[4])
            self.stream.append(n)
            self.owner.extend([i] * len(n))
        self.text = "".join(self.stream)

    def count(self, snippet: str) -> int:
        target = norm_chars(unescape(snippet))
        return self.text.count(target) if target else 0

    def find(self, snippet: str):
        target = norm_chars(unescape(snippet))
        if len(target) < 18:
            return None
        pos = self.text.find(target)
        if pos < 0:
            return None
        idx = sorted(set(self.owner[pos:pos + len(target)]))
        lines = defaultdict(list)
        for i in idx:
            w = self.words[i]
            lines[(w[5], w[6])].append(fitz.Rect(w[:4]))
        rects = []
        for k in sorted(lines):
            r = fitz.Rect(lines[k][0])
            for x in lines[k][1:]:
                r |= x
            rects.append(r * self.page.rotation_matrix)
        return rects


def collect_citations() -> dict[str, list[tuple[str, str, str]]]:
    cites: dict[str, list] = defaultdict(list)
    for pattern in SOURCES:
        for f in sorted(HERE.glob(pattern)):
            text = f.read_text(encoding="utf-8")
            text = re.sub(r"(?<!\\)%.*", "", text)  # drop comments
            for m in PC_RE.finditer(text):
                key, page, snip = m.group(1).strip(), m.group(2).strip(), m.group(3)
                cites[key].append((page, snip, f.name))
    return cites


def collect_plain_refs() -> set[str]:
    keys = set()
    for pattern in SOURCES:
        for f in sorted(HERE.glob(pattern)):
            for m in PP_RE.finditer(f.read_text(encoding="utf-8")):
                keys.add(m.group(1).strip())
    return keys


def locate(reg, cites):
    """Return anchors[key][rel_page] = list of dicts, a list of problems, and page fixes.

    A fix is (source file, key, stated page, snippet, page where the snippet was found)."""
    by_key = {e["key"]: e for e in reg}
    anchors = defaultdict(lambda: defaultdict(list))
    problems = []
    fixes = []
    for key, items in cites.items():
        e = by_key.get(key)
        if not e:
            problems.append(f"unknown key {key!r} ({items[0][2]})")
            continue
        if not e["path"]:
            problems.append(f"{key}: no PDF to anchor {len(items)} citation(s)")
            continue
        doc = fitz.open(e["path"])
        rng = page_range(e, doc)
        cache = {}
        seen = set()
        for page, snip, src in items:
            h = anchor_hash(key, page, snip)
            if h in seen:
                continue
            seen.add(h)
            try:
                rel = int(page)
            except ValueError:
                problems.append(f"{key}: page {page!r} is not an integer ({src})")
                continue
            if not 1 <= rel <= len(rng):
                problems.append(f"{key}: page {rel} outside 1..{len(rng)} ({src})")
                continue
            def idx(r):
                if r not in cache:
                    cache[r] = PageIndex(doc[rng[r - 1]])
                return cache[r]
            rects = idx(rel).find(snip)
            if rects is None:
                hint = ""
                for other in range(max(1, rel - 3), min(len(rng), rel + 3) + 1):
                    if other != rel and idx(other).find(snip):
                        hint = f" (found on page {other})"
                        if idx(other).count(snip) == 1:
                            fixes.append((src, key, page, snip, other))
                        break
                short = " (too short: need >= 18 letters/digits)" if len(norm_chars(unescape(snip))) < 18 else ""
                problems.append(f"{key} p.{rel}: snippet not found{short}{hint}: {snip[:70]!r} ({src})")
                continue
            if idx(rel).count(snip) > 1:
                problems.append(f"{key} p.{rel}: ambiguous snippet (occurs {idx(rel).count(snip)}x): {snip[:70]!r} ({src})")
            anchors[key][rel].append({"hash": h, "rects": rects, "snippet": unescape(snip)})
    return anchors, problems, fixes


def apply_page_fixes(fixes) -> int:
    """Rewrite \\pc{key}{page}{snippet} with the page on which the snippet was found."""
    done = 0
    for src, key, page, snip, new in fixes:
        f = next((p for pattern in SOURCES for p in HERE.glob(pattern) if p.name == src), None)
        if f is None:
            continue
        text = f.read_text(encoding="utf-8")
        old = f"\\pc{{{key}}}{{{page}}}{{{snip}}}"
        if text.count(old) == 1:
            f.write_text(text.replace(old, f"\\pc{{{key}}}{{{new}}}{{{snip}}}"), encoding="utf-8")
            done += 1
    return done


# --------------------------------------------------------------------------- headings for bookmarks
HEAD_NUM = re.compile(r"^((?:\d+\.)*\d+\.?|[IVX]+\.|[A-H]\.?\d*(?:\.\d+)*)\s+([A-Z][^\n]{2,90})$")
HEAD_WORD = re.compile(r"^(abstract|introduction|background|related work|methods?|methodology|materials and methods|"
                       r"study design|design|results|findings|discussion|limitations|conclusions?|references|"
                       r"bibliography|appendix(?: [a-z0-9]+)?(?:[:.].*)?|acknowledge?ments?|summary|overview|"
                       r"implications|future work|ethics|data analysis|procedure|sample|participants)\.?$", re.I)


def detect_headings(doc: fitz.Document, rng: list[int]):
    toc = doc.get_toc(simple=True)
    out = []
    if toc:
        inv = {src: i + 1 for i, src in enumerate(rng)}
        for level, title, pno in toc:
            if pno - 1 in inv and level <= 3 and title.strip():
                out.append((level, title.strip(), inv[pno - 1]))
        if out:
            return out
    sizes = []
    pages = []
    for i, src in enumerate(rng):
        d = doc[src].get_text("dict")
        lines = []
        for b in d["blocks"]:
            for l in b.get("lines", []):
                spans = [s for s in l["spans"] if s["text"].strip()]
                if not spans:
                    continue
                text = " ".join(s["text"].strip() for s in spans)
                size = max(s["size"] for s in spans)
                bold = all((s["flags"] & 16) or "bold" in s["font"].lower() or "black" in s["font"].lower()
                           or "semibold" in s["font"].lower() for s in spans)
                for s in spans:
                    sizes.extend([round(s["size"], 1)] * min(len(s["text"]), 200))
                lines.append((text, size, bold, l["bbox"][1]))
        pages.append(lines)
    body = statistics.median(sizes) if sizes else 10
    seen = set()
    for i, lines in enumerate(pages):
        for text, size, bold, _y in lines:
            t = re.sub(r"\s+", " ", text).strip()
            if len(t) > 95 or len(t) < 4:
                continue
            emph = bold or size >= body * 1.12
            if not emph:
                continue
            m = HEAD_NUM.match(t)
            if m and not re.search(r"\d{3,}|[=<>]|\bet al\b|\bp\.\s*\d", t):
                depth = m.group(1).rstrip(".").count(".") + 1
                level = min(depth, 3)
            elif HEAD_WORD.match(t):
                level = 1
            else:
                continue
            k = t.lower()
            if k in seen:
                continue
            seen.add(k)
            out.append((level, t, i + 1))
    return out[:60]


# --------------------------------------------------------------------------- generation
def fmt(x: float) -> str:
    return f"{x:.1f}"


def write_registry_tex(reg, anchors):
    lines = ["% generated by build_digest.py -- do not edit"]
    for e in reg:
        has = "1" if e["path"] else "0"
        lines.append(f"\\regpaper{{{e['key']}}}{{{e['num']}}}{{{tex_escape(e['label'])}}}{{{has}}}")
    (GEN / "registry.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")


def overlay_for_page(e, rel, total, H, W, page_anchors):
    key = e["key"]
    out = [r"\setlength\unitlength{1bp}\renewcommand\HyperRaiseLinkDefault{0pt}"]
    out.append(f"\\put(0,{fmt(H)}){{\\hypertarget{{p:{key}:{rel}}}{{}}}}")
    if rel == 1:
        out.append(f"\\put(0,{fmt(H)}){{\\hypertarget{{paper:{key}}}{{}}}}")
    if page_anchors:
        out.append(r"\put(0,0){\begin{tikzpicture}[overlay,x=1bp,y=1bp]")
        for a in page_anchors:
            for r in a["rects"]:
                out.append(f"\\fill[digesthl,blend mode=multiply]({fmt(r.x0 - 1.5)},{fmt(H - r.y1 - 1)})"
                           f" rectangle ({fmt(r.x1 + 1.5)},{fmt(H - r.y0 + 1)});")
            # margin bar at the page edge so a passage is easy to spot when scrolling
            ytop = max(H - r.y0 for r in a["rects"]) + 1
            ybot = min(H - r.y1 for r in a["rects"]) - 1
            xbar = 3 if min(r.x0 for r in a["rects"]) < W / 2 else W - 6
            out.append(f"\\fill[digestmark]({fmt(xbar)},{fmt(ybot)}) rectangle ({fmt(xbar + 3)},{fmt(ytop)});")
        out.append(r"\end{tikzpicture}}")
        for a in page_anchors:
            top = min(r.y0 for r in a["rects"])
            out.append(f"\\put(0,{fmt(min(H, H - top + 28))}){{\\hypertarget{{a:{a['hash']}}}{{}}}}")
            for r in a["rects"]:
                out.append(f"\\put({fmt(r.x0 - 1.5)},{fmt(H - r.y1 - 1)}){{\\backlinkbox{{{a['hash']}}}"
                           f"{{{fmt(r.width + 3)}bp}}{{{fmt(r.height + 2)}bp}}}}")
    out.append(f"\\put({fmt(W - 4)},{fmt(H - 3)}){{\\makebox(0,0)[rt]{{\\appendixtag{{{key}}}{{{rel}}}{{{total}}}}}}}")
    return "".join(out)


def write_appendix(reg, anchors):
    app = ["% generated by build_digest.py -- do not edit"]
    stage_index = defaultdict(list)
    for e in reg:
        for s in e.get("stages", []):
            stage_index[s].append(e)
        title = pdf_string(f"[{e['num']}] {e['label']}: {e['title']}")
        if not e["path"]:
            app.append(f"\\missingfulltext{{{e['key']}}}")
            app.append(f"\\bookmark[dest=bib:{e['key']},level=0]{{{title} (no full text)}}")
            continue
        doc = fitz.open(e["path"])
        rng = page_range(e, doc)
        total = len(rng)
        rel_path = e["path"].resolve().as_posix()
        heads = detect_headings(doc, rng)
        app.append(f"% [{e['num']}] {e['key']}: {total} pages")
        for rel, src in enumerate(rng, start=1):
            page = doc[src]
            W, H = page.rect.width, page.rect.height
            pa = anchors.get(e["key"], {}).get(rel, [])
            ov = overlay_for_page(e, rel, total, H, W, pa)
            app.append(f"\\includepdf[pages={{{src + 1}}},fitpaper,pagecommand={{\\thispagestyle{{empty}}}},"
                       f"picturecommand*={{{ov}}}]{{{rel_path}}}")
            if rel == 1:
                app.append(f"\\bookmark[dest=paper:{e['key']},level=0]{{{title}}}")
                if heads:
                    app.append(f"\\bookmark[dest=paper:{e['key']},level=1]{{Sections of the paper}}")
            for level, htext, hp in heads:
                if hp == rel:
                    app.append(f"\\bookmark[dest=p:{e['key']}:{rel},level={1 + level}]{{{pdf_string(htext)}}}")
        cited = sorted(((p, a) for p, lst in anchors.get(e["key"], {}).items() for a in lst),
                       key=lambda pa: (pa[0], min(r.y0 for r in pa[1]["rects"])))
        if cited:
            app.append(f"\\bookmark[dest=a:{cited[0][1]['hash']},level=1]{{Cited passages ({len(cited)})}}")
            for p, a in cited:
                snip = a["snippet"]
                snip = snip if len(snip) <= 70 else snip[:67].rsplit(" ", 1)[0] + "..."
                app.append(f"\\bookmark[dest=a:{a['hash']},level=2]{{p. {p}: {pdf_string(snip)}}}")
    (GEN / "appendix.tex").write_text("\n".join(app) + "\n", encoding="utf-8")

    idx = ["% generated by build_digest.py -- do not edit"]
    idx.append(r"\bookmark[named=FirstPage,level=-1]{Full texts by stage}")
    for s in (ONLY if ONLY else STAGES):
        idx.append(f"\\bookmark[dest=stage:{s},level=0]{{{s} -- {STAGE_NAMES[s]} ({len(stage_index[s])})}}")
        for e in stage_index[s]:
            dest = f"paper:{e['key']}" if e["path"] else f"bib:{e['key']}"
            idx.append(f"\\bookmark[dest={dest},level=1]{{{pdf_string('[' + str(e['num']) + '] ' + e['label'])}}}")
    (GEN / "stage-bookmarks.tex").write_text("\n".join(idx) + "\n", encoding="utf-8")


def write_bibliography(reg, anchors):
    out = ["% generated by build_digest.py -- do not edit"]
    for e in reg:
        n_cites = sum(len(v) for v in anchors.get(e["key"], {}).values())
        doi = e.get("doi") or ""
        url = e.get("url") or ""
        pages = ""
        if e["path"]:
            doc = fitz.open(e["path"])
            pages = str(len(page_range(e, doc)))
        stages = ",".join(e.get("stages", []))
        if doi:
            url = f"https://doi.org/{doi}"
        url_tex = url.replace("%", "\\%").replace("#", "\\#")
        doi = tex_escape(doi)  # display form; the link itself travels in url_tex
        out.append(
            f"\\bibmeta{{{e.get('priority', '')}}}{{{tex_escape(e.get('list_id', ''))}}}{{{pages}}}"
            f"{{{n_cites}}}{{{tex_escape(e.get('version', ''))}}}{{{tex_escape(e.get('category', ''))}}}"
        )
        out.append(
            f"\\bibentry{{{e['key']}}}{{{e['num']}}}{{{tex_escape(e['authors'])}}}"
            f"{{{tex_escape(str(e['year'] or 'n.d.'))}}}{{{tex_escape(e['title'])}}}{{{tex_escape(e.get('venue', ''))}}}"
            f"{{{doi}}}{{{url_tex}}}{{{stages}}}"
        )
    (GEN / "bibliography.tex").write_text("\n".join(out) + "\n", encoding="utf-8")


def write_cards_list(reg):
    out = ["% generated by build_digest.py -- do not edit"]
    cards = {p.stem.split("_", 1)[1]: p for p in (HERE / "cards").glob("*.tex")}
    order = ["App reviews", "App appraisal", "Walkthrough", "Privacy interfaces", "Policy annotation",
             "Coding", "Agreement", "LLM annotation", "Context/harm", "Review/reporting",
             "Official and methods", "Additions"]
    groups = defaultdict(list)
    for e in reg:
        if e["key"] in cards:
            groups[e["category"]].append(e)
    for cat in order + sorted(set(groups) - set(order)):
        if not groups.get(cat):
            continue
        title = {"Context/harm": "Privacy harm and context", "Review/reporting": "Reviews and reporting guidelines",
                 "Official and methods": "Official guidance and non-DOI method sources",
                 "Additions": "Additional literature found while reading"}.get(cat, cat)
        out.append(f"\\chapter{{{title}}}")
        for e in groups[cat]:
            out.append(f"\\input{{cards/{cards[e['key']].name}}}")
    (GEN / "cards.tex").write_text("\n".join(out) + "\n", encoding="utf-8")


def compile_pdf(stage=None):
    BUILD.mkdir(exist_ok=True)
    if stage:
        outdir = BUILD / f"stage_{stage}"
        outdir.mkdir(exist_ok=True)
        pretex = "\\def\\onlystage{%s}\\def\\gendir{generated/stage_%s}" % (stage, stage)
        cmd = ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", f"-outdir={outdir}",
               f"-jobname=stage_{stage}", "-usepretex", f"-pretex={pretex}", "digest.tex"]
        jobname = f"stage_{stage}"
    else:
        outdir = BUILD
        cmd = ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", f"-outdir={BUILD}", "digest.tex"]
        jobname = "digest"
    r = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True, encoding="utf-8", errors="replace")
    log = outdir / f"{jobname}.log"
    if r.returncode != 0:
        tail = log.read_text(encoding="latin-1", errors="replace")[-4000:] if log.exists() else r.stdout[-4000:]
        print(tail)
        sys.exit("latexmk failed")
    text = log.read_text(encoding="latin-1", errors="replace")
    for pat in [r"Package hyperref Warning: .*", r"pdfTeX warning \(dest\): .*", r"LaTeX Warning: .*undefined.*"]:
        hits = re.findall(pat, text)
        if hits:
            print(f"{len(hits)} x {pat[:40]} e.g. {hits[0][:120]}")
    src = outdir / f"{jobname}.pdf"
    if stage:
        (BUILD / "by-stage").mkdir(exist_ok=True)
        n = STAGES.index(stage) + 1
        name = STAGE_NAMES[stage].replace(" ", "-")
        out = BUILD / "by-stage" / f"{n}_{stage}_{name}.pdf"
    else:
        out = HERE / "build" / "Methods-Digest.pdf"
    doc = fitz.open(src)
    doc.save(out, garbage=3, deflate=True, use_objstms=1)
    print(f"wrote {out} ({out.stat().st_size / 1e6:.1f} MB, {doc.page_count} pages)")


KEY_RE = re.compile(r"\\(?:pc|pp|pa|pt)\{([^{}]+)\}")


def stage_subset(reg, stage):
    """Papers of one stage volume: registry-tagged for the stage, cited in its chapter, and
    everything those papers' cards cite (one fixed-point pass)."""
    by_key = {e["key"]: e for e in reg}
    keys = {e["key"] for e in reg if stage in e.get("stages", [])}
    chapter = HERE / "sections" / f"{stage}.tex"
    keys |= {k.strip() for k in KEY_RE.findall(chapter.read_text(encoding="utf-8"))} & set(by_key)
    card_files = {p.stem.split("_", 1)[1]: p for p in (HERE / "cards").glob("*.tex")}
    changed = True
    while changed:
        changed = False
        for k in list(keys):
            if k in card_files:
                found = {x.strip() for x in KEY_RE.findall(card_files[k].read_text(encoding="utf-8"))} & set(by_key)
                if not found <= keys:
                    keys |= found
                    changed = True
    return [e for e in reg if e["key"] in keys]


def main():
    global GEN, ONLY
    GEN.mkdir(exist_ok=True)
    reg = load_registry()
    cites = collect_citations()
    anchors, problems, fixes = locate(reg, cites)
    if "--fix-pages" in sys.argv and fixes:
        print(f"fixed the page of {apply_page_fixes(fixes)} citation(s); re-checking")
        anchors, problems, fixes = locate(reg, collect_citations())
    known = {e["key"] for e in reg}
    for k in sorted(collect_plain_refs() - known):
        problems.append(f"unknown key in \\pp/\\pa/\\pt: {k!r}")
    n = sum(len(v) for d in anchors.values() for v in d.values())
    print(f"{n} passages anchored across {len(anchors)} papers; {len(problems)} problem(s)")
    for p in problems:
        print("  -", p)
    if "--check" in sys.argv:
        sys.exit(1 if problems else 0)
    write_registry_tex(reg, anchors)
    jobs = []
    if "--stage" in sys.argv:
        jobs = [sys.argv[sys.argv.index("--stage") + 1]]
    elif "--all-stages" in sys.argv:
        jobs = list(STAGES)
    if not jobs or "--with-complete" in sys.argv:
        write_appendix(reg, anchors)
        write_bibliography(reg, anchors)
        write_cards_list(reg)
        if "--no-pdf" not in sys.argv:
            compile_pdf()
    base = GEN
    for s in jobs:
        sub = stage_subset(reg, s)
        GEN = base / f"stage_{s}"
        GEN.mkdir(exist_ok=True)
        ONLY = s
        write_registry_tex(reg, anchors)
        write_appendix(sub, anchors)
        write_bibliography(sub, anchors)
        write_cards_list(sub)
        print(f"stage {s}: {len(sub)} papers")
        if "--no-pdf" not in sys.argv:
            compile_pdf(s)
        ONLY = None
        GEN = base


if __name__ == "__main__":
    main()
