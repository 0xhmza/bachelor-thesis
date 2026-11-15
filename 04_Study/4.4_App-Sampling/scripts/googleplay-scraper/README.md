# Google Play sampling collector

Reads Google Play directly with the pinned open-source `google-play-scraper`
parser (1.2.7); no commercial estimates, no authenticated Developer API. Versions
live in `vNNN/`; outputs stay in the version's `output/` folder. Setup from the
repository root:

```powershell
python -m venv 04_Study/4.4_App-Sampling/scripts/googleplay-scraper/.venv
04_Study/4.4_App-Sampling/scripts/googleplay-scraper/.venv/Scripts/python.exe -m pip install -r 04_Study/4.4_App-Sampling/scripts/googleplay-scraper/v005/requirements.txt
04_Study/4.4_App-Sampling/scripts/googleplay-scraper/.venv/Scripts/python.exe 04_Study/4.4_App-Sampling/scripts/googleplay-scraper/v005/scraper.py 04_Study/4.4_App-Sampling/scripts/googleplay-scraper/v005/input.json > 04_Study/4.4_App-Sampling/scripts/googleplay-scraper/v005/output/run.json
```

| Version | What it is |
|---|---|
| `v001/` | Command-line collector (`fitness --region de --limit 20`; defaults region `de`, language `en`, limit 200); writes `googleplay-scraper-<region>-<keywords>-<UTC timestamp>.json` |
| `v002/` | Shortest version: JSON input with `keywords` and/or `ids` (product-page lookup without a search), `region`, `language`, `limit`; JSON on stdout, failures under `errors`. ID mode tested 22 October 2026; keyword mode ran the 19-keyword pilot of 22 October (D2) at the author's direction, although `robots.txt` disallows `/store/search` |
| `v003/` | Sampling collector of 23 October 2026 (D2, D3): adds developer ID, genre ID, minimum installs, histogram, in-app purchase and content-rating fields, summary and full description; keeps the whole first search page. Its `hits_without_id` were the highlighted top results, whose ID the parser misses (for `running`: adidas Running), so it dropped each query's top result. Its run of 23 October took about 5 s per product page and was stopped after 2 h 50 min without output |
| `v005/` | **Shortened collector, shown in Appendix E** (26 October 2026; 88 lines instead of 145). Opens the product page of every app within `depth` (no install-band order, `pages` limit, `search_from` or cutoff fields) and prints no progress. Gives the same `results` as v004's sample run: replaying v004's search hits and page cache through v005 without network calls reproduced all 1,139 result rows of `run-2026-10-25-all.json` |
| `v004/` | **Sampling collector of 24–25 October 2026** (D2); its output is frozen in `05_Data/raw/app-sample_2026-10-25/`. Reads the search page for every keyword and records each hit's position, title, developer and install band, taking a top result's ID from its details URL; ranks the distinct apps by band (ties: best position, package ID); opens the first `pages` product pages, appending each to the `cache` file so an interrupted run resumes; `search_from` reuses an earlier search. Adds `search`, `distinct_apps`, `page_band_cutoff` and `apps_at_cutoff_without_page`. The run of 24 October opened 100 pages; the run completed on 25 October (`pages` 1000, search of 24 October) opened all 645, used by `app-ranking/v003` |

All versions restore the TLS certificate verification the library disables on
import, use 30-second timeouts and one-second pacing, and reject requests or
redirects that drop the storefront parameter, so no result silently comes from
another country.

## Recorded data

App Name, package ID, genres, developer identity, release/update/version, install
band, numeric install lower bound, embedded install count, average rating, rating
and review counts, histogram, prices, free/IAP/advertising flags, content rating,
listing text, screenshots, videos, embedded review snippets (not a review corpus)
and Google, developer and policy links. Parser fallback values are disabled, so a
failed extraction does not invent zeros, empty lists or a version; missing fields
are omitted, observed zeros kept. Each app keeps its `Search Position` in the
returned order; repeated apps stay under each keyword; details are fetched once per
package; failed details keep the hit and are listed in `detail_errors`. Request
metadata: times, requested and final URLs, status, response hashes. A small local
search adapter handles missing top-result sections, which break the upstream search
function on current pages. One search response is read, without pagination; the
merged order is not verified as the native store rank and does not mark ads.

## What the fields mean (checked 22 and 25 October 2026)

| Field | Basis | Evidence |
|---|---|---|
| `Rating Count` | worldwide; labelled "reviews" on the page | identical for `gl=de`, `us`, `gb` (5 apps, one session) |
| `Downloads`, `Minimum Installs`, `Embedded Install Count` | worldwide band, its lower bound, and an undocumented integer (`realInstalls`) | identical across storefronts |
| `Average Rating` | country | MyFitnessPal 3.94 DE, 4.41 US |
| `histogram` | the country's distribution scaled to the worldwide count | MyFitnessPal one-star 428,497 DE, 205,443 US; bins sum to the worldwide count. An earlier note here wrongly called it worldwide |
| `Review Count` | country (`gl`), not language (`hl`); not displayed; undocumented | 22 October: MyFitnessPal 32,560 DE, 454,136 US, 89,533 GB. 25 October: 32,562 DE, 2,887 AT, 454,109 US, unchanged between `hl=de` and `hl=en`. The German measure of the ranking since 25 October |

The page's JSON-LD `aggregateRating` pairs the country average with the worldwide
count; a chart badge for the storefront (e.g. "#2 top grossing health & fitness",
US) is shown but not recorded. Google announced country-specific phone ratings
from November 2021 ([Android Developers Blog](https://android-developers.googleblog.com/2021/08/making-ratings-and-reviews-better-for.html));
country installs go to the developer only ([Play Console help](https://support.google.com/googleplay/android-developer/answer/139628)).
Field mappings: the library's [search](https://github.com/JoMingyu/google-play-scraper/blob/ce1df6d67e6d8c39826daac2f668808fc025f284/google_play_scraper/features/search.py)
and [element](https://github.com/JoMingyu/google-play-scraper/blob/ce1df6d67e6d8c39826daac2f668808fc025f284/google_play_scraper/constants/element.py)
code; positional parsers break when Google changes its pages. All known Play
interfaces, with robots rules, are listed in
[D2](../../../../00_Notes/Decisions/D02_ranking-and-rating-floor.md).
