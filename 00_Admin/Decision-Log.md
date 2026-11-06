# Decision log

Every methodological choice the thesis depends on, with its evidence. A decision
is **open** until it has a cited reason and, where the supervisor must confirm it,
a confirmation date. The methodology chapter cites these records; it never states
a choice that is still open here.

Status: `open` · `proposed` (evidence and choice written, awaiting supervisor) ·
`confirmed` (date and source of confirmation) · `superseded` (link to the newer record).

## Register

| ID | Question | Status | Evidence so far | Record |
|---|---|---|---|---|
| D1 | Sample size and stopping rule | proposed (47 ranked + 3 preinstalled, no quotas); note 11-06: "why 50?" needs a justification text, open | Meeting 10-13: first 50 eligible, no quotas | [D01](Decisions/D01_sample-size.md) |
| D2 | Store search, ranking, rating/download floor | proposed: one ranking of both stores by German-market popularity score P, no floor (10-25); terminology, store-specific contributions and assumptions clarified without changing the calculation; search frame and one app per developer (10-23); provider identity rules P1–P3 (10-26); cross-store product identity I1–I5 with a decision register (10-28); materiality rule for sensitivity checks proposed: more than 5 of 50 providers changed (11-04); materiality denominator corrected to the 47 ranked providers (11-04 evening); decided 11-04 (night): threshold of five of 47 ranked providers kept (k/50 bound under D18) | Meeting 10-13; sampling trial 2026-10-11; storefront check 2026-10-22; evaluation 2026-10-23; country check of Play reviews 2026-10-25; v004 implementation and outputs on the frozen dataset (10-26); peer review F01, Steinböck et al. 2024 §3.2–3.3, 5.2, Hu et al. 2018 §3.1, v005 and the identity register (10-28) | [D02](Decisions/D02_ranking-and-rating-floor.md) |
| D3 | Tracker scope and keyword space | 11-06: E1 expanded into E1a–E1d without a change of rule; keyword reverse engineering, result counts, three must-include apps and API test recorded, open; proposed (10-23): domains and keywords of Hutton et al. 2018 and Malki et al. 2024, EN + DE; tracking-over-time rule; operational checks of E1–E5 on the store listing (10-26) | Meeting 10-13; Hutton 2018; Malki 2024; Robillard 2019; screening log | [D03](Decisions/D03_scope-keywords-function.md) |
| D4 | Payment, trial and account eligibility | proposed (10-23): free to install; payment recorded, decides walkthroughs only | Meeting 10-13; Robillard 2019 | [D04](Decisions/D04_payment-access.md) |
| D5 | Apps without a privacy policy | confirmed (meeting 10-13; adopted 10-23): included, absence reported | Meeting 10-13; Sunyaev 2015; O'Loughlin 2019 | [D05](Decisions/D05_apps-without-policy.md) |
| D6 | Native / platform health apps | proposed (10-25): leading vendor per platform (Apple, Samsung) → Apple Health, Apple Fitness, Samsung Health; replaces the 10 % threshold | Meeting 10-13; StatCounter vendor and OS shares | [D06](Decisions/D06_preinstalled-apps.md) |
| D7 | Language rule per material type | confirmed (meeting 10-13; adopted 10-23): English first, German fallback; kept by the author after the 11-04 review; cost and language limitation now stated in the methodology (11-04); applicable-version check and fixed difference-log rule (11-04 evening) | Meeting 10-13; Arora et al. 2022 on English–German policy differences | [D07](Decisions/D07_language.md) |
| D8 | Two-coder procedure | proposed (11-01): author codes all, second coder codes the validation set independently; who the second coder is stays open; revised (11-04): author and second coder code the D9 validation sample of units; Krippendorff α; second coder also checks trees (D12) and rates recorded walkthroughs (D10); fallback = smaller probability sample across all strata; tasks separated (11-04 evening); decided 11-04 (night): second coder a computing student with no other part in the thesis, trained on 20 pilot units, about 22 h budget; name to be entered | Meeting 10-13; McDonald 2019; Campbell 2013 | [D08](Decisions/D08_two-coder.md) |
| D9 | LLM role and acceptance thresholds | proposed (11-01): the model screens and proposes, people decide; three stages, spans checked by script; model chosen in the pilot; applies to policy and captured UI text, with validation limits reported by surface (11-03); revised (11-04, author): two models of different families code all units; people check every high-stakes label without seeing model labels; stratified double-coded validation sample; corrected estimates; estimator specified: priority-partition strata, difference estimator on the independent corpus, app/pathway maxima as detection summaries, optional whole-app audit (11-04 evening); decided 11-04 (night): 500 units, Neyman allocation, floors V5 ≥ 150 and others ≥ 30; variance floor; precision bound 0.80 kept; no whole-app audit; scripts/validation-sample/v001 | Meeting 10-13; Rodriguez 2024; Törnberg 2024; Baumann 2025; Pangakis 2023; Xie 2025 | [D09](Decisions/D09_llm-role.md) |
| D10 | Walkthrough checklist and outputs | closed (11-05, author's instruction): all 50 apps, no subsample; proposed (11-01), reviewed 11-03: attempt all 50 apps; Q1–Q4 on T1–T7; defaults before control changes, deletion last; task non-finding does not prove incapability; preserve screen/text provenance, separate policy from UI, and report partial access; three outputs feed applicability, D9 coding and RQ4; second rating of recorded sessions of ten apps proposed (11-04); T5–T7 subgoals, lay scenarios, matched-state language capture (11-04 evening); decided 11-04 (night): Android for dual-listed apps, emulator/iPhone frozen at first pilot day, 5-min search limit, ten-app re-rating, walkthrough before model-code review, T3c redress subgoal; protocol v8 | Meeting 10-13; Wharton 1994; Mahatody 2010; Malki 2024; Habib 2020 | [D10](Decisions/D10_walkthrough.md) |
| D11 | Device scope (apps only) | proposed (10-23, in D3): companion apps eligible if the app records or displays tracking data; devices not analysed | Meeting 10-13 | [D03](Decisions/D03_scope-keywords-function.md) |
| D12 | Basis of the harm tree ("best app") | note 11-06: "harm trees for 3 apps" recorded, reading open, not applied; proposed (11-01, author's instruction): one generic health tracker holding every function a tracker can have; a real app is a subset. Supervisor to confirm the reading; independent check of every pathway before the freeze proposed (11-04); OR+ as OR of sufficient combinations with actor access; IM12 by usable route; pathway-matched harm coverage; denials as mentions (11-04 evening, model v2 pending); decided 11-04 (night): reference model v2 (K10 sufficient combinations, IM12 deletion and IM14 export across routes); evaluator v002 | Meeting 10-13; Knabenhans 2026 §4; De & Le Métayer 2017 (full text not read); Deng 2011 | [D12](Decisions/D12_reference-model.md) |
| D13 | Literature search, filter and screening | superseded by D14 (10-28) and D21 (11-06); was: staged procedure of Baumann et al. 2025 (App. A) on OpenAlex and Semantic Scholar, ≥ 3 citations per year | Baumann 2025 App. A pp. 56–57; meeting 10-13 §3; API access test 10-26 | [D13](Decisions/D13_literature-review.md) |
| D14 | Literature search, screening and reporting (v002 run, v003 method) | superseded by D21 (11-06): the procedure leaves the thesis, the run and its data stay; was: proposed (10-28), revised by the author (10-30): eight security, privacy and HCI venues listed in full, PubMed / IEEE Xplore / arXiv / ACL Anthology searched with strands S1–S4, one per sub-question LQ1–LQ4, one round of citation searching from four seed papers; no German strand; automatic deduplication; criteria C1–C4 (English only), ordered rules R1–R8 with one primary reason, R7 for paywalled papers without university or public access; no citation filter. The run of 10-28 still includes S5, the thesis-citation and digest routes and the old C2/R7 (results not yet revised); decided 11-04 (night): verification of AI screening (all inclusions and full-text exclusions, random fifth of T/A exclusions with escalation) | Baumann 2025 App. A; PRISMA 2020, PRISMA-S, PRISMA-ScR; Cochrane Handbook ch. 4; Distler 2021; Wohlin 2014; meeting 10-13 §3; access tests 10-28; author's revision 10-30 | [D14](Decisions/D14_literature-review-v2.md) |
| D15 | Study domain and category allocations | 11-06: categories are search keywords only, no subcategories (stated in the thesis); confirmed by author (10-28): one domain, health trackers; source categories inform scope and keywords only; pilot, validation and walkthrough totals apply across the sample | Author's explicit clarification in chat, 28 October 2026; meeting 10-13: no category quotas and include mental-health trackers | [D15](Decisions/D15_health-tracker-domain.md) |
| D16 | Instrument test on one app before the pilot | proposed (11-01, author's instruction): Clue, purposive; real policy, invented walkthrough, stand-in manual coding; no estimate for the sample; version-5 synthetic classifications and applicability changes need re-evaluation under corrected D10 (11-03); decided 11-04 (night): test kept as v1/v5 record; v2 re-evaluation recorded; no synthetic re-run | Author's instruction in chat; D10 review | [D16](Decisions/D16_instrument-test.md) |
| D17 | Surfaces compared in RQ4 | confirmed by author (11-04): privacy policy and inspected interface only; listings remain applicability evidence | Methodology review 2026-11-04 (M1); author in chat | [D17](Decisions/D17_rq4-surfaces.md) |
| D18 | Primary weighting unit of RQ1 | proposed (11-04): equal weight per app; pooled pathways secondary; uncertain-pathway calculations are sensitivity scenarios; decided 11-04 (night): equal weight per app adopted as primary view | Submission review 2026-11-04 (R8) | [D18](Decisions/D18_reporting-unit.md) |
| D19 | Release of study records | proposed (11-04, night): instruments, scripts and labels open; captured third-party texts as research copies for examiners (§ 60d UrhG); recordings private | § 60d UrhG; walkthrough protocol v8 | [D19](Decisions/D19_data-release.md) |
| D20 | No pilot or instrument test in the method | confirmed by author (11-05): the methodology is taken as complete and applied to all apps; one corpus, no development apps; test removed from Results, Discussion and Appendix H; the rules the pilot would have settled are proposed; supersedes D16 | Author in chat, 5 November 2026; Lohr 2021 ch. 3 for the allocation | [D20](Decisions/D20_no-pilot.md) |
| D21 | Literature review: brief, at most ten papers | confirmed by author for application (11-06, supervisor meeting: PRISMA and Boolean search belong to review papers); the ten-paper selection was proposed by the assistant and confirmed by the author the same day; supersedes D13/D14 for the thesis | Meeting 11-06; Page 2021 p. 178; Knabenhans 2026 §§4.2–4.3; pathways of reference model v2 cite seven papers | [D21](Decisions/D21_brief-literature-review.md) |
| D22 | Research questions: wording and set | wording confirmed (11-06): full questions with question marks, in the text, applied; set open: separate question on uncovered harms, RQ2 postponed, justification by related work | Meeting 11-06 | [D22](Decisions/D22_research-questions.md) |

The reading that supports each decision is mapped in
[`01_Literature/catalog/Methods-Reading-List.md`](../01_Literature/catalog/Methods-Reading-List.md)
("Meeting decision → reading → extraction target") and in the literature map.

## Collector development — 20 October 2026

An iPhone App Store keyword collector (first query `fitness`) was built as a
development run; settings and limits are in its
[documentation](../scripts/appstore-scraper/v001/README_app_store_search.md).
Germany is the default storefront (the [13 October meeting](Meeting-Notes/2026-10-13_Supervisor-Meeting_Organized.md)
keeps the German market); English text is requested. Apple's
[Search API](https://performance-partners.apple.com/search-api) takes keyword and
storefront parameters and a limit of 1–200. The run fixed no search frame,
threshold or eligibility rule and did not establish that API order equals
store-UI order.

## Record template

Copy into `Decisions/Dnn_short-name.md` and link it from the register.

```markdown
# Dnn — <question>

- **Status:** open | proposed | confirmed (YYYY-MM-DD, source) | superseded by Dmm
- **Affects:** RQ… · protocol file(s) · thesis section
- **Options considered:**
  1. …
  2. …
- **Evidence:** precedent papers with page/section, pilot result, supervisor input
- **Choice:** …
- **Reason:** one paragraph, every claim cited
- **Would change if:** the observation that should reopen this decision
```
