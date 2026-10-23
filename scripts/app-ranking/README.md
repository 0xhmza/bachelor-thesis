# App ranking

Ranks eligible apps by exposure (rating count), as proposed in
[D2](../../00_Admin/Decisions/D02_ranking-and-rating-floor.md). Average rating is
an optional blend used for sensitivity checks. Each version lives in `vNNN/`;
outputs stay in the version's `output/` folder.

- `v001/rank.py`: standard-library ranking script with unit tests in `v001/tests/`.

```powershell
python scripts/app-ranking/v001/rank.py scripts/appstore-scraper/v005/output/<file>.json --domain fitness
python scripts/app-ranking/v001/rank.py a.json b.csv --domain fertility --floor 1000 --top 20 --exclude excluded_ids.txt
python scripts/app-ranking/v001/rank.py a.json --domain fitness --weight-exposure 0.5   # blend in rating quality
python -I -m unittest discover -s scripts/app-ranking/v001/tests
```

**Inputs.** A v005 scraper JSON (Apple), or a CSV with `id, name, store, rating,
rating_count` and optionally `released, keywords` (use it for Google Play data).
Listings are de-duplicated by ID and keep every keyword that found them.

**Method.** Within each store: floor on rating count, then rank by `E = log10(rating
count)`. Stores are merged by within-store percentile. The default exposure weight
`w = 1` ranks on exposure alone. With `w < 1` the score is `w·rank(E) + (1−w)·rank(Q)`,
where `Q` is the average rating shrunk toward the pool mean with prior weight `m`
(default: the floor). API position and downloads are not used. The JSON reports how
the top N changes under blends (`w` = 0.75, 0.5, 0.25) and under rating count per
year since release.

**What a rating count means per store.** App Store counts come from the requested
storefront (`--region de` gives German counts). Google Play's rating count,
histogram and install figure are global whatever `gl` says, so Play CSV input
carries a global count. Rankings are therefore made within each store. See
[D2](../../00_Admin/Decisions/D02_ranking-and-rating-floor.md).

**Eligibility.** The script applies only the rating floor. Function, language,
payment and DiGA rules are manual: list the excluded IDs (`apple:123`, one per
line) in a file passed to `--exclude`.

**Outputs.** `ranking-<domain>-<timestamp>.csv` (ordered list) and `.json`
(parameters, input hashes, exclusion cascade, sensitivity variants). A run on
unfiltered scraper output demonstrates the mechanics and is not a sample.
