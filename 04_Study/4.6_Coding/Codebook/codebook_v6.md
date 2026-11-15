---
version: 6
date: 2026-11-04
status: draft for the pilot — tree nodes from reference model v2 (D12); two-model coding and the validation sample of D9; examples to be filled from the pilot
source: current 03_Thesis/chapters/04_methodology.tex; author clarification recorded in 00_Admin/Decisions/D15_health-tracker-domain.md; harm model from Knabenhans et al. (2026), ePrint 2026/867, version of 4 May 2026
supersedes: codebook_v5.md
---

# Codebook v6

The harm model is taken from Knabenhans et al. (2026), *On the (Privacy) Harms
of the European Digital Identity Framework*, §4.1, §5 and Appendix A
(`01_Literature/library/Knabenhans_2026_PrivacyHarms-EUDigitalIdentity.pdf`, the
version of 4 May 2026; the paper was revised on 16 September 2026). Elements
that do not come from that paper are marked **[not Knabenhans]** with their
source.

**Current authority:** the thesis methodology, the supervisor guidance of 13 October and the author's confirmed clarification in D15 govern this instrument. The 5 October proposal and codebook v3 are historical versions. The study domain is health trackers overall; source-paper categories inform the scope and search vocabulary, and app features determine pathway applicability.

**Every category needs a definition, a positive example, and a
counter-example.** Without the counter-example the category is not codable:
neither a human coder nor a model has a boundary, and both drift. A category
that still has no counter-example after the pilot is merged or dropped. Every
change to a category means a new version of this file.

---

## 0. The harm model

**Harm** (Knabenhans et al. §4.1, following the CyberPeace Institute): "an
impairment or disruption of an entity's capacity or ability to function and
exist as it otherwise would have in its usual context". **Baseline [not
Knabenhans]:** the user's situation without the modelled pathway.

**Harm tree** (Knabenhans et al. §4.1): three levels.

| Level | What it is | Tracker examples |
|---|---|---|
| System component | information the system leaks, the result of an interaction, or a requirement imposed on the user | cycle data sent to a server; an advertising ID shared with an SDK; "an account is required" |
| Capability | what a set of components lets an actor do — or prevents someone from doing (an *incapability*) | distinguishing, tracking/profiling, inference; a user unable to use a feature without agreeing to data sharing |
| Harm | the impairment itself | discrimination in insurance; prosecution; distress |

**Origin** of a component (Knabenhans et al. §4.1, black/blue/red):

| Code | Origin | Meaning | Tracker examples |
|---|---|---|---|
| `O-CORE` | Core functionality | cannot be removed without stopping the app from doing what it is for | logged cycles; predicted fertile window; step count |
| `O-CTX` | Digital context | arises from running on a phone and network at all | OS/platform telemetry; store account; network metadata |
| `O-IMP` | Implementation choice | the provider chose it and could choose otherwise | advertising/analytics SDKs; cloud sync; retention period; plaintext storage |

Origin labels are **argued** in the reference trees, not proven: Knabenhans et
al. derive theirs from a formal model, this study from the literature. An
identifier is not labelled unavoidable (`O-CTX`) merely because some phones or
apps expose it.

**What a measure can do.** Whether a protection measure addresses a pathway is
judged per claim and per scope: a measure addresses a pathway only if it
removes one of that pathway's necessary conditions. Do **not** apply a blanket
rule such as "PETs can only remove `O-IMP` components" — a measure may address
an access condition even when the data itself is core (see the proposal's
Appendix A: an app lock against partner access to on-device cycle data).

### Reference harm trees

Origin is **not** coded from provider text. It is fixed in advance for each pathway
in [`reference_model_v2.yaml`](../../4.3_Analytical-Framework/reference_model_v2.yaml) (D12) for health trackers overall.
Every OR+ of the sources is stated there as an OR of sufficient AND-combinations, each
naming the actor and the component that gives that actor the data; a combination the
sources do not establish is not added, and the capability stays uncertain.
Sources include Salehzadeh Niksirat et al. 2024, Gabriele & Chiasson 2020,
Shipp & Blasco 2020, Malki et al. 2024, Hudig & Singh 2025 and Cao et al. 2024,
extended by the logged literature search with a recorded reason. App categories
do not select separate reference trees; applicability is assessed per app and pathway. Each pathway names the data, potential adversary, access conditions,
capability and possible consequence; required conditions are joined with AND/OR.
A prediction the app makes *for its user* does not by itself establish
third-party access.

### Applicability record (one row per app × pathway)

| Field | Content |
|---|---|
| App ID, pathway ID | |
| Required feature | what the app must do for the pathway to exist |
| Evidence | where the feature is documented: listing, policy, or walkthrough (with location) |
| Access assumptions | who can reach the data, and how |
| Context assumptions | anything else the pathway assumes |
| Decision | applicable · not applicable · uncertain |
| Reason | one sentence |

Every state records whether it rests on the app's evidence or on an assumption
about outside events (`basis: evidence | assumption`), so that the report can show
which applicable pathways the assumptions create. An incapability component is
present only if **no** usable route offers the function: IM12 (deletion) and IM14
(export) are judged separately and across the app and other routes, such as a
request to the provider. A missing in-app control is a walkthrough finding, not
evidence for IM12, IM14 or I2.

A harm category applies to an app when at least one of its pathways does.
`uncertain` rows are **counted and reported**, never silently dropped, so that
sparsely documented providers do not vanish from the gap analysis. Decision
rules are fixed in the pilot and versioned with this file.

---

## Axis A — Coverage (RQ1)

### A.1 Nodes mentioned

Record **every** tree node a unit mentions, each marked `asserted`,
`possible`, or `denied`. **A denial is a mention with negative polarity, not an
absence** (Andow et al. 2019, §1): polarity is an attribute of the mention and is
never folded into whether a node was mentioned. Coverage counts a denied node as
mentioned; the denial is reported beside the level. The highest level reached
(`L-CMP` < `L-CAP` < `L-HRM`) is a derived summary, so a harm mention does not
erase the data-flow information next to it.

**Pathway matching.** A named harm counts for a pathway only if the text matches
the pathway's consequence and is compatible with its data, actor and access
(Shvartzshnaider et al. 2019). A harm mention whose scope fits no single pathway is
kept as a **category-level mention** (field `scope: category`) and gives no pathway
level 3.

| Code | Level | Codes as present when the text names… | Not this when… |
|---|---|---|---|
| `L-CMP` | Component | what is collected, shared, stored, or required | — (the default for data-practice text) |
| `L-CAP` | Capability | what someone *could do* with the data (single users out, track or profile them, infer something), or an incapability | the text only lists data types or recipients |
| `L-HRM` | Harm | a concrete negative consequence for the user (denied insurance, outed, stalked, prosecuted, distress) | the text stays at "your data may be used against you" (→ `L-GEN`) |
| `L-GEN` | Generic risk [not Knabenhans] | possible misuse without a concrete consequence | a consequence is named (→ `L-HRM`) |

Feature descriptions can mention inference without presenting it as a risk:
"we estimate your fertile window" is `L-CAP` / `K-INF`, not a harm.

### A.2 Capability — Knabenhans et al. §5

| Code | Capability | Definition |
|---|---|---|
| `K-DIS` | Distinguishing | sorting users into classes from what they reveal (e.g. "users trying to conceive", "users with irregular cycles") |
| `K-TRK` | Tracking / profiling | recognising the same user again, across sessions, apps, or services; building a profile |
| `K-INF` | Inference | deriving attributes the user did not enter (pregnancy, illness, mood, routine, personality) |
| `K-INC` | Incapability | the user cannot do something they otherwise could, e.g. use a feature without consenting to sharing, or leave without losing their data |
| `K-ACC` | Access [not Knabenhans — from the literature review] | someone reads or obtains the data itself (an attacker, an authority, a partner with the phone) |

**Not `K-INF` when** the text only lists categories of data collected, even
sensitive ones.

### A.3 Harm type — Knabenhans et al. Appendix A

Seven categories, which Knabenhans et al. draw from Citron & Solove (2022) and
the CyberPeace Institute's methodology.

| Code | Category | Codes as present when the text names… |
|---|---|---|
| `H-ECO` | Economic | financial loss or loss of value: fraud, impersonation, higher prices, lost job or insurance |
| `H-PHY` | Physical | injury or risk to physical safety, including stalking enabled by location; reduced access to care |
| `H-PSY` | Psychological | anxiety, distress, fear of being watched |
| `H-AUT` | Autonomy / deprivation | coercion, manipulation, restricted choices, restricted freedom of movement or expression |
| `H-DSC` | Discrimination | differential treatment on demographic or health attributes, incl. profile-based pricing |
| `H-REP` | Reputational | damage to reputation or dignity |
| `H-SOC` | Societal | chilling effects, surveillance of groups, effects on society as a whole |

**Relationship tag `T-REL` [not Knabenhans — Citron & Solove]:** damage to
trust or intimate relationships (partner, family, employer). Applied
**alongside** any applicable category above, never instead of one. Harms that
fit none of the categories are documented in the pilot log, not forced in.

### A.4 Breach and incident details [not Knabenhans — from the GDPR gap analysis]

#### `P-BRC` — Breach consequence
- **Definition:** what would happen **to the user** if data were exposed to
  unauthorised parties.
- **Not this when:** the text only asserts that security measures exist
  (→ Axis C).

#### `P-INC` — Incident handling
- **Definition:** concrete steps the provider takes to detect, respond to, and
  notify users about security or privacy incidents.
- **Not this when:** the text only promises to notify users "as required by
  law". Record that as `P-NOT` (general notification commitment), not as a
  response procedure.

---

## Axis B — Stance (RQ2) [not Knabenhans — adapted from Zou et al. 2019]

Stance is attached to a **particular named harm** (`L-HRM`) and its supporting
span, not to the paragraph as a whole. One harm can carry **several** stances
(e.g. acknowledged and qualified). Units without a named harm get no stance;
dismissive language without one ("there is nothing to worry about") is coded
`C-REA` under Axis C, and responsibility placed on the user without a named harm
is coded `S-GRS` (below). Both feed the secondary analysis of RQ2. RQ2 itself
measures stance toward named harms only.

| Code | Stance | Definition | Boundary |
|---|---|---|---|
| `S-ACK` | Acknowledged | the harm is presented as possible | — |
| `S-QUA` | Qualified | uncertainty or likelihood language; record its **target**: the breach (`likelihood of the event`) or the consequence (`severity`) | qualification alone is not minimisation |
| `S-MIN` | Minimised | the harm is dismissed without supporting reasons in the unit or adjacent text | judged from wording only, never from inferred intent; a stated reason makes it `S-QUA` |
| `S-RSP` | Responsibility shifted | responsibility for the harm is placed on the user | — |
| `S-DEN` | Denied / prevented | the harm is presented as impossible or prevented | if a measure is claimed, also code it under Axis C |
| `S-GRS` | Generic responsibility [not Zou et al.] | responsibility for privacy or safety is placed on the user **without** a named harm ("you are responsible for keeping your login secure") | with a named harm → `S-RSP`; secondary analysis only, coded in Stage 1 |

**Minimisation measures the text, not the risk.** `S-MIN` records an explicit
dismissal that the local text does not support; it does not record whether the
provider understates an actual risk. A "no evidence" statement ("there is no
evidence that your data was affected") is `S-QUA` when it reports the basis of the
judgement and `S-MIN` when it dismisses the harm itself.

Absence is **not** a stance. Whether an applicable harm goes unmentioned is
derived in the analysis from the applicability records (RQ1).

---

## Axis C — Protection (RQ3)

### C.1 Measure claimed

Any **technical** measure claimed to limit exposure or misuse counts, whether
or not the provider calls it a PET, including ordinary security controls.
Non-technical commitments are coded separately.

| Code | Measure | Source |
|---|---|---|
| `T-3RD` | Limiting third-party access | Martin et al. 2025 |
| `T-INF` | Inferences instead of raw data | Martin et al. 2025 |
| `T-DEV` | On-device processing or storage | Martin et al. 2025 |
| `T-ENC` | Encryption | [not Knabenhans / Martin] |
| `T-ANO` | Anonymisation, pseudonymisation, aggregation | [not Knabenhans / Martin] |
| `T-SEC` | Other security control (access control, app lock, 2FA, …) | [not Knabenhans / Martin] |
| `T-OTH` | Other named technical measure | free text |
| `N-COM` | Non-technical practice commitment (e.g. "we never sell your data") | [not Knabenhans / Martin] |

For each measure record the **actor, data, claimed outcome and conditions**
where the text specifies them; vague scope is recorded as `unclear`.

### C.2 Framing and strength

| Code | Framing | Definition |
|---|---|---|
| `F-FLW` | Data flow | protection presented as less data leaving, fewer recipients, "nobody else sees your data" |
| `F-HRM` | Harm prevention | protection presented as preventing a specific bad outcome |

Strength: `partial` ("reduces exposure") · `scoped` (prevention for a named
actor or data) · `absolute` ("no one can harm you").

### C.3 `C-MIS` — Potential mismatch (human-reviewed only)
- **Definition:** a tension between a protection claim and a reference
  pathway **within the claim's scope**, with a written explanation of why the
  stated measure does not address that pathway's necessary conditions.
- **Example:** "Keeping cycle data on your phone prevents anyone, including
  someone using your phone, from inferring a pregnancy" — the claim names that
  actor, and local storage does not address readable access to an unlocked
  phone (proposal, Appendix A, P3).
- **Not this when:** the residual risk lies outside the claim's scope (P2 in
  the appendix), or the claim is partial and accurate. Partial protection is
  not a mismatch merely because other risks remain.
- **Who codes it:** the author only, never the model. A mismatch says nothing
  about whether the deployed system is safe; no system is judged safe or unsafe.

### C.4 `C-REA` — Reassurance without substance
- **Definition:** broad safety language such as "your data is safe with us"
  that names no specific measure, scope, or consequence.
- **Not this when:** a specific, checkable measure is named (→ C.1).

---

## Metadata recorded with every coding unit

| Field | Notes |
|---|---|
| Unit ID | stable, derived from document ID + offset |
| App ID | from the sampling protocol; a shared document links to every app that uses it |
| Provider ID | groups apps of the same provider |
| App category / relevant features | descriptive metadata; reference-pathway applicability is assessed separately |
| Source | `privacy_policy` · `store_description` · `structured_label` · `website` · `privacy_blog` · `in_app_ui` · `advertisement` |
| Language | de / en, **per source** |
| Verbatim quote | **mandatory for every positive code** |
| Tree node | ID of the node in the reference model (for example `IM4`, `K5`), if any. A mention counts for a pathway only if it concerns that pathway's data |
| Location | heading path, paragraph number, or screen name |
| Capture date | |
| App version | |
| Coder | `llm:<model>@<prompt version>`, `human:check` (single checked label) or `human:reference` (double-coded, settled) |

---

## Coding rules

1. A unit is one paragraph or one coherent block of interface text. **List
   items stay attached to their introductory sentence.** Adjacent text may be
   read for context; the supporting quote must be located precisely.
2. Code the **text as written**, never what the company is assumed to mean.
3. A unit may receive several codes; codes are not mutually exclusive across
   axes, and one harm may carry several stances.
4. Record the source and a verbatim quote (with location) for **every**
   positive code. A model label without a valid span is dropped from the data
   but **counted as a failure of that model**, so that it lowers measured
   performance.
5. When unsure, code it and flag it — do not silently drop it. An uncertain
   model answer is kept as uncertain, never becomes a negative code, and counts
   as 1/2 in the combined model value g (D9).
8. Two models of different families code every unit with the same prompts.
   Routine labels (components, capabilities, measures and scope) are kept when
   both models return them; a label of one model only, or an uncertain one, is
   kept as uncertain and lands in stratum V1 or V2. High-stakes labels (named
   harm, generic risk, stance including `S-GRS`, framing and strength,
   reassurance) are the union of both models, and a person checks every one
   **without seeing the models' labels**; the result is a `human:check` label.
9. Only double-coded, settled labels of the validation sample are reference
   labels. A single human check is never used as a reference label.
6. Origin and applicability are never coded from the text; they come from the
   reference trees and the applicability records.
7. Any change to a category, a decision rule, or a reference tree produces a
   new version with the reason recorded below.

## Validation

Aligned with the methodology (Validation Sample, Agreement, and Error Estimates), D8 and D9.
Script: `scripts/validation-sample/v001/` (draw, manifest, estimator, tests).

- **Pilot:** five apps drawn at random with a recorded seed; the author codes them
  completely. They choose the two models, tune the prompts and fix the allocation
  below. Pilot and instrument-test apps are **development material**: reported
  separately, never as independent evidence of model performance.
- **Target:** the independent corpus, all units of the apps outside the pilot and
  the instrument test.
- **Strata (priority partition):** each unit goes to the first stratum it meets:
  V1 the models disagree on any code; V2 a model returned an uncertain label;
  V3 harm vocabulary (frozen list below) without a high-stakes label; V4 interface
  unit; V5 every remaining unit.
- **Size and allocation:** 500 units, Neyman allocation from the pilot's stratum
  sizes and error standard deviations, at least 150 units in V5 and at least 30 in
  each other stratum (or the whole stratum if smaller). Simple random sampling
  without replacement within strata, recorded seed; π = n_h / N_h. If the pilot's
  time per unit means that 500 units would take a coder more than 12 hours, the
  total is reduced to what fits, with the same allocation rule and floors.
- **Double coding:** the author and the second coder code every sampled unit
  blind to model output and to each other; Krippendorff's α per code on binary
  unit indicators, unweighted over the sample, before discussion (reliable ≥ .800,
  tentative ≥ .667, otherwise qualitative only; undefined without variation);
  then settled. A code redefined or merged after validation is a new codebook
  version; its evaluation on this sample is exploratory. The author recodes a
  random tenth after at least two weeks.
- **Correct detection:** right label, right unit, span overlapping the reference
  span; a label dropped for an invalid span is a miss. Stage 1 misses count at
  Stage 2.
- **Reported:** weighted precision and recall per code and surface with counts and
  prevalence; Jeffreys intervals where counts are small; the share of reference
  mentions only the second model found; model–model agreement as robustness only.
- **Corrected estimates:** unit-level totals by the difference estimator with the
  stratified variance and the variance floor of the script (a stratum without
  observed errors is not treated as error-free). Joint misses from every stratum.
  App- and pathway-level figures are detection summaries, not corrected.
- **Reporting rules:** fewer than 20 reference positives for a code → recall not
  estimable, absence worded as "not found by the two models or in the vocabulary
  sample"; a routine code whose precision has a lower bound below 0.80 is reported
  only as a corrected estimate, never as a raw count.
- **V3 vocabulary (frozen at the pilot):** harm, risk, damage, misuse, discriminat*,
  stalk*, harass*, insurer, employer, prosecut*, distress, anxiety, embarrass*,
  identity theft, fraud, single out, identify, recognise, link, Profil, Schaden,
  Risiko, Missbrauch, Diskriminierung, Belästigung, Versicherung, Arbeitgeber,
  Strafverfolgung, Identitätsdiebstahl, wiedererkennen, verknüpfen. The pilot may
  add terms; none is removed after the draw.

## Version history

| Version | Date | Change | Reason |
|---|---|---|---|
| 1 | 2026-09-18 | Initial draft: three axes, 7 harm categories, 4 probe codes, 3 pathway stages, 5 stances, PET framing | Operationalises §4.5 of the proposal |
| 2 | 2026-10-04 | Harm model rebuilt on Knabenhans et al.: tree level (`L-*`) replaces pathway stage and `P-CON`; capabilities `K-*`; harm types from Knabenhans et al. Appendix A; origin `O-*` from reference trees; `C-OVR` added; `F-SEC` renamed `F-FLW` | Ground the classification in one published harm model |
| 3 | 2026-10-05 | Aligned with the proposal: every mentioned node recorded (highest level is a summary); `L-GEN` and incapability `K-INC` added; relationship becomes tag `T-REL` alongside a category; `P-NOT` for statutory-notice promises; stance attached to a named harm with several allowed, `S-HDG`→`S-QUA` (with target), `S-DEF`→`S-RSP`, `S-DEN` added, `S-ABS` removed (absence comes from applicability records); blanket "PETs only remove `O-IMP`" rule replaced by per-claim, per-scope judgement; `C-OVR` replaced by human-only `C-MIS`; measure definition includes ordinary security controls (`T-SEC`) and non-technical commitments (`N-COM`); applicability record, harm baseline, provider ID and per-source language added; validation section rewritten | Supporting instruments had drifted from the proposal; the proposal is authoritative |

| 4 | 2026-10-28 | One health-tracker study domain; feature-based pathway applicability; descriptive category metadata; five pilot and ten independent validation apps across the sample, without category allocations | Author clarification D15; retain existing coding axes, totals and validation safeguards |
| 5 | 2026-11-01 | Reference model v1 replaces the planned `harm_trees_v1.md`; tree-node field tied to it; capability type `K-ACC` added | D12; K6, K7, K8 and K9 are access to the data, which none of the three capability types of Knabenhans et al. covers |
| 6 | 2026-11-04 | Reference model v2 (no OR+, IM12 deletion and IM14 export across routes); polarity-neutral coverage, pathway matching and category-level mentions; `S-GRS` generic responsibility; minimisation and "no evidence" rule; evidence/assumption basis of applicability; two-model rules, checked vs. reference labels, span failures count as misses; validation rewritten to the V1–V5 sample of D9 | Submission review R3–R5, R7, privacy card W1–W4, W6; D8, D9, D12, D18 |
