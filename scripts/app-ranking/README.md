# App ranking

Ranks eligible apps by exposure (rating count), as proposed in
[D2](../../00_Admin/Decisions/D02_ranking-and-rating-floor.md). Each version lives in
`vNNN/`; outputs stay in the version's `output/` folder.

- `v001/rank.py`: standard-library ranking script with unit tests in `v001/tests/`.
  It merges the stores by within-store percentile, a rule D2 has since replaced by
  alternation; kept for the record.
- `v002/rank.py`: the selection of 23 October 2026 (D1, D2, D3, D6). Standard library,
  unit tests in `v002/tests/`.

## v002

```powershell
python scripts/app-ranking/v002/rank.py scripts/app-ranking/v002/config.json
python -I -m unittest discover -s scripts/app-ranking/v002/tests
```

**Inputs** (paths in `config.json`): an `appstore-scraper/v007` and a
`googleplay-scraper/v003` output, the keyword table
`04_Study/App-Sample/keywords.csv` and the screening decisions
`04_Study/App-Sample/screening.csv` (one row per screened listing: decision,
criterion E1–E5, category, reason).

**Method.** Within each store, listings in the first `depth` results of any keyword
with at least `floor` ratings are ranked by rating count, ties by listing ID; the
preinstalled listings are removed. Apps are taken alternately from the two lists,
starting with `start`. A listing is skipped when its developer is already in the
sample, including the preinstalled vendors; developers are compared after removing
case, punctuation and legal forms (`aliases` maps further spellings). A listing
without a screening decision counts as eligible and is reported as pending; the
selection is final only when nothing is pending.

**Outputs.** `selection.csv` (order, store, listing, developer, ratings, category,
best search position, counterpart in the other store), `excluded.csv`,
`sensitivity.csv` (how many selected providers change under each variant),
`report.json` (cascade per store, proxy check, depth, categories, German exposure
check) and `screening-sheet.csv` (pending listings with a description excerpt, for
screening).

**What a rating count means per store.** App Store counts come from the requested
storefront. Google Play's rating count and install figure are worldwide; its
histogram is the country's distribution scaled to the worldwide count. Rankings are
therefore made within each store.
