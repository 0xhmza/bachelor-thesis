# Systematic literature search — 26 October 2026

The literature review of the thesis (Methodology, Literature Review; Results,
Literature Search; Appendix F), run with the staged procedure of Baumann et al.
(2025, App. A) as adapted in [D13](../../../00_Admin/Decisions/D13_literature-review.md).

| Stage | What | Where |
|---|---|---|
| 0 | Queries Q1–Q4 in OpenAlex and Semantic Scholar (titles and abstracts), 15 works added by hand, duplicates merged, ≥ 3 citations per year | [`scripts/literature-search/v001`](../../../scripts/literature-search/README.md); frozen results in `05_Data/raw/literature-search_2026-10-26/` (historical hash reference: `05_Data/raw/README.md`, no longer present after the data reorganisation) |
| 1 | Title and abstract screening of 953 records, one code each | [`screening.csv`](screening.csv) |
| 2 | Extraction cards for the included works that are used | [`../Methods-Digest/cards/`](../../Methods-Digest/cards) (to be written) |
| 3 | Capabilities from the I1 works, for the harm trees | to be written |

**Status:** the screening decisions were prepared by an AI assistant (Claude)
from titles and abstracts on 26 October 2026. None has been checked by the
author yet. Check every decision before the thesis says who screened.

## `screening.csv`

One row per record that passed the citation filter. `rid` is the record ID in
the frozen `records.csv`; `decision` is `include` or `exclude`; `code` is the
criterion:

| Code | Meaning |
|---|---|
| I1 | documents privacy harms, risks, threats or inferable capabilities affecting users of health apps, fitness trackers or health wearables |
| I2 | analyses the privacy communication (policies, labels, store listings, notices, terms) of such apps or wearables |
| I3 | uses or evaluates language models to annotate, classify or extract information from privacy policies or similar privacy text |
| I4 | analyses how policies, notices or labels present or word data practices, risks or protections, in any domain |
| E1 | technical system (protocol, encryption, architecture, detection model) without documenting harms or analysing communication |
| E2 | outside the domain and topics |
| E3 | health apps or wearables without privacy harm or communication analysis (quality, usability, adoption, features) |
| E4 | no usable scholarly record (commentary, dissertation, duplicate) |
| E5 | language models without annotating privacy text (language models as a privacy risk, privacy-norm benchmarks, policy generation) |

Known duplicates coded E4: two records of Zou et al., *You 'Might' Be Affected*
(one misspelt "Afected"), and two of *Format vs. Content* (journal and
conference records); the other copy of each is included.

After changing a decision, run `python scripts/literature-search/v001/report.py`
to regenerate the thesis tables.
