# Action plan after the 2026-10-13 supervisor meeting

Source: [organized notes](Meeting-Notes/2026-10-13_Supervisor-Meeting_Organized.md). Where they differ
from the proposal, the meeting wins. Dates are suggestions working back from
[Timeline.md](Timeline.md) (instruments frozen 2026-10-30, registration 2026-11-02).

**Order of work:** define → gather evidence → decide (with a cited reason) → write protocols →
pilot → freeze → rewrite the methodology. No decision without evidence; ❓ = needs the supervisor.

**Status, 23 October:** D1, D2 (ranking part) and D6 are proposed; the other decisions are open.
The app-selection evaluation and the literature gap search of 23 October added §7 and §8 below.
Legend: ☐ open · ◐ started · ☑ done.

## 1 · Clarify and define (by 10-20)
- [ ] ❓ One email with the open questions: what "post-harm reaction" and "accessible mechanisms" mean;
      the venue names ("pets, css, useix, ieee smp, …"); what "best app" for the harm tree means;
      the download threshold *x*; which decisions the pilot should settle; who the second coder is.
      **Add the three app-selection questions from §7** (domain in the sample, one app per provider,
      pregnancy and workout-plan apps).
- [ ] Glossary with sources: capability, harm, health tracker (fitness, fertility, sleep, mental health),
      PET, harm tree, surface, stance, protection claim. Each borderline tracker type decided by rule.
      CHARISMHA (2016) gives the German government's definitions of health apps
      ([gap search](../01_Literature/Literature-Gap-Search_2026-10-23.md) §6).

## 2 · Gather evidence (by 10-24)
- [ ] ◐ Search log (database, query, date, hits, inclusion) for PETS, CCS, USENIX Sec., IEEE S&P, CHI/CSCW, arXiv.
      Queries and dates of the 23 October search are logged in the
      [gap search](../01_Literature/Literature-Gap-Search_2026-10-23.md) §9; hits and inclusion per query are not.
- [ ] Extraction sheet over the app-analysis papers in `01_Literature/` — one column per decision below.
      The digest's stage A table (`Methods-Digest/sections/A.tex`) covers 15 selection designs already.
- [ ] Capability table for the harm tree (capability → source → data → adversary). New inputs: personality
      inference from activity data (Zufferey et al. 2023), location leaks through privacy zones
      (Hassan et al. 2018; Dhondt et al. 2022), FemTech threat actors (Mehrnezhad et al. 2024).
- [ ] Finish the three core harm papers (Citron & Solove, Knabenhans et al., Martin et al.).
- [ ] Read the priority-A papers of the gap search; their digest cards are the short version.

## 3 · Decide — one cited record each (by 10-26) · register: [Decision-Log.md](Decision-Log.md)

| ID | Decision | Proposal says | Meeting says | Status |
|---|---|---|---|---|
| D1 | Sample size, stopping rule | 50, quota 30/20 | first 50 eligible, no quotas; justify 50 | proposed; see §7.2 |
| D2 | Search and ranking | DE keywords, ≥ 1,000 ratings | DE + EN keywords; ratings plus a download floor *x* | ranking proposed; search frame open; see §7 |
| D3 | Tracker scope | fitness + fertility | add mental health, sleep, snoring, chronic disease | open; see §7.4 |
| D4 | Access | free to install | free to install vs. free to use; card-required trials | open |
| D5 | No privacy policy | excluded | included, absence reported | open |
| D6 | Native apps (Apple/Samsung/Huawei Health) | — | state how they can enter the sample | proposed |
| D7 | Language | German first | English first, German fallback | confirmed 10-23 ([D07](Decisions/D07_language.md)) |
| D8 | Coding | one coder, second sought | two coders | open |
| D9 | LLM | screener, chosen on pilot | test usability on policies | open; see §8 |
| D10 | Walkthrough | 12 apps, expert inspection | checklist; define the data it yields | open |
| D11 | Devices | wearables via companion apps | apps only | open |
| D12 | Harm tree | one per domain | built on the "best app" ❓ | open |

## 4 · Protocols (by 10-28)
- [ ] RQ → method → data → justification table (backbone of the rewrite).
- [ ] Update `04_Study/`: sampling protocol, collection table (material · source · procedure · analysis),
      walkthrough checklist, codebook with the two-coder procedure, LLM test with thresholds set in advance.

## 5 · Pilot and freeze (by 10-30)
- [ ] Write pass criteria first, run the pilot, log every instrument change, compute two-coder agreement.
- [ ] Freeze a dated release of all instruments; ask for written ethics confirmation.

## 6 · Rewrite and send
- [ ] Rewrite Chapter 4 of the thesis as bullets in the meeting's structure, every decision cited.
      The supervisor's Word copy (`03_Thesis/Thesis_Review-Copy.docx`) updates with the commit.
- [ ] Update `Open-Points.md` and `Timeline.md`; file the reply under `Meeting-Notes/`.

## 7 · App selection: follow-ups from the 23 October evaluation

Source: [App-Selection-Evaluation_2026-10-23.md](App-Selection-Evaluation_2026-10-23.md). Figures are from the
Google Play pilot of 22 October (19 keywords, first 20 results, Samsung Health moved to the preinstalled
group) and are reproduced by `scripts/sampling-checks/v001/check_pool.py`. Order = order of work.

1. [ ] **Run the App Store collector with the same 19 keywords and depth** (D2). *Comment:* everything below
   rests on Play alone. Do this first, because the App Store half may fix or worsen the domain mix and may
   have its own provider clusters. Small: one collector run, then `check_pool.py` needs an App Store loader.
2. [ ] ❓ **Decide how domain enters the sample** (D1, D3). *Comment:* this is the most consequential point.
   Without quotas the 24 Play places hold 3 period trackers and 2 pregnancy apps, and the top 47 hold 7 and 3.
   The methodology still plans 6 walkthroughs and 5 validation apps per domain and separate reporting, which
   needs at least 7 fertility apps outside the 2 pilot apps before any walkthrough. The supervisor ruled out
   30/20 quotas, so the choice is theirs. Options: (a) domain as a descriptor only, which drops per-domain
   walkthrough and validation slots; (b) a minimum per domain, e.g. 10; (c) places in proportion to each
   domain's share of all ratings, which keeps the exposure logic: on Play that is about 10 fertility,
   4 pregnancy and 33 fitness places. Suggest (c) in the email, with the pilot numbers.
3. [ ] ❓ **One app per developer** (D2). *Comment:* Leap Fitness Group holds 10 of the Play top 47 under one
   policy URL, and Simple Design Ltd. 3. Coding a shared policy once saves work but leaves those places with
   no new communication, and RQ1–RQ3 are about what providers say. Take each developer's highest-ranked app
   and continue down the list; report the clustered list as sensitivity. In the pilot this changes 6 of the
   24 Play places and adds one period tracker. Small: a script option in `scripts/app-ranking/v002/`.
4. [ ] **Tracking-over-time eligibility rule with an exclusion log** (D3, D4). *Comment:* the ranked pool mixes
   trackers with workout-plan apps, meditation (*Calm*), pregnancy and baby apps, and on the App Store
   off-topic hits (*Google Gemini*, a timer, a shop). Adopt Robillard et al.'s rule (personal or sensor data
   recorded over time) and write five boundary examples into D3 before screening. Decide with the supervisor
   whether pregnancy apps count as fertility tracking (❓).
5. [ ] **Saturation and keyword checks** (D2, D3). *Comment:* 13 of the Play top 47 were found only at result
   positions 11–20, and dropping `Workout` alone removes 7. Rerun with 50 results per keyword and report how
   many selected apps change; keep a leave-one-keyword-out table as a sensitivity result. Add mental-health
   keywords once D3 settles the scope, and take the keyword list from a stated source (as Hutton et al. 2018
   and Malki et al. 2024 did).
6. [ ] **German exposure check for Play-selected apps** (D2). *Comment:* Play counts are worldwide. Record for
   each selected app whether it has a German listing and a German category-chart position, and report the
   number with neither. Cheap, and it answers the obvious examiner question.
7. [ ] **Reword the floor** (D2, methodology). *Comment:* no decision needed. The 1,000-rating floor never decides
   a selected app (47th Play app: 309,727 ratings; 24th App Store app in the trial: 10,718). Say it filters the
   candidate pool and the proxy check, not the sample.
8. [ ] **Tighten the claim wording** (methodology, limitations). *Comment:* results hold for "the most-rated
   fitness and fertility apps in the German storefronts" (Martin et al. 2015 on popularity-only samples), and
   rating counts respond to in-app prompts (Google's Babbel case: +64 % rating volume). The limitations section
   already says most of this.

## 8 · Literature follow-ups from the 23 October gap search

Source: [Literature-Gap-Search_2026-10-23.md](../01_Literature/Literature-Gap-Search_2026-10-23.md).

- [ ] Save the open-access PDFs that block scripted download into `01_Literature/PDFs/Methods-Reading/_Inbox/`
      and run `import_manual.py`: Velykoivanenko et al. 2021 (advisor co-author; iris.unil.ch, CC BY-ND),
      Mehrnezhad & Almeida 2021 (ACM, CC BY), Doherty et al. 2025 (npj Digital Medicine), Gasteiger et al. 2023
      (BMJ Open), Wang et al. 2024 (CHI), Bijker et al. 2024 (JMIR).
- [ ] Library login for the paywalled stance sources: Pollach 2005 and 2007, Bhatia et al. 2016, Draper & Turow 2019;
      and for Martin et al. 2015, Garg & Telang 2013.
- [ ] Get PDFs for the two works the methodology already cites without one: Calo 2011, Zimmeck et al. 2019.
- [ ] D9 inputs to settle in the pilot: span-level recall per axis (Chanenson et al. 2025: prompting below 20 %
      on span annotation), segment size (Xie et al. 2025), German test on MAPP (Arora et al. 2022), word-level
      GDPR annotation design (Cory et al. 2026), repeated runs (Atil et al. 2025).
- [ ] D8: whether a second coder can label 50–100 units, which the alternative annotator test needs
      (Calderon et al. 2025).
- [x] D7: revisit "English first, German fallback". *Comment:* in Arora et al. 2022 (MAPP corpus), 14 of 59 apps
      acknowledged the GDPR only in their German policy, and 13 English–German pairs differed substantially.
      **Settled 10-23:** the meeting rule stands (English first, German fallback); both versions are captured where
      both exist and differences are logged ([D07](Decisions/D07_language.md)).

**Start with:** the email (§1, now with the §7 questions), the App Store run (§7.1), the glossary (§1).
