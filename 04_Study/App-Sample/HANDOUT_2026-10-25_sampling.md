# App sampling: state on 25 October 2026

For the thesis author and whoever continues. The sample is drawn with
`app-ranking/v003`; Results "Sample" (`sec:results-sample`) and Appendix C are
written from its output.

## 1. Where things stand

| Step | State |
|---|---|
| Design decisions | D1–D7, D11 written before collection; all **proposed** except D5 and D7 (13 October meeting). D2 revised on 25 October: one German ranking of both stores |
| App Store collection | Done, 23 October, `appstore-scraper/v007` |
| Google Play collection | Search 24 October, product pages of all 645 apps 24–25 October, `googleplay-scraper/v004` |
| Screening | 275 listings decided ([screening.csv](screening.csv)); **first pass by an AI assistant, to be checked by the author** |
| Selection and sensitivity checks | Done, `app-ranking/v003`, nothing pending |

## 2. The result

- Ranking: E = v + c·r (v German Play reviews, r German App Store ratings);
  c = 0.090 from 114 apps listed in both stores (Spearman r–v 0.80) and the
  German OS shares (Android 72.3 %, iOS 27.7 %).
- 47 ranked apps from 47 providers (32 in both stores, 9 Google Play only,
  6 App Store only) plus Apple Health, Apple Fitness and Samsung Health: 50 apps.
- Categories of the 47: activity 22, diet and weight 12, cycle 4, sleep 3,
  pregnancy 2, mood 2, heart 1, wearable companion 1.
- Providers changed out of 47: pool-sum scale 0, depth 20 1, App Store depth 200 2,
  English only 2, German only 3, one keyword left out ≤ 1, equal platform weights 5,
  no developer rule 10, earlier selection (v002) 10, worldwide Play count 11.

Full figures: `scripts/app-ranking/v003/output/report.json`.

## 3. Next steps

1. **Check [screening.csv](screening.csv)**, then remove the `\todo` in Results
   §5.1 and state who screened. Borderline calls: Headspace (in, mood tracking)
   against Calm, Insight Timer, 7Mind and BetterSleep (out); Gymondo and Kinomap
   (out) against other workout apps (in); STADTRADELN, komoot and Bikemap (in,
   activity recording); Oviva (out as a DiGA; confirm in the BfArM directory);
   Meine AOK (out, E2).
2. **Supervisor questions:** domain from Hutton et al. and Malki et al. (D3); one
   app per developer and the German exposure ranking (D2); the vendor rule (D6);
   the two mood apps and the six cycle and pregnancy apps against the two-domain
   design.
3. Back up the git-ignored outputs: `scripts/appstore-scraper/v007/output/`,
   `scripts/googleplay-scraper/v004/output/`, `scripts/app-ranking/v003/output/`.

To rerun: `python scripts/app-ranking/v003/rank.py scripts/app-ranking/v003/config.json`
(it also rewrites `03_Thesis/tables/app-sample.tex`).
