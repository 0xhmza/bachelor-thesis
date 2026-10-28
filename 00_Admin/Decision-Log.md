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
| D2 | Store search, ranking, rating/download floor | proposed: one ranking of both stores by German-market popularity score P, no floor (10-25); terminology, store-specific contributions and assumptions clarified without changing the calculation; search frame and one app per developer (10-23); provider identity rules P1–P3 (10-26) | Meeting 10-13; sampling trial 2026-10-11; storefront check 2026-10-22; evaluation 2026-10-23; country check of Play reviews 2026-10-25; v004 implementation and outputs on the frozen dataset (10-26) | [D02](Decisions/D02_ranking-and-rating-floor.md) |
| D3 | Tracker scope and keyword space | proposed (10-23): domains and keywords of Hutton et al. 2018 and Malki et al. 2024, EN + DE; tracking-over-time rule; operational checks of E1–E5 on the store listing (10-26) | Meeting 10-13; Hutton 2018; Malki 2024; Robillard 2019; screening log | [D03](Decisions/D03_scope-keywords-function.md) |
| D4 | Payment, trial and account eligibility | proposed (10-23): free to install; payment recorded, decides walkthroughs only | Meeting 10-13; Robillard 2019 | [D04](Decisions/D04_payment-access.md) |
| D5 | Apps without a privacy policy | confirmed (meeting 10-13; adopted 10-23): included, absence reported | Meeting 10-13; Sunyaev 2015; O'Loughlin 2019 | [D05](Decisions/D05_apps-without-policy.md) |
| D6 | Native / platform health apps | proposed (10-25): leading vendor per platform (Apple, Samsung) → Apple Health, Apple Fitness, Samsung Health; replaces the 10 % threshold | Meeting 10-13; StatCounter vendor and OS shares | [D06](Decisions/D06_preinstalled-apps.md) |
| D7 | Language rule per material type | confirmed (meeting 10-13; adopted 10-23): English first, German fallback | Meeting 10-13; Arora et al. 2022 on English–German policy differences | [D07](Decisions/D07_language.md) |
| D8 | Two-coder procedure | open | Meeting 10-13 | — |
| D9 | LLM role and acceptance thresholds | open | Proposal; meeting 10-13 | — |
| D10 | Walkthrough checklist and outputs | open | Meeting 10-13 | — |
| D11 | Device scope (apps only) | proposed (10-23, in D3): companion apps eligible if the app records or displays tracking data; devices not analysed | Meeting 10-13 | [D03](Decisions/D03_scope-keywords-function.md) |
| D12 | Basis of the harm tree ("best app") | open — needs supervisor | Meeting 10-13, wording ambiguous | — |
| D13 | Literature search, filter and screening | superseded by D14 (10-28); was: staged procedure of Baumann et al. 2025 (App. A) on OpenAlex and Semantic Scholar, ≥ 3 citations per year | Baumann 2025 App. A pp. 56–57; meeting 10-13 §3; API access test 10-26 | [D13](Decisions/D13_literature-review.md) |
| D14 | Literature search, screening and reporting (v002) | proposed (10-28): supervisor's venues listed in full, PubMed / IEEE Xplore / arXiv / ACL Anthology searched with one query per sub-question LQ1–LQ4, citation searching from the four supervisor papers, every thesis citation and digest paper screened; criteria C1–C4, ordered rules R1–R8 with one primary reason; no citation filter; contextual collection for cited works outside the criteria | Baumann 2025 App. A; PRISMA 2020, PRISMA-S, PRISMA-ScR; meeting 10-13 §3; access tests 10-28 | [D14](Decisions/D14_literature-review-v2.md) |

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
