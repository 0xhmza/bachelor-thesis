# Review of the shared methodology (Google Doc PDF, "HCS Thesis Proposal.pdf")

Reviewed on 6 November 2026 against `03_Thesis/chapters/04_methodology.tex`, Appendices A–F
and the scripts. The corrected PDF is `Methodology_corrected.pdf` in this folder (built from
`04_methodology_review.tex`). No paragraphs were added; the fixes are sentence-level.

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

## D. Appendices (A–F, Corpus Inventory left out)

- A: Step 6 talked about one language model, "tuned to miss as little as possible" → two models, "the combination favours recall". The RQ4 bullet coded "the store listing, the website": contradicts 4.5.1 → interface text only.
- C: The pointer to the results chapter is now plain text. The data path `05_Data/App Sampling/26. Oct/Raw/` did not match Appendix E and the frozen collection → `05_Data/raw/app-sample_2026-10-25/`.
- F: Section F.4 "Corpus Inventory" left out. Its own note says it is inconsistent with the revised method, the doc does not cite it, and it lists results. F.1–F.3 (cited) are kept, so Table F.1/F.2/F.4 numbering still matches the doc.
- Appendix G (reference model) is not cited in the shared text and is not included.

## E. Open points I did not change (your decision)

1. **Who screens the literature?** The cut removed the only sentence that said who made the screening decisions. A reader will ask. I did not add anything, because the true answer (AI-prepared screening, checked by the author) is what you chose to leave out. A neutral option: "Every inclusion and full-text exclusion is checked by the author", but only if that check is done.
2. **Minimisation:** Table 4.12 says minimisation is "decided by people only", but the Stage 2 prompt (`stage2_stance_v2.md`) does return `S-MIN`, and Axis B says it is coded. Consistent if read as "models propose, people decide"; consider saying so.
3. **Appendix A says "codebook version 4"**; the frozen bundle is v7. All codes used in the example still exist in v7, but I did not change the version number without checking the definitions.
4. **Sunyaev et al., Spearman 0.89:** kept as in the LaTeX; not re-checked against the PDF.
5. **Length:** the text is about as long as the Google Doc (a few added clauses, one removed sentence). The thesis layout makes the chapter about 20 pages instead of 15.
