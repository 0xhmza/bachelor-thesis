# Project checks

Run `python scripts/check_project.py` from the project root. The entry point
selects v002. Each version can also be run directly from the root.

- **v001:** the original checker, preserved before changing its scope.
- **v002:** validates project Markdown while leaving `05_Data/raw/` collections
  untouched. Links from project documents **to** raw evidence are still checked.
  Vendored upstream READMEs inside ignored raw collections are not project
  documentation, and missing upstream files must not require editing raw data.

Tests: `python -m unittest discover -s scripts/project-check/v002/tests`.
