# App ranking

Selects the ranked apps of the sample as set out in
[D2](../../00_Admin/Decisions/D02_ranking-and-rating-floor.md). Each version lives in
`vNNN/`; outputs stay in the version's `output/` folder.

- `v001/rank.py`: merges the stores by within-store percentile; replaced, kept for
  the record.
- `v002/rank.py`: selection of 24 October 2026 by store alternation with the worldwide
  Play count; replaced by v003, kept for the comparison.
- `v003/rank.py`: the selection of 25 October 2026 (D2 revision); replaced by v004,
  kept for the record. Its Daylio and MeetYou aliases never matched.
- `v004/rank.py`: the selection of 26 October 2026 on the frozen dataset
  `05_Data/raw/app-sample_2026-10-25/`; provider identity rules P1–P3 (D2).
  Replaced by v005, kept for the record: its title rule paired different
  products of one publisher (peer review F01).
- `v005/rank.py`: the selection of 28 October 2026; the same app in both stores
  only where the identity register says so (D2, rules I1–I5).

## v005

```powershell
python scripts/app-ranking/v005/rank.py scripts/app-ranking/v005/config.json
python -I -m unittest discover -s scripts/app-ranking/v005/tests
```

Changes from v004. The title rule (same provider and a shared first word, the
App Store listing with the most ratings taken first) is gone, and so are the
hand-made `pairs`. A Google Play and an App Store listing are one candidate only
if `04_Study/4.4_App-Sampling/identity.csv` records them as `same`; rating counts and
input order play no part. The script proposes pairs for review in the union of
all frames used (Google Play depth 30, App Store depth 200, all queries): same
developer key, same app identifier (bundle ID = package name), same normalised
title, or at least 20 rare four-word passages of description text. Proposals
without a decision go to `output/identity-review.csv`. Both listings of a
`same` pair belong to one provider (union of their developer keys). An
`unresolved` pair is not merged; every run is repeated with the unresolved
pairs merged, and the run is final only if no selected listing changes. The
register is checked before use: known listings, decisions `same`, `different`
or `unresolved`, evidence codes (`web`, `id`, `name`, `en-name`, `text`,
`listing`) for every `same` pair, rationale, reviewer and date, and no listing
in two `same` pairs; any error stops the run.

When anything is pending (unscreened candidates, provider-review pairs,
undecided proposals, unresolved pairs that change a selection) the script
writes its `output/` files and exits with an error, without writing the thesis
tables or the dataset. `sensitivity.csv` also counts selected listings that
change (`listings_differ`) and changed positions (`order_changes`). New
generated tables: `03_Thesis/tables/identity-providers.tex` (same app under two
developer names) and `03_Thesis/tables/sensitivity.tex`. Inputs and the
dataset are in `05_Data/App Sampling/26. Oct/` (the frozen collections, moved
unchanged). Runs in about ten seconds.

## v004

```powershell
python scripts/app-ranking/v004/rank.py scripts/app-ranking/v004/config.json
python -I -m unittest discover -s scripts/app-ranking/v004/tests
```

Changes from v003, described below: aliases fixed (Daylio, MeetYou) and Philips
narrowed to Philips Digital; the run stops if an alias matches no developer or one
store account falls under two providers; `provider-review.csv` lists provider
pairs among the reached candidates whose website or policy links share a domain,
and the tables are written only when each pair is merged or listed in `distinct`.
The score field is `popularity` (v003: `exposure`). It also writes
`03_Thesis/tables/developer-rule.tex` (selection without the developer rule),
`03_Thesis/tables/developer-aliases.tex` (aliases with `alias_evidence`) and the
sample as `05_Data/processed/app-sample/apps.csv`. Takes about four minutes
(60 sensitivity variants).

## v003

```powershell
python scripts/app-ranking/v003/rank.py scripts/app-ranking/v003/config.json
python -I -m unittest discover -s scripts/app-ranking/v003/tests
```

**Inputs** (paths in `config.json`): an `appstore-scraper/v007` and a
`googleplay-scraper/v004` output, the keyword table
`04_Study/4.4_App-Sampling/keywords.csv` and the screening decisions
`04_Study/4.4_App-Sampling/screening.csv` (one row per screened listing: decision,
criterion E1–E5, category, reason).

**Method.** Listings in the first `depth` results of any keyword are pooled per
store; the preinstalled listings are removed. The same app in both stores (same
provider and a matching title, or a hand-made pair in `pairs`) becomes one
candidate. Each candidate gets the German-market popularity score P = v + c·r:
r is the German App Store rating count, v the German Google Play written-review
count, and c = median(v / r) over matched candidates with positive counts in both
stores, before eligibility screening, × `os_share.ios` / `os_share.android`.
These shares are mobile web page-view shares used as a proxy for the platform
distribution of users. The score has Play review-equivalent units; it does not
estimate actual users or encounters with privacy communication. A listing absent
from the search frame contributes zero from that store, without implying actual
store unavailability. Script v003 retains the output field `exposure` for this
unchanged score. Candidates are taken by descending score, with ties broken by
the candidate key; one is skipped when its
developer is already in the sample, including the preinstalled vendors. Developers
are compared after removing case, accents, punctuation and legal forms; `aliases`
maps further spellings. An excluded listing in either store excludes the candidate.
A candidate without a screening decision counts as eligible and is reported as
pending; the selection is final only when nothing is pending.

**Outputs.** `selection.csv`, `excluded.csv`, `sensitivity.csv` (how many selected
providers change under each variant), `report.json` (cascade, calibration, checks,
categories) and `screening-sheet.csv` (pending listings, for screening). It also
writes `03_Thesis/tables/app-sample.tex`.

**What the counts mean.** App Store rating counts come from the requested
storefront. On Google Play, the rating count and installs are worldwide, the
histogram is the country's distribution scaled to the worldwide count, and the
review count embedded in the product page follows the storefront country (checked
25 October 2026).
