---
version: 1
date: 2026-09-18
status: draft — definitions written, examples to be filled from the pilot
source: 02_Proposal/sections/04_methodology.tex §4.5
---

# Codebook v1

Operational version of the three-axis coding framework in §4.5 of the proposal.

**Every category needs a definition, a positive example, and a
counter-example.** Without the counter-example the category is not codable:
neither a human coder nor a model has a boundary, and both drift. A category
that still has no counter-example after the pilot is merged or dropped. Every
change to a category means a new version of this file.

The three axes are independent. A coding unit may carry codes on all three, or
on none.

---

## Axis A — Harm type and pathway (RQ1)

### A.1 Harm type — Citron & Solove (2022), pp. 830–861

Seven categories, used as the top-level buckets. The originals were written for
adjudication; the operational definition below is what makes each codable in
provider text.

| Code | Category | Codes as present when the text names… |
|---|---|---|
| `H-PHY` | Physical | bodily injury or risk to physical safety, including stalking and physical location tracking that enables it |
| `H-ECO` | Economic | monetary loss, fraud, higher prices, loss of a job or an economic opportunity |
| `H-REP` | Reputational | damage to standing, esteem, or how the person is regarded by others |
| `H-PSY` | Psychological | emotional distress, anxiety, or disturbance (intrusion, unwanted contact) |
| `H-AUT` | Autonomy | coercion, manipulation, failure to inform, thwarted expectations, lack of control, chilling effects |
| `H-DIS` | Discrimination | differential treatment on a protected or sensitive basis — insurance, employment, credit, health status |
| `H-REL` | Relationship | damage to a relationship of trust or confidence (partner, family, doctor, employer) |

For each code, fill in from the pilot:

- **Definition:** (as above, refined against real text)
- **Positive example:** verbatim quote + source + app ID
- **Counter-example:** verbatim quote that looks like this category but is not,
  with one sentence on why

### A.2 Probe codes — the four silences

These are the core of the study. They are coded independently of A.1 because a
unit can name inference without naming any harm.

#### `P-INF` — Inference
- **Definition:** a statement about what can be *derived* from the collected
  data beyond what the user explicitly provided (pregnancy, illness, mood,
  routine, location patterns, personality traits).
- **Codes as present when:** the text refers to deriving, predicting, inferring,
  estimating, modelling, or profiling from data the user did not enter directly.
- **Not this when:** the text only lists categories of data **collected**, even
  if those categories are sensitive.

#### `P-BRC` — Breach consequence
- **Definition:** a statement about what would happen **to the user** if data
  were exposed to unauthorised parties.
- **Codes as present when:** the text describes an outcome for the user after an
  exposure.
- **Not this when:** the text only asserts that security measures exist
  (→ that is `C-REA` or a PET-framing code, not this).

#### `P-INC` — Incident handling
- **Definition:** a statement about how the provider detects, responds to, and
  notifies users about security or privacy incidents.
- **Codes as present when:** detection, response, notification, or a timeline is
  described.
- **Not this when:** the text only points at the statutory duty in the abstract
  without saying what the provider does.

#### `P-CON` — Concrete consequence
- **Definition:** a named, concrete consequence for the user — denied insurance,
  outed, stalked, prosecuted, refused employment, targeted.
- **Codes as present when:** a specific real-world outcome is named.
- **Not this when:** the text stays at the level of data flows ("your data may be
  shared with partners").

### A.3 Pathway stage — Knabenhans et al. (2026)

Where a unit does describe a route to harm, record which stage of the harm tree
it refers to. This captures whether providers talk about mechanisms,
capabilities, or outcomes.

| Code | Stage | Example of what it covers |
|---|---|---|
| `W-SYS` | System component | information the functionality leaks; requirements imposed on the user |
| `W-CAP` | Adversarial capability | distinguishing between users, tracking users, inferring attributes |
| `W-HRM` | Harm | the outcome itself |

---

## Axis B — Stance (RQ2)

Exactly **one** stance per harm code applied.

| Code | Stance | Definition |
|---|---|---|
| `S-ACK` | Acknowledged | the harm is named as a real possibility |
| `S-HDG` | Hedged | named, but qualified into improbability ("in the unlikely event…") |
| `S-MIN` | Minimised | named alongside a claim that defuses it without substantiation |
| `S-DEF` | Deflected | named, but made the user's own responsibility |
| `S-ABS` | Absent | **document- and app-level only** — asserted after the whole corpus for that app has been coded, never at unit level |

---

## Axis C — How protection is framed (RQ3)

### C.1 Which PET principle is invoked — Martin et al. (2025)

| Code | Principle |
|---|---|
| `T-3RD` | Limiting third-party access to personal data |
| `T-INF` | Minimising use and retention of raw data in favour of inferences |
| `T-DEV` | Keeping personal data on the user's device |

### C.2 Framing of the protection

| Code | Framing | Definition |
|---|---|---|
| `F-SEC` | Secrecy | protection presented as "nobody else sees your data" |
| `F-HRM` | Harm prevention | protection presented as preventing a specific bad outcome |

### C.3 Reassurance without substance

- **`C-REA` Definition:** a claim such as "your data is safe with us" that
  carries no verifiable commitment — no mechanism, no scope, no consequence.
- **Not this when:** a specific, checkable measure is named (a named encryption
  scheme, a stated retention period, a named certification).

---

## Metadata recorded with every coding unit

| Field | Notes |
|---|---|
| Unit ID | stable, derived from document ID + offset |
| App ID | from the sampling protocol |
| Source | `privacy_policy` · `store_description` · `structured_label` · `website` · `privacy_blog` · `in_app_ui` · `advertisement` |
| Language | de / en |
| Verbatim quote | **mandatory for every code applied** |
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
6. Any change to a category produces a new version of this file with the reason
   recorded below.

## Validation

- Stratified 20 % subsample double-coded by hand, blind to model output.
- Cohen's κ **per code**, not pooled. Target κ ≥ 0.70.
- Below target → diagnose as codebook problem or prompt problem, revise, bump
  the version, redraw the subsample. Two failed revisions → the code is reported
  as unreliable and excluded from quantitative claims.
- Precision audit: every code entering the results is checked against its
  verbatim span; unsupported codes are discarded and counted.

## Version history

| Version | Date | Change | Reason |
|---|---|---|---|
| 1 | 2026-09-18 | Initial draft: three axes, 7 harm categories, 4 probe codes, 3 pathway stages, 5 stances, PET framing | Operationalises §4.5 of the proposal |
