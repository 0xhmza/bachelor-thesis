# Bachelor's Thesis — Privacy Harm Communication in Fitness and Health Tracking Apps

**Author:** Hamza · **Programme:** B.Sc. IT-Sicherheit / Informationstechnik, RUB
**Advisor:** Kavous Salehzadeh Niksirat (MPI-SP) · **Semester:** WiSe 2026/27

---

## Folder map

| Folder | What lives here |
|---|---|
| `00_Admin/` | Meeting notes, supervisor input, timeline, the official thesis offer. Start here. |
| `01_Literature/` | Papers (`PDFs/`), reading notes (`Notes/`), reading-list tracker. |
| `02_Proposal/` | **LaTeX proposal**, in two versions — see below. Open `proposal_short.tex` or `proposal.tex` in TeXstudio. |
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

## Two versions of the proposal

| File | Pages | What it is |
|---|---|---|
| `02_Proposal/proposal_short.pdf` | **4** | **The hand-in.** The supervisor asked for four pages. |
| `02_Proposal/proposal.pdf` | 25 | The full record. Every decision in the short version is argued here at length, with ten points listed for the supervisor's confirmation. The thesis methodology chapter is written from this one, not from the short version. |

They are separate `.tex` files and share `_shared/references.bib`. **When a
decision changes, change it in both.** The short version carries a hard
four-page constraint: after editing it, recompile and check the page count. If
it spills onto a fifth page, cut content — do not shrink the margins or the
font.

```bash
.uild.ps1 proposal-short
```

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

See `00_Admin/Timeline.md`. The proposal is written and compiles
(`02_Proposal/proposal.pdf`, 23 pages). What is left before it goes to the
advisor:

1. **Fill the two title-page placeholders** in `02_Proposal/proposal.tex`:
   `\matriculation` and `\supervisorone` (the RUB examiner). They print as
   `TODO: ...` on the title page until you do. The same two are also in
   `03_Thesis/config/metadata.tex`, along with place of birth, second examiner,
   chair and submission date.
2. **Read §7 of the proposal, *Open Points for Confirmation*.** It lists ten
   decisions the proposal makes on your behalf so that work could proceed —
   scope, harm taxonomy, "highest rated", sample size, walkthrough subsample,
   ads, language, second coder, model choice, ethics. Take that list to the next
   meeting and close them.
3. **Set up the shared Google Doc** for the advisor (still open from 2026-09-04).
4. **Read the three harm papers** in `01_Literature/PDFs/` end to end — Citron &
   Solove (taxonomy), Knabenhans et al. (harm model), Martin et al. (PET
   framing). The proposal uses all three; you need to be able to defend that use.
5. **Get the ethics answer in writing** before any collection starts, and file it
   in `04_Study/Ethics/`.
6. After approval and registration: sampling per
   `04_Study/App-Sample/sampling_protocol.md`, then the pilot.

The literature search the advisor asked for has had its first pass: 17 verified
entries were added to `_shared/references.bib` on 2026-09-18, covering privacy
harms, health-tracker security and privacy, and methods. Keep adding to it — the
thesis needs a related-work chapter, not just a proposal's worth of citations.
