# Methods reviewer report

Calibration status: `NOT_CALIBRATED`. Fresh methods-only invocation from the same model family as the other seats; no peer reports or earlier review reports read. No numeric scores. This is a review of a proposed design, not a report of completed validation.

Scope: full current `03_Thesis/chapters/04_methodology.tex` (2,099 lines), D8/D9/D10/D14, codebook v5, current stage prompts, walkthrough protocol v7, and study README. Project files were read only. Source anchors below use current repository-relative paths and one-based line numbers. Graphify query was used first; its returned locations were verified in source.

## Assessment

The study can support a descriptive comparison of captured provider communication against explicitly argued reference pathways. Its boundaries around technical effectiveness, user behaviour and synthetic evidence are unusually clear. The two-model design is compatible with limited human reading, but its statistical correction is presently a promise rather than an identified procedure. The most consequential gap is that validation samples paragraph/block labels while the main outcomes are app/pathway-level maxima and existence indicators. A valid correction for unit totals does not automatically correct these outcomes. The chapter also excludes development units from the gold sample while retaining them in the target corpus, leaves overlapping validation strata undefined, and depends on an unnamed second coder whose fallback changes the reference-label design. These are design issues requiring decisions and implementation before data collection, not additional citations or stronger prose.

## Strengths

- **The inferential boundary fits the material.** `04_methodology.tex:160–166`, `1481–1497`, `1533–1536`, `1566–1568`, and `2097–2099` distinguish captured text, analyst judgment, interface confirmation and actual system behaviour. No causal user-effect or technical-security conclusion is licensed. This is appropriate for the proposed content analysis and analyst walkthrough.
- **Model agreement is correctly separated from accuracy.** `04_methodology.tex:1707–1716` explicitly recognises correlated errors; `1768–1778` hides model answers during human checks and preserves raw outputs; `1986–1993` proposes end-to-end evaluation so early-stage misses count. The architecture permits useful automation without treating consensus as ground truth.
- **The intended sampling and provenance are auditable.** Frozen collections, reproducible ranking and matching decisions are specified at `1028–1040`, `1099–1127`, `1176–1199`, and `1250–1259`; model versions, reference labels and selection probabilities are promised at `2053–2059`. The app sample is explicitly not representative of all apps or German users (`2067–2074`).
- **Missing evidence is not automatically negative evidence.** `1782–1799` supplies three-valued applicability; `1845–1851` and `1864–1874` distinguish unavailable sources, uncertain pathways and inspected material. Walkthrough protocol v7:72–85 preserves bounded non-findings and barriers. These rules reduce an important source of artificial communication gaps.
- **The preliminary fixture is honestly delimited.** `1902–1911` identifies the invented walkthrough and AI stand-in coding and denies that they validate the model. `1574–1577` also labels historical classifications as pending re-evaluation. These disclosures should survive final editing.

## Prioritized weaknesses and minimum repairs

### M1 — The corrected estimator does not yet identify the main outcomes (major; first priority)

**Evidence:** `04_methodology.tex:1601–1602` counts unit/code labels; `1803–1809` defines coverage as the highest level anywhere on an app/pathway/surface; `1845–1857` reports applicable app/pathway counts and coverage categories; `1995–2002` promises corrected figures and valid intervals from a sample of units. The named procedure, equation, target population, treatment of uncertain predictions, and correction for nonlinear aggregation are absent.

**Why it matters:** an app with ten mentions of a capability and an app with one mention each count once for presence. An estimated correction to the number of positive paragraphs can estimate a unit total; it cannot simply be converted into the number of apps mentioning the capability or the number of pathways whose maximum level is two. Correlated mistakes within a policy make this distinction consequential. Provider-resampling does not repair an unidentified target/estimator.

**Minimum fix:** enumerate the estimands in a short analysis table: observational unit, target corpus, numerator, denominator, aggregation function and uncertainty source. Choose a concrete design-based difference estimator for additive unit totals (for fixed predictions g, a finite-corpus mean can use the full-corpus prediction mean plus the probability-weighted sample mean of y−g). State how uncertain labels enter g. For app/pathway maxima, either (a) add probability-sampled complete app/surface or app/pathway audits sufficient to observe their true aggregated outcome, or (b) supply and justify a specific estimator using the joint-inclusion information needed by that nonlinear target. Report uncorrected detection summaries explicitly as such if neither is feasible. Treat this as a choice, not a demand to manually read every app.

**Needs actual work:** estimator implementation; small simulated corpora with repeated mentions, within-provider dependence, false positives/negatives and unequal sampling; verification that the claimed interval targets the declared quantity. Wording alone cannot establish validity. Egami et al., §4, specifies a concrete pseudo-outcome and cross-fitting procedure; Angelopoulos et al. starts by choosing the estimand and its rectifier. Neither citation itself supplies this study's aggregation rule ([Egami et al.](https://proceedings.neurips.cc/paper_files/paper/2023/file/d862f7f5445255090de13b825b880d59-Paper-Conference.pdf), [Angelopoulos et al.](https://www.stat.ubc.ca/~john/papers/AngelopoulosScience2023.pdf)).

### M2 — Positivity, overlapping strata and interval design need a single executable sampling specification (major)

**Evidence:** `04_methodology.tex:1897–1900` and `1931–1933` retain test/pilot apps while excluding their units from validation; `1944–1963` excludes prompt-development units, lists overlapping V1–V4 conditions, and says probabilities are known for the whole corpus. A disagreeing, uncertain interface unit can satisfy three strata. No precedence or multiple-frame selection formula is stated. `1990` only says intervals resample providers.

**Why it matters:** development units have zero gold-sample inclusion in the stated target corpus. Their residual error cannot be corrected design-wise by weighting the rest. For other units, inclusion probabilities depend on whether the five categories are a partition or overlapping draws. Naive provider bootstrap can also fail to reproduce a stratified unequal-probability audit; the sample of providers is not a random sample of all health-tracker providers.

**Minimum fix:** define a mutually exclusive priority partition or a documented multi-frame draw with deduplication and exact union-inclusion probabilities. Freeze vocabulary and allocation rules before drawing, including rules for small/exhausted strata. Separate development apps as a fully human-coded census contribution, or narrow the corrected target to the independent corpus and report development apps separately. Avoid using development coding to claim independent model performance. Define whether intervals describe gold-audit uncertainty within this fixed corpus or a wider superpopulation, then choose a survey/design-respecting variance procedure with provider/document clustering where relevant. Do not interpret these intervals as German-market sampling uncertainty.

**Needs actual work:** a sampler that records frame membership, stratum, seed and inclusion probabilities, checks all target units have nonzero support (or a census gold outcome), and produces reproducible draws and appropriate replicate weights/variance. Egami et al., Assumption 1, requires known, positive gold-label probabilities; the paper's guarantee is asymptotic and conditional on its assumptions ([primary paper](https://proceedings.neurips.cc/paper_files/paper/2023/file/d862f7f5445255090de13b825b880d59-Paper-Conference.pdf)).

### M3 — Rare-label detection and high-stakes counts are less secure than the text claims (major)

**Evidence:** `04_methodology.tex:1735–1739` checks returned high-stakes labels; `1951–1963` proposes vocabulary enrichment plus 150 residual units; `2000–2007` says remaining error is only joint model misses and V3/V5 estimate it; `2008–2012` gates interface claims and some routine counts. The preliminary policy contains no harm mentions (`1941–1942`), but no observed pilot prevalence or workload exists here.

**Why it matters:** human checking can still mislabel returned candidates. Jointly missed high-stakes labels may occur in V1/V2/V4 too, for example a paragraph that disagrees only about a routine code while both models miss a harm. If V5 is the residual partition, it represents only that residual. Raw positive counts plus an overall missed-mention fraction do not correct app-level absence or rare harm/stance combinations. Twenty positives is a reporting convention, not a guarantee of useful precision; zero positives is particularly uninformative about rare misses.

**Minimum fix:** estimate missed positives using all probability-sampled strata and report actual observed numerator/denominator counts, weights and uncertainty. Distinguish single-human checked findings from settled double-coded reference findings. Define rare-code outputs prospectively: no corpus absence conclusion when precision/recall cannot be usefully bounded; retain bounded detection language and qualitative examples. Predefine a feasible precision or interval-width target for principal codes and an escalation or reduced-scope rule if pilot evidence cannot support it. Clarify that an overall unit-level recall does not certify that a particular app contains no mention.

**Needs actual work:** real pilot prevalence and time measurements, then independent gold labels and code/surface-specific error bounds. The proposed 500/150 allocation cannot currently be called adequate or inadequate numerically; its adequacy has not been demonstrated.

### M4 — The second-coder fallback does not preserve the principal validation design (major)

**Evidence:** `04_methodology.tex:1966–1984` calls every validation unit independently double-coded but permits supervisor coding of V1/V2 only. `1927–1929` also requires this person to check every tree pathway, `1381–1387` adds ten walkthrough re-ratings, and `2031–2036` leaves effort and reduction rules to the pilot. D8:15–16 confirms identity remains open and the V1/V2 fallback. `2000–2002` nevertheless treats human-checked labels as leaving only model misses.

**Why it matters:** the fallback leaves blind-spot, vocabulary and some interface units with one reference coder. It cannot establish human reliability across the corpus or the same quality of gold correction as the main design. Unit sampling may expose many or nearly all apps, so “decisions of the sampled apps” (`1982–1983`) is not a bounded app-review workload.

**Minimum fix:** before freeze, confirm a named coder, availability and actual coding budget; separate the workload for text units, source-checking pathways, app-level decisions and walkthrough ratings. Specify a scientifically coherent reduced design if the coder is unavailable: e.g., a smaller probability sample double-coded across all relevant strata, with narrower claims, rather than only difficult/disagreement units. State clearly which reference labels remain single-coded if that route is chosen. Define a sample of app-level decisions including positive and negative mismatch judgments, not just “sampled apps”.

**Needs actual work:** coder recruitment, training/calibration separate from evaluation, timed pilot double-coding and subsequent independent coding. A supervisor decision and available labour are required; prose cannot replace them.

### M5 — Current instruments implement the earlier design (major for reproducibility; straightforward pre-freeze repair)

**Evidence:** codebook v5:274–300 still prescribes ten whole validation apps, Cohen's κ/AC1, two recoded apps, a separate exhaustive lexical sweep and full-manual-review triggers; thesis `1938–2013` now prescribes sampled units, two models, α and estimated correction. Walkthrough protocol v7:189–195 still references the old manual-decision/second-inspection route. Study README:6 points to codebook v4 and walkthrough v3. D9:22 explicitly supersedes the earlier triggers. Stage prompts are labelled instrument-test only (each line 5). The RQ2 secondary outcome includes responsibility wording without named harm (`04_methodology.tex:1858–1860`), while codebook v5:165–169 and stage2:6,21 restrict responsibility stance to named harms.

**Minimum fix:** make a versioned instrument bundle matching the chosen method: codebook, stage schemas/routing, human-blind sheets, sample/weight manifest, app-decision review form and walkthrough rating sheet. Define responsibility-without-harm as a separate code if retained; do not silently re-use a harm-conditioned stance. Identify a single authoritative manifest and update navigation. Preserve old versions as historical.

**Needs actual work:** run the new bundle on the real pilot. A consistency edit is necessary now, but it does not constitute validation.

### M6 — Post-validation merging and selective reliability statistics can change the frozen target (moderate)

**Evidence:** `04_methodology.tex:1931–1933` freezes instruments and recodes affected material after changes; `1972–1978` computes α per axis/code “with enough positives” and then merges a code below a threshold. Axis codes are multilabel (`1601–1602`, `1672–1679`), and the validation sample deliberately enriches ambiguity (`1949–1955`). No representation/distance for axis α, weighted versus unweighted α, positive sufficiency rule, or independent revalidation after merging is specified.

**Minimum fix:** compute agreement on a declared representation (e.g., separate binary unit/code indicators, plus explicitly justified span/relationship agreement), state the effect of the enriched design and whether weighting is used, and retain raw prevalence/confusion tables. Distinguish unreliability from undefined/unstable α. Predefine code aggregation during development where possible. If evaluation triggers a substantive code change, freeze a new version, recode affected material and use fresh independent evaluation or label the revised result exploratory. Do not reuse a tuned validation set as untouched confirmation.

**Needs actual work:** agreement computation and, if rules change after validation, additional independent labels. Existing threshold prose cannot show that categories are reproducible.

### M7 — Applicability uncertainty is displayed but not yet propagated coherently to the reported gap (moderate)

**Evidence:** `04_methodology.tex:1782–1799` derives applicability partly from provider disclosures and applies strong assumptions to external events. `1845–1853` alternates “each harm's” app denominator, pathway denominators and two calculations with uncertain pathways. It does not specify what enters the numerator when uncertain pathways are included. `1806` counts a named harm for every pathway in its category, while codebook v5:248 requires matching the pathway's data.

**Why it matters:** disclosure supplies both the opportunity to classify a pathway as applicable and the communication outcome. Transparent providers can have more known pathways, while sparse providers have more uncertain ones. Adding uncertain pathways only to the denominator is not a general bound unless their unknown communication/applicability states are handled explicitly. Broad harm language can also cover numerous pathways by the tree's construction rather than by provider-specific evidence.

**Minimum fix:** define one primary weighting unit (equal provider/app, equal pathway, or a stated within-provider average); keep alternative units as sensitivity analyses. Write the numerator as well as the denominator for uncertain-case scenarios and label them sensitivity scenarios rather than identification bounds unless bounds are derived. Specify matching by data/actor/scope for broad harm mentions. Report documented versus argued pathways and state external-event assumptions separately so readers can see whether those modeling choices drive the gap.

**Needs actual work:** second-person appraisal of applicability and source support, and sensitivity outputs once real records exist. Definitional ambiguity is repairable in prose; sensitivity results cannot be invented in advance.

## Other scope limits

- D14:35–40 explicitly records that the collection/screening run differs from the currently stated literature procedure; `04_methodology.tex:501–502` says screening needs author checking. Since these sources construct the reference yardstick, actual reconciliation and checking are prerequisites for calling the trees frozen. I did not assess literature completeness or read previous review outputs.
- Re-rating recorded walkthroughs tests agreement on captured routes and judgments, not independent discovery of omitted routes. The chapter largely says this correctly (`1381–1385`); preserve the limitation when reporting agreement.
- No reported inferential test statistics in the reviewed methodology call for arithmetic recomputation. Proposed sample sizes and thresholds are design proposals, not empirical results.

## Smallest defensible next step

Set the target estimands and sampling/estimation specification first, then conduct the real five-app timed pilot with the proposed coder and two model families. Use that evidence to freeze a feasible, internally consistent instrument bundle and independent gold-sample design. Keep unit-level corrected estimates separate from app/pathway detection summaries until an aggregation-level correction is actually implemented and checked. This preserves the author's requirement that models do most corpus coding while avoiding unsupported certainty about app-level gaps.


## Synthesis note

This role card was committed before the panel synthesis. Use [Citation-Audit.md](Citation-Audit.md) for final source and access verdicts: the actual De2016 proceedings paper and published Iwaya/Rodriguez papers were obtained; a free De2017 manuscript was obtained. These retrievals supersede earlier access observations, but do not settle the design issues.
