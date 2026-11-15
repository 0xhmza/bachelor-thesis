# Validation sample, version 1

Draws the validation sample of Chapter 4 (Validation Sample, Agreement, and Error Estimates)
and computes the corrected estimates. Decision D9.

| File | Does |
|---|---|
| `design.py` | priority partition V1–V5, stratified draw with recorded seed and exact selection probabilities (the sampling manifest), difference estimator with stratified variance, joint misses from every stratum, Jeffreys intervals |
| `tests/test_design.py` | the constructed-corpus checks the methodology requires before use: repeated and single mentions, errors correlated within a policy, unequal selection probabilities, census of small strata, positivity |

Run `python -m pytest tests` (needs pytest and SciPy). The manifest of the real draw is
written at the freeze to `04_Study/4.7_Validation/validation_manifest.csv`; generated files
stay in `output/`, which is excluded from Git.
