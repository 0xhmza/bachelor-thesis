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

Every PDF is attached to exactly one Zotero item as a linked file (a pointer; Zotero storage is
not used). Done directly in `zotero.sqlite` by `scripts/literature-new/v002/repair.py` (Zotero
closed, backup made first). It replaced a first attempt (`v001`) that had created duplicates of
thesis items; do not run `v001/apply_links.py` again.

- 36 PDFs belong to items already in "Bachelor Thesis References" (matched by DOI, then title);
  they are linked there and no second item was created.
- Those thesis items now carry the full author lists from `_shared/references.bib` (18 had been
  cut short) and abstracts where the repository holds one (`literature-index.json`,
  `records.csv`). Titles, citation keys and the other fields were not changed.
- The other 109 PDFs became new items in the collection "Methodology literature" only, with type,
  venue, DOI, authors and abstract where known. 20 have only the first author (flagged in the
  Extra field); the full list would need a Crossref lookup, i.e. a download.
- 15 thesis items have no PDF in the repository (laws, web pages, software, and Calo 2011,
  Zimmeck 2019, Priem 2022, Kinney 2023, Bitkom 2025, Grinsted 2021).

The paths are absolute (`C:\Users\Hamza\Desktop\Share\Projects\bachelor-thesis\literature_new\references\`);
rerun `v002/repair.py` if the repository moves.

Built by `scripts/literature-new/v001/` (`catalogue.py`, `build.py`) and `v002/` (`match.py`,
`repair.py`).
