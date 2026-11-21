# Editorial Decision: ARS panel review of the thesis draft (03_Thesis-v2)

Review of 21 November 2026, ARS `academic-paper-reviewer` v1.11.1, mode `full`
(contract `reviewer/reviewer_full/v2`). Reviewed: commit `229c7bc`,
`03_Thesis-v2/` (Background, Related Work with RQ1–RQ4, Methodology = Android
app sampling, Results = sample, Appendices A and B). The empty Introduction and
the missing Discussion and Conclusion were out of scope by design. Calibration:
`NOT_CALIBRATED`. No venue was confirmed (`criteria_binding_unavailable`).

Full reviewer cards, Phase 1 commitments, contract, synthesis audit and
provenance: [Panel-Review_Thesis-v2_2026-11-21/](Panel-Review_Thesis-v2_2026-11-21/).

## Review panel provenance

Five seats, each in two fresh model invocations (Phase 1 without the paper,
Phase 2 with it); no seat saw another seat's output before committing. All
Phase 1 and Phase 2 cards passed `check_phase_conformance.py`; the synthesis
passed `check_panel_synthesis.py`; provenance passed `review_panel_provenance.py validate`.

| Axis | Value |
|---|---|
| role_separated | true |
| fresh_context | true (within this panel attempt only) |
| blind_to_peer_outputs | true |
| model_family_distinct | false (all seats: one model family) |
| provider_distinct | false |
| human_distinct | false (no human reviewer) |

Correlated-error disclosure: all model-executed seats used one model family;
role separation does not remove correlated-error risk.

## Decision

### Major Revision (of the written chapters)

```
dimension_verdicts: [D1=block, D2=warn, D3=block, D4=warn, D5=pass, D6=warn]
fired_conditions: [F2, F3, F5]
da_critical_adjudications: []
editorial_decision=major_revision
```

F2 fired because two mandatory dimensions were blocked, both as *repairable*:
D1 methodology rigour (Reviewer 1) and D3 argumentative coherence (Devil's
Advocate). No dimension was blocked as fatal and the Devil's Advocate raised no
CRITICAL issue. In plain terms: the design and the writing hold, and the
counts are correct, but the sampling report and the gap argument need
rewriting and two small extra analyses before the next chapters build on them.
No new data collection is required.

## Blocking issues (immutable source order)

1. **D1 — the sampling procedure is not fully disclosed** (Reviewer 1, block,
   repairable): no information on who screened or on reliability; 44 of the 53
   screening decisions were carried over from the October screening, 3 of them
   made on App Store listings, and the text discloses neither; the stated rule
   for keeping extra queries does not produce the five queries kept.
2. **D3 — two load-bearing claims break as written** (Devil's Advocate, block,
   repairable; Reviewer 1 warn): the well-known-app check is called a test of
   market reach although it tuned the queries it tests; the gap statements
   behind RQ2–RQ4 are contradicted by Malki et al., which the same chapter cites.

## Reviewer summary

| Seat | Scored | Overall signal |
|---|---|---|
| Journal-Fit Reviewer | D5 pass, D6 warn | between minor and major, leaning minor |
| R1 Methodology | D1 block (repairable), D3 warn | every count re-derived and correct; disclosure and rule gaps |
| R2 Domain | D2 warn | all cited numbers correct; gap claims too absolute; Data Safety missing |
| R3 Perspective | D4 warn | needs a yardstick for "unmentioned" harms and an access/ethics statement |
| Devil's Advocate | D3 block (repairable) | no CRITICAL; four MAJOR (M1–M4) |

## Consensus analysis (four non-DA reviewers)

**[CONSENSUS-3]**
- *Unit of analysis*: the RQs speak of providers, the sample counts apps; the
  eight Leap Fitness apps link one policy page (`leap.app/privacypolicy.html`,
  verified in `pages.jsonl`). Raised by Journal-Fit (W2), R1 (W6), corroborated
  by R3; R2 silent. DA M2 agrees.
- *Google Play Data Safety section left out without a reason*: R2 (W2), R3 (W5),
  Journal-Fit (question 3); R1 silent. DA minor 7 agrees.

**Corroborated (two reviewers, no conflict)**
- Android-only scope stated but not argued (Journal-Fit W1, R3 W4).
- Popularity proxy: Malki et al. ranked by reviews of the last 12 months, the
  thesis uses the cumulative count (R1 W4, R2 W7; DA M3). Verified, Malki p. 4.
- Screening disclosure and the Calm/Headspace boundary (R1 W3, Journal-Fit W7;
  DA minor 1). Both screening reasons cite the App Store listing; verified.
- Gap claims for RQ2–RQ4 too absolute (R2 W1, W9; Journal-Fit W4; DA M4).
  Verified in Malki §4.2.7: safeguards in all but one policy, breach risk
  acknowledged in all, responsibility shifted to users in 9/19.
- GDPR baseline sentence too narrow: Recital 39, Art. 13(2)(e), 33–34, 49 (R2 W3,
  R3 W2; DA minor 4).
- Main RQ omits RQ4; "downstream" and "harm communication" undefined (Journal-Fit
  W3, R3 W7).

**Single-reviewer findings (assessed on evidence)**
- Known-app check is circular and its keep rule is order-dependent (R1 W1–W2;
  DA M1). Verified: 7 of the 49 ranked apps enter only through the five added
  queries (Garmin Connect, Zepp, Zepp Life, Mi Fitness, Withings, Da Fit,
  GloryFit); without `fitness tracker`/`Fitnesstracker`, GloryFit is replaced by
  Sleep Monitor.
- No threshold for which harms a provider is expected to state (R3 W1; DA
  "unexamined premise").
- Store access: Google Play's robots.txt disallows `/store/search`; access,
  load and legal basis are not reported (R3 W3).
- Search instability and the effective depth of 8–30 results (R1 W5).

**Points of disagreement:** none (no SPLIT).

## Devil's Advocate

No CRITICAL issue. MAJOR: M1 known-app check as a test (corroborated by R1),
M2 unit of analysis (corroborated by Journal-Fit, R1, R3), M3 proxy precedent
(corroborated by R1, R2), M4 gap overclaim (corroborated by R2, Journal-Fit).
Strongest counter-argument, in short: RQ1/RQ2 risk confirming what the law and
Malki et al. already predict; the original part is RQ3 (protection claims
against harm pathways), which the thesis could lead with.

## Required revisions (must fix)

R1. **Known-app check** — present it as a disclosed extension of the queries to
device companion apps, not as a test; report the untuned result (20 of 25) as
the test; state the rule actually used to keep terms and that the term pool was
open; list the 66 tried terms in an appendix; report the 7 dependent apps and
the GloryFit/Sleep Monitor swap. Cost: section + appendix.

R2. **Screening transparency** — say that one person screened, that 44 decisions
were carried over from 26 October (3 from App Store listings) and re-checked on
the 21 November Google Play pages; resolve Calm vs. Headspace on the Google Play
text; add a blind second rating of the boundary decisions (all exclusions, the
apps around the cut-off, the workout-plan apps) or report how the sample changes
when they are reversed. Cost: small re-analysis.

R3. **Popularity proxy** — describe Malki et al. correctly (12-month count),
state that the cumulative count favours older apps, and show that the count is
scoped to the German storefront (one probe with another `gl`/`hl`). Cost: sentence
+ small check.

R4. **Unit of analysis** — fix before coding: app for the interface, distinct
policy text (or provider) for the policy; report both denominators; align the
word "providers" in the main RQ. Cost: section.

R5. **Gap statements** — narrow the RQ2–RQ4 gaps against Malki §4.2.5/§4.2.7
(no new citation), and phrase absolute absence claims as "the studies reviewed
here". Cost: sentences.

## Suggested revisions (should fix)

- Argue the Android-only choice: reason for one platform, what is excluded
  (~28 % iOS, Apple Health, Apple's label/ATT regime), qualify title or main RQ.
- Define the yardstick for expected harm statements (e.g., tiers from GDPR
  duties and WP29 para. 10) as a decision record before coding.
- State why the Data Safety section is not a surface, or code its sharing and
  security declarations for RQ3.
- Add an access-and-ethics paragraph for the store collection (robots.txt,
  load: 54 searches + 704 pages over 17 min, data minimisation, legal basis).
- Report the search as one snapshot: per-query result counts, the 8–30 range,
  and the depth-20 robustness result (same 49 apps).
- Correct the GDPR baseline sentence (Recital 39; Art. 13(2)(e), 33–34, 49).

## Consider (minor)

Harm definition vs. harm trees and attribution to De and Le Métayer (R2 W4–W5);
law-enforcement access is a flow, not a consequence (R2 W6); Huckvale scope
(R2 W8); main RQ omits RQ4, define "downstream" (Journal-Fit W3, R3 W7); RQ labels
before definition (W6); duplicate "Search" heading (W10); Xiaomi share base (W8);
rank gaps in Table A.1 caption (W9); rule for missing review counts, 264 pages
(R1 W7); where the frozen snapshot is archived (R1 W8; partly contradicted by the claim check, see below); rule for the main-function
category (R1 W9); what the preinstalled rule does when the app ranks above the
cut-off (R1 W10); methodology page budget for later steps (Journal-Fit W5);
stance codes as text features (R3 W6); reason for the DiGA exclusion (R3 W8);
"all 50 apps are free" follows from rule I6 (DA minor 6).

## Revision roadmap

Human-readable, in source order. The machine-readable `revision-roadmap/1.0`
JSON was not emitted, because the draft has no anchorized block manifest; it can
be produced in `academic-paper` revision mode.

| # | Item | Sources | Obligation | Cost scope |
|---|---|---|---|---|
| 1 | Known-app check reframed, keep rule, 66 terms, 7 dependent apps | R1 W1–W2, DA M1 | must_fix | section + appendix |
| 2 | Screening disclosure, second rating or reversal sensitivity, Calm/Headspace | R1 W3, Journal-Fit W7, DA m1 | must_fix | re_analysis (small) |
| 3 | Proxy: Malki 12-month, age bias, storefront scope | R1 W4, R2 W7, DA M3 | must_fix | sentence + check |
| 4 | Unit of analysis per surface | Journal-Fit W2, R1 W6, R3, DA M2 | must_fix | section |
| 5 | Narrow gap claims against Malki §4.2.5/4.2.7 | R2 W1/W9, Journal-Fit W4, DA M4 | must_fix | sentences |
| 6 | Android-only scope argued | Journal-Fit W1, R3 W4 | should_fix | sentences |
| 7 | Yardstick for expected harm statements | R3 W1, DA premise | should_fix | decision record + section |
| 8 | Data Safety section | R2 W2, R3 W5, Journal-Fit Q3, DA m7 | should_fix | sentences or new coding |
| 9 | Access and ethics paragraph | R3 W3 | should_fix | paragraph |
| 10 | Search snapshot and effective depth | R1 W5 | should_fix | sentences + table |
| 11 | GDPR baseline sentence | R2 W3, R3 W2, DA m4 | should_fix | sentence |
| 12 | Minor items listed above | various | consider | sentences |

## Attachment: Suggested-Reference Check (advisory, #1001)

Script output, not a reviewer finding.

| Seat | Reference | Result |
|---|---|---|
| R2 | De and Le Métayer (2016), Privacy Harm Analysis: A Case Study on Smart Grids, doi:10.1109/SPW.2016.21 (already in references.bib) | Found in an index |
| R2 | Pollach (2005), A Typology of Communicative Strategies in Online Privacy Policies, doi:10.1007/s10551-005-7898-3 (already in references.bib) | Found in an index |
| R3 | Ben-Shahar and Schneider (2014), More Than You Wanted to Know | Found in an index |
| R3 | Morgan et al. (2002), Risk Communication: A Mental Models Approach | Found in an index |
| R3 | Fiesler et al. (2020), No Robots, Spiders, or Scrapers | Found in an index |
| R3 | EDPB (2023), Guidelines 03/2022 on deceptive design patterns | Title not matched; no DOI or arXiv ID |
| R3 | Directive (EU) 2019/790 | Title not matched; no DOI or arXiv ID |
| R3 | CJEU C-319/20 | Title not matched; no DOI or arXiv ID |

"Found" means an index holds a record with this title or DOI; it does not show
that the work supports the recommendation.

## Attachment: Reviewer Claim Check (advisory, #1002)

Unchanged script report: [claim_check.txt](Panel-Review_Thesis-v2_2026-11-21/claim_check.txt). The judge (same model family) answered 41 of 41 findings: 1 marked as contradicted, 3 not checkable from the manuscript alone. The contradicted one is R1 W8 (archive location not stated): Listing B.1 does print the screening-file path and the output folder. The finding still holds in part, because the frozen copy in `05_Data/App Sampling/21. Nov/` with its checksums is not named. Deviation: the judge read the prompt file with a file-reading tool instead of receiving it inline; it used no other tool.

## Attachment: Acronym Check (advisory, #849)

The unchanged script report is
[acronym_check.txt](Panel-Review_Thesis-v2_2026-11-21/acronym_check.txt). It ran
on the concatenated LaTeX source, so file markers and company names appear.
Relevant for the text: RQ1–RQ4 are used in §3.1–3.3 before
§3.4 defines them; FAQ, DiGA (defined in Table 4.1 only), UTC and GPS are not
spelled out; "PET" is introduced as "privacy-enhancing technologies (PETs)".
