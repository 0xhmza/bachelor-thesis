# Action plan after the 2026-10-13 supervisor meeting

- **Source:** [Organized notes](Meeting-Notes/2026-10-13_Supervisor-Meeting_Organized.md) (§8 checklist) and [raw notes](Meeting-Notes/2026-10-13_Supervisor-Meeting_Raw.md). Where they differ from the proposal, the meeting notes win.
- **Written:** 2026-10-17. Dates are *suggested* and work back from the plan in [Timeline.md](Timeline.md): proposal approved and instruments frozen by 2026-10-30, planned registration 2026-11-02. Move them freely; keep the order.
- **Rule for this list:** no decision is settled here. Each decision in Phase C needs evidence from Phase B first, and is then recorded with its reason. Items marked ❓ need the supervisor's answer, not more thinking.

## Why this order

The meeting asked for "evidence for each decision". That fixes the order of work: **define terms → gather evidence → decide with a recorded reason → write the protocols → test on the pilot → freeze → write up.** A protocol written before its decision has evidence is the thing the supervisor found hard to follow and hard to defend.

```
A Clarify + define ─┐
                    ├─► C Decide (with evidence) ─► D Protocols ─► E Pilot ─► F Freeze ─► G Rewrite + send
B Gather evidence ──┘
```

A and B run in parallel. Nothing in D starts before its decision in C is logged.

---

## Phase A — Clarify and define (2026-10-17 → 10-20)

Goal: remove ambiguity before any design work. Cost is low and it unblocks everything.

- [ ] **A1 ❓ One batched question list to the supervisor** (one email, not five). Ask only what the notes leave unclear:
  - "Post-harm reaction from the user from the app overview" and "how accessible are these mechanisms": which mechanisms (e.g. reporting, deletion, support contact, incident notice), and what should the app overview record?
  - Which venues did he mean by "pets, css, useix, ieee smp, mdmp, ccw, acmpl"? (Likely PETS, CCS, USENIX Security, IEEE S&P, … — confirm.)
  - "Harm tree on the best app": what does "best" mean, and is it one app or one tree per domain?
  - Download threshold "x": a number to try, or derive from the literature?
  - "According to the pilot": which decisions should the pilot settle?
  - Is the second coder a person he arranges, or do I find one?
- [ ] **A2 Glossary with sources.** One entry per term: definition, source, boundary example. Terms: *capability, harm, privacy harm vs. violation, health tracker, fitness / fertility / sleep / mental-health tracker, communication surface, PET, harm tree, component, stance, protection claim*. Done when every term used in RQs and the harm tree has a cited definition.
- [ ] **A3 Argue where fertility and sleep sit inside "health tracker"** (the notes ask for this explicitly). Done when the definition decides each borderline case (snoring, chronic disease, mental health) by a stated rule, not by app.

## Phase B — Gather evidence (2026-10-17 → 10-24)

Goal: every later decision cites something. Use the PDFs already in `01_Literature/PDFs/Methods-Reading/` (89 of 93 held; none read yet).

- [ ] **B1 Fix the search plan.** Confirm venue names (A1), then write the search log: database, query string, date, hits, inclusion decision. Cover PETS, CCS, USENIX Security, IEEE S&P, arXiv, ACM DL, Google Scholar, plus CHI/CSCW for methods.
- [ ] **B2 Build an extraction sheet for app-analysis papers.** One row per paper, one column per decision the thesis must make:
  | Column | Answers decision |
  |---|---|
  | Sampling frame and store access (countries, categories, keywords, scraping) | D2, D3 |
  | Ranking criterion (ratings vs. downloads), thresholds, tie-breaks | D2 |
  | Eligibility: free to install / free to use, trials, paid, login walls | D4 |
  | Sample size and how it was justified | D1 |
  | Handling of apps without a privacy policy | D5 |
  | Material collected and how (policies, ads, listings, screens) | D6 |
  | Language handling | D7 |
  | Coding: coders, agreement statistic, codebook development | D8 |
  | LLM use and validation | D9 |
  | Walkthrough or checklist method | D10 |
- [ ] **B3 Read and extract**, highest-ranked methods papers first (the ranking is in `01_Literature/`). Done when each D-column has at least two cited precedents, or the gap is written down.
- [ ] **B4 Capability and harm literature for the harm tree.** Extract capabilities from the tracker S&P literature (Niksirat 2024, Gabriele 2020, Shipp 2020, Malki 2024, Hudig 2025, Cao 2024, plus new finds). Output: a table of capability → source → data needed → adversary.
- [ ] **B5 Read the three core harm papers** still open in the Timeline: Citron & Solove, Knabenhans et al., Martin et al. Done when A2's harm and capability definitions cite them with page or section.
- [ ] **B6 Native and platform health apps** (Apple Health, Samsung Health, Huawei Health): find how, if at all, prior app-analysis studies treated pre-installed or OEM apps.

## Phase C — Decide, one record per decision (2026-10-21 → 10-26)

Goal: turn evidence into explicit, reasoned choices. For each: **question → options → evidence (cite) → choice → reason → RQ affected → what would change it.** Keep them in a single decision log so the methodology can link to them.

| ID | Decision | Current proposal says | Meeting guidance | Needs |
|---|---|---|---|---|
| D1 | Sample size and stopping rule | 50, stratified 30/20 | First 50 eligible by the methodology; no quotas; justify 50 | B2, B3 |
| D2 | Search, ranking and download/rating floor | German keywords, ≥ 1,000 ratings, ranked by rating | Ratings preferred; exclude below x downloads; German and English keywords; category search or not | B2, A1 |
| D3 | Tracker scope and keyword space | Fitness + fertility only | Add mental health, sleep, snoring, chronic disease; general or specific tracker type? | A2, A3 |
| D4 | Access and payment eligibility | Free to install | Free to install vs. free to use; credit-card trials | B2 |
| D5 | Apps with no privacy policy | Excluded from text analysis | **Included and reported as a finding** | B2 |
| D6 | Native / platform health apps | Not addressed | Say how they could enter the sample | B6 |
| D7 | Language rule | German-first, English fallback | **English mainly, German fallback**; say which materials it applies to | B2 |
| D8 | Coding team | One coder, second sought | **Two coders**; define what each codes | A1, B2 |
| D9 | LLM role | Screener, model chosen on pilot | Test usability on privacy policies | B2 |
| D10 | Walkthrough design | 12 apps, expert inspection | Checklist-based; define the data it produces | B2 |
| D11 | Device scope | Wearables via companion apps | **Apps only, not connected devices** | A3 |
| D12 | Harm-tree basis | One tree per domain | Synthesise on the "best app" | A1 ❓ |

- [ ] **C1** Write D1–D12 as decision records. Done when none cites only "common practice".
- [ ] **C2** Mark which decisions the pilot must still settle (D9, D10, parts of D2); everything else is decided on literature before the pilot.

## Phase D — Write the protocols (2026-10-24 → 10-28)

Goal: a reader could repeat the study from these documents alone.

- [ ] **D-1 RQ → method → data → justification table.** One row per RQ (RQ1–RQ4). This is the backbone of the rewritten methodology.
- [ ] **D-2 Sampling protocol** (update `04_Study/App-Sample/sampling_protocol.md`): stores, keywords (DE + EN, mental health, sleep, specialised), category rule, ranking, floor, eligibility, de-duplication, stopping at 50, replacement rule, log format.
- [ ] **D-3 Material collection protocol.** A table with columns *material / data · source · how collected · tool · stored as · analysed by*. Rows: privacy policy (including its absence), store listing, store disclosures, ads, blog posts, walkthrough recordings. State for each what exactly is collected from the app and what from the walkthrough.
- [ ] **D-4 Walkthrough checklist.** Tasks, the four questions per step, starting states, time limits, outcome categories, and the data produced (screens, quotes, outcomes).
- [ ] **D-5 Coding protocol** (update `04_Study/Codebook/codebook_v1.md`): units, labels with definition + example + counter-example, who codes what, how disagreements are resolved, the agreement statistic and when it is computed.
- [ ] **D-6 LLM feasibility test design.** Sample of policies, human reference labels, prompts versioned, metrics (precision, recall, κ / AC1), pass/fail thresholds written *before* running.
- [ ] **D-7 Harm-tree procedure.** How capabilities enter from B4, how the reference app is chosen (A1 answer), how the tree is validated against other apps.

## Phase E — Pilot (2026-10-27 → 10-30)

Goal: test the instruments, not the hypotheses. Write the success criteria *before* starting.

- [ ] **E1** State what the pilot evaluates and the criterion for each: search and eligibility rules (do they return apps?), collection procedure (is every material reachable?), walkthrough checklist (completable?), codebook (do two coders agree?), LLM (is it usable on policies?), effort and cost (does the plan fit the weeks?).
- [ ] **E2** Run the pilot on a small set (the earlier plan used five apps; set the number from D1).
- [ ] **E3** Log every change to an instrument with date and reason.
- [ ] **E4** Compute the two-coder agreement on the pilot and decide whether the codebook needs another round.

## Phase F — Freeze (by 2026-10-30)

- [ ] **F1** Freeze sampling rules, codebook, walkthrough checklist, prompts and harm tree as a dated, versioned release.
- [ ] **F2** Fix the minimum feasible study if the pilot shows it will not fit; agree cuts with the supervisor.
- [ ] **F3** Ethics: ask for written confirmation that no review is needed.

## Phase G — Rewrite and send (can start once Phase C is logged; finish after F)

- [ ] **G1 Rewrite the methodology** in the structure the notes suggest: (1) scope and definitions, (2) RQ → method → data → justification, (3) app search, eligibility, ranking and selection, (4) systematic material collection, (5) checklist-based walkthrough, (6) pilot, two-coder procedure and LLM test, (7) capability identification and harm-tree synthesis. Bullets, short subsections, one colour per phase if it helps navigation.
- [ ] **G2 Cite every decision** from the decision log.
- [ ] **G3 Update [proposal.tex](../03_Thesis/proposal/proposal.tex) and the supervisor's Google Doc** so they no longer contradict the notes (see the conflict list below). Rebuild the PDF.
- [ ] **G4** Update [Open-Points.md](Open-Points.md) and [Timeline.md](Timeline.md); file the supervisor's replies as a new note under `Meeting-Notes/`.
- [ ] **G5** Send the revised methodology with the decision log and extraction sheet attached.

---

## Where the current proposal and the Google Doc conflict with the 13 October notes

These must change in G3; the current text still says the opposite.

| Topic | Currently in proposal / Doc | Per meeting |
|---|---|---|
| Quotas | 30 fitness + 20 fertility | No quotas; first 50 eligible |
| Language | German-first, English fallback | English mainly, German fallback |
| Apps without a reachable policy | Excluded from text analysis | Included; absence reported |
| Scope | Fitness and fertility only | Add mental health, sleep, snoring, specialised; decide general vs. specific |
| Devices | Wearables via companion apps | Apps only |
| Second coder | "Will be sought" | Double coding |
| Ranking floor | ≥ 1,000 ratings | Ratings, with a minimum-download floor x |
| Method presentation | Dense prose | Bullets, RQ → method → justification |

## First three actions

1. Send the A1 question list (blocks A2, D12 and the pilot design).
2. Start B2: the extraction sheet and the first ten methods papers.
3. Draft A2: the glossary.

Everything else waits on these.
