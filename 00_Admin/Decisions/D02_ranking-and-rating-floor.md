# D2 — How are eligible apps ranked, and what is the rating floor?

- **Status:** proposed, awaiting the supervisor. Author's choice of 22 October 2026, revised 23, 24 and 25 October (history below). The methodology states the current choice. Sample size and preinstalled apps: [D1](D01_sample-size.md), [D6](D06_preinstalled-apps.md); keywords: [D3](D03_scope-keywords-function.md). API order versus store-UI order is unverified and stated as a limitation.
- **Affects:** RQ-sampling · [`scripts/app-ranking/`](../../scripts/app-ranking/README.md) · Methodology, App Sampling

## Current choice (25 October 2026)

- **Frame.** Both stores searched in one session, logged out, German storefronts: Apple's Search API with `country=de` (iPhone-compatible results) and the Google Play search page with `gl=de`, `hl=de`; the 49 queries of D3; the first 30 results per query in each store. The App Store is also searched to 200 results, used only as a saturation check.
- **Measure.** r = German App Store rating count; v = German Google Play review count (the product page's embedded review count, which follows the storefront country). Every Google Play candidate within depth 30 gets its product page (645 apps).
- **Score.** The German-market popularity score is P_i = v_i + c · r_i, where c = median(v_j / r_j) over matched candidates with positive counts in both stores × s_iOS / s_Android. Calibration precedes eligibility screening. The score is expressed in Google Play review-equivalent units and ranks candidates; it does not estimate users, downloads or encounters with privacy communication. StatCounter's shares describe mobile web page views, used here as a proxy for the platform distribution of users. OS shares, September 2026 (read 25 October): Android 72.3 %, iOS 27.7 %.
- **Selection.** The same app in both stores is one candidate. Rank all candidates by descending P_i; break ties by the stable candidate key, as in `app-ranking/v003`. A candidate is skipped when its developer is already in the sample, including the preinstalled vendors; stop at 47 (D1). Developers are matched by developer ID within a store and by normalised name across stores. If a counterpart listing is absent from the search frame, its score contribution is zero; this does not establish that the app is unavailable in that store. No rating floor (it never decided a selected app).
- **Checks.** Spearman correlation of r and v for apps in both stores. Sensitivity, as the number of the 47 providers that change: no developer rule; equal platform weights; pool-sum scale; worldwide Play rating count; the earlier selection (v002); depth 20; App Store depth 200; leave one keyword out; English-only and German-only keywords.
- **Reason.** The thesis prioritises popular apps in the German market. Storefront-specific feedback counts provide an observable proxy when German download counts are unavailable. App Store ratings and Google Play written reviews represent different feedback actions, so one common conversion factor is applied before combining them. Sunyaev et al. (2015, PDF p. 3) support rating counts as a popularity proxy; they do not validate this cross-store conversion. The score is a study-specific sampling rule whose assumptions and sensitivity must be reported.

### Terminology and interpretation clarified (25 October 2026)

At the author's request, the paper calls the unchanged ranking measure the
**German-market popularity score**, denoted P rather than E. This replaces the
earlier name because the observed feedback counts do not measure exposure to
privacy communication. Script v003 retains the output field `exposure`; its
values, calibration and selection are unchanged.

The conversion assumes approximately stable platform-specific feedback rates
across apps and a typical Android-to-iOS user ratio among matched candidates
that follows the platform-share ratio. Under the simplified model
v_i ≈ q_A N_Ai and r_i ≈ q_I N_Ii, the observed ratio includes both the feedback-rate
ratio and the platform-size ratio. Multiplying its median by s_iOS / s_Android
removes the assumed platform-size component, giving c ≈ q_A / q_I. The sum is
then proportional to combined use only under those assumptions. The median
limits the influence of extreme ratios; it does not remove systematic bias.

Evidence: `scripts/app-ranking/v003/rank.py` (`calibration`, `german`, `ranked`)
and `output/report.json` / `output/selection.csv`; Sunyaev et al., PDF p. 3;
StatCounter's page-view basis recorded in `statcounter2026os` in the shared
bibliography. App-specific platform preferences, feedback prompts and the
accumulation of counts over different app lifetimes limit interpretation.
Correlation and selection sensitivity are checks of agreement and stability,
not validation against actual German user counts. D2 remains proposed.

## As run

- **25 October 2026** (`scripts/app-ranking/v003/`): 1,367 candidates, 123 in both stores. c = 0.090 (median v / r = 0.234 over the 114 apps with both counts; Spearman r–v 0.80). 47 apps from 47 providers: 32 in both stores, 9 Google Play only, 6 App Store only. Developer spellings matched by hand (`aliases` in `config.json`): Clue, Pregnancy+, Alarmy, Leap Fitness, Map My Run, Daylio, MeetYou, BabyCenter (24 October), Fddb, Headspace, Macadam, BetterSleep, Babelli (25 October); translated titles paired by hand (`pairs`): Monitor Your Weight, Instant Heart Rate, WalkFit. Providers changed out of 47: pool-sum scale 0, equal weights 5, worldwide Play count 11, earlier selection 10, no developer rule 10. Outcome in the thesis, Results, section "Sample".
- **24 October 2026** (`scripts/app-ranking/v002/`, superseded): Play pages showed 8 to 50 results per query (`happiness` and `Schritte` 50), so depth 30 also cut Google Play. Accents are removed in the developer comparison.

## Evidence

- **Exposure, not quality.** Hutton et al. (2018): popularity measures (downloads, stars, number of ratings) did not predict privacy (card `hutton2018`, p. 6). Sampling rules in the digest cards rank by counts, rank positions or download bands, none by average rating: 300 most frequently rated apps per store (Sunyaev et al. 2015, p. 3); reviews in the preceding 12 months (Malki et al. 2024, p. 4); search rank with a rank-stability check (Huckvale et al. 2019, p. 2); seven most popular apps per category (Hutton et al. 2018); up to the top 250 per category (Arkalakis et al. 2024); weekly top-100 lists (Tangari et al. 2021; Grundy et al. 2019). Alfawzan et al. (2022) used rating values only to justify a floor, because few ratings mean high variance, and checked the next excluded apps (p. 5). Digest summaries, not rechecked against the papers.
- **Supervisor, 13 October:** "ratings or downloads: rating makes more sense, exclude if downloaded less than x times" ([raw notes](../Meeting-Notes/2026-10-13_Supervisor-Meeting_Raw.md)). Whether rating count or average is meant needs confirmation.
- **Downloads.** No verified German download figure exists for either store. Apple's search API returns no downloads; the Play integer is worldwide; Sensor Tower estimates covered 15 of 169 apps before rate-limiting. Rating count as download proxy: Sunyaev et al. (2015) used it on iOS; on Android the two correlated at Spearman 0.89, p < 0.001 (card `sunyaev2015`, p. 3; download measure and sample not described).
- **Storefront check, 22 October 2026** (public Apple lookups and Play product pages; 6 Apple and 5 Play apps; DE, US, GB; one session, run once, so it shows how the fields behave but does not describe every app; scratch scripts not in the repository):
  - Apple rating count and average are storefront-specific (DE / US / GB): Yazio 446,768 / 51,379 / 12,351; Google Gemini 270,417 / 2,363,183 / 241,116; MyFitnessPal 80,176 / 2,381,357 / 474,412.
  - Play rating count and installs are worldwide: Home Workout 4,045,258 ratings in DE and US, 4,045,260 in GB. The average and the embedded review count vary (MyFitnessPal reviews 32,560 DE, 454,136 US).
  - The Play one-to-five-star histogram is the country's distribution scaled to the worldwide total: MyFitnessPal one-star 428,497 DE, 205,443 US; weighted means 3.94 and 4.41 equal the country averages; bins sum to the worldwide count. (A first check had compared only the sums and called it worldwide.)
  - The App Store product page has a storefront histogram the API lacks (Yazio five-star 349,509 DE, 42,759 US). Both stores show a storefront chart badge (Yazio no. 3 in Health & Fitness, German App Store; MyFitnessPal no. 2 top grossing in Health & Fitness, US Play, none in DE); Apple's chart pages (e.g. `apps.apple.com/de/iphone/charts/6013?chart=top-free`) list the storefront's top apps. Chart position is a possible alternative or check, not part of the choice.
  - Apple documents one summary rating per country or region ([Apple ratings help](https://developer.apple.com/help/app-store-connect/monitor-ratings-and-reviews/ratings-and-reviews-overview)); Google announced country-specific phone ratings from November 2021 ([Android Developers Blog](https://android-developers.googleblog.com/2021/08/making-ratings-and-reviews-better-for.html)); downloads go to the developer only ([Apple acquisition help](https://developer.apple.com/help/app-store-connect-analytics/acquisition/acquisition), [Play Console help](https://support.google.com/googleplay/android-developer/answer/139628)).
- **Play review count is German, 25 October 2026:** it follows `gl`, not `hl`. MyFitnessPal 32,562 (`gl=de`), 2,887 (`at`), 454,109 (`us`), unchanged between `hl=de` and `hl=en`; Yazio 41,493 / 3,358 / 2,766.
- **Worldwide reach is not German reach:** among the 100 Play apps chosen by worldwide install band, German reviews ranged from 5 (Mylo) to 99,884 (komoot).
- **Proxy pilot, 22 October 2026** (v002 Play collector, 19 keywords, German storefront, `language` de, first 20 results, no detail errors): 190 distinct apps, 159 with both figures. Spearman worldwide rating count vs embedded installs 0.959 (n = 159); vs install band 0.949; among the 135 apps with at least 1,000 ratings 0.936. Output `scripts/googleplay-scraper/v002/output/pilot-de-19kw.json` (git-ignored). Uses the search page that `robots.txt` disallows, at the author's direction.
- **Evaluation, 23 October 2026** ([App-Selection-Evaluation](../App-Selection-Evaluation_2026-10-23.md), Play pilot re-analysed with `scripts/sampling-checks/v001/`): Leap Fitness Group held 10 of the Play top 47 under one policy URL; the 24 Play places held 3 period trackers and 2 pregnancy apps; 13 of the top 47 were found only at positions 11–20; the 1,000 floor decided no selected app (47th Play app: 309,727 ratings).
- **Blend pilot** (v005 trial output, `fitness` and `fitness sleep-tracker`, Apple DE, 185 listings, 98 above the floor, unfiltered): blending in the shrunk rating changed the top 20 by 3 apps at exposure weight 0.75, 8 at 0.5 and 11 at 0.25; rating count per year changed 1. Mechanics only, not a sample.
- **Equal store depth:** O'Loughlin et al. (2019) capped the App Store at the 250 results Google Play shows so that results "would not be biased towards findings from the iTunes App Store"; Sunyaev et al. (2015) took 300 apps per store (both checked against the PDFs on 22 October). A Play search page returned 20–30 results in a probe on 23 October (`sleep` 28, `Periode` 30, `running` 20); deeper results need the paging endpoint under `/_`.
- **Pool sums distort the scale:** off-topic hits dominate them (Google Play: Roblox 314,584 and Minion Rush 122,681 German reviews), hence the calibration through apps in both stores.

## History of the choice

- **22 October (superseded):** eligibility first, then a floor of 1,000 ratings (reliability threshold after Alfawzan et al.); within each store rank by rating count (log10 recorded; ties by listing ID); no domain quotas (D1); take apps alternately from the two lists, starting with Google Play because Android runs on most German phones (Samsung 39.3 %, Xiaomi 21.4 %, Apple 27.6 % of mobile page views, September 2026, [StatCounter](https://gs.statcounter.com/vendor-market-share/mobile/germany)); skip an app already selected through the other store; stop at 47. Proportional allocation by OS share was rejected because it would compare counts on different bases. Average rating, Play review count and install band recorded for sensitivity only (blends at 0.75, 0.5, 0.25; rating count per year). Earlier the same day: draft rule (floor 1,000, rank by average rating, count as tie-break) → blended score → exposure only; percentile merge → alternation.
- **23 October (kept):** search frame and one app per developer, fixed before that day's collection. Reason for the developer rule: one developer held 10 of the Play top 47 under one policy URL ([evaluation](../App-Selection-Evaluation_2026-10-23.md) §1); RQ1–RQ3 concern what providers communicate. It replaced "skip an app already selected through the other store". Added checks: no developer rule; App Store first; depth 20; App Store depth 200; leave one keyword out; English-only and German-only keywords; for each Play-selected app, whether it is in the German App Store and with how many ratings (evaluation §5).
- **24 October (superseded):** product pages limited to 100. The first Play run (23 October, `googleplay-scraper/v003`) took about 5 s per page and was stopped after 2 h 50 min with no output; the 49 queries reach up to about 1,500 distinct apps. Play hits were ranked by the install band on the search page (present for 30 of 30 hits of `Periode`, 20 of 20 of `running`, 24 October), ties by best position and package ID; only the first 100 got pages. Collector fix found in the same probe: the parser misses the app ID of the highlighted top result (for `running`, adidas Running); `googleplay-scraper/v004` reads it from the details URL.
- **25 October (current), author's direction:** the alternation compared a German App Store ranking with a worldwide Play ranking. Replaced by one German ranking; the 100-page limit and the floor were dropped. The first formula, E = s_iOS · r / R + s_Android · v / V with R and V the sums over each store's candidates, was amended to the calibrated scale after the page collection and before any ranking was computed; it remains a sensitivity check.

## Would change if

- The supervisor means the average rating, prefers downloads or asks for a different weighting.
- A verified German install or rating figure becomes available for Google Play (for example a licensed estimate with a country filter).
- The sensitivity variants change most of the selection.

## Endpoint inventory (checked 22 October 2026)

Every interface known to give store data on ratings, reviews, downloads or popularity, including interfaces that `robots.txt` disallows and interfaces open only to an app's developer. "Regional": the value depends on the storefront requested. Each was called once or a few times for Yazio (App Store, id 946099227) and MyFitnessPal (Google Play, `com.myfitnesspal.android`). Ignoring `robots.txt` is the author's decision; store terms may also restrict automated access, which the ethics section should address. Robots rules: `itunes.apple.com` disallows `/search*`, `/*/lookup?` and `/*/rss/*`; `apps.apple.com` product and chart pages are allowed; Google Play disallows `/store/search`, `/store/getreviews` and `/_` and allows product pages. Apple documents the Search API for programmatic use; whether the robots rule applies to it is open.

**App Store, public**

| Interface | Data | Regional | robots.txt | Result |
|---|---|---|---|---|
| Search API `itunes.apple.com/search` ([docs](https://performance-partners.apple.com/search-api)) | rating count and average, also for the current version; result order | storefront | disallowed | works; used by the collectors |
| Lookup API `itunes.apple.com/lookup?id=…&country=…` | same fields for known IDs | storefront | allowed without a country path segment | works |
| Product page `apps.apple.com/<cc>/app/id…` | rating count, average, 1–5★ histogram, chart badge, a few review texts; schema.org `reviewCount` equals the rating count | storefront | allowed | works; repeated requests gave HTTP 429 |
| Chart page `apps.apple.com/<cc>/iphone/charts/6013?chart=top-free` | top 50 Health & Fitness, rank only | storefront | allowed | works |
| Old RSS chart `itunes.apple.com/<cc>/rss/topfreeapplications/limit=200/genre=6013/json` | top 100 by category | storefront | disallowed | works |
| Old RSS reviews `itunes.apple.com/<cc>/rss/customerreviews/page=N/id=…/sortBy=mostRecent/json` | newest 500 reviews (10 pages of 50): text, stars, version, votes, date | per storefront URL (DE and US not compared) | disallowed | works; no total count |
| RSS v2 `rss.marketingtools.apple.com/api/v2/<cc>/apps/top-free/N/apps.json` | overall top apps, rank only | storefront | no rules | works; no category filter |
| Web-store API `amp-api.apps.apple.com/v1/catalog/<cc>/apps/…` | ratings and paged reviews | storefront | — | not reached: no access token found |

**Google Play, public**

| Interface | Data | Regional | robots.txt | Result |
|---|---|---|---|---|
| Product page `play.google.com/store/apps/details?id=…&gl=…` | rating count (worldwide), average (country), histogram (country shape scaled to the worldwide total), embedded review count (country, not displayed), install band and exact integer (worldwide), chart badge (country) | mixed | allowed | works |
| Search page `/store/search` | result order | storefront | disallowed | works; used by the collectors |
| Reviews RPC `/_/PlayStoreUi/data/batchexecute` | review text, stars, version, thumbs-up, developer reply; paged | **by language, not country** (`lang=de` gave the same 50 newest reviews for DE and US) | disallowed | works; no total count |
| Data safety page `/store/apps/datasafety?id=…` | data collected and shared, security practices | — | disallowed | works |
| Permissions RPC | permission groups | — | disallowed | works |
| Category page `/store/apps/category/HEALTH_AND_FITNESS` | short ranked carousels | country | allowed | works |
| Top-charts RPC (Node library `list()`) | full category charts | country | disallowed | untested; not in the Python library 1.2.7 |

**Developer only:** App Store Connect Analytics (total, first-time and redownloads by territory, bulk export through the analytics reports API; ratings and reviews per country or region); Play Console (installs and uninstalls by country; all reviews). **Third party** (modelled estimates): Sensor Tower, Appfigures, AppMagic, AppTweak, 42matters; Sensor Tower rate-limited after 15 of 169 apps, Appfigures required an account for German data.

**Conclusion.** No public interface gives German download counts. The public market-specific signals are the App Store storefront rating count and histogram, the Play country average, histogram shape and embedded review count, and the chart positions in both stores.
