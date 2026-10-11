# How the Google Play scraper retrieves data

Research date: **11 October 2026**, Europe/Berlin.

**Finding:** the Python `JoMingyu/google-play-scraper` uses a hybrid mechanism. App details and keyword search results are extracted from structured data embedded in an HTML response. Reviews and permissions are retrieved through an undocumented Google Play web RPC endpoint. Neither route uses the authenticated Google Play Developer API.

## Scope and reproducibility

The principal audit examined Python release **1.2.7**, Git commit `ce1df6d67e6d8c39826daac2f668808fc025f284`. PyPI's metadata reported this as the latest release during this check, uploaded on 7 June 2024. The downloaded wheel was checked against its published SHA-256, `a485510b09265f0096fc3813cfc26eef27e9a5c0035f99ee23f80e00de724530`. Seven relevant modules matched the checkout after normalising Windows line endings. The initial byte comparisons differed solely because of those line endings. [PyPI release](https://pypi.org/project/google-play-scraper/1.2.7/).

For comparison, the Node implementation was inspected at commit `ed4df8c3eb261542f62eed1fd148ea8634208be8` (package file: 10.1.3). It is a separate project with separate release history. [Pinned Node source](https://github.com/facundoolano/google-play-scraper/tree/ed4df8c3eb261542f62eed1fd148ea8634208be8).

Validation consisted of source inspection, offline checks with artificial responses, and two live HTTP GETs for Clue's product page, using the same German language with DE and US country parameters. This is a mechanism demonstration, not the thesis sample or a validation against developer analytics. Search and review RPC requests were not executed; their mechanisms were traced in source.

## Request routes

| Python function | HTTP request | Returned data | Extraction route |
|---|---|---|---|
| `app()` | GET `/store/apps/details?id=…&hl=…&gl=…` | HTML including embedded initialisation data | Regex extraction, JSON decoding, positional mappings |
| `search()` | GET `/store/search?q=…&c=apps&hl=…&gl=…` | HTML including search datasets | Same embedded-data extraction; returns part of one response |
| `reviews()` / `reviews_all()` | POST `/_/PlayStoreUi/data/batchexecute?hl=…&gl=…` | Framed RPC response containing nested JSON | RPC method `oCPfdb`, nested decoding, continuation tokens |
| `permissions()` | POST to the same RPC endpoint | Nested permission data | RPC method `xdSrCf`, nested decoding and grouping |

The URL formats and form-body templates are explicit in [the pinned request constants](https://github.com/JoMingyu/google-play-scraper/blob/ce1df6d67e6d8c39826daac2f668808fc025f284/google_play_scraper/constants/request.py). The Python project exports those functions; its README phrase “provides APIs” refers to its own callable library interface, not a claim that Google offers a supported public market-data API.

The transport uses Python's `urllib.request`. The main paths have no browser engine, Selenium, JavaScript runtime, OAuth setup or developer API credentials. These facts describe the audited implementation, not a guarantee that Google will continue accepting every request. [Transport source](https://github.com/JoMingyu/google-play-scraper/blob/ce1df6d67e6d8c39826daac2f668808fc025f284/google_play_scraper/utils/request.py).

## App details: HTML contains the data

After downloading a product page, `app()` passes the response text to `parse_dom()`. It gathers script fragments containing `AF_initDataCallback`, associates each fragment with a dataset key, and decodes its `data` array. The HTML page therefore acts as the carrier of the data. The scraper is not selecting visible rating labels with CSS selectors, executing scripts, or contacting a separate statistics endpoint for the install number. [App implementation](https://github.com/JoMingyu/google-play-scraper/blob/ce1df6d67e6d8c39826daac2f668808fc025f284/google_play_scraper/features/app.py), [regex definitions](https://github.com/JoMingyu/google-play-scraper/blob/ce1df6d67e6d8c39826daac2f668808fc025f284/google_play_scraper/constants/regex.py).

The field mapper uses fixed numeric positions in the decoded arrays. For example, the three install fields use the same installation block:

| Output name | Source path |
|---|---|
| `installs` | `dataset['ds:5'][1][2][13][0]` |
| `minInstalls` | `dataset['ds:5'][1][2][13][1]` |
| `realInstalls` | `dataset['ds:5'][1][2][13][2]` |

Those names are assigned by the library. The extraction of `realInstalls` has no statistical estimator or extrapolation step. It copies the value at that position. That proves provenance of the number, not its metric definition. [Field mappings](https://github.com/JoMingyu/google-play-scraper/blob/ce1df6d67e6d8c39826daac2f668808fc025f284/google_play_scraper/constants/element.py).

## Live evidence: Clue

The two pages were captured on 11 October 2026 at approximately **15:22 Europe/Berlin**, with no signed-in account, no cookie reuse, an explicit user agent and verified HTTPS. The request language was `hl=de` in both cases.

| Extracted field | `gl=de` | `gl=us` |
|---|---:|---:|
| Displayed install band | `50.000.000+` | `50.000.000+` |
| Numeric lower bound | 50,000,000 | 50,000,000 |
| Value returned as `realInstalls` | 70,425,176 | 70,425,176 |
| Rating | 4.248807 | 4.4884133 |
| Rating count | 1,501,038 | 1,501,038 |
| Review count | 10,118 | 32,947 |
| Version field | `Varies with device` | `272.0` |

In each saved response, the installation block was `['50.000.000+', 50000000, 70425176, '50 Mio.+']` (the final label contains a non-breaking space). The raw number matched the parser output exactly. These are observed snapshot values, not forecasts or claims about Clue's current active audience.

**Inference:** the unchanged install value across countries supports treating the country parameter as storefront context rather than a geographic filter for installs. Two requests for one app do not establish universal field semantics. The differing ratings and review counts also show why researchers should not assume all extracted numbers describe the same geographic or linguistic population.

Raw pages and metadata are retained under `05_Data/raw/2026-10-11_scraper-research/20261011T132202417187Z/`. The corresponding `mechanism_check.json` contains the URLs, timestamps, hashes, arrays and parsed fields. This raw folder is gitignored and needs separate backup.

## Reviews: an internal API-like interface

The review code submits a form containing `f.req`, which encodes an RPC envelope. Within it are the RPC identifier, another serialised JSON value, and request options such as app ID, sort, count, filters and continuation token. Google returns a prefixed response whose outer layer is decoded before the nested payload is decoded again. The prefix is consistent with an anti-XSSI guard; this interpretation is distinct from what the parser itself proves.

Continuation tokens request subsequent batches. `reviews_all()` repeats calls until the token disappears. The source imposes a maximum requested batch of 4,500; this is a client-side setting, not proof of a guaranteed server limit or complete review coverage. [Review implementation](https://github.com/JoMingyu/google-play-scraper/blob/ce1df6d67e6d8c39826daac2f668808fc025f284/google_play_scraper/features/reviews.py).

This endpoint is an API in the technical sense of a callable remote interface. It is an undocumented web UI interface, rather than Google's supported Developer API. The official API has documented setup, OAuth/service accounts and account permissions. [Official API setup](https://developers.google.com/android-publisher/getting_started).

## What the source does not establish

The numeric installation field has no counting definition in the inspected Google documentation. Neither the extraction nor the live comparison establishes whether it counts unique users, devices, repeat installations, preinstalls or another aggregate; its update cadence is also unverified. A Google-origin number can be measured or processed by Google's systems without the scraper explaining that processing.

Consequently, describe it as **a Google Play embedded install-count field, extracted by the library as `realInstalls`**. Do not describe it as verified exact downloads, German users or monthly active users. Different developer-dashboard metrics have different definitions; those definitions cannot simply be attached to an undocumented positional field. [Google's documented dashboard metrics](https://support.google.com/googleplay/android-developer/answer/139628/view-app-statistics-computer?co=GENIE.Platform%3DDesktop&hl=en).

The Node mapper reads the same installation position but names it `maxInstalls`. That naming mismatch is further reason to record the raw path and value. It does not establish that today's value is an interval upper bound. Historical discussion of older visible install ranges should not override the current mapping. [Node app mapper](https://github.com/facundoolano/google-play-scraper/blob/ed4df8c3eb261542f62eed1fd148ea8634208be8/lib/app.js).

## Reliability findings affecting a study

Offline checks reproduced a country-specific 404 followed by a successful retry with `gl` removed. The app result exposes the fallback URL, but no exception warns that country context changed. The same retry policy exists for search. A German-storefront collector should reject or explicitly flag this fallback rather than treating success as evidence of German availability.

Python search extracts a special top result and an ordinary result section, then limits the returned list. It does not implement continuation-token paging. `n_hits` is therefore a cap, not a guarantee of a complete search or of the exact first N cards seen in a phone interface. It also lacks an explicit sponsored/organic classification in its result mappings. [Search implementation](https://github.com/JoMingyu/google-play-scraper/blob/ce1df6d67e6d8c39826daac2f668808fc025f284/google_play_scraper/features/search.py).

The offline failure check showed that a review transport exception is caught and converted to an empty result with no continuation token. Likewise, absent embedded datasets produce missing fields and some default values. A successful function return cannot by itself establish collection completeness. Preserve an explicit distinction between observed absence and retrieval/parser failure.

Finally, the Python transport globally replaces the default HTTPS context with an unverified context at import time. That is a concrete source-authenticity problem for research. The check script restores certificate verification immediately after import and uses an explicit verified context for live downloads. A production collector should repair that behavior rather than inherit it. The audited transport also lacks an explicit request timeout.

These findings justify preserving raw responses, checking expected field types and ranges, rejecting unexpected layouts, and recording errors separately. Fixed positional mappings can fail after a layout change, including returning plausible values from an unintended position.

## Access conditions found during the check

The retrieved `robots.txt` does not disallow the app-details path for the generic crawler group, but explicitly disallows `/store/search` and `/_`, covering the search and RPC routes described above. Google's general terms address automated access contrary to machine-readable instructions. This is an operational finding about current access instructions, not a legal determination about every research use. It does not establish blanket permission to reuse all page content. [Robots instructions](https://play.google.com/robots.txt), [Google terms](https://policies.google.com/terms?hl=en), [Play terms](https://play.google.com/intl/en_us/about/play-terms/index.html).

Accordingly, the live check was restricted to product-page GETs. A study cannot infer permission for automated keyword searches or bulk reviews merely from the library's MIT license. The project protocol already requires checking store terms before automated collection.

## Implication for the thesis

The scraper can support a free, traceable snapshot of app metadata and a more granular install field than the visible band. It does not resolve the need for German usage data or provide comparable iOS install data.

A defensible Android sampling measure could use the embedded install field as a declared proxy for reach, retaining the visible band alongside it and checking whether selections change under a band-based ranking. Such a design still needs a separately documented candidate discovery method and revised eligibility/tie rules before freezing the sample. The existing proposal has not been changed by this research.

For every captured listing retain package ID, requested and final URL, `hl`/`gl`, retrieval timestamp/timezone, HTTP status, response hash, library version/commit, raw field path and value, visible band, and collection/error status. Generate rankings from frozen captures so they can be reproduced offline.

## Local verification

`check_mechanism.py` contains the mechanism checks. Its default run is offline; `--live-listings` additionally checks robots and retrieves two product pages. All captures use unique directories and exclusive file creation. The script is a research demonstration, not a ready-made sampling tool.

Completed checks: synthetic embedded-data extraction; country fallback; missing dataset defaults; RPC payload decoding; review failure behavior; two live listing captures; published wheel SHA-256; and normalised wheel/source comparisons. Live review pagination, phone-interface search order, actual install-count accuracy and cross-app coverage remain unverified.
