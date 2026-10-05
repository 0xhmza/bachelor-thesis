---
version: 2
date: 2026-10-04
status: superseded by codebook_v3.md (2026-10-05) — kept for the version history
source: 03_Thesis/proposal/proposal.tex (Reference harm trees, Coding); harm model from Knabenhans et al. (2026), ePrint 2026/867
supersedes: codebook_v1.md
---

# Codebook v2

The harm model is taken from Knabenhans et al. (2026), *On the (Privacy) Harms
of the European Digital Identity Framework*, §4.1, §5 and Appendix A
(`01_Literature/PDFs/Knabenhans_2026_PrivacyHarms-EUDigitalIdentity.pdf`).
Elements that do not come from that paper are marked **[not Knabenhans]** with
their source.

**Every category needs a definition, a positive example, and a
counter-example.** Without the counter-example the category is not codable:
neither a human coder nor a model has a boundary, and both drift. A category
that still has no counter-example after the pilot is merged or dropped. Every
change to a category means a new version of this file.

---

## 0. The harm model

**Harm** (Knabenhans et al., following the CyberPeace Institute): "an
impairment or disruption of an entity's capacity or ability to function and
exist as it otherwise would have in its usual context".

**Harm tree** (Knabenhans et al. §4.1, after De & Le Métayer): three levels.

| Level | What it is | Tracker examples |
|---|---|---|
| System component | information the system leaks, the result of an interaction, or a requirement imposed on the user | cycle data sent to a server; an advertising ID shared with an SDK; "an account is required" |
| Capability | what a set of components lets an adversary do | distinguishing, tracking/profiling, inference |
| Harm | the impairment itself | discrimination in insurance; prosecution; distress |

**Origin** of a component (Knabenhans et al. §4.1, black/blue/red):

| Code | Origin | Meaning | Tracker examples |
|---|---|---|---|
| `O-CORE` | Core functionality | cannot be removed without stopping the app from doing what it is for | logged cycles; predicted fertile window; step count |
| `O-CTX` | Digital context | cannot be removed from any app on a phone | device identifiers; OS/platform telemetry; store account; network metadata |
| `O-IMP` | Implementation choice | the provider chose it and could choose otherwise | advertising/analytics SDKs; cloud sync; retention period; plaintext storage |

PETs can only remove `O-IMP` components (§4.5). Every harm whose tree has a
pathway made only of `O-CORE`/`O-CTX` components cannot be prevented by any
PET.

### Reference harm trees

Origin is **not** coded from provider text. It is fixed in advance, per domain,
in `harm_trees_v1.md` (to be built before the pilot), following Knabenhans et
al. §4.2: harms are taken from the tracker literature (Salehzadeh Niksirat et al. 2024,
Shipp & Blasco 2020, Cao et al. 2024, …) and the seven harm types, and each
pathway's components are labelled with an origin. Coding then records which
nodes of the tree a unit reaches. The trees are versioned like this file.

---

## Axis A — Pathway (RQ1)

### A.1 Highest level reached

Exactly one per unit that says anything about data or risk.

| Code | Level | Codes as present when the text names… | Not this when… |
|---|---|---|---|
| `L-CMP` | Component | what is collected, shared, stored, or required | — (this is the default for data-practice text) |
| `L-CAP` | Capability | what someone *could do* with the data (single users out, track or profile them, infer something) | the text only lists data types or recipients |
| `L-HRM` | Harm | a concrete outcome for the user (denied insurance, outed, stalked, prosecuted, distress) | the text stays at "your data may be shared" |

`L-HRM` replaces v1's `P-CON` (concrete consequence).

### A.2 Capability — Knabenhans et al. §5

| Code | Capability | Definition |
|---|---|---|
| `K-DIS` | Distinguishing | sorting users into classes from what they reveal (e.g. "users trying to conceive", "users with irregular cycles") |
| `K-TRK` | Tracking / profiling | recognising the same user again, across sessions, apps, or services; building a profile |
| `K-INF` | Inference | deriving attributes the user did not enter (pregnancy, illness, mood, routine, personality) |

`K-INF` replaces v1's `P-INF`. **Not `K-INF` when** the text only lists
categories of data collected, even sensitive ones.

### A.3 Harm type — Knabenhans et al. Appendix A

Seven categories. Knabenhans et al. build them on Citron & Solove (2022) and
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

**Candidate for the pilot [not Knabenhans]:** Citron & Solove's *relationship*
harm (partner, family, employer surveillance). Not in Knabenhans et al.'s list
but plausibly frequent for cycle trackers. Added as `H-REL` only if the pilot
finds units that no code above captures.

### A.4 Probes [not Knabenhans — from the GDPR gap analysis, proposal §1]

#### `P-BRC` — Breach consequence
- **Definition:** what would happen **to the user** if data were exposed to
  unauthorised parties. In tree terms: the pathway retention → leak →
  economic/psychological harm (Knabenhans et al. Fig. 7b).
- **Not this when:** the text only asserts that security measures exist
  (→ Axis C).

#### `P-INC` — Incident handling
- **Definition:** how the provider detects, responds to, and notifies users
  about security or privacy incidents.
- **Not this when:** the text only points at the statutory duty in the abstract.

---

## Axis B — Stance (RQ2) [not Knabenhans — adapted from Zou et al. 2019]

Exactly **one** stance per harm-level (`L-HRM`) unit. Units that stop at a
capability or component get no stance (proposal: "stance is coded only where a
harm is named").

| Code | Stance | Definition |
|---|---|---|
| `S-ACK` | Acknowledged | named as a real possibility |
| `S-HDG` | Hedged | named, but qualified into improbability ("in the unlikely event…") |
| `S-MIN` | Minimised | named alongside a claim that defuses it without substantiation |
| `S-DEF` | Deflected | named, but made the user's own responsibility |
| `S-ABS` | Absent | **app level only** — asserted after the whole corpus for that app has been coded, never at unit level |

---

## Axis C — Protection (RQ3)

### C.1 Measure claimed

| Code | Measure | Source |
|---|---|---|
| `T-3RD` | Limiting third-party access | Martin et al. 2025 |
| `T-INF` | Inferences instead of raw data | Martin et al. 2025 |
| `T-DEV` | On-device processing | Martin et al. 2025 |
| `T-ENC` | Encryption | [not Knabenhans / Martin] |
| `T-ANO` | Anonymisation, pseudonymisation, aggregation | [not Knabenhans / Martin] |
| `T-OTH` | Other named measure | free text |

### C.2 Origin addressed — Knabenhans et al. §4.5

For each measure, the origin of the component it removes, read from the
reference tree: normally `O-IMP`. A measure claimed to remove an `O-CORE` or
`O-CTX` component is flagged for adjudication.

### C.3 Framing

| Code | Framing | Definition |
|---|---|---|
| `F-FLW` | Data flow | protection presented as less data leaving, fewer recipients, "nobody else sees your data" |
| `F-HRM` | Harm prevention | protection presented as preventing a specific bad outcome |

### C.4 `C-OVR` — Overclaim (Knabenhans et al. §4.5, §6)
- **Definition:** a measure presented as preventing a harm (`F-HRM`, or
  "you are protected / safe") whose reference tree keeps a pathway made only of
  `O-CORE`/`O-CTX` components. This is the "false sense of safety" Knabenhans
  et al. warn about.
- **Example:** a cycle tracker saying on-device processing "keeps your
  reproductive health private" — the fertile-window inference is `O-CORE`.
- **Not this when:** the claim stays at data flow (`F-FLW`) and is accurate.

### C.5 `C-REA` — Reassurance without substance
- **Definition:** a claim such as "your data is safe with us" that carries no
  verifiable commitment — no mechanism, no scope, no consequence.
- **Not this when:** a specific, checkable measure is named.

---

## Metadata recorded with every coding unit

| Field | Notes |
|---|---|
| Unit ID | stable, derived from document ID + offset |
| App ID | from the sampling protocol |
| Domain | fitness · fertility (selects the reference tree) |
| Source | `privacy_policy` · `store_description` · `structured_label` · `website` · `privacy_blog` · `in_app_ui` · `advertisement` |
| Language | de / en |
| Verbatim quote | **mandatory for every code applied** |
| Tree node | ID of the reference-tree node the code maps to, if any |
| Location | heading path, paragraph number, or screen name |
| Capture date | |
| App version | |
| Coder | `llm:<model>@<prompt version>` or `human` |

---

## Coding rules

1. Code the **text as written**, never what the company is assumed to mean.
2. A unit may receive several codes; codes are not mutually exclusive across
   axes.
3. Record the source and a verbatim quote (with location) for **every** code
   applied. A code without a quote is discarded automatically.
4. When unsure, code it and flag it — do not silently drop it.
5. `S-ABS` is never a unit-level code.
6. Origin is never coded from the text; it comes from the reference tree.
7. Any change to a category or to a reference tree produces a new version with
   the reason recorded below.

## Validation

Unchanged from v1 (asymmetric calibration, κ per code with prevalence, precision
and recall audits). The lexical sweep adds capability vocabulary:
`single out, identify, recognise, link, wiedererkennen, verknüpfen, Profil`.

## Version history

| Version | Date | Change | Reason |
|---|---|---|---|
| 1 | 2026-09-18 | Initial draft: three axes, 7 harm categories, 4 probe codes, 3 pathway stages, 5 stances, PET framing | Operationalises §4.5 of the proposal |
| 2 | 2026-10-04 | Harm model rebuilt on Knabenhans et al.: tree level (`L-*`) replaces pathway stage and `P-CON`; capabilities `K-*` (`K-INF` replaces `P-INF`); harm types switched to Knabenhans et al. Appendix A (societal added, relationship moved to pilot candidate); origin `O-*` from reference trees; `C-OVR` added; `F-SEC` renamed `F-FLW` | Ground the classification in one published harm model and measure absence against a stated baseline |
