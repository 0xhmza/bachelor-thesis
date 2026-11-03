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
| D1 | Sample size and stopping rule | proposed (47 ranked + 3 preinstalled, no quotas) | Meeting 10-13: first 50 eligible, no quotas | [D01](Decisions/D01_sample-size.md) |
| D2 | Store search, ranking, rating/download floor | proposed: one ranking of both stores by German-market popularity score P, no floor (10-25); terminology, store-specific contributions and assumptions clarified without changing the calculation; search frame and one app per developer (10-23); provider identity rules P1–P3 (10-26); cross-store product identity I1–I5 with a decision register (10-28) | Meeting 10-13; sampling trial 2026-10-11; storefront check 2026-10-22; evaluation 2026-10-23; country check of Play reviews 2026-10-25; v004 implementation and outputs on the frozen dataset (10-26); peer review F01, Steinböck et al. 2024 §3.2–3.3, 5.2, Hu et al. 2018 §3.1, v005 and the identity register (10-28) | [D02](Decisions/D02_ranking-and-rating-floor.md) |
| D3 | Tracker scope and keyword space | proposed (10-23): domains and keywords of Hutton et al. 2018 and Malki et al. 2024, EN + DE; tracking-over-time rule; operational checks of E1–E5 on the store listing (10-26) | Meeting 10-13; Hutton 2018; Malki 2024; Robillard 2019; screening log | [D03](Decisions/D03_scope-keywords-function.md) |
| D4 | Payment, trial and account eligibility | proposed (10-23): free to install; payment recorded, decides walkthroughs only | Meeting 10-13; Robillard 2019 | [D04](Decisions/D04_payment-access.md) |
| D5 | Apps without a privacy policy | confirmed (meeting 10-13; adopted 10-23): included, absence reported | Meeting 10-13; Sunyaev 2015; O'Loughlin 2019 | [D05](Decisions/D05_apps-without-policy.md) |
| D6 | Native / platform health apps | proposed (10-25): leading vendor per platform (Apple, Samsung) → Apple Health, Apple Fitness, Samsung Health; replaces the 10 % threshold | Meeting 10-13; StatCounter vendor and OS shares | [D06](Decisions/D06_preinstalled-apps.md) |
| D7 | Language rule per material type | confirmed (meeting 10-13; adopted 10-23): English first, German fallback | Meeting 10-13; Arora et al. 2022 on English–German policy differences | [D07](Decisions/D07_language.md) |
| D8 | Two-coder procedure | proposed (11-01): author codes all, second coder codes the validation set independently; who the second coder is stays open | Meeting 10-13; McDonald 2019; Campbell 2013 | [D08](Decisions/D08_two-coder.md) |
| D9 | LLM role and acceptance thresholds | proposed (11-01): the model screens and proposes, people decide; three stages, spans checked by script; model chosen in the pilot; applies to policy and captured UI text, with validation limits reported by surface (11-03) | Meeting 10-13; Rodriguez 2024; Törnberg 2024; Baumann 2025; Pangakis 2023; Xie 2025 | [D09](Decisions/D09_llm-role.md) |
| D10 | Walkthrough checklist and outputs | proposed (11-01), reviewed 11-03: attempt all 50 apps; Q1–Q4 on T1–T7; defaults before control changes, deletion last; task non-finding does not prove incapability; preserve screen/text provenance, separate policy from UI, and report partial access; three outputs feed applicability, D9 coding and RQ4; device, platform, limits, second inspection and policy-coding order stay open | Meeting 10-13; Wharton 1994; Mahatody 2010; Malki 2024; Habib 2020 | [D10](Decisions/D10_walkthrough.md) |
| D11 | Device scope (apps only) | proposed (10-23, in D3): companion apps eligible if the app records or displays tracking data; devices not analysed | Meeting 10-13 | [D03](Decisions/D03_scope-keywords-function.md) |
| D12 | Basis of the harm tree ("best app") | proposed (11-01, author's instruction): one generic health tracker holding every function a tracker can have; a real app is a subset. Supervisor to confirm the reading | Meeting 10-13; Knabenhans 2026 §4; De & Le Métayer 2017 (full text not read); Deng 2011 | [D12](Decisions/D12_reference-model.md) |
| D13 | Literature search, filter and screening | superseded by D14 (10-28); was: staged procedure of Baumann et al. 2025 (App. A) on OpenAlex and Semantic Scholar, ≥ 3 citations per year | Baumann 2025 App. A pp. 56–57; meeting 10-13 §3; API access test 10-26 | [D13](Decisions/D13_literature-review.md) |
| D14 | Literature search, screening and reporting (v002 run, v003 method) | proposed (10-28), revised by the author (10-30): eight security, privacy and HCI venues listed in full, PubMed / IEEE Xplore / arXiv / ACL Anthology searched with strands S1–S4, one per sub-question LQ1–LQ4, one round of citation searching from four seed papers; no German strand; automatic deduplication; criteria C1–C4 (English only), ordered rules R1–R8 with one primary reason, R7 for paywalled papers without university or public access; no citation filter. The run of 10-28 still includes S5, the thesis-citation and digest routes and the old C2/R7 (results not yet revised) | Baumann 2025 App. A; PRISMA 2020, PRISMA-S, PRISMA-ScR; Cochrane Handbook ch. 4; Distler 2021; Wohlin 2014; meeting 10-13 §3; access tests 10-28; author's revision 10-30 | [D14](Decisions/D14_literature-review-v2.md) |
| D15 | Study domain and category allocations | confirmed by author (10-28): one domain, health trackers; source categories inform scope and keywords only; pilot, validation and walkthrough totals apply across the sample | Author's explicit clarification in chat, 28 October 2026; meeting 10-13: no category quotas and include mental-health trackers | [D15](Decisions/D15_health-tracker-domain.md) |
| D16 | Instrument test on one app before the pilot | proposed (11-01, author's instruction): Clue, purposive; real policy, invented walkthrough, stand-in manual coding; no estimate for the sample; version-5 synthetic classifications and applicability changes need re-evaluation under corrected D10 (11-03) | Author's instruction in chat; D10 review | [D16](Decisions/D16_instrument-test.md) |

The reading that supports each decision is mapped in
[`01_Literature/Methods-Reading-List.md`](../01_Literature/Methods-Reading-List.md)
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
