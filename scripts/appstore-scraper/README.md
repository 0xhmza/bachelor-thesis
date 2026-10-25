# App Store scraper

Each scripting project gets its own folder under `scripts/`, with named versions
`v001/`, `v002/`, etc. Outputs stay in the version's `output/` folder.

- `v001/`: previous full collector, with product-page enrichment and tests.
- `v002/scraper.py`: minimal standard-library collector; all returned API fields
  for iPhone-compatible apps, up to 200 API results per keyword. English requested.
- `v003/scraper.py`: previous selected-fields version with null placeholders.
- `v004/scraper.py`: previous version; omits unavailable fields, App Name first,
  optional `--downloads` retrieves public monthly download estimate ranges.
- `v005/scraper.py`: compact Apple-only collector for sampling/ranking
  metadata, including original API position and per-keyword collection provenance.
- `v006/scraper.py`: shortest working version, shown in Appendix E of the thesis.
  Input is a JSON file, output is JSON on stdout, and fewer fields are kept
  (see the `fields` map). Run
  `python scripts/appstore-scraper/v006/scraper.py scripts/appstore-scraper/v006/input.json > scripts/appstore-scraper/v006/output/run.json`
  after creating `v006/output/`. The `Rating Count` fields keep the v005 names, so
  `app-ranking` reads the output unchanged.
- `v007/scraper.py`: sampling collector of 23 October 2026 (D2, D3). Same input and
  output form as v006, plus developer ID, seller, bundle ID, genres, version, content
  rating, full description and seller URL; logs every request (URL, time, returned
  count, SHA-256) under `requests` and backs off on HTTP 403/429/5xx. `input.json`
  holds the 49 keywords of `04_Study/App-Sample/keywords.csv` with `limit` 200; the
  ranking uses the first 30 positions and the rest only for a saturation check.

```powershell
python scripts/appstore-scraper/v005/scraper.py fitness --region de
python scripts/appstore-scraper/v005/scraper.py fitness "sleep tracker" -r de --limit 20
```

Prints the saved JSON path. File names contain the project, region, keywords and
UTC timestamp, e.g. `appstore-scraper-de-fitness-sleep-tracker-20261020T190000000000Z.json`.
JSON contains `region`, `timestamp`, and `results` mapping each keyword to its apps.
The default region is `de`. Region is a storefront, and positions reflect API
order. API downloads and product-page-only privacy details are not included.

## Current sampling data (v005)

App Name comes first. Records retain IDs, genres, developer/seller identity,
release/update dates and version, average ratings and rating counts (overall and
current version), price/currency, languages, age/content advisories, descriptions,
release notes, minimum iOS, features, screenshots, icon and provider/store links.
Each record also retains its original `API Position`, assigned before iPhone
filtering. Results stay in returned order; repeated apps remain under each
matching keyword, preserving cross-query discovery evidence. The root records
region, requested language/limit, collection timestamp and per-keyword request
URL, capture time and returned count. `--limit` is 1–200, default 200.

This captures observable listing and rating signals relevant to selection and
visibility; it does not measure users' preferences, impressions, exposure or
downloads. API position is not verified native iPhone App Store search rank.
No ranking score, eligibility threshold or final sample is imposed. An API limit
is a requested cap, and no exhaustive coverage is claimed. If the study uses a
native-store first-N rule, those interface results need separate capture.

The requested Dev. Type, Downloads, written Reviews and 2023 review counts are
not supplied by this API, so they remain omitted from app records. `Seller`
provides related developer identity without inferring an individual/company
classification. Rating Count counts ratings, not written reviews or downloads;
the script does not reproduce Malki et al.'s preceding-12-month review measure.
Missing/null fields are omitted; real zeros and observed empty lists are kept.
This version uses Apple directly and has no third-party estimate option.

`v003` keeps App Name, ID, Genre, Dev. Name, Dev. Type, Released, Downloads,
Ratings, Rating Count, Reviews, Reviews (2023), Version, Updated, Price, Currency,
Seller, App URL and Developer URL, in that order. Ratings is the average score;
Rating Count counts ratings, not written reviews. Dev. Type, Downloads, Reviews
and Reviews (2023) remain `null` because this API response does not provide them.
The capture is current; it does not reconstruct historical 2023 statistics.

`v004` removes the unavailable fields entirely and names the average score
`Average Rating`. Any missing/null API fields are omitted while real zero values,
such as a free download price, are retained.

## Rating counts are storefront-specific (checked 22 October 2026)

Apple's `lookup` returns different `userRatingCount` and `averageUserRating` values
per `country`, and `scraper.py` requests with `country=<region>`. With the default
`--region de`, `Rating Count` therefore describes the German storefront. Example
(DE / US / GB): Yazio 446,768 / 51,379 / 12,351; Google Gemini 270,417 / 2,363,183 /
241,116; MyFitnessPal 80,176 / 2,381,357 / 474,412. The check covered 6 apps and
3 storefronts in one session. The Google Play counterpart does not behave this way, see
[the Play README](../googleplay-scraper/README.md) and
[D2](../../00_Admin/Decisions/D02_ranking-and-rating-floor.md).

## Download sources checked on 20 October 2026

The optional `--downloads` flag extracts Sensor Tower's public overview metadata
for each distinct app ID. For example, the [Home Workout overview](https://app.sensortower.com/overview/1313192037?country=US)
currently exposes `100k-500k` downloads for "Last month"; MyFitnessPal exposes
`500k-1m` and Apple Fitness `< 5k`. The script retains these strings as reported,
with the source URL, retrieval timestamp and period under `Estimated Downloads`.
It does not turn a range into a precise number. Failed/missing estimates are
omitted from app records and recorded separately in `estimate_errors`.
Requests are spaced by four seconds; an HTTP 429 stops estimate collection and
records `estimate_collection_stopped`, retaining all App Store candidates.

The first full `fitness` trial obtained 15 estimate ranges for 169 apps before
the provider rate-limited the requests. That trial preceded the stop-on-429
guard and recorded 154 HTTP 429 errors. It establishes only partial coverage;
the free public pages are not a demonstrated reliable bulk data source.

These are third-party estimates, not Apple-reported cumulative counts. The
public overview's download card labels its metric worldwide. The retrieved HTML
metadata does not itself state geography or exact date boundaries, so the script
does not assert either. `country=US` selects the provider's overview context;
neither that parameter nor this script's `--region de` makes the estimate German.
The date of the HTTP capture also does not prove when a provider refreshed its
estimate. The unversioned metadata wording can change; bulk coverage and accuracy
are not established by the initial three-app check. No final sampling choice is
made by enabling this prototype option.

For an automated estimate with explicit country and date filters,
[Appfigures' estimates API](https://docs.appfigures.com/api/reference/v2/estimates)
supports `countries`, `start_date` and `end_date`, with access on select plans.
Its [free tier announcement](https://news.appfigures.com/free-revenue-download-estimates-for-millions-of-apps-278725)
describes worldwide last-month snapshots, not free German cumulative counts.
Apple's [Analytics Reports API](https://developer.apple.com/documentation/appstoreconnectapi/downloading-analytics-reports)
provides reports for apps accessible through a developer account and requires
an appropriate API-key role; it is not a public competitor-download lookup.

## All known App Store interfaces (checked 22 October 2026)

Includes interfaces that `robots.txt` disallows and interfaces open only to the
app's developer. Tested once, at low volume, on Yazio (id 946099227). Ignoring
`robots.txt` is the author's decision; see
[D2](../../00_Admin/Decisions/D02_ranking-and-rating-floor.md) for the inventory of
both stores and the conclusion.

| Interface | Data | Regional | robots.txt | Result |
|---|---|---|---|---|
| Search API `itunes.apple.com/search` | rating count and average, both also for the current version; result order | storefront | disallowed (`/search*`) | works; used by v001–v006 |
| Lookup API `itunes.apple.com/lookup?id=…&country=…` | same fields for known IDs | storefront | allowed without a country path segment | works |
| Product page `apps.apple.com/<cc>/app/id…` | rating count, average, 1–5★ histogram (`ratingCounts`), chart-position badge, a few review texts; schema.org `reviewCount` equals the rating count | storefront | allowed | works; repeated requests returned HTTP 429 |
| Category chart page `apps.apple.com/<cc>/iphone/charts/6013?chart=top-free` | top 50 Health & Fitness, rank only | storefront | allowed | works |
| Old RSS chart `itunes.apple.com/<cc>/rss/topfreeapplications/limit=200/genre=6013/json` | top 100 by category, rank only | storefront | disallowed (`/*/rss/*`) | works |
| Old RSS reviews `itunes.apple.com/<cc>/rss/customerreviews/page=N/id=…/sortBy=mostRecent/json` | 50 reviews per page, pages 1–10: title, text, stars, version, votes, date | per storefront URL | disallowed (`/*/rss/*`) | works; no total count |
| RSS v2 `rss.marketingtools.apple.com/api/v2/<cc>/apps/top-free/N/apps.json` | overall top free and paid apps, rank only | storefront | no rules | works; no category filter found |
| Web-store API `amp-api.apps.apple.com` | rating data and paged reviews | storefront | — | not reached: no access token found |
| App Store Connect Analytics (developer only) | total, first-time and redownloads by territory; ratings and reviews per country | storefront | — | needs the app's own account |

None of these gives a public download count or a total of written reviews. The
collectors record only the Search API fields; the product-page histogram and chart
badge would need a separate capture.
