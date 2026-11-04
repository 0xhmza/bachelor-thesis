# Methodology Review: Notes (2026-11-04)

**Reviewed:** `03_Thesis/chapters/04_methodology.tex` at commit `7a56aa2`. The instrument-test results in `05_results.tex` (§ Test Case to § Assessment of the Case) and decisions D8 and D9 are used as evidence.
**Mode:** `academic-paper-reviewer`, methodology-focus. Two seats, with cards confirmed by the author on 2026-11-04:
- Journal-Fit Reviewer, adapted to thesis fit;
- Peer Reviewer 1, Methodology.

**Provenance:**
- Both seats were run inline by one model (Claude Opus 5.5) in one session. They are role-separated, not independent reviewers.
- The review is not calibrated.
- No venue was set, so the yardstick is a bachelor thesis in usable privacy against field-general standards (`criteria_binding_unavailable`).

**Not changed:** the thesis. These notes are a separate document.

**Author's question:** the author asked specifically about the LLM-assisted coding and the two-coder validation on 10 apps. They are covered in depth in **Part 3**, and the recommended alternative is in **Part 4**.

---

## Part 0: Bottom line

**Verdict: major revision of the methods plan before the pilot.**

The chapter is careful, honest about its limits, and unusually well documented for a bachelor thesis. The reference-model and applicability logic (Steps 1 to 3, the AND/OR evaluation, the "uncertain" state) are the strongest part.

The weak point is exactly the one the author suspects. The LLM-screener plus 10-app validation design does three things wrong:

1. It validates a different procedure from the one it uses. The model is scored alone, but the main corpus is coded by a person reviewing model proposals.
2. Its validation set cannot produce the positives its own acceptance rule needs.
3. The thesis's own instrument test already shows that, in practice, it collapses into "a person reads everything".

A small change of roles fixes all three: **the person codes first, and the LLM becomes the independent second coder on 100% of the units.** Part 4 sets this out.

There are three further issues worth fixing before the pilot:
- RQ4 and the coded material do not match.
- Coding English text first for a German-market study is a threat to validity.
- RQ2 can end up nearly empty because stance attaches only to named harms.

---

## Part 1: Journal-Fit Reviewer (thesis fit)

**Strengths**
- The design is fully traceable. Each RQ is tied to a measure, a method and a precedent (Table `tab:rq-method`), and each LLM rule has a precedent (`tab:llm-steps`).
- Permissible conclusions are stated explicitly (§ `sec:limitations`). The study says what it cannot show (intent, behaviour, actual harm).
- The instrument test is reported honestly. Invented and AI-prepared inputs are tagged (`\synthtag`), and the stand-in coding is explicitly said not to be validation.
- The instruments are frozen before main collection, and later changes are logged.

**Issues**

| # | Severity | Where | Issue | Suggested fix |
|---|---|---|---|---|
| J1 | Major | Whole chapter (about 17k words of source) | It is out of proportion for a BA thesis. Sampling (§ `sec:app-sampling`) and the sensitivity checks alone are longer than most BA methods chapters, and the reader loses the thread from RQ to evidence. | Keep the decision rules in the chapter. Move the walk-throughs of examples (P1–P3 alias evidence, StatCounter arithmetic, the list of sensitivity variants) and the full LLM rule table to appendices, and keep a one-paragraph summary each. |
| J2 | Major | Feasibility | One author has to do all of these: 50 walkthroughs, coding of about 4–5k units, review of every model label, the applicability records, the mismatch review, the missed-mention audit, a recode of two apps, and the validation. The LLM was meant to save time, but the instrument test suggests it does not (see M-L4). | Run the pilot with an explicit time budget per app. Define the "minimum feasible study" (§ `sec:ethics`) **now**, in concrete terms: which RQ parts are dropped first. |
| J3 | Minor | § `sec:design`, Figure `fig:pipeline` | The figure is still marked `Draft!`, and its lower row says "Walkthrough all 50 apps", which conflicts with "inspection is attempted …" (some apps will be blocked). | Change it to "Walkthrough (attempted for every app)". |
| J4 | Minor | Contribution | The expected gap ("policies stop before the consequence") is already visible in the instrument test (no named harm in a 9,427-word policy). That is useful, but it means RQ1 risks a predictable headline. | Frame the contribution as *where* the silence starts (component, capability or harm) and *which* harm categories, not only *whether* it exists. The § Assessment of the Case paragraph already does this well, so carry it into the RQ framing. |

---

## Part 2: Methodology Reviewer: issues outside the LLM part

| # | Severity | Where | Issue | Suggested fix |
|---|---|---|---|---|
| M1 | **Major** | § `sec:material` (TODO), RQ4 in Ch. 1 and § `sec:rq-approach` | RQ1 and RQ4 name **listings and marketing** as surfaces, but only the policy and the interface are coded. Results also has an empty "Privacy Content in Advertising" section. | Decide now, not after the pilot. Either narrow RQ4 to "policy vs. interface" everywhere, or code listings with the same codebook (they are short and already collected, so the cost is low). Remove the advertising section if marketing stays out. |
| M2 | **Major** | § `sec:material`, ¶ Language | **English is primary for a German-market study.** German users mostly meet the German interface and policy, and the German version may be the binding one for them. Coding English first measures something a German user may never see. | For the **interface**, use device locale de-DE as the primary session. For the **policy**, code the version linked from the German storefront and treat English as the fallback. Code German text in German, because the model and both coders can handle it. If English stays primary, justify it (for example, the English version prevails, as for Clue) and state it as a validity limit. |
| M3 | **Major** | Axis B, § `sec:axes`; RQ2 | Stance attaches **only to named harms**. The instrument test found **no named harm** in a long, detailed policy, so RQ2 may be empty or near-empty across the corpus. | Keep the rule, which is correct and conservative, but plan for this outcome. (a) Report RQ2 with explicit denominators, as "named harms are rare; stance is coded on n units". (b) Pre-register a secondary analysis of stance-like wording without a named harm (reassurance, generic risk, responsibility language) so that RQ2 has content either way. The codebook already has these labels, so the change is in reporting, not in coding. |
| M4 | Major | § `sec:apply`, § `sec:comparison` | Uncertain pathways are "counted and reported", but RQ1's denominator is "applicable apps". It is not specified how uncertain pathways enter the coverage proportions. | Report two bounds for every RQ1 proportion: *applicable only* (conservative) and *applicable + uncertain* (upper). State this rule in § `sec:comparison`. |
| M5 | Major | § `sec:harm-trees`, Limitations ¶ Framework | **Circularity:** "missing harm" is measured against a reference model that the author built. Nobody independent checks the trees. | Have one independent check of the trees before the freeze: the supervisor or the second coder reviews each pathway against its literature source, and the outcome is logged. A short, documented expert check is enough for a BA. Report it in § `sec:instruments`. |
| M6 | Major | § `sec:walkthroughs` (D10 open) | The walkthrough is done by one analyst. A second inspection depends on D8. | A second analyst **re-rates the recorded sessions** of 5 to 10 apps (Q1–Q4 and task outcome) instead of re-inspecting the apps. That takes about 15 minutes per session, needs no device or account, and gives agreement on the outcomes. It fits the existing recording protocol. |
| M7 | Minor | § `sec:axes` | The coding unit is a paragraph, but the coding is span-based. Long paragraphs can hold several codes with different stances. | This is fine as it is. State that one unit can carry several labels (the table caption says so) and that agreement is computed per unit × code (see Part 4). |
| M8 | Minor | § `sec:selection`, ¶ Sensitivity checks | There are 12 or more sensitivity variants, but no rule says what counts as "robust". | Add one sentence: a variant counts as material if it changes more than *k* providers. Report the rest in an appendix table. |
| M9 | Minor | § `sec:instrument-test` | This is good practice. Note, though, that the stand-in coding was prepared by an AI of the same vendor as the model under test. That is stated in the text, but it should also be in the limitations, because readers skim. | Add one line to Limitations ¶ Coding. |

---

## Part 3: Methodology Reviewer: the LLM-assisted coding and the 10-app validation (in depth)

The current design (§ `sec:llm`, § `sec:validation`, D8, D9) works like this:
- the model screens every unit in three stages;
- people decide every retained code;
- the author codes 10 validation apps blind, and a second coder (still unnamed) codes the same apps;
- performance is per-code precision, recall, κ and AC1;
- a code with fewer than 20 positives or recall below 0.90 triggers manual checking.

### What is good (keep it)
- The model is treated as a screener and people decide, with validation against human labels. This is the right stance, and it follows Pangakis et al. and Törnberg.
- Every code needs an exact span that a script checks, and a code without a span is discarded. This blocks hallucinated evidence.
- An uncertain answer or a missing span goes to manual review. It never becomes a negative code.
- Raw model output is stored apart from the adjudicated labels, and every configuration is reported (Baumann et al. 2025).
- The missed-mention audit with 100 non-hit units is a good independent check of recall.
- The review triggers are a sensible acceptance rule in principle.

### The problems

**M-L1 (Critical): the validation measures a different procedure from the one used.**
In validation, the author codes blind and the *raw* model output is scored against that. In the main corpus, the author **reviews model proposals**. That is a different procedure, with a known bias: people who review pre-annotations anchor on them.
- Berzak et al. (2016) found that human correction of parser output shows a clear anchoring effect.
- Schroeder, Roy and Kabbara (2025) found that annotators who saw LLM suggestions adopted them readily. The label distribution moved toward the model, and the model's measured F1 rose from about .47 to .79 when the human-reviewed labels were used as ground truth.

So the main-corpus labels are likely to drift toward the model in exactly the interpretive codes (stance, framing, strength, mismatch), and the validation numbers will not show it.

The design does not say how a reviewer would notice a **model miss** outside the uncertain or one-run items. Main-corpus recall is therefore simply the model's recall, plus whatever the keyword audit catches.

**M-L2 (Critical): 10 apps cannot yield the positives the acceptance rule needs.**
The trigger needs at least 20 validation positives per code.
- The instrument test policy (178 units, 9,427 words, picked *because* it exercises the instrument) had **0 named harms**, **2 generic-risk units** and **0 breach, incident or notification units**. Stance therefore had 0 positives.
- Ten random apps will very likely give fewer than 20 positives for every Axis A harm code, every Axis B code and most Axis C strength and framing codes.
- So the trigger will fire for exactly the codes that RQ1 (harm level), RQ2 and RQ3 depend on. The result is that "all relevant material is checked manually", which is full manual coding by another name.

Even when a code reaches 20 positives, 18/20 (recall 0.90) has a 95% Wilson interval of **0.70–0.97**, so the 0.90 threshold cannot be distinguished from 0.70. (With 10 positives, 9/10 gives 0.60–0.98.)

**M-L3 (Major): the sampling unit is the app, but the evidence lives in units and positives.**
Ten apps means about 10 policies (fewer when providers share documents) plus their interface text. Stratifying by language is good, but the positives that matter are clustered in a few units. Sampling apps does not control how many positives you get.

**M-L4 (Major): the instrument test shows the screener saves little.**
From § What the Language Model Did:
- 113 of 487 labels were marked *unsure*, and so go to manual review.
- 47 of 203 stage-1 labels came from one run only, and are also reviewed.
- Six capability or component labels were wrong.
- The harm trigger fired, so "a person has to read the whole policy".
- The runs used about one million tokens for one policy.

The design ends up with a person reading every unit **and** checking every model label. That is more work than coding blind, and it adds the anchoring risk of M-L1.

**M-L5 (Major): the roles and wording are inconsistent across chapter and decisions.**
- § `sec:instruments` intro says the validation set is "coded independently by a second human coder", while § `sec:validation` says the author codes it blind and a second coder also codes it. Who provides the reference labels for model performance: the author, the second coder, or an adjudicated consensus?
- § `sec:validation` says **two** paraphrased prompts, Table `tab:llm-steps` says **a** paraphrased prompt, and D9 says **one**.
- ¶ Second coder says "the author therefore codes everything", which conflicts with "the model proposes; people decide" in § `sec:llm`. A reader cannot tell whether the author codes from scratch or adjudicates.

**M-L6 (Major): the second coder is still unnamed (D8).**
The whole two-coder design and the walkthrough re-check (D10) hang on this. The fallback ("the supervisor reviews a sample") is undefined: which sample, what size, which measure.

**M-L7 (Minor): the metrics.**
Cohen's κ plus Gwet's AC1 is defensible. But the thesis cites Krippendorff and does content analysis with two or more coders (human, human and model) and missing cells, which is the standard case for **Krippendorff's α**. Its customary benchmarks are α ≥ .800 for reliable data and α ≥ .667 as the lowest limit for tentative conclusions. "Correct only with the right label, unit **and evidence span**" also needs an operational span rule (for example, character overlap ≥ 50%, or the human span contains the model span). Otherwise trivial boundary differences count as misses.

**M-L8 (Minor): the model configuration.**
The instrument-test setup (fresh Claude Code subagents, no temperature or seed) cannot be reproduced, and hosted snapshots get retired. D9 already prefers an open-weight model if it is close to a hosted one. Make that decision in the pilot, and pin the exact snapshot or weights and the inference settings.

---

## Part 4: Recommended alternative: human-first coding, with the LLM as an independent second coder

### The idea in one paragraph
Swap the roles. **The author codes every unit first, blind to the model.** The model then codes every unit independently, with the same codebook, stages, span rule and uncertainty rule as now. A script compares the two. Every disagreement is adjudicated with the source of each label hidden, and the adjudicated set is the data. A **human second coder** independently codes a reliability sample of units, which gives a real human–human benchmark. The model's usefulness (the supervisor's request) is then measured on **the whole corpus** as model–human agreement and compared with human–human agreement, instead of on 10 apps.

This is LLM-assisted content analysis in the sense of Chew et al. (2023). The model supports the deductive coding and flags disagreements, and a person keeps the final decision.

### Why this is better on each problem

| Problem | Current design | Alternative |
|---|---|---|
| M-L1 anchoring | The author reviews model proposals, so labels drift toward the model | The author codes before seeing model output, so the human labels are independent of the model. The model can only add disagreements to look at. |
| M-L2 positives | 10 apps give fewer than 20 positives for harm and stance codes, so the trigger fires and nothing can be estimated | **Every** positive in the corpus is double-coded (human + model). Model recall and precision are estimated on all corpus positives, which is the largest number possible. |
| M-L4 effort | A person reads everything **and** checks every model label | A person reads everything **once**, and checks only the disagreements (in the test, mostly the 113 "unsure" labels and the one-run labels, reduced to those that differ from the author). |
| "Two coders" (D8, supervisor) | Only on 10 apps, and the second coder is unnamed | 100% of units are double-coded (human + model). A human second coder on a sample gives the human benchmark. |
| "Test whether a model can assist" (D9, supervisor) | Answered on 10 apps, with wide intervals | Answered on the full corpus: per-code α(model, human) next to α(human, human), and the number of human misses the model caught. That is a substantive result in its own right. |
| Misses | Model misses are invisible outside the keyword audit | A model miss shows up as a disagreement, and so does a human miss. Both are counted. |

### Specification (drop-in for § `sec:llm` and § `sec:validation`)

**1. Coding (main corpus, all apps)**
- **Units** are fixed by the existing script, as now.
- **Pass H (human):** the author codes all units on Axes A–C under the frozen codebook. Model output is not opened until the app is finished. Applicability, minimisation and mismatch decisions stay human-only, as now.
- **Pass M (model):** the frozen model runs the three stages on all units. Keep the span check, the uncertain → review rule and the three runs, with the union of runs as the model's label set (recall-oriented, as now). Keep one paraphrased-prompt run on the reliability sample only, because that is enough to show prompt sensitivity.
- **Compare:** a script aligns H and M per unit × code, using the operational span rule from M-L7.
- **Adjudicate:** every H/M disagreement is shown as "label A / label B", with the sources hidden and the order randomised. The author decides and logs a reason code (one of: human miss, model miss, codebook ambiguity, span boundary). Agreed labels stand.
- **Data** = agreed labels + adjudicated labels. Raw H and raw M are kept unchanged, so agreement is always computed **before** adjudication.

**2. Reliability sample (human second coder)**
- **Size and composition**, in **units**, fixed before coding:
  - **All units that carry any Axis A harm, generic-risk, Axis B or Axis C framing or strength label from either pass.** These are rare, so this stays small; it is the enriched part.
  - **Plus a random sample of the remaining units, stratified by surface and language, at about 10% (at least 300 units).**
- **Procedure:** the second coder works blind to both passes. Run a short training round on pilot units first, with no agreement reported.
- **Report:**
  - Krippendorff's α (nominal) per axis, and per code where n allows, for human–human, human–model and second coder–model, each with a bootstrap 95% CI that resamples units within providers;
  - for rare codes, prevalence and raw counts alongside;
  - the enriched part and the random part **separately**, because enrichment inflates prevalence;
  - model precision and recall against the adjudicated set **for the whole corpus**, with Wilson intervals.
- **If no second coder is found:** the supervisor codes the enriched part only. If even that fails, state plainly that human–human reliability is not estimated, and keep the model–human comparison as a secondary check (not as reliability), as the current limitation already says.

**3. Acceptance, replacing the review triggers**
- The data rest on human coding throughout, so they never depend on the model being good. Model acceptance becomes a **reported result**, not a gate.
- Corpus-wide absence claims ("no policy names harm X") need both passes and the keyword audit to agree. A unit flagged by any of the three is read.
- A code is reported as reliable if human–human α ≥ .800, and tentative if .667 ≤ α < .800. Below .667, that code is merged into a coarser code or reported qualitatively only, and this rule is fixed before coding.

**4. Keep unchanged**
- The pilot on 5 apps, the instrument freeze and the change log.
- The span check, the prompt archive, the separate storage of raw output, and the reporting of all configurations.
- The missed-mention audit (it now checks both passes).
- The recode of two apps by the author after two weeks (intra-coder).

### What it costs
Using the instrument test as the yardstick (178 units for one long policy), the corpus is roughly 50 apps, minus shared policies, at about 80–180 units each, which is about 4–6k policy units plus interface units. This is only an order-of-magnitude estimate; the pilot gives the real figure.
- **Pass H:** the author would have to read every unit anyway (the trigger in M-L2), so the new work is only recording codes while reading instead of checking model labels afterwards. With the codebook frozen and most units carrying 0–2 component codes, expect it to cost about the same as or less than the current review load. The pilot should time both procedures on 1–2 apps to settle this.
- **Second coder:** the enriched part is probably well under 200 units, plus about 300 random units. That is roughly 1–2 working days, which is realistic for a fellow student or a PhD student.
- **Model:** the same runs as now.

### Changes this needs in the text and decisions
- § `sec:llm`: rewrite the first and last paragraphs for the reversed roles. In `tab:llm-steps`, change rows *Human role* and *Doubt* and add a *Compare/Adjudicate* row; the *Wording* row stays, applied to the reliability sample.
- § `sec:validation`: replace ¶ Validation set with the reliability sample of step 2. Rewrite ¶ Performance measures using α and corpus-wide precision and recall. Replace ¶ Review triggers with the acceptance rule of step 3.
- § `sec:instruments`, intro: drop "withheld validation set of ten apps".
- Figure `fig:pipeline`: change the Coding box from "the model proposes, people decide" to "person codes, model codes, disagreements decided".
- Limitations ¶ Coding: rewrite.
- **D8** (two coders): new option 4, chosen, *"human-first full coding, model as second coder on all units, human second coder on an enriched unit sample"*. It still needs the supervisor to name the second coder.
- **D9** (LLM role): change "the model screens and proposes; people decide" to "the model codes independently; disagreements are decided by people". Acceptance moves from a gate to a reported result.
- One decision row for the supervisor: is a model that **checks** the author's coding (instead of proposing it) still "testing its usability"? Present it as a stronger test, because it is measured on the whole corpus.

### Fallbacks, if the alternative is rejected
- **B: keep the screener, but repair the validation.**
  - Make the validation sample unit-based and enriched (step 2 above) instead of 10 apps.
  - Have the author review model proposals **without seeing the model's label**: the author sees only "unit flagged for Axis X" and assigns the label themself, which reduces anchoring.
  - Code 2 pilot-excluded apps in both conditions (blind vs. reviewing) and report the difference, to measure the anchoring effect.
  - Fix the inconsistencies in M-L5.
  - Weaker than the alternative, because model misses stay invisible.
- **C: no model in the coding; the model only in the audit.**
  - Human coding plus a human second coder on a sample. The model is used only as a third "missed-mention" reader next to the keyword search.
  - Simplest and fully defensible, but it does not meet the supervisor's request to test usability beyond the audit.

---

## Part 5: Synthesis and revision list

**Decision:** major revision of the methods plan. Do these before the pilot, because the pilot freezes the instruments.

**Critical, fix before the pilot**
1. M-L1 and M-L2: replace the LLM-screener and the 10-app validation with the human-first design of Part 4, or at least apply Fallback B.
2. M-L6 and D8: name the second coder, or fix the fallback precisely.

**Major, fix before the freeze**
3. M1: align RQ4 with the coded surfaces, and remove or keep the advertising section accordingly.
4. M2: settle the language rule for a German-market study.
5. M3: plan RQ2 reporting for the case where named harms are rare.
6. M4: define the two-bound rule for uncertain pathways in RQ1.
7. M5: have one independent check of the harm trees before the freeze.
8. M6: a second analyst re-rates recorded walkthrough sessions for 5 to 10 apps.
9. M-L5: make the coder roles and the number of paraphrased prompts consistent across Ch. 4, D8 and D9.
10. J2: set a concrete minimum feasible study.

**Minor**

11. J1: move detail to appendices.
12. J3: fix the figure label and the "Draft!" mark.
13. J4: frame the contribution as *where* the silence starts.
14. M7: state that one unit can carry several labels, and compute agreement per unit × code.
15. M8: add a robustness rule for the sensitivity checks.
16. M9: add the same-vendor stand-in coding to the limitations.
17. M-L7: switch to Krippendorff's α and define the span rule.
18. M-L8: pin the model.

**Out of scope for this review:** literature-review procedure details (§ Literature Review Procedure), the generic-model construction, and the tree-by-tree content. These were read at the level of design logic only.

---

## Sources
- [Schroeder, Roy & Kabbara (2025), *Just Put a Human in the Loop? Investigating LLM-Assisted Annotation for Subjective Tasks*, arXiv:2507.15821](https://arxiv.org/abs/2507.15821): reviewing LLM suggestions shifts labels and inflates measured model performance.
- [Berzak et al. (2016), *Anchoring and Agreement in Syntactic Annotations*, EMNLP](https://people.csail.mit.edu/berzak/papers/D16-1239.pdf): anchoring in the human correction of automatic pre-annotation.
- [Chew et al. (2023), *LLM-Assisted Content Analysis: Using Large Language Models to Support Deductive Coding*, arXiv:2306.14924](https://arxiv.org/abs/2306.14924): the LLM as support for deductive coding, benchmarked against human coders.
- [Krippendorff's alpha: thresholds α ≥ .800 and α ≥ .667 (Krippendorff 2004, p. 241)](https://www.statisticshowto.com/krippendorffs-alpha/).
- Already in the thesis bibliography and relied on above: Törnberg 2024; Baumann et al. 2025; Pangakis et al. 2023; McDonald et al. 2019; Campbell et al. 2013; O'Connor & Joffe 2020; Krippendorff 2019.
- Wilson intervals computed for these notes: 18/20 → [0.70, 0.97]; 9/10 → [0.60, 0.98].
