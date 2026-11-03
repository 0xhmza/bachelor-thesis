# Sampling audit v001

Run `python scripts/sampling-audit/v001/audit.py` from the project root.
Python standard library only; no network requests.

The audit checks the archived App Store v007 and Google Play v004 collections,
screening keys, selected listing prices/counts, developer uniqueness, final
cache and progress log, calibration, and the complete ranking v003 replay.
The replay redirects all output and generated table paths into this version's
`output/`. SHA-256 checks confirm the original inputs and outputs are unchanged.

Artifacts in the ignored `output/` directory:

- `audit.json`: checks, data-quality findings, source hashes and counterfactuals.
- `main-cascade.csv`: all 70 reached candidates and their selection outcomes.
- `matched-listings.csv`: the 123 matched pairs, with both identities visible.
- `missing-play-review-counts.csv`: missing fields distinguished from explicit zeros.
- `replayed-v003/` and `replayed-app-sample.tex`: isolated production replay.

The five identity reference cases use distinct product names and IDs from the
archived listings. The screening scenarios are hypothetical: especially Lady
Pill Reminder requires an author decision about recorded intake versus a
calculated schedule. No screening decision, matching config, sample, or thesis
result is changed. Passing replay checks establish reproducibility, not valid
app identities or correct eligibility judgments. A successful audit invocation
can therefore still report serious issues in `audit.json`.
