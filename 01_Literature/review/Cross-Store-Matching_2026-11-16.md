# Cross-store app matching in prior studies

Prepared 16 November 2026 for the same-app matching of the app sample (Decision D2: several apps of one provider stay separate apps; two listings are merged only when they are the same app on Google Play and the App Store).

Every method below was read in the paper itself. Page numbers refer to the PDF in `library/` unless a printed page is given. Quotes are kept under 15 words.

## Overview

| Study | Field | Scale | How the same app is found | Validation |
|---|---|---|---|---|
| Han et al. 2013 (NDSS) | Security/privacy | 312,171 Android + 478,819 iOS apps | App name, developer, description similarity (term-frequency vectors, cosine ≥ 0.45; name edit distance ≤ 5) → five candidate sets | 60 random pairs per set checked by hand; 1,300 analysed pairs all checked by hand |
| Ali et al. 2017 (MOBILESoft) | Software engineering | 1.4 M Android + 1 M iOS apps | Cluster per platform (same developer, category, similar name), then exact app name + exact developer name across stores | 100 random pairs checked by hand: no false positives |
| Hu et al. 2018 (EMSE) | Software engineering | Top 50 free apps of each US store | Manual inspection of the two charts | None reported beyond the manual pairing |
| Kollnig et al. 2022 (PoPETs) | Privacy | 285,680 iOS + 283,065 Android apps | TF-IDF vectors of app title + app identifier, cosine similarity ≥ 0.95 | None reported |
| Steinböck et al. 2024 (MSR) | Software engineering / privacy | ~10,000 apps per store | Seven features (name, developer, app ID, privacy-policy URL, description, icon, deep links), averaged; best candidate with average ≥ 0.5 | 3,467 reference pairs from Google's iPhone-to-Android migration service: 95.82 % correct |
| Huckvale et al. 2019; O'Loughlin et al. 2019 (health apps) | Health apps | 36 and 116 apps | "Deduplication" by hand; no rule stated | None reported |

The two health-app papers show the usual practice in this field: both stores are searched and duplicates are removed by hand, without a stated rule. The four computer-science papers give an explicit rule.

## 1. Han et al. 2013: candidate sets by name, developer and description

*Comparing Mobile Privacy Protection through Cross-Platform Applications*, NDSS 2013. `library/Han_2013_MobilePrivacyCrossPlatformApps.pdf`.

- **Data.** Crawled product pages of 312,171 Android and 478,819 iOS apps, April–May 2012 (§III.A, p. 3).
- **Definition.** Two apps are versions of one cross-platform app if they have the same functionality; example: Facebook on both platforms (§III.B, p. 3).
- **Rule.** An automatic tool compares app name, developer ("developing company") and description, and sorts pairs into five non-overlapping candidate sets (§III.B, p. 3; Appendix A, Table X, pp. 14–15):
  - **Description:** compared with a vector space model, using term-frequency weights and cosine similarity after removing stop words, numbers and HTML tags. High similarity means at least 0.45, a threshold set "by manual tuning".
  - **Name:** "similar name" means a Levenshtein distance of at most 5.

  | Set | Condition | Pairs | True-positive rate |
  |---|---|---|---|
  | CS1 | same name, same company, high description similarity | 20,171 | 100 % |
  | CS2 | same name, same company, low similarity | 2,230 | > 98.3 % |
  | CS3 | same name, different company, high similarity | 8,870 | 83.3 % |
  | CS4 | similar name, same company, high similarity | 10,837 | 68.3 % |
  | CS5 | same name, different company, low similarity | 14,046 | 6.67 % |

- **Validation.** For each set, 60 random pairs were checked by hand on description, company, icon and screenshots (Appendix A, p. 15). From the true-positive rates, they estimate that 12.2 % of Android apps have an iOS version (§III.B, p. 3).
- **Use.** They analysed only CS1, the strictest set. From it they drew 1,300 pairs, stratified by category and taking the most popular free apps, and checked all of them by hand (§III.C, pp. 3–4).
- **Lesson.** A different developer name is a weak signal. Same name with a different developer is correct in 83 % of pairs when descriptions agree, but in only 7 % when they do not.

## 2. Ali et al. 2017: exact name and developer, after clustering

*Same App, Different App Stores: A Comparative Study*, MOBILESoft 2017, pp. 79–90, doi:10.1109/MOBILESoft.2017.3. `library/Ali_2017_SameAppDifferentAppStores.pdf`.

- **Data.** 1.4 million Android and 1 million iOS apps, Sep–Nov 2015; only attributes available in both stores (§2.1, p. 2).
- **Why not IDs.** The app identifiers differ in form between the stores (an Android package name versus an 8-digit iOS number), so they cannot link apps. Names are "generally consistent", so app name and developer name are used (§2.2, p. 2).
- **Rule.**
  1. Cluster the apps within each platform. One cluster holds apps with the same developer, the same category and similar names, which catches near-variants of one app (§2.2, pp. 2–3).
  2. Match each Android cluster to iOS clusters with a similar developer name.
  3. Within a matched cluster, look for an exact app name *and* exact developer name (criterion E). If there is none, relax both to similar (criterion S) (§2.2, p. 3, Fig. 4).
- **Result.** Criterion E gave 80,169 pairs (8 % of iOS apps, 5.7 % of Android apps). Criterion S gave 116,326 pairs (§3.1, p. 5).
- **Validation.** Two authors compared name, description, developer, icon and screenshots of 100 random E pairs and found no false positives (§2.2, p. 3).
- **Limitation (their own).** Exact matching misses true pairs, for example *The Wonder Weeks* (iOS) vs. *Baby Wonder Weeks Milestones* (Android) (§ Threats to Validity, p. 9).
- **Lesson.** Exact matching is precise but misses pairs. That is acceptable for comparing stores, but not for a sample in which a missed pair would count one app twice.

## 3. Hu et al. 2018: manual matching of top charts

*Studying the consistency of star ratings and the complaints in 1 & 2-star user reviews for top free cross-platform Android and iOS apps*, Empirical Software Engineering 23:3442–3475, doi:10.1007/s10664-018-9604-y. `library/Hu_2018_ConsistencyStarRatingsComplaints_manuscript.pdf` (manuscript version; §3.1 is on p. 5 of this copy and on pp. 6–7 of the SAIL manuscript that the `.bib` note cites).

- **Data.** The top 50 free apps of the US Google Play and App Store charts on 30 October 2015, taken from App Annie (§3.1, p. 5).
- **Rule.** Fully manual. Names differ between the stores (Skype is *Skype for iPhone* on iOS and *Skype – free IM & video calls* on Android), so the authors "did not use an automated approach". They inspected the two charts by hand and found 19 apps in both (§3.1, p. 5).
- **Validation.** No second rater is reported for the pairing.
- **Limitation (their own).** The 19 apps are few and do not cover all categories (§6.1.1).
- **Lesson.** For small, popular samples, manual matching is accepted in a peer-reviewed journal, but it should state its criteria, which this paper does not.

## 4. Kollnig et al. 2022: title and identifier similarity

*Are iPhones Really Better for Privacy? A Comparative Study of iOS and Android Apps*, PoPETs 2022, pp. 6–24, doi:10.2478/popets-2022-0033. `library/Kollnig_2022_iPhonesBetterForPrivacy.pdf` (arXiv version; pages below are its pages).

- **Data.** 568,745 free apps (285,680 iOS, 283,065 Android) from the UK stores, Dec 2019–Feb 2020. 24,000 apps were downloaded, 12,000 per platform (§3.1, p. 5).
- **Rule.** Terms from app titles and app identifiers are TF-IDF weighted over all apps of both stores. Two apps count as cross-platform if their vectors have a cosine similarity of at least 0.95 (§3.1, p. 6). The developer name is not used.
- **Result.** 13.7 % of the downloaded Android apps and 12.8 % of the iOS apps (§3.1, p. 6). The authors call it "a simple similarity algorithm".
- **Validation.** None reported.
- **Use.** Cross-platform apps are compared with all apps on privacy indicators. They show more tracking, which the authors relate to popularity (§4.5, pp. 13–14).
- **Lesson.** Cross-platform apps differ from the average app. Steinböck et al. found that this method recovers about 51 % of true pairs (see 5).

## 5. Steinböck et al. 2024: seven features, validated against reference pairs

*Comparing Apples to Androids: Discovery, Retrieval, and Matching of iOS and Android Apps for Cross-Platform Analyses*, MSR 2024, doi:10.1145/3643991.3644896. Already cited in the thesis (`steinboeck2024comparing`). Printed pages.

- **Definition.** Two apps are the same if human experts would judge them so: same use cases, same core functionality, same provider, different platforms (§3.2, p. 352). Merely similar apps (two calculators) or separate builds (Firefox vs. Firefox Nightly) are not the same.
- **Why names fail.** *Babbel – Language Learning* vs. *Babbel – Learn Languages*, and *1&1 Mail & Media GmbH* vs. *1&1 Telecom GmbH*, have normalized Levenshtein distances of about 0.5 (p. 352).
- **Features** (§3.2.2, Table 1, p. 353), each scored between 0 and 1:
  - **App name, developer name and app ID:** the higher of shared-prefix length and Levenshtein similarity.
  - **Privacy-policy URL:** same domain plus string similarity.
  - **Description:** TF-IDF cosine similarity, with English and German stop words removed.
  - **Icon:** the best of three image hashes (average, perceptual, wavelet).
  - **Deep links:** identical URL schemes and app links, taken from the app binary.
- **Rule.** Every iOS app is scored against every Android app. The match is the candidate with the highest *average* score, and it must reach at least 0.5. The average beat the median and a clamped linear function (§3.4, p. 354; §5.2, p. 355).
- **Validation.**
  - **Reference pairs:** Google's iPhone-to-Android data-migration service. The 300 most-rated pairs were checked by two authors, with a third breaking ties (§3.3, pp. 353–354).
  - **Accuracy:** 3,322 of 3,467 reference pairs (95.82 %) were matched correctly, with 14 false positives (§5.2.2, p. 355).
- **Features alone.** No single feature separates matches from non-matches. Name, ID and developer need a strict cut-off that misses real pairs (§5.2.3, p. 356).
- **Comparison with the earlier methods** (Table 5, pp. 356–357):

  | Method | Correct pairs |
  |---|---|
  | Exact name + developer (Ali; Han-style exact matching) | under 17 % |
  | Kollnig et al. | about 51 % |
  | Steinböck et al. | 95.82 % |

## Health-app studies that searched both stores

- **Huckvale et al. 2019** searched the US and Australian stores for "depression" and "smoking cessation" and kept the first 10 results of each search. "After pooling and deduplication" they had 36 apps: 15 Android-only, 14 iOS-only and 7 on both platforms. No matching rule is given (Methods, p. 3).
- **O'Loughlin et al. 2019** had three raters remove 29 duplicates in two steps: first from the store descriptions, then by downloading and reviewing the app (§2.2, p. 112). They report results separately for single-platform and multiplatform apps (§3). No matching rule is given.
- **Sunyaev et al. 2015** took the 300 most-rated apps of each store and analysed them per store, without matching across stores.

## What this means for the app sample

1. **The definition** follows Steinböck et al. (§3.2, p. 352), as Methodology 4.4.2 already does. Under D2 it decides only whether two listings are one app. A shared provider alone no longer matters, because several apps of one provider stay separate.
2. **A stated rule is better than the health-app practice.** Huckvale and O'Loughlin report only "deduplication". Han, Ali, Kollnig and Steinböck show that the rule and its error rate can be reported.
3. **Names and developers are not enough.** Ali's exact rule misses pairs; Han's sets CS3 to CS5 show that a different developer or a low description similarity makes errors likely; Steinböck shows names fail on their own. The current proposal step (shared developer, app ID, title or description passages) followed by a manual decision on product evidence fits a sample of about 1,500 listings, where Hu et al. also matched by hand.
4. **Two of Steinböck's features are cheap to add from the collected listings:**
   - **Icon hash:** both stores give an icon URL.
   - **Privacy-policy URL:** both listings link to their policy.

   Deep links need the app binary, and the migration-service reference pairs need a rooted phone, so neither is practical here.
5. **Validation like Ali and Han.** A second check of a random sample of decided pairs (Ali: 100 pairs; Han: 60 per set) would give an error estimate. It would also fit the validation chapter (Methodology 4.7).
6. **Cross-platform apps differ** (Kollnig §4.5): apps in both stores are more popular and track more. This is a reason to report the store composition of the sample (Results 5.2 already does: 36 in both stores, 5 Google Play only, 6 App Store only).

## Bibliography status

Hu 2018 is in `03_Thesis/references.bib` as `hu2018studying` but is not yet cited. Han 2013, Ali 2017 and Kollnig 2022 are **not in the bibliography**. The DOIs above were checked against Crossref on 16 November 2026; NDSS 2013 has no DOI. Add the entries only if the thesis cites them. The PDFs of Han, Ali and Kollnig were saved to `library/` on 16 November 2026; Hu 2018 was already there.
