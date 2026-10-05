# Sampling Protocol

**Version:** 1 (draft) · **Date:** 2026-09-18 · **Status:** awaiting supervisor
confirmation of the points marked ⚠ in
[`00_Admin/Open-Points.md`](../../00_Admin/Open-Points.md)

This file is the operational version of the Sampling paragraph of the proposal (`03_Thesis/proposal/`; argued in full in `99_Archive/_junk/02_Proposal/sections/04_methodology.tex` §4.2). Fill in the empty
cells **before** collecting anything, and do not change the protocol afterwards
without an entry in the change log at the bottom. The methodology chapter is
written from this document.

## Platforms

| Platform | Storefront | Device / locale | Access method | Date range of collection |
|---|---|---|---|---|
| Google Play Store | Germany (de) | Android, region DE, system language DE | manual capture; automated retrieval only if the store terms permit | |
| Apple App Store | Germany (de) | iOS, region DE, system language DE | manual capture; automated retrieval only if the store terms permit | |

Check each store's terms of service before any automated collection and record
the date of that check here:

| Store | Terms checked on | Automated collection permitted? | Note |
|---|---|---|---|
| Google Play | | | |
| Apple App Store | | | |

## Search keywords

The seed list is frozen before collection. Every keyword actually used is
recorded here in the language it was used in. Additions after freezing go in the
change log with a reason.

### Fitness and activity domain

| # | Keyword | Language | Rationale |
|---|---|---|---|
| F1 | Fitness | de/en | umbrella term, both stores |
| F2 | Fitness Tracker | de/en | device-paired apps |
| F3 | Schrittzähler | de | step counting, the most common entry point |
| F4 | Aktivitätstracker | de | activity tracking |
| F5 | Schlaf-Tracker | de | sleep tracking |
| F6 | Herzfrequenz | de | heart-rate monitoring |
| F7 | Kalorienzähler | de | nutrition / calorie tracking |
| F8 | Ernährungstagebuch | de | food diary |
| F9 | Workout | en | used untranslated in German listings |

### Fertility and period domain

| # | Keyword | Language | Rationale |
|---|---|---|---|
| P1 | Periode | de | most common German term |
| P2 | Zyklus | de | cycle tracking |
| P3 | Zyklustracker | de | compound used in listings |
| P4 | Menstruation | de | clinical term |
| P5 | Eisprung | de | ovulation |
| P6 | Fruchtbarkeit | de | fertility |
| P7 | Kinderwunsch | de | conception-oriented apps |
| P8 | period tracker | en | used untranslated in German listings |
| P9 | ovulation | en | as above |
| P10 | fertility | en | as above |

## Categories considered

- [x] Health & Fitness
- [x] Medical
- [ ] Lifestyle — only if an app surfaced by a keyword sits there; not searched directly
- [ ] Other: ___

## Inclusion criteria

An app is included if **all** of the following hold:

1. It is available in the German storefront of at least one of the two platforms.
2. It collects health, fitness, or body-related self-tracking data from the user
   or from a paired device.
3. It is free to install, so the walkthrough can reach onboarding without a
   purchase.
4. A privacy policy is reachable from the store listing.
5. Its interface is available in German or English.

## Exclusion criteria

An app is excluded if **any** of the following hold:

1. No privacy policy is reachable, or the link is dead at capture time.
   → Record it as a finding first, then exclude from text coding.
2. It is a DiGA (listed in the BfArM DiGA directory). Apps certified as
   medical devices but freely installable are **not** excluded; they are
   flagged in the `Medical device` field, since users meet them in the same
   search results.
3. It is a pure device companion with no tracking function of its own.
4. *(Walkthrough eligibility only.)* Account creation requires identity
   verification or payment (forbidden by the ethics rules — see
   [`../Ethics/README.md`](../Ethics/README.md)). Such apps stay in the
   document sample, which needs no account; they are skipped in walkthroughs
   with a recorded reason.
5. It duplicates an app already in the sample from the same provider under a
   different name.

## Ranking and cut-off

- **Per keyword:** record the first **20** results in the store's default
  ordering, together with average rating and rating count.
- **Filter:** keep only apps with **≥ 1,000 ratings** on the platform in
  question — a practical threshold to limit reliance on very small rating
  counts, not a statistical cut-off.
- **Ranked by:** average store rating, descending.
- **Ties broken by:** rating count, descending.
- **Target sample size:** **50 apps**, stratified **30 fitness / 20 fertility**.
- **Pilot:** 5 apps (3 fitness, 2 fertility) collected and coded first to test
  the instruments. Pilot apps are re-coded with the final instruments and stay
  in the sample, but are **kept out of the validation set**, because they
  shaped the codebook and prompts.
- **Unit:** the app, not the listing. An app on both stores is one sample
  member with two listings, ranked by the rating-count-weighted mean of its two
  average ratings.
- **Walkthrough subsample:** 12 apps, **balanced** 6 fitness / 6 fertility, each
  domain split 3 Android / 3 iOS: the highest-ranked eligible app for each slot,
  no app twice. Apps that cannot be set up without a paired device are not
  eligible for the walkthrough.

## What is recorded per app

| Field | Notes |
|---|---|
| App ID | stable internal identifier, used in every downstream file |
| App name | as shown in the German storefront |
| Developer | as shown in the store listing |
| Platform | Play / App Store / both |
| Store category | |
| Keyword(s) that surfaced it | may be several |
| Rating and rating count | **as of the capture date**, per platform |
| App version | |
| Privacy policy URL | |
| Policy language(s) captured | de / en / both |
| Structured disclosure captured | Data Safety section / Privacy Nutrition Label |
| Capture date | **mandatory** |
| SHA-256 of each archived file | **mandatory** |
| Domain stratum | fitness / fertility |
| Medical device | certified as a medical device? yes/no, with class if stated |
| Walkthrough done? | yes/no, date |

## Freeze

| | |
|---|---|
| Corpus frozen on | |
| Number of apps in the final sample | |
| Number excluded, with reasons | see exclusion log |

## Change log

| Date | Change | Reason |
|---|---|---|
| 2026-09-18 | Initial version written from §4.2 of the proposal | Closes action item 7 of the 2026-09-05 supervisor input |
| 2026-09-29 | Medical-device apps no longer excluded, only DiGA; `Medical device` field added | Excluding them would drop certified contraceptive apps that users meet in the same fertility results |
| 2026-09-29 | Pilot apps kept out of the validation set | They shaped the instruments, so validating on them would overstate accuracy |
| 2026-09-29 | Unit of analysis and walkthrough selection rule stated | Both were implicit; the proposal now states them |
