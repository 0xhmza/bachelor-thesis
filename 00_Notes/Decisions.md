# Decisions

One row per methodological decision. The methodology states a rule only after it has a row
here. Full reasoning and evidence: `Archive/Decisions/Dnn_*.md` (linked in the last column).

Status: **open** · **proposed** (written, not yet confirmed) · **confirmed** / **decided** · **superseded**.

| ID | Topic | Rule | Status | Record |
|---|---|---|---|---|
| D1 | Sample size | 47 ranked + 3 preinstalled apps, no quotas; Android only since 11-21: 49 ranked + 1 preinstalled (D26) | proposed; justification by comparison with prior studies added 11-15 | [D01](Archive/Decisions/D01_sample-size.md) |
| D2 | Ranking | One ranking of both stores by German-market popularity, no rating floor; several apps of one provider are separate apps, each studied on its own (provider rule dropped 11-16); two listings are merged only when they are the same app in both stores, decided by hand; candidate pairs are the listings of the same provider, identified as the controller named in the privacy policy (GDPR Art. 13(1)(a); App Store seller if no policy) (decided 11-16); sensitivity threshold 5 of 47 providers (to restate for apps) | proposed; provider rule dropped, decided 11-16 | [D02](Archive/Decisions/D02_ranking-and-rating-floor.md) |
| D3 | Scope and keywords | Keywords of Hutton 2018 and Malki 2024, EN + DE; eligibility I1–I7 and X1–X8 (restating E1a–E1d to E5) checked on the store listing | proposed; keyword reverse engineering, store-API test and must-include apps dropped 11-15 | [D03](Archive/Decisions/D03_scope-keywords-function.md) |
| D4 | Payment | Free to install; payment is recorded and only limits walkthroughs | proposed | [D04](Archive/Decisions/D04_payment-access.md) |
| D5 | No privacy policy | App included, absence reported | confirmed 10-13 | [D05](Archive/Decisions/D05_apps-without-policy.md) |
| D6 | Preinstalled apps | Leading vendor per platform: Apple Health, Apple Fitness, Samsung Health; Android only since 11-21: Samsung Health (D26) | proposed | [D06](Archive/Decisions/D06_preinstalled-apps.md) |
| D7 | Language | English first, German fallback | confirmed 10-13 | [D07](Archive/Decisions/D07_language.md) |
| D8 | Coders | No second coder: two models code, the author is the only human (checks, validation reference); author recodes a tenth after two weeks; Krippendorff's α | decided 11-15 (replaces the 11-04 rule) | [D08](Archive/Decisions/D08_two-coder.md) |
| D9 | LLM role | Two models code all units; people check high-stakes labels blind; 500-unit stratified validation sample | decided 11-04 | [D09](Archive/Decisions/D09_llm-role.md) |
| D10 | Walkthrough | All 50 apps; tasks T1–T7; Android for dual-listed apps; ten-app second rating | closed 11-05 | [D10](Archive/Decisions/D10_walkthrough.md) |
| D11 | Devices | Apps only; companion apps are eligible | proposed (inside D3) | [D03](Archive/Decisions/D03_scope-keywords-function.md) |
| D12 | Harm-tree basis | One generic health tracker; reference model v2 | decided 11-04; refined by D23 | [D12](Archive/Decisions/D12_reference-model.md) |
| D13 | Literature search v1 | Staged search with citation filter | superseded by D21 | [D13](Archive/Decisions/D13_literature-review.md) |
| D14 | Literature search v2 | Venue listing, strands, screening rules | superseded by D21 | [D14](Archive/Decisions/D14_literature-review-v2.md) |
| D15 | Domain | One domain: health trackers; categories are search keywords only; each app gets one primary category (first function on its listing, or multipurpose) that only describes the sample, reported with count and share | confirmed 10-28; primary category added 11-16 (proposed) | [D15](Archive/Decisions/D15_health-tracker-domain.md) |
| D16 | Instrument test | One-app test (Clue) | superseded by D20 | [D16](Archive/Decisions/D16_instrument-test.md) |
| D17 | RQ4 surfaces | Privacy policy and inspected interface only | confirmed 11-04 | [D17](Archive/Decisions/D17_rq4-surfaces.md) |
| D18 | Reporting unit | Equal weight per app | decided 11-04 | [D18](Archive/Decisions/D18_reporting-unit.md) |
| D19 | Data release | Instruments, scripts, labels open; captured texts for examiners only; recordings private | proposed | [D19](Archive/Decisions/D19_data-release.md) |
| D20 | No pilot | Method applied to all apps as written; no pilot or development apps | confirmed 11-05 | [D20](Archive/Decisions/D20_no-pilot.md) |
| D21 | Literature review | Brief review, at most ten papers, no PRISMA | confirmed 11-06 | [D21](Archive/Decisions/D21_brief-literature-review.md) |
| D22 | Research questions | Full questions in the text; RQ1–RQ4 kept, RQ2 not postponed; no separate RQ on uncovered harms | decided 11-15 | [D22](Archive/Decisions/D22_research-questions.md) |
| D23 | Harm trees | Built use case by use case; stop after two cases that add nothing; app-specific trees drawn in full for five apps (number may change with feasibility) | proposed 11-07; five apps decided 11-15 | [D23](Archive/Decisions/D23_use-case-subtrees.md) |
| D24 | Study type | Document and interface analysis; no user study or survey | confirmed 11-15 | — |
| D25 | Ethics | No ethics review: no human participants, only public documents and the analyst's own use of the apps | decided 11-15 | — |
| D26 | Platform | Android only: the App Store and Apple's preinstalled apps are dropped. 49 Google Play apps (German storefront) + Samsung Health, the preinstalled tracker of the leading Android vendor (D6 rule). Keywords, depth 30, rules I1–I7/X1–X8, German-market popularity (Google-Play-only case of D2: German review count) and no provider rule stay as before. New collection of 21 November 2026 with `googleplay-scraper/v007`; thesis draft in `03_Thesis-v2/` | decided 11-21 (author); replaces the iOS parts of D1, D2, D6 | — |
| D27 | Known-app check | 25 well-known trackers, listed before the check, must be among the search hits; a missing one leads to new generic EN/DE query pairs, never brand names; result reported in Results | decided 11-21 (author) | [check](../04_Study/4.4_App-Sampling/known-apps-check.md) |

New decision: add a row; write a record only if the reasoning does not fit the row.
The earlier long register is kept as [Archive/Decisions/Decision-Log.md](Archive/Decisions/Decision-Log.md).
