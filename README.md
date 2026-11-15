# Bachelor's thesis — Privacy Harm Communication in Health Tracking Apps

Author: Hamza Sghaier · RUB · Advisor: Kavous Salehzadeh Niksirat, MPI-SP

## Main document

`03_Thesis/thesis.tex` with its `chapters/` and `appendix/` fragments. The proposal
of 5 October 2026 is integrated (abstract, introduction, background, related work,
methodology, Appendix D); its source and PDF stay in `03_Thesis/proposal/` as a
snapshot. The CycleMate worked example is in Appendix A. The methodology marks the
revisions from the supervisor meeting of 13 October; results beyond the sample,
conclusions and submission metadata are unfinished.

```powershell
.\build.ps1 thesis       # main thesis; latexmk runs pdflatex and biber
.\build.ps1 proposal     # proposal snapshot
.\build.ps1 slides
```

`build.ps1` adds TeX Live 2025 to the session; each document's `latexmkrc` defines
its chain. TeXstudio: open `thesis.tex` as root; VS Code: open `03_Thesis/` (LaTeX
Workshop settings there). Bibliography: `03_Thesis/references.bib`.

## Review copy for the supervisor

`03_Thesis/Thesis_Review-Copy.docx` is generated from the LaTeX sources by the
pre-commit hook on every commit that changes the thesis; the box on its first page
names that commit. Citation numbers link to the bibliography, entries to their DOI
or URL; diagrams appear as text descriptions. Annotated copies come back under a
new name, because the next commit replaces the file. `thesis.pdf` is the
authoritative layout.

## Working routine

```powershell
sh scripts/hooks/install.sh                 # once per clone: review-copy hook
python scripts/check_project.py             # citations, links, reading rule, TODOs
python scripts/build_review_docx.py         # review copy now (the hook does it on commit)
.\graphify.ps1 refresh                      # graph, literature index, map, reading tracker
```

Decisions go into `00_Admin/Decision-Log.md` before the methodology states them;
progress into `00_Admin/Weekly-Log.md`, risks into `00_Admin/Risk-Register.md`;
reading status into `01_Literature/catalog/reading-status.csv`. CI
(`.github/workflows/ci.yml`) runs the checks, builds the review copy and compiles the
thesis on every push (artifacts of the run). Agent rules: [AGENTS.md](AGENTS.md).

## Folder map

| Folder | Content |
|---|---|
| `00_Admin/` | Supervisor input, meeting notes, correspondence, action plan, decision log, risk register, weekly log, timeline |
| `01_Literature/` | `library/` (every full text, flat, `Author_Year_ShortTitle.pdf`), `notes/`, `catalog/` (reading tracker, methods corpus, generated index and map), `review/` (literature review) and `digest/` (Methods Digest); start at its `README.md` |
| `03_Thesis/` | Main thesis, chapters, appendices, bibliography (`references.bib`, Zotero file), review copy, proposal snapshot |
| `04_Study/` | Sampling protocol and app sample, codebook versions, walkthrough protocol, LLM prompts, ethics |
| `05_Data/` | Raw, processed and analysis material; raw data is git-ignored |
| `06_Presentation/` | Beamer presentation |
| `99_Archive/` | Application material and the cleanup recovery archive |
| `scripts/` | Collectors, ranking, graph integration, review-copy builder, project checks, git hooks |
| `.github/` | CI |
| `graphify-out/` | Queryable graph, report, HTML, freshness information |

Read a folder's README before changing study records; research trials are
historical evidence.

## Graphify

Graphify 0.9.90 runs from the git-ignored `.venv/`; the wrapper uses that
interpreter without changing PATH.

```powershell
.\graphify.ps1 query "blind validation and missed mentions" --budget 1200
.\graphify.ps1 explain "RQ3"
python -m venv .venv                                              # recreate the environment
.\.venv\Scripts\python.exe -m pip install -r requirements-graphify.txt
.\.venv\Scripts\python.exe -m graphify install --platform codex
```

The graph combines Graphify's code AST and semantic extraction with the project's
own LaTeX/Markdown structure, citations, bibliography entries and literature file
names (Graphify does not detect `.tex`/`.bib`). Semantic fragments are reused only
while their source hash matches; changed sources are listed for re-extraction with
the Graphify skill. The 93 corpus works are indexed on every refresh from the
catalogue and download manifest (topic, stage, research question, PDF, download
gap, reading status) plus the abstract and keywords from each PDF's title page
(`scripts/literature_index.py`, cached in `01_Literature/catalog/literature-index.json`);
full text is not indexed. The refresh also writes `01_Literature/catalog/Literature-Map.html`.
`.graphifyignore` excludes generated files, archives, duplicate proposal content,
raw/processed data and PDF text. Token savings were not measured.

## Cleanup recovery

The retired `_junk/` folder, sync conflicts and temporary files were removed on
14 October 2026; source and PDF recovery is in
`99_Archive/2026-10-14_cleanup-recovery.zip`, full removed folders in the adjacent
`../bachelor-thesis-cleanup-20261014/`. The superseded `output/` research folder
was removed on 25 October 2026 (in Git history; its git-ignored raw data was lost,
see `00_Admin/Risk-Register.md` R9) and later restored from Git as the historical
evidence it is.

On 30 October 2026 the stale duplicate `01_Literature/.tex/`, the `#_Junk_Backup/`
folder, the second copy of the digest volumes in `01_Literature/PDFs/AI Literature
Analysis/`, 155 sync and cloud conflict copies, LaTeX intermediates, bytecode
caches and the scratch folder `tmp/` were removed. Everything tracked is in
Git up to commit `f50e097`; what Git did not hold and was not provably a duplicate
went to the adjacent `../bachelor-thesis-cleanup-20261030/` (`manifest.json` lists
every file moved or deleted).

On 2 November 2026 the same folders were back, most likely through Syncthing, which also
syncs `.git`, along with 190 new conflict copies. They, Git's interrupted leftovers,
`tmp/`, unused literature tables and LaTeX intermediates went to the adjacent
`../bachelor-thesis-cleanup-20261102/` (`manifest.json` lists every item). Nothing
was deleted. `digest - Copy.pdf` stays, as `01_Literature/digest/HANDOFF.md` asks.

On 5 November 2026 `01_Literature/` was reorganised into `library/`, `notes/`, `catalog/`, `review/` and `digest/`;
the 761 MB `literature_new/` copy, all byte-identical duplicate PDFs and the generated checklist, HTML and DOI list were
removed (old -> new table: `scripts/literature-reorg/v001/mapping.csv`). If Syncthing brings an old folder back, delete it
on the other device first.
