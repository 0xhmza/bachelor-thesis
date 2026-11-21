contract_role: methodology

## Dimension Scores

### D1: methodology_rigor
score: block
trigger: "a single coder screening with no reliability check or mitigation, decisions reused across stores without disclosure, or selection rules or stopping points changed after seeing the data without saying so"
block_class: repairable

### D2: domain_accuracy
score: not_assessed

### D3: argumentative_coherence
score: warn
trigger: "Claims mildly overstate completeness or generality, a limitation is acknowledged in one place but not carried through"

### D4: cross_disciplinary_relevance
score: not_assessed

### D5: writing_and_structure
score: not_assessed

### D6: venue_fit_and_contribution
score: not_assessed

## Review Body

Peer Reviewer 1 (Methodology), set up as a researcher who runs large app-store measurement studies. Calibration status: NOT_CALIBRATED. This is an unbound run, so I make no claim about venue alignment. Scope: Chapter 4 (which covers only app sampling), §5.1, and Appendices A and B, as the author's scope notes describe. I do not penalise the Introduction, which is empty on purpose, or the missing Discussion.

**Summary.** The sampling chapter is short and rule-based, and it is easier to audit than most: one script, one config file, a frozen snapshot, and a selection that stops at a fixed count. I re-derived every count in §5.1 from the deposited files, and all of them match (see Verification below). The weaknesses are not in the arithmetic. They are in four places where the text does not let a reader rebuild or trust the frame:
(1) The stated rule for keeping extra queries after the well-known-app check does not determine the five queries that were kept. The check that tuned the queries is then presented as a test of those queries.
(2) The text never says who screened or how reliable the screening was. Most decisions were carried over from an earlier screening, and three of them were made on App Store listings. Neither fact is disclosed.
(3) The review-count proxy is justified only by a citation, and the cited study used a different count.
(4) The text does not report that store search is unstable, or that nearly half of the queries return far fewer than 30 apps.
Developer concentration is reported but not analysed. Every one of these can be fixed in the text and appendix with data that is already collected.

**Dimension rationale.** D1 is block (repairable). The block trigger is met in three ways:
- No screener count, reliability check or mitigation is reported.
- 44 of the 53 screening decisions were carried over from a screening of 26 October, and 3 of them rest on App Store listings. Neither is disclosed (W3).
- The rule that actually chose the five added queries is not the rule the text states (W1).

D1 is not fatal: the stage counts and the sample follow exactly from the described pipeline and the frozen data.

D3 is warn rather than block. The central sampling claim (apps selected by popularity among search hits) does not rest on the known-app check, and the paper itself reports that Polar Flow was missed. But the check is called a test of market reach although it tuned the queries it tests (W2). The visibility condition that Polar Flow exposes is also not carried back into §4.1, which describes the 49 apps simply as "selected by popularity".

**Verification against the deposited data.** This is my own re-analysis of 05_Data/App Sampling/21. Nov and screening-android.csv; it is not a set of claims made by the paper.
- config.json holds 54 queries (49 base plus 5 added) and matches SHA256SUMS.
- The 15 mHealth terms in Hutton et al.'s Table 2 and the 12 terms in Malki et al. §3.1, with the stated EN/DE de-duplication, give 49 queries.
- search.json holds 1,220 results, 8 to 30 per query, covering 704 distinct apps. pages.jsonl holds 704 pages with no error.
- The base queries find 20 of the 25 well-known apps; all 54 queries find 24.
- Walking candidates.csv against the screening file screens 53 apps. It excludes exactly Temple Run 2, GuitarTuna, DoubleU Casino (all X2) and Calm (X4), and selects 49 apps with 4,142 to 99,995 reviews.
- Samsung Health ranks 8th with 33,757 reviews. 22 of the 25 well-known apps are in the sample.
- 43 of the 49 ranked apps appear in at least one top ten.
- The sample comes from 40 developers (Leap 8, Simple Design 3, Google 2). The category counts 22/9/8/6/2/2/1 sum to 50. 39.3/72.3 gives 54%.

I also ran sensitivity checks on the same snapshot and screening file; every app the alternative walks reach was already screened:
- A depth of 20 gives the identical 49 apps; a depth of 10 keeps 43.
- Dropping all five added queries keeps 42 of the 49.
- Dropping only fitness tracker and Fitnesstracker keeps 48.

### S1: Selection reproducible offline from a frozen snapshot
**Evidence Anchor**: text: Appendix B, first paragraph "a second run reuses them, so the screening does not change the candidates"

The script reads search.json and pages.jsonl again instead of searching anew, and the deposited copy carries SHA256 checksums. I reproduced the 53-app walk and the 49 selections exactly. The script also stops at the first unscreened app, which forces screening to follow rank order.

### S2: Selection and stopping rules are fixed and mechanical
**Evidence Anchor**: text: §4.4 (Selection) "ties are broken by the package name"

The text fixes the ranking key, the tie-break, the handling of unreadable pages, the fixed count of 49, and the treatment of the preinstalled app (screened separately and skipped in the ranking). Apart from screening, nothing in the walk is left to discretion.

### S3: The check's negative results are reported
**Evidence Anchor**: text: §5.1 (Search) "so the search misses at least this companion app of sports watches"

The paper reports the miss of Polar Flow with its review count, and the result before tuning (20 of 25). It also excludes brand-name queries, which protects against favouring single providers.

### S4: Stage counts are complete and correct
**Evidence Anchor**: text: §5.1 (Search) "They contained 704 different apps, and every store page could be read."

Each stage, from queries through results, distinct apps and readable pages to screened, excluded (with rule) and selected apps, has a count and a denominator, and every count checks out against the data.

### S5: Keyword set traceable to prior studies with an explicit translation rule
**Evidence Anchor**: text: §4.2 (Keywords) "This gives 49 queries."

The source term lists and the de-duplication rule reproduce the 49 base queries in Table B.1.

### S6: Eligibility rules are explicit and exclusions are coded by rule
**Evidence Anchor**: table: Table 4.1 (tab:eligibility), §4.3

Each rule is numbered, and each of the four exclusions in §5.1 names the rule it falls under.

### W1: The rule for keeping added queries does not produce the five queries kept
**Severity**: Major
**Evidence Anchor**: text: §4.2 (Check with well-known apps) "Only terms that found a missing app were kept, with their translation."
**Confidence**: 5 — recomputed from known-apps-probe.json and search.json

The probe log records 66 generic terms. Sixteen of them placed at least one of the five missing apps in their top 30 (for example fitness band, health tracker, Sportuhr, smart band, sleep tracker and Personenwaage), yet only five terms were kept. The stated rule ("only … were kept") is a necessary condition, not a selection rule, so a reader cannot derive the last row of Table B.1 from it.

The project's check notes describe the actual rule as "the smallest set that finds every reachable app". That set is not minimal either. In both the probe and the main run, smartband alone places Garmin Connect (position 8), Zepp (9) and Zepp Life (1) in its top 30, which makes fitness tracker and Fitnesstracker redundant. They were kept because they were tried first.

This order dependence reaches the sample. GloryFit enters only through fitness tracker (position 18). Without the two redundant queries, the 49th slot goes to Sleep Monitor (3,873 reviews) instead.

The stopping point ("when no further generic term finds a missing app") is open-ended: the pool of possible terms has no limit, and the order and number of trials (66) were chosen while the check was running.

Remedy:
- State the rule that was actually used and how ties were broken. One option is a candidate pool listed in advance and tried in full, followed by a minimal set chosen by a stated criterion.
- List all 66 tried terms with their hits in an appendix.
- Report how the sample changes under the other minimal set.

### W2: The well-known-app check tunes the queries and is then reported as testing them
**Severity**: Major
**Evidence Anchor**: text: §4.2 (Check with well-known apps) "It tests whether the queries reach the market; it does not force any app into the sample."
**Confidence**: 4 — design logic, confirmed against search.json and the screening file

The list of 25 is the author's own, queries were added until its apps were found, and §5.1 then reports that 22 of the 25 are in the sample. Once the queries are tuned this way, finding 24 of 25 is guaranteed. Only the result before tuning (20 of 25) is a real test, and it showed that the base queries miss all five device companion apps.

"Does not force any app" is true for each app on its own, but the step changes the sample's composition. Seven of the 49 ranked apps enter the frame only through the five added queries: Garmin Connect, Zepp, Zepp Life and Withings, plus Mi Fitness, Da Fit and GloryFit, which were not on the list. Without those queries, 7 of the 49 ranked slots would hold different apps. The project's own check notes call it "a plausibility check of the queries, not a measure of market coverage", but the manuscript does not carry this limitation.

Remedy:
- Report 20 of 25 as the test result, and report the 7-app effect.
- Present the added queries as a disclosed extension of the frame to device companion apps.
- If a coverage claim is wanted, test against a list that was not used for tuning, for example a second list fixed independently, or the German Health & Fitness top charts on the collection date.

### W3: No reliability information for screening, and undisclosed reuse of earlier, partly cross-store decisions
**Severity**: Major
**Evidence Anchor**: text: §4.3 "The rules are checked on the German Google Play page of the app"
**Confidence**: 4 — source column of screening-android.csv; the single screener is inferred from the one decision column and the silence of the text

The text says nothing about who screened, whether a second person checked any decision, or how unclear cases were settled. screening-android.csv shows that 44 of the 53 screening decisions were carried over from a screening of 26 October, done for an earlier design. Three of these (komoot, Lifesum, Freeletics) were made on App Store listings. Two further reasons (Calm, Headspace) say "as on the App Store", although their source column names Google Play. The file marks all carried-over decisions as re-checked on the 21 November page, which is a mitigation, but the text discloses neither the reuse nor the re-check.

The decisions that matter are boundary cases that a second rater could reasonably decide the other way:
- Calm (4,562 reviews) is excluded under X4 as recording only meditation time, while Headspace (4,142) is included as mood tracking. The two apps do nearly the same thing, and these opposite decisions decide who fills the 49th slot.
- The five Leap Fitness workout-plan apps sit on the line between I1.1 and X1.

Remedy:
- State that one person screened, and disclose the carry-over and the re-check.
- Add a second, blind rating of at least the boundary decisions (all exclusions, the eligible apps near the cut-off, and the workout-plan apps) and report raw agreement. Alternatively, report how the sample changes when those decisions are reversed.

### W4: The popularity proxy is justified by citation only, and the cited study used a different count
**Severity**: Major
**Evidence Anchor**: text: §4.4 (Popularity) "also ranked Google Play apps by their number of reviews"
**Confidence**: 4 — checked against Malki et al. §3.1 (p. 4) and pages.jsonl

Malki et al. ranked apps by the reviews they received in the preceding 12 months, explicitly so as not to favour older apps. The thesis uses the cumulative count, which favours apps that have been listed for a long time, and does not say why.

The text also asserts that the count is "for the German storefront" without showing whether the count is filtered by country (gl=de) or by language (hl=de, which would also include Austrian and Swiss reviewers). No check of its own is reported, although the collected pages contain what such a check needs. For example, the ratio of reviews to ratings is 34% for Fddb, which is used almost only in Germany, but 0.5% for Temple Run 2 and 0.3% for Flo. That pattern suggests a German-specific filter. The ratings and realInstalls fields would also allow a rank-agreement check.

Remedy:
- State that the cumulative count was chosen and that it is biased towards older apps.
- Show which filter the count reflects; one probe with hl=en or gl=at on a few apps is enough.
- Report a rank correlation with global ratings or installs as a plausibility check.

### W5: Search instability and the effective result depth are not reported
**Severity**: Major
**Evidence Anchor**: text: §4.2 (Search) "keeps up to the first 30 apps of the result page, in the order shown; some queries return fewer"
**Confidence**: 4 — search.json and known-apps-probe.json

Of the 54 queries, 26 returned fewer than 30 apps, including core terms such as cycling (10), diet (14), steps (12) and Schlaf (17). The effective depth therefore ranges from 8 to 30, and it is set by what the logged-out web page happened to serve, not by the design. The text does not explain this. It also does not check that the regular expression over the page HTML captures the results shown, in the order shown, or discuss how web-storefront results relate to what Android devices display.

Results are also unstable:
- Six queries were sent cleanly in both the probe and the main run of the same night. Three of them swapped an app in or out (komoot, for example, entered fitness tracker at position 30 only in the main run), and four changed order.
- For some base queries the number of results changed as well (fertility returned 14 in the probe and 29 in the main run), although the probe's trailing line break confounds those comparisons.

The manuscript says nothing about this instability, although the project's check notes acknowledge it. The offline rerun (S1) makes the selection reproducible from the snapshot, but a new collection would not reproduce it.

Remedy:
- State that the frame is one snapshot of the logged-out web search.
- Report the result count for each query and explain why some pages are short.
- Measure stability with one or two repeat collections, reporting the overlap of the candidate sets and of the selected 49.
- The data already contain one robustness result worth reporting: a depth of 20 gives the identical sample.

### W6: Developer concentration is noted but not analysed
**Severity**: Major
**Evidence Anchor**: text: §4.4 (Selection) "Apps from the same developer count as separate apps, because each has its own store page and interface."
**Confidence**: 3 — the facts are verified in pages.jsonl; how much they matter depends on how the RQ results will be aggregated, which is not yet written

Leap Fitness Group supplies 8 of the 49 ranked apps (16%), and Simple Design supplies 3. All eight Leap apps link to one policy page (leap.app/privacypolicy.html) that differs only in a pkg parameter, and the three Simple Design apps use two such pages. RQ1 to RQ4 are answered from policies and interfaces. If each app counts once, a single policy text could account for up to 16% of the policy-level observations. The stated justification (each app has its own store page and interface) covers the interface surface but not the policy surface.

Remedy:
- State the concentration as a property of the sample in the methodology.
- Fix the reporting unit before coding: per app with a sensitivity check per developer or per policy text, or a cap per developer.
- Report whether the Leap policies are one text.

### W7: Missing review counts are treated as zero without saying so
**Severity**: Minor
**Evidence Anchor**: absence: §4.4 Ranking and Selection — expected a rule for apps whose store page returns no review count; checked §4.4, §5.1, Appendix B prose and Listing B.2
**Confidence**: 5 — pages.jsonl and the sort key in Listing B.2

Of the 704 pages, 258 (37%) carry no review count, rating or score. The sort key (reviews or 0) ranks them as zero, tied and ordered by package name. This is probably harmless: the same pages show no rating, which points to few German ratings. But the set includes apps with more than a million installs worldwide (Periodenkalender Paula has about 3.5 million). Remedy: state the rule and the count, and explain why these apps cannot reach the cut-off.

### W8: Where the frozen snapshot and screening file are archived is not stated
**Severity**: Minor
**Evidence Anchor**: absence: Appendix B — expected a statement of where the collected search results, store pages and screening decisions are archived; checked Chapters 4 and 5, Appendix A, Appendix B prose and Listings B.1–B.2
**Confidence**: 4 — the files exist in the repository with checksums, but the text does not point to them

The script cannot reproduce the sample without search.json, pages.jsonl and the screening file, and the text reports only four of the 53 decisions. Remedy: state where the snapshot (with checksums) and the screening file, with the rule and reason for each app, are archived, and list every screened app with its decision in an appendix table.

### W9: The main-function category is reported, but the rule for assigning it is not stated
**Severity**: Minor
**Evidence Anchor**: text: §5.1 (The sample) "By main function, 22 apps track activity"
**Confidence**: 4 — searched Chapter 4 and Table 4.1

No rule in Chapter 4 says how the category is assigned or by whom. Table A.1 labels Headspace as Mood, although its title names sleep and meditation; a stated rule would make cases like this checkable. Remedy: add one sentence to §4.3 or §4.4.

### W10: The stated reason for the preinstalled rule does not apply to the actual case
**Severity**: Minor
**Evidence Anchor**: text: §4.4 (Preinstalled app) "their review counts understate how many people have them"
**Confidence**: 3 — design logic

Samsung Health ranks 8th and would have been selected anyway. In a fixed 49+1 design, the rule's net effect is therefore to admit one more ranked app (Headspace, rank 54). §5.1 reports this honestly. Remedy: add one sentence to the methodology on what the rule does when the vendor's app ranks above the cut-off.

**Questions for the author.**
1. Who screened? Did a second person check any decision, and were the carried-over decisions re-read in full on the 21 November pages?
2. Was the pool and order of the 66 generic terms fixed before the check? What would the sample be under the smaller set {smartband, scale, Waage}?
3. Why do 26 queries return fewer than 30 apps? Is the served page shorter, or does the parser miss results? Have you compared the parser output with the displayed page for a few queries?
4. Does the review count reflect the German storefront or German-language reviews?
5. Why a depth of 30? Was it fixed before any search, and is it the limit of the server-rendered page?
6. Are the eight Leap policies one text, and how will RQ results weight them?

**Statistical reporting (Step 4a).** NOT_ASSESSED: the chapters report descriptive counts only, and no inferential statistic is used or needed at this stage.

**Methodological fallacies.** Visibility (survivorship-type) bias: the frame contains only apps that reach the top 30 for a query, which is why Polar Flow, with 10,314 reviews, is missing (W5, W2). Confirmation-type circularity: a reference list is used both to tune the queries and to validate them (W2). The checklist's inferential fallacies do not apply, because no inference is drawn yet.

## Arithmetic Receipts

no_recomputable_statistics: Chapters 4-5 and Appendices A-B report only counts, ranges and shares (49 and 54 queries, 1,220 results, 704 apps, 53 screened, 72.3%, 39.3%, 54%, 30%); no test statistic, df, p-value, mean or SD is reported, so p_from_test_statistic, grim, grimmer and n_from_df do not apply
