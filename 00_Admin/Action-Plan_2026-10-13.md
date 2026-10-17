# Action plan after the 2026-10-13 supervisor meeting

Source: [organized notes](Meeting-Notes/2026-10-13_Supervisor-Meeting_Organized.md). Where they differ
from the proposal, the meeting wins. Dates are suggestions working back from
[Timeline.md](Timeline.md) (instruments frozen 2026-10-30, registration 2026-11-02).

**Order of work:** define → gather evidence → decide (with a cited reason) → write protocols →
pilot → freeze → rewrite the methodology. No decision without evidence; ❓ = needs the supervisor.

## 1 · Clarify and define (by 10-20)
- [ ] ❓ One email with the open questions: what "post-harm reaction" and "accessible mechanisms" mean;
      the venue names ("pets, css, useix, ieee smp, …"); what "best app" for the harm tree means;
      the download threshold *x*; which decisions the pilot should settle; who the second coder is.
- [ ] Glossary with sources: capability, harm, health tracker (fitness, fertility, sleep, mental health),
      PET, harm tree, surface, stance, protection claim. Each borderline tracker type decided by rule.

## 2 · Gather evidence (by 10-24)
- [ ] Search log (database, query, date, hits, inclusion) for PETS, CCS, USENIX Sec., IEEE S&P, CHI/CSCW, arXiv.
- [ ] Extraction sheet over the app-analysis papers in `01_Literature/` — one column per decision below.
- [ ] Capability table for the harm tree (capability → source → data → adversary).
- [ ] Finish the three core harm papers (Citron & Solove, Knabenhans et al., Martin et al.).

## 3 · Decide — one cited record each (by 10-26) · register: [Decision-Log.md](Decision-Log.md)

| ID | Decision | Proposal says | Meeting says |
|---|---|---|---|
| D1 | Sample size, stopping rule | 50, quota 30/20 | first 50 eligible, no quotas; justify 50 |
| D2 | Search and ranking | DE keywords, ≥ 1,000 ratings | DE + EN keywords; ratings plus a download floor *x* |
| D3 | Tracker scope | fitness + fertility | add mental health, sleep, snoring, chronic disease |
| D4 | Access | free to install | free to install vs. free to use; card-required trials |
| D5 | No privacy policy | excluded | included, absence reported |
| D6 | Native apps (Apple/Samsung/Huawei Health) | — | state how they can enter the sample |
| D7 | Language | German first | English first, German fallback |
| D8 | Coding | one coder, second sought | two coders |
| D9 | LLM | screener, chosen on pilot | test usability on policies |
| D10 | Walkthrough | 12 apps, expert inspection | checklist; define the data it yields |
| D11 | Devices | wearables via companion apps | apps only |
| D12 | Harm tree | one per domain | built on the "best app" ❓ |

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

**Start with:** the email (§1), the extraction sheet (§2), the glossary (§1).
