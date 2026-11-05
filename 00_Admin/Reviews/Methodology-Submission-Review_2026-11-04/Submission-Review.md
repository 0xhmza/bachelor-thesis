# Methodology submission review — 4 November 2026

**Assessment: major revision and completion before final empirical-thesis submission.** The current design has a coherent contribution: a source-linked reference model, app-specific applicability, and a comparison of how far policy/interface wording reaches from data practices to consequences. Keep that contribution and its clear communication-only scope. The immediate need is to make the measurement and validation executable and to complete the empirical evidence required by the retained research questions. A larger sample, a new user study or more communication surfaces are not necessary repairs.

**Reviewed snapshot:** commit `4ed6672`, `03_Thesis/chapters/04_methodology.tex`, 2,099 lines; SHA-256 `86528ad0cd4c5b854e7b3823a9d4328617f5aa43bb5ba5a0d3780e3cf0874ab7`. All chapter line references below refer to that snapshot. Relevant current decision records, instruments, supervisor guidance and results status were checked to interpret it. Citation checking is restricted to this chapter; checks elsewhere are limited to consistency/readiness.

**Review status:** `NOT_CALIBRATED`. The five roles were accepted by the author and executed in fresh, role-separated contexts from the same model family. They are not independent human experts, and agreement among them is not evidence of independent error processes. The synthesis below weighs their source-anchored arguments. It does not count votes or assign a thesis grade. The thesis and decision register have not been revised by this review.

## What has already improved

The current chapter supersedes the earlier one-model/ten-whole-app validation plan. It now uses two model families, hides proposed model answers during human checks, samples coding units across informative strata, and proposes error-corrected estimates. RQ4 is already narrowed to privacy policy versus inspected interface. It retains apps with missing policies or blocked inspection, separates non-finding from absence, and labels the invented walkthrough and AI stand-in coding honestly. Several earlier review criticisms therefore no longer describe the current text.

These are worthwhile design improvements. Their specifications and supporting evidence still need the repairs below. Two-model agreement alone is correctly not treated as human reliability; preserve that boundary.

## The five-perspective debate

| Role | Strongest case for the current design | Challenge that survives that defense | Synthesis |
|---|---|---|---|
| Thesis fit | One health-tracker domain, two coded surfaces and explicit limits give a plausible bachelor-thesis contribution. | The manuscript still documents a planned main study and a synthetic development test; its final RQ results, discussion and conclusion are unfinished. | Preserve the scope. Complete the retained empirical work, or agree and document a narrower contribution before changing the claims. |
| Methods | Stratified human auditing can concentrate effort and support useful model-assisted inference. | Unit-label error correction does not automatically correct app/pathway maxima or any-mention indicators. The estimator, target population, stratum overlaps and variance procedure are unspecified. | Fix the estimands and executable sampling/estimation design before claiming valid intervals. |
| Privacy/domain | A common author-built harm model is a defensible, traceable yardstick; being author-built is not itself circularity. | Category-wide credit, exclusion of denials and OR+ treated as OR can change what the study calls covered or applicable. | Repair those operational definitions and test their boundary cases before freezing the trees/codebook. |
| Usable privacy | English-first follows the recorded supervisor/author choice. Bounded analyst walkthroughs and access-barrier reporting fit the scope. | The English document must actually apply to German/EEA users; route states, composite-task success and bilingual comparison need executable rules. | Retain the agreed language rule, add jurisdiction and matched-state checks, and finish the real pilot. |
| Devil’s advocate | The chapter already rejects claims about actual security, realised harm, provider intent and observed user performance. | A difference from a researcher’s catalogue does not by itself prove a disclosure obligation, concealment or understatement of actual risk. | Describe a dated, framework-conditional communication gap. Keep stronger normative/intent claims outside the evidence. |

The panel did not establish an unrepairable flaw in the bounded descriptive study. That is different from saying the present manuscript is submission-ready.

## Repairs before the instrument freeze

### R1. Define the quantities and estimator at the level actually reported

**Priority: essential design repair. Chapter lines 1803–1809, 1845–1857, 1938–1963 and 1995–2002.**

The validation observes paragraph/interface-block labels, while the reported outcomes include whether an app mentions anything and the highest coverage level reached anywhere on a pathway. These are nonlinear aggregates. Ten repeated mentions in one app and one mention in each of ten apps can have the same unit total and different app counts. Correcting the unit total does not identify the latter.

Make an analysis specification with one row per primary outcome: target corpus, observational/weighting unit, numerator, denominator, aggregation, fixed model prediction and uncertainty source. Name and implement the estimator, including how uncertain model labels are encoded. For additive unit totals, a probability-weighted difference estimator is a plausible option. For app/pathway existence or maxima, justify an estimator for that aggregate or add probability-sampled complete app/surface or app–code audits. A feasible alternative is to keep corrected unit estimates and label app/pathway detection summaries with their actual evidential limits.

Egami and Angelopoulos support principled correction under stated designs and assumptions; neither citation establishes this study’s new aggregation, unequal-probability audit or provider-resampling procedure. Check the implemented estimator on small constructed corpora with repeated and singleton mentions, correlated errors and unequal inclusion. This needs implementation and evidence, not another assurance sentence.

### R2. Make the validation frames, inclusion probabilities and uncertainty executable

**Priority: essential design repair. Lines 1897–1900, 1931–1933 and 1944–1993.**

V1–V4 overlap: an uncertain interface unit can also be a disagreement unit. Define either a mutually exclusive precedence partition or a multiple-frame draw with exact union inclusion probabilities and duplicate handling. Specify small/exhausted-stratum rules and freeze the vocabulary/allocation before drawing.

Development/test/pilot units remain in the corpus but have zero validation inclusion. A design-based correction for the entire corpus cannot silently extrapolate to them. Give them an independently checked census contribution, or state a narrower independent target and report development material separately. Development coding must not count as independent model evaluation.

State whether intervals describe audit uncertainty within this fixed selected corpus or a wider population. The app sample is purposive/feedback-prioritised, so these intervals do not provide German-market sampling representativeness. Use a variance procedure that respects the actual validation design and relevant shared-document/provider dependence. Provider bootstrapping alone is not a derivation of validity.

### R3. Separate a mention from its polarity and from pathway-specific coverage

**Priority: essential measurement repair. Lines 99–108, 1667–1679 and 1803–1818.**

An explicit statement that a harm is impossible is still a mention. Recording denial elsewhere does not make it correct for a coverage scale to call it silent. Keep polarity-neutral mention/coverage separately from acknowledgment, prevention and denial; if affirmative-risk coverage is desired, name it separately.

Likewise, one psychological or economic harm mention cannot automatically cover every pathway in that category. Match the consequence and relevant data/actor/context to the pathway. Keep a separate coarse category-mention indicator if it is useful. Check a constructed case where one category has two different actors/pathways and only one is described. These are operational choices to record under D9/D12 before rewriting the method.

### R4. Resolve OR+ sufficiency and actor access

**Priority: essential model repair. Lines 884–885 and 1793–1797; reference-model K10/P13/P16.**

“More than one may be needed” cannot become “any single input suffices” solely because the study asks about possibility rather than likelihood. K10 currently makes this an active issue. Explicitly encode supported sufficient combinations as an OR of ANDs, or retain uncertainty where the source does not identify the combination. Ordinary OR is justified only if each listed alternative is sufficient in the named actor/context.

An on-device data item does not by itself give a provider, advertiser or other recipient the ability to use it. Make actor access/conditions explicit. Run the evaluator and affected examples again after the rule is chosen. The independent pathway check should examine those contextual prerequisites, not only whether a paper uses a similar harm term.

### R5. Bring the current instrument bundle into agreement with the chapter

**Priority: essential reproducibility repair. Chapter lines 1935–2013; codebook v5 lines 274–300; study navigation and current prompts.**

The chapter has moved to two models, sampled units, alpha and corrected estimates, but current instruments still contain the earlier ten-app/one-model workflow and old acceptance/escalation rules. Version the revised codebook, prompts/schemas, blind human sheets, validation-sampling manifest and app-decision forms. Preserve older versions as historical, as required by the project workflow.

RQ2’s new responsibility wording without named harm also needs a separate operational code; the existing named-harm stance rule does not automatically collect it. Update the authoritative instrument manifest and navigation so a second person can execute the same procedure. Then run that actual bundle in the real pilot.

### R6. Confirm second-coder capacity and use the pilot to choose a feasible plan

**Priority: essential execution decision. Lines 1381–1387, 1921–1933, 1961–1984 and 2031–2036; D8–D10.**

The same second person is expected to code validation units, check trees/app judgments and rate recordings. Their identity and capacity remain open. Confirm the person, training, tasks and time budget. Measure actual capture, transcript checking, coding, adjudication and model cost in the five-app pilot; account for the planned two-week recoding interval.

A supervisor coding V1/V2 only is a different validation design: it does not establish the same human reliability across blind-spot and interface strata. If capacity is limited, choose a smaller probability sample double-coded across the relevant strata and narrow claims accordingly, rather than treating selective disagreement-only coding as equivalent.

The proposed 500-unit total, 150-unit residual allocation, 20-positive reporting rule, precision bound and 10% sensitivity threshold are choices awaiting feasibility/precision justification. This review does not declare them numerically adequate or inadequate without prevalence/workload evidence. Do not change codes on the validation set and then call that same set untouched confirmation.

### R7. Count remaining misses across all relevant strata and retain human uncertainty

**Priority: essential analysis clarification. Lines 1735–1739, 1951–1963 and 2000–2012.**

Both models can miss a harm in a unit sampled because of a routine-code disagreement or an interface stratum. V3/V5 alone do not necessarily exhaust joint misses. Use all appropriate probability-sampled units to estimate misses with their weights. A human check can also be wrong; distinguish single-human reviewed findings from independently double-coded/adjudicated reference labels.

Report weighted precision/recall with observed denominators, prevalence and uncertainty by code/surface. A small number of positives or zero observed misses cannot certify an individual app’s silence. Keep “not found in the captured material” language where absence cannot be supported. Specify alpha’s coding representation/metric, weighting and undefined/rare-code handling; Krippendorff’s thresholds are cautious guidelines, not proof of truth.

### R8. Specify applicability scenarios, numerators and the primary weighting unit

**Priority: required before reporting. Lines 1782–1799 and 1845–1857.**

The dual applicable-only/applicable-plus-uncertain calculation is useful, but both numerators and denominators must be stated. Adding uncertain cases to a denominator is not automatically a valid lower/upper identification bound. Call them sensitivity scenarios unless bounds are derived. Choose equal app/provider weighting or explicit pathway weighting, and explain the alternative. Show source/assumption-dependent applicability so a more transparent provider is not silently penalised for revealing more pathways.

There is also a concrete counting inconsistency to check: line 1256 refers to “50 selected providers,” while the results describe 47 ranked providers plus Apple and Samsung, with two Apple apps (results lines 429–431, 520–522). The threshold denominator must distinguish 50 apps, 49 providers and the 47 ranked providers; the current sensitivity table uses the latter. This is an arithmetic/unit clarification, not a new sampling result.

### R9. Freeze executable walkthrough and bilingual rules

**Priority: required for retained interface findings. Lines 1386–1447, 1474–1579 and 1342–1355; D7/D10/D17.**

Fix platform/device/OS, account and reset states, permission/consent profile, route preparation, stopping/time rules, synthetic inputs and subgoal success criteria. Account deletion, data deletion and portability are distinct outcomes; preserve partial completion rather than one ambiguous “success.” The model’s in-app-only incapability condition must agree with the protocol’s treatment of a usable external route.

For English-first collection, verify that the selected document applies to the German/EEA user and app. Arora’s semi-parallel US/German policies are evidence that versions can differ, not interchangeable translations. Compare language counterparts in matched account/consent/task states before destructive changes, record which pairs were inspected, and define how a material difference triggers additional coding during main collection. Until then the log documents observed differences; it does not measure all effects of language choice.

Specify the lay task scenario and assumed privacy knowledge. Re-rating recordings assesses interpretation of recorded routes, not independent discovery of omitted routes. Keep that distinction and the explicit absence of a user study.

## Citation repairs and source access

The complete [citation audit](Citation-Audit.md) covers **53 references and all 127 active citation–source pairs**. The [CSV](Citation-Audit.csv), [JSON](Citation-Audit.json) and [reference/download provenance](Reference-Inventory.json) preserve every result and its source/locator.

| Verdict | Pairs | Meaning |
|---|---:|---|
| Supported | 73 | The inspected source supports the relevant narrow claim. |
| Partial/qualified | 36 | A component is supported, with an adaptation, scope or overstatement qualification. |
| Mislocated | 4 | Locator/support attachment needs correction. |
| Version unverified | 13 | Specified source copy was read; exact cited edition/revision remains unresolved. |
| Full text inaccessible | 1 | Wang2024 has not been checked against its actual paper. |

Several support qualifications concern reasonable thesis adaptations; they should be labelled as choices rather than treated as pre-validated published procedures. The most consequential citation changes are Rodriguez journal pagination, Deng’s direct LINDDUN section, Polisis’s actual hierarchical task, Xie’s extraction/validation scope, Baumann’s reporting-versus-raw-scoring attribution, and the limits of Sunyaev’s rating/download correlation. The exact occurrence remedies and page/section locators are in the ledger. Citations in comments do not appear to readers: turn necessary methodological precedents into active citations, or clearly state the rule as this study’s documented choice. Examples include the search/matching/deduplication design notes; this review did not audit every comment-only reference as if it were an active chapter citation.

**Downloads:** 11 scholarly PDFs (10 works, including two Schroeder versions) and four labelled official-web text captures were added to [the literature folder](../../../01_Literature/catalog/Audit-Sources_2026-11-04.md). Existing usable source PDFs were reused. Altogether 52 of the 53 cited references have a local source copy, including the three web references; this is not a claim that 52 exact publisher editions were verified. The complete Krippendorff book was already held privately and remains outside the new files.

**Institutional access:** Springer’s De2017 publisher edition is subscription content, but a free HAL manuscript is saved and its method checked. Hu2018 also has a free author manuscript. Several other existing accepted/manuscript copies need edition alignment; that alone does not prove a paywall. Actual published De2016, Rodriguez and Iwaya PDFs were retrieved without login. Wang2024 remains blocked by ACM/Cloudflare in both direct retrieval and the in-app browser; a normal-browser verification attempt is the next step, followed by university login only if the publisher actually requests it. This run cannot honestly say that institutional login is required for Wang. Do not certify its claim from the authors’ summary alone.

## What is still missing from the final empirical thesis

These are completion gates, not claims that the work is impossible or that unreported work cannot exist elsewhere:

- [ ] **Adopt the design choices:** resolve the marked proposals with author/supervisor evidence and update D8–D10/D12/D14 and related records before the methodology states them as final rules. This review adopts none on the author’s behalf.
- [ ] **Reconcile the literature review:** the results still report an earlier search/screening configuration; complete the required retrieval attempts, check AI-prepared screening/extraction, and align reported flow/counts with the adopted D14 procedure. “Not retrieved” and thematic ineligibility need distinct reporting. This is separate from this chapter’s citation audit.
- [ ] **Verify the selected app sample:** complete accountable human checks of eligibility, cross-store identity and provider decisions, including the current marked result passages. Keep the frozen inputs and deterministic selection provenance.
- [ ] **Check and freeze the reference model:** independent source/context appraisal of every pathway, documented/argued distinction, corrected operator semantics and tested evaluator; show what changed after objections.
- [ ] **Run the real timed pilot:** actual app inspections, actual human coding and candidate-model runs; select/freeze the two models and the operational instrument bundle using that evidence.
- [ ] **Collect and code real main-study material:** archived dated policies, authentic UI recordings/transcripts, access states, source-bound applicability and per-claim judgments. The invented test walkthrough is development material only.
- [ ] **Complete independent validation:** frozen sampler and inclusion probabilities, both coders’ unreconciled labels, reliability and end-to-end model errors, subsequent adjudication, defensible uncertainty and any justified correction at the actual reported aggregation level.
- [ ] **Answer the retained RQs:** report observed coverage, stance, protection and captured-surface comparisons with the right denominators, uncertainty and examples that challenge as well as support the expected gap. Do not infer intent, actual security or user comprehension.
- [ ] **Finish and align the manuscript:** results/discussion/conclusion, abstract/introduction/RQs, source/version locators and final method tense; remove resolved draft/done/TODO markers only when the author has actually resolved them. Preserve unresolved orange highlights.
- [ ] **Decide artifact release:** codebook/prompts/model/scripts, source manifests, reproducibility instructions and which recordings/third-party material remain private. Then build the final thesis in an isolated copy using the required bibliography passes and inspect its rendered layout.

The next useful milestone is a documented estimand/sampling specification followed by the real timed five-app pilot with confirmed coder capacity. It will show which of the proposed validation and interface commitments are feasible. A larger research programme would not close these immediate gaps.

## Review instruments and provenance

The review used the [academic-paper-reviewer roles](https://github.com/Imbad0202/academic-research-skills/blob/530659d983c2f4aa584ba3f2df224df08d90b264/academic-paper-reviewer/SKILL.md) and [claim-verification protocol](https://github.com/Imbad0202/academic-research-skills/blob/530659d983c2f4aa584ba3f2df224df08d90b264/academic-pipeline/references/claim_verification_protocol.md) from the requested repository, pinned at `530659d`. This is an adapted source-grounded review, not a schema-certified execution of that repository’s Claude-specific pipeline. Reviewer card confirmation occurred before the seats were dispatched. Graphify was queried first and returned sources were verified. Actual PDFs were read with PyMuPDF; DOI/publisher/author records corroborated identity and access where available. AI inspection does not mark author reading complete, and no methodological decision has been silently adopted.

Individual role cards: [thesis fit](01_Thesis-Fit.md), [methods](02_Methods.md), [privacy](03_Privacy.md), [usable privacy](04_Usable-Privacy.md), [devil’s advocate](05_Devils-Advocate.md). The source ledger supersedes intermediate access observations inside the cards. Their common model family and any shared source material remain limits on treating their convergence as independent corroboration.
