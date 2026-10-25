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
| D2 | Store search, ranking, rating/download floor | proposed: ranking, floor, store balance; search frame and one app per developer (10-23) | Meeting 10-13; sampling trial 2026-10-11; storefront check 2026-10-22; evaluation 2026-10-23 | [D02](Decisions/D02_ranking-and-rating-floor.md) |
| D3 | Tracker scope and keyword space | proposed (10-23): domains and keywords of Hutton et al. 2018 and Malki et al. 2024, EN + DE; tracking-over-time rule | Meeting 10-13; Hutton 2018; Malki 2024; Robillard 2019 | [D03](Decisions/D03_scope-keywords-function.md) |
| D4 | Payment, trial and account eligibility | proposed (10-23): free to install; payment recorded, decides walkthroughs only | Meeting 10-13; Robillard 2019 | [D04](Decisions/D04_payment-access.md) |
| D5 | Apps without a privacy policy | confirmed (meeting 10-13; adopted 10-23): included, absence reported | Meeting 10-13; Sunyaev 2015; O'Loughlin 2019 | [D05](Decisions/D05_apps-without-policy.md) |
| D6 | Native / platform health apps | proposed (Apple Health, Apple Fitness, Samsung Health) | Meeting 10-13; StatCounter vendor shares | [D06](Decisions/D06_preinstalled-apps.md) |
| D7 | Language rule per material type | confirmed (meeting 10-13; adopted 10-23): English first, German fallback | Meeting 10-13; Arora et al. 2022 on English–German policy differences | [D07](Decisions/D07_language.md) |
| D8 | Two-coder procedure | open | Meeting 10-13 | — |
| D9 | LLM role and acceptance thresholds | open | Proposal; meeting 10-13 | — |
| D10 | Walkthrough checklist and outputs | open | Meeting 10-13 | — |
| D11 | Device scope (apps only) | proposed (10-23, in D3): companion apps eligible if the app records or displays tracking data; devices not analysed | Meeting 10-13 | [D03](Decisions/D03_scope-keywords-function.md) |
| D12 | Basis of the harm tree ("best app") | open — needs supervisor | Meeting 10-13, wording ambiguous | — |

The reading that supports each decision is mapped in
[`01_Literature/Methods-Reading-List.md`](../01_Literature/Methods-Reading-List.md)
("Meeting decision → reading → extraction target") and in the literature map.

## Collector development — 20 October 2026 (D2 remains open)

The user requested a Python iPhone App Store keyword collector, starting with
`fitness`, returning as much available app information as possible. The
[collector documentation](../scripts/appstore-scraper/v001/README_app_store_search.md) records its
technical settings and interpretation limits. Germany is the configurable
default because the [13 October meeting](Meeting-Notes/2026-10-13_Supervisor-Meeting_Organized.md)
retains the German market; English text is requested. Apple's
[Search API documentation](https://performance-partners.apple.com/search-api)
supports keyword/storefront parameters, a requested limit of 1–200 and JSON
responses. Public product pages provide supplementary privacy and listing data.
These choices support a candidate-discovery development run, with original API
order and raw evidence retained. They do not confirm an API-to-store-UI rank
equivalence, a final search frame, a rating threshold, or eligibility decisions.
No methodology chapter or sampling protocol is changed; D2 remains open.

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
