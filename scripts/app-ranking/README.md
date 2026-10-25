# App ranking

Selects the ranked apps of the sample as set out in
[D2](../../00_Admin/Decisions/D02_ranking-and-rating-floor.md). Each version lives in
`vNNN/`; outputs stay in the version's `output/` folder.

- `v001/rank.py`: merges the stores by within-store percentile; replaced, kept for
  the record.
- `v002/rank.py`: selection of 24 October 2026 by store alternation with the worldwide
  Play count; replaced by v003, kept for the comparison.
- `v003/rank.py`: the selection of 25 October 2026 (D2 revision).

## v003

```powershell
python scripts/app-ranking/v003/rank.py scripts/app-ranking/v003/config.json
python -I -m unittest discover -s scripts/app-ranking/v003/tests
```

**Inputs** (paths in `config.json`): an `appstore-scraper/v007` and a
`googleplay-scraper/v004` output, the keyword table
`04_Study/App-Sample/keywords.csv` and the screening decisions
`04_Study/App-Sample/screening.csv` (one row per screened listing: decision,
criterion E1–E5, category, reason).

**Method.** Listings in the first `depth` results of any keyword are pooled per
store; the preinstalled listings are removed. The same app in both stores (same
provider and a matching title, or a hand-made pair in `pairs`) becomes one
candidate. Each candidate gets the German exposure E = v + c·r: r is the German App
Store rating count, v the German Google Play review count, and
c = median(v / r) over candidates in both stores × `os_share.ios` /
`os_share.android`. Candidates are taken in the order of E; one is skipped when its
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
