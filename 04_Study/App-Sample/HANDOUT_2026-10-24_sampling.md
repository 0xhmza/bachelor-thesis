# App sampling: state on 24 October 2026 (evening)

For the thesis author and whoever continues. The sample is drawn; the Results
section "Sample" and Appendix C are written from the script output. Nothing is
committed.

## 1. Where things stand

| Step | State |
|---|---|
| Design decisions | Written before collection (D1–D7, D11); all **proposed** except D5 and D7, which follow the 13 October meeting |
| App Store collection | Done, 23 October, `appstore-scraper/v007` |
| Google Play collection | Done, 24 October, `googleplay-scraper/v004`, 100 product pages chosen by install band (D2) |
| Screening | 263 listings decided ([screening.csv](screening.csv)); **first pass by an AI assistant, to be checked by the author** |
| Selection and sensitivity checks | Done, `app-ranking/v002`, nothing pending |
| Thesis | Methodology App Sampling, Results "Sample" (`sec:results-sample`), Appendix C (generated table), Appendix E (v007, v004) |

## 2. The result in brief

- 47 ranked apps from 47 providers (24 Google Play, 23 App Store) plus Apple
  Health, Apple Fitness and Samsung Health: 50 apps.
- Categories of the 47: activity 23, diet and weight 8, cycle 7, pregnancy 4,
  sleep 2, mood 2, wearable companion 1.
- Stable under search-frame changes (depth 20: 0 changes; App Store depth 200: 2;
  App Store first: 1; one keyword left out: at most 1); less stable under other
  ranking measures (rating count per year: 8; blend with average rating: 14).
- The 100-page limit did not change the selection: the three unopened apps of
  the cut-off band have fewer ratings than the last selected Play app.

Full figures: `scripts/app-ranking/v002/output/report.json` and Results §5.1.

## 3. What happened on the way (all recorded in D2)

- The v003 Play run (23 October) took about 5 s per page and was stopped after
  2 h 50 min without output; it also dropped each query's highlighted top result,
  because the parser misses that card's app ID. v004 reads the ID from the
  card's details URL, ranks hits by install band, opens 100 pages and writes each
  page to a resumable cache.
- Play pages showed 8 to 50 results per query, not 20 to 30.
- Developer names differ between the stores for eight providers (Clue,
  Pregnancy+, Alarmy, Leap Fitness, Map My Run, Daylio, MeetYou, BabyCenter);
  before they were matched by hand, Clue and Pregnancy+ were selected twice.
- Apple Health has a German App Store listing (D6 corrected).

## 4. Next steps

1. **Check [screening.csv](screening.csv)**, then remove the `\todo` in Results
   §5.1 and state who screened. Borderline calls: Headspace (in, mood tracking)
   against Calm, Insight Timer, 7Mind and BetterSleep (out); Gymondo and Kinomap
   (out) against other workout apps (in); STADTRADELN, komoot, Outdooractive and
   Bikemap (in, activity recording); Pokémon Sleep (in, records sleep); Oviva
   (out as a DiGA; confirm in the BfArM directory); Meine AOK (out, E2).
2. **Supervisor questions** the sample now makes concrete: domain from Hutton et
   al. and Malki et al. (D3); one app per developer (D2); the two mood apps do not
   fit the two-domain design (two harm trees, per-domain walkthroughs and
   validation); with 11 reproductive apps the per-domain walkthrough and
   validation plans are feasible.
3. Back up the git-ignored raw data: `scripts/appstore-scraper/v007/output/`,
   `scripts/googleplay-scraper/v004/output/`, `scripts/app-ranking/v002/output/`
   (or copy them to `05_Data/raw/` with a date sidecar).
4. Semantic re-extraction of the graph (19 files reported stale).

To rerun the selection: `python scripts/app-ranking/v002/rank.py scripts/app-ranking/v002/config.json`
(it also rewrites `03_Thesis/tables/app-sample.tex`).
