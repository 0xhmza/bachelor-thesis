# literature_new

Tidy copy of the literature material: full texts, the methods-digest volumes and
their LaTeX sources. Nothing was downloaded; every file comes from this repository.
The originals stay where they are (`01_Literature/`), because scripts and the digest
build point at them.

| Folder | Contents |
|---|---|
| `references/` | 146 full-text PDFs, named `Author Year - Title.pdf`; index in `references index.csv` |
| `literature methodology analysis/` | The Methods Digest: `Methods Digest - Complete.pdf` and `by stage/` (nine stage volumes) |
| `literature methodology analysis/tex/` | LaTeX backup: `digest.tex`, `sections/`, `cards/`, `generated/`, `registry.json` |
| `zotero/` | `link-pdfs-in-zotero.js`, the script that links each PDF to a Zotero item |

## Notes

- Same-content files were merged (the seven loose copies in `01_Literature/PDFs/`
  duplicate numbered files), so 155 PDFs became 146 references.
- `04_Coding/74_Braun_2006_Using-thematic-analysis-in-psychology.pdf` is not Braun & Clarke;
  it is a two-page HAL paper on sexual health in women with lung cancer. It is left out here.
  The correct Braun & Clarke (2006) is the manuscript from `12_Additions`.
- Only `Stage 7 - LLM Feasibility.pdf` contains the 116-paper state; the other volumes (and
  the complete digest) still show the 99-paper state, as in `AI Literature Analysis/README.md`.
- `Methods Digest - Complete.pdf` (122 MB, over GitHub's 100 MB limit) and the Krippendorff 2019
  copy (private use only) are git-ignored; they exist on disk only.
- Rebuilding the digest: `01_Literature/Methods-Digest/HANDOFF.md`, section 3.
- The `tex/` copy keeps the relative layout, so it compiles in place; `build_digest.py`
  and the paper PDFs stay in `01_Literature/Methods-Digest/`.

## Zotero

Each PDF is attached to a Zotero item as a linked file (a pointer; Zotero storage is not
used). Run `zotero/link-pdfs-in-zotero.js` once: Zotero, Tools, Developer, Run JavaScript,
paste, Run. It reuses existing items (matched by DOI or title), creates the missing ones as
`document` items in the collection "Methodology literature", and is safe to run again. The
paths are absolute (`C:\Users\Hamza\Desktop\Share\Projects\bachelor-thesis\literature_new\references\`);
regenerate with `scripts/literature-new/v001/make_zotero_js.py` if the repo moves.
Created items carry title, year, DOI and authors from the digest registry; where only the
first author is known, the Extra field says so.

Built by `scripts/literature-new/v001/` (`catalogue.py`, `build.py`, `make_zotero_js.py`).
