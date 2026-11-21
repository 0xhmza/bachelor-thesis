# Known-app check of the Android search (21 November 2026)

Decision: [D27](../../00_Notes/Decisions.md). Collection: `scripts/googleplay-scraper/v007/`
(frozen copy in `05_Data/App Sampling/21. Nov/`).

## Why

The sample should contain the health trackers that most people know. If a
well-known tracker does not appear in any search result, the queries miss part
of the market. The check tests the queries, not the ranking: an app that is
found but has fewer German reviews than the last selected app is correctly left
out by the popularity rule.

## Rules

1. The list of well-known apps was fixed before the check (below). It covers
   running and cycling, nutrition and weight, sleep, mood, the menstrual cycle
   and the companion apps of the largest wearable and scale brands.
2. An app passes when it is among the first 30 results of at least one query.
3. For a missing app, a generic term for its function or device is added in
   English and German, and the search is repeated. Brand or product names are
   never used, because they would favour single providers.
4. The check does not force any app into the sample.

Two further apps were considered and dropped from the list before the check,
because they are not offered in the German Google Play storefront (store page
returns 404): Huawei Health (`com.huawei.health`) and Mi Fitness under the
package name `com.mi.health`.

## Rounds

| Round | Queries | Result |
|---|---|---|
| 0 | the 49 queries of Hutton et al. and Malki et al. | 20 of 25 found; missing: Garmin Connect, Zepp, Zepp Life, Polar Flow, Withings (all companion apps of devices) |
| 1 | + `fitness tracker`, `Fitnesstracker`, `smartwatch` | Garmin Connect and Zepp found (`fitness tracker` 9 and 13, `Fitnesstracker` 9 and 10) |
| 2 | + 35 device and generic terms, for example `fitness band`/`Fitnessarmband`, `activity tracker`/`Aktivitätstracker`, `health tracker`/`Gesundheitstracker`, `smart band`, `smartband`, `sleep tracker`/`Schlaftracker`, `smart scale`/`Körperwaage`, `scale`/`Waage`, `Personenwaage`, `heart rate monitor`/`Pulsuhr`, `blood pressure`/`Blutdruck` | Zepp Life found by `smartband` (1), `smart band` (22), `sleep tracker` (29); Withings by `Waage` (17), `Personenwaage` (18) |
| 3 | + 13 terms aimed at sports watches, for example `running watch`/`Laufuhr`, `sports tracker`/`Sporttracker`, `heart rate sensor`/`Pulsmesser`, `training plan`/`Trainingsplan`, `multisport` | Polar Flow still not found |

In total 66 generic queries were tried beyond the 49 (probe log:
`05_Data/App Sampling/21. Nov/Raw/known-apps-probe.json`). The smallest set that
finds every reachable app was kept and added to the collection:

| Added query | Language | Finds |
|---|---|---|
| fitness tracker | EN | Garmin Connect, Zepp |
| Fitnesstracker | DE | Garmin Connect, Zepp |
| smartband | EN and DE (same word) | Zepp Life |
| scale | EN | (pair of `Waage`) |
| Waage | DE | Withings |

`smartwatch` was not kept: it found no listed app that the kept queries miss.
`scale` finds none of the listed apps but stays as the English half of the pair.

## Result of the collection run

The full run of 21 November 2026 used the 54 queries. Google Play search is not
fully stable between runs (a few positions moved between the probe runs and the
main run), so the table below is taken from the main run (`search.json`). "Base" says whether one of the 49 original queries
finds the app; "found by" gives up to three queries with the position.

| App | Package | Base | Found by (position) | Outcome |
|---|---|---|---|---|
| Strava | `com.strava` | yes | cycling (5); Radfahren (2); Training (16) | in sample |
| adidas Running | `com.runtastic.android` | yes | Training (10); running (1); Laufen (6) | in sample |
| Nike Run Club | `com.nike.plusgps` | yes | Training (7); running (3); Laufen (3) | in sample |
| komoot | `de.komoot.android` | yes | cycling (2); Radfahren (1); Laufen (8) | in sample |
| ASICS Runkeeper | `com.fitnesskeeper.runkeeper.pro` | yes | running (5); Laufen (4); Fitnesstracker (20) | in sample |
| Pacer | `cc.pacer.androidapp` | yes | walking (14); steps (5); Schritte (5) | in sample |
| Google Fit | `com.google.android.apps.fitness` | yes | exercise (7); heart rate (27); walking (21) | in sample |
| Fitbit (Google Health) | `com.fitbit.FitbitMobile` | yes | heartrate (5); heart rate (5); fitness tracker (7) | in sample |
| Garmin Connect | `com.garmin.android.apps.connectmobile` | no | fitness tracker (9); Fitnesstracker (9); smartband (8) | in sample |
| Samsung Health | `com.sec.android.app.shealth` | yes | heartrate (6); heart rate (6); Schritte (7) | in sample (preinstalled) |
| Zepp Life | `com.xiaomi.hm.health` | no | smartband (1) | in sample |
| Zepp | `com.huami.watch.hmwatchmanager` | no | fitness tracker (13); Fitnesstracker (10); smartband (9) | in sample |
| Polar Flow | `fi.polar.polarflow` | no | — | not found |
| Withings | `com.withings.wiscale2` | no | Waage (17) | in sample |
| MyFitnessPal | `com.myfitnesspal.android` | yes | diet (5); Diät (2); Ernährung (1) | in sample |
| Yazio | `com.yazio.android` | yes | diet (9); Diät (6); Ernährung (5) | in sample |
| Lifesum | `com.sillens.shapeupclub` | yes | diet (8); Diät (7); Ernährung (2) | in sample |
| FatSecret | `com.fatsecret.android` | yes | diet (1); Diät (1); Ernährung (4) | in sample |
| WeightWatchers | `com.weightwatchers.mobile` | yes | weight (3); Fitnesstracker (30); smartband (29) | in sample |
| Flo | `org.iggymedia.periodtracker` | yes | female health (2); Frauengesundheit (2); reproduktive Gesundheit (2) | in sample |
| Clue | `com.clue.android` | yes | female health (7); Frauengesundheit (7); reproductive health (3) | in sample |
| Natural Cycles | `com.naturalcycles.cordova` | yes | fertility (27); contraception (4); birth control (1) | found; rank 195 (171 German reviews), below the cut-off |
| Sleep Cycle | `com.northcube.sleepcycle` | yes | sleep (2); Schlaf (2) | found; rank 80 (1,989 German reviews), below the cut-off |
| Sleep as Android | `com.urbandroid.sleep` | yes | sleep (1); Schlaf (3) | in sample |
| Daylio | `net.daylio` | yes | mood (5); Stimmung (10) | in sample |

Summary: the 49 original queries find 20 of the 25 apps; with the five added
queries 24 are found. 22 of the 24 are in the sample; Natural Cycles and Sleep
Cycle are found but have fewer German reviews than the last selected app
(4,142). The check therefore supports the queries for every category except
sports-watch companion apps (Polar Flow).

## Limits

- Polar Flow (`fi.polar.polarflow`, 10,314 German reviews) is not reached by
  any generic query that was tried. Google Play ranks it below position 30 for
  every such term; only its brand name would find it, which rule 3 excludes.
- The list of well-known apps is the author's own. It is a plausibility check
  of the queries, not a measure of market coverage.
