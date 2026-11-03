# Raw data

Files here are not in Git (see `../README.md`). This list is, so a backup can be
checked against it.

## app-sample_2026-10-25

The store collections the app sample is built on. All later work (ranking,
screening, policy coding, walkthroughs) reads these files, not the scripts'
`output/` folders. Copied unchanged on 26 October 2026 and set read-only.

| File | Collected | Collector | From | SHA-256 |
|---|---|---|---|---|
| `appstore_2026-10-23.json` | 23 Oct 2026, 19:46 UTC; 49 queries, limit 200 | `scripts/appstore-scraper/v007` | `v007/output/run-2026-10-23.json` | `f222b474cbec444732dbc3fbb51a4a15b6ff1e72fba982f45cff08b24c6d43b6` |
| `googleplay_2026-10-24.json` | search 24 Oct 2026, 15:07 UTC; pages 24–25 Oct; 49 queries, depth 30, 645 apps | `scripts/googleplay-scraper/v004` | `v004/output/run-2026-10-25-all.json` | `4ea95c01b6e89ed638b21c44aef51e3d2580836d0c82bda7d6a0cd8426da46fe` |
| `googleplay-pages_2026-10-24.jsonl` | product pages of the run above, one per line | `scripts/googleplay-scraper/v004` | `v004/output/pages-2026-10-24.jsonl` | `814c1936fa67805908e9793689352c310de60daa90a7ed797befeb495dfc6488` |
| `googleplay_2026-10-24.log` | progress log of the run above | `scripts/googleplay-scraper/v004` | `v004/output/run-2026-10-25-all.log` | `5befc207822c5dfd1aca6e9e6be58bd6c59729ab798e2a8dd41cc5d7d16dbc83` |
| `googleplay-pilot_2026-10-22.json` | 22 Oct 2026, 20:58–21:12 UTC; 19 keywords, first 20 results (trial collection, D2) | `scripts/googleplay-scraper/v002` | `v002/output/pilot-de-19kw.json` | `43c808297fc5c7200098be241b3d56775f1ba375b457499b7ea47724cbdd07f7` |

Check: `sha256sum 05_Data/raw/app-sample_2026-10-25/*`. The selected apps derived
from these files are in [`../processed/app-sample/`](../processed/app-sample/README.md).

## literature-search_2026-10-26

The database search of the literature review (D13). The screening in
`01_Literature/Systematic-Review/screening.csv` and the thesis tables read these
files. Copied unchanged from `scripts/literature-search/v001/output/` on
26 October 2026.

| File | Content | SHA-256 |
|---|---|---|
| `hits.jsonl` | every hit of Q1–Q4 in OpenAlex and Semantic Scholar, searched 26 Oct 2026, 18:13 UTC; 5,667 lines | `14288889e5c8552fa49416b1617f0e4b3addab10f042e418b74485517ae88cf0` |
| `manual-hits.jsonl` | the 15 works added by hand (`v001/manual.json`) | `1cf3ba324252f65416a6fae8656279a7be0f1667cb5eca681f42cbf062bf8928` |
| `records.csv` | 3,506 merged records with citations per year and the filter result | `85fce998438363dafe839b2cbddc7b59e4081fee94541f5b613f270d65f203a1` |
| `run.json` | counts per query and database and per stage | `54fdd1cc81b4cf8f832737756349a021ae15c4d18aed0d158f8f59bf27ca0c26` |

Check: `sha256sum 05_Data/raw/literature-search_2026-10-26/*`.

## appstore/fitness_de_2026-10-20

Earlier App Store fitness search (20 October 2026), kept for the record.
