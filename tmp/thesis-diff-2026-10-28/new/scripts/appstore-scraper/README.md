# App Store scraper

Versions live in `vNNN/`; outputs stay in the version's `output/` folder.

| Version | What it is |
|---|---|
| `v001/` | Full collector with product-page enrichment (privacy labels, purchases, version history) and tests; see its [README](v001/README_app_store_search.md) |
| `v002/` | Minimal standard-library collector; all API fields for iPhone-compatible apps, up to 200 results per keyword, English requested |
| `v003/` | Selected fields in a fixed order; unavailable fields (Dev. Type, Downloads, Reviews, Reviews (2023)) kept as `null` |
| `v004/` | As v003 without the unavailable fields (`Average Rating` for the score); optional `--downloads` adds Sensor Tower estimate ranges |
| `v005/` | Compact collector for sampling metadata: original `API Position` (before iPhone filtering) and per-keyword request URL, time and count |
| `v006/` | Shortest version: JSON input, JSON on stdout, fewer fields; `Rating Count` names as in v005 |
| `v007/` | **Sampling collector of 23 October 2026** (D2, D3), shown in Appendix E: v006 plus developer ID, seller, bundle ID, genres, version, content rating, full description and seller URL; logs every request (URL, time, count, SHA-256) under `requests`; backs off on HTTP 403/429/5xx. `input.json` holds the 49 keywords of `04_Study/App-Sample/keywords.csv` with `limit` 200; the ranking uses the first 30 positions, the rest only the saturation check |

```powershell
python scripts/appstore-scraper/v007/scraper.py scripts/appstore-scraper/v007/input.json > scripts/appstore-scraper/v007/output/run.json
```

## What the data means

- Source: Apple's Search API with `country=<region>` (default `de`). Results keep
  API order; repeated apps stay under each keyword. API position is not verified
  as the native iPhone App Store rank, and a limit is a requested cap, not proof
  of complete coverage.
- Rating counts and averages are storefront-specific (checked 22 October 2026, 6
  apps, 3 storefronts, one session). DE / US / GB: Yazio 446,768 / 51,379 / 12,351;
  Google Gemini 270,417 / 2,363,183 / 241,116; MyFitnessPal 80,176 / 2,381,357 /
  474,412. `Rating Count` counts ratings, not written reviews or downloads.
- The API supplies no developer type, downloads, written-review counts or
  historical counts; the product page's histogram (`ratingCounts`) and chart badge
  need a separate capture. Missing fields are omitted, real zeros kept.
- All known App Store interfaces, with robots rules and regional behaviour, are
  listed in [D2](../../00_Admin/Decisions/D02_ranking-and-rating-floor.md); Google
  Play behaves differently ([Play README](../googleplay-scraper/README.md)).

## Download estimates (checked 20 October 2026)

`v004 --downloads` reads Sensor Tower's public overview metadata per app (e.g.
[Home Workout](https://app.sensortower.com/overview/1313192037?country=US):
`100k-500k` for "Last month"; MyFitnessPal `500k-1m`; Apple Fitness `< 5k`) and
keeps the range strings with source URL, time and period under `Estimated
Downloads`; failures go to `estimate_errors`. Requests are 4 s apart; HTTP 429
stops collection (`estimate_collection_stopped`). The first full `fitness` trial
got 15 ranges for 169 apps (154 HTTP 429 errors, before the stop guard). The
estimates are third-party and labelled worldwide; neither `country=US` nor
`--region de` makes them German. [Appfigures' estimates API](https://docs.appfigures.com/api/reference/v2/estimates)
filters by country and date on select plans (its [free tier](https://news.appfigures.com/free-revenue-download-estimates-for-millions-of-apps-278725)
gives worldwide last-month snapshots); Apple's [Analytics Reports API](https://developer.apple.com/documentation/appstoreconnectapi/downloading-analytics-reports)
covers only the developer's own apps.
