# Open points

Only what is still open. Details: [meeting checklist 2026-11-06](../Meetings/2026-11-06_Supervisor-Meeting_Organized.md), [Decisions](../Decisions.md).

## To decide (author)
- [ ] Which five apps get a worked harm tree; keep five if feasible (D23)
- [ ] Confirm the checks that replace the second coder, marked orange in Methodology 4.5 (walkthrough re-rating), 4.7.1 and 4.7.2: the two models check cards and pathways, the author re-rates ten walkthroughs and re-decides a sample of decisions after two weeks (D8)
- [ ] Ethics: whether any request is sent to a provider during walkthrough tasks T3, T6 or T7 (Methodology 4.8.1)

## For the next supervisor meeting
- [ ] **Unit of the sample: one app per provider, or every app?** (affects D2, Methodology 4.4.2–4.4.3, Results 5.2)
  - *Idea:* since the sample already keeps one app per provider, match providers across the stores instead of apps, which is simpler.
  - *Catch:* the app-level matching does two jobs a provider match does not. It adds both listings of one app into one score ($P_i = v_i + c\,r_i$); without it, an app listed in both stores ranks below single-store apps. It also gives the 166 pairs that calibrate $c$. Matching providers only works if the ranking also moves to providers: a provider's score is the sum over its apps in both stores, its highest-scoring eligible app enters, and $c$ is calibrated on providers found in both stores.
  - *Provider identity, proposed evidence (strongest first):* (1) the data controller named in the privacy policy, which GDPR Art. 13(1)(a) requires and which fits RQ1–RQ3 (what providers communicate); (2) the trader details the stores show in the EU (name, address, registration number); (3) App Store seller, Impressum, or a shared web domain (today's P1–P3). Open: does a corporate group count as one provider, or each legal entity (for example Leap Fitness, Simple Design, ABISHKKING)?
  - *Exposure concern:* dropping a provider's other apps lowers its share of the app count, but counting apps does not measure exposure either. A clone-heavy provider (Leap: 10 of the 47 most-rated Play apps in the trial, one policy) would weigh 10×, while a single app with far more users weighs 1×. Proposal: keep one app per provider and also report results weighted by the provider's summed popularity score (all its apps in the frame), next to the unweighted ones. The score is a feedback proxy, not a user count, so the weighted results describe relative reach only.
  - *To check first:* a published source showing that apps of one developer share one privacy policy (so far only the trial of 22 Oct shows it).
  - *Questions:* (a) provider or app as unit? (b) controller in the privacy policy as the provider test? (c) group or legal entity? (d) add popularity-weighted results?

## To do
- [ ] Read the Background and Related Work rewrite of 15 Nov (literature → gap → RQ)
- [ ] Discussion: compare findings with earlier literature
