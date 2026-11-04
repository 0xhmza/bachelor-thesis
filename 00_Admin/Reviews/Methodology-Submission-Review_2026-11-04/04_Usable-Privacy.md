# Usable-privacy perspective review — current methodology

Calibration status: `NOT_CALIBRATED`.

Role: usable privacy / practical HCI perspective only. This is a role-separated review by a model from the same model family as the other seats, without peer reports. It is not evidence of independent reviewer errors. No scores or sprint contract were used.

Reviewed on 4 November 2026: the complete current `03_Thesis/chapters/04_methodology.tex` (substantive text L1–2099), D07, D10, D17, walkthrough protocol v7, and the current sampling-protocol amendment. Project root for every relative anchor below is `C:/Users/Hamza/Desktop/Share/Projects/bachelor-thesis/`. The initial Graphify query was verified against the underlying files. No prior review report or other seat's output was consulted. The project was kept read-only.

## Assessment

The design can support a useful descriptive comparison of provider policies and inspected interface text. It cannot establish what ordinary users understand, how often users encounter the text, whether controls work at the backend, or the frequency of actual harms; the chapter now makes those boundaries clear. No participant study is claimed or required to answer the narrowed RQ4. Its most important improvements are retaining partial access, distinguishing non-finding from absent functionality, and separating provider UI wording from linked policies and OS/ad text.

The remaining issues are operational and interpretive. Before empirical findings are presented as final, the pilot must turn the open device/platform/search/task choices into an executable frozen protocol; English-language selection needs a jurisdiction check; composite privacy-control tasks need scope-specific success criteria; and the bilingual difference-log procedure needs enough definition to support its claimed role. These are repairable without reversing the supervisor's English-first rule or expanding into a user study. The novice model also needs a narrower, explicit account of the privacy goal supplied to the analyst's imagined user.

## Criterion-bound judgments

| Criterion in this seat's remit | Authority | Judgment | Evidence | Limit | Decision bearing |
|---|---|---|---|---|---|
| Appropriate claim boundary for expert inspection | Wharton pp.106,109–111; Mahatody manuscript pp.20–22 | Meets | Methodology L160–166, L1481–1497, L1533–1536, L2097–2099 | Depends on keeping results equally bounded | Yes: permits analyst inspection without participants |
| Practical repeatability of the collection procedure | Wharton pp.109–111; current D10/protocol | Partly meets | L1389–1407, L1442–1497, L1919–1933 | Pilot and frozen session instructions are not yet evidence of execution | Yes: W1/W3 |
| Respect for surface identity and access-related missingness | D17; Malki §§3–3.4 | Meets | L1300–1325, L1538–1568, L1864–1874 | Access barriers still bound the inspected sample | Yes: preserves interpretable RQ4 |
| German-market applicability under English-first collection | D07; Arora §§6–6.1 | Partly meets | L1331–1355, L2093–2095 | Language alone does not establish a policy's territorial audience | Yes: W2/W4 |
| Plausible interpretation of novice findability | Wharton pp.109–111 | Partly meets | L1395–1417, L1473–1484 | No participant evidence about real privacy goals, literacy or recognition | Yes, if results imply general user findability: W5 |
| Reliability of judgments versus completeness of inspected routes | Mahatody manuscript pp.20–22; Malki §3.4 | Partly meets | L1380–1387; protocol L192–201 | A second video rating cannot find an unrecorded route | Scope qualifier; not an automatic demand for repeat inspections |

## Strengths

1. **The study is candid about what happened and what did not.** Methodology L164–166 explicitly excludes a user study; L1481–1484 identifies Q1–Q4 as analyst predictions; L1902–1911 labels the synthetic walkthrough and AI stand-ins. This avoids presenting simulated evidence as empirical user behavior.
2. **Access failure no longer becomes a false privacy gap.** L1389–1393, L1486–1497, L1557–1568 and L1864–1874 retain accessible evidence, require explicit evidence for unsupported functionality, keep uncertain applicability, and use task-specific denominators. This matters especially for companion apps and gated account features.
3. **Surface identity is controlled.** L1300–1325 and L1550–1555 implement D17: policies and provider UI are the coded surfaces; listings support applicability; linked policies stay policies; OS and third-party ad wording retain their origin. The new wording is suited to the narrowed RQ4.
4. **The procedure preserves contextual evidence that practitioners need.** L1456–1471 captures consent screens and initial settings before controls are changed; L1491–1497 distinguishes route taps from other actions and downstream effects; L1538–1549 requires screen-checked transcripts and interface-specific validation. A reader can trace a troubling phrase or control to a dated version and screen.
5. **English-first is an explicit governed choice with a visible limitation.** L1344–1355, L1442–1446 and L2093–2095 follow D07 instead of quietly treating English as equivalent to what German users encounter. Capturing counterparts is a constructive mitigation, subject to W2/W4.

## Weaknesses and minimum fixes

### W1 — The draft does not yet contain an executable frozen walkthrough

**Severity:** Major for a final empirical submission; expected incompleteness for a pre-pilot plan.

**Evidence anchor:** `text: methodology L1392–1393, "the platform rule for apps listed in both stores"; L1495–1496, "The pilot fixes starting states, search boundaries, time limits and completion criteria"; L1447–1448; L1919–1933; protocol L23–34.`

**Finding:** Platform choice, device/OS, concrete task scenarios, starting states, search boundaries, time limits, consent/permission profile and completion criteria materially determine which messages and controls are reachable. They remain deferred. The promise to settle them is appropriate in a plan, but it is not a procedure another analyst could currently execute consistently across all 50 apps. The second-rater identity/subset and proposed feasibility reductions also remain open (L1386–1387, L1982–1984, L2033–2037).

**Minimum fix:** After the pilot, replace each open execution choice with the chosen rule and reason in D10 and a versioned protocol; include a complete worked real task record showing initial state, search/preparation, evaluated route, Q1–Q4, endpoint, duration and stopping reason. Record the pilot's workload estimate for all apps, bilingual captures and any second ratings. Confirm or remove the proposed policy-code-review order and second-rating promises. This is a collection/final-submission gate, not a reason to invent a choice now.

**Confidence:** High: all these items are explicitly deferred in the current text; Wharton pp.109–111 supports their role as inputs.

### W2 — English-first needs an applicability check for the policy's audience

**Severity:** Major.

**Evidence anchor:** `text: methodology L1335–1336, "A supplement for another region is recorded but not coded"; L1344–1345, "English text is primary for every source"; L1350–1352; D07 L13–19.`

**Finding:** The draft excludes out-of-region supplements, but does not explicitly state how the primary English document is checked for applicability to a German-market user. An English US policy and a German EU policy may differ because their audiences differ, rather than because one translation omitted text. Arora's MAPP-59 pairs are expressly semi-parallel policies aimed at US versus German users (PDF p.1); §§6–6.1 discuss jurisdiction-specific provisions. A difference log alone cannot make a US-only policy an applicable primary representation for German users. This is a possible failure mode, not a finding that any sampled provider has such a mismatch.

**Minimum fix:** Preserve English first, but require the capture record to identify product, policy scope, territorial audience, and applicable regional sections for every primary policy. Prefer an English version demonstrably covering German/EEA users. If only an out-of-region English document exists, keep its audience label explicit and document the treatment of the applicable German policy under the existing fallback/supervisor decision; do not silently equate language availability with market applicability. Keep comparisons within matching jurisdiction and scope.

**Confidence:** High about the missing explicit check and Arora's source population; moderate about practical frequency because no sampled policy pairs were audited here.

### W3 — Composite control tasks can hide partial success and different protections

**Severity:** Major for comparative task-outcome claims.

**Evidence anchor:** `text: methodology L1434, "Turn off sharing with third parties"; L1436, "Delete the account and the data"; L1486–1492; protocol L63–79.`

**Finding:** The endpoint record is a strong improvement, but the fixed task labels still combine distinct goals. Disabling personalized advertising, analytics or one vendor is not the same control as stopping all third-party sharing. Removing a local history, an account, a server copy and community contributions are likewise different scopes. A single completed/not-found/unsupported/barrier outcome could conceal those differences unless the pilot's completion criteria explicitly preserve them. Malki directly illustrates separate controls, contradictory sharing preferences, account-only deletion and distinct device/cloud deletion (§§4.3.2,4.3.4; PDF pp.10–12).

**Minimum fix:** Keep T1–T7, but give T5/T6/T7 structured subgoal fields: data/recipient or purpose, account/local/server scope, offered action, requested versus interface-confirmed endpoint, and any partial or unresolved remainder. Apply the four neutral outcome categories per relevant subgoal or define a transparent task-level aggregation rule. Do not require backend verification. For apps without accounts, explicitly distinguish data deletion from an inapplicable account-deletion subgoal. Freeze these rules before main collection and report scoped outcomes.

**Confidence:** High that task labels are composite; moderate that they would cause actual miscoding, because a sufficiently detailed pilot protocol could resolve the ambiguity.

### W4 — The bilingual difference log is promised without a complete operating rule

**Severity:** Major if used to claim the language cost has been measured; otherwise Minor drafting incompleteness.

**Evidence anchor:** `text: methodology L1345–1346, "both are captured and their differences logged"; L1353–1355, "If the pilot shows"; L1444–1446; L2093–2095, "the difference log measures how much this matters"; protocol L26–28, L151–163.`

**Finding:** The current text does not specify the comparison unit, reviewer, classification of a material difference, completeness check, or denominator for the log. The extra-coding trigger is stated for a source noticed in the pilot; the treatment of a German-only harm/protection passage first noticed during main collection is not explicit. For UI, a counterpart pass after T5 changes or account deletion can also yield a different state rather than a language difference unless matched-state capture is specified. The protocol sensibly says all evidence precedes T7, but it does not explain how counterpart capture is placed relative to state-changing tasks.

**Minimum fix:** Add a compact template/rule: source/screen pair, jurisdiction and version, matched account/consent/setting state, English and German spans, changed node or claim scope, and reviewer judgment. State whether the same source-level trigger for extra German coding applies throughout collection, with logged instrument changes and recoding when necessary. Capture counterparts before destructive/state-changing actions or document a controlled equivalent state. Report pairs compared, unavailable counterparts and materially different pairs. Until such a procedure exists, say the log documents observed differences, not that it measures the full effect of language choice.

**Confidence:** High for the textual omissions; moderate for UI feasibility, which the real pilot must establish. This finding does not recommend replacing English-first.

### W5 — The novice is specified by app experience, but the privacy goal is still researcher-supplied

**Severity:** Minor with the current cautious claim boundary; Major only if results generalize to ordinary user success or spontaneous discovery.

**Evidence anchor:** `text: methodology L1397–1400, "no prior knowledge of this app or its privacy policy"; L1409–1417; L1476–1483; protocol L38–53.`

**Finding:** A first-time platform user can still vary greatly in privacy vocabulary, literacy, language fluency and knowledge of third-party sharing or inference. The tasks ask a novice to pursue concepts derived from an expert harm tree. Without an explicit lay scenario and supplied knowledge, a Q1 judgment about trying the right effect risks importing the analyst's privacy expertise into the imagined user. Malki's app novice is not evidence of no technical training or no privacy knowledge. This does not require recruiting users.

**Minimum fix:** Freeze a short lay scenario and assumed privacy knowledge/language competence for each task, clarify that the user is assumed to have been given that goal, and rate Q1–Q4 conditional on those assumptions. Keep findings about likely obstacles for that persona rather than prevalence of concern or spontaneous discovery. List low-literacy, disabled and coercively monitored users as outside the tested persona where relevant, without claiming their experiences were studied.

**Confidence:** High on the distinction between task instruction and spontaneous user goals; moderate on how much the planned pilot will already address it.

## Limits that are already handled; do not reopen as mandatory redesigns

- A second analyst rating the same video tests interpretation of recorded actions, not completeness of route discovery. L1383–1385 makes that distinction and protocol L192–195 is explicit. Add one sentence to the final limitations if needed; a second live inspection is an optional strengthening, not an automatic blocker.
- Access barriers and one-platform inspection restrict who and what the findings describe. The current task-specific records and separate reporting are a defensible way to preserve those limits; no paid account or device purchase is required by this review.
- Route taps are descriptive action cost on the located route. The chapter does not claim a proven global minimum or participant time. Keep that wording; Habib's action counts do not validate taps alone as a measure of usability or comprehension.
- A full policy and bounded UI capture offer unequal opportunities to mention harms. The narrowed RQ4 can still compare those captured materials. Do not interpret a policy/UI count difference as a measured difference in users' actual exposure or understanding.
- T3 concerns incident/exposure information. The marked supervisor issue at L1577–1579 must be clarified or explicitly bounded before it becomes a post-harm-response criterion; present text does not settle it.

## Final-submission gates from this seat

1. Close W1 with a real pilot and frozen executable protocol; do not describe open proposals as completed procedures.
2. Add the market-audience check in W2 before treating an English primary policy as German-market communication.
3. Resolve W3's scoped success criteria and W4's bilingual comparison/coding rule before producing final comparable outcomes.
4. Demonstrate actual captured UI evidence and validation, or narrow/withhold affected RQ4 and UI-absence conclusions in accordance with L2004–2010. The invented instrument test cannot discharge this requirement.
5. Resolve the marked second-rater, feasibility and post-harm-response promises, or transparently reduce the claims. No rule requires inventing a second inspector or user tests.

W5 is a small clarification if cautious inference is maintained. Neither English-first nor the D17 two-surface scope is itself a submission blocker.



## Synthesis note

This role card was committed before the panel synthesis. Use [Citation-Audit.md](Citation-Audit.md) for final source and access verdicts: the actual De2016 proceedings paper and published Iwaya/Rodriguez papers were obtained; a free De2017 manuscript was obtained. These retrievals supersede earlier access observations, but do not settle the design issues.
