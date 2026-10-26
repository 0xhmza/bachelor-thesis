# Literature search

Stage 0 of the literature review ([D13](../../00_Admin/Decisions/D13_literature-review.md)):
database search, works added by hand, duplicates and citation filter; and the thesis
tables built from the screening. Each version lives in `vNNN/`; outputs stay in the
version's `output/` folder.

- `v001/`: the search of 26 October 2026, frozen in `05_Data/raw/literature-search_2026-10-26/`.

## v001

```powershell
python scripts/literature-search/v001/search.py scripts/literature-search/v001/config.json
python scripts/literature-search/v001/search.py scripts/literature-search/v001/config.json --reuse-hits
python scripts/literature-search/v001/report.py
python -I -m unittest discover -s scripts/literature-search/v001/tests
```

`search.py` sends the four queries of `config.json` to OpenAlex and Semantic Scholar
(titles and abstracts), looks up the works in `manual.json` (OpenAlex by DOI; one
USENIX paper without DOI in Semantic Scholar by paper ID), merges records that share a
DOI, arXiv ID or normalised title (years at most one apart) and applies the filter of
at least 3 citations per year (no exemption for recent works). It writes
`output/hits.jsonl`, `output/manual-hits.jsonl`, `output/records.csv` and
`output/run.json`. `--reuse-hits` rebuilds `records.csv` and `run.json` from the saved
hits without querying again. Without an API key OpenAlex shares a small daily budget
per IP address and allows page-number paging only; the full search takes about ten
minutes.

`report.py` reads the frozen collection and `01_Literature/Systematic-Review/screening.csv`
and writes `03_Thesis/tables/literature-queries.tex`, `literature-flow.tex` and
`literature-included.tex`.

Standard library only.
