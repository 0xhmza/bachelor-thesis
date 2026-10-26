# App sample

`apps.csv` is the 50-app sample: rows 1–47 are the ranked apps in descending
order of the German-market popularity score, 48–50 the preinstalled apps (D1,
D2, D6). Written by
[`scripts/app-ranking/v004/rank.py`](../../../scripts/app-ranking/README.md) from
the frozen collections in `05_Data/raw/app-sample_2026-10-25/` (listed in
[`../../raw/README.md`](../../raw/README.md)); do not edit by hand. Later work
(policy coding, walkthroughs) starts from these store IDs.

Columns: `order`; `name`, `developer` (as listed); `stores`; `apple_id` and
`play_id`; `german_ratings_app_store` (r), `german_reviews_google_play` (v),
`popularity` (P = v + c·r, rounded); `category`; `best_position` (best search
position in either store); `provider` (normalised provider key, rules P1–P3 in
D2); `preinstalled`.
