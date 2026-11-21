contract_role: domain
## Dimension Scores

### D1: methodology_rigor
score: not_assessed

### D2: domain_accuracy
score: warn
trigger: "a main literature strand is missing or covered only by a secondary source, a legal or prior-work statement is imprecise without changing the argument, a term is used loosely, an absence claim is stated more broadly than the cited evidence supports, or the fit between the harm typology and the harm-tree approach is asserted without explanation"

### D3: argumentative_coherence
score: not_assessed

### D4: cross_disciplinary_relevance
score: not_assessed

### D5: writing_and_structure
score: not_assessed

### D6: venue_fit_and_contribution
score: not_assessed

## Review Body

### Reviewer Identity
Senior researcher in health-app privacy (privacy-policy analysis, femtech, Google Play Data Safety sections). Peer Reviewer 2, domain seat. Scope: Chapters 2 to 4 and the results of the sample as written; the empty introduction and the missing discussion and conclusion are not judged as such.

### Confidence Score
4. Every cited study was checked against the PDF in the literature library (Malki et al. 2024; Huckvale et al. 2019; Zou et al. 2019; Hutton et al. 2018; Citron and Solove 2022; Knabenhans et al. 2026; Article 29 WP WP260; Salehzadeh Niksirat et al. 2024; the StatCounter captures). The GDPR text is not in the library, so I checked the GDPR statements against the official text as I know it. Confidence is an uncertainty/scope disclosure only; it never changes consensus counts, severity, decision bearing, or arbitration.

### Calibration Status
`NOT_CALIBRATED`

### Criterion-Bound Judgements
| Dimension / criterion | Criterion source | Judgement | Evidence anchors | Rationale | Uncertainty or scope limit | Decision bearing? |
|---|---|---|---|---|---|---|
| D2: related work covers the key strands with few citations | Reviewer Configuration Card, review focus 1 | PARTLY_MEETS | see S5, W2, W8 | Harms, policy-versus-practice and risk wording are covered with eight sources; store privacy labels (Data Safety) are missing as a strand even though the sample is Android-only | Author asked for minimal citations; I only flag gaps that leave a claim or RQ scope unsupported | yes: affects the scope of RQ3 and RQ4 |
| D2: accuracy of GDPR and WP29 statements | Card, review focus 2 | PARTLY_MEETS | see S2, W3 | WP29 paragraphs are pinned and reported correctly; the "only" in the GDPR sentence is too strong and Recital 39 is missing | GDPR text checked from knowledge, not a library PDF | no: the argument survives a rewording |
| D2: fit of privacy-harm typology and harm-tree approach | Card, review focus 3 | PARTLY_MEETS | see S3, S4, W4, W5 | Both concepts are correctly sourced, but the harm definition (violation, one person) sits uneasily with harm trees that trace harms from the intended core function, and the link between types and tree roots is not stated | Methodology for building harm trees is not written yet | yes: it defines the unit of RQ1 |
| D2: each RQ motivated by a real gap | Card, review focus 4 | PARTLY_MEETS | see W1, W9 | RQ1 and RQ3 gaps hold in substance; RQ2 and RQ4 gap statements omit what the key cited study already reports | Gaps judged against the library and my knowledge of the field | yes: the novelty claim for RQ2 to RQ4 must be repositioned |
| D2: absence claims hold against the literature | Card, "will particularly care about" | PARTLY_MEETS | see W1, W9 | Absence claims are absolute where the evidence base is two to three studies; one is partly contradicted by Malki et al. 2024, section 4.2.7 | Not a systematic search on my side | yes, through W1 |

Do not total, weight, average, or mechanically map these judgements to the recommendation.

### Summary Assessment
The draft asks what health tracker providers tell users about downstream privacy harms and how they frame protection, and it rests this on a clear conceptual move: a protection claim can be true while a harm stays possible, because harm trees show pathways that come from the core function of a system (Knabenhans et al.). This is a real and useful contribution to health-app privacy research, which has mostly compared stated practice with actual practice and has not coded provider texts for harms. The citations are few, and the numbers taken from them are reported correctly; the WP29 paragraphs and the Malki section pin check out.

The domain weaknesses are repairable and concern the gap argument rather than the study. First, the gap statements for RQ2 to RQ4 understate the main cited study: Malki et al. already report breach-risk acknowledgements, responsibility shifting, safeguard claims and cross-surface contradictions in protection claims. The thesis keeps its novelty (systematic stance coding across harm types, protection claims set against harm pathways, a general tracker sample), but must say so precisely. Second, the Android-only study excludes the Google Play Data Safety section from its surfaces without a reason, although that section carries provider-declared protection claims. Third, the harm definition and the harm-tree approach need one explicit bridge. Smaller points concern the word "only" in the GDPR sentence, the origin of harm trees, the scope of Huckvale et al., and how the thesis describes the Malki ranking.

### Strengths

### S1: Numbers and pins from prior work are reported correctly
I checked every count against the PDFs: Huckvale et al. 33 of 36 apps and 12 of 28 (Results and Table 2); Zou et al. 161 notifications, 112 with hedge terms, 9 linking breached data to misuse (Section 5, p. 7); Malki et al. 13 of 19 policies on law-enforcement access and the FAQ contradiction (Section 4.2.5, p. 8), 20 apps (p. 4) and the 12 search terms (Section 3.1); Hutton et al. 64 apps and the 15 health keywords (p. 5, Table 2). All are correct.
**Evidence Anchor**: text: §3.3 (manuscript.md l.132-133) "analysed 161 data breach notifications: 112 used hedge words such as"

### S2: WP29 transparency guidance is represented accurately and with paragraph pins
Paragraph 10 does recommend that for complex, technical or unexpected processing controllers separately spell out the most important consequences; paragraph 35 covers layered notices and paragraph 39 push and pull (just-in-time) notices. The thesis also correctly separates the operative duty from guidance.
**Evidence Anchor**: text: §2.2 (manuscript.md l.65-67) "it recommends that for complex or unexpected processing providers also explain the most important consequences"

### S3: A clear, transferable conceptual core
The idea that a true protection claim can leave a harm possible is taken correctly from Knabenhans et al. (abstract and Section 4.5 of the preprint: PETs reduce information flows but every analysed harm keeps a pathway in the core functionality or its digital nature). It gives RQ3 a test that goes beyond checking whether a claim is true.
**Evidence Anchor**: text: §2.3 (manuscript.md l.81) "A protection claim can therefore be true and still leave a harm possible."

### S4: The harm typology is cited from the original source and listed correctly
Citron and Solove (2022, Part V, p. 831) group privacy harms into exactly the seven types named, in the same order. Knabenhans et al. use the same typology for their impairment notion (Section 4.1), so the pairing has a precedent.
**Evidence Anchor**: text: §2.1 (manuscript.md l.41-42) "Citron and Solove sort privacy harms into seven types"

### S5: Gap logic organised by research strand
Each related-work section ends with the question it leaves open, which makes the link between literature and RQs easy to check with only eight sources.
**Evidence Anchor**: text: Chapter 3 intro (manuscript.md l.92-93) "Each section ends with the question that its line of research leaves open."

### Weaknesses

### W1: Gap statements for RQ2 to RQ4 understate what Malki et al. already report
Section 3.2 says that in prior studies "harms are part of the researchers' threat model, not something the provider's text is examined for", and Section 3.3 states that for health trackers the wording of harms "has not been studied". Malki et al. (2024), the key cited study, examined provider texts on exactly these points, if only descriptively. In Section 4.2.7, 18 of 19 policies describe safeguards (encryption in transit, de-identification, data minimisation). All 19 contain liability statements saying that the risk of a breach cannot be removed, and 9 of 19 disclaim responsibility for third parties and shift the duty to review their policies to the user. In Section 4.2.5 one app claims that anonymisation would stop it from producing period data in answer to a subpoena, which is a provider claim aimed at one harm pathway. Section 5.2 reports contradictions across policies, Data Safety sections and interfaces about deletion and sharing, which are protection claims. The RQ4 gap sentence in Section 3.2 mentions harms only, yet RQ4 also compares protection claims across surfaces, which Malki et al. partly did. Female health apps fall under the thesis's own definition of a health tracker (six are in the sample), so the absolute claim does not hold as written.
The novelty survives. No study codes stance systematically across harm types, sets claimed protections against the harm pathways they would have to cut, or does this for a general tracker sample. The gap sentences should say this and acknowledge Malki et al. Sections 4.2.5 and 4.2.7 as descriptive precursors. This also gives RQ2's "user's responsibility" category and its "acknowledge" and "qualify" categories within-domain support (the same paper, no new citation), so the argument no longer rests only on the analogy with US breach notifications.
**Severity**: Major
**Evidence Anchor**: text: §3.3 (manuscript.md l.138-140) "For health trackers, the wording of harms has not been studied, and no study relates a claimed protection to the pathways to harm"
**Confidence**: 5 — verified in the Malki et al. 2024 PDF, Sections 4.2.5, 4.2.7 and 5.2

### W2: The Google Play Data Safety section is excluded from the surfaces without a reason
The study is Android-only, yet "surface" covers only the privacy policy and the app interface. The Data Safety section is the privacy summary that Google requires developers to complete and shows on every store page. It contains provider-declared protection claims, namely whether data are encrypted in transit and whether users can ask for deletion, as well as "no data shared" declarations (Malki et al., Section 3.2). Malki et al. found that all 8 of 20 apps whose Data Safety section said they share no personal data described sharing in their policies, and that 8 of the 19 apps declaring encryption in transit did not mention it in their policies (Section 4.1). Its exemptions, for example for data shared for legal reasons, leave law-enforcement disclosure out by design (Section 5.2). These are RQ3 and RQ4 material. The related work also has no strand on store privacy labels, the one place where the thesis's protection claims are standardised.
Norm evidence: Android privacy-communication studies analyse the Data Safety section next to the policy (Malki et al. 2024, Sections 3.2 and 4.1, already cited), and Xiang et al. (arXiv:2511.13576, in the library) treat data safety, privacy policy and permission manifest as Google Play's transparency channels.
Minimum remedy: state in Section 2.1 why the Data Safety section is not a surface (for example, it uses a vocabulary that Google fixes, it has no free text in which a harm could be named, and Malki et al. already compared it with policies), and name the exclusion as a limitation of RQ3 and RQ4. Stronger option: code only its sharing and security-practice declarations as a structured third source for RQ3. This is cheap because the fields are fixed.
**Severity**: Major
**Evidence Anchor**: text: §2.1 (manuscript.md l.38-39) "This thesis looks at two surfaces: the privacy policy and the interface of the app"
**Confidence**: 4 — Malki et al. sections verified in the PDF; the Data Safety form fields come from my knowledge of the Play Console form

### W3: The GDPR sentence on consequences is too absolute and leaves out Recital 39
"Consequences must be explained only for automated decisions" is not literally correct. Art. 13(2)(e) also requires informing about "the possible consequences of failure to provide such data", and Art. 34(2) with Art. 33(3)(c) requires a breach communication to describe the likely consequences. Art. 14(2)(g) is the Art. 14 counterpart of Art. 13(2)(f) and is not cited. More importantly for the argument, WP29 paragraph 10 bases its consequences recommendation on the fairness principle (Art. 5(1)(a)) and on Recital 39, which says natural persons "should be made aware of risks". So the GDPR itself names risk awareness, in a recital, although no operative article requires an explanation of harms. Suggested wording: "Among the information to be given at collection, only Art. 13(2)(f) and 14(2)(g) require the envisaged consequences of processing to be explained; Recital 39 and the fairness principle underlie WP29's recommendation to explain the most important consequences more generally." The conclusion of Section 2.2 then still holds.
**Severity**: Minor
**Evidence Anchor**: text: §2.2 (manuscript.md l.61-62) "Consequences must be explained only for automated decisions with legal or similarly significant effects"
**Confidence**: 4 — WP29 paragraph 10 verified in the PDF; GDPR articles and recital from the official text, not a library PDF

### W4: The harm definition and the harm-tree approach are not connected
Privacy harm is defined as the consequence of "a privacy violation" for "a person". This is close to Citron and Solove, whose typology is built "for courts" to remedy privacy violations (p. 793-794). Harm trees as used by Knabenhans et al. (Section 4.1) define harm as an impairment relative to a usual context. They include harms to groups and society, and their central finding is that harms arise from the intended, possibly lawful, core function. If "violation" means unlawful processing, the definition excludes exactly the harms that Section 2.3 and RQ3 rely on. The thesis should also say how the seven types relate to tree roots. Knabenhans et al. root their trees in concrete harms taken from the literature (for example discrimination or targeted-advertising harms) and use the typology as the impairment dimension. Two short additions would close the gap: a sentence saying that harm does not require an unlawful act (or that "violation" is meant in the contextual sense) and whether group harms are in scope, and a sentence saying that each tree's root is a concrete harm classified by one of the seven types. Also state whether Citron and Solove's "failure to inform" autonomy harm is in scope; counting it would make RQ1 partly circular.
**Severity**: Minor
**Evidence Anchor**: text: §2.1 (manuscript.md l.40-41) "A negative consequence that a privacy violation has for a person."
**Confidence**: 4 — Citron and Solove pp. 793-794 and 831-861 and Knabenhans et al. Section 4.1 verified in the PDFs

### W5: Harm trees are attributed to a secondary source, and the levels are renamed
Knabenhans et al. state in Section 4.1 that their method is "based on harm trees" from De and Le Métayer (2016, 2017; their references 16 and 17), and both works are already in references.bib. One clause ("harm trees, introduced by De and Le Métayer and adapted by Knabenhans et al.") would attribute the method correctly without adding weight. The thesis also renames Knabenhans's levels inconsistently: "parts of a system" (Section 2.1), "data flows" (RQ1) and "system components" in the source, which also cover requirements and interactions, not only data flows. The source also allows incapabilities (for example being unable to access a service), which "a capability that these parts give someone" leaves out. Section 2.3's "core function" shortens Knabenhans's "core functionality or its digital nature". Pick one term for each level and use it in both the Key Terms and RQ1.
**Severity**: Minor
**Evidence Anchor**: text: §2.1 (manuscript.md l.47-48) "combines the pathways that lead to one harm"
**Confidence**: 5 — Knabenhans et al. Section 4.1 and reference list verified in the PDF

### W6: Law-enforcement access is called a statement about consequences
In the thesis's own pathway terms, disclosure to authorities is a data flow (a system component), and prosecution or loss of safety is the harm. Malki et al. themselves present it as a sharing practice that "could lead to dire physical safety consequences" (Section 4.1). Calling it a consequence blurs the flow, capability and harm levels that RQ1 asks coders to keep apart. Write "statements about disclosure to authorities, a flow that can lead to harm, appear only in passing".
**Severity**: Minor
**Evidence Anchor**: text: §3.2 (manuscript.md l.116-118) "Statements about consequences appear only in passing: 13 of 19 policies said that law enforcement"
**Confidence**: 4 — terminology judgement; source passage verified in Malki et al. Sections 4.1 and 4.2.5

### W7: The Malki ranking is described imprecisely
Malki et al. ranked apps by the number of reviews "received in the preceding 12 months", chosen on purpose to include newer, rising apps (Section 3.1, p. 4). The thesis ranks by cumulative German review count, which favours older apps. Citing Malki et al. as having "also" ranked by reviews hides this difference. Write "also used reviews as a popularity proxy (counted over the last 12 months)" and note that the thesis uses the cumulative count.
**Severity**: Minor
**Evidence Anchor**: text: §4.4 (manuscript.md l.257-258) "also ranked Google Play apps by their number of reviews"
**Confidence**: 5 — verified in Malki et al. Section 3.1

### W8: Huckvale et al. are used beyond their scope
Huckvale et al. studied depression and smoking-cessation apps, most of which are not health trackers under the thesis's definition. Most transmissions they observed carried identifiers and usage data: only 2 of 36 apps sent user-reported health status (a health diary entry, substance use), and no other sensitive data such as names, dates of birth or medical data were seen in transmissions to third parties (Results). In a section titled "Harms of Health Tracking", "Health apps also pass data on" can read as health data being passed on. Also, "only 12 disclosed this" means that 12 of 28 policies "made a specific reference to data sharing with Google", that is, named Google. Say "mental-health apps" and "named Google", or replace the example with a tracker study if one is at hand.
**Severity**: Minor
**Evidence Anchor**: text: §3.1 (manuscript.md l.100-101) "Health apps also pass data on: 33 of 36 depression and smoking-cessation apps sent data to third"
**Confidence**: 5 — verified in the Huckvale et al. 2019 PDF, Results and Table 2

### W9: The RQ1 absence claim is absolute on a two-study basis
"It has not been collected into a list of the harms" is broadly true: most work lists inferences or threats. Iwaya et al. 2023 (in the library), for example, map mental-health app findings to LINDDUN threats rather than harms. But the cited survey itself links inferences to adversaries (insurers, employers, advertisers) who may "discriminate" (Salehzadeh Niksirat et al., end of the inference part of Section 4). A qualifier such as "we found no study that organises this evidence into harms for health trackers" makes the claim safe without more citations.
**Severity**: Minor
**Evidence Anchor**: text: §3.1 (manuscript.md l.105-106) "It has not been collected into a list of the harms that apply to a health tracker"
**Confidence**: 3 — judgement about how broad the claim is; survey passage verified in the PDF

### Detailed Comments

#### Literature Review
- Coverage: the three strands (harms of tracking, policy-versus-practice communication, risk wording) fit the RQs, and eight sources are enough for a bachelor's thesis that wants few citations. The missing strand is store privacy labels (W2). No other gap leaves a claim unsupported.
- Integration quality: the synthesis is critical rather than a list; each strand ends in a gap.
- Research gap argument: convincing for RQ1 and RQ3 in substance. For RQ2 and RQ4 it needs to be repositioned against Malki et al. (W1). RQ2's motivation currently rests on breach notifications (Zou et al.), a genre that US law mandates after an incident; Malki et al. Section 4.2.7 gives within-domain evidence at no citation cost. If a source for the stance categories themselves is wanted, Pollach (2005), already in references.bib, gives a typology of communicative strategies in privacy policies (for example mitigation and obfuscation). That would be the single addition I would accept.
- WP29 paragraph 35 says the layers of a notice should "not provide conflicting information". This is a ready normative anchor for RQ4 from a source the thesis already cites.

#### Theoretical Framework
- Appropriateness: harm trees fit RQ1 and RQ3 well. Starting from harms, they suit a study that asks which harms communication leaves out, better than threat taxonomies such as LINDDUN, which stop at threats.
- Application depth: so far the framework is defined but not yet applied, which is expected while the methodology covers only the sample. The bridge between the seven types and tree roots must be stated before the coding chapter (W4).
- Alternative frameworks: contextual integrity would give an alternative sense of "violation" if the author keeps that word; one sentence is enough.

#### Academic Argument Quality
- Factual accuracy: all cited numbers are correct (S1). Imprecisions: the GDPR "only" (W3), the scope of Huckvale et al. (W8) and the Malki ranking (W7). The StatCounter September figures (72.3 %, 39.3 %) are consistent within rounding with the October capture in the library (Android 72.29 %, Samsung 39.74 %, Xiaomi 21.34 %, which is about 30 % of Android). The September page itself is not archived; that is a reproducibility matter for the methodology seat, not scored here.
- Argument logic: the step from "PETs leave core-function pathways" (EU digital identity) to health trackers is an analogy. It is reasonable, and RQ3 will test it empirically.
- Terminology: the level names of the harm tree drift (W5), and a flow is called a consequence (W6). "PETs" in the main RQ and "protective measures" in RQ3 should be aligned, or the difference explained.

#### Contribution to the Field
- Incremental contribution: it moves health-app privacy research from "does the policy match the app" to "does the provider's communication cover the harms the app makes possible, and how does it frame protection against them". This is a real, mostly empirical and conceptual increment.
- Positioning: clear against Huckvale et al. and Zou et al., and too sharp against Malki et al. (W1).
- Overclaiming: the absolute absence claims (W1, W9) are the only risk. The RQs themselves do not overclaim.

#### Missing Key References
- De and Le Métayer (2016), already in references.bib: the original source of harm trees (W5).
- Pollach (2005), already in references.bib: optional, a privacy-policy-specific typology of communicative strategies to ground the RQ2 stance categories. I have not read the full text in this session; its existence and DOI come from the bibliography entry.
- No new source is needed for W1 to W3: Malki et al. Sections 3.2, 4.1, 4.2.5, 4.2.7 and 5.2, WP29 paragraph 10 and GDPR Recital 39 and Art. 13(2)(e) are all in sources the thesis already cites.

~~~yaml suggested-references
- title: "Privacy Harm Analysis: A Case Study on Smart Grids"
  authors: ["De, S. J.", "Le Métayer, D."]
  year: "2016"
  doi: "10.1109/SPW.2016.21"
  arxiv_id: null
- title: "A Typology of Communicative Strategies in Online Privacy Policies: Ethics, Power and Informed Consent"
  authors: ["Pollach, I."]
  year: "2005"
  doi: "10.1007/s10551-005-7898-3"
  arxiv_id: null
~~~

### Questions for Authors
1. Is the Data Safety section left out of the surfaces on purpose, and on what domain grounds, given that it carries provider-declared encryption, deletion and sharing claims?
2. In RQ1, is a "harm identified for the app" one of the seven Citron and Solove types, or a concrete harm (for example prosecution after pregnancy data are disclosed) that is then classified by type?
3. Does "privacy violation" in the harm definition include lawful processing in the core function, and are harms to groups in scope?
4. Where do the RQ2 stance categories (acknowledge, qualify, minimise, deny, user's responsibility) come from?
5. Is Citron and Solove's "failure to inform" counted as a harm? If so, how does RQ1 avoid counting the communication gap it measures as a harm?

### Minor Issues
- Editorial suggestions only, beyond W3 to W9: cite WP29 paragraph 35's consistency expectation for RQ4, and tie the RQ2 "deny" category to Zou et al.'s "no evidence" claims (Section 5, p. 7), which the thesis already cites.
