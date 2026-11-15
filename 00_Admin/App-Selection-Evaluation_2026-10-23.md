# App selection and ranking — evaluation, 23 October 2026

Evaluation of the selection rule (methodology, App Sampling) and of
[D1](Decisions/D01_sample-size.md), [D2](Decisions/D02_ranking-and-rating-floor.md)
and [D6](Decisions/D06_preinstalled-apps.md) as of 22 October. It proposes
changes and decides nothing. Outcomes: §1 and §3–§6 were adopted in D2 and D3 on
23 October; §5 was superseded by the German ranking of 25 October (D2).

**Evidence.** (1) Google Play pilot of 22 October
(`04_Study/4.4_App-Sampling/scripts/googleplay-scraper/v002/output/pilot-de-19kw.json`, git-ignored; 19
keywords, German storefront, first 20 results), re-analysed with
[`04_Study/4.4_App-Sampling/scripts/sampling-checks/v001/check_pool.py`](../04_Study/4.4_App-Sampling/scripts/sampling-checks/v001/check_pool.py).
(2) App Store ranking trial of 22 October (`04_Study/4.4_App-Sampling/scripts/app-ranking/v001/output/`,
2 keywords). (3) The [gap search](../01_Literature/review/Gap-Search_2026-10-23.md)
and the digest's stage A. **Not checked:** no App Store run with all 19 keywords
existed; eligibility was not applied, so counts are for the ranked pool before
screening.

## What holds up

- Exposure, not quality, fits the research questions. Exposure is concentrated:
  for depression and anxiety apps on Google Play, the top three per condition had
  about 90 % of downloads and monthly users (Wasil et al. 2020); chart rank falls
  steeply with downloads (Garg and Telang 2013). In the pilot the top 47 Play apps
  carry 89 % of the pool's ratings, the 24 Play places 73 %.
- The proxy: Sunyaev et al. (2015) Spearman 0.89 between rating count and
  downloads; the pilot gives 0.96 (0.94 above 1,000 ratings).
- Separate store rankings were needed: the 24th app has 873,216 ratings on Play
  (worldwide) and 10,718 on the German App Store (trial), a factor of about 80.
- Documentation (endpoint inventory, storefront check, sensitivity variants, no
  lowering of thresholds after seeing results) goes further than the app reviews
  in the digest.

## Problems and proposed changes

### 1. Provider clustering (high)

| Pilot, Play, Samsung Health in the preinstalled group | Top 24 (Play half) | Top 47 |
|---|---|---|
| Distinct developers | 18 | 34 |
| Leap Fitness Group | 5 apps, one policy URL | 10 apps, one policy URL |
| Simple Design Ltd. | 3 apps (incl. a period tracker), one policy URL for 2 | 3 |

Coding a shared policy once handles coding, not selection: variants such as
*Sixpack in 30 Tagen*, *Abnehmen für Männer*, *Abnehm-App für Frauen* add almost
no new communication. **Proposed:** at most one app per developer, clustered list
as sensitivity check. In the pilot this changes 6 of the 24 Play places and 13 of
the top 47 and raises period trackers in the Play half from 3 to 4.

### 2. Historical category-allocation concern — superseded by D15

**Update, 28 October 2026:** the author confirmed health trackers as the single study domain ([D15](Decisions/D15_health-tracker-domain.md)). Categories inform scope and keyword collection only. Pilot, validation and walkthrough totals now apply across the sample. The concern below records the earlier draft and is no longer an open design objection.

| Pilot, Play | Top 24 | Top 47 |
|---|---|---|
| Fitness (incl. sleep, nutrition, steps) | 19 | 37 |
| Period or fertility trackers | 3 | 7 |
| Pregnancy apps (genre *Eltern*, found by `Kinderwunsch`) | 2 | 3 |

Expected: roughly 6–8 period or fertility trackers of 47. The methodology assumes
six walkthrough apps per domain, five validation apps per domain from outside the
pilot (which uses two fertility apps, so at least seven fertility apps), and
separate reporting by domain. With quotas ruled out, the options are: (1) domain
as a descriptor only; (2) a minimum per domain (e.g. 10), still a quota needing
approval; (3) separate domain rankings with places in proportion to their total
rating counts. D3 must also say whether pregnancy apps count
(*Schwangerschaft + Tracker-App*, 3.7 million ratings, is not a period tracker).

### 3. Search frame and keywords (medium to high)

- Depth: of the Play top 47, 9 were found only at positions 11–15 and 4 only at
  16–20 (e.g. *Abnehmen in 30 Tagen*, 1.25 million ratings, position 18 for
  `Workout`); apps beyond 20 may exceed the 47th (309,727 ratings). Eight keywords
  returned fewer than 20 results.
- Keyword dependence: 23 of the top 47 were found by one keyword only; leaving out
  `Workout` removes 7, `Schrittzähler` 4, `Schlaf-Tracker` and `Kinderwunsch` 3 each.
- The 19 keywords had no mental-health terms, which the meeting asked for.

**Proposed:** saturation check at 50 results per keyword; leave-one-keyword-out
table; a sourced keyword list tested in the store, as Hutton et al. (2018) and
Malki et al. (2024) did; store category charts as a possible keyword-free frame.

### 4. Functional tracking rule (medium)

The pool mixes trackers with workout-plan apps (Leap Fitness), meditation (*Calm*,
found by `Schlaf-Tracker`) and pregnancy and baby apps; the App Store trial ranked
*Google Gemini* second and contained *Timer Plus* and *Myprotein* (shopping).
**Proposed:** personal input or sensor data recorded over time (Robillard et al.
2019), screened on the store page, each exclusion logged with its reason (Huckvale
et al. 2015); Gasteiger et al.'s (2023) TECH elements as a checklist; an explicit
line for device companions (D11).

### 5. Play's worldwide count and German exposure (medium)

An app used mostly elsewhere can take a German place on Play's worldwide count.
**Proposed:** for every Play-selected app, record a German listing text and a
German chart position (Garg and Telang 2013), and the same app's German App Store
rating count as a cross-check.

### 6. The rating floor does not bind (low)

The 47th Play app has 309,727 ratings, the 24th App Store app in the trial
10,718; a floor of 1,000 decides no selected app. **Proposed:** say so in D2 and
the methodology.

### 7. Rating counts respond to prompting (low)

Google's case study reports that in-app review prompts raised one app's rating
volume by 64 %; this affects both stores. Already a stated limitation.

### 8. What the sample can claim (low)

Samples of the most popular apps differ systematically from the store population
(Martin et al. 2015): state results for the most-rated apps in the German
storefronts only.

## Questions for the supervisor

1. Resolved by the author on 28 October 2026 (D15): health trackers form one study domain; categories are descriptors and source-paper vocabulary, with no category-specific walkthrough or validation slots.
2. Is one app per provider acceptable as the selection unit?
3. Are pregnancy apps and workout-plan apps inside "health tracker"?
