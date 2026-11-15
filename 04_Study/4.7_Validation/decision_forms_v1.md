# Decision forms: applicability and potential mismatch

**Version:** 1 · **Date:** 2026-11-04 · Part of the instrument bundle. Codebook v7,
reference model v2; D8, D12.

These decisions are made by people only. The second coder re-checks a random sample of
them, including decisions judged negative (no mismatch, not applicable).

## Applicability (one row per app and component)

| Field | Entry |
|---|---|
| App ID; component ID (reference model v2); decider; date | |
| State | present / absent / uncertain |
| Basis | `evidence` (the app's own sources) or `assumption` (an outside event, EX1–EX3, or an argued link) |
| Evidence | policy unit, listing field or walkthrough screen, with location |
| Reason | one sentence |
| Incapability components only (IM11–IM14) | routes checked: in the app / by request to the provider / other; a missing in-app control alone is no evidence |

Pathway states follow from the components by `04_Study/4.7_Validation/scripts/instrument-test/v002/evaluate.py`.

## Potential mismatch (`C-MIS`, one row per claim and pathway in its scope)

| Field | Entry |
|---|---|
| App ID; claim ID and unit; pathway ID; decider; date | |
| Claim as written: measure, actor, data, outcome, conditions, strength | |
| Is the pathway within the claim's scope? | yes / no / unclear, with reason |
| Components the measure removes, if it works as claimed | |
| Pathway state after removal (`after_measure`) | absent / still open / uncertain |
| Decision | potential mismatch / no mismatch / not assessable |
| Explanation | which necessary condition the measure misses |
