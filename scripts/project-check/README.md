# Project checks

Run `python scripts/check_project.py` from the project root. The entry point
selects v003. Each version can also be run directly from the root.

- **v001:** the original checker, preserved before changing its scope.
- **v002:** validates project Markdown while leaving `05_Data/raw/` collections
  untouched. Links from project documents **to** raw evidence are still checked.
  Vendored upstream READMEs inside ignored raw collections are not project
  documentation, and missing upstream files must not require editing raw data.
- **v003:** v002 plus a warning when the Zotero library file
  (`03_Thesis/references-zotero.rdf`) was built from another `references.bib`
  (compared by the SHA-256 recorded in the file's header, line endings ignored).

Tests: `python -m unittest discover -s scripts/project-check/v003/tests`
(v002: `.../v002/tests`).
