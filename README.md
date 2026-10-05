# Bachelor's Thesis — Privacy Harm Communication in Fitness and Health Tracking Apps

**Author:** Hamza · **Programme:** B.Sc. IT-Sicherheit / Informationstechnik, RUB
**Advisor:** Kavous Salehzadeh Niksirat (MPI-SP) · **Semester:** WiSe 2026/27

---

## Folder map

| Folder | What lives here |
|---|---|
| `00_Admin/` | Meeting notes, supervisor input, timeline, the official thesis offer. Start here. |
| `01_Literature/` | Papers (`PDFs/`), reading notes (`Notes/`), reading-list tracker. |
| `03_Thesis/` | **LaTeX thesis** — open `thesis.tex` in TeXstudio. Its subfolder `proposal/` holds **the proposal**, the first kernel of the thesis: a four-page paper for the supervisor (`proposal/proposal.tex`). |
| `04_Study/` | App sample, codebook, LLM prompts, ethics, survey instrument. |
| `05_Data/` | `raw/` (untouched, gitignored), `processed/`, `analysis/`. |
| `06_Presentation/` | Beamer slides for the proposal talk and the defence. |
| `_shared/` | `references.bib` — **the single bibliography** for all three documents. |
| `99_Archive/` | Application-phase material, and `_junk/` — the retired long proposal (`02_Proposal/`). Not part of the thesis. |

Every folder above carries its own `README.md` with the rules that apply inside it.

---

## Getting started

### 1. TeX distribution — already installed
Two distributions are present on this machine:

- **TeX Live 2025** — `C:\texlive\2025\bin\windows` — **on the user `PATH`**, and
  the one every document is compiled with
- **MiKTeX** — `C:\Users\Hamza\AppData\Local\Programs\MiKTeX\miktex\bin\x64` —
  installed but deliberately *not* on `PATH`, so that only one distribution and
  one package set is ever used

Check it with `latexmk -v`. If that fails, add `C:\texlive\2025\bin\windows` to
your user `PATH` and open a new terminal.

### 2. The build chain — defined once, in `latexmkrc`
Every document folder (`03_Thesis/proposal/`, `03_Thesis/`, `06_Presentation/`) carries a
`latexmkrc` that pins the chain:

    pdflatex -> biber -> pdflatex -> pdflatex      (output in place)

`biber` is never listed anywhere: `latexmk` reads the `.bcf` file and inserts the
bibliography pass by itself. **Change the build here and nowhere else** — not in
`build.ps1`, not in an editor profile.

From a terminal, inside any document folder:

```powershell
latexmk            # builds the document(s) of that folder
latexmk -pvc       # watch the sources and rebuild on every save
latexmk -c         # drop auxiliary files, keep the PDF
```

Or build everything from the repository root:

```powershell
.\build.ps1            # all four documents
.\build.ps1 thesis     # just the thesis
```

### 3. TeXstudio
`Options → Configure TeXstudio → Build`:

- **Default Compiler:** `PdfLaTeX`
- **Default Bibliography Tool:** `Biber` ← important, not BibTeX
- **Build & View:** `Compile & View`

`Options → Configure TeXstudio → Commands`: leave every path on its default now
that TeX Live is on `PATH`. If TeXstudio still cannot find a tool, it is holding
on to a stale environment — restart it.

### 4. Open a document
Open `03_Thesis/proposal/proposal.tex` and press **F5** (Build & View).

TeXstudio finds the distribution on its own now. If citations show as `[?]`, run
the full cycle once: **F6** (compile) → **F8** (bibliography) → **F6** → **F6**.

### 5. Set the root document
When editing a file in `sections/` or `chapters/`, tell TeXstudio which file is the
master: `Options → Root Document → Set Current Document As Explicit Root`
(do this with `proposal.tex` / `thesis.tex` open). Otherwise F5 tries to compile
the fragment you are editing and fails.

### 6. VS Code (LaTeX Workshop)
Open a **document folder** (`03_Thesis`), not a single file — the folder's
`.vscode/settings.json` holds the toolchain definition. The settings JSON is
documented inline; the short version:

| Action | How |
|---|---|
| Build | `Ctrl+Alt+B`, or just save a `.tex` file (build-on-save) |
| View PDF | `Ctrl+Alt+V` — `Ctrl+Click` in the PDF jumps back to the source |
| Other recipe | *LaTeX Workshop: Build with recipe* → `pdflatex -> biber -> pdflatex x2` |
| Clean | *LaTeX Workshop: Clean up auxiliary files* — never touches `thesis.pdf` |
| Format | `Shift+Alt+F` (runs `latexindent`; leaves a git-ignored `indent.log`) |
| Build everything | `Ctrl+Shift+B` → *LaTeX: build all documents* (wraps `build.ps1`) |

Only `03_Thesis/` has a `.vscode/settings.json`. The other folders work with
LaTeX Workshop's defaults, because their `latexmkrc` defines the same chain.

**One limitation.** `_shared/references.bib` sits *outside* the `03_Thesis` folder,
and VS Code cannot watch files outside the workspace. After editing the
bibliography, either save any `.tex` file or press `Ctrl+Alt+B` to pick it up.

---

## The proposal

`03_Thesis/proposal/proposal.tex` → `proposal.pdf` is **the hand-in**: the first
kernel of the thesis, written as a paper (ACM two-column layout, no ACM
boilerplate) and holding only what the supervisor asked for — Background,
Research Problem, Why the Problem Is Important, Methodology — plus the RQ and
scope from his written input of 2026-09-05.

The supervisor originally asked for three pages; the approved length is now
**four pages of content**, then the reference list (page 5, not counted) and
one appendix page with a worked example. After any edit, recompile and check. If the text spills, cut content — do not shrink the font or
the margins.

```powershell
.\build.ps1 proposal
```

The former two-version proposal (4-page short, 25-page long) is retired to
`99_Archive/_junk/02_Proposal/`. It still compiles and is the source to mine when
the thesis chapters are written: the long version argues every methodological
decision in full, and holds the schedule and the ten points for confirmation
(their current state is in `00_Admin/Timeline.md` and
`00_Admin/Open-Points.md`).

---

## Working rules

**Bibliography.** One file: `_shared/references.bib`. All three documents point at
it with a relative path. Never create a second `.bib`.

**Citation style.** Currently `numeric-comp`. To switch, change the one
`\usepackage[...]{biblatex}` line in `03_Thesis/proposal/proposal.tex` and
`03_Thesis/config/preamble.tex`. `style=apa` needs the `biblatex-apa` package.

**TODOs.** Every stub uses `\todo{...}`, which renders in red. Before submitting:

```bash
grep -rn "todo{" 03_Thesis 06_Presentation
```

That command must return nothing.

**Metadata.** Edit `03_Thesis/config/metadata.tex` and the `\author` /
`\affiliation` block of `03_Thesis/proposal/proposal.tex`. Nowhere else.

**Figures.** Generate them from scripts in `05_Data/analysis/` that write directly
into `03_Thesis/figures/`. Never hand-edit a figure you will need to regenerate.

**Git.** Commit after every writing session. Auxiliary files and `indent.log` are
ignored; the compiled `*.pdf` files, the `latexmkrc` files and the `.vscode/`
LaTeX Workshop settings **are** tracked, so a fresh clone builds the same way the
editor does. `05_Data/raw/` is ignored.

---

## Next actions

See `00_Admin/Timeline.md`. The proposal is written and compiles
(`03_Thesis/proposal/proposal.pdf`, four pages of content plus references and
a one-page appendix).
What is left before it goes to the advisor:

1. **Read it once more, on paper**, and check the author block in
   `03_Thesis/proposal/proposal.tex` (name, affiliation) is what you want the
   supervisor to see. Matriculation number, examiners, chair and submission date
   belong in `03_Thesis/config/metadata.tex`, not in the proposal.
2. **Read `00_Admin/Open-Points.md`.** It lists the decisions the proposal makes
   on your behalf so that work could proceed — scope, harm taxonomy, "highest
   rated", sample size, walkthrough subsample, second coder, ethics. Take that
   list to the next meeting and close them.
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
