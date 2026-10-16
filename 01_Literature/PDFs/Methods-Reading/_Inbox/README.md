# Inbox for hand-saved PDFs

Save PDFs you obtained yourself (browser, library login, author copy) here, then run
`.venv/Scripts/python.exe output/research/2026-10-14_methodology-literature/import_manual.py`.
Each file is matched to a missing catalogue entry, validated, moved into its topic folder and
the checklist is regenerated. Files that cannot be identified stay here; for scans without a
text layer use `--assume <catalogue ID>` (IDs are listed in `download-status.json`).
