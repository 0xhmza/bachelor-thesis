# Google Play sampling collector

`v001/scraper.py` is the Google Play counterpart of the Apple collector. It reads
Google Play directly using the pinned open-source `google-play-scraper` parser;
it does not use commercial estimates or the authenticated Developer API.

The project has an isolated environment at `.venv/`. Setup from the repository root:

```powershell
python -m venv scripts/googleplay-scraper/.venv
scripts/googleplay-scraper/.venv/Scripts/python.exe -m pip install -r scripts/googleplay-scraper/v001/requirements.txt
scripts/googleplay-scraper/.venv/Scripts/python.exe scripts/googleplay-scraper/v001/scraper.py fitness --region de --limit 20
scripts/googleplay-scraper/.venv/Scripts/python.exe scripts/googleplay-scraper/v001/scraper.py fitness "sleep tracker" -r de -n 20 -l en
```

Defaults: region `de`, language `en`, requested limit 200. Prints the JSON path in
`v001/output/`, named `googleplay-scraper-<region>-<keywords>-<UTC timestamp>.json`.
Create future versions as `v002/`, etc., preserving prior sources.

`v002/scraper.py` is the shortest working version, shown in Appendix E of the
thesis. Input is a JSON file with `keywords` and/or `ids` (package IDs looked up
on the product page without a search), `region`, `language` and `limit`. Output is
JSON on stdout, with failed lookups under `errors`. It keeps the v001 safeguards
(TLS verification restored, storefront parameter enforced, no country fallback)
but records fewer fields. Run it with the environment above, after creating
`v002/output/`:
`scripts/googleplay-scraper/.venv/Scripts/python.exe scripts/googleplay-scraper/v002/scraper.py scripts/googleplay-scraper/v002/input.json > scripts/googleplay-scraper/v002/output/run.json`.
The ID mode was tested live on 22 October 2026. The keyword mode reuses the v001
search adapter unchanged and was not run again, because `robots.txt` disallows the
`/store/search` path (see the [mechanism note](../../output/research/2026-10-11_scraper-mechanism/research-note.md)).

## Recorded data

App Name first, package ID, genres, developer identity, release/update/version,
displayed install band, numeric install lower bound, raw embedded install count,
average rating, rating/review counts, rating histogram, prices, free/IAP/advertising
flags, age/content advisories, listing text, screenshots, videos, embedded review
snippets and Google/developer/policy links. Missing fields are omitted; observed
zeros are retained. Parser fallback values are disabled so a failed extraction
does not invent zero ratings, empty screenshots, false flags or a version string.
Developer type and historical 2023 counts are not supplied by this parser and
are omitted. Embedded review snippets, when available, are not a review corpus.

Each app retains its original `Search Position` in the parser's returned web-search
order. Repeated apps remain under each keyword, and details are fetched once per
distinct package. Failed details retain the search candidate and position, with
the failure recorded in `detail_errors`. HTTP request metadata includes timestamps,
requested/final URLs, status and response hashes. No eligibility or ranking score
is imposed. Empty search results or fewer results than requested are not proof
of exhaustive coverage; this parser reads one search response, without pagination.
Its merged top-result/ordinary-result ordering is not verified native Android
store rank and does not label advertisements versus organic entries.
A small local search adapter handles missing/null top-result sections, which
otherwise cause the pinned upstream search function to fail on current pages.
It keeps the upstream field mappings and stops after the first ordinary grid.

## Which fields change with the storefront (checked 22 October 2026)

Product-page requests for the same app with `gl=de`, `us` and `gb` (5 apps, one
session) returned identical `Rating Count` and install figures (`Downloads`,
`Minimum Installs`, `Embedded Install Count`). `Average Rating` and `Review Count`
differed, for example MyFitnessPal reviews 32,560 (DE), 454,136 (US) and 89,533
(GB). `Review Count` is not displayed on the page and its meaning is undocumented.

**Correction.** The rating histogram (`histogram`, recorded by v001 as `Rating
Distribution`) is **not** worldwide, although an earlier note here said so. Its
bins differ by country (MyFitnessPal one-star: 428,497 in DE, 205,443 in US), their
weighted mean equals the country's `Average Rating`, and they sum to the worldwide
`Rating Count`. It is the country's distribution scaled to the worldwide total. The
first check compared only the sums.

The page labels the worldwide rating count "reviews" (for example "2.92M
reviews"), and its JSON-LD `aggregateRating` pairs the country average with the
worldwide count. A product page also shows a chart badge for the storefront when
the app is ranked (for example "#2 top grossing health & fitness" in the US), which
this collector does not record.

Setting `--region de` therefore does **not** make `Rating Count` or `Embedded
Install Count` German, and no parameter in this collector changes that. The only
other source, the reviews RPC endpoint, is under a path that `robots.txt`
disallows, as are `/store/search` and `/store/getreviews`. Google announced
country-specific phone ratings from November 2021
([Android Developers Blog](https://android-developers.googleblog.com/2021/08/making-ratings-and-reviews-better-for.html)),
and country install figures are shown only to the developer
([Play Console help](https://support.google.com/googleplay/android-developer/answer/139628)).
Treat `Rating Count` as worldwide, `Average Rating` and the histogram's shape as
country-specific, and `Review Count` as country-specific but undocumented and
unvalidated as an exposure measure. See
[D2](../../00_Admin/Decisions/D02_ranking-and-rating-floor.md) for how this enters
the ranking.

## Metric and transport limits

`Downloads` is Google's displayed install band (for example `100,000,000+`),
not a precise download count. `Minimum Installs` is its lower bound.
`Embedded Install Count` is the field the library calls `realInstalls`: a number
copied from Google's page data, not a third-party estimate. Its counting definition
and update cadence are not established here, so it is not labeled exact downloads,
users or German installs. Region is storefront context; rating/review/install
fields must not be assumed to describe identical geographic populations. Review
Count is the returned listing aggregate, not a preceding-12-month review count.

The library's [search implementation](https://github.com/JoMingyu/google-play-scraper/blob/ce1df6d67e6d8c39826daac2f668808fc025f284/google_play_scraper/features/search.py)
and [field mappings](https://github.com/JoMingyu/google-play-scraper/blob/ce1df6d67e6d8c39826daac2f668808fc025f284/google_play_scraper/constants/element.py)
explain these extraction routes. The prior [project audit](../../output/research/2026-10-11_scraper-mechanism/research-note.md)
documents their limitations. This script restores the TLS factory after importing
the library and replaces its GET transport with certificate-verified requests,
30-second timeouts and one-second pacing. Country-removing fallbacks and unexpected
country/host redirects are rejected. Version-specific positional parsers can break
when Google changes its pages; successful extraction is not independent validation
of each metric's meaning or the app's eligibility in a final study.

## All known Google Play interfaces (checked 22 October 2026)

Includes interfaces that `robots.txt` disallows and interfaces open only to the
app's developer. Tested once, at low volume, on MyFitnessPal
(`com.myfitnesspal.android`). Ignoring `robots.txt` is the author's decision; see
[D2](../../00_Admin/Decisions/D02_ranking-and-rating-floor.md) for the inventory of
both stores and the conclusion.

| Interface | Data | Regional | robots.txt | Result |
|---|---|---|---|---|
| Product page `/store/apps/details?id=…&gl=…` (library `app()`) | rating count (worldwide), average (country), 1–5★ histogram (country shape scaled to the worldwide total), undocumented review count (country, not displayed), install band and exact integer (worldwide), chart badge when ranked (country) | mixed | allowed | works; used by v001 and v002 |
| Search page `/store/search` | result order | storefront | disallowed | works; used by v001 and v002 keyword mode |
| Reviews RPC `/_/PlayStoreUi/data/batchexecute` (library `reviews()`) | review text, stars, app version, thumbs-up count, developer reply; paged | **by language, not country**: `lang=de` gave the same 50 newest reviews for DE and US | disallowed (`/_`) | works; no total count |
| Data safety page `/store/apps/datasafety?id=…` | data collected and shared, security practices | — | disallowed | works (HTTP 200) |
| Permissions RPC (library `permissions()`) | permission groups | — | disallowed (`/_`) | works |
| Category page `/store/apps/category/HEALTH_AND_FITNESS` | short ranked carousels, not a full chart | country | allowed | works |
| Top-charts RPC (Node library `list()`) | full category charts per country | country | disallowed (`/_`) | untested; not in the Python library 1.2.7 |
| Play Console (developer only) | installs and uninstalls by country; all reviews | country | — | needs the app's own account |

None of these gives a public German install count or a total of written reviews.
