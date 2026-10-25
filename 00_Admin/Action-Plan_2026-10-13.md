# Action plan after the 2026-10-13 supervisor meeting

Source: [organized notes](Meeting-Notes/2026-10-13_Supervisor-Meeting_Organized.md); where
they differ from the proposal, the meeting wins. Dates work back from
[Timeline.md](Timeline.md) (instruments frozen 2026-10-30, registration 2026-11-02).
Order: define → gather evidence → decide with a cited reason → protocols → pilot →
freeze → rewrite the methodology. ❓ = needs the supervisor.
Legend: ☐ open · ◐ started · ☑ done. **Status: 25 October 2026.**

## 1 · Clarify and define (by 10-20)
- ☐ ❓ One email with the open questions: "post-harm reaction" and "accessible
  mechanisms"; the venue names ("pets, css, useix, ieee smp, …"); "best app" for the
  harm tree; which decisions the pilot settles; the second coder; the three
  app-selection questions of §7 (domain in the sample, one app per provider,
  pregnancy and workout-plan apps); the German exposure ranking (D2) and the vendor
  rule (D6).
- ☐ Glossary with sources: capability, harm, health tracker, PET, harm tree,
  surface, stance, protection claim. CHARISMHA (2016) gives the German government's
  definitions of health apps ([gap search](../01_Literature/Literature-Gap-Search_2026-10-23.md) §6).

## 2 · Gather evidence (by 10-24)
- ◐ Search log (database, query, date, hits, inclusion) for PETS, CCS, USENIX Sec.,
  IEEE S&P, CHI/CSCW, arXiv: queries and dates of 23 October are in the gap search
  §9; hits and inclusion per query are not.
- ☐ Extraction sheet over the app-analysis papers, one column per decision; the
  digest's stage A table (`Methods-Digest/sections/A.tex`) covers 15 selection designs.
- ☐ Capability table for the harm tree (capability → source → data → adversary). New
  inputs: personality inference from activity data (Zufferey et al. 2023), location
  leaks through privacy zones (Hassan et al. 2018; Dhondt et al. 2022), FemTech
  threat actors (Mehrnezhad et al. 2024).
- ☐ Finish the three core harm papers (Citron & Solove, Knabenhans et al., Martin et al.).
- ☐ Read the priority-A papers of the gap search (digest cards are the short version).

## 3 · Decide (by 10-26) · register: [Decision-Log.md](Decision-Log.md)

| ID | Decision | Proposal | Meeting | Status |
|---|---|---|---|---|
| D1 | Sample size, stopping rule | 50, quota 30/20 | first 50 eligible, no quotas; justify 50 | proposed |
| D2 | Search and ranking | DE keywords, ≥ 1,000 ratings | DE + EN keywords; ratings plus a download floor *x* | proposed (German exposure, 10-25) |
| D3 | Tracker scope | fitness + fertility | add mental health, sleep, snoring, chronic disease | proposed 10-23 |
| D4 | Access | free to install | free to install vs. free to use; card-required trials | proposed 10-23 |
| D5 | No privacy policy | excluded | included, absence reported | confirmed 10-23 |
| D6 | Native apps | — | state how Apple/Samsung/Huawei Health can enter | proposed |
| D7 | Language | German first | English first, German fallback | confirmed 10-23 |
| D8 | Coding | one coder, second sought | two coders | open |
| D9 | LLM | screener, chosen on pilot | test usability on policies | open; see §8 |
| D10 | Walkthrough | 12 apps, expert inspection | checklist; define the data it yields | open |
| D11 | Devices | wearables via companion apps | apps only | proposed 10-23 (in D3) |
| D12 | Harm tree | one per domain | built on the "best app" ❓ | open |

## 4 · Protocols (by 10-28)
- ☐ RQ → method → data → justification table.
- ◐ Update `04_Study/`: sampling protocol (v2 done), collection table, walkthrough
  checklist, codebook with the two-coder procedure, LLM test with thresholds set in advance.

## 5 · Pilot and freeze (by 10-30)
- ☐ Pass criteria first, then the pilot; log every instrument change; two-coder agreement.
- ☐ Freeze a dated release of all instruments; written ethics confirmation.

## 6 · Rewrite and send
- ◐ Rewrite Chapter 4 in the meeting's structure, every decision cited (App Sampling
  done). The review copy `03_Thesis/Thesis_Review-Copy.docx` updates with each commit.
- ☐ Update `Open-Points.md` and `Timeline.md`; file the reply under `Meeting-Notes/`.

## 7 · App selection: follow-ups from the [23 October evaluation](App-Selection-Evaluation_2026-10-23.md)

1. ☑ App Store collection with the same keywords and depth: 23 October, 49 queries
   (`appstore-scraper/v007`).
2. ☐ ❓ How domain enters the sample (D1, D3). Pilot, Play: the 24 Play places held 3
   period trackers and 2 pregnancy apps, the top 47 held 7 and 3. The per-domain
   plans (6 walkthroughs and 5 validation apps per domain, separate reporting) need
   at least 7 fertility apps besides the 2 pilot apps. Options: (a) descriptor only;
   (b) a minimum per domain, e.g. 10; (c) places in proportion to each domain's share
   of ratings (on Play about 10 fertility, 4 pregnancy, 33 fitness). The drawn sample
   has 4 cycle, 2 pregnancy and 2 mood apps among 47.
3. ☑ One app per developer (D2, 23 October). Pilot: Leap Fitness Group held 10 of the
   Play top 47 under one policy URL, Simple Design Ltd. 3; the rule changed 6 of the
   24 Play places.
4. ☑ Tracking-over-time rule E1 with an exclusion log (D3, 23 October;
   [screening.csv](../04_Study/App-Sample/screening.csv)). Pregnancy apps are inside the
   domain, following Malki et al. (2024); ❓ supervisor to confirm.
5. ☑ Saturation and keyword checks: keyword list from Hutton et al. (2018) and Malki
   et al. (2024), incl. mood (D3); App Store depth 200 and leave-one-keyword-out
   reported as sensitivity (Results 5.1).
6. ☑ German exposure: superseded by the German ranking of both stores (D2, 25 October).
7. ☑ Floor: dropped (D2, 25 October); it decided no selected app (47th Play app in the
   pilot: 309,727 ratings; 24th App Store app in the trial: 10,718).
8. ☐ Claim wording: results hold for the most-rated apps in the German storefronts
   (Martin et al. 2015); rating counts respond to in-app prompts (Google's Babbel
   case: +64 % rating volume).

## 8 · Literature follow-ups from the [23 October gap search](../01_Literature/Literature-Gap-Search_2026-10-23.md)

- ☐ Save the open-access PDFs that block scripted download into
  `01_Literature/PDFs/Methods-Reading/_Inbox/` and run `import_manual.py`: Velykoivanenko
  et al. 2021 (advisor co-author; iris.unil.ch, CC BY-ND), Mehrnezhad & Almeida 2021
  (ACM, CC BY), Doherty et al. 2025 (npj Digital Medicine), Gasteiger et al. 2023
  (BMJ Open), Wang et al. 2024 (CHI), Bijker et al. 2024 (JMIR).
- ☐ Library login for the paywalled stance sources: Pollach 2005 and 2007, Bhatia et
  al. 2016, Draper & Turow 2019; and for Martin et al. 2015, Garg & Telang 2013.
- ☐ PDFs for two works the methodology cites without one: Calo 2011, Zimmeck et al. 2019.
- ☐ D9 inputs for the pilot: span-level recall per axis (Chanenson et al. 2025:
  prompting below 20 % on span annotation), segment size (Xie et al. 2025), German test
  on MAPP (Arora et al. 2022), word-level GDPR annotation (Cory et al. 2026), repeated
  runs (Atil et al. 2025).
- ☐ D8: whether a second coder can label 50–100 units, which the alternative
  annotator test needs (Calderon et al. 2025).
- ☑ D7: English first, German fallback stands (10-23); both versions captured where
  both exist (Arora et al. 2022: 14 of 59 apps acknowledged the GDPR only in their
  German policy; 13 English–German pairs differed substantially).

**Next:** the email (§1), the glossary (§1), the domain question (§7.2).
