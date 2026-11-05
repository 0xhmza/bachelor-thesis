# D21 — The search terms are compared with published vocabularies after the search

- **Status:** superseded by [D22](D22_search-term-development.md) (2026-11-05). Was: proposed (author's instruction, 2026-11-05, chat: the comparison option for search terms whose source is not recorded). The search of 28 October is frozen and does not change. The comparison stays as a record of that search.
- **Affects:** Methodology, Section 4.2 (Search concepts); Results (Search terms); Appendix F.1; [`term_check.py`](../../scripts/literature-term-check/v001/term_check.py); [D14](D14_literature-review-v2.md).

## Problem

D14 records the term groups, and the config says the groups derive from the RQ and the sub-questions. Nothing records where the individual terms came from: no record names a source for any term. So the thesis cannot say that the terms were taken from published vocabularies, and this check does not show that either. It shows only how far they overlap, and it was made after the search.

## Choice

The thesis states that the terms were chosen for this review, then reports the comparison as an after-the-fact check. It changed no term. Each term falls into one of four classes, using the search's own matching rules (`lit.py`):

1. **Listed:** the term, with its truncation, is an entry of a published term list or a phrase within an entry, or an entry's truncation covers it.
2. **Published word:** a single word from such a list followed by `app*` or `track*` (`fertility app*`).
3. **Held before:** in no list, but in the title or abstract of a work held before the search, meaning the records whose route is the thesis citations or the Methods Digest in the frozen `records.csv`.
4. **Neither.**

A spelling or inflection (`m-health`, `reidentif*`, `inferred`, `analyz*`, `framed`, `llms`) takes the result of its base term.

## Lists compared

Only lists reported by works in the thesis bibliography count, so that the comparison set is fixed by a rule and not chosen term by term. Each was read in the PDF:

| Work | Locator | Used by that study to search |
|---|---|---|
| Baumann et al. 2025 | App. A, Table 6, pp. 56–57 | literature |
| Hutton et al. 2018 | Table 2, p. 5 | Google Play |
| Malki et al. 2024 | Sec. 3.1, p. 4 | Google Play |
| Salehzadeh Niksirat et al. 2024 | Sec. 1.2, 183:4 | literature |
| Shipp and Blasco 2020 | Sec. 3.1, PDF p. 3 (printed p. 493) | app stores |
| Doan et al. 2024 | Sec. 4.5, p. 9 | the text of policies, for risk and benefit passages |

Robillard et al. 2019 (App. 1), Huckvale et al. 2019 and O'Loughlin et al. 2019 also report lists in the bibliography; no term matches them.

## Result

The eight groups hold 117 term entries, 110 distinct.

| Group | Listed | Published word | Held before | Neither | All |
|---|---:|---:|---:|---:|---:|
| D | 5 | 10 | 11 | 6 | 32 |
| P | 1 | 0 | 4 | 0 | 5 |
| H | 1 | 0 | 12 | 3 | 16 |
| C | 0 | 0 | 9 | 9 | 18 |
| T | 0 | 0 | 7 | 3 | 10 |
| L | 4 | 0 | 3 | 2 | 9 |
| A | 3 | 0 | 8 | 1 | 12 |
| F | 0 | 0 | 10 | 5 | 15 |
| All | 14 | 10 | 64 | 29 | 117 |

The domain and language-model terms have published support. The communication, privacy-text and framing groups have no listed term, because no list in the bibliography searches for those concepts.

## Limits

- The check shows overlap, not origin.
- 45 of the 128 works held before the search have no abstract in the frozen records, so "neither" can understate use in those works. Only titles and abstracts are read, the same fields the search used.
- The Doan et al. list locates passages in policies and is not a search for apps or literature. It alone makes `harm*` a listed term.
- The library holds five more lists from works outside the bibliography: Benjumea et al. 2020 (p. 2), Georgiou et al. 2026 (p. 2), Mehrnezhad et al. 2024 (p. 4), Stoyanov et al. 2015 (p. 2) and Alfawzan et al. 2022 (Textbox 1). Counting them would move 12 terms up: `health app*`, `mhealth`, `m-health`, `mobile health`, `health track*`, `cycle track*`, `femtech`, `app description*`, `analys*`, `analyz*`, `assess*`, `evaluat*`.

## Would change if

The author recalls or finds a record of how the terms were chosen; the thesis then states that source and keeps this check as a check.
