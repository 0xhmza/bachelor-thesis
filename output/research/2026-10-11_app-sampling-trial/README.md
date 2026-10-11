# App sampling trial - 11 October 2026

Start with **report.pdf** or the editable **report.md**. This folder contains an
executed feasibility trial, not the frozen thesis sample. It preserves the
proposal's rating rule and records Play install counts as a separate measure.

## Contents

- `report.pdf`: professional report, findings, protocol, limitations and 50-row working set.
- `report.md`: editable report source, generated from the actual run.
- `config/protocol.json`: frozen rules, 19 keywords, country, ranking and proposal hash.
- `config/proposal_snapshot.tex`: proposal version used for this trial.
- `config/play_seeds.json` and `discovery_log.json`: provenance of the 24 Play feasibility seeds.
- `config/app_review.json`: provisional identity matches and explicit domain notes.
- `scripts/`: acquisition, offline parsing, selection, verification and reporting.
- `raw/20261011T135045038162Z/`: original responses, HTTP metadata, hashes and collection inputs.
- `processed/20261011T135045038162Z/`: candidate listings, screening, rankings, 50-app working set and empty final-sample register.
- `data_dictionary.md`: data semantics and interpretation rules.
- `qa/`: report-rendering previews and text checks.
- `bundle_manifest.json`: hashes of evidence, inputs, scripts, tables and report; an immutable derivation snapshot is also saved under `raw/`.

The 50-row `trial_working_set.csv` is **provisional**. Its rows have not passed
all eligibility checks, and seven cross-store identities are provisional.
`final_sample.csv` intentionally has a header and no rows. Apple API result
positions and Play web-discovery seeds are not the proposal's first 20 store-UI results.

## Reproduce from the saved capture (no network)

From this folder, using Python 3.11 or later:

```powershell
python -X utf8 scripts/process.py raw/20261011T135045038162Z
python -X utf8 scripts/sample_set.py raw/20261011T135045038162Z
python -X utf8 scripts/verify.py raw/20261011T135045038162Z
python -X utf8 scripts/build_report.py raw/20261011T135045038162Z
```

The first three commands use only Python's standard library. Report generation
also needs `reportlab` and the Windows Arial font files; the QA rendering uses
PyMuPDF. These packages were already available in the execution environment.
JSON is the canonical structured representation. CSV exports are UTF-8 with a
BOM for convenient spreadsheet import; cells beginning with formula characters
are escaped in CSV, without changing the JSON values.

## Collect a fresh dated trial

```powershell
python -X utf8 -u scripts/collect.py
```

This creates a new append-only raw directory and prints its path. Use that path
with the offline commands. The live script uses the existing frozen inputs;
edit a copied/versioned protocol for a new design rather than overwriting the
old one. Each run copies its collection inputs and scripts. Do not rerun
`initialize.py` or `prepare_review.py` over this trial: they deliberately refuse
to replace frozen files.

Optional policy reachability trial for an already processed capture:

```powershell
python -X utf8 -u scripts/check_policies.py raw/20261011T135045038162Z
```

Every call creates a new raw policy-check directory. HTTP 200 is a transport
result, not a decision that the page is the relevant, readable privacy policy.
The displayed policy CSV references the most recent check.

## Completing the study sample

Use `required_store_UI_sessions.csv` to record the 38 prescribed store searches,
and `manual_review_register.csv` to record evidence for eligibility. The latter
is a review worksheet; it is not automatically ingested. Transfer reviewed,
evidence-backed decisions to a versioned `config/app_review.json`. Set
`discovery_complete` only after the complete search frame and its linkage to
listings have been verified. Never set all flags merely to populate a sample.

Then rerun processing/selection and retain the decision-file hash. Keep both
store listings for matched apps; verify counterparts even if only one was
discovered. The trial's rank can change when missing counterparts or duplicate
products are resolved. Implement walkthrough and validation selection only
after the document sample is frozen.

## Preservation

Raw responses are ignored by Git through this folder's `.gitignore`; back up
the **whole folder**, including raw data, separately. This self-contained trial
folder is an explicitly documented organizational exception to the normal
`05_Data/raw/` location. Raw bytes are append-only and never edited. Derived
files can be regenerated. The original proposal and sampling protocol were
not changed. No accounts, installs, payments or personal health inputs were
used. No review endpoint was queried; complete product-page HTML may contain
the store's embedded review previews, which are not extracted or analysed.
