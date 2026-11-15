# keyword-coverage

Which keyword categories of `keywords.csv` the 47 ranked apps of the sample cover
(Results 5.2, Decision D3 update of 15 November 2026).

- `v001/coverage.py` reads the frozen search results in `05_Data/App Sampling/26. Oct/Raw/`
  and the sample in `05_Data/App Sampling/26. Oct/Processed/apps.csv`. An app counts for a
  category when it appears within the first 30 positions of at least one query of that
  category, in either store. Writes `v001/output/coverage.csv` (not in Git).

Run: `python 04_Study/4.4_App-Sampling/scripts/keyword-coverage/v001/coverage.py`
