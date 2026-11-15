# Literature search

The literature review of the thesis: search, deduplication, screening log and the
thesis tables and figures. Each version lives in `vNNN/`; outputs stay in the
version's `output/` folder (outside Git).

- `v001/`: the search of 26 October 2026 in OpenAlex and Semantic Scholar
  ([D13](../../00_Notes/Archive/Decisions/D13_literature-review.md), superseded), frozen in
  `05_Data/Literature Search/26. Oct/`.
- `v002/`: the search of 28 October 2026 ([D14](../../00_Notes/Archive/Decisions/D14_literature-review-v2.md)),
  frozen in `05_Data/Literature Search/28. Oct/`; screening protocol and log in
  [`01_Literature/review/`](../../01_Literature/review/README.md).
- `v003/`: the v002 method as revised in the thesis on 30 October 2026, without the
  German-language strand S5 (groups DE and DEP). The search is not repeated: `report.py`
  reads the frozen search of 28 October. So far only the search strings of Appendix F
  come from v003; the other tables and figures are still those of v002 until the results
  are revised.

## v003

```powershell
python scripts/literature-search/v003/report.py groups strings   # -> 03_Thesis/tables/literature-groups*.tex, literature-strings.tex
python -I -m unittest discover -s scripts/literature-search/v003/tests
```

`report.py` without an argument writes every table and figure, as in v002; it needs
`output/merge.json` and `output/screening.json` of v003, which exist only once the
remaining steps have been rerun for the revised method.

## v002

Run in this order (standard library only; PyMuPDF only for reading the full texts):

```powershell
python scripts/literature-search/v002/search.py pubmed arxiv acl venues   # databases and venue lists
# IEEE Xplore: the four strings of output/run-*.json were run in its web interface; results in output/ieee-raw.json
python scripts/literature-search/v002/citations.py   # backward and forward citations (OpenCitations, Crossref)
python scripts/literature-search/v002/merge.py       # deduplication and provenance -> output/records.csv
python scripts/literature-search/v002/enrich.py      # abstracts by DOI (OpenAlex), for screening only
python scripts/literature-search/v002/merge.py
python scripts/literature-search/v002/show.py batch NAME [SOURCE] [N]   # reading aid; decisions go to decisions/raw/NAME.txt
python scripts/literature-search/v002/show.py expand                    # -> decisions/title.csv
python scripts/literature-search/v002/fulltext.py    # open-access full texts of the records that passed
python scripts/literature-search/v002/screening.py   # -> 01_Literature/review/screening.csv, counts per rule
python scripts/literature-search/v002/extract.py     # evidence-map codes -> 01_Literature/review/extraction.csv
python scripts/literature-search/v002/report.py      # -> 03_Thesis/tables/literature-*.tex, figures/literature-*.tex
python -I -m unittest discover -s scripts/literature-search/v002/tests
```

`config.json` holds the term groups, strands, venues, extraction rules, citation seeds, the
43 thesis citations before the review and the duplicates merged by hand. `search.py`
caches every GET response in `output/cache/http`, so an interrupted run resumes.

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
