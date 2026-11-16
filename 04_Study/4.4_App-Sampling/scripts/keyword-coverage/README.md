# keyword-coverage

Which keyword categories of `keywords.csv` the 47 ranked apps of the sample cover
(Results 5.2, Decision D3 update of 15 November 2026).

- `v001/coverage.py` reads the frozen search results in `05_Data/App Sampling/26. Oct/Raw/`
  and the sample in `05_Data/App Sampling/26. Oct/Processed/apps.csv`. An app counts for a
  category when it appears within the first 30 positions of at least one query of that
  category, in either store. Writes `v001/output/coverage.csv` (not in Git).

- `v002/coverage.py` (16 November 2026) groups the ten keyword categories into the six
  health categories of the domain (activity: cycling, exercise, running, step count; diet and
  weight: diet, weight) and writes one table with both views of the sample: the main function
  (primary category of all 50 apps, each app once) and the ranked apps found by each group's
  queries (an app can count in several). It also prints how many groups found each ranked app.
  Writes `v002/output/categories.csv` (not in Git) and `03_Thesis/tables/sample-categories.tex`
  (Table 5.3). Replaces v001's two tables.

- `v003/coverage.py` (16 November 2026) adds the reach of each of the 49 queries in the final
  sample of 50 apps (preinstalled apps through their store listings): apps within the first 30
  positions in either store, share of 50, and apps that no other query found. Writes
  `v003/output/keywords.csv` (not in Git), `03_Thesis/tables/keyword-reach-top.tex` (Table 5.4,
  ten widest) and `03_Thesis/tables/keyword-reach.tex` (appendix, all queries), and still writes
  `sample-categories.tex`.

Run: `python 04_Study/4.4_App-Sampling/scripts/keyword-coverage/v003/coverage.py`
