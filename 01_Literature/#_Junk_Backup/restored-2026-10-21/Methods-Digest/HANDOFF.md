# Methods Digest: handoff for the next agent

Written 2026-10-20 at the end of a long session. Read this first, then `python build_digest.py --check` to confirm the state.

## 1. What this is

The user (Hamza, bachelor thesis on how harms of privacy/data practices in health apps are communicated) asked for a long LaTeX **ingest report** that replaces reading all ~100 papers of the reading corpus:

- one chapter per stage **S** scope/definitions, **A** app search/selection, **D** material capture, **W** walkthrough, **C** codebook/pilot, **I** two-coder comparison, **L** LLM feasibility, **H** harm tree, **R** reporting;
- each chapter gives, per paper, the methodology it used, with subsections for the different approaches, comparison tables and "what this means for the thesis";
- **every reference label `[n]` is a hyperlink to the exact passage in the paper**, so all papers are appended to one large, well-bookmarked PDF (highlight on the cited sentence, back-links from the highlight to the citing sentence);
- extra literature found along the way is to be added and downloaded (user is on a university network); best practices may be implemented freely; graphify first (done, only for the stage mapping).

Final deliverable: `01_Literature/Methods-Digest/build/Methods-Digest.pdf` (generated; about 150 MB, thousands of pages).

## 2. Standing constraints (from AGENTS.md and the user)

- Never edit `03_Thesis/Thesis_Review-Copy.docx`. Keep `_shared/references.bib` the only bibliography.
- After modifying LaTeX or Markdown run `.\graphify.ps1 refresh`; after editing thesis/bibliography/Markdown links run `python scripts/check_project.py` (must report 0 errors). This handoff file is Markdown: run both before finishing.
- Do not invent results or resolve open decisions; record methodological choices in `00_Admin/Decision-Log.md` with evidence. The digest is an organisational file and adds no thesis content.
- Do not commit or push unless asked. The repo is pushed to GitHub: the Krippendorff 2019 shadow-library copy (key `krippendorff2019`, no. 22) must stay in git-ignored `private/`.
- Never send the user's email to external services. Do not touch `digest - Copy.pdf` in the repo root (the user's copy).
- Do not spawn subagents unless the user asks.

## 3. Files and pipeline

```
01_Literature/Methods-Digest/
  digest.tex            master document (macros below)
  build_digest.py       locate cited passages, write generated/, run latexmk
  add_paper.py          register an additional paper in registry.json
  registry.json         100 papers: num, key, label, stages, pdf path, pages, ...
  cards/NNN_key.tex     one paper card each (94 files, 99 papers)
  sections/*.tex        stage chapters S A D W C I L H R, synthesis Z, front matter, intros (written)
  tools/package.py      collect the PDFs into build/deliverables/ with a README index
  tools/blocks.py       text of a paper with relative page markers -> text-cache/
  tools/ocr_pdf.py      add an invisible OCR text layer to a scanned PDF (RapidOCR)
  text-cache/           extracted texts (git-ignored); regenerate with tools/blocks.py
  candidates.md         additional literature worth adding
  build/, generated/, pdf-cache/, private/   git-ignored
```

Commands (run from the repo root; the first one is the quick loop):

```
python 01_Literature\Methods-Digest\build_digest.py --check --fix-pages   # locate and report only, fixes wrong page numbers within +-3
python 01_Literature\Methods-Digest\build_digest.py --fix-pages           # full build incl. latexmk (10+ minutes; run in background)
python 01_Literature\Methods-Digest\build_digest.py --no-pdf              # write generated files only
python 01_Literature\Methods-Digest\tools\blocks.py key [key ...]         # read a paper: text-cache/NNN_key.txt
```

### 3a. Volumes: complete PDF and one PDF per stage

```
python 01_Literature\Methods-Digest\build_digest.py --fix-pages                  # complete volume -> build/Methods-Digest.pdf
python 01_Literature\Methods-Digest\build_digest.py --stage S                    # one stage volume -> build/by-stage/1_S_Scope-and-definitions.pdf
python 01_Literature\Methods-Digest\build_digest.py --all-stages                 # all nine stage volumes
python 01_Literature\Methods-Digest\tools\package.py                             # copy to build/deliverables/ with an index
```

A stage volume = front matter + the stage chapter + the cards, references and full texts of (a) papers whose registry `stages` contain the stage, (b) every paper cited in the chapter, (c) everything those cards cite. It is built from `digest.tex` with `\def\onlystage{X}\def\gendir{generated/stage_X}` (latexmk `-usepretex`, own job name and output folder `build/stage_X/`). Registry numbers `[n]` are identical in all volumes. Papers outside a stage volume appear as plain labels. Each volume takes a few minutes; the complete volume 10+ minutes (about 150 MB). Run them in the background and one after the other.

State: `--check` reports 2111 passages anchored across 99 papers; 0 problems.

### Macros (digest.tex)

- `\pc{key}{page}{snippet}`: passage citation, renders `[n, p. x]`, links to the highlighted passage in the appended full text. **page = page number inside the appended copy** (the `=== PAGE n ===` marker in text-cache), not the printed page number.
- `\pp{key}` `[n]` link to the full text; `\pa{key}` Author (Year) [n]; `\pt{key}` Author (Year).
- `papercard` environment with `\cf{Heading}` items (see cards). `\stagetag{X}` coloured stage letter. `\stagechapter{X}{Title}`. Boxes: `thesisbox`, `notebox`, `protocolbox`.
- `\regpaper` / bibliography entries are generated from the registry (`generated/registry.tex`).

## 4. How to write a card (the loop that worked)

1. `python tools/blocks.py key` then read `text-cache/NNN_key.txt` (whole paper; for long documents read the method/results/limitations sections and skim the rest).
2. Write `cards/NNN_key.tex` as a `papercard`. Existing headings in order: **Stages** (with `\stagetag`), then topic paragraphs (aim, design, procedure, reliability, findings, ...), then **Limits (card)**, then **Use for this thesis**. Look at `cards/053_artstein2008.tex`, `cards/063_rodriguez2024.tex`, `cards/023_citron2021.tex` as the current style: dense, factual, numbers kept, own critique clearly labelled as card critique, no invented results.
3. Cite with `\pc` after each substantive claim (about 15 to 30 per card).
4. `python build_digest.py --check --fix-pages` until 0 problems.

### Snippet rules (what makes `\pc` fail)

- Matching is NFKC, lower-case, alphanumeric-only on the PDF text layer. Insensitive to spaces and hyphenation, sensitive to dropped glyphs and OCR errors.
- At least 18 alphanumeric characters; must occur **exactly once** on that page; must not span a page break (a column break inside a page is fine).
- Copy the sentence from `text-cache` verbatim. Do not paraphrase inside the braces, do not add or drop words.
- Avoid: footnote digits inside the sentence ("workers1 or"), Greek letters/maths (glyphs often dropped), ligature words in PDFs where fi/ff/fl are lost (e.g. "frst", "ofer" in the ACM Li et al. text; check the cache), words with accents that the text layer splits.
- Page numbers can be off by one or two for long documents; `--fix-pages` repairs this when the snippet is unique on a page within +-3.
- Scanned PDFs have no text layer: run `tools/ocr_pdf.py in.pdf out.pdf` and register the OCR copy (see Nissenbaum below); snippets must then match the OCR text, errors included.

## 5. Status (updated 2026-10-21)

**Done:** cards for 99 of 100 papers (all but Parker 2019, no PDF). The instrument appendices (094, 097-100) are second `papercard` blocks inside the cards of their parent papers (002, 016, 018, 025, 036). The nine stage chapters (`sections/S,A,D,W,C,I,L,H,R.tex`), `Z_synthesis.tex`, `00_front.tex` and the three intro files are written. `--check` reports 0 problems. **Remaining:** a full build of the complete volume and the nine stage volumes (see section 3a), visual check of the PDFs, `.\graphify.ps1 refresh`, `python scripts/check_project.py`; optionally the candidate literature below.

The tables in the next subsection are the old to-do list from before this session and are kept only for the notes on individual papers.

### Cards still to write (old list, now done except Parker)
| no. | key | note |
|---|---|---|
| 070 | nissenbaum2009 | The PDF originally registered contained **front matter only**. I downloaded the open TOC+Introduction scan (Yale course copy), added an OCR text layer (`PDFs/Methods-Reading/12_Additions/X_Nissenbaum_2010_Privacy-in-Context_TOC-and-Introduction_OCR.pdf`, 22 pages) and **re-pointed registry no. 70 to it**. Text is in text-cache (OCR errors such as "1g6os"). Card not written. Keep the original file; tell the user. |
| 071 | deng2011 | LINDDUN. Read to p. 12 of 32: privacy properties (hard/soft), seven threat types Linkability, Identifiability, Non-repudiation, Detectability, Disclosure of information, Content unawareness, Policy/consent non-compliance; DFD elements E/DF/DS/P and Table 4 mapping; STRIDE background (9 steps). Still to read: threat-tree catalog (Sect. 6 from 6.4), misuse cases (7), PET mapping (8), related work/discussion/limits. |
| 072 | brooks2017 | NIST IR 8062 (privacy engineering/risk). Not read. First PDF page has no text. |
| 056-059, 075, 076 | page2021, rethlefsen2021, tricco2018, obrien2014, arksey2005, vonelm2007 | Reporting guidelines (PRISMA 2020, PRISMA-S, PRISMA-ScR, SRQR, Arksey and O'Malley, STROBE). Cards should list the reporting items and which apply to a thesis that is not a systematic review. 059 PDF is only the supplemental appendix (list of 40 sources), say so. |
| 080-082, 084 | gabriele2020, cao2024, niksirat2024, knabenhans2026 | Harm/context: fitness-tracker users' privacy knowledge (CHI 2020), period-tracker concerns after Roe (Duke), survey of wearable trackers (236 studies), privacy harms of the EU digital identity framework (harm derivation method). |
| 090-093 | apa2024, wp292018, aoir2019, bfarm2023 | Official: APA App Evaluation Model (web capture), Article 29 WP transparency guidelines (WP260), AoIR ethics 3.0 (83 pp.), BfArM DiGA fast-track guide (128 pp.). Extract decision rules the thesis can apply. |
| 094 | hutton2017heuristics | text-cache missing; run blocks.py. |
| 095 | nissenbaum2004 | Privacy as Contextual Integrity (41 pp.). |
| 097-100 | lamonica2021tool, messner2020marsg, huckvale2015af, stoyanov2015mars | Instrument appendices; short cards (or fold into 016/018/025/036 cards and say so). |
| 041 | parker2019 | No PDF available; cannot be anchored. Either obtain it or give it a bibliography-only entry. |

### Chapters still to write (the main remaining work)
`sections/S.tex, A.tex, D.tex, W.tex, C.tex, I.tex, L.tex, H.tex, R.tex` are stubs (A.tex holds a 2-line test). Also `00_front.tex` (title, how to use, legend, TOC), `Z_synthesis.tex`, `cards_intro.tex`, `refs_intro.tex`, `fulltexts_intro.tex`. Each stage chapter should: define the stage in one paragraph, then one subsection per approach found in the literature, with `\pc` citations to the exact passages, a comparison table, and a `thesisbox`/`protocolbox`/`notebox`. Use the `Stages` line of each card and `registry.json` (`stages`, `when`, `use`, `caution`) to find which papers belong. Suggested content per stage:

- **I (reliability)**: percent agreement, Scott pi, Cohen kappa, Fleiss, Krippendorff alpha (+ CI by bootstrap), Gwet AC1, ICC, kappa paradoxes (Feinstein and Cicchetti, Gwet, Hallgren), thresholds (Krippendorff .800/.667, Landis and Koch, McHugh stricter, Lombard .70/.80/.90), sample sizes (Lombard 30 pilot, 50 or 10 percent; McHugh >= 30; Artstein >= 5 chance agreements per category), reporting checklists (Lombard 10 items, Hallgren). Note disputes: Krippendorff 2004 vs Lombard (liberal/conservative myth), McHugh's mislabelled Landis and Koch bands.
- **L (LLM)**: Pangakis 5-step workflow, Toernberg 9 points, Baumann "LLM hacking" and pre-registration, Rodriguez prompt-tuning and determinism data, Gilardi (self-agreement is not inter-coder reliability; gold standard drops disagreements), Mayring 2025 (qualitative inductive coding), Harkous and Wilson (pre-LLM baselines).
- **H (harm)**: Solove 2006 activities x Citron and Solove 2022 harm types, Martin et al. (purpose and inference), Moniz and Almeida (user-perceived harms), Doan et al. (CI flows, stated risks), LINDDUN, Nissenbaum CI.
- **D/A/W/C**: see cards 001-029 (app reviews, walkthrough, heuristics, codebooks); Arkalakis and Li show label-vs-behaviour designs and capture cadence.
- **R**: reporting guidelines cards (to be written) plus Lombard's reporting list.

### Additional literature (not yet added)
See `candidates.md`. High priority: Henson/Torous APA framework papers, Zimmeck APP-350, Cicchetti and Feinstein 1990 Part II (the "resolving the paradoxes" companion of card 034). Others: Krippendorff 2011/2016, Hertzum and Jacobsen, Gasteiger TECH, Mehrnezhad and Almeida 2021, attack trees (Schneier/Mauw), Calo 2011, Xiao 2023 (Rumi consent chatbot, cited by Moniz). Procedure: download (university network), put under `01_Literature/PDFs/Methods-Reading/12_Additions/`, `python add_paper.py '{...json...}'`, then `blocks.py` and a card.

## 6. Things to tell the user at the end

- Nissenbaum 2009 PDF problem and the OCR replacement (section 5).
- Card critiques worth surfacing: Gilardi's "intercoder agreement" for ChatGPT is run-to-run consistency and the gold standard keeps only items both coders agreed on; McHugh's cut-off and squared-kappa table are the author's own proposals; Doan et al. report 37% vs 32% bloated flows, 59 vs 62 flows and 37 vs 31 risks inconsistently; Lombard et al. and Krippendorff disagree on percent agreement and overlapping coding.
- Parker 2019 (no. 41) has no PDF.
- Krippendorff 2019 stays in `private/` (not pushed).
- Build time (10+ minutes) and PDF size (about 150 MB).

## 7. Gotchas from this session

- PowerShell `cd` persists across calls and sometimes resets; always use absolute paths or `cd` first.
- `Copy-Item` of many files into a directory that does not exist fails silently per file; create the directory first.
- Do not run Python with `-I` when you need user-site packages such as PyMuPDF (`fitz`) or RapidOCR.
- The text extraction (`blocks.py`, `sort=False` blocks) is the reference for what `\pc` can match; the build uses the same layer.
- The `Read` tool truncates large text files; use offsets (a 250k-character paper needs 3 or more reads) or grep section headings first.
