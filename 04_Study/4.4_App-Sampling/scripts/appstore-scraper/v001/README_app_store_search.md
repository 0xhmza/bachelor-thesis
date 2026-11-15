# iPhone App Store keyword collector

Search a keyword, retain every returned API field, and enrich each confirmed
iPhone-compatible app from its public App Store product page. Python 3.10 or newer;
standard library only, no API key or package installation.

From the repository root:

```powershell
python 04_Study/4.4_App-Sampling/scripts/appstore-scraper/v001/app_store_search.py fitness -o 05_Data/raw/appstore/fitness.json --raw-dir 05_Data/raw/appstore/fitness-responses
```

The defaults are Germany (`--country de`), English requested, up to 200 API
results, and product-page enrichment. Choose new output/archive names for each
run: existing snapshots are protected against overwriting. Raw study data under
`05_Data/raw/` is ignored by Git; preserve it in the project's data backup.

Other examples:

```powershell
python 04_Study/4.4_App-Sampling/scripts/appstore-scraper/v001/app_store_search.py "sleep tracker" --country de --limit 20 -o 05_Data/raw/appstore/sleep.json
python 04_Study/4.4_App-Sampling/scripts/appstore-scraper/v001/app_store_search.py fitness --api-only --limit 20
python 04_Study/4.4_App-Sampling/scripts/appstore-scraper/v001/app_store_search.py --reparse 05_Data/raw/appstore/fitness.json -o 05_Data/raw/appstore/fitness-reparsed.json
```

Without `-o`, the script prints JSON to stdout; progress goes to stderr. Python
callers can import `collect` from `app_store_search` with `v001/` on the Python import path and receive a dict.
`--api-only` skips product pages. `--raw-dir` saves the exact response bodies and
HTTP metadata, including attempts, dates, URLs and SHA-256 hashes. With `-o`, the
JSON is checkpointed as pages finish. `--reparse` verifies archived page hashes
and rebuilds page fields offline, recording the source JSON and parser hashes.
It can also recover an interrupted checkpoint if every pending app's response
was archived successfully. Atomic checkpoint saves retry transient Windows locks.
Archive paths in the JSON are absolute; update them explicitly if moving data.

Exit codes: `0` completed, `1` collection/input failure, `2` saved results with
one or more product-page errors. A failed page leaves the app and API fields
in the JSON. `collecting` means an interrupted checkpoint rather than a final run.

## Data available per app

| JSON field | Contents |
|---|---|
| `api_result_position`, `app_id`, `bundle_id` | Original API position and stable listing identifiers |
| `name`, `developer`, `seller`, developer/store URLs | Identity and provider information |
| `description`, `genres`, language and age fields | Listing text and classification |
| Price, currency, `free_to_download` | Download price; a free download can still require payment inside the app |
| Rating fields | API average/count and current-version fields as returned; no independent validation of their scope |
| Version, release dates, release notes | API version metadata |
| Device support, minimum iOS, file size | Compatibility and binary metadata |
| Screenshots and artwork | URLs; media files are not downloaded |
| `raw_api_data` | Every field returned by Apple, including future/unknown fields |
| `app_store.offer`, `subtitle` | Public page offer flags and subtitle |
| `app_store.privacy_policy_urls`, `external_links` | Links extracted from primary-app page actions; linked websites/policies are not fetched |
| `app_store.privacy_summary`, `privacy_details` | Developer-declared privacy labels, purposes, categories and data types where embedded |
| `app_store.in_app_purchases` | Displayed purchase/subscription titles and localized prices where embedded |
| `app_store.version_history`, `latest_update` | Embedded release history and latest update |
| `app_store.information` | Compatibility, languages, copyright and public provider/trader details where shown |
| `app_store.ratings`, `displayed_reviews` | Page ratings and embedded reviews; not an exhaustive review export |
| `app_store.structured_data`, `product_page_data` | JSON-LD and primary product-page content, including accessibility, screenshots and other available shelves |
| `app_store.source`, `collection.source` | Request/response provenance, hashes and archive locations |

`product_page_data` omits analytics/metrics and related-app recommendation
shelves; raw archived HTML preserves the original page. Some normalized page
fields duplicate parts of this data for convenient access. Missing values are
`null` or empty lists, and page extraction failures have explicit error status.
The script does not invent download counts or infer eligibility from descriptions.

## Interpretation for sampling

The source is Apple's [public iTunes Search API](https://performance-partners.apple.com/search-api)
with `media=software`, `entity=software`, `country=de`, `lang=en_us`, and
`explicit=Yes`. The [overview](https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/index.html)
identifies App Store search as a supported use. Apple documents `limit` as 1–200
and approximately 20 API calls/minute; the client spaces API requests by 3.2
seconds and page requests by one second across workers. It retries transient
HTTP/network failures, honors Retry-After up to 60 seconds and reports longer
server-requested waits. These are collection settings, not sample-size choices.

There is no documented pagination parameter here; a result below the requested
limit is not evidence of complete keyword coverage. The response may vary over
time. `api_result_position` describes returned order, not verified native iPhone
App Store search rank, German popularity, or downloads. The script preserves
order, does not sort by ratings, and records the requested versus actual count.

The returned `supportedDevices` must explicitly include an iPhone. iPad-only,
unknown compatibility, invalid records and duplicate IDs go into
`excluded_results`, with original positions and full API records. These technical
exclusions do not apply thesis eligibility rules. Paid apps, native apps and
apps without an extracted policy link remain candidates.

Product pages must retain both the requested country and app identity, verified
against the final URL, canonical URL when present and embedded page intent.
There is no silent switch to another country's storefront. English is requested;
actual HTML language is recorded, and provider text can still use another language.
The observed page implementation redirects `l=en` to `l=en-GB` for Germany.

The product-page parser reads embedded `serialized-server-data`. This page
structure is not a versioned public API and may change; errors remain explicit,
and archived HTML enables later reprocessing. No downloaded app, account,
device interaction, permission inspection, or full review history is involved.
A missing policy link means only that this parser did not find one in supported
fields. Privacy disclosures are declarations, not independently tested behavior.

This collector implements the user's 20 October 2026 request to start with
`fitness`. It does not freeze a thesis sample, choose a rating floor, replace
native store search capture, or resolve the open sampling decisions in the
[decision log](../../../../../00_Admin/Decision-Log.md).

## Verification

```powershell
python -m unittest discover -s 04_Study/4.4_App-Sampling/scripts/appstore-scraper/v001/tests -p test_app_store_search.py -v
python scripts/check_project.py
```

Offline checks cover identity/storefront mismatches, unknown fields and missing
values, iPhone filtering, API order, purchase/privacy/history extraction, page
failures without candidate loss, HTTP retries, Windows file locks, checkpoint
recovery, and hash-verified offline reprocessing.
