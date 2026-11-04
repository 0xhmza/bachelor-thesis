# Google Docs export (v001)

Generates `documents.batchUpdate` request lists that fill the thesis Google Doc
from the review copy (`03_Thesis/Thesis_Review-Copy.docx`, built by
`scripts/build_review_docx.py`). Used only when editing the Google Doc is asked
(see AGENTS.md, "Google Doc").

1. `pandoc Thesis_Review-Copy.docx -t json -o review.json`
2. `python gdocs_export.py plan review.json` lists tabs and call counts.
3. `python gdocs_export.py build review.json <key> <tabId> <prefix> --max 26000`
   writes call files (send them in order, first call = end of tab).
4. `python gdocs_export.py check review.json <key> <read_doc.json> <tabId>` compares text.
5. `python runin.py <read_doc.json>` emits bold requests for run-in headings.

`tabids.json` maps tab keys to the tab IDs of the live doc.
