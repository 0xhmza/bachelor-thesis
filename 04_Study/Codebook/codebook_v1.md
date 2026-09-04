---
version: 1
date: TODO
status: draft
---

# Codebook v1

Each category needs a **definition**, a **positive example**, and a
**counter-example**. Without the counter-example the category is not codable and
the LLM will drift. Every change to a category means a new version of this file.

## A. What the communication *does* cover

### A1. Data collected
- **Definition:**
- **Codes as present when:**
- **Example:**
- **Not this when:**

### A2. Purposes of processing
- **Definition:**
- **Example:**
- **Not this when:**

### A3. Third-party sharing
### A4. Retention
### A5. User controls (access, deletion, export, opt-out)
### A6. Legal basis / GDPR references

## B. What the communication may *omit* — the core of the study

### B1. Inference
- **Definition:** statements about what can be *derived* from the collected data
  beyond what the user explicitly provided (e.g. pregnancy, mood, illness,
  personality traits, location patterns).
- **Codes as present when:**
- **Example:**
- **Not this when:** the text only lists categories of data collected.

### B2. Data breach
- **Definition:** statements about what happens if data is exposed to
  unauthorised parties.

### B3. Incident handling
- **Definition:** statements about how the provider detects, responds to, and
  notifies users about security or privacy incidents.

### B4. Concrete harms to the user
- **Definition:** statements naming a concrete consequence for the user
  (discrimination, insurance, employment, stalking, outing, reputational damage).
- Map to the Citron & Solove (2021) harm taxonomy where possible.

## C. How it is communicated

### C1. Source
`privacy_policy` · `store_description` · `website` · `in_app_ui` · `advertisement`

### C2. Readability / register
### C3. Placement and prominence
### C4. Reassurance language without substance
- **Definition:** claims such as "your data is safe with us" that carry no
  verifiable commitment.

## Coding rules

1. Code the **text as written**, never what you infer the company means.
2. A segment may receive multiple codes.
3. Record the source and a verbatim quote (with location) for every code applied.
4. When unsure, code it and flag it — do not silently drop it.

## Version history

| Version | Date | Change | Reason |
|---|---|---|---|
| 1 | | initial draft | — |
