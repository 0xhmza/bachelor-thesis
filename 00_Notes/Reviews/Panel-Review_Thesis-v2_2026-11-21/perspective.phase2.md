contract_role: perspective
## Dimension Scores

### D1: methodology_rigor
score: not_assessed

### D2: domain_accuracy
score: not_assessed

### D3: argumentative_coherence
score: not_assessed

### D4: cross_disciplinary_relevance
score: warn
trigger: "The yardstick or key constructs are present but only implicit, partly sourced or applied unevenly"

### D5: writing_and_structure
score: not_assessed

### D6: venue_fit_and_contribution
score: not_assessed

## Review Body

### Reviewer Identity
Peer Reviewer 3 (cross-disciplinary / practical): a consumer-protection and risk-communication scholar working on EU consumer law and data-protection enforcement. I am an outsider to usable-privacy measurement and HCI conventions, and I do not assess statistics, sampling efficiency or coding reliability; those belong to other seats.

### Overall Recommendation
Major Revision (within my remit). The changes I ask for are mostly conceptual and textual, not new data, but the first one (W1) has to be settled before any policy or interface is coded.

### Confidence Score
4

Confidence is an uncertainty/scope disclosure only; it never changes consensus counts, severity, decision bearing, or arbitration.

### Calibration Status
`NOT_CALIBRATED`

### Criterion-Bound Judgements
| Dimension / criterion | Criterion source | Judgement | Evidence anchors | Rationale | Uncertainty or scope limit | Decision bearing? |
|---|---|---|---|---|---|---|
| D4: normative yardstick for what providers should say about harms | Contract D4; accepted Reviewer Configuration Card (review focus 1) | PARTLY_MEETS | `text: §2.2 "it recommends that for complex or unexpected processing providers also explain the most important consequences"` | A sourced legal baseline exists, but no threshold says which harms a provider is expected to state, so RQ1/RQ2 cannot yet separate an unmet expectation from lawful silence (W1, W2) | Results not yet written; judged on framing and RQs | yes: drives the D4 warn |
| D4: measurability of harm communication from provider texts | Contract D4; Configuration Card (review focus 2) | PARTLY_MEETS | `text: §3.4 RQ2 "how do they word it"` | Two surfaces are studied, but stance and claim-strength categories are reader-effect concepts not yet tied to observable text features (W6, W7) | Coding scheme is outside the written methodology | yes, jointly with the yardstick |
| D4: ethics and legality of collecting data from the store | Contract D4; Configuration Card (review focus 3) | DOES_NOT_MEET | `text: Appendix B "keeps up to the first 30 apps of each result page"` | The search path is disallowed by robots.txt and the thesis says nothing about access conditions, load or legal basis (W3) | I verified robots.txt and the terms of service on 21 November 2026; the legal route is a lead, not an opinion | yes: Major finding, though it does not touch sample validity |
| D4: consequences of excluding one platform's users and other surfaces | Contract D4; Configuration Card (review focus 4) | PARTLY_MEETS | `text: §4.1 "Android is the larger mobile platform there"` | The choice is justified by share, but what it cannot cover (iOS users, Apple Health, Apple's label and tracking-prompt regime, the store listing) is not stated (W4, W5) | A discussion chapter may later address this | no: scope statements fix it |
| D4: definitions usable by legal and risk-communication readers | Contract D4 | MEETS | `text: §2.1 "A chain that starts with parts of a system"` | Key terms draw on recognised legal scholarship and are defined before use; two title-level terms are missing (W7) | none identified | no |
| D4: practical implications for regulators, providers and users | Contract D4 | NOT_ASSESSED | — | No discussion or conclusion exists yet by design | Intentionally missing chapters | no |

### Summary Assessment
Reading as an EU consumer-protection and risk-communication scholar, I find a draft whose framing is unusually honest about the legal baseline. Section 2.2 states that GDPR information duties cover data practices and that explaining consequences is mostly recommended rather than required. That is the right starting point for a study of harm communication, and it makes the work legible to lawyers and regulators. Key terms draw on recognised legal scholarship (Citron and Solove), and the sampling choices (German storefront, a reach proxy, the preinstalled vendor app) follow how consumers actually meet these products.

Three things limit uptake by adjacent fields. First, the research questions ask which harms providers leave unmentioned or downplay, but the thesis does not say which harms a provider would be expected to state. Without that threshold, absence will read as failure, which the thesis's own legal analysis does not support. The WP29 guidance it already cites supplies such a threshold. Second, the collection script queries a store path that robots.txt disallows, sending a generic browser user-agent string, and the thesis says nothing about access conditions, load or legal basis. Third, the consequences of the Android-only design and of the two-surface definition (no store listing or Data safety section) are not stated. None of this threatens the integrity of the sample. All of it can be fixed mainly in text, but the threshold has to be fixed before coding.

Strengths (S1 to S6) and weaknesses (W1 to W8) follow.

### S1: The legal baseline is stated, and duty is kept apart from recommendation
Section 2.2 says plainly what Articles 12 to 14 require and that consequence information outside automated decisions is guidance, not duty. Many privacy-policy studies treat every missing item as non-compliance. This one gives a legal reader the means to keep "not said" apart from "unlawfully not said", provided W1 is addressed.
**Evidence Anchor**: text: §2.2 "Outside automated decisions, the law therefore asks for a description of data practices"

### S2: The harm construct rests on an established legal taxonomy
Defining privacy harm through Citron and Solove's seven types lets lawyers, regulators and consumer organisations map the study's harm codes onto categories they already use in enforcement and litigation.
**Evidence Anchor**: text: §2.1 "Citron and Solove sort privacy harms into seven types"

### S3: The collection keeps personal data to a minimum and spreads its load
The script removes the review-comments field from every store-page record before caching it, so reviewers' texts and names are never stored. It also waits one second between requests. A data-protection reader will welcome both; they belong in the text (see W3).
**Evidence Anchor**: dataset: Appendix B, Listing lst:sample (sample.py), main(), where the comments field is popped from each store-page record before it is written to the cache

### S4: The preinstalled tracker reflects how consumers actually get these apps
Adding the vendor's preinstalled tracker recognises that reach does not run only through the store. This is good stakeholder realism for a consumer-protection reading.
**Evidence Anchor**: text: §4.4 "They reach users without a download, so their review counts understate how many people have them"

### S5: Two surfaces rather than the policy alone
Comparing the privacy policy with in-app notices matches the WP29 layered model and the consumer-law view that information counts where the consumer meets it. RQ4 can show contradictions such as the policy/FAQ conflict reported by Malki et al., which are directly relevant to enforcement.
**Evidence Anchor**: text: §2.1 "This thesis looks at two surfaces: the privacy policy and the interface of the app"

### S6: The reach proxy is chosen for exposure and stated as a proxy
Ranking by German review counts approximates how many consumers are exposed. That is the right weighting when the question is what consumers are told, and the thesis does not overclaim it.
**Evidence Anchor**: text: §4.4 "The review count is a proxy for popularity, not a count of users."

### W1: No threshold for which harms a provider is expected to state
**Severity**: Major
**Evidence Anchor**: text: §3.4 main research question "What types of downstream privacy harms do health tracker providers acknowledge or downplay"
**Confidence**: 4 — EU data-protection transparency law and risk-communication practice

The main question, RQ1 ("remain unmentioned") and the RQ2 stance categories treat unmentioned or qualified harms as provider behaviour to be explained. Section 2.3 sets the reference standard as "the harms that their apps make possible", that is, every pathway in the harm tree. No legal or professional norm I know of expects a notice to list every possible harm. Article 12 asks for concise information, and WP29 warns against information fatigue and recommends layering (para. 35). Research on mandated disclosure finds that longer lists reduce use. An unmentioned harm therefore has several readings: lawful brevity, placement in another layer, a harm below any reasonable threshold, or downplaying. The thesis cannot yet tell these apart.

The thesis already holds the missing yardstick. WP29 para. 10, cited in §2.2, says that for complex, technical or unexpected processing controllers should spell out the most important consequences and assess which particular risks to bring to users' attention.

Minimum remedy: record a decision (Dnn) before coding that defines tiers. (T1) Statements the GDPR requires where it touches risk: transfers and the absence of an adequacy decision (Art. 13(1)(f)), the risks of transfers based on consent (Art. 49(1)(a)) and automated decisions (Art. 13(2)(f)). (T2) The "most important consequences" WP29 expects for processing that is complex, technical or unexpected for a tracker user, for example special-category data shared with advertisers, inference of conditions, or access by authorities. (T3) All other harm-tree harms, reported descriptively. Then report RQ1 gaps per tier, and use "downplay" only for a coded textual pattern (W6). No new citation is needed.

Stronger, costlier option: check the T2 list against an outside view, such as a short expert or lay rating of which consequences users would expect to be told. This is the author's choice and may exceed the scope of a bachelor's thesis.

### W2: The legal baseline understates where the GDPR asks for risk information
**Severity**: Minor
**Evidence Anchor**: text: §2.2 "an explanation of what could follow from them is a recommendation"
**Confidence**: 4 — GDPR text and WP29 guidance checked (WP260 rev.01, para. 10)

The statement holds for the information duties at collection, but a legal reader will find it too broad. WP29 para. 10 ties its advice on consequences to the fairness principle (Art. 5(1)(a)) and to Recital 39, under which people should be made aware of risks. The GDPR also requires consequence or risk information in specific cases: Art. 49(1)(a) for transfers based on consent, and Art. 34(2) with Art. 33(3)(c) for the likely consequences of a breach (the setting of Zou et al., whom §3.3 cites). Suggested wording: "At collection, Articles 13 and 14 require a description of practices; information on consequences is required in specific cases and recommended, as part of fair processing, for complex or unexpected processing." I leave the accuracy question itself to the domain seat. I flag it because W1's tiers depend on it.

### W3: Store access conditions, request load and legal basis are not reported
**Severity**: Major
**Evidence Anchor**: absence: §4.2 Search and Appendix B — expected a statement of the store's access conditions (robots.txt, terms of service), the request load and the handling of personal data in the scripted collection; checked §4.1–§4.4, §5.1, Appendix B prose, Table tab:keywords, Listings lst:config and lst:sample
**Confidence**: 4 — research-ethics and data-protection practice; 3 on the copyright route mentioned below

The search function requests `play.google.com/store/search` with the user-agent string `Mozilla/5.0`. On 21 November 2026 I checked Google Play's robots.txt: it disallows `/store/search` (and `/store/apps/datasafety*`) for all user agents, while product pages are not disallowed. Google's Terms of Service (effective 30 July 2026, section "Don't abuse our services") treat automated access that ignores robots.txt as abuse. The thesis does not mention any of this. The project's own script README and decision archive record the restriction, so this is a reporting gap rather than an oversight. An ethics reviewer or examiner reading Appendix B will still ask about it.

The facts in the author's favour are strong and should be stated. The raw data show 54 search requests and 704 product-page requests over about 17 minutes, at least one second apart. There was no login and no circumvention of access controls, review texts were discarded, and only public listing data were kept. Developer names that belong to individual people are personal data, but they are published and minimal.

Minimum remedy: add a short "Access and ethics" paragraph to §4.2 or Appendix B. It should cover what was requested, the robots.txt and terms-of-service status, the load, the handling of personal data, and why the disallowed path was needed (the German result order appears only on the search page). It should also give the legal basis. One lead to check with the university, not a legal opinion: the text-and-data-mining exception for scientific research (Directive (EU) 2019/790, Art. 3, with Art. 7(1) making contrary contract terms unenforceable; §60d UrhG in Germany).

Stronger option: replace the scripted search with a documented, logged-out manual browser search of the 54 queries, saving each result page. This uses an allowed route and records exactly what a consumer sees, which also helps ecological validity. The product-page reads can stay scripted. Trade-offs: about an hour of manual work, some risk of transcription errors, and possible drift in results since 21 November. This is the author's choice. If the Data safety section is ever collected (W5), its path is disallowed too, so it would need the same treatment.

### W4: What the Android-only design leaves out is not stated
**Severity**: Minor
**Evidence Anchor**: text: §4.1 "The study covers Android apps offered in Germany."
**Confidence**: 4 — consumer-law scope reasoning; the shares come from the thesis's own StatCounter source

The justification (72.3% of page views) explains the choice but not what it costs. By the same source, about 28% of German mobile page views come from iOS. Apple Health is preinstalled on every iPhone, and the thesis's own reason for adding a preinstalled tracker applies to it with more force. Apple also runs a separate interface-level disclosure regime (App Store privacy labels and the App Tracking Transparency prompt), so RQ4's interface findings are Android-specific. Many policies are shared across platforms, so RQ1 to RQ3 results based on policies may well transfer while interface results may not.

Remedy: add one or two sentences to §4.1 saying what an Android-only sample can and cannot say about users in Germany. Qualify the main question or title ("on Android") if the interface results are central. The full discussion can wait for the Discussion chapter.

### W5: The store listing and the Data safety section are left out of "surfaces" without a reason
**Severity**: Minor
**Evidence Anchor**: text: §2.1 "A place where a provider tells users how it handles their data."
**Confidence**: 4 — EU consumer law (Unfair Commercial Practices Directive) and app-store disclosure practice

The definition of a surface covers the store listing, yet only the policy and the interface are studied. For a consumer lawyer, the listing is where the consumer decides to install, which is the "transactional decision" of the Unfair Commercial Practices Directive. It is also where protection claims are used as marketing ("encrypted", "we never sell your data"). The Data safety section is a disclosure Google requires from developers, and Malki et al., whom the thesis cites, used it. The Directive is already in references.bib.

Remedy: either justify the exclusion in the methodology (scope, or the platform-structured format of Data safety), or code the listing's protection claims for RQ3 only. Collect any Data safety content manually (see W3).

### W6: Stance and claim strength are reader-effect concepts, not yet text features
**Severity**: Minor
**Evidence Anchor**: text: §3.4 RQ2 "do they acknowledge, qualify, minimise or deny it, or present it as the user's responsibility"
**Confidence**: 4 — risk-communication research and the "average consumer" test in EU consumer law

Whether a passage minimises a harm, or a protection claim is strong, depends on how a reader takes it. EU consumer law judges this against the average consumer, and risk-communication research (the mental-models approach) shows that meaning depends on the reader's prior beliefs. Document analysis can measure textual features, not what users receive or understand.

Remedy: when the coding is written up, define each stance code by observable features (hedges and modal verbs, as in the Zou et al. work the thesis cites; who is named as responsible; whether likelihood or severity is stated). Add one sentence on the limit of inference from text to users. Keep "downplay" in the main question only if it is defined as such a pattern.

### W7: "Harm communication" and "downstream" harms are not defined
**Severity**: Minor
**Evidence Anchor**: text: title "Understanding Privacy Harm Communication in Health Tracking Apps"
**Confidence**: 4 — risk-communication terminology

Section 2.1 defines privacy harm, but neither the title's "harm communication" nor the main question's "downstream privacy harms" is defined. Risk-communication readers will ask whether communication means naming a harm or also conveying its likelihood and severity, which are the two parts their field treats as core. Remedy: add one Key Terms entry. Define "downstream" as the harm at the end of a harm-tree pathway, or drop the word.

### W8: The DiGA exclusion carries no rationale
**Severity**: Minor
**Evidence Anchor**: table: Table tab:eligibility (§4.3), row X8
**Confidence**: 3 — general familiarity with the German DiGA regime, not specialist knowledge

DiGA are the one group of German health apps that must meet binding, sector-specific data-protection requirements to be listed and reimbursed. Excluding them is defensible because they fall under a different regime and are often prescribed. Saying so in one clause would turn the rule into a clear scope statement and point to a natural comparison for future work: regulated versus unregulated trackers.

### Detailed Comments

#### Assumption Audit
- **Explicit assumptions**: The legal baseline (§2.2), the review count as a reach proxy (§4.4) and harm trees as a way to find possible harms (§2.3) are stated and sourced. They hold from my perspective, subject to W1 and W2.
- **Implicit assumptions**: (a) More harm statements mean better communication. Mandated-disclosure research disputes this, so the thesis should not let RQ1 imply it (W1). (b) The provider writes everything on the interface. On Android, runtime permission dialogs and Health Connect consent screens are platform text, so RQ4 coding should record who wrote each statement. (c) What a document says is what users are told (W6). The two-surface design partly answers this.
- **Paradigmatic assumptions**: The framing inherits the EU "information paradigm" of consumer protection, the informed consumer who reads and decides. The thesis can turn this into a strength by presenting its contribution as testing whether a precondition of that paradigm holds (is harm information there at all?), without implying that providing it would protect users.

#### Cross-Disciplinary Connections
- **Parallel research**: Work on the limits of mandated disclosure (Ben-Shahar and Schneider) and the mental-models approach to risk communication (Morgan et al.) address the same question from law and decision science: when does telling people about a risk help?
- **Borrowing opportunities**: The EDPB guidelines on deceptive design patterns include a "Left in the dark" category (conflicting or ambiguous information) that maps onto RQ2 and RQ4. The policy/FAQ contradiction reported by Malki et al. is a textbook case. For RQ3, the misleading-action and misleading-omission tests of the Unfair Commercial Practices Directive give protection claims a legal yardstick next to the technical one from harm trees.
- **Methodological borrowing**: A small lay-reader check of a few coded passages would test whether the stance codes match how consumers read them. This is optional and probably beyond the scope of a bachelor's thesis.

#### Practical Impact
- **Real-world application**: German consumer associations can bring representative actions over GDPR breaches (CJEU, C-319/20), and data-protection authorities and Google's Data safety programme are further audiences. Results split by tier (W1) would tell them which gaps are legal deficits and which are gaps against good practice. That split is what makes a descriptive study usable for enforcement.
- **Implementation feasibility**: The recommendations the thesis may later make to providers are only feasible if they respect the conciseness duty. Suggesting layered harm notices for T2 consequences is more realistic than longer policies.
- **Stakeholders**: iOS users (W4); users of reproductive-health apps, for whom access by authorities is a salient harm; and German consumers facing English-only texts. Rule I7 admits English-only apps, and intelligibility under Art. 12 is judged for the audience addressed, so the language of each surface is worth recording.

#### Broader Implications
- **Ethical dimensions**: Beyond W3, the later interface inspection will mean creating test accounts, accepting terms and possibly entering health-like data. Planning and recording this now (no real health data, deleting accounts afterwards, handling any data-subject requests) will avoid a second ethics gap.
- **Social impact**: Provider concentration matters for what "providers" means in the results. Leap Fitness Group has eight of the 50 apps, and if they share one policy, results reported per app weight that policy eightfold.
- **Future directions**: Comparisons with DiGA (W8) and with iOS (W4), and a reader-side study of whether tiered harm notices change understanding.

### Cross-Disciplinary Reading Recommendations
- Ben-Shahar and Schneider (2014), More Than You Wanted to Know: The Failure of Mandated Disclosure. From law and economics; it supports keeping "unmentioned" apart from "deficient" (W1).
- Morgan, Fischhoff, Bostrom and Atman (2002), Risk Communication: A Mental Models Approach. From decision science; it grounds the reader-effect caveat and the likelihood/severity elements of harm communication (W6, W7).
- Fiesler, Beard and Keegan (2020), No Robots, Spiders, or Scrapers: Legal and Ethical Regulation of Data Collection Methods in Social Media Terms of Service (ICWSM). From research ethics; a short citation for the access paragraph (W3).
- EDPB (2023), Guidelines 03/2022 on deceptive design patterns in social media platform interfaces, version 2.0. From data-protection enforcement; its taxonomy fits RQ2 and RQ4.
- Directive (EU) 2019/790 (Digital Single Market copyright directive), Art. 3 and Art. 7(1), and CJEU C-319/20 (Meta Platforms Ireland v Bundesverband der Verbraucherzentralen, 2022). Legal anchors for W3 and for the practical-impact point. Given the author's preference for few citations, at most one or two of these need to enter the thesis; GDPR, WP29 and the Unfair Commercial Practices Directive are already in references.bib.

~~~yaml suggested-references
- title: "More Than You Wanted to Know: The Failure of Mandated Disclosure"
  authors: ["Ben-Shahar, O.", "Schneider, C. E."]
  year: "2014"
  doi: null
  arxiv_id: null
- title: "Risk Communication: A Mental Models Approach"
  authors: ["Morgan, M. G.", "Fischhoff, B.", "Bostrom, A.", "Atman, C. J."]
  year: "2002"
  doi: null
  arxiv_id: null
- title: "No Robots, Spiders, or Scrapers: Legal and Ethical Regulation of Data Collection Methods in Social Media Terms of Service"
  authors: ["Fiesler, C.", "Beard, N.", "Keegan, B. C."]
  year: "2020"
  doi: null
  arxiv_id: null
- title: "Guidelines 03/2022 on deceptive design patterns in social media platform interfaces: how to recognise and avoid them"
  authors: ["European Data Protection Board"]
  year: "2023"
  doi: null
  arxiv_id: null
- title: "Directive (EU) 2019/790 on copyright and related rights in the Digital Single Market"
  authors: ["European Parliament and Council of the European Union"]
  year: "2019"
  doi: null
  arxiv_id: null
- title: "Meta Platforms Ireland Ltd v Bundesverband der Verbraucherzentralen und Verbraucherverbände (C-319/20)"
  authors: ["Court of Justice of the European Union"]
  year: "2022"
  doi: null
  arxiv_id: null
~~~

### Questions for Authors
1. Which harms do you expect a provider to state, on what basis, and will you fix this in a decision record before coding starts?
2. If Leap Fitness Group's eight apps share one policy, will RQ1 to RQ3 be reported per app, per policy or per provider?
3. Will the interface coding separate provider-written text from Android and Health Connect system text?
4. What is the ethical and legal basis for querying `/store/search` despite robots.txt, and would a manual logged-out search have produced a different sample?
5. Will you record the language of each policy and interface, given that rule I7 admits apps offered only in English to German consumers?

### Minor Issues
None beyond W2 and W4 to W8.
