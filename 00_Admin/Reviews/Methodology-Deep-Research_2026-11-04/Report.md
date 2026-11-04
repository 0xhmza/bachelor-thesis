# Methods evidence for the methodology repairs (deep research, 4 November 2026)

**Question (confirmed by the author, 2026-11-04):** How do published studies (a) estimate corpus- and document-level quantities from LLM labels checked by humans on an unequal-probability sample, (b) define coverage, negation and combination rules when coding privacy text against a harm or threat model, and (c) fix interface-inspection and language-version procedures? Which of these practices can a one-person bachelor study adopt?

**Input:** the ChatGPT submission review of 4 November 2026 (`00_Admin/Reviews/Methodology-Submission-Review_2026-11-04`): synthesis R1–R9, the five role cards and the citation audit. This report answers the parts of R1–R4, R7 and R9 that literature can answer. R5, R6 and R8 are execution and bookkeeping tasks for the author and supervisor. **Review form:** the author did not choose a review form when asked, so this is a targeted methods-evidence review, not a systematic review.

**Verification:** every source below was checked against its publisher, proceedings or arXiv record (title, authors, venue, pages). Claims drawn from abstracts are marked. Sources I could not verify against a primary record are not used.

---

## 1. Estimation (SQ1 → R1, R2, R7)

### What the literature offers

- **The difference estimator is the common core.** Design-based supervised learning combines a model prediction for every unit with a probability-weighted correction from a gold-labelled sample. It needs known, positive inclusion probabilities, and it is valid even when the predictions are biased (Egami et al. 2023, §2 Assumption 1, §4). Prediction-powered inference builds the same correction (a "rectifier") for means and other estimands (Angelopoulos et al. 2023). For an additive unit total *T* = Σ*y*ᵢ with fixed predictions *g*ᵢ, the estimator is
  *T̂* = Σ_{i∈U} *g*ᵢ + Σ_{i∈S} (*y*ᵢ − *g*ᵢ)/πᵢ.
  This is the Horvitz–Thompson estimator applied to the residuals *y* − *g* (Horvitz & Thompson 1952).
- **Stratified sampling is supported, and helps.** Stratified PPI derives valid intervals under stratified sampling. It narrows them when the auto-rater's accuracy varies across strata, which is exactly the V1–V5 situation (Fisch et al. 2024; abstract and §1).
- **Targeting the human budget where the model is unsure is legitimate,** as long as the inverse-probability weights are kept. Active statistical inference prioritises labels where the model is uncertain and keeps valid intervals (Zrnic & Candès 2024). Confidence-driven inference applies this to LLM annotation in computational social science and cut human annotations by over 25% at equal validity (Gligorić et al. 2025, abstract).
- **Recall for rare positives needs samples from the "unretrieved" side.** E-discovery samples the retrieved and the unretrieved segments separately, stratifies each, and computes recall intervals from the two yields. Normal approximations cover poorly, and beta-binomial intervals are closer to nominal coverage (Webber 2013). In the TREC Legal Track, assessor error often had a larger effect than sampling error (Webber et al. 2010; summarised by Tomlinson & Hedin 2011). That is evidence for keeping a single-human check apart from double-coded reference labels.
- **Stratified and cluster designs, and their variances, are textbook survey methods** (Lohr 2021, chs. 3–6). Units are drawn from mutually exclusive strata by simple random sampling without replacement, so πᵢ = *n*_h/*N*_h. The design variance of the total of residuals *d* = *y* − *g* is Σ_h *N*_h²(1 − *n*_h/*N*_h)*s*²_{d,h}/*n*_h. That interval describes audit uncertainty **within the fixed corpus** (finite-population inference). It does not describe sampling of apps or providers.

### What this means for the thesis

1. **R2, overlapping strata.** Use a **priority partition**. Each unit goes to the first stratum it qualifies for, in the order V1 disagreement → V2 uncertain → V3 vocabulary without high-stakes label → V4 interface → V5 rest. Draw by simple random sampling without replacement within each stratum, with a census of any stratum smaller than its allocation. Then πᵢ = *n*_h/*N*_h exactly, and no multiple-frame correction is needed.
2. **R1, additive quantities.** Use the difference estimator above. *g*ᵢ is the mean of the two models' indicators for a code (0, ½ or 1, with an uncertain answer counting as ½ for that model). Variance is the stratified formula. Intervals are stated as uncertainty within the fixed corpus, and provider bootstrapping is dropped.
3. **R1, app and pathway maxima** ("does the app ever mention …", "highest level reached"). These are nonlinear. A unit sample does not identify them, and no cited source supplies an estimator for them from a unit-level audit. Two honest options:
   - (a) Audit whole app–code clusters. A probability sample of apps is read in full for the high-stakes codes only (cluster sampling, Lohr ch. 5), which gives an app-level estimate of false "silence".
   - (b) Report app and pathway maxima as **detection summaries**, with their limits stated, next to the corrected unit totals.

   The revision makes (b) the default and (a) an optional extension that depends on capacity. Option (a) means reading a few whole policies, which conflicts with the "no person reads everything" constraint, so it stays the author's decision.
4. **R2, positivity.** Pilot and test units cannot enter the validation sample, so the corrected target is the **independent corpus**. Pilot apps are coded by the author in the pilot anyway; their results are reported separately as development material and never as independent model performance.
5. **R7, joint misses.** Estimate the high-stakes mentions that both models missed from **all** strata with their weights (the Horvitz–Thompson total of units where *y* = 1 and *g* = 0), not from V3 and V5 alone. Report recall intervals with beta-based (Jeffreys) intervals where counts are small (Webber 2013). A single human check outside the sample is a "checked" label. Only settled double-coded labels are reference labels.
6. **R7, agreement.** Compute α on binary unit×code indicators of the unweighted sample, with the enriched composition stated. Report α as undefined where a code shows no variation. A set-valued alternative uses the MASI distance (Passonneau 2006). The .800/.667 rules are Krippendorff's guidelines (2019, pp. 356–357), not proof of validity.

## 2. Measurement semantics (SQ2 → R3, R4)

- **Negation is part of meaning, not absence.** PolicyLint models negative statements explicitly, because "not sharing" and "sharing" are different statements about the same practice. It found contradictory statements in 14.2% of 11,430 app policies (Andow et al. 2019, pp. 585ff.). → **R3:** a denial is a *mention* with negative polarity. The revision separates polarity-neutral mention coverage from affirmative coverage and reports denials in their own column.
- **Completeness of a flow description depends on its parameters.** Contextual-integrity annotation codes sender, recipient, subject, attribute and transmission principle. The method flags policy statements that leave one or more parameters unstated as incomplete (Shvartzshnaider et al. 2019, HCOMP pp. 162–170). → **R3/W1:** a harm mention credits a pathway only where its consequence and its data or actor scope match. A mention whose scope is unclear is kept as a category-level mention with the label "scope unclear".
- **Tree semantics.** In the multiset semantics of attack trees, a tree denotes a set of alternative attacks, each a bundle of components that together suffice (Mauw & Oostdijk 2005, LNCS 3935 pp. 186–198). → **R4:** OR+ is written as an OR of explicitly sufficient AND-bundles. A combination the sources do not establish stays uncertain. Each capability names its actor, and the actor's access is a component of its own.

## 3. Inspection and language versions (SQ3 → R9)

- **Privacy choices have distinct scopes.** An expert inspection of 150 websites assessed data deletion, email opt-outs and targeted-advertising opt-outs separately. It recorded locations and action paths, and found that many sites did not say what an opt-out covers or when deletion completes (Habib et al. 2019, SOUPS pp. 387–406). Account deletion varies across platforms and devices, and one-third of users' deletion attempts were never completed (Schaffner et al. 2022, PACM HCI 6(CSCW2), abstract). → **R9/W3:** T5–T7 get structured subgoals: recipient or purpose, local/account/server scope, the action offered, the endpoint, and any partial remainder. Account deletion and data deletion are separate outcomes.
- **Language versions are often jurisdiction versions.** The MAPP corpus pairs English policies for US users with German policies for German users, and their disclosures differ (Arora et al. 2022). After the GDPR, policies for EU and non-EU audiences diverged (Linden et al. 2020, PoPETs 2020(1) pp. 47–64). → **R9/W2:** English first, *among the versions that apply to users in Germany*. The capture record states each document's territorial scope.
- **Matched states** for bilingual interface captures, and **lay scenarios** for the walkthrough persona, are not settled by a specific empirical source. They stay the study's own procedural rules, stated as such. Wharton et al. (1994) require the user description and the task as explicit inputs.

## 4. What the literature cannot settle

- sample sizes and allocations (they need the pilot's prevalence and timing);
- who the second coder is and how much time they have (R6);
- whether option (a), whole-app audits, fits the budget;
- the sufficient combinations for K10 and the other pathways, which must be argued from the tree sources and checked by the second person (R4);
- reconciling the instrument bundle (R5).

The revision marks these as proposals or TODOs rather than as settled rules.

## Sources (verified)

- Andow, B. et al. (2019). PolicyLint: Investigating internal privacy policy contradictions on Google Play. *USENIX Security*, 585–602.
- Angelopoulos, A. N. et al. (2023). Prediction-powered inference. *Science* 382, 669–674.
- Arora, S. et al. (2022). A tale of two regulatory regimes. *LREC*, 5460–5472.
- Egami, N. et al. (2023). Using imperfect surrogates for downstream inference. *NeurIPS* 36.
- Fisch, A. et al. (2024). Stratified prediction-powered inference for effective hybrid evaluation of language models. *NeurIPS* 37. doi:10.52202/079017-3541.
- Gligorić, K., Zrnic, T., Lee, C., Candès, E., & Jurafsky, D. (2025). Can unconfident LLM annotations be used for confident conclusions? *NAACL*, 3514–3533. doi:10.18653/v1/2025.naacl-long.179.
- Habib, H. et al. (2019). An empirical analysis of data deletion and opt-out choices on 150 websites. *SOUPS*, 387–406.
- Horvitz, D. G., & Thompson, D. J. (1952). A generalization of sampling without replacement from a finite universe. *JASA* 47(260), 663–685.
- Krippendorff, K. (2019). *Content Analysis* (4th ed.), pp. 356–357 (locator from the citation audit).
- Linden, T. et al. (2020). The privacy policy landscape after the GDPR. *PoPETs* 2020(1), 47–64. doi:10.2478/popets-2020-0004.
- Lohr, S. L. (2021). *Sampling: Design and Analysis* (3rd ed.). CRC Press.
- Mauw, S., & Oostdijk, M. (2005). Foundations of attack trees. *ICISC 2005*, LNCS 3935, 186–198. doi:10.1007/11734727_17.
- Passonneau, R. (2006). Measuring agreement on set-valued items (MASI). *LREC*.
- Schaffner, B., Lingareddy, N. A., & Chetty, M. (2022). Understanding account deletion and relevant dark patterns on social media. *PACM HCI* 6(CSCW2). doi:10.1145/3555142.
- Shvartzshnaider, Y. et al. (2019). Going against the (appropriate) flow. *HCOMP* 7(1), 162–170. doi:10.1609/hcomp.v7i1.5266.
- Webber, W. (2013). Approximate recall confidence intervals. *ACM TOIS* 31(1).
- Webber, W., Oard, D. W., Scholer, F., & Hedin, B. (2010). Assessor error in stratified evaluation. *CIKM*, 539–548. doi:10.1145/1871437.1871508.
- Zrnic, T., & Candès, E. J. (2024). Active statistical inference. *ICML*, PMLR 235, 62993–63010.

**Not used:** Wang et al. 2024 (CHI). The citation audit could not check its full text, and under the rule that an unverifiable claim is a failed claim, its claim is removed from the chapter. OPP-115's "Does/Does Not" attribute could not be confirmed in the ACL paper, so OPP-115 is not cited for negation.

*AI disclosure:* this report was compiled with an AI research assistant (Claude). Sources were retrieved and checked against their records by the assistant; the author has not yet read them.
