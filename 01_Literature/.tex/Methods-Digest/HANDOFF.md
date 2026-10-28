# Methods Digest: handoff for the next agent

Written 2026-10-20, updated 2026-10-23. Read this first, then run
`python build_digest.py --check` to confirm the state. For the reader's view see
[handout.md](handout.md).

## 1. What this is

A LaTeX ingest report that replaces reading the ~100 papers of the methodology
corpus: one chapter per stage (**S** scope/definitions, **A** app search/selection,
**D** material capture, **W** walkthrough, **C** codebook/pilot, **I** two-coder
comparison, **L** LLM feasibility, **H** harm tree, **R** reporting), each comparing
the papers' approaches with tables and "what this means for the thesis". Every
label `[n]` links to the highlighted passage in the paper, appended to one
bookmarked PDF, with back-links from the highlight to the citing sentence.
Deliverable: `build/Methods-Digest.pdf` (generated; about 150 MB, thousands of pages).

## 2. Constraints

- Project rules in [AGENTS.md](../../AGENTS.md) apply (review copy, single
  bibliography, graphify refresh, `check_project.py`, commit and push).
- The digest is organisational and adds no thesis content; it decides nothing.
- Krippendorff 2019 (key `krippendorff2019`, no. 22) is a shadow-library copy and
  stays in git-ignored `private/`. Do not touch `digest - Copy.pdf` in the repo root.

## 3. Files and pipeline

```
01_Literature/Methods-Digest/
  digest.tex            master document (macros below)
  build_digest.py       locate cited passages, write generated/, run latexmk
  add_paper.py          register an additional paper in registry.json
  registry.json         papers: num, key, label, stages, pdf path, pages, ...
  cards/NNN_key.tex     one card per paper
  sections/*.tex        stage chapters S A D W C I L H R, synthesis Z, front matter, intros
  tools/package.py      collect the PDFs into build/deliverables/ with an index
  tools/blocks.py       paper text with relative page markers -> text-cache/
  tools/ocr_pdf.py      invisible OCR text layer for a scanned PDF (RapidOCR)
  candidates.md         additional literature worth adding
  build/, generated/, pdf-cache/, private/, text-cache/   git-ignored
```

```
python 01_Literature\Methods-Digest\build_digest.py --check --fix-pages   # locate and report; fixes page numbers within ±3
python 01_Literature\Methods-Digest\build_digest.py --fix-pages           # complete volume -> build/Methods-Digest.pdf (10+ min)
python 01_Literature\Methods-Digest\build_digest.py --stage S             # one stage -> build/by-stage/1_S_Scope-and-definitions.pdf
python 01_Literature\Methods-Digest\build_digest.py --all-stages          # all nine stage volumes
python 01_Literature\Methods-Digest\build_digest.py --no-pdf              # generated files only
python 01_Literature\Methods-Digest\tools\blocks.py key [key ...]         # paper text -> text-cache/NNN_key.txt
python 01_Literature\Methods-Digest\tools\package.py                      # copy to build/deliverables/
```

### 3a. Volumes

A stage volume = front matter + the stage chapter + cards, references and full
texts of (a) papers whose registry `stages` contain the stage, (b) every paper the
chapter cites, (c) everything those cards cite. Built from `digest.tex` with
`\def\onlystage{X}\def\gendir{generated/stage_X}` (latexmk `-usepretex`, own job
name, output `build/stage_X/`). Numbers `[n]` are identical in all volumes; papers
outside a volume appear as plain labels. Run builds in the background, one after
the other.

**Macros.** `\pc{key}{page}{snippet}`: passage citation `[n, p. x]`, linked to the
highlight; *page* = page inside the appended copy (the `=== PAGE n ===` marker in
text-cache), not the printed page. `\pp{key}` `[n]`; `\pa{key}` Author (Year) [n];
`\pt{key}` Author (Year). `papercard` environment with `\cf{Heading}` items;
`\stagetag{X}`; `\stagechapter{X}{Title}`; boxes `thesisbox`, `notebox`,
`protocolbox`. `\regpaper` and bibliography entries come from the registry
(`generated/registry.tex`).

## 4. Writing a card

1. `tools/blocks.py key`, then read `text-cache/NNN_key.txt` (for long documents:
   method, results, limitations; skim the rest).
2. Write `cards/NNN_key.tex` as a `papercard`: **Stages** (with `\stagetag`), topic
   paragraphs (aim, design, procedure, reliability, findings), **Limits (card)**,
   **Use for this thesis**. Style models: `053_artstein2008`, `063_rodriguez2024`,
   `023_citron2021` — dense, numbers kept, card critique labelled, no invented results.
3. `\pc` after each substantive claim (about 15 to 30 per card).
4. `build_digest.py --check --fix-pages` until 0 problems.

**Snippet rules.** Matching is NFKC, lower-case, alphanumeric-only on the PDF text
layer: insensitive to spaces and hyphenation, sensitive to dropped glyphs and OCR
errors. At least 18 alphanumeric characters, exactly once on that page, not across
a page break (column breaks are fine). Copy verbatim from text-cache. Avoid
footnote digits inside the sentence ("workers1 or"), Greek letters and maths,
ligature words where fi/ff/fl are lost ("frst", "ofer" in the ACM Li et al. text),
accented words the layer splits. `--fix-pages` repairs pages off by up to 3 when
the snippet is unique. Scanned PDFs: `tools/ocr_pdf.py in.pdf out.pdf`, register
the OCR copy, match its text including errors.

## 5. Status

- **21 October:** cards for 99 of 100 papers (not Parker 2019, no. 41: no PDF).
  Instrument appendices (094, 097–100) are second `papercard` blocks inside their
  parent cards (002, 016, 018, 025, 036). All stage chapters, `Z_synthesis.tex`,
  `00_front.tex` and the intros are written. `--check`: 2,111 passages, 99 papers,
  0 problems.
- **23 October:** registry nos. 101–116 are the priority-A papers of the
  [gap search](../Literature-Gap-Search_2026-10-23.md) (PDFs in
  `PDFs/Methods-Reading/13_Search-2026-10-23/`, cards `101_xie2025` …
  `116_mehrnezhad2024`). Chapter L has two new sections (recent LLM policy studies;
  from model labels to conclusions) and extended table, notebox, checklist and
  thesisbox; H and C one new item each. `--check`: 2,317 passages, 115 papers,
  0 problems. Only the stage L volume was rebuilt; the other volumes show the
  99-paper state. Priority-A items without a PDF (Velykoivanenko 2021, Mehrnezhad &
  Almeida 2021, Doherty 2025, Gasteiger 2023, Martin 2015, Pollach 2005, Bhatia 2016)
  are listed in the gap search and the action plan §8.
- **Remaining:** rebuild the complete volume and the eight older stage volumes;
  visual check of the PDFs; optionally the [candidates](candidates.md) (high
  priority: Henson/Torous APA framework papers, Zimmeck APP-350, Cicchetti and
  Feinstein 1990 Part II). Procedure for an addition: download to
  `PDFs/Methods-Reading/12_Additions/`, `python add_paper.py '{...json...}'`,
  `blocks.py`, card.

**Notes on individual papers**

- 070 `nissenbaum2009`: the registered PDF had front matter only; registry no. 70
  now points to an OCR copy of the open TOC + Introduction scan (Yale course copy,
  `PDFs/Methods-Reading/12_Additions/X_Nissenbaum_2010_Privacy-in-Context_TOC-and-Introduction_OCR.pdf`,
  22 pages; OCR errors such as "1g6os"). The original file is kept.
- 059 `obrien2014`: the PDF is only the supplemental appendix (list of 40 sources).
- 072 `brooks2017` (NIST IR 8062): first PDF page has no text.
- 041 `parker2019`: no PDF; cannot be anchored.
- Card critiques worth surfacing: Gilardi's "intercoder agreement" for ChatGPT is
  run-to-run consistency, and the gold standard keeps only items both coders agreed
  on; McHugh's cut-off and squared-kappa table are the author's own proposals; Doan
  et al. report 37 % vs 32 % bloated flows, 59 vs 62 flows and 37 vs 31 risks
  inconsistently; Lombard et al. and Krippendorff disagree on percent agreement and
  overlapping coding.

## 6. Gotchas

- PowerShell `cd` persists and sometimes resets; use absolute paths.
- `Copy-Item` of many files into a missing directory fails silently per file;
  create the directory first.
- Do not run Python with `-I` when user-site packages are needed (PyMuPDF `fitz`,
  RapidOCR).
- `blocks.py` (`sort=False` blocks) is the reference for what `\pc` can match; the
  build uses the same layer.
- The `Read` tool truncates large text files; use offsets or grep headings first.
