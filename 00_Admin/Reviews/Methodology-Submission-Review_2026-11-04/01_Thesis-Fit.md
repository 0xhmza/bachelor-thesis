# Thesis-fit review card

Role: thesis-fit seat, adapted from the academic-paper-reviewer journal-fit role. Scope: bachelor's thesis contribution, scope, coherence, feasibility and final-submission readiness. This is one reviewer card, not an editorial synthesis or an institutional grading decision.

Calibration status: **NOT_CALIBRATED**. Fresh role-separated context; same model family as the panel. No venue criteria, sprint contract, numeric scores, prior reviews or peer outputs used. References to earlier reviews inside current decision records were treated only as provenance of the current choices.

Assessment basis: the complete current `03_Thesis/chapters/04_methodology.tex`, introduction, abstract, current results status and relevant result passages, discussion and conclusion status, `00_Admin/Decision-Log.md`, D8–D10 and D12 records, and the organized 13 October supervisor notes. I did not audit underlying PDFs, raw data or the estimator implementation. The criteria below come from the assigned remit and project/supervisor instructions, not a supplied university assessment rubric.

## Overall assessment

**A credible bachelor's thesis design with a potentially useful contribution, but not ready for final empirical-thesis submission.** Substantial completion and verification are required. This conclusion concerns the current manuscript's readiness; it does not establish that the intended study is infeasible or that its findings will be weak.

The design asks a coherent communication question: whether providers move beyond naming data and inferences to explaining consequences, and how the protection they describe relates to applicable harm pathways. A common reference model and the same codes across policies and interfaces give the work an identifiable analytical contribution. The scope also excludes several expensive and unsupported claims: app security, actual downstream harms, provider intent and effects on users.

The main risk is the distance between the specified design and demonstrated execution. Sampling and a reference model have been reported, but the one-app instrument test uses invented interface material and AI-prepared reference records. It is not a completed pilot or independent validation. The planned real study also depends on a second person whose identity remains open, and on a pilot that must establish workload and settle collection choices. Final readiness therefore requires actual evidence for the agreed empirical contribution, human verification of the evidence foundations, and a manuscript that consistently describes what was really done. A smaller defensible claim set is preferable if resources require a supervisor-approved scope change; expansion is unnecessary.

## Criterion-bound judgements

| Dimension | Criterion source | Judgement | Evidence | Rationale and scope limit | Decision bearing |
|---|---|---|---|---|---|
| Contribution and disciplinary fit | Assigned thesis-fit remit; supervisor notes lines 10–19, 99–101 | Partly meets | text: methodology lines 93–108, "Which data flows, capabilities and harms are mentioned"; introduction lines 8–10, "A documented literature search will test and refine this proposed gap." | The contribution is identifiable, but novelty and completed empirical value are still provisional. No university rubric supplied. | Yes: final contribution must match verified evidence. |
| Bounded scope and RQ coherence | Assigned remit; confirmed D15 and D17, decision register lines 29–31 | Meets at design level | text: methodology lines 160–166, "No user study is conducted."; lines 1300–1303, "listings and marketing material are not coded surfaces." | One health-tracker domain and two coded surfaces form a coherent scope. Execution and document-wide alignment remain open. | Yes: preserve the scope when stating conclusions. |
| Feasibility | Assigned remit; supervisor notes lines 85–95 | Partly meets | text: methodology lines 1921–1926, "estimates capture time, coding units, manual effort and model cost"; D8 lines 15–16, "Who the second coder is remains open" | The design contains the right feasibility checkpoint, but its resource assumptions have not been demonstrated. No submission deadline or confirmed staffing was supplied. | Yes: feasibility is conditional on the real pilot and staffing. |
| Final-submission readiness | Assigned final BA submission remit; project evidence and decision requirements | Does not meet yet | text: results lines 567–571, "It gives no estimate for the sample."; conclusion lines 4–5, "To be written." | Substantive empirical work and the concluding argument remain unfinished; this is more than copyediting. | Yes: current chapter cannot represent a completed study. |

## Strengths

### S1. The analytical contribution has a clear shape

The chain from app components through capabilities to harms offers a specific way to explain a communication gap, and the four research questions separate coverage, stance, protection and surfaces. It is a reasonable bachelor's thesis contribution without requiring a new general theory or a user experiment.

**Evidence Anchor:** text: `03_Thesis/chapters/04_methodology.tex:31–45`, "The study asks which harms providers communicate."; `:99–108`, "How do coverage, stance and protection claims differ between privacy policies and inspected interfaces?"

### S2. The scope places sensible limits on what can be concluded

The explicit separation between communicated claims and actual technical effectiveness protects the thesis from promising an app audit it cannot perform. Captured policy text and analyst judgments are also kept distinct from user behaviour.

**Evidence Anchor:** text: `03_Thesis/chapters/04_methodology.tex:160–166`, "the study tests neither the apps' behaviour nor their security."; `:2097–2099`, "The study cannot establish provider intent, actual harms or effects on users."

### S3. Existing infrastructure makes a focused study plausible

Frozen store material, reported sampling, a machine-readable model and an explicit pilot/freeze stage provide useful groundwork. The methodological chapter already links each RQ to material, a measure and a precedent. These are substantive assets even though they do not demonstrate completion of the empirical study.

**Evidence Anchor:** text: `03_Thesis/chapters/04_methodology.tex:115–116`, "ties each research question to what is measured, the material, the method and its precedent."; `03_Thesis/chapters/05_results.tex:556–562`, "A tested script checks that every node a tree uses exists".

### S4. Preliminary work is candidly labelled

The instrument-test subsection states that its interface input is invented and its reference coding is an AI stand-in. Preserving these distinctions helps the author use the test as development evidence without passing it off as fieldwork or validation.

**Evidence Anchor:** text: `03_Thesis/chapters/04_methodology.tex:1905–1911`, "Nobody opened the app."; "It is not validation, since both come from one vendor."

## Weaknesses and minimum remedies

### W1. The promised empirical contribution has not yet been delivered

**Severity:** Major — a final-submission readiness blocker, not evidence that the proposed method is unsound.

**Evidence Anchor:** text: `03_Thesis/chapters/05_results.tex:794`, "Not answered: the only interface in the test is invented"; `:800–807`, "To be written."; `03_Thesis/chapters/07_conclusion.tex:4–8`, "To be written."

**Confidence:** High — directly stated manuscript status; no claim about unreported work outside the reviewed material.

The current results establish sampling, construction of the reference model and operation of a preliminary pipeline. They do not yet answer the four questions for the intended empirical sample. A polished methodology alone cannot support the advertised final thesis contribution.

**Minimum final-submission remedy:** perform and report the agreed real collection, pilot/freeze, coding and validation necessary for the retained questions; then write results, discussion and conclusion from those observations. If the intended contribution is deliberately narrowed, document the author/supervisor decision and revise the RQs and claims accordingly. Keep synthetic test records clearly separated from empirical evidence. Do not invent outcome values or fill result sections from expectations.

### W2. The minimum viable study remains conditional on unconfirmed resources

**Severity:** Major.

**Evidence Anchor:** text: `03_Thesis/chapters/04_methodology.tex:1961–1964`, "The sample holds at least 500 units"; `:1982–1984`, "Who is the second coder?"; `:2033–2036`, "If time runs short".

**Confidence:** High about the dependency; moderate about total workload because no real pilot timings, staffing commitment or deadline were supplied.

The same second person is expected to double-code the validation sample, check reference pathways and judged decisions, and rate recorded walkthroughs. Fifty inspections with seven tasks, language counterparts, transcription checks and human review add substantial work around the automated coding. The proposed fallback covers V1 and V2 only, whereas the main procedure describes independent coding of the whole validation sample. That is a different level of evidence, not simply fewer hours. The proposed reduction of the interface stratum could also narrow the support for RQ4.

**Minimum final-submission remedy:** use the real five-app pilot to record actual effort and cost, confirm the second person's availability and tasks, and adopt a feasible collection/validation plan before main coding. Record the resulting scope in the decision log. If a fallback is used, explicitly state which independence, reliability and surface-specific claims remain supportable. The planned two-week intra-coder interval must also fit the actual schedule. This finding does not require hiring extra researchers or adding inspections.

### W3. The evidence supporting the reference yardstick and research gap is unfinished

**Severity:** Major.

**Evidence Anchor:** text: `03_Thesis/chapters/04_methodology.tex:501–502`, "Check every decision"; `03_Thesis/chapters/05_results.tex:8–10`, "currently inconsistent with it."; `:168–169`, "the university library was not tried."

**Confidence:** High — explicit unresolved checks in the current manuscript and D14 register entry.

The literature is foundational here: it supports both the claimed gap and the pathways against which omissions are judged. The results still report superseded search routes/rules, screening decisions await author checking, and retrieval has not reached the stopping rule the current method specifies. The second-person source check of the trees is also still proposed. A structured pipeline does not substitute for settling this evidence base.

**Minimum final-submission remedy:** reconcile the retained corpus and search/screening results with the adopted D14 procedure, complete the stated retrieval attempts or record the justified terminal status for unresolved records, and check the screening/extraction decisions that support the trees and gap. Complete and report the promised source review of the pathways before freezing the yardstick. Verify or remove the unread De and Le Métayer 2017 method claim flagged at methodology lines 640–642. State the contribution as an evidenced, bounded extension of preceding work; a claim that no similar study exists is unnecessary.

### W4. The selected sample still needs accountable human sign-off

**Severity:** Major.

**Evidence Anchor:** text: `03_Thesis/chapters/05_results.tex:405–410`, "Check every decision"; "Check them before this section states who decided."

**Confidence:** High — the results explicitly identify unresolved eligibility and cross-store identity checking.

The sampling infrastructure is a strength, but the final sample's identity and eligibility decisions are still described as AI-prepared. Since those decisions determine which providers supply the empirical evidence, their verification is essential work, not an optional extension to the sample.

**Minimum final-submission remedy:** have the author check the retained screening and identity decisions against the archived evidence, record any corrections, regenerate affected selection/sensitivity outputs, and accurately state who screened and decided. This does not require a second independent full sampling study.

### W5. The surrounding manuscript still describes a different study

**Severity:** Minor — clarity and coherence repair; the adopted method's central question survives.

**Evidence Anchor:** text: `03_Thesis/chapters/00_abstract.tex:5–7`, "privacy policies, store listings and provider websites"; `03_Thesis/chapters/04_methodology.tex:1300–1303`, "listings and marketing material are not coded surfaces."; `03_Thesis/chapters/01_introduction.tex:36`, "the three major applications pre-installed by device manufacturers."

**Confidence:** High — direct cross-document comparison.

The abstract promises coded sources outside the confirmed D17 scope and still says the LLM methodology is unspecified. The introduction fixes three preinstalled apps in the scope instead of distinguishing the selection rule from its observed result. Expected contributions and the thesis roadmap are unfinished. These mismatches make it harder to see what the final thesis actually contributes.

**Minimum final-submission remedy:** after the study scope and findings are settled, align the abstract, introduction and chapter summaries with the two coded surfaces, actual model/human roles, rule-based sampling and completed contribution. Remove or resolve draft marks only through the author's normal decision process. Do not let wrapper text reopen already confirmed scope decisions.

## Essential work versus optional enhancement

Essential for the currently promised final thesis: real evidence for retained RQs; the agreed pilot/freeze and executable validation; accountable screening and identity decisions; a verified, documented reference yardstick; a consistent method/results record; and results-based discussion and conclusion. A defensible null or sparse result is acceptable. If named harms are rare, retain the prespecified secondary wording analysis and report the resulting limits rather than manufacturing a rich stance analysis (methodology lines 1857–1862).

Optional enhancement: more than 50 apps, both-platform inspection of every app, additional coded marketing surfaces, a user study, hardware/security testing, extra model families, or an expanded theoretical framework. None is needed to make this bachelor's thesis valuable. Resource changes that remove support for an existing RQ are scope decisions, not optional polish.

## Questions for the author/supervisor

1. Who can commit to the second-person tasks, and what real pilot measurements will determine the feasible validation allocation?
2. Does the supervisor accept the generic reference model as the intended reading of “best app” (D12), and what precise post-harm mechanisms were meant in the meeting notes?
3. If the complete planned study cannot fit the actual submission schedule, which contribution and RQs will be formally retained? No deadline was supplied, so this report cannot choose that trade-off.

The design merits completing as a focused communication study. Its readiness depends on closing the stated empirical and evidence checks, not on adding a broader research programme.


## Synthesis note

This role card was committed before the panel synthesis. Use [Citation-Audit.md](Citation-Audit.md) for final source and access verdicts: the actual De2016 proceedings paper and published Iwaya/Rodriguez papers were obtained; a free De2017 manuscript was obtained. These retrievals supersede earlier access observations, but do not settle the design issues.
