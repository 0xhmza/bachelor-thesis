# Sampling Protocol

**Version:** 2 · **Date:** 2026-10-23 · **Status:** proposed (D1–D7, D11 in the
[Decision Log](../../00_Admin/Decision-Log.md)); fixed before the collection of
23 October 2026. Version 1 (2026-09-18) follows below as history; where the two
differ, version 2 applies.

## Version 2 (2026-10-23)

| Step | Rule | Record |
|---|---|---|
| Frame | German App Store (Search API, `country=de`, iPhone-compatible results) and German Google Play (search page, `gl=de`, `hl=de`); one session, logged out | collector outputs of `appstore-scraper/v007` and `googleplay-scraper/v003` |
| Keywords | 49 queries: the mHealth keywords of Hutton et al. (2018) and the terms of Malki et al. (2024), each in English and German ([keywords.csv](keywords.csv)) | D3 |
| Depth | First 30 results per query in each store; App Store also to 200 for a saturation check | D2 |
| Play pages | Google Play hits ranked by the install band on the search page (ties: best position, package ID); product pages, and so rating counts, for the first 100 only (added 2026-10-24, before the Play collection) | D2; `googleplay-scraper/v004` |
| Preinstalled | Apple Health, Apple Fitness, Samsung Health: own group; their listings leave the rankings; Apple and Samsung count as providers in the sample | D6 |
| Floor | At least 1,000 ratings in the store's own count | D2 |
| Ranking | Within each store by rating count, ties by listing ID | D2 |
| Eligibility | E1 records the user's own health or body data over time in a Hutton or Malki category; E2 consumer app for the general public; E3 free to install; E4 German or English listing; E5 not a DiGA. A policy is **not** required (D5) | [screening.csv](screening.csv), one row per screened listing with the reason |
| Selection | Alternate Google Play, App Store, …; skip a listing whose developer is already in the sample; stop at 47 | D1, D2 |
| Sensitivity | No developer rule; App Store first; depth 20; App Store depth 200; leave one keyword out; English-only and German-only keywords; rating count per year; blend with shrunk average rating | `app-ranking/v002` output |

Screening is done in rank order on the store listing (name, developer, genre,
price, description). A listing is eligible under E1 only if its listing states
that the app records, logs or stores the user's own measurements or activities
(for example workouts, steps, food, weight, cycle, mood, sleep); instructional or
content apps without such a statement, apps that track a child, games, shops and
general-purpose apps are excluded. DiGA are identified by a listing that
describes prescription or reimbursement by statutory health insurance and are
confirmed against the BfArM directory.

# Version 1 (history)

**Version:** 1 (draft) · **Date:** 2026-09-18 · **Status:** superseded by version 2
where they differ; kept for the record.

This file is the operational version of the Sampling paragraph of the proposal (`03_Thesis/proposal/`; argued in full in `99_Archive/2026-10-14_cleanup-recovery.zip` (legacy member `99_Archive/_junk/02_Proposal/sections/04_methodology.tex`) §4.2). Fill in the empty
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
  domain split 3 Android / 3 iOS, filled in rank order **alternating** Android
  and iOS slots, no app twice. The balance serves coverage, not platform
  comparison. Apps that cannot be set up without a paired device, or that need
  payment or identity verification, are skipped with a recorded reason.
- **Validation set:** 10 apps, 5 per domain, drawn at random with a recorded
  seed from providers and documents **not used in the pilot**, stratified by
  the language of the coded policy where both languages occur.

## Search and matching rules

⚠ Proposed defaults — confirm or change them in the pilot, before collection.

- **Collection window:** all keyword searches for one store run within the same
  7-day window; record the dates, device and account state (logged out where
  the store allows).
- **Sponsored results:** results marked as ads ("Anzeige", "Ad") are recorded
  but do not count towards the first 20 and are not eligible.
- **Exact ties** (same average rating and rating count): ordered by app ID,
  which is assigned at random with a recorded seed.
- **Cross-store matching:** an Android and an iOS listing are the same app if
  developer, product name, and privacy-policy URL match; borderline cases are
  logged with the reason.
- **Duplicate vs. different product:** a duplicate is the same provider's app
  with the same core tracking function and the same policy under another name;
  an app with a different core function (e.g. a cycle tracker and a step
  counter from one provider) is a different product. Repeated providers are
  flagged so they are not read as independent.
- **Language:** recorded per source, not per app. English is primary; German is
  used when no English version is available. Where both exist, both are captured
  and differences logged (D7). Search keywords combine German and English terms.
- **Source completeness:** record for each core source whether it was captured,
  is **not offered** by the provider, or **exists but could not be
  retrieved**. Only the last reduces an analysis denominator.

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
| 2026-10-05 | Walkthrough slots alternate Android/iOS; validation set excludes pilot providers and documents; search and matching rules added as proposed defaults | Android-first filling favoured Android; shared policies could leak pilot material into validation; ties, sponsored results, matching, duplicates and source completeness were undefined |
| 2026-10-23 | Version 2: sourced keywords (D3), depth 30 in both stores (D2), rating-count ranking with store alternation (D2), one app per developer (D2), function rule E1 (D3), free to install (D4), policy not required (D5), English first (D7) | Supervisor meeting of 13 October and the app-selection evaluation of 23 October; rules fixed before the collection of that day |
