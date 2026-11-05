# literature-reorg v001 (5 November 2026)

One-off reorganisation of `01_Literature/` into `library/`, `notes/`, `catalog/`, `review/`, `digest/`
(layout and naming rules: `01_Literature/README.md`).

| File | Role |
|---|---|
| `names.py`, `plan.py` | Name rules and the plan: one library file per distinct PDF (SHA-256), `Author_Year_ShortTitle.pdf` |
| `apply.py` | Moved the files (resumed by hand after a case-insensitive `Notes`/`notes` clash on Windows) |
| `rewrite_refs.py` | Rewrote paths and relative Markdown links in the repository; earlier script versions were left as they were |
| `mapping.csv` | Old path -> new path for every PDF and moved document (empty `new` = dropped) |
| `relink_zotero.py` | Updates Zotero's linked-file paths from `mapping.csv`. **Not run by the assistant**: Zotero lives on your PC and must be closed |

Dropped on purpose: exact duplicates (same SHA-256), the `.tex` and `#_Junk_Backup` copies, the generated
`Download-Checklist.md`, `Methods-Reading-List.html` and `ranked-dois.txt`, and one wrong file
(`74_Braun_2006_...pdf`, a two-page HAL document, not Braun & Clarke; the correct manuscript is in the library).
