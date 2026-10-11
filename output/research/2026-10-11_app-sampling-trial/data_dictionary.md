# Data dictionary and decision rules

## Identity and observation

| Field | Meaning |
|---|---|
| `listing_id` | `apple:<trackId>` or `play:<packageId>`; store-specific observation unit. |
| `app_id` | Canonical study product identifier. Seven groups have provisional cross-store matches. Other IDs inherit a listing ID and are not proof of single-platform availability. |
| `captured_utc` | Request-start time in UTC, retained in a response sidecar and listing row. |
| `source_sha256` | SHA-256 of exact source-response bytes; no HTML normalization. |
| `raw_file` | Filename relative to the run's raw directory. |
| `source_rank` | Position in the Apple API response. Never interpret as native-store UI rank. |
| `store_ui_rank` | Empty until the actual prescribed store search is captured. |
| `domain_hint` | Keyword/discovery context; not a reviewed classification. |
| `domain_provisional` | Heuristic classification, with explicit overrides in the review file. |

## Ranking inputs

| Field | Source and interpretation |
|---|---|
| `rating` | Apple `averageUserRating`, or Play `ds:5[1][2][51][0][1]`. Store-reported average; stores have different rating systems. |
| `rating_count` | Apple `userRatingCount`, or Play `ds:5[1][2][51][2][1]`. Used for threshold and weighting; not written review count. |
| `written_review_count` | Play `ds:5[1][2][51][3][1]`; separate from ratings. Not needed for proposal ranking. |
| `weighted_score` | Sum(rating × rating_count) / sum(rating_count), using numerically passing listings assigned to the app. Decimal arithmetic; descending. |
| `eligible_rating_count` | Sum over the same numerically passing listings; secondary sort key. The label concerns numeric screening only in the working set. |
| `ranking_listing_ids` | Listings contributing to the trial score. All captured counterparts remain in `listing_ids`. |
| `domain_rank` | Within-domain position in the provisional or final set, identified by `status`. |

The exact final tie uses canonical ID ascending. This is an operational trial
choice, since the proposal does not specify ties after rating and rating count.
Displayed report scores round to four decimals; sorting uses the unrounded
Decimal value. The weighted score follows the proposal but does not establish
that Apple and Google averages measure an identical rating population.

## Install counts

| Field | Meaning and limitation |
|---|---|
| `installs_label` | Play's formatted band, for example `50.000.000+`. |
| `minInstalls` | Numerical lower bound accompanying that label. |
| `realInstalls` | Play embedded integer at `ds:5[1][2][13][2]`. The library-style name is preserved for traceability. Google counting semantics are not documented here. |
| `install_proxy_rank` | Descending embedded count among the Play listings passing the trial's numerical screen. It has a different denominator from the 50-app working set. |

Country parameter `gl=de` sets listing context; it does not turn `realInstalls`
into German downloads. Do not equate this field with exact people, active
users, current impact, or a country/time-specific acquisition count. No
corresponding Apple download count is inferred, and missing values are never
filled with zero. Counts across stores are not summed as distinct users.

## Screening

`E01`: fewer than 1,000 ratings on that listing. `E02`: paid installation.
`E03`: Apple language metadata explicitly lists neither German nor English.
Several codes may apply to one listing; reason totals are nonexclusive.
Numeric exclusion of one listing does not automatically exclude the product
if another eligible listing exists. A missing field is pending, not zero.

`passes_numeric` means sufficient rating data and free installation survived
the automated screen. It does not establish the remaining inclusion rules.
Human/evidence checks are `tracking_function`, `free_install`, `interface_DE_EN`,
`policy_reachable`, `not_DiGA`, `not_duplicate`, `German_available`,
`store_UI_membership`, and `identity_verified`. All must be explicitly true
with evidence, and the overall discovery frame must be complete, before a
row can enter the final set. `pending_checks` lists missing affirmative checks;
a false check must be interpreted using the recorded decision reason.

A translated store description is not evidence of the app's interface
language. A successful Play product-page request is not proof that a German
device can install the app. A policy URL is not proof of policy reachability,
and a returned HTTP 200 may still be a consent page, error template or empty
JavaScript shell. Automated policy retrieval failures need verification before
an app is excluded for an unreachable policy.

Descriptions contain developer claims. They support preliminary feature
screening, not validation of clinical accuracy, effectiveness or privacy.
