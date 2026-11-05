# Methods Digest: handout

For the thesis author, or anyone opening the PDFs for the first time. (The agent-to-agent notes for continuing the work are in [HANDOFF.md](HANDOFF.md).)

## What it is

A reading replacement for the ~100 methodology papers of the thesis corpus. Nine stage chapters compare what the literature did, with numbers, cautions and "implications for this thesis" boxes. Behind them sit one card per paper, the numbered reference list and the papers themselves, appended to the PDF. It adds no thesis content and decides nothing; the evidence for each open decision (D1 to D12) is mapped in the synthesis chapter.

## Which file to open

All PDFs are in `build/deliverables/` (git-ignored; see "Rebuild" if missing). The list with sizes and page counts is `build/deliverables/README.md`.

| I want to... | Open |
|---|---|
| Read everything, search across stages | `00_Methods-Digest_complete.pdf` (122 MB, 2,923 pages) |
| Work on one part of the method | `by-stage/N_X_Name.pdf` |

| Stage | File | Question it answers | Decisions |
|---|---|---|---|
| S | `1_S_Scope-and-definitions` | What is a tracker app, what is harm, privacy, transparency; what kind of study? | D3, D6, D11 |
| A | `2_A_App-search-and-selection` | Stores, keywords, ranking, thresholds, flow of numbers | D1 to D5, D7 |
| D | `3_D_Material-capture` | What is captured per app and how it is archived | D2, D5, D7 |
| W | `4_W_Walkthrough` | Tasks, questions, outcomes of the interface inspection | D10, D11 |
| C | `5_C_Codebook-and-pilot` | Origin of codes, entry structure, pilot | D8, D10 |
| I | `6_I_Two-coder-comparison` | Agreement statistic, thresholds, sample, reporting | D8 |
| L | `7_L_LLM-feasibility` | Configuring, validating, reporting an LLM | D9 |
| H | `8_H_Harm-tree` | Harm definitions, typologies, tree structure | D12 |
| R | `9_R_Reporting` | Which reporting guidelines to adapt | none |

A stage volume holds its chapter plus the cards, references and full texts of the papers of that stage and of every paper its chapter cites. Papers outside the volume appear as plain text, not links. Paper numbers `[n]` are the same in every file.

## How to read the PDF

- **Start** with the "How to use this digest" page, then the stage chapter, then the `Implications for this thesis` box at its end.
- **`[12, p. 4]`** is a link: it jumps to page 4 of the appended paper 12, where the cited sentence is highlighted in yellow. Page numbers are those of the appended copy, not the journal. Return with Alt+Left.
- **Orange mark** beside a highlight: click to jump back to the sentence that cites it.
- **Author (Year) [n]** links to the reference entry and to the paper.
- **Bookmarks** (outline panel): parts, chapters, all cards, all papers with their section headings, and the cited passages per paper.
- A **card** is the per-paper summary: stages, design, numbers, authors' limits, `Limits (card)` (the compiler's critique) and `Use for this thesis`. Check card critiques against the paper before adopting them.

## What to know before relying on it

- 115 papers have cards (nos. 101–116 added on 23 October; only the stage L volume
  includes them so far); Parker 2019 (no. 41) has no PDF and no card.
- Nissenbaum 2009 (no. 70) is only the table of contents and introduction, from a scan with an OCR text layer. Quotes may contain recognition errors, as may Polson 1992 and Cohen 1960 (also OCR).
- Several files are author manuscripts, preprints, web captures (APA, 20 Oct 2026) or supplementary appendices; each card says so. The BfArM guide is the 2020 text although the corpus label says 2023.
- The thesis plan statements come from `03_Thesis/chapters/04_methodology.tex` (draft) and the Decision Log. They change as decisions close.
- **Private use only.** The full texts include copies that must not be redistributed (Krippendorff 2019, kept in git-ignored `private/`). Do not share or publish these PDFs.

## Rebuild

From the repository root (Windows, TeX Live 2025, PyMuPDF; no internet needed). Run `build_digest.py` from the repo root.

```
# 1. check citations, write all generated files (about 80 s)
python 01_Literature\digest\build_digest.py --all-stages --with-complete --no-pdf --fix-pages

# 2. compile one volume (fast recipe: two draft passes, one real pass)
python 01_Literature\digest\build_digest.py --compile-only --fast               # complete
python 01_Literature\digest\build_digest.py --compile-only --fast --stage A     # one stage

# 3. collect into build/deliverables/ with an index
python 01_Literature\digest\tools\package.py
```

Compiling all ten in parallel (about four at a time, limited by RAM) took roughly 13 minutes; one after another about 80. If a compile stops at `\begin{document}` with "File ended while scanning use of \BKM@entry", delete that volume's folder under `build/` and rerun.

Quick check without building PDFs: `python 01_Literature\digest\build_digest.py --check --fix-pages` (2,317 passages across 115 papers, 0 problems, on 23 October).

The `text-cache/` and `pdf-cache/` folders were deleted as reproducible. Recreate the text of a paper with `tools\blocks.py KEY`. `pdf-cache/012_Polson_1991_OCR.pdf` is needed by the build and is made with `tools\ocr_pdf.py` from the scan in `PDFs/Methods-Reading/03_Walkthroughs/`; it already exists again.

## Where things are

```
01_Literature/digest/
  sections/    stage chapters S A D W C I L H R, Z_synthesis, front matter, intros
  cards/       one file per paper (instrument appendices sit inside their parent card)
  digest.tex   master document;  build_digest.py  citation anchoring and builds
  registry.json  the 100 papers;  candidates.md  literature worth adding
  tools/       blocks.py (paper text), ocr_pdf.py, package.py
  build/       output (git-ignored);  deliverables/ is what you open
```

## Next steps

1. Skim each stage chapter's implications box against the Decision Log and close or reword decisions D1 to D12.
2. Decide on the candidate literature in `candidates.md` (APA framework papers, Zimmeck APP-350, Cicchetti and Feinstein 1990 Part II, others).
3. Recreate the root `.venv` if you want to run `.\graphify.ps1 refresh` again (`python -m venv .venv`, then `.\.venv\Scripts\python.exe -m pip install -r requirements-graphify.txt`).
