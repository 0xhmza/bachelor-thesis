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
| D1 | Sample size and stopping rule | open | Meeting 10-13: first 50 eligible, no quotas | — |
| D2 | Store search, ranking, rating/download floor | open | Meeting 10-13; sampling trial 2026-10-11 | — |
| D3 | Tracker scope and keyword space | open | Meeting 10-13: add mental health, sleep, specialised | — |
| D4 | Payment, trial and account eligibility | open | Meeting 10-13 | — |
| D5 | Apps without a privacy policy | open | Meeting 10-13: include, report absence | — |
| D6 | Native / platform health apps | open | Meeting 10-13 | — |
| D7 | Language rule per material type | open | Meeting 10-13: English first, German fallback | — |
| D8 | Two-coder procedure | open | Meeting 10-13 | — |
| D9 | LLM role and acceptance thresholds | open | Proposal; meeting 10-13 | — |
| D10 | Walkthrough checklist and outputs | open | Meeting 10-13 | — |
| D11 | Device scope (apps only) | open | Meeting 10-13 | — |
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
