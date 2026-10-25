# Bachelor's thesis — Privacy Harm Communication in Health Tracking Apps

Author: Hamza Sghaier · RUB · Advisor: Kavous Salehzadeh Niksirat, MPI-SP

## Main document

Work in `03_Thesis/thesis.tex` and its `chapters/` and `appendix/` fragments.
The 5 October 2026 proposal is integrated into the main thesis: abstract,
introduction, background, related work, methodology and Appendix D. Its original
source and PDF remain in `03_Thesis/proposal/` as a historical submission snapshot.
The existing CycleMate worked example remains in Appendix A.

The methodology marks the revisions required by the supervisor meeting of
13 October. Empirical results, final conclusions and personal submission metadata
remain unfinished.

```powershell
.\build.ps1 thesis       # main thesis; latexmk handles pdflatex and biber
.\build.ps1 proposal     # historical proposal snapshot
.\build.ps1 slides
```

TeX Live 2025 is installed; `build.ps1` adds its binary folder to the current
session. Each document's `latexmkrc` defines its build chain. In TeXstudio open
`thesis.tex` as the root document; in VS Code open `03_Thesis/` and use the
LaTeX Workshop settings there. The shared bibliography is `_shared/references.bib`.

## For the supervisor: review copy

`03_Thesis/Thesis_Review-Copy.docx` is a Word version of the current thesis draft
for comments and tracked changes. It is generated from the LaTeX sources and rebuilt
with **every commit that changes the thesis**, so the copy in the repository always
matches the committed draft; the box on its first page names that commit. Citation
numbers link to the bibliography, and bibliography entries link to their DOI or URL.
Save an annotated copy under a new name and send it back: the next commit replaces
this file. `thesis.pdf` remains the authoritative layout (diagrams appear in the
Word copy as text descriptions).

## Working routine

```powershell
sh scripts/hooks/install.sh                 # once per clone: review-copy hook
python scripts/check_project.py             # citations, links, reading rule, TODOs
python scripts/build_review_docx.py         # review copy now (the hook does it on commit)
.\graphify.ps1 refresh                      # graph, literature index, map, reading tracker
```

- **Decisions** are recorded in `00_Admin/Decision-Log.md` before the methodology states them.
- **Progress** goes into `00_Admin/Weekly-Log.md`; risks into `00_Admin/Risk-Register.md`.
- **Reading status** is edited in `01_Literature/reading-status.csv` (the README table follows it).
- **CI** (`.github/workflows/ci.yml`) runs the checks, builds the review copy and compiles
  the thesis on every push; download both from the run's artifacts.

## Folder map

| Folder | Content |
|---|---|
| `00_Admin/` | Supervisor input, meeting notes, action plan, decision log, risk register, weekly log, timeline |
| `01_Literature/` | Core reading list with PDFs and notes, the ranked methodology corpus (89 of 93 works as PDFs), the reading tracker, the abstract index and the interactive literature map. Start at its `README.md` |
| `03_Thesis/` | Main thesis, chapters, appendices, the supervisor's review copy (.docx) and the proposal snapshot |
| `04_Study/` | Sampling protocol, codebook versions, walkthrough and LLM prompts |
| `05_Data/` | Raw, processed and analysis study material; raw data is gitignored |
| `06_Presentation/` | Beamer presentation |
| `_shared/` | Single bibliography |
| `99_Archive/` | Application material and compact cleanup recovery archive |
| `scripts/` | Graphify integration (LaTeX/BibTeX structure, literature layer), review-copy builder, project checks, git hooks |
| `.github/` | CI: checks, review copy and thesis PDF on every push |
| `graphify-out/` | Queryable graph, report, HTML and freshness information |

Read the relevant folder README before changing study records. Research trials
are historical evidence; preserve their source data and manifests.

## Graphify for LLM navigation

Graphify 0.9.90 is installed in the ignored project `.venv/`. Its Codex skill is
installed in the user's skill folder; `AGENTS.md` directs assistants to scoped
queries. The wrapper uses the project interpreter without changing global PATH.

```powershell
.\graphify.ps1 query "blind validation and missed mentions" --budget 1200
.\graphify.ps1 explain "RQ3"
.\graphify.ps1 refresh
```

To recreate the local environment:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-graphify.txt
.\.venv\Scripts\python.exe -m graphify install --platform codex
.\graphify.ps1 refresh
```

The graph combines Graphify's code AST and semantic extraction with local
LaTeX/Markdown structure, citations, bibliography entries and literature file names.
Graphify does not natively detect `.tex`/`.bib`, so the project integration handles
those formats. Refresh updates structural information locally and reuses semantic
fragments only while their source hashes match. Changed semantic sources are listed
for re-extraction using the Graphify skill; no API key is required for assistant extraction.

The methodology literature corpus is indexed from its catalogue and download manifest
on every refresh, so it never goes semantically stale: each of the 93 works becomes a
node with its topic, method stage, research question, local PDF and any download gap,
alongside the reading guide's meeting-decision map. Paper full text is not indexed;
the abstract and keywords printed on each local PDF's title page are
(`scripts/literature_index.py`, cached by file hash in
`01_Literature/literature-index.json`), together with each work's reading status, so
queries such as "which agreement-statistics papers are still to read" work. The same
refresh writes `01_Literature/Literature-Map.html`, an interactive map of thesis
chapters, cited works, the corpus, meeting decisions and reading status.

`.graphifyignore` excludes generated files, archives, duplicate proposal content,
raw/processed trial data and full PDF text. Original literature is reached through
its file and bibliography nodes; open a paper when needed for evidence. Query with a
small budget and then read the located passage. Actual token savings depend on the
question and were not measured against a real assistant baseline.

## Cleanup recovery

The retired `_junk/` folder, sync conflicts and temporary build/review files are
removed from the active project. Source/PDF recovery is stored in
`99_Archive/2026-10-14_cleanup-recovery.zip`; full removed folders/files are kept in
the adjacent `../bachelor-thesis-cleanup-20261014/` because permanent deletion was
blocked by automatic approval review.
