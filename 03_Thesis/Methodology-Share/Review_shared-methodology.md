# Review of the shared methodology (Google Doc PDF, "HCS Thesis Proposal.pdf")

Reviewed on 6 November 2026 against `03_Thesis/chapters/04_methodology.tex`, Appendices A–F
and the scripts. The corrected PDF is `Methodology_corrected.pdf` in this folder (built from
`04_methodology_review.tex` and `appendix_share/`). No paragraphs were added; the fixes are
sentence-level.

**Appendix numbering changed in the second version (see D).** The PDF now has three appendices:
A Literature Search (old F), B App Sampling Details (old C), C Rules of the LLM Coding (old B).
Table and appendix numbers named in A–C below are those of the Google Doc; in the PDF they are
renumbered automatically, so the Google Doc's "Table C.6", "Table F.4", "Table B.1" and so on no
longer match it.

## A. Broken references left by the trimming (must fix)

| # | Where | Problem | Fix applied |
|---|---|---|---|
| A1 | Chapter intro | "Section 4.8 closes with ethics, availability and limitations" – there is no 4.8 | Sentence removed |
| A2 | 4.4.2 Ranking, 4.4.2 Same app, 4.4.3 heading | "tested by the sensitivity checks below", "in any check", heading "…and Sensitivity Checks", but the paragraph was cut | One sentence names the checks and points to Table C.8; heading now "Provider Rule and Preinstalled Apps" |
| A3 | 4.4.3 Preinstalled | "a rule with three steps", only two (Vendors, Apps) remain | "two steps" |
| A4 | 4.4.3 Preinstalled, Apps | The E1–E5 condition was cut, so any preinstalled health app would qualify | "…and if it meets the eligibility criteria E1 to E5" restored |
| A5 | Table 4.6 "K1–K8" | K1–K8 never introduced | 4.2.4: "Capabilities are grouped into eight categories (K1–K8)" |
| A6 | Table 4.6 "Black, blue, red… grey" | Colours refer to the removed harm-tree figure | Row names the three origins; text adds one sentence on the fourth mark (events outside the app) |
| A7 | 4.6.3 "deletion (IM12) and export (IM14)" | Node IDs belong to Appendix G, which is not shared | IDs removed; the rule ("present only if no usable route, including a request to the provider") restored |
| A8 | 4.6.5 RQ1/RQ4, Table 4.1, Table 4.12 | "corrected estimates", "detection summaries", "Absence … follows Section 4.7.2": the paragraphs that define them were cut, so 4.7.2 defines none of them | Three sentences added to the opening paragraph of 4.7.2 (difference estimator, detection summaries, absence worded with recall) |
| A9 | Table 4.9 caption | "…and related tree nodes or codes", but that column was cut | "Walkthrough tasks and the user goal of each" |
| A10 | Figure numbering | Figure 4.1 is followed by Figure 4.3 (4.2 was deleted) | Renumbered automatically (now Figure 4.2) |
| A11 | 4.1.1 "Section 1.2", 4.4 "Section 5.2" | Point outside the shared chapter | Kept as plain text ("introduction of the thesis (Section 1.2)", "with the results (Section 5.2)") |
| A12 | 4.6.1 "A script fixes units before coding (Section 4.7.2)" | Wrong target; 4.7.2 is the validation sample | Says why instead: models and coders label the same units |
| A13 | 4.6.1 "Appendix A defines the labels" | Appendix A has no label definitions, only the CycleMate worked example | "Appendices A and D apply the labels to two constructed examples" |

## B. Content changed in the Google Doc that is now wrong

| # | Where | Problem | Fix applied |
|---|---|---|---|
| B1 | 4.2.3 Deduplication | Says titles are only flagged and reviewed by hand *after* exclusion, in future tense. `scripts/literature-search/v002/merge.py` merges on DOI/arXiv **and** normalised title with years ≤1 apart (≤3 for arXiv). Reviewing duplicates after screening would also break the PRISMA counts | Text describes what the script does |
| B2 | 4.4.1 Eligibility | "in the collection, this never happened" is a result inside the method | Removed |
| B3 | 4.4.3 footnote | "Collected with the same collection scripts as in Section 4.4.1": the trial used Google Play only, 19 keywords, depth 20 (Appendix C.2) | Footnote states those settings |
| B4 | 4.5.2 | "before reviewing the model's codes": there are two models | "models' codes" |
| B5 | 4.5.2 Preparation | "iOS for App Store–only apps" misses preinstalled iOS apps | "iOS for apps available only on iOS" |
| B6 | 4.5.2 | "Interface confirmations establish what the app reports…" | "establish only what the app reports …, not that it took place" |
| B7 | 4.1 | Says the study examines privacy *policies* only, while it codes interface text too; "It has three parts" right after "two steps" | "policies and app interfaces", "the text", "The study has three parts" |
| B8 | 4.2.1 | "derived from the RQ 'what harms service providers communicate'" does not match the research question | Uses the chapter's wording |
| B9 | 4.4 | No rule says how the 50 places are filled (preinstalled + ranked); groups (ii)/(iii) overlap | One clause each: an app in both stores is one candidate; the remaining places go to the highest-ranked eligible store apps, one per provider |
| B10 | 4.6.2 | "One open-weight model is preferred" (sounds like one model) | "An open-weight model is preferred for one of the two"; why agreement is only a robustness check (correlated errors) |
| B11 | 4.5.2 Procedure | "the protocol's synthetic profile": the protocol is introduced only in 4.7.1 | "the synthetic profile fixed in the walkthrough protocol" |

## C. Language (ChatGPT edits)

- 4.6.1–4.7.2 switched to imperative orders ("Code…", "Record…", "Report…", "Draw 500 units…"). The rest of the chapter states rules declaratively; these are now declarative with the same content.
- American/British mix: "analyzes" → "analyses", "reevaluates" → "re-evaluates", "judgments" → "judgements".
- Missing full stop after "[20]" in 4.3.2; "builds the tree" → "builds the harm trees"; "the extraction table" (never introduced) → "an extraction table"; list item 1 of 4.1 was not bold.
- Citations now carry the page and section pinpoints that the LaTeX already had (lost in the Google Doc).

## D. Appendices: only the tables the chapter cites (second version, 6 November 2026)

No worked examples, prompts, search strings, scripts or results. The PDF keeps:

| New | Content | Old number |
|---|---|---|
| A.1 | Complete term groups | F.1 |
| A.2 | Venues and selection rules | F.2 |
| A.3 | Databases, fields and limits | F.4 |
| B.1 | Search keywords | C.6 |
| B.2 | Public listing data by geographic basis | C.7 |
| B.3 | Sensitivity variants | C.8 |
| C.1 | Rules of the LLM coding | B.1 |

Removed: Appendix A (codebook worked example, CycleMate), B's prompt listings, C's sample table,
the selection without the developer rule, the identity register, the Google Play trial
collection and the hand-matched developer names (records of the collection), the provider
examples, D (worked example), E (scraping scripts), F's syntax table, search strings and corpus
inventory, and G (reference model). The vendor-share calculation stays as one paragraph in B.3.

Matching changes in the chapter:
- The references to Appendix D, to "Appendices A and D … constructed examples", to the
  collectors in Appendix E ("with collection scripts of this project"), to the search strings,
  to the provider examples and to the prompts appendix were removed.
- The Reporting row of Table C.1 no longer says that the prompts are archived in an appendix.
- Table A.3 now says "records of short anchor queries" instead of "the anchor pool", which was
  defined only in the removed search strings.
- 4.4.3 Selection keeps the trial finding (one developer held 10 of the 47 most-rated apps) but
  no longer points to a table; the footnote states the trial's settings, including that it was
  ranked by the worldwide rating count. The P3 sentence no longer points to a table either.

## E. Open points I did not change (your decision)

1. **Who screens the literature?** The cut removed the only sentence that said who made the screening decisions. A reader will ask. I did not add anything, because the true answer (AI-prepared screening, checked by the author) is what you chose to leave out. A neutral option: "Every inclusion and full-text exclusion is checked by the author", but only if that check is done.
2. **Minimisation:** Table 4.12 says minimisation is "decided by people only", but the Stage 2 prompt (`stage2_stance_v2.md`) does return `S-MIN`, and Axis B says it is coded. Consistent if read as "models propose, people decide"; consider saying so.
3. **The thesis's Appendix A says "codebook version 4"** (no longer in the shared PDF); the frozen bundle is v7.
4. **Sunyaev et al., Spearman 0.89:** kept as in the LaTeX; not re-checked against the PDF.
5. **Length:** the text is about as long as the Google Doc (a few added clauses, one removed sentence). The thesis layout makes the chapter about 20 pages instead of 15; with bibliography and appendices the PDF has 32 pages.
6. **The Google Doc still cites the old appendix numbers** (Table B.1, C.2, C.4, C.6–C.8, F.1, F.2, F.4, Appendices A, D, E). Update them if you keep sharing the doc.
