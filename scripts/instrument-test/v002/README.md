# Instrument test, version 2

Version 2 of the evaluator and the reference-model tables (Decision D12, update of
4 November 2026). Version 1 stays as it was: it produced the instrument test of
1 November 2026 that Chapter 5 and Appendix H report.

| What changed | Why |
|---|---|
| `evaluate.py` rejects OR+ instead of reading it like OR | Asking whether a pathway is possible does not make one input sufficient; every OR+ is stated as an OR of sufficient AND-combinations (submission review R4) |
| `build_reference.py` writes only the reference tables, from `reference_model_v2.yaml` | The instrument-test tables need the raw data of the test and describe the v1 test |
| `build_reference.py` re-evaluates the test app under model v2 | Records what the v2 rules change, without rewriting the original fixture |

| Step | Command | Result |
|---|---|---|
| Tables of Appendix G and the re-evaluation | `python build_reference.py <repo root>` | `03_Thesis/tables/reference-*`, `output/reevaluation_clue.{json,md}` |
| Test the evaluator and model v2 | `python -m pytest tests` | |

`output/` is excluded from Git. Needs PyYAML (and pytest for the tests).
