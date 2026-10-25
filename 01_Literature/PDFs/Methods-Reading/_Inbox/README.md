# Inbox for hand-saved PDFs

Save PDFs you obtained yourself (browser, library login, author copy) here, then run
the importer (`import_manual.py`), which was removed on 25 October 2026 and is in Git history; file new PDFs by hand.
Each file is matched to a missing catalogue entry, validated, moved into its topic folder and
the checklist is regenerated. Files that cannot be identified stay here; for scans without a
text layer use `--assume <catalogue ID>` (IDs are listed in `download-status.json`).
