# App selection and ranking — evaluation, 23 October 2026

An evaluation of the selection rule in the methodology (§ App Sampling) and the
proposed decisions [D1](Decisions/D01_sample-size.md),
[D2](Decisions/D02_ranking-and-rating-floor.md) and
[D6](Decisions/D06_preinstalled-apps.md) as of 22 October. It proposes changes
and changes no decision. All are for the author and the supervisor to accept or
reject in the Decision Log.

**Evidence used.** (1) The Google Play pilot of 22 October
(`scripts/googleplay-scraper/v002/output/pilot-de-19kw.json`, git-ignored; 19
keywords, German storefront, first 20 results), re-analysed with
[`scripts/sampling-checks/v001/check_pool.py`](../scripts/sampling-checks/v001/check_pool.py).
(2) The App Store ranking trial of 22 October
(`scripts/app-ranking/v001/output/`, 2 keywords only). (3) Literature from the
[gap search](../01_Literature/Literature-Gap-Search_2026-10-23.md) and the
digest's stage A chapter.

**Not checked.** No App Store run with all 19 keywords exists, so the App Store
half of the selection could not be simulated. Eligibility (function, language,
payment) was not applied: the counts below are for the ranked pool before
manual screening.

## Verdict

The core idea holds and is better argued than most precedents: rank by
exposure, not by quality, with rating count as a documented download proxy,
each store ranked on its own, and sensitivity variants reported. The pilot
supports the proxy (Spearman 0.96 between Play rating count and installs).
Three problems would change the sample materially and should be settled before
collection:

1. **One provider can take many places.** On Play, Leap Fitness Group holds 10
   of the top 47 apps and 5 of the 24 Play places under alternation, all under
   one policy URL.
2. **The domain mix does not support the per-domain design.** Without quotas,
   about 3 period trackers and 2 pregnancy apps reach the 24 Play places. The
   methodology still reports by domain, plans six walkthroughs per domain and
   draws five validation apps per domain from outside the pilot.
3. **The search frame is not saturated.** More than a quarter of the Play top
   47 (13 apps) was found only at result positions 11–20, and dropping the keyword `Workout`
   alone removes 7 of the 47.

## What holds up

- **The criterion fits the research question.** The thesis studies
  communication that users meet, so exposure is the right target and average
  rating is not. Exposure is concentrated: for depression and anxiety apps on
  Google Play, the top three per condition had about 90 % of downloads and
  monthly users (Wasil et al. 2020), and chart rank falls steeply with
  downloads (Garg and Telang 2013). In the pilot the top 47 Play apps carry
  89 % of all ratings in the pool, the 24 Play places 73 %.
- **The proxy has evidence behind it.** Sunyaev et al. (2015) reported Spearman
  0.89 between rating count and downloads; the pilot replication gives 0.96
  (0.94 above 1,000 ratings).
- **Separate rankings per store are necessary, not cosmetic.** The 24th app
  has 873,216 ratings on Play (worldwide count) and 10,718 on the German App
  Store in the trial: a factor of about 80. Alternating between the two lists
  keeps these bases apart.
- **The documentation is strong.** The endpoint inventory, the storefront field
  check, the sensitivity variants and the rule against lowering thresholds after
  seeing results go further than the app reviews in the digest.

## Problems and proposed changes

### 1. Provider clustering (high)

| Pilot, Play, Samsung Health moved to the preinstalled group | Top 24 (Play half) | Top 47 |
|---|---|---|
| Distinct developers | 18 | 34 |
| Leap Fitness Group | 5 apps, one policy URL | 10 apps, one policy URL |
| Simple Design Ltd. | 3 apps (incl. a period tracker), one policy URL for 2 | 3 |

The methodology codes a shared policy once and links it to all its apps. That
handles coding, but not selection: places spent on one provider's variants
(*Sixpack in 30 Tagen*, *Abnehmen für Männer*, *Abnehm-App für Frauen*, …)
add almost no new communication and reduce the number of independent
providers. RQ1–RQ3 are about what providers say, so the provider is the
natural unit.

**Proposed:** take at most one app per developer (its highest-ranked listing)
and continue down the list. In the pilot this changes 6 of the 24 Play places
and 13 of the top 47, and raises period trackers from 3 to 4 in the Play half.
Report the clustered variant as a sensitivity check. A developer's other apps
can still be listed as sharing the policy.

### 2. Domain mix against the per-domain design (high, needs the supervisor)

| Pilot, Play | Top 24 | Top 47 |
|---|---|---|
| Fitness (incl. sleep, nutrition, steps) | 19 | 37 |
| Period or fertility trackers | 3 | 7 |
| Pregnancy apps (genre *Eltern*, found by `Kinderwunsch`) | 2 | 3 |

If the App Store half looks similar, the sample will hold roughly 6–8 period or
fertility trackers out of 47. The methodology assumes more:

- six walkthrough apps per domain (three Android, three iOS);
- five validation apps per domain drawn from outside the pilot, which itself
  uses two fertility apps, so at least seven fertility apps are needed before
  the walkthroughs are counted;
- results "reported separately for fitness and fertility apps".

The supervisor ruled out quotas such as 30/20. That leaves three consistent
options, each the supervisor's call:

1. Keep one ranking and treat domain as a descriptor only: drop per-domain
   walkthrough and validation slots and per-domain comparisons.
2. Keep one ranking but set a **minimum** per domain (for example 10), filled
   from the domain's own ranked list. This is a floor, not a 30/20 split, but it
   is still a quota and needs explicit approval.
3. Rank each domain separately and split the 47 places in proportion to the
   domains' total rating counts, which keeps the exposure logic.

Separately, D3 must say whether pregnancy apps count as fertility tracking.
They are ranked high (*Schwangerschaft + Tracker-App*, 3.7 million ratings) but
are not period trackers.

### 3. Search frame and keywords (medium to high)

- **Depth.** Of the Play top 47, 9 apps were found only at positions 11–15 and
  4 only at 16–20 (for example *Abnehmen in 30 Tagen*, 1.25 million ratings,
  position 18 for `Workout`). Apps at positions 21+ may well have more ratings
  than the 47th app (309,727). Eight keywords returned fewer than 20 results.
- **Keyword dependence.** 23 of the top 47 were found by one keyword only.
  Leaving out `Workout` removes 7, `Schrittzähler` 4, `Schlaf-Tracker` and
  `Kinderwunsch` 3 each.
- **Missing scope.** The 19 keywords contain no mental-health terms, which the
  meeting asked for (D3 open).

**Proposed:** (a) a saturation check: rerun with 50 results per keyword and
report how many selected apps change; stop increasing depth when the
selection no longer changes. (b) Report a leave-one-keyword-out table as a
sensitivity check. (c) Derive the keyword list from a stated source and test
each term in the store, as Hutton et al. (2018; survey-derived keywords) and
Malki et al. (2024; terms tested in the store) did; add the mental-health terms
or record why not. (d) Store category charts (Health & Fitness, Medical) could
serve as a second, keyword-free frame. Apple publishes them; Play's are
partly reachable (D2 endpoint inventory).

### 4. Eligibility needs a functional tracking rule (medium)

The ranked pool mixes trackers with apps that may not track health data over
time: workout-plan apps (the Leap Fitness group), meditation (*Calm*, found by
`Schlaf-Tracker`), pregnancy and baby apps (genre *Eltern*). The App Store
trial ranked *Google Gemini* second and also contained *Timer Plus* and
*Myprotein* (shopping). The current rule ("collect health or body-related
tracking data") does not decide these cases.

**Proposed:** adopt a function rule from the digest: personal input or sensor
data **recorded over time** (Robillard et al. 2019), not one-off input or
content only; screen on the store page and, where unclear, on the app; log
each exclusion with its reason (Huckvale et al. 2015, additional file).
Gasteiger et al.'s (2023) TECH elements (Target user, Evaluation focus,
Connectedness, Health domain) give a checklist for writing the rule, and
connected-device companions need an explicit line because devices are out of
scope (D11).

### 5. Play's worldwide count and German exposure (medium)

Play counts are worldwide. An app heavily used elsewhere can take a German
place on Play's ranking even if few German users meet it. The current design
states this limitation but does not test it.

**Proposed:** for every Play-selected app, record whether it has a German
listing text and whether it appears in the German Play or App Store category
chart. Report how many selected apps have neither. Chart rank is a
market-specific exposure signal with a published link to downloads (Garg and
Telang 2013). Second, the same app's German App Store rating count, where it
has one, is a German-market cross-check.

### 6. The rating floor does not bind (low; wording)

The 47th Play app has 309,727 ratings and the 24th App Store app in the trial
10,718. A floor of 1,000 never decides a selected app, so the Alfawzan-style
justification in D2 is about the candidate pool and the proxy check, not the
sample. **Proposed:** say so in D2 and in the methodology; keep the floor for
the correlation check and for the case that eligibility exhausts a list.

### 7. Rating counts respond to prompting (low; already a stated limitation)

Google's own case study reports that in-app review prompts raised one app's
rating volume by 64 %. This affects both stores and both domains. The
"rating count per year since release" variant does not address it; the chart
check in point 5 partly does.

### 8. What the sample can claim (low; wording)

Selecting only the most popular apps gives samples that differ systematically
from the store population (Martin et al. 2015). Results should be stated for
"the most-rated fitness and fertility apps in the German storefronts", never
for fitness or fertility apps in general. The limitations section is close to
this already.

## Summary of proposed changes

| # | Change | Affects | Effort |
|---|---|---|---|
| 1 | At most one app per developer; clustered list as sensitivity | D2, methodology | Small (script option) |
| 2 | Decide how domain enters: descriptor only, a minimum, or proportional split; decide pregnancy apps | D1, D3, walkthrough and validation sections | Supervisor decision |
| 3 | Saturation check (50 results), leave-one-keyword-out table, sourced keyword list incl. mental health | D2 (search frame), D3 | Medium (one collector rerun) |
| 4 | Tracking-over-time eligibility rule with an exclusion log | D3, D4 | Small |
| 5 | German chart and listing check for Play-selected apps | D2 | Small to medium |
| 6 | State that the floor does not decide the sample | D2, methodology | Trivial |
| 7–8 | Keep the limitation; tighten the claim wording | Methodology | Trivial |

## Questions for the supervisor

1. Should domain shape the sample (minimum per domain or proportional split), or
   be reported only as a descriptor without per-domain walkthrough and
   validation slots?
2. Is one app per provider acceptable as the selection unit?
3. Are pregnancy apps and workout-plan apps inside "health tracker"?
