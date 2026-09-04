# Meeting Notes — Proposal Scoping

- **Date:** 2026-09-04
- **Participants:** Hamza (student), Kavous Salehzadeh Niksirat (supervisor, MPI-SP)
- **Purpose:** Scope the thesis and agree on what goes into the proposal
- **Working title:** Understanding Privacy Harm Communication in Fitness and Health Tracking Apps

---

## 1. Scope

**Broadened from devices to apps.** The study is not restricted to physical wearables.
Any health-tracking app is in scope, including:

- fitness / activity tracking apps
- period and cycle tracking apps
- other health and wellness self-tracking apps

The unit of analysis is the **app and its surrounding communication**, not the hardware.

## 2. Core research angle

**How do these apps communicate privacy to their users?**

Central observation motivating the study: platform privacy communication (terms of
service, privacy policies) tends to speak about **downstream data practices only** —
who receives data, for which purposes, on which legal basis. It is largely **silent on**:

- **inference** — what can be derived from the collected data beyond what was
  explicitly provided
- **breaches** — what happens if data is exposed
- **incidents** — how the provider handles security or privacy incidents

That silence is the gap: users may believe they are protected against harms the
communication never actually addresses.

## 3. Methodology (as discussed)

### Step 1 — Build the app sample
- **Platforms:** Google Play Store and Apple App Store
- **Market:** Germany
- **Selection:** keyword-driven search (health / fitness / period / sleep tracking, ...)
- **Ranking:** by rating and by store category
- **Target size:** ~50 apps (first pass)

### Step 2 — Define what we look at per app
For each app in the sample, collect and analyse:
- the **privacy policy**
- the **store description** (Play Store / App Store listing)
- the **provider website**: service description, how privacy is talked about
- **UI / app walkthrough** — what privacy-relevant content is actually shown in use

### Step 3 — Advertising material
- Check whether **app advertisements** contain anything privacy-related, and if so, what.

## 4. Data collection and analysis

- **LLM-assisted analysis** to handle the volume of text: prompts are designed and
  applied systematically over the collected privacy-related texts.
  → prompts must be versioned and documented so the process is reproducible.
- **App walkthroughs are done manually.** No automation there.
- All privacy-related text collected across the sources above is analysed.

## 5. Reading

- EPFL / UNIL paper on **privacy harms** — read before the next step.
  (See `01_Literature/` — Citron & Solove 2021 "Privacy Harms", plus the
  Salehzadeh Niksirat et al. 2024 wearable trackers survey already in the folder.)

## 6. Proposal — required structure

The proposal must cover, in this order:

1. **Background**
2. **Research problem**
3. **Why the problem is important**
4. **Methodology**

## 7. Action items

| # | Action | Owner | Status |
|---|--------|-------|--------|
| 1 | Set up a Google Doc for shared writing / supervisor comments | Hamza | open |
| 2 | Read the EPFL privacy-harms paper | Hamza | open |
| 3 | Draft the proposal (background, problem, importance, methodology) | Hamza | open |
| 4 | Define keyword list and inclusion/exclusion criteria for the app sample | Hamza | open |
| 5 | Draft the first version of the LLM analysis prompts | Hamza | open |

## 8. Open questions for the next meeting

- The written thesis offer describes a **scenario-based online survey** (users rate
  privacy-harm scenarios before/after reading platform communication). This meeting
  described an **app-store / document analysis** of how privacy is communicated.
  → Are these two phases of one thesis (analysis first, survey second), or has the
  scope shifted to the analysis only? This needs to be settled before the proposal
  methodology section is written.
- Expected sample size: is 50 apps the final target, or a pilot?
- Which LLM, and how is its output validated against manual coding (inter-rater
  agreement on a subsample)?
- Language of the material: German store listings, English policies, or both?
- Does the app-store scraping / walkthrough part need an ethics review?
