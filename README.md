# Bachelor's Thesis — Privacy Harm Communication in Fitness and Health Tracking Apps

**Author:** Hamza · **Programme:** B.Sc. IT-Sicherheit / Informationstechnik, RUB
**Advisor:** Kavous Salehzadeh Niksirat (MPI-SP) · **Semester:** WiSe 2026/27

---

## Folder map

| Folder | What lives here |
|---|---|
| `00_Admin/` | Meeting notes, supervisor input, timeline, the official thesis offer. Start here. |
| `01_Literature/` | Papers (`PDFs/`), reading notes (`Notes/`), reading-list tracker. |
| `02_Proposal/` | **LaTeX proposal.** Open `proposal.tex` in TeXstudio. |
| `03_Thesis/` | **LaTeX thesis.** Open `thesis.tex` in TeXstudio. |
| `04_Study/` | App sample, codebook, LLM prompts, ethics, survey instrument. |
| `05_Data/` | `raw/` (untouched, gitignored), `processed/`, `analysis/`. |
| `06_Presentation/` | Beamer slides for the proposal talk and the defence. |
| `_shared/` | `references.bib` — **the single bibliography** for all three documents. |
| `99_Archive/` | Application-phase material. Not part of the thesis. |

Every folder above carries its own `README.md` with the rules that apply inside it.

---

## Getting started in TeXstudio

### 1. TeX distribution — already installed
Two distributions are present on this machine:

- **TeX Live 2025** — `C:\texlive\2025\bin\windows`  ← all three documents were
  test-compiled with this one
- **MiKTeX** — `C:\Users\Hamza\AppData\Local\Programs\MiKTeX\miktex\bin\x64`

Neither is on the system `PATH`. TeXstudio normally finds one anyway; if it
complains that `pdflatex` or `biber` cannot be found, either add the TeX Live
path above to `PATH`, or set the absolute paths in
`Options → Configure TeXstudio → Commands`.

To compile from a terminal, put TeX Live on `PATH` for that session first:

```bash
export PATH="/c/texlive/2025/bin/windows:$PATH"
```

### 2. Configure the build chain (once)
`Options → Configure TeXstudio → Build`:

- **Default Compiler:** `PdfLaTeX`
- **Default Bibliography Tool:** `Biber` ← important, not BibTeX
- **Build & View:** `Compile & View`

`Options → Configure TeXstudio → Commands`: leave the defaults unless
`biber` is not found, in which case point it at your MiKTeX `biber.exe`.

### 3. Open a document
Open `02_Proposal/proposal.tex` and press **F5** (Build & View).

The first run will pull in packages — let MiKTeX install them. If citations show
as `[?]`, run the full cycle once: **F6** (compile) → **F8** (bibliography) →
**F6** → **F6**. TeXstudio's F5 usually handles this on its own after the first time.

### 4. Set the root document
When editing a file in `sections/` or `chapters/`, tell TeXstudio which file is the
master: `Options → Root Document → Set Current Document As Explicit Root`
(do this with `proposal.tex` / `thesis.tex` open). Otherwise F5 tries to compile
the fragment you are editing and fails.

---

## Working rules

**Bibliography.** One file: `_shared/references.bib`. All three documents point at
it with a relative path. Never create a second `.bib`.

**Citation style.** Currently `numeric-comp`. To switch, change the one
`\usepackage[...]{biblatex}` line in `02_Proposal/proposal.tex` and
`03_Thesis/config/preamble.tex`. `style=apa` needs the `biblatex-apa` package.

**TODOs.** Every stub uses `\todo{...}`, which renders in red. Before submitting:

```bash
grep -rn "todo{" 02_Proposal 03_Thesis 06_Presentation
```

That command must return nothing.

**Metadata.** Edit `03_Thesis/config/metadata.tex` and the `\newcommand` block at
the top of `02_Proposal/proposal.tex`. Nowhere else.

**Figures.** Generate them from scripts in `05_Data/analysis/` that write directly
into `03_Thesis/figures/`. Never hand-edit a figure you will need to regenerate.

**Git.** Commit after every writing session. `build/` and `05_Data/raw/` are ignored.

---

## Next actions

See `00_Admin/Timeline.md`. From the 2026-09-04 meeting and the advisor's written
input of 2026-09-05 (`00_Admin/Supervisor-Input/`):

1. Read the three harm papers now in `01_Literature/PDFs/` — Citron & Solove
   (taxonomy), Knabenhans et al. (harm model), Martin et al. (PET framing).
2. Run your own literature search on privacy harms, health-tracker security and
   privacy, and methods (privacy-policy analysis, cognitive walkthrough). The
   advisor asked for this explicitly — the sent papers are examples, not the review.
3. Set up the shared Google Doc for the advisor.
4. Confirm the scope question — the 2026-09-05 input points at document and
   interface analysis, but say so out loud at the next meeting
   (`00_Admin/Meeting-Notes/2026-09-04_Proposal-Meeting.md`, §8).
5. Fix the keyword list and inclusion criteria for the German app sample
   (→ `04_Study/App-Sample/sampling_protocol.md`).
6. Draft the proposal: background → research problem → why it matters → methodology.
