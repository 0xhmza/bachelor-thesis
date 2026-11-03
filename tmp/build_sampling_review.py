"""Create assessment artifacts only; never edits thesis or collection files."""
from pathlib import Path
import json, re, shutil, html, sys
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'00_Admin/Reviews/Sampling-Peer-Review_2026-10-28'
OUT.mkdir(parents=True,exist_ok=True)
AUD=ROOT/'tmp/sampling-peer-audit-2026-10-28'

# IDs are shared by the detailed and brief versions, preventing omitted findings.
F=[]
def finding(id,severity,title,brief,detail,evidence,required):
 F.append(dict(id=id,severity=severity,title=title,brief=brief,detail=detail,evidence=evidence,required=required))

finding('F01','CRITICAL','Selected cross-store identities are wrong',
 'Nike Run Club is paired with Nike Training Club on iOS; BabyCenter is paired with What to Expect. Five evidence-backed pairing corrections leave the selected providers and order unchanged, but change two selected iOS IDs, the candidate total (1,365 to 1,364), calibration pairs (116 to 117), and c (0.0895807 to 0.0896263). Provider stability does not make the selected products correct.',
 '''The matcher accepts a shared first word of at least three characters when the normalized provider agrees, and greedily takes the available Apple listing with the largest rating count. This is a product-identity error, not a harmless spelling issue. In selected row 25, Play com.nike.plusgps is paired with Apple 301521403, whose archived name is Nike Training Club and bundle is com.nike.niketrainingclub. Nike Run Club is Apple 387771637, bundle com.nike.nikeplus-gps. Selected row 17 pairs com.babycenter.pregnancytracker with Apple 289560144, Pregnancy Tracker App - WTE, bundle com.ryanbond.PregnancyTracker. BabyCenter is Apple 386022579, bundle com.babycenter.mypregnancytoday. Shared publishing accounts do not establish the same product.

The same rule reverses the other Nike pair and pairs a men's weight-loss app with a women's product. The five-reference-case scenario is an isolated diagnostic, not an adopted sample correction or a complete identity certification. The unchanged provider order hides a real change in what iOS app would be collected and inspected. BabyCenter's observed Apple contribution would be based on 6,928 ratings rather than WTE's 648; the selected Apple minimum of 648 consequently also requires regeneration.''',
 'scripts/app-ranking/v004/rank.py: same_app, candidates; v004/output/selection.csv rows 17 and 25; archived Apple IDs 289560144, 386022579, 301521403, 387771637; evidence.json: scenarios[0].',
 'Review product identity for every matched pair using product-specific evidence; preserve explicit decisions, add negative regression cases, and regenerate the sample, score summaries and all sensitivity results together.')

finding('F02','MAJOR','Unobserved Play feedback is silently treated as zero',
 '240 of 645 Play listings omit both review and rating counts, while five contain an explicit review count of zero. load() collapses these distinct states to zero. Missing-count candidates may never reach screening; observed counts for the selected apps do not prove the sample is unaffected.',
 '''The collector deliberately disables parser fallback values, retaining missingness by omitting failed or unavailable fields. The ranking immediately discards that distinction through row.get(...) or 0. Missing reviews affect 37.2% of collected Play apps, so this is not an isolated edge case. The missing group includes Periodenkalender Paula (3,540,694 embedded worldwide installs) and iMumz (2,166,851). Worldwide installs do not reveal German reviews; they show why a missing German observation cannot establish no German feedback.

The archived data cannot distinguish a valid absence of regional feedback from a schema problem or other extraction failure. The 47 selected candidates all have observed inputs for their present listings, but a ranking audit must also assess candidates that were suppressed before selection. No defensible upper bound on the missing candidates' possible German counts is documented. The existing sample therefore cannot be certified insensitive to the missing-data policy.''',
 'v004/rank.py: load; frozen-equivalent Play JSON and page cache; evidence.json: missing_play_reviews, explicit_zero_reviews; missing-play-counts.csv.',
 'Retain missing, observed zero and absent counterpart as separate states; establish field semantics and an evidence-backed missing-data rule, then rerun or bound its selection impact.')

finding('F03','MAJOR','The reported 0.95 correlation is inflated by imputed zero pairs',
 'The reported Spearman rho 0.9490524 uses 644 Play candidates after zero substitution. Restricting the same calculation to the 404 candidates with both counts observed gives rho 0.8167324. The 0.95 is reproducible but is not the observed-count association suggested by the prose.',
 '''Both missing fields become zero for the same 240 listings. This creates a large artificial tied block at the bottom of both rankings, increasing their agreement. The complete-observation calculation excludes Samsung Health just as the main candidate frame does, and retains actual recorded zeros. It is therefore n=404, not 405 or 644.

The corrected observation-only coefficient is still positive and substantial. The issue is the interpretation and missingness disclosure, rather than a claim that the measures have no relationship. Neither correlation validates German user reach or resolves selection bias. Any replacement analysis should state the population, missing-value policy, sample size, and whether the statistic is Spearman, rather than presenting an unlabeled correlation as general validation.''',
 '03_Thesis/chapters/05_results.tex:101-104; v004/rank.py: load, spearman, report; evidence.json: observed_correlation.',
 'Report the observed-count association and disclose the imputed calculation separately if retained; do not use the larger coefficient as evidence that missing values are harmless.')

finding('F04','MAJOR','The documented current ranking command cannot run unchanged',
 'v004 config points to absent 05_Data/raw/app-sample_2026-10-25 files and an absent processed-data destination. The data now live under 05_Data/App Sampling/26. Oct. Exact reproduction succeeded only with a temporary configuration that redirected inputs and every output.',
 '''Both configured input files are missing in the audited checkout. This breaks the executable chain from documented command to results even though the source data still exist. The configured processed destination also differs from the committed sample's actual location, so an adapted rerun could create a second sample tree unless its output paths are deliberately reconciled.

The reviewer did not repair the configuration or populate the old paths. In the isolated replay, the same production ranking code received the relocated files and wrote all CSV, JSON, dataset and table outputs inside the ignored audit folder. All eight comparisons passed: report, selection, exclusions, sensitivity rows, processed apps.csv, and the three generated tables. This establishes conditional computational repeatability, while leaving the documented entry point broken.''',
 'scripts/app-ranking/v004/config.json; scripts/app-ranking/README.md; evidence.json: configured_paths, actual_inputs, replay.',
 'Reconcile one canonical input/output location and test the documented command from a clean checkout or supplied artifact package.')

finding('F05','MAJOR','Freeze documentation and the current data layout have separated',
 'The current tree lacks the raw hash README, sampling protocol and processed-sample README referenced throughout the project. All five relocated sampling files match the hashes recovered from the preceding commit. This supports unchanged bytes, but current documentation no longer provides a working freeze/backup trail.',
 '''The historical manifest was recovered read-only with git show HEAD^:05_Data/raw/README.md. The App Store JSON, final Play JSON, page cache, pilot JSON and progress log all match its recorded SHA-256 values. There is no evidence here of byte alteration during the move. The distinction matters: missing present-day provenance documentation should not be described as demonstrated raw-data corruption.

The files are now tracked under a path outside the old raw-data exclusion rule. AGENTS.md and several READMEs still say that raw collections are ignored and must be separately backed up. The historical protocol is recoverable from Git, but absent from the current working tree. These are assessable packaging and governance failures. A durable snapshot must identify its actual location, contents, hashes, generating versions and access/backup policy in the version being reviewed.''',
 'Current git ls-files; absent 05_Data/raw/README.md and 04_Study/App-Sample/sampling_protocol.md; HEAD^ historical manifest; evidence.json: manifest.',
 'Restore an accurate current manifest and protocol through the normal author workflow; distinguish relocation from data mutation and document the intended tracking and backup policy.')

finding('F06','MAJOR','Original HTTP evidence is incomplete',
 'The final Play JSON retains only the last request. Across retained collector JSONs, hashes exist for 104 of 645 product-page IDs; 541 lack a retained response hash. Parsed rows and capture times survive, but original response bodies are not available for independent reparsing.',
 '''The append-only cache stores parsed rows and timestamps, not the response body or its hash. A cache-reusing execution starts a fresh process-local requests dictionary and does not recover earlier HTTP metadata. Consequently, a complete progress log is evidence that cached or new records were processed, not that all 645 pages were fetched again. All 645 cache rows reproduce the final parsed records, which is a meaningful preservation check but not validation of the upstream parsing.

The App Store collection records 49 response hashes, but the raw API response bodies are likewise not retained here. Hashes attest to a particular body only if that body or independently verifiable archival evidence is available; a hash alone cannot show that the parser read the correct field. Existing missing HTTP hashes cannot be reconstructed honestly by hashing the parsed JSON.''',
 'googleplay-scraper/v004/scraper.py: fetch and cache entry; retained v004/output/*.json; evidence.json: cache; App Store requests mapping.',
 'For future captures preserve source bodies where permitted, per-row URL, capture time, response hash, status/final URL and parser version. Describe the historical gap explicitly rather than claiming full source-level reproducibility.')

finding('F07','MAJOR','Country-sensitive review counts are not fully semantically validated',
 'The embedded Play review field varies with country in the documented probes, but the original comparison responses and scratch scripts are not preserved. Official country-specific rating documentation does not identify the undocumented integer as a complete German written-review total.',
 '''The project's DE/AT/US and language checks are plausible evidence that the integer is country-sensitive, and the distinction from worldwide rating counts is methodologically useful. However, D2 explicitly says that the initial storefront-check scratch scripts are not in the repository. The retained final German sample cannot reproduce a cross-country or cross-language experiment by itself.

Google's announcement concerns ratings seen by users registered in a country and device-specific presentation; it does not document the exact positional field consumed by google-play-scraper. A variable's response to gl is evidence of regional behavior, not sufficient evidence of exhaustiveness, historical period, deduplication or precise event meaning. Current live pages would not by themselves validate what the archived parser extracted on 24-25 October. The missing-value pattern makes this validation especially consequential. Source: https://android-developers.googleblog.com/2021/08/making-ratings-and-reviews-better-for.html''',
 'D02 storefront checks and endpoint inventory; googleplay-scraper/README.md field basis; scraper FIELDS mapping; official Google announcement.',
 'Preserve a reproducible country/language validation fixture, identify the exact upstream field, distinguish empirical inference from platform documentation, and qualify the measurement name until its semantics are established.')

finding('F08','MAJOR','The cache can bypass storefront and parser freshness safeguards',
 'A network-free execution of the unchanged v005 main function reproduced all 1,139 stored result rows. Requesting US/en with the same cache then returned the identical German rows while labeling the output US. Cache keys contain package ID only; cached failures also remain failures unless manually removed.',
 '''Both sampling-era v004 and shortened v005 accept an existing entry solely because its app ID is in the cache. They do not validate country, interface language, schema version, collector version, expiry or response provenance. fetch()'s storefront test runs only on new requests, so it does not protect cache reuse. The synthetic US replay demonstrates a latent correctness defect without making live requests. It does not establish that the historical German collection was contaminated by another country.

The same cache policy reuses an error entry indefinitely; the loop does not retry an ID already present with error rather than row. The historical final collection has no unresolved page errors, so this hazard should not be misreported as a current missing-page count. HTTP failures have a timeout, but persistent failure records and lack of robust retry/backoff in the Play collector can matter during a fresh rerun.''',
 'v004/v005 cache-loading and if-ID-not-in-cache loops; diagnostics.json: collector_replay.',
 'Key or validate caches by storefront, language and parser/schema version; distinguish successful records from retryable failures; retain immutable historical caches separately.')

finding('F09','MODERATE','Endpoint coverage and ordering are incompletely validated',
 'The frame is the collectors\' first-page/API output, not a verified native-store ranking or a complete census. Sponsored-result handling and all search-card types are not validated. Equal nominal depth does not establish equal coverage across two different interfaces.',
 '''The Apple collector preserves API position before iPhone filtering, so the first 30 API positions can yield fewer than 30 eligible device-compatible results. The Google parser adds highlighted results, takes one regular carousel and stops. The supplied metadata show no missing IDs in the observed parsed frame, but cannot expose cards omitted before a row was created. Original search bodies are unavailable for an independent completeness comparison.

The thesis already acknowledges that endpoint order was not checked against the native store order; this is a strength and should be retained. The deeper App Store check is asymmetric and cannot demonstrate Play search saturation. The historical protocol contains proposed ad exclusion language, whereas the current collectors do not record ad status. Absence of ad markers in the parsed data is not proof that sponsored placements were absent.''',
 'appstore v007: API Position and supportedDevices filter; Play v004/v005: search; Methodology Search; historical protocol Search and matching rules.',
 'Define the endpoint-based frame precisely, validate retained versus omitted cards on archived fixtures, and either operationalize ad handling or disclose it as unmeasured.')

finding('F10','MAJOR','The common popularity scale is conditional, not independently validated',
 'The formula is mathematically coherent under its explicit model; there is no demonstrated arithmetic error or automatic double weighting. Its assumptions about app-specific platform use and feedback rates remain unvalidated. StatCounter measures web page views, not unique app users.',
 '''Let v_i=q_A N_Ai and r_i=q_I N_Ii, with platform-specific feedback propensities q_A and q_I. If a typical matched app has N_Ai/N_Ii=s_A/s_I, then median(v/r) times s_I/s_A estimates q_A/q_I, and v+c r is proportional to N_Ai+N_Ii. Thus the factor direction has a defensible derivation. A rigorous review should not invent a double-weighting mistake that the stated model does not imply.

The empirical weakness is that app user splits and feedback behavior can vary substantially by domain, price, age and prompts. StatCounter's own methodology describes page-view-based internet usage. Using it to approximate the user distribution of health apps adds an external validity assumption, not a measured correction. The equal-platform variant changes five providers, demonstrating dependence on the conversion rule. No actual German active-user or download benchmark was supplied. Source: https://gs.statcounter.com/faq''',
 'v004 calibration; Methodology:444-464; D02 simplified model; main and equal-platform sensitivity outputs; StatCounter FAQ.',
 'Present P as a study-specific purposive ordering, retain the model derivation and assumptions, and validate against independent German reach data if making stronger popularity claims.')

finding('F11','MODERATE','Calibration heterogeneity and uncertainty are underreported',
 'Of 116 positive calibration pairs, 57 are recorded eligible, eight excluded and 51 unscreened. Their review/rating ratios range from 0.0114 to 26.05, with quartiles 0.0843 and 0.6107. One median hides substantial variation and includes unverified identities and off-domain products.',
 '''Calibration before eligibility is documented and therefore not a secret implementation mismatch. It still needs justification: games, content tools and unscreened apps may have different review propensities from the intended health-tracker population. Multiple products from one provider can also enter calibration even though selection later limits providers. The known identity errors contaminate some ratio observations, even when their effect on the median is small.

As a diagnostic only, 2,000 seeded resamples of the current 116 ratios gave a 2.5th-97.5th percentile factor range of 0.06308-0.12829. Across 200 sampled factors, provider changes ranged from zero to four, with 15 runs reaching unscreened candidates. These are not population confidence intervals: the frame is purposive, the pair errors remain, and provider dependence is not adjusted. They illustrate uncertainty that one fixed alternative weight does not summarize. Restricting to already-screened eligible positive pairs gives c=0.09167, which does not settle representativeness of that subset.''',
 'evidence.json: calibration; diagnostics.json: bootstrap, calibration_groups; seed 20261028.',
 'After identity repair, assess calibration by relevant domain/provider groups, report uncertainty and missingness, and fully screen every candidate reached by any adopted robustness analysis.')

finding('F12','MAJOR','Missing counterpart discovery creates differential score truncation',
 'A listing absent from a store\'s top-30 frame contributes nothing even if the app exists there. Cross-platform products with one undiscovered listing can therefore rank below equally popular products found in both stores. "Store only" must mean found only in this frame.',
 '''The thesis correctly says that no observed counterpart is not proof of no counterpart. However, the computational consequence is more than terminology: the score is a lower-information sum for poorly retrieved apps. Search discoverability can therefore change the ranking through two mechanisms, entry into the frame and availability of the second score contribution.

The reported 33 both-store, eight Play-only and six Apple-only selected products describe the matched search frame, subject also to F01. They do not establish platform exclusivity. Targeted lookup of known candidate products is a possible way to reduce missing counterpart contributions, but would be a methodological change requiring a documented prospective rule and new processing version. Sensitivity analyses that drop keywords also alter matching and recalibrate, so their differences combine frame and scoring effects.''',
 'v004 pool, candidates, build; Results:151-158; Appendix C Listed in definition; D02 missing counterpart clarification.',
 'Report frame-specific presence consistently, assess counterpart discovery before stronger cross-platform claims, and separate the mechanisms changed in sensitivity interpretations.')

finding('F13','MAJOR','Screening remains an unadjudicated AI first pass',
 'All 275 screening keys are unique and exist in the collections; 156 eligible and 119 excluded reproduce. These structural checks do not validate eligibility. The thesis still says every AI-prepared decision awaits author review; the CSV has no reviewer, date, criterion-level outcomes or evidence spans.',
 '''The current no-pending result means that the program encountered a row with a decision. It does not mean an independent person reviewed it. Many reasons are short paraphrases; some assert that a listing states no recording when the text merely does not mention it. Those are different evidentiary standards. A single final exclusion code also does not preserve which of the other four criteria were checked or passed.

The review inspected the whole screening sheet structurally and all recorded exclusion reasons, then checked selected and high-risk descriptions in detail. It did not recreate 275 independent human eligibility judgments or install every candidate. Claiming perfect screening would exceed that evidence. In particular, listing-based eligibility is an operational proxy for capability, not a functional test. A failure of the listing to establish tracking should be distinguished from evidence that tracking does not exist.''',
 '04_Study/App-Sample/screening.csv schema; Results:57-59; v004 decision/select; evidence.json: screening.',
 'Complete and date author adjudication, retain quoted criterion-specific evidence and uncertainty, and independently review high-impact inclusions/exclusions before calling the sample final.')

finding('F14','MAJOR','Kinomap\'s exclusion reason is contradicted by its archived listing',
 'Apple 611177969 is excluded as not recording user data. Its archived German description explicitly says that the app records individual training sessions and describes exporting activities. Making Kinomap eligible does not change the main selection because its score is below the cutoff; the screening error still matters.',
 '''The record says interactive training videos; listing states no recording of the user's data. Under the archived Freies Training heading, the description explicitly states that individual sessions are recorded so users can maintain an overview. It also mentions synchronization of activities with Strava and adidas Running. This directly contradicts the stated factual rationale under E1.

This finding need not decide every other criterion to establish that the recorded reason is unsupported. Its score is approximately 2,066 versus the 3,819 main cutoff. An isolated E1-eligible scenario left the main provider set and order unchanged, which bounds this particular main-selection effect. It does not excuse the record or prove no sensitivity output could be affected; all relevant variants should be regenerated after the author adjudicates the app.''',
 'screening.csv apple/611177969; archived App Store Description, Freies Training and Andere Funktionen; evidence.json Kinomap scenario.',
 'Correct the rationale through recorded author adjudication and rerun the affected analysis rather than silently relabeling the old screening record.')

finding('F15','MAJOR','Lady Pill Reminder is an unresolved cutoff-changing boundary case',
 'The listing says users can retrieve how many pills they have already taken during the current cycle. The record categorically says no recording. Whether this means user-confirmed intake or a schedule-derived count is unresolved. If eligible, Lady Pill Reminder enters and Sleep Monitor leaves.',
 '''An intake record over time is potentially relevant to the stated reproductive-health boundary. A reminder generated only from a fixed schedule might fail that rule. The archived sentence alone does not distinguish these implementations, so the strict conclusion is that the current categorical rationale is too strong, not that eligibility is already proved.

The candidate has 4,742 observed German reviews, above the main cutoff. Changing only this screening decision in memory substitutes one provider in the 47 and changes 11 order positions. This is a concrete sample-changing ambiguity. It should be resolved by a consistent operational rule and appropriate functional/documentary evidence, then applied to comparable medication and contraception reminder apps rather than adjudicating only the convenient cutoff case.''',
 'screening.csv play/com.baviux.pillreminder; archived Play Description; main-cascade.csv; evidence.json Lady Pill Reminder scenario.',
 'Adjudicate confirmed intake history versus scheduled reminders with retained evidence; apply the same rule to comparable apps and regenerate sample and sensitivities.')

finding('F16','MAJOR','The mental-health boundary needs consistent evidence',
 'Headspace is supported by explicit progress/reflection wording, so its inclusion is not disproved. Calm is excluded for recording only meditation, although its listing also mentions saving meditation and sleep sessions to Apple Health. That may describe content sessions rather than physiological sleep. A Calm-eligible scenario replaces Sleep Monitor.',
 '''Headspace's archived Apple description expressly mentions tracking mental health, documenting reflections and progress, which is more evidence than a meditation-only label suggests. A fair review must retain that support. Calm lists time spent meditating and daily streaks, and mentions saving meditation and sleep sessions. Those sessions are not automatically evidence of measured sleep, so the present record should not be reversed without clarifying what counts as health tracking.

The operational boundary among recording wellbeing/reflection, recording activity completion and measuring mood or sleep remains insufficiently explicit for consistent exclusion of Calm, 7Mind and Insight Timer. The isolated Calm scenario changed both its Apple and Play decisions to eligible and replaced Sleep Monitor, with no pending candidates. This is a diagnostic, not an adopted classification. The relevant question is consistent application of a rule across all mental-health candidates, not whether one popular app seems desirable.''',
 'Archived Headspace Apple/493145008 and Calm Apple/571800810 descriptions; corresponding screening rows; diagnostics.json: calm_counterfactual.',
 'Define the recording boundary before adjudication and apply it to all similar apps, preserving uncertain and proxy-based judgments.')

finding('F17','MODERATE','The DiGA exclusion lacks its required verification record',
 'Oviva Direkt Apple 1556652646 is excluded under E5 while its reason still says confirm in the BfArM directory. Prescription/reimbursement language is a trigger for checking the registry, not the retained check itself.',
 '''The methodology requires registry confirmation. The screening row records the listing-level reimbursement signal and explicitly leaves confirmation outstanding. No dated registry capture or exact entry identifier is linked from this row. The classification may be correct; the audit finding is that the prescribed evidence trail is incomplete.

It is also necessary to distinguish the exact Oviva Direkt product from other apps of the same provider. A later web page or a provider-level reimbursement statement would not establish the exact historical registry status of the selected product. This review makes no independent legal or regulatory determination and does not infer that E5 was substantively wrong.''',
 'screening.csv apple/1556652646; D03 E5 operational check; Methodology:363-366.',
 'Retain the exact registry identity, date/status and documentary evidence for the exclusion; clearly label unresolved checks.')

finding('F18','CRITICAL','The pilot and validation allocation is infeasible as written',
 'The ranked sample has four cycle and two pregnancy apps: six reproductive-health apps. The plan requires two reproductive pilot apps plus five different validation apps, with pilot apps/providers excluded from validation. Seven are needed. No allocation satisfying the stated rules exists under the reported primary categories.',
 '''The pilot specifies five apps, three fitness and two fertility. Validation specifies ten apps, five per domain, from providers/documents not used in the pilot. Even if every pregnancy app is treated as reproductive/fertility, only six candidate apps are available for that domain. Once two enter the pilot, four remain, below the required five. If pregnancy is not included in fertility, the shortage is larger.

The three preinstalled apps do not supply additional reproductive-primary apps. Some multi-function apps might have reproductive features, but no explicit domain mapping or disjoint allocation has been supplied that permits counting them in this stratum. The honest conclusion is infeasibility under the stated classification, requiring a revised justified design. Quietly reusing a pilot app in validation would undermine the claimed separation between instrument development and validation.''',
 'Results:154-156; Methodology Pilot and Validation and Missed Mentions; v004/output/report.json categories; D03 Consequences.',
 'Choose and document a feasible allocation before pilot selection; preserve independent validation and explain any change in size, stratification or domain definition.')

finding('F19','MAJOR','The expanded sample is not aligned with downstream domain plans',
 'Mood tracking was added to meet the supervisor\'s guidance, but harm trees, walkthrough strata, pilot and validation still largely assume fitness and fertility. The two mood apps and the multi-function companion have no complete mapping to those plans. A no-quota sample does not itself define an analysis taxonomy.',
 '''The supervisor explicitly requested mental-health trackers and broader consideration of sleep and specialized tracking. The current search adds mood and happiness and reports two mood apps. D03 itself recognizes the two-domain consequences as open. Nevertheless, the methodology defines separate fitness/fertility harm trees, six walkthroughs per domain and five validation apps per domain without a complete mapping for the sampled categories.

Sleep, diet, activity and heart-rate tracking might reasonably be grouped under a broader physical-health domain, but that taxonomy has to be stated and justified. Assigning all non-reproductive apps to fitness would hide substantively different mental-health pathways. Broad keyword coverage also does not establish comprehensive coverage of depression, anxiety or specialized chronic-disease tracking; the chosen source vocabularies delimit this study.''',
 '13 October organized notes sections 1 and 4; D03 Consequences; Methodology App Walkthroughs, Reference Harm Trees, Pilot and Validation.',
 'Define app-to-domain and multi-function mappings and align harm applicability, walkthroughs and validation with them; state the search-domain limits.')

finding('F20','MODERATE','Provider independence and repeated-source handling need qualification',
 'The 47 ranked apps have unique provider keys, but adding Apple Health and Apple Fitness plus Samsung Health gives 50 apps from 49 provider keys. One account/normalized name/shared domain is an operational grouping, not proof of independent corporate entities or unique policies.',
 '''The deliberate two-app Apple exception is defensible if it is explicitly an exception. It prevents describing the full sample as 50 independent providers. Provider normalization removes legal/regional words, while aliases and domain reviews handle some further spellings; these checks improve consistency but do not verify corporate ownership or cross-provider policy duplication. The main reached set has no shared-domain flags under the implementation, which is narrower than proving no organizational dependence.

The pilot evidence for one policy among ten Leap products strips query strings from policy URLs. A pkg query parameter may only select a product-specific view, but stripping it does not itself establish identical text, controller or scope. The provider-diversity rationale can remain useful without claiming that every additional app of the provider has identical communication. Downstream coding and resampling should track unique documents as well as provider keys.''',
 'v004 config preinstalled_table, provider_key and shared_domains; processed apps.csv; sampling-checks/v002/pilot_table.py: policy; Appendix C developer-pilot explanation.',
 'State the 49-provider total and Apple exception, audit shared document identities/scopes, and use the actual dependence structure in analysis and validation.')

finding('F21','MODERATE','Preinstalled-app coverage is not established to the stated current-phone rule',
 'Apple/Samsung are a plausible purposive group, but D6 relies partly on secondary reporting and lacks a model/OS/market-specific preinstallation matrix. Failure to identify a Xiaomi tracker is not proof that none ships on current global phones, so the claimed identical 10%/80% alternatives remain conditional.',
 '''The methodology requires that an eligible tracker ship on the vendor's current phones without a download. Store availability, eligibility and historical availability without a wearable are separate propositions. D6 describes Apple's iOS 16 behavior, Samsung listings and unsuccessful identification of a global Xiaomi preinstalled tracker, but does not retain a current model-level observation or official preinstallation table covering the German market.

Vendor page-view share divided by a platform page-view share can compare vendors within an assumed platform, but does not measure the fraction of devices on which an app is actually installed, enabled or used. The claim that alternative vendor coverage rules produce the same three apps depends on the unresolved Xiaomi premise. This review does not assert that a fourth app must be added; it requires evidence adequate to the rule being stated.''',
 'D06 Evidence and Would change if; Methodology:496-521; Results:71-85.',
 'Retain dated official vendor/model/OS/region evidence or clearly narrow the preinstalled claim; report uncertainty in alternatives rather than treating an unsuccessful search as verified absence.')

finding('F22','MAJOR','Sensitivity outcomes conceal product-level failures',
 'The depth-200 variant pairs Fitbit with Google Search and Google Fit with Chrome. Their screened exclusions can then exclude tracker candidates. Counting only changed provider keys hides these mistakes and changes of app, platform listing or within-provider representative.',
 '''This failure is reproducible from the current matcher: Google Health (Fitbit), Play com.fitbit.FitbitMobile, pairs with Apple 284815942 (Google), and Google Fit pairs with Apple 535886823 (Google Chrome). A provider-normalized shared first word is insufficient. The one-store exclusion rule then propagates unrelated off-topic decisions to the tracker. D03 acknowledges these examples, but acknowledgment does not repair the variant.

All 58 stored sensitivity rows reproduce, including the earlier selection comparison. The reported provider differences are valid counts under that implementation; their interpretation as reliable robustness evidence is compromised. The five identity corrections in F01 already show why zero provider turnover can coexist with two different selected iOS products. One-factor-at-a-time checks also do not bound joint effects, missing counts, screening uncertainty or discovery incompleteness.''',
 'diagnostics.json: deep_google_pairs; D03 final operational-check bullet; v004/output/sensitivity.csv; evidence.json replay.',
 'Repair and adjudicate identities across every variant, then report provider, app, listing and order changes separately and state which uncertainties remain untested.')

finding('F23','MAJOR','Tests and finality gates do not enforce the scientific invariants',
 'All 12 v004 tests pass despite known product errors and missing-value collapse. Missing screening rows provisionally count as eligible, and an unfinal run still writes selection/report files before its warning. The old audit targets v003 and hard-codes 114 calibration pairs, so it cannot certify current v004.',
 '''The tests cover positive matching examples, provider skips, aliases and arithmetic, but have no negative Nike/BabyCenter/gender-specific product cases or explicit missing-versus-zero behavior. A candidate with one eligible store decision is accepted even if the other listing was never screened. The final table/dataset gate checks pending rows and unresolved domain pairs, not author adjudication, identity approval, raw hashes or all five eligibility fields.

When pending work exists, selection.csv and report.json have already been written, and main prints a warning without raising an error. Previously generated final tables/datasets may remain. This can leave provisional and older final artifacts side by side. Similarly, write() does nothing for an empty row list, potentially retaining an older nonempty file in an existing output directory. These are latent lifecycle risks, not evidence that the present zero-byte screening/provider-review files contain stale nonempty rows.''',
 'v004/tests/test_rank.py; rank.py: decision, select, write, main output block; scripts/sampling-audit/v001/audit.py.',
 'Add meaningful negative and missing-state tests, schema validation and machine-enforced finality; prevent stale/provisional artifacts from being mistaken for an approved sample; update independent verification to the active version.')

finding('F24','MODERATE','Sample-size precedent is contextual, not an adequacy argument',
 'The cited sample sizes are real: Malki 20, Huckvale 36 and Hutton 64. They support feasibility, not saturation, precision or adequacy for this study\'s full domain/validation plan. Hutton\'s 64 include non-health tracking categories; Malki ranks recent-year reviews rather than this study\'s lifetime mixed counts.',
 '''The original PDFs support the important precedents. Hutton PDF page 5 derives categories from 105 London Quantified Self members, reports 64 apps and includes spending and time keeping as other self-tracking categories. Malki PDF page 4 reports 20 apps and ranks reviews during the preceding 12 months to reduce bias against newer apps. Huckvale PDF page 3 reports 36 apps and a different search-rank design. Robillard PDF page 2 supports free download and repeated personal input. Sunyaev PDF page 3 reports the 0.89 Android ratings/download correlation.

Those papers justify borrowing selected components with transparent adaptation. They do not validate a combined-store conversion factor, a universal first-30 rule, one app per provider, 50 apps across a broader domain or the new downstream allocation. Sunyaev's ratings/download result is not a direct validation of undocumented German written-review counts. The chapter should distinguish literature precedent, practical constraints, supervisor preference and empirical validation.''',
 'Local original PDFs: Malki 2024 p4; Hutton 2018 p5; Huckvale 2019 p3; Robillard 2019 p2; Sunyaev 2015 p3; Methodology sample-size and ranking paragraphs.',
 'State the intended descriptive claims and practical adequacy argument explicitly; explain adaptations and avoid presenting precedent as statistical validation.')

finding('F25','MAJOR','Protocol timing and decision authority need reconciliation',
 'Major ranking and provider rules changed after collection on 25-26 October; D1-D4/D6 remain proposed and D8-D12 include open decisions. The historical protocol simultaneously says fixed before collection and records later revisions. The methodology should not imply complete prospective specification or settled authority.',
 '''Post-collection methodological revision is not automatically misconduct or invalid research. Here the history is largely visible and the ranking rationale changed when the worldwide/market-specific distinction was recognized. That is preferable to concealing the change. The problem is inconsistent descriptions of what was predetermined and which rules remain proposed.

The current Decision Log says a choice is open until supported and confirmed where needed and that methodology does not state open choices. The chapter nevertheless states several proposed choices as operative and retains plans for open D8-D12 matters. The preserved protocol labels version 2 fixed before 23 October while also incorporating later score and preinstalled changes. The scope and timing need a clear versioned account separating pre-collection frame rules, post-collection revisions, exploratory checks and author/supervisor approvals. No claim of outcome-driven manipulation is established by this audit.''',
 'Decision-Log register and introductory rule; D02 History; D03 operational checks; historical sampling_protocol.md header and change log; current Methodology.',
 'Provide one accurate chronology and authority/status table; retain proposed language and open decisions where appropriate and avoid retrospective preregistration claims.')

finding('F26','MODERATE','Results blur distinct denominators and overstate some checks',
 'There are 27 matched candidates with both listings screened across the main frame, but only 22 among the 33 selected matched apps; D3 incorrectly attributes 27 to main selection. Eleven selected both-store apps are decided from one listing. The prose also calls frame presence store availability and turns provider-name/domain checks into broader assurances.',
 '''The actual screening counts are 27 both-screened matched candidates, 38 one-screened matched candidates and 60 with neither listing screened among 125 matched candidates. Selected matched apps are 22 both-screened plus 11 one-screened, totaling 33. This is compatible with the documented one-listing decision rule; it is not evidence that the code secretly demands two decisions. It does expose an incorrect denominator in D03's explanatory note.

Methodology says that where both listings are screened, an exclusion in either excludes the app and that this never happened in the collection. The deep variant's wrong Google pairings contradict an unqualified across-variants reading. Main-frame absence of conflicting decisions does not establish cross-platform equivalence of access, features, price or language. Similarly, the category label multiple is described as one wearable companion in Results; that interpretation should be recorded rather than silently substituting taxonomy labels. F01 also invalidates the present 648 Apple minimum for the intended BabyCenter product.''',
 'D03 operational-check final bullet; evidence.json: screening; all-matched-pairs.csv; Results:115-119,151-159; Methodology:386-391.',
 'Use separate counts for listings, matched candidates, reached candidates, selected apps and providers; reconcile D3 and Results and qualify checks to their actual implementation scope.')

finding('F27','MAJOR','The rest of the methodology is still a plan, with unresolved operational dependencies',
 'The chapter contains explicit literature-search rework, material-scope TODOs, unfinished instruments and open LLM/two-coder decisions. These are not fabricated results, but prevent a claim that the whole methodology is publication ready. The supervisor required two coders; seeking one later or substituting a small supervisor review is not the same procedure.',
 '''The sampling work should not be confused with completed privacy coding or walkthrough results: the substantive Results sections remain placeholders. The chapter honestly uses future tense and retains revision marks. However, its opening is unsure about related provider pages, while Material and Language specifies linked provider pages and a supplementary blog search. Walkthrough protocol setup still has device, OS and language blanks. Reference model, coding acceptance and validation choices require a settled decision record and pilot outcomes.

The literature section names OpenAlex/Semantic Scholar while an inline instruction says to redo the remainder using traditional platforms; much of the detailed procedure is commented out even though literature Results report finalized counts. This review does not audit that literature retrieval pipeline numerically. The relevance here is that methodological decisions and harm trees depend on an unsettled evidence workflow. These items are design incompleteness rather than errors in the reproduced sample counts.''',
 'Methodology introduction, Literature Review, Material and Language, Validation, Ethics; Decision Log D8-D13; 04_Study/Instrument/walkthrough_protocol.md; Results stubs; supervisor notes section 6.',
 'Resolve and freeze the operational design through its decision records before main collection/coding; align material scope, coder roles, instruments and evidence review. Keep unresolved passages visibly provisional.')

finding('F28','MODERATE','Collection-terms and ethics documentation is incomplete',
 'The project acknowledges collection of disallowed search endpoints at the author\'s direction, but the historical terms-check table is blank and the current methodology says terms will be checked before retrieval. No dated completed collection review was located. Robots rules alone are not a legal or ethics determination.',
 '''The scraper READMEs and D02 are candid about robots restrictions. That disclosure should not be omitted. However, an author's instruction to collect and a technical robots file are different from a retained terms assessment or an institutional determination where required. The thesis's future-tense ethics promise is chronologically incomplete for a collection that has already occurred.

The proportionate publication issue is a documented acquisition basis and appropriate handling of any incidental public review snippets in retained pilot data. This audit does not assert a breach of law or that a human-subjects review is necessarily required for public listings. Those questions depend on the actual terms, jurisdiction, data and institutional guidance; the evidence reviewed here does not resolve them.''',
 'D02 Endpoint inventory; scraper READMEs; historical protocol Terms table; 04_Study/Ethics/README.md; Methodology Ethics and Feasibility.',
 'Record what acquisition review was actually performed, by whom and when; resolve any required institutional/terms questions without retroactively presenting an unchecked condition as completed.')

finding('F29','MAJOR','The project\'s own validation infrastructure currently fails',
 'python scripts/check_project.py crashes on missing 01_Literature/README.md, and graphify refresh fails on the same missing file. Neither reports a successful project-wide check. The graph is useful for navigation, but its old semantic assertions cannot establish the state of deleted or moved files.',
 '''These were direct read/check attempts in the audited checkout, not hypothetical failures. Twelve ranking tests passed independently. The checker crash means no 0-error result was obtained; it should not be summarized as a clean project or as a known exact number of remaining errors. The same absent README stops literature_index.update during graph refresh.

The normal artifact package should also identify the exact collection environment, local adapters, dependency versions and commands. The Play parser requirement is pinned to 1.2.7, which is good; a pin alone does not preserve source-response fixtures or the collection-time runtime. Current code plus a historical output does not independently establish the historical environment. The current artifact is recoverable and partially reproducible after input redirection, but not exercisable as documented without intervention.''',
 'Captured check_project.py and graphify refresh tracebacks; v004 tests; googleplay requirements; scripts/thesis_graph.py and literature_index.py.',
 'Restore a runnable check/data package and verify documented commands; report environment and evidence coverage. Do not equate passing narrow unit tests with project or scientific validation.')

finding('F30','MODERATE','Repeated Apple records use an implicit first-observation rule',
 'Twenty-one repeated Apple occurrences disagree with their first metadata observation, including counts and some versions. load() silently keeps the first row while updating search positions. This is deterministic but order dependent and not described as the snapshot-resolution rule.',
 '''The original collection preserves repeated per-query observations, which makes the inconsistency visible. For Fitbit, the first Apple count is 48,117, while a later query has 48,097. Sleep Cycle has 5,778 versus 5,770. Napper appears with different versions and update timestamps; Meditopia also changes version. Caching, update timing or backend variation could explain these records, and they are not evidence of fabrication.

The selection code's setdefault takes its factual metadata from the earliest occurrence in JSON query order, including an occurrence outside the analysis depth, while positions are accumulated from all occurrences. A keyword subset sensitivity can consequently use metadata first observed under an omitted query. A declared per-listing observation-resolution policy would make this behavior auditable. The present examples are small count changes, but version divergence can matter when claims are tied to captured product text.''',
 'v004/rank.py: load; diagnostics.json: repeated_apple_listing_conflicts; raw Apple per-query records.',
 'Specify and justify first/last/canonical observation handling, retain timestamps and conflicting values, and test its effect where a cutoff or text/version comparison is sensitive.')

finding('F31','MODERATE','The reported Play search end time includes product-page collection',
 'Results say Google Play was searched from 15:07 to 15:29 UTC on 24 October. The 49 search requests in the retained first run span 15:07:47-15:14:57; its first 100 product-page requests span 15:15:01-15:28:49. Search and enrichment windows have been conflated.',
 '''The final Play file reuses exactly the search mapping in run-2026-10-24-first.json. That source's request URLs identify 49 search captures ending at 15:14:57.626043 UTC and 100 details captures ending at 15:28:49.334605 UTC. The claimed 15:29 search endpoint is consistent with rounding the end of the whole first collection phase, not the search phase.

The broader Results statement that product pages were collected on 24 and 25 October is supported: the cache has 100 captures on the 24th and 545 on the 25th. This is a precise reporting error of limited direct sampling impact, but important for a strict snapshot audit and for distinguishing changing search results from later changing product counts.''',
 'Results:64-68; scripts/googleplay-scraper/v004/output/run-2026-10-24-first.json requests; final raw search mapping equality; evidence.json cache dates.',
 'Report search and product-page enrichment times separately, preferably from a machine-generated provenance summary.')

# The author has now resolved the scope that made the old allocation impossible.
# Preserve the evidence audit while explicitly closing these prospective objections.
for f in F:
 if f['id']=='F18':
  f.update(severity='RESOLVED',title='Pilot and validation use the full health-tracker sample',
   brief='Resolved by the author\'s 28 October clarification, recorded in D15. Five pilot apps and ten validation apps are selected across the full health-tracker sample without category allocations. Pilot providers and documents remain excluded from validation. The earlier category-specific numerical shortage no longer applies.',
   detail='The author confirmed that the study domain is health trackers overall. The methodology and active instruments now draw five pilot apps and ten validation apps across the full sample, retaining recorded random seeds, separation by provider and document, and policy-language stratification where both languages occur. No category-specific sample requirement remains. The earlier feasibility objection arose from the superseded allocation and is closed by this change. This does not certify that the actual random draws, independent-document checks or validation have been performed.',
   evidence='00_Admin/Decisions/D15_health-tracker-domain.md; revised Methodology Pilot and Validation; codebook v4.',
   required='Implement the revised sample-wide draws and document their seeds and provider/document separation; no additional category quota is required.')
 if f['id']=='F19':
  f.update(severity='RESOLVED',title='One health-tracker domain governs the study design',
   brief='Resolved by D15. Prior studies\' categories support scope definition and keyword collection; they do not define separate study populations, analysis strata or reference-tree assignments. Reference pathways apply to apps through their features and context. The twelve walkthroughs retain six Android and six iOS places across the whole sample.',
   detail='The author clarified that source-paper categories belong to the operational domain definition and keyword provenance. The active methodology, codebook v4 and walkthrough protocol v3 now apply to health trackers overall. Category allocations have been removed from pilot, validation and walkthrough selection. Reference trees form a shared health-tracker framework; each pathway\'s applicability is determined from an app\'s features, data, access and context conditions. Categories may still describe the sample. The earlier domain-mapping objection is closed. This clarification does not establish exhaustive keyword coverage or decide the separate open question about the supervisor\'s phrase "best app".',
   evidence='D15; D03 current Consequences; revised Methodology, Appendix A, codebook v4 and walkthrough protocol v3.',
   required='Use the single-domain procedures in main work and assess pathway applicability per app; retain the separate open D12 decision.')

intro='''Assessment date: 28 October 2026 (Europe/Berlin)
Audited Git revision: 6664310f669407bf79b6b09c3780191bb22aa0cc
Role: independent adversarial assessment of the sampling evidence; no adopted methodological decisions or corrections.
Repository root: C:/Users/Hamza/Desktop/Share/Projects/bachelor-thesis
All project source paths below are relative to that root. Line references identify the audited snapshot.

VERDICT: MAJOR REVISION. The current sample should not be certified or frozen as scientifically validated. Its stored calculations are repeatable after temporary path redirection, and the relocated raw files match their historical hashes. Those strengths coexist with wrong selected product identities, unresolved missing counts, incomplete source provenance, unadjudicated screening and an infeasible pilot/validation allocation. There is no evidence here of fabricated raw bytes or invented completed privacy-study results. There is also insufficient evidence to call the entire process correct.

The review distinguishes confirmed defects, bounded implementation hazards, and unresolved methodological judgments. CRITICAL means a central identity or design condition fails; MAJOR means a validity, reproducibility or interpretability issue must be resolved before the affected claim is relied on; MODERATE means a material justification, evidence or reporting weakness. These are reviewer priorities, not a publisher's formal decision.
'''

scope='''## Scope, coverage and limits
The audit traced the 49-query vocabulary, original Apple v007 and Play v004 collectors, shortened Play v005, current ranking v004, decision records and the 13 October supervisor guidance, screening.csv, relocated raw collections/cache, stored outputs, generated tables, the processed 50-app sample, Methodology, sampling Results and relevant appendices. The preserved proposal was not treated as the current authority.

Every retained sampling raw file was compared to the historical manifest. The entire frame and screening key structure were checked computationally; all 125 main matched title/ID pairs and all 119 recorded exclusion reasons were inspected, with focused original-description checks for selected and borderline cases. The reviewer did not independently adjudicate every full listing or install every app. HTTP extraction could not be revalidated from missing original response bodies. No current live-store scrape was used to substitute for historical evidence.

The original PDFs of Malki, Hutton, Robillard, Sunyaev and Huckvale were checked for the methodological claims discussed in F24. This is not a full audit of all bibliography entries, the literature-search dataset, later policy coding, harms or actual app behavior. Future research activities are assessed for coherence and feasibility, not certified as completed.

No production .tex file, frozen-equivalent collection, screening decision, ranking configuration, generated table, processed sample or historical script was edited. All replays and counterfactuals wrote only to tmp/sampling-peer-audit-2026-10-28. Source hashes were checked before and after the main replay. The reports introduce findings; they do not resolve author/supervisor decisions.

## Review benchmark
The main benchmark is traceable agreement between stated rules, retained evidence, executable processing and reported claims. ACM CCS artifact guidance distinguishes documented, consistent, complete and exercisable artifacts from mere availability; a successful replay does not independently validate a measurement or judgment. These criteria are used as a demanding comparison, not a claim of an official badge or universal mandatory publication checklist. The guidance also distinguishes archival availability from functionality. Different venues implement artifact policies differently; no venue was specified here.
Source: https://sigsac.hosting.acm.org/ccs/CCS2025/call-for-artifacts/

For this study, no probability-sample claim or population margin of error is warranted. A transparent purposive sample can support bounded descriptive analysis of the selected corpus. It does not require an invented power calculation, exhaustive market coverage or perfect software, but it does require correct identities, explicit inclusion rules, honest missingness, a feasible validation design and reproducible claims.

## Verified results and what they establish
* Five sampling raw/cache/log files match the historical SHA-256 manifest exactly. This verifies preservation of those bytes across relocation, not correctness of the website fields.
* Apple has 8,172 retained iPhone-compatible per-query rows and 5,058 distinct listings across the depth-200 collection. Its first 30 API positions contain 1,440 hits and 848 distinct listings. These totals describe different frames, not contradictory counts.
* Play has 1,178 parsed search hits, 1,138 at positions <=30 and 645 distinct product-page records. The final results mapping has 1,139 rows because an ID fetched due to one qualifying occurrence can also be emitted at a deeper occurrence in another query. The ranking reapplies the depth filter. This is not an extra selected app or a missing-page error.
* Removing preinstalled listings gives 846 Apple and 644 Play listings. Current matching gives 125 pairs, 721 Apple-only and 519 Play-only candidates: 1,365 in total. These are implementation outputs; F01 establishes incorrect product identities within them.
* Calibration reproduces: 116 positive pairs, median v/r=0.2338153494668798, c=0.08958070788703418. Positive-pair Spearman rho=0.7948624798781704. The current pair count is 116, while the earlier v003 audit's 114 belongs to its earlier version.
* The main cascade reproduces: 70 reached =47 selected +12 provider skips +11 E1 exclusions. Provider skips are not eligibility exclusions. The 275-row screening total covers more than the main reached candidates, including sensitivity work.
* Current selection: 47 ranked apps, 47 provider keys; 33 paired, eight Play-only and six Apple-only in the frame. There are 39 selected Apple and 41 selected Play listings (80 total), all with observed score inputs and zero recorded install price. The 41 Play listings carry policy URLs; URL presence is not policy validity, applicability or availability.
* Category counts reproduce: activity 22, diet/weight 12, cycle four, pregnancy two, sleep three, mood two, heart one and multiple one. Together with three preinstalled apps, apps.csv has 50 rows and 49 provider keys.
* The 645 distinct cache entries all match final Play rows. Capture dates are 100 on 24 October and 545 on 25 October. This verifies no absent final parsed product-page record, not complete HTTP provenance.
* The 12 current ranking unit tests pass. Exact isolated replay passes for report.json, selection.csv, excluded.csv, all 58 sensitivity rows, processed apps.csv, and app-sample/developer-rule/developer-aliases tables. A separate replay also reproduces developer-pilot.tex from the relocated pilot. Unchanged v005 main reproduces all 1,139 final result rows using retained searches and cache without network.
* The project checker and graph refresh both fail because 01_Literature/README.md is absent. No successful global project-check or graph-refresh result was obtained.

## Overall assessment by stage
Raw preservation: supported for the five retained files; original response-level completeness is not supported.
Collectors: enough retained parsed evidence for downstream replay; full extraction accuracy, search completeness and regional field semantics are not certified.
Processing: calculations repeat; product matching and missing-value semantics have confirmed defects.
Eligibility: structural consistency passes; human adjudication and several high-impact judgments remain unresolved.
Results: most stated implementation counts reproduce; correlation interpretation, selected identities, timestamp and some denominators require correction.
Study design: purposive sampling can be defensible, but the validation allocation and broader domain mapping do not currently align.
'''

closing='''## What must happen before a defensible freeze
1. Establish the current canonical data package and restore a runnable documented entry point and current manifest. Keep the verified original files unchanged.
2. Review all product pairs, repair identity rules in a new script version, and test negative examples across every sensitivity frame.
3. Resolve the meaning and treatment of missing feedback counts, retain uncertainty, and replace misleading correlation reporting.
4. Complete documented human screening adjudication, including Kinomap, Lady Pill Reminder, mental-health boundaries and exact DiGA evidence. A reviewer scenario is not an author decision.
5. Revise the infeasible pilot/validation allocation and map all sampled domains to harm models and instruments before the pilot is drawn. Resolve the required coder procedure.
6. Rerun the corrected, approved rules and all affected variants; regenerate sample/table/report artifacts together and reconcile claims with their actual denominators and provenance.
7. Freeze a dated package with raw/parsed distinctions, hashes, source/collector versions, environment, schema, commands, screening evidence and documented remaining limitations. An archive or DOI may support a later venue artifact process, subject to rights and data handling; this review has not published anything.

No finding is closed by this assessment. Mechanical replay does not clear identity, construct validity or unresolved eligibility. Conversely, the confirmed issues do not justify discarding preserved raw data whose hashes and downstream replay pass. The evidence supports repair and re-adjudication, not a claim of universal failure or a claim of perfection.

## Evidence package and reproduction
evidence.json records original-source hashes, raw and frame totals, cache checks, main cascade, replay comparisons and isolated identity/eligibility scenarios. diagnostics.json records the seeded calibration diagnostic, current/deep matching examples, repeated Apple metadata conflicts and the network-free v005/cache experiment. all-matched-pairs.csv, main-cascade.csv and missing-play-counts.csv permit direct inspection of all affected records.

Local verification programs are retained in tmp/sampling_peer_audit.py and tmp/sampling_peer_diagnostics.py. They import the production ranking read-only and explicitly redirect table/dataset outputs. Their source copies are included as audit-source.txt and diagnostics-source.txt; to rerun from the repository root, copy them to the named tmp paths and run python tmp/sampling_peer_audit.py followed by python tmp/sampling_peer_diagnostics.py. They require the existing local collections and stored ranking outputs. Do not invoke the ordinary production ranking command merely to inspect this report: its configured paths are stale and its normal outputs include thesis tables.

The bootstrap uses seed 20261028 and 2,000 matched-ratio resamples; the selection diagnostic evaluates every tenth sorted bootstrap factor. It preserves unresolved candidates as pending. It is neither a population confidence interval nor a corrected-sample estimate.

Checked commands: python -I -m unittest discover -s scripts/app-ranking/v004/tests (12 passed); python scripts/check_project.py (failed: missing literature README); .\\graphify.ps1 refresh (failed: same dependency). No TeX compilation was performed because the assessment changes no TeX and the requested audit concerns sampling validity rather than typesetting.

## Primary sources used for interpretation
ACM CCS artifact evaluation: https://sigsac.hosting.acm.org/ccs/CCS2025/call-for-artifacts/
StatCounter methodology and page-view basis: https://gs.statcounter.com/faq
Google country/device-specific ratings announcement: https://android-developers.googleblog.com/2021/08/making-ratings-and-reviews-better-for.html
Apple ratings/reviews overview: https://developer.apple.com/help/app-store-connect/monitor-ratings-and-reviews/ratings-and-reviews-overview/
Apple permits summary-rating resets on version release. This is an additional comparability limitation for interpreting counts as a uniform lifetime accumulation; no reset is demonstrated for the selected apps here.

Original PDFs used for F24 are in 01_Literature/PDFs/Methods-Reading/01_App-Reviews/: 01_Malki_2024_Exploring-Privacy-Practices-of-Female-mHealth-Apps-in-a-Post-Roe-World.pdf (PDF p4); 02_Hutton_2018_Assessing-the-Privacy-of-mHealth-Apps-for-Self-Tracking-Heuristic-Evaluation-Approach.pdf (p5); 06_Robillard_2019_Availability-readability-and-content-of-privacy-policies-and-terms-of-agreements-of-mental.pdf (p2); 07_Sunyaev_2015_Availability-and-quality-of-mobile-health-app-privacy-policies.pdf (p3, printed e30); 26_Huckvale_2019_Assessment-of-the-Data-Sharing-and-Privacy-Practices-of-Smartphone-Apps-for-Depression-and.pdf (p3). The report distinguishes PDF page numbers from printed pagination.
'''

intro=intro.replace(', unadjudicated screening and an infeasible pilot/validation allocation', ' and unadjudicated screening')
intro+='\nScope amendment, 28 October 2026: the author confirmed health trackers as the single study domain (D15). The current methodology and instruments now remove category allocations. F18 and F19 are resolved; the remaining findings retain their original audit scope and evidence date and have not been re-audited for unrelated intervening changes. There are 31 review records, including these two resolved items.\n'
scope=scope.replace('No production .tex file, frozen-equivalent collection', 'During the original audit, no production .tex file, frozen-equivalent collection')
scope=scope.replace('Study design: purposive sampling can be defensible, but the validation allocation and broader domain mapping do not currently align.', 'Study design: one health-tracker domain now governs the pilot, validation, walkthroughs and reference-pathway applicability. The former category-allocation and mapping objections are resolved by D15.')
closing=closing.replace('5. Revise the infeasible pilot/validation allocation and map all sampled domains to harm models and instruments before the pilot is drawn. Resolve the required coder procedure.', '5. Apply D15: draw the five pilot and ten independent validation apps across the full sample, without category allocations. Assess reference pathways per app and resolve the required coder procedure.')
closing=closing.replace('No finding is closed by this assessment.', 'F18 and F19 are closed by the author\'s subsequent scope clarification and its implementation; the other findings are not closed by this assessment.')
closing=closing.replace('No TeX compilation was performed because the assessment changes no TeX and the requested audit concerns sampling validity rather than typesetting.', 'No TeX compilation was performed during the original audit. The subsequent scope edit is verified separately in a copied tree, without writing build files into the author\'s thesis directory.')
detailed=intro+'\n'+scope+'\n## Detailed findings\n'
for f in F:
 detailed+=f"\n## {f['id']} | {f['severity']} | {f['title']}\n{f['detail']}\n\nEvidence: {f['evidence']}\n\nRequired resolution: {f['required']}\n"
detailed+='\n'+closing
brief=intro+'''\n## Verified strengths and limits
Five relocated raw files match historical hashes; all 12 current ranking tests pass. With input/output paths redirected temporarily, the ranking report, selection, exclusions, 58 sensitivity rows, processed 50-app sample and three generated tables reproduce exactly; the pilot table and v005 parsed results also reproduce. Current main counts are 1,365 candidates, 116 positive calibration pairs and 70 reached=47 selected+12 provider skips+11 exclusions. These are repeatable implementation results, subject to the defects below. The 50 apps represent 49 provider keys. All present selected score inputs are observed; 41 Play policy URLs are present, which does not establish valid policies.

Coverage: complete structural checks of retained sampling data and 275 screening keys; title/ID inspection of 125 main matched pairs and all 119 exclusion reasons; targeted original-description and source-PDF checks. This is not an independent human re-screen of every full listing, installation audit, validation of missing original HTTP bodies, literature-search audit or certification of completed coding. No production .tex, raw data, screening, configuration, sample or generated table was changed.

## All findings (same IDs as the detailed report)
'''
for f in F:brief+=f"\n### {f['id']} | {f['severity']} | {f['title']}\n{f['brief']}\n"
brief+='''\n## Priority sequence
Repair canonical paths and manifest; verify all product identities; resolve missing counts and field semantics; complete human screening; apply the single-domain pilot and validation rules and resolve the coder procedure; rerun every affected result; reconcile chronology, denominators and acquisition evidence; freeze an executable, dated package. D15 resolves F18 and F19; the other corrections are not adopted by this assessment.

The score has a coherent conditional derivation; it is not a validated user count. The sample is purposive, so no population margin of error or representative German-market prevalence claim is justified. Apple also permits rating resets: counts need not share one lifetime accumulation basis, and no selected-app reset was established.

The main review comparison is ACM's documented/consistent/complete/exercisable artifact framework, not an official publisher verdict or claim of a universal checklist. StatCounter explicitly uses page views, and Google's country-specific ratings announcement does not define the scraper's undocumented review-count field. Primary sources: https://sigsac.hosting.acm.org/ccs/CCS2025/call-for-artifacts/ ; https://gs.statcounter.com/faq ; https://android-developers.googleblog.com/2021/08/making-ratings-and-reviews-better-for.html ; https://developer.apple.com/help/app-store-connect/monitor-ratings-and-reviews/ratings-and-reviews-overview/

The detailed version supplies evidence locators and a required resolution for every finding. The accompanying JSON/CSV evidence preserves exact checks and distinguishes current results from hypothetical scenarios. The project-wide checker and graph refresh failed on a missing literature README; no clean global check is claimed. The review supports major revision before sample freeze, while preserving the distinction between valid byte preservation, repeatable calculations and unvalidated scientific judgments.
'''

brief=brief.replace('No production .tex, raw data, screening, configuration, sample or generated table was changed.', 'During the original audit, no production .tex, raw data, screening, configuration, sample or generated table was changed. The subsequent D15 amendment changes the active methodology and instruments to implement the author\'s scope clarification.')
(OUT/'Detailed-Review.txt').write_text(detailed,encoding='utf-8')
(OUT/'Brief-Review.txt').write_text(brief,encoding='utf-8')
(OUT/'findings.json').write_text(json.dumps(F,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
for name in ['evidence.json','diagnostics.json','all-matched-pairs.csv','main-cascade.csv','missing-play-counts.csv']:
 shutil.copy2(AUD/name,OUT/name)
shutil.copy2(ROOT/'tmp/sampling_peer_audit.py',OUT/'audit-source.txt')
shutil.copy2(ROOT/'tmp/sampling_peer_diagnostics.py',OUT/'diagnostics-source.txt')

from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
FONTROOT=Path('C:/Windows/Fonts')
for name,filename in [('Review','arial.ttf'),('Review-Bold','arialbd.ttf'),('Review-Italic','ariali.ttf')]:pdfmetrics.registerFont(TTFont(name,str(FONTROOT/filename)))
pdfmetrics.registerFontFamily('Review',normal='Review',bold='Review-Bold',italic='Review-Italic',boldItalic='Review-Bold')
body=ParagraphStyle('body',fontName='Review',fontSize=9.1,leading=13.3,spaceAfter=8.0,textColor=colors.HexColor('#203047'),splitLongWords=True)
heading=ParagraphStyle('heading',parent=body,fontName='Review-Bold',fontSize=12.3,leading=16,spaceBefore=14,spaceAfter=8,keepWithNext=True,textColor=colors.HexColor('#123959'))
smallhead=ParagraphStyle('smallhead',parent=heading,fontSize=10.7,leading=14)
title=ParagraphStyle('title',parent=heading,fontSize=24,leading=29,spaceBefore=0,spaceAfter=14)
subtitle=ParagraphStyle('subtitle',parent=body,fontSize=12,leading=17,textColor=colors.HexColor('#477086'),spaceAfter=20)
evidence_style=ParagraphStyle('evidence',parent=body,fontSize=8,leading=11.5,textColor=colors.HexColor('#526175'))
def footer(c,doc):
 w,h=doc.pagesize;c.setStrokeColor(colors.HexColor('#c8d5df'));c.line(45,42,w-45,42)
 c.setFont('Review',8);c.setFillColor(colors.HexColor('#526175'));c.drawString(45,29,'Sampling peer review | 28 October 2026 | Assessment only')
 c.drawRightString(w-45,29,str(doc.page))
def render(text,name,label):
 doc=SimpleDocTemplate(str(OUT/name),pagesize=(595.28,841.89),leftMargin=46,rightMargin=46,topMargin=44,bottomMargin=57,title='Sampling peer review - '+label,author='Scientific evidence audit')
 story=[Paragraph('Sampling peer review',title),Paragraph(label+' | Methodology, data, collectors, processing and reported sample',subtitle)]
 for para in re.split(r'\n\s*\n',text):
  for chunk in re.split(r'(?m)(?=^#{2,3} )',para):
   chunk=chunk.strip()
   if not chunk:continue
   if chunk.startswith('## '):
    first,*rest=chunk.split('\n',1);story.append(Paragraph(html.escape(first[3:]),heading))
    if rest:story.append(Paragraph(html.escape(rest[0]).replace('\n','<br/>'),body))
   elif chunk.startswith('### '):
    first,*rest=chunk.split('\n',1);story.append(Paragraph(html.escape(first[4:]),smallhead))
    if rest:story.append(Paragraph(html.escape(rest[0]).replace('\n','<br/>'),body))
   else:
    sty=evidence_style if chunk.startswith('Evidence:') else body
    story.append(Paragraph(html.escape(chunk).replace('\n','<br/>'),sty))
 # Keep a finding's claim, evidence and resolution on the same page.
 grouped=[]; group=[]
 for item in story:
  if isinstance(item,Paragraph) and item.getPlainText()=='Detailed findings':continue
  is_heading=isinstance(item,Paragraph) and item.style.name in ['heading','smallhead']
  if is_heading:
   if group:grouped.append(KeepTogether(group));group=[]
   if re.match(r'F\d{2} \|',item.getPlainText()):group=[item];continue
  if group:group.append(item)
  else:grouped.append(item)
 if group:grouped.append(KeepTogether(group))
 doc.build(grouped,onFirstPage=footer,onLaterPages=footer)
render(detailed,'Detailed-Review-Scope-Amended.pdf','Detailed assessment - 29 open findings, 2 resolved')
render(brief,'Brief-Review-Scope-Amended.pdf','Concise assessment - 29 open findings, 2 resolved')

from pypdf import PdfReader
for name in ['Detailed-Review','Brief-Review']:
 p=OUT/(name+'-Scope-Amended.pdf');reader=PdfReader(p);text='\n'.join(x.extract_text() or '' for x in reader.pages)
 missing=[f['id'] for f in F if f['id'] not in text]
 if missing:raise AssertionError((name,missing))
 print(name,'pages',len(reader.pages),'words',len((OUT/(name+'.txt')).read_text(encoding='utf-8').split()),'bytes',p.stat().st_size)
assert all(f['id'] in brief for f in F)
