# Decisions

One row per methodological decision. The methodology states a rule only after it has a row
here. Full reasoning and evidence: `Archive/Decisions/Dnn_*.md` (linked in the last column).

Status: **open** · **proposed** (written, not yet confirmed) · **confirmed** / **decided** · **superseded**.

| ID | Topic | Rule | Status | Record |
|---|---|---|---|---|
| D1 | Sample size | 47 ranked + 3 preinstalled apps, no quotas | proposed; "why 50?" justification open | [D01](Archive/Decisions/D01_sample-size.md) |
| D2 | Ranking | One ranking of both stores by German-market popularity, no rating floor, one app per provider; sensitivity threshold 5 of 47 providers | proposed | [D02](Archive/Decisions/D02_ranking-and-rating-floor.md) |
| D3 | Scope and keywords | Keywords of Hutton 2018 and Malki 2024, EN + DE; eligibility E1a–E1d to E5 checked on the store listing | proposed; keyword tests and 3 must-include apps open | [D03](Archive/Decisions/D03_scope-keywords-function.md) |
| D4 | Payment | Free to install; payment is recorded and only limits walkthroughs | proposed | [D04](Archive/Decisions/D04_payment-access.md) |
| D5 | No privacy policy | App included, absence reported | confirmed 10-13 | [D05](Archive/Decisions/D05_apps-without-policy.md) |
| D6 | Preinstalled apps | Leading vendor per platform: Apple Health, Apple Fitness, Samsung Health | proposed | [D06](Archive/Decisions/D06_preinstalled-apps.md) |
| D7 | Language | English first, German fallback | confirmed 10-13 | [D07](Archive/Decisions/D07_language.md) |
| D8 | Two coders | Author codes all; an independent second coder codes the validation sample; Krippendorff's α | decided 11-04; name open | [D08](Archive/Decisions/D08_two-coder.md) |
| D9 | LLM role | Two models code all units; people check high-stakes labels blind; 500-unit stratified validation sample | decided 11-04 | [D09](Archive/Decisions/D09_llm-role.md) |
| D10 | Walkthrough | All 50 apps; tasks T1–T7; Android for dual-listed apps; ten-app second rating | closed 11-05 | [D10](Archive/Decisions/D10_walkthrough.md) |
| D11 | Devices | Apps only; companion apps are eligible | proposed (inside D3) | [D03](Archive/Decisions/D03_scope-keywords-function.md) |
| D12 | Harm-tree basis | One generic health tracker; reference model v2 | decided 11-04; refined by D23 | [D12](Archive/Decisions/D12_reference-model.md) |
| D13 | Literature search v1 | Staged search with citation filter | superseded by D21 | [D13](Archive/Decisions/D13_literature-review.md) |
| D14 | Literature search v2 | Venue listing, strands, screening rules | superseded by D21 | [D14](Archive/Decisions/D14_literature-review-v2.md) |
| D15 | Domain | One domain: health trackers; categories are search keywords only | confirmed 10-28 | [D15](Archive/Decisions/D15_health-tracker-domain.md) |
| D16 | Instrument test | One-app test (Clue) | superseded by D20 | [D16](Archive/Decisions/D16_instrument-test.md) |
| D17 | RQ4 surfaces | Privacy policy and inspected interface only | confirmed 11-04 | [D17](Archive/Decisions/D17_rq4-surfaces.md) |
| D18 | Reporting unit | Equal weight per app | decided 11-04 | [D18](Archive/Decisions/D18_reporting-unit.md) |
| D19 | Data release | Instruments, scripts, labels open; captured texts for examiners only; recordings private | proposed | [D19](Archive/Decisions/D19_data-release.md) |
| D20 | No pilot | Method applied to all apps as written; no pilot or development apps | confirmed 11-05 | [D20](Archive/Decisions/D20_no-pilot.md) |
| D21 | Literature review | Brief review, at most ten papers, no PRISMA | confirmed 11-06 | [D21](Archive/Decisions/D21_brief-literature-review.md) |
| D22 | Research questions | Full questions in the text; extra RQ and "RQ2 postponed" undecided | wording confirmed 11-06; set open | [D22](Archive/Decisions/D22_research-questions.md) |
| D23 | Harm trees | Built use case by use case; stop after two cases that add nothing | proposed 11-07 | [D23](Archive/Decisions/D23_use-case-subtrees.md) |

New decision: add a row; write a record only if the reasoning does not fit the row.
The earlier long register is kept as [Archive/Decisions/Decision-Log.md](Archive/Decisions/Decision-Log.md).
