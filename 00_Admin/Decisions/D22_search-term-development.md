# D22 — How the literature search terms are developed and tested

- **Status:** proposed (2026-11-05, author in chat: "discard literature review results, reformulate the methodology of the terms so it is robust and correct. do not delete the results, just add a todo that says that the results do not reflect the methodology anymore."). The reviewer of the search is still to be named. Supersedes [D21](D21_search-term-check.md); replaces the term part of [D14](D14_literature-review-v2.md).
- **Affects:** Methodology, Section 4.2; Results, Literature Review, and Appendix F (kept, marked as no longer reflecting the method); the input of the capability table to the harm trees (Section 4.3).

## Problem

The search of 28 October has terms with no recorded source (D21), no test against known relevant studies and no peer review. A comparison made afterwards cannot repair that. The results of that search are therefore discarded as evidence. They stay in the thesis, marked, until a new search replaces them. The frozen data in `05_Data/Literature Search/28. Oct/` stays unchanged.

## Choice

The concept groups and strands stay. They follow from the sub-questions, and a concept-based and multi-stranded structure is what Cochrane describes (§4.4.2). Only the terms within the groups change, by this procedure:

1. **Reference set.** For each sub-question: the studies included in published reviews of that question; where none exists, the studies selected from a precise search of one database. All must meet the eligibility criteria. Each set is split at random, with a recorded seed, into two thirds for development and one third for validation (Hausner et al.).
2. **Candidates.** From three sources:
   - word and phrase frequencies in the titles and abstracts of the development set, keeping those in at least 20% of its studies and at most 2% of a random sample of records (Hausner et al.);
   - term lists that published studies report for the same concept (the lists in D21 are a starting point);
   - for PubMed, the MeSH headings of the development records, by frequency and relevance (Hausner et al.; Cochrane §4.4.4).
3. **Widening.** Spelling variants, synonyms, acronyms and truncation (Cochrane §4.4.4, MECIR C33). A term log records each term's source, group and the reason it was kept or dropped.
4. **Assembly.** Terms are combined by trial until each strand retrieves its development studies, at a precision that stays screenable (Hausner et al.; Cochrane §4.4.3).
5. **Validation.** Each strand is run against its validation set, compared by identifier and counting only studies the database holds. Every missed study is examined. A term it shows to be missing is added and the strand retested. First and final values are both reported, with their counts.
6. **Peer review.** A second person with search experience reviews the strings with the PRESS checklist before they run, and the review is reported (Cochrane §4.4.8; PRISMA-S Item 14).
7. **Freeze and check.** The terms are frozen for the run. Included studies found only by citation searching are checked for missing terms (Cochrane §4.4.11). A term found this way is added, the search rerun and the change logged. The results report how many included studies lie outside the reference set, because a search that finds only known studies may be biased towards them (Cochrane §4.4.11).

## Project rules without a direct precedent

- **Population sample:** Hausner et al. sample one database (MEDLINE). This review spans health and computing, so the sample is drawn from PubMed and from the enumerated venue papers. IEEE Xplore and the ACL Anthology offer no equivalent random sample.
- **Cut-offs:** 20% and 2% are Hausner et al.'s, set for a medical topic. They are starting values here, changed only with a logged reason.
- **No pass mark:** Hausner et al. state no numeric target in the Methods, and Cochrane gives none. So the value is reported with its counts, and every miss is examined. This replaces a threshold rather than copying one. A threshold is often attributed to Zhang et al. 2011 (quasi-sensitivity, doi:10.1016/j.infsof.2010.12.010), but only the abstract could be read, so it is neither used nor cited.
- **Missed validation study:** Hausner et al. do not say what to do. The retest rule above is this project's, and reporting both values keeps the first test visible.

## Evidence and what was read

- Hausner, Waffenschmidt, Kaiser and Simon 2012, *Systematic Reviews* 1:19, doi:10.1186/2046-4053-1-19. Read in the Europe PMC full text on 5 November 2026: Background and Methods verbatim. The Results and Discussion came only as a summary, so nothing here rests on them. Crossref record checked. Not in the library.
- Lefebvre et al., Cochrane Handbook v6.5.1 (2025), ch. 4, §§4.2.2, 4.4.2, 4.4.3, 4.4.4, 4.4.8, 4.4.11, read on the Cochrane page on 5 November 2026. The Technical Supplement was not read.
- McGowan et al. 2016, *J Clin Epidemiol* 75:40–46, doi:10.1016/j.jclinepi.2016.01.021. Crossref record checked. Abstract and Cochrane §4.4.8 only; the checklist itself still has to be read before it is used.
- Rethlefsen et al. 2021 (PRISMA-S), Item 14, read in the library PDF.

## Limits

- The set depends on published reviews of each question, and the method may fail where they are absent or incomplete. The precise search is the fallback, and it brings in the searcher's own choice of terms.
- Assembly stays partly a judgement, so the log has to show the changes.
- Small sets test little, so the counts are always reported.
- A new search has to be run and screened before any of this has results. The capabilities and harm trees that rest on the old review stand until then.

## Would change if

A qualified searcher reviewing the strings recommends otherwise, or reading the full text of a source changes what it supports.
