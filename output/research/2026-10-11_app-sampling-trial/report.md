# App-store sampling feasibility trial

**Methods, reproducible collection and provisional working set**

Bachelor-thesis research report | 11 October 2026 | Protocol app-sampling-trial-v1

**Status: executed trial. The 50-product working set is provisional and must not be described as the final eligible analysis sample.**

## 1. Executive findings

The trial retrieved 202 distinct store listings, preserved their source responses, and demonstrated an automated ranking pipeline that produces a 30-fitness / 20-fertility working set. The current proposal ranks by average rating after a 1,000-rating threshold; that rule was retained. Google Play's embedded install count was captured separately for evaluating a possible later change toward a reach-based design.

The collection frame is incomplete relative to the proposal. Apple candidates came from the documented Search API, whose result order has not been validated against the native App Store. Play candidates came from 24 documented feasibility seeds, rather than the first 20 results of each prescribed store search. Consequently, the working set demonstrates acquisition and selection mechanics, but cannot establish the proposal's final sample or the most popular apps in Germany.

| Measure | Observed result |
| --- | --- |
| Apple keyword API requests | 19 successful / 19 attempted |
| Apple search appearances | 322 |
| Distinct Apple listings | 179 |
| Play listing requests | 24 attempted; 23 successful; 1 HTTP 404 |
| Total distinct captured listings | 202 |
| Pass automated numerical screen | 109 |
| Fail automated listing screen | 87 |
| Pending numerical data | 6 |
| Provisional working set | 50 products: 30 fitness / 20 fertility |
| Verified final thesis sample | 0; not frozen |

The strongest practical outcome is an auditable pipeline: collection inputs are frozen, errors are retained, identities are explicit, raw responses have SHA-256 hashes, and the final-selection gate stays closed when evidence is missing. No proposal text or original sampling protocol was changed.

## 2. Methodological authority and scope

The authority is the Sampling paragraph in the current proposal, archived as `config/proposal_snapshot.tex`. Its SHA-256 is recorded in `config/protocol.json`. The older sampling protocol supplies the concrete 19-keyword list. Where it conflicts with the newer proposal, the proposal prevails: device companions remain eligible when they record or display relevant tracking data.

The unit of analysis is the product, with one or more store listings. The target document sample is 50 products: 30 fitness and 20 fertility. The proposal additionally calls for a five-app coding pilot and 12 walkthroughs. This run is an acquisition feasibility trial; it is not that five-app coding pilot and includes no walkthroughs or harm coding.

The raw collection ran from 2026-10-11T13:50:45.058369+00:00 to 2026-10-11T13:54:21.831792+00:00. Times are UTC. Requests originated from the available host network; actual IP geolocation was not verified. Requests used no authenticated account and no persistent cookie jar. Country parameters were explicitly German, but this does not simulate a clean German Android or iOS device.

## 3. Search specification

The following terms were frozen before this run, without additions after inspecting returned ratings. German terms cover common local descriptions; English terms reflect vocabulary commonly used in German listings. The original protocol's broad fitness scope includes activity, exercise, sleep, heart rate and nutrition tracking.

| Domain | ID | Fixed keyword |
| --- | --- | --- |
| fitness | F1 | Fitness |
| fitness | F2 | Fitness Tracker |
| fitness | F3 | Schrittzähler |
| fitness | F4 | Aktivitätstracker |
| fitness | F5 | Schlaf-Tracker |
| fitness | F6 | Herzfrequenz |
| fitness | F7 | Kalorienzähler |
| fitness | F8 | Ernährungstagebuch |
| fitness | F9 | Workout |
| fertility | P1 | Periode |
| fertility | P2 | Zyklus |
| fertility | P3 | Zyklustracker |
| fertility | P4 | Menstruation |
| fertility | P5 | Eisprung |
| fertility | P6 | Fruchtbarkeit |
| fertility | P7 | Kinderwunsch |
| fertility | P8 | period tracker |
| fertility | P9 | ovulation |
| fertility | P10 | fertility |

For a proposal-faithful collection, record the first 20 organic results per keyword and store in default ordering, with sponsored placements logged separately. This gives 38 search sessions and at most 760 organic appearances before deduplication. Capture within a declared seven-day window, with storefront, query, device, OS, account state, timestamp, displayed rank, app ID and screenshot or page evidence. The organic-result interpretation and collection window operationalize the older protocol's proposed defaults; the proposal itself leaves these details open.

In this trial Apple requests used country=de, media=software, entity=software, limit=20 and lang=en_us. Apple's documented API supports English or Japanese response-language parameters; German interface language was assessed only from declared language codes when available. API requests returned fewer than 20 entries for some queries. Those actual counts are preserved, with no invented padding or follow-up searches. API positions are labelled `source_rank`, while `store_ui_rank` remains empty. [2]

Play seeds were found through logged web searches linking to actual Play product pages, plus the earlier Clue mechanism test. Web-search positions were not converted into store positions. Their domains are initial hints. This seed approach tests the collector and install fields; it creates selection bias and is not a replacement for keyword discovery.

## 4. Inclusion, exclusion and uncertainty rules

An eligible product must be available through a German storefront, collect or display health/body-related tracking data, be free to install, offer German or English interface text, have a reachable relevant policy, and have at least one listing meeting the 1,000-rating threshold. A listing with insufficient ratings contributes neither its rating nor its count to the ranking score. A qualifying counterpart can still make the product numerically eligible.

Exclude products without relevant tracking, paid-only installation, neither permitted interface language, confirmed unreachable policies, DiGA status, or duplicate product identity. Record an unreachable policy as a screening finding before excluding it from text analysis. Confirm DiGA status against the BfArM directory; a medical-device claim alone is not a DiGA exclusion. DiGA checks were not completed in this trial. [5]

Device companions are not excluded solely because they use a paired device. A missing device, payment requirement or identity verification may prevent a walkthrough while leaving the document sample eligible. These separate decisions must not be collapsed. No account creation, installation, payment or personal health input occurred here.

Apps spanning both domains enter fertility when cycle tracking is a main function, with overlap recorded. Preliminary review allocated Ovy to fertility from its description. Oura was provisionally allocated to fitness with cycle overlap flagged for confirmation. Infant sleep trackers were held in an unresolved domain rather than automatically treated as fitness. An EV-charging result named FLO illustrates why keyword or title matches alone cannot establish relevance.

Automated screen codes are E01 (<1,000 ratings), E02 (paid installation), and E03 (declared interface languages exclude both DE and EN). The run produced 85 E01 occurrences and four E02 occurrences across 87 excluded listings; two listings failed both rules. Six listings had missing numerical data and remained pending. Zero counts and missing values are kept distinct. These are listing-level screening outcomes, not counts of fully excluded products.

## 5. Product identity and ranking

Seven provisional cross-store groups were created: StepsApp, ITO Pedometer, Flo, Clue, Clover, GP Apps Period Tracker, and SimpleInnovation My Calendar. The evidence is the captured brand, developer and provider-domain information. Apple policy equivalence and exact product identity remain unverified; every such group is marked provisional. Shared providers do not automatically imply the same product.

SimpleInnovation's additional Cycle Tracker has similar functionality and is flagged for duplicate review. Other same-provider apps may also be duplicates. A single-store row does not prove the other platform has no counterpart. Missing counterparts and revised identity decisions can change the weighted rank.

For each provisional product, the score is the sum of rating multiplied by rating count, divided by the sum of rating counts, using only numerically passing listings. Sort descending by that score, then descending by the contributing rating count. The final tie uses canonical app ID ascending, a stated trial choice because the proposal does not specify the last tie. Computation uses Decimal values without rounding before ranking; report values round to four decimals.

This implements the proposal's arithmetic. It does not establish that the two stores have identical rating populations or scoring systems. Google counts can dominate the weighted score. The result selects highly rated candidates in this trial frame, not a population-representative or Germany-wide popularity sample.

## 6. Technical collection and automation

`collect.py` uses Python's standard-library HTTP client. It issues bounded GET requests, verifies HTTPS certificates, requests German language preference, sets a descriptive user agent, uses a 30-second timeout and spaces request starts by at least 3.5 seconds. It performs no retry and stops further requests to a host after 403 or 429. A 404 is logged as a failed request; the country parameter is never removed to obtain a fallback response.

Apple responses are parsed as JSON. For Play, `process.py` extracts the JSON value inside AF_initDataCallback script blocks and reads the known ds:5 field paths. It executes no page JavaScript and imports no upstream scraper runtime. Field paths were checked against the pinned google-play-scraper source audited earlier. Name, rating range, integer counts and install-bound consistency are validated. A missing dataset is an explicit parser failure; it does not become a successful empty listing. [1]

Every response has original bytes plus a sidecar containing request URL, final URL where available, start/end timestamps, HTTP status, selected response headers, byte count and SHA-256. Failed responses are preserved too. Request cookies and credentials are not collected. The main run saved its protocol, source proposal and collection scripts before fetching. Subsequent derivation scripts and decision hashes identify how the tables were produced.

The same listing can occur in several Apple keyword responses. All 322 appearances remain in the occurrence table, while the listing table uses its first observation under the frozen keyword order. That policy is deterministic and avoids silently mixing values from later observations. Refreshes create a new raw run; they do not overwrite this one.

The automation is an explicit command-line workflow: fetch, parse, review identities, rank, verify, then report. No recurring task was scheduled. Google search endpoints, batchexecute RPCs, individual reviews and detailed Data Safety pages were not crawled. The current robots file disallows automated Play search and RPC paths, and the repository's ethics instructions prefer permitted access. Public product-page retrieval was used after checking robots rules. These checks are operational access controls, not a claim of blanket legal permission. [3,4]

## 7. Policy reachability trial

All 23 captured Play policy URLs entered a separate reachability check. Each provider's robots file was checked first; denied or unavailable rules prevented retrieval. A missing robots file (404) was treated as no robots restriction. These are transport observations only, not verified inclusion decisions.

| Policy retrieval outcome | Count |
| --- | --- |
| HTTP_200_content_unverified | 20 |
| robots_denied_or_unavailable | 3 |

The policy-link check preserves the listed URL and any final redirect URL. A returned HTTP 200 can be an error template, consent page or JavaScript shell. For example, the MAXX policy response was only 765 bytes, which warrants content inspection. Automated access failures do not establish that a human cannot reach the policy. The Apple API did not supply policy URLs in the fields used here, so those policy checks remain pending. No app was marked policy-eligible merely because it had a link or a 200 response.

## 8. Embedded install counts and the reach question

The Play integer conventionally named realInstalls was available in this run's public HTML without login or payment. Clue returned 70,425,176, alongside the displayed 50.000.000+ band. The scraper did not estimate the integer; the parser copied it from the returned embedded data.

| Play app | Embedded count | Displayed band |
| --- | --- | --- |
| Google Fit: Aktivitätstracker | 369,725,740 | 100.000.000+ |
| Flo Zyklus- & Periodenkalender | 206,749,524 | 100.000.000+ |
| Schrittzähler & Pedometer | 89,461,128 | 50.000.000+ |
| Clue Perioden Kalender | 70,425,176 | 50.000.000+ |
| BetterMe Well-Being Coach | 45,765,847 | 10.000.000+ |
| Periodenkalender - Zyklus | 33,153,880 | 10.000.000+ |

These figures are suitable for testing a clearly named embedded-install-count proxy. Their exact counting definition, update schedule and user deduplication are not established by the public field. They are not verified German downloads, active users or affected people. No Apple equivalent was inferred. The separate comparison file ranks numerically passing Play listings by this proxy and preserves the average-rating order alongside it.

Changing the primary sampling rule to installs would require a recorded protocol amendment before main collection: define the platform coverage, geographic scope, observation period, metric, tie-break and missing-data treatment. Retaining this proxy alongside ratings now allows that decision to be made from actual data without silently rewriting the proposal. An Android-only install ranking would change the study's two-store scope.

## 9. Quality checks and reproducibility

Four automated logic tests passed: embedded-number preservation; rejection of an absent dataset; rejection of an impossible install lower bound; and correct cross-store weighting, deduplication and rejection of incomplete final eligibility. The audit verified 89 response hashes and unique IDs for all 202 captured listings. The 50 working-set identifiers are unique under the current provisional mapping. These checks validate the pipeline's mechanics, not the correctness of all methodological judgements.

The exact saved response can reproduce the derived observation and ordering. Repeating a live request later may produce different listings, scores or positions; reproducibility therefore rests on versioned inputs and archived evidence, not an expectation that the live stores never change. The raw directory is Git-ignored and must be backed up with the rest of this folder. It is kept here, rather than in the repository's usual raw-data location, to satisfy the requested self-contained trial folder.

## 10. What remains before a final sample

1. Capture the prescribed 38 store-UI search sessions and their first 20 organic positions, or formally amend the protocol to a documented API-based frame. Do not retroactively label this trial's sources as native-store results.
2. Resolve all product matches and same-provider duplicates; verify and capture both store counterparts. Preserve excluded counterparts as observations even when they do not contribute to the score.
3. Review tracking relevance, interface language, German installability, policy content and DiGA status with dated evidence. Distinguish exclusion, missing information and retrieval failure.
4. Apply the frozen ranking to the verified frame. Retain all eligible candidates and report any stratum shortfall rather than lowering thresholds after inspection.
5. Freeze the document sample, then choose the five-app coding pilot and the 12 distinct walkthrough apps using the proposal's alternating-platform rule. Keep pilot providers and documents out of the later validation set.

These tasks are represented by the review registers; they are not hidden inside a completed-looking sample file. `final_sample.csv` is intentionally empty. No final inclusion decision or study finding is claimed for the 50 products below.

## 11. Provisional working set

The tables below demonstrate the target allocation and rating calculation on the collected trial candidates. Both eligibility and product identity may change after review. Store labels show captured listings, not the full platform availability of the product. Full IDs, source URLs, scores, counts and pending checks are in `trial_working_set.csv` and its JSON equivalent.


### Fitness working set

| Rank | Product | Store(s) | Score |
| --- | --- | --- | --- |
| 1 | Alpha Progression Gym Tracker | iOS | 4.8995 |
| 2 | Hevy - Gym Tracker Workout Log | iOS | 4.8868 |
| 3 | Pedometer & Step Counter | iOS | 4.8686 |
| 4 | Strong Workout Tracker Gym Log | iOS | 4.8242 |
| 5 | 30 Day Fitness at Home | iOS | 4.8235 |
| 6 | Pacer Pedometer: Step Counter | iOS | 4.8200 |
| 7 | GAINSFIRE Workout Tracker | iOS | 4.8102 |
| 8 | Home Workout - No Equipments | iOS | 4.8003 |
| 9 | RepCount - Gym Workout Tracker | iOS | 4.7917 |
| 10 | WeightBuddy: Calorie Tracker | iOS | 4.7902 |
| 11 | Schrittzähler - Pedometer | Play | 4.7900 |
| 12 | WeWard - The Walking App | iOS | 4.7897 |
| 13 | Bevel: AI Health Coach | iOS | 4.7722 |
| 14 | Workout for Women: Fit at Home | iOS | 4.7702 |
| 15 | GymBook ・ Strength Training | iOS | 4.7665 |
| 16 | Macadam: Step Counter, Rewards | iOS | 4.7638 |
| 17 | Six Pack in 30 Days: Core, Abs | iOS | 4.7621 |
| 18 | Instant Heart Rate: HR Monitor | iOS | 4.7616 |
| 19 | Pedometer by ITO Technologies | iOS/Play | 4.7581 |
| 20 | Eatrack: Food Tracker | iOS | 4.7448 |
| 21 | Gymondo: Fitness Workout Plans | iOS | 4.7398 |
| 22 | Oura | iOS | 4.7348 |
| 23 | Welmi - Calorie Counter & Diet | iOS | 4.7297 |
| 24 | Workout for Women: Fitness App | iOS | 4.7258 |
| 25 | Calorie Counter by fatsecret | iOS | 4.7256 |
| 26 | Zumba - Tanzen zu abnehmen | Play | 4.7200 |
| 27 | Nike Training Club | iOS | 4.7168 |
| 28 | StepUp Pedometer Step Counter | iOS | 4.7147 |
| 29 | StepsApp | iOS/Play | 4.6912 |
| 30 | Sleep Tracker & Sound by Remly | iOS | 4.6716 |

### Fertility working set

| Rank | Product | Store(s) | Score |
| --- | --- | --- | --- |
| 1 | Period & Cycle Tracker | iOS | 4.9051 |
| 2 | Femometer - Fertility Tracker | iOS | 4.8508 |
| 3 | My Calendar by SimpleInnovation | iOS/Play | 4.8367 |
| 4 | cyclotest Periodenkalender App | Play | 4.7525 |
| 5 | Periodentracker und -rechner | Play | 4.7407 |
| 6 | Cycle Tracker: Period Calendar | iOS | 4.7083 |
| 7 | Stardust Period Tracker | iOS | 4.7036 |
| 8 | Period Tracker My Cycle | iOS | 4.6860 |
| 9 | Maya - Period & Health | iOS | 4.6630 |
| 10 | HiMommy: Pregnancy & Period | iOS | 4.6537 |
| 11 | Lively - Period Tracker, Cycle | iOS | 4.6485 |
| 12 | Flo | iOS/Play | 4.6389 |
| 13 | urbia Eisprungkalender | iOS | 4.6327 |
| 14 | Life - Period Tracker Calendar | iOS | 4.6220 |
| 15 | Ovulation Tracker By Premom | iOS | 4.6193 |
| 16 | Perioden-Tracker & Eisprung | Play | 4.6111 |
| 17 | Period Tracker by GP Apps | iOS/Play | 4.6005 |
| 18 | Cycles: Period & Cycle Tracker | iOS | 4.5665 |
| 19 | Clover | iOS/Play | 4.5350 |
| 20 | Clue | iOS/Play | 4.2730 |


## 12. Sources and audit trail

[1] JoMingyu, google-play-scraper, pinned source ce1df6d67e6d8c39826daac2f668808fc025f284: https://github.com/JoMingyu/google-play-scraper/blob/ce1df6d67e6d8c39826daac2f668808fc025f284/google_play_scraper/constants/element.py

[2] Apple, iTunes Search API documentation, accessed 11 October 2026: https://performance-partners.apple.com/search-api

[3] Google Play robots.txt, archived in this run: https://play.google.com/robots.txt

[4] Google Terms of Service and Google Play Terms, German context, archived in this run: https://policies.google.com/terms?hl=en&gl=de and https://play.google.com/intl/de_de/about/play-terms/index.html

[5] BfArM DiGA directory, designated verification source; per-app checks remain pending: https://diga.bfarm.de/de/verzeichnis

Internal authority: `03_Thesis/proposal/proposal.tex`, Sampling paragraph beginning at line 217; `04_Study/App-Sample/sampling_protocol.md`; `04_Study/Ethics/README.md`. The proposal snapshot, protocol, seed list and decision file are included in this folder. Acquisition run: 20261011T135045038162Z.
