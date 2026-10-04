# Proposal readiness review — 5 October 2026

**Verdict: revise before delivery as the finished proposal.** The topic is worthwhile, the main research question matches the supervisor's written input, and the document is readable and professionally typeset. However, the current version contains a consequential overstatement of GDPR obligations, an unsupported transfer of the harm model into an automatic overclaim rule, a factual citation error, and contradictions in the planned study. These are substantive issues, not merely proofreading. It is suitable for discussion as a draft if those unresolved questions are explicitly identified.

This review concerns proposal readiness, not completion of the thesis or approval by the supervisor/examination office.

## Scope and evidence

I read the current seven-page `03_Thesis/proposal/proposal.pdf`, its complete TeX source, the shared bibliography, and all nine files under `00_Admin`, including both original PDFs. I rendered and visually inspected every proposal page and the three pages in the original admin PDFs. I inspected the existing LaTeX/Biber logs and checked the correspondence between the 28 citation keys and bibliography entries. I also read relevant passages in the available literature PDFs and consulted the sampling protocol, both codebook versions, the walkthrough protocol, and the literature index where they resolved questions raised by the proposal.

External checking included all 15 DOI-bearing references through Crossref metadata, primary publisher/author sources for important claims, and targeted searches for closely related work. This was not a systematic literature review, an exhaustive legal review, or a full reading of every cited book and article. A verified bibliographic record does not by itself validate every interpretation of that source. The original proposal, bibliography, admin files, and study instruments were not edited or rebuilt.

Page numbers below mean PDF viewer pages: the document currently has no printed page numbers. TeX line numbers refer to the version reviewed.

## Findings to resolve before delivery

### 1. The legal gap is stated too categorically

**Priority: high. Location: p. 1, Background; `proposal.tex` lines 138–162; repeated on p. 2, lines 185–191.**

The statements that “to personalise your experience” is enough even for pregnancy or illness estimation, that users learn inferences “only on request,” and that all advance harm communication outside solely automated decisions is voluntary are not established by the cited provisions. Profiling is a form of processing; merely naming it does not necessarily identify a sufficiently specific purpose. The argument also reduces transparency duties to data flows despite the binding fairness/transparency principle and clear-information requirements. See [GDPR Articles 5 and 12](https://eur-lex.europa.eu/eli/reg/2016/679/).

The fact that recitals and guidelines are not independent operative legislation does not make their interpretation of binding duties irrelevant. As a concrete counterexample to treating vague personalisation language as sufficient, [EDPB Opinion 08/2024, paragraphs 148–150](https://www.edpb.europa.eu/system/files/2024-04/edpb_opinion_202408_consentorpay_en.pdf) requires specificity in its particular large-platform behavioural-advertising context. Its scope should not be silently extended to all trackers; it nevertheless undermines the proposal's blanket assurance.

**Correction:** frame the contribution as an empirical examination of downstream-consequence communication, without needing to prove a universal legal exemption. Suggested replacement:

> The study examines how providers communicate possible downstream privacy harms alongside information about their data practices. It does not assess legal compliance or assume that all such communication is voluntary.

Also distinguish an information obligation from the surface on which it is fulfilled: required notices can appear in an interface. Narrow “solely automated decisions” to the relevant Article 22 category where appropriate. Avoid turning the proposal into a legal thesis merely to sustain an unnecessarily broad motivating claim.

### 2. The tracker harm tree does not establish the claimed impossibility of protection

**Priority: high. Location: p. 1, lines 121–135; p. 3, lines 357–371; pp. 6–7, lines 569–630 and 686–690.**

The appendix goes from locally logged period dates to pregnancy inference to prosecution, then calls this a path consisting only of a core component that no PET can close. It omits essential conditions: who obtains the data, how they access it, whether it is identifiable, what additional evidence or inference is needed, and the applicable legal/social setting. The beneficial prediction available to the user is not automatically an adversary's inference capability. An adversary's access to readable data is precisely something protections may affect.

The source paper models specific entities, interactions and leakage, and combines components using AND/OR conditions. Its PET argument is explicitly bounded to PETs inside its defined EUDIF system, with broader infrastructural changes outside scope. The proposal cannot import the conclusion merely by relabelling stored tracker data “core.” See the local Knabenhans PDF, §4 and §4.1, printed pp. 6–7, and [the source record](https://eprint.iacr.org/2026/867).

**Correction:** adapt the method rather than claim it “transfers directly.” Name the adversary, asset, access conditions and contextual assumptions on each pathway. Distinguish data existing from data being available to an adversary. Use “may enable” rather than the unconditional “leads to” in the illustrative graph. Specify the jurisdiction of prosecution examples and explain their relevance to German-storefront apps; do not imply that the US context can simply stand for Germany.

### 3. The automatic `OVERCLAIM` rule is stronger than the evidence allows

**Priority: high. Location: pp. 3–4, lines 357–371, 424–426, 450–452 and 471–476; p. 7, lines 759–763.**

“On-device processing protects your reproductive privacy” need not promise elimination of every conceivable harm. A residual path does not alone disprove a claim of partial protection, or protection against a specific actor. The proposed rule collapses risk reduction, scoped prevention, vague reassurance, and absolute guarantees. It also says “no judgement is left to the model,” although the model still determines the promise's meaning and scope.

Table 2 says its constructed sentence is “accurate” solely because its measures concern implementation. That establishes neither actual deployment nor truth. The scope section explicitly excludes verifying whether claims are true.

**Correction:** code the claimed measure, actor, protected data, outcome, scope and strength separately. Use a category such as “potential mismatch with the reference threat model,” subject to manual adjudication and stated assumptions. Reserve a definite overclaim for explicit guarantees contradicted within that same scope. Acknowledge partial protection. Replace “the sentence is accurate” with “the sentence makes a data-flow claim without naming a downstream harm.” Treat “not selling data” as a practice commitment, not automatically a PET.

### 4. The literature gap needs narrowing and another comparison

**Priority: high. Location: Abstract; pp. 1–2, lines 166–193 and 236–239.**

The two-part account of prior work as truth checking versus user beliefs is useful but incomplete. A targeted search found [Doan, Doğan and Rossi, *Analysis of Transparency and User-relevancy of DTC Company Policies*](https://orbilu.uni.lu/bitstream/10993/61227/1/PrivIno2024_paper_46-3.pdf). It examines six genetic-testing companies' privacy/research-consent policies, including available risk/benefit information and missing collective risks. This is an adjacent domain, not proof that the proposed tracker study has already been done. It does require comparison before claiming that provider harm communication has barely been studied or has never been mapped before an incident.

**Correction:** claim the specific combination of fitness/fertility trackers, cross-surface communication, harm/capability coverage, stance and PET framing. Explain how this differs from risk communication in other sensitive-data services. Maintain a dated search log and comparison matrix. A proposal may promise further literature review; it should label the current gap as provisional rather than established exhaustively.

### 5. Correct the Huckvale statistic

**Priority: high factual correction. Location: p. 1, lines 166–168; bibliography comment for `huckvale2019assessment`.**

“29 of 36 ... while only 12 disclosed it” mixes different denominators. The paper reports 29/36 transmitting to Google or Facebook services, but the specific-name disclosures are 12/28 for Google and 6/12 for Facebook. Its results also distinguish general transmission disclosure from naming the company. See [Huckvale et al., abstract and results](https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2730782).

**Suggested replacement:**

> Huckvale et al. found that 29 of 36 apps transmitted data to Google or Facebook services; only 12 of 28 apps transmitting to Google and 6 of 12 transmitting to Facebook named the respective company in their policies.

For brevity, omit the disclosure numbers rather than merge them incorrectly.

### 6. The recall audit cannot establish general recall or whole-provider silence

**Priority: high. Location: p. 3, lines 481–504; p. 4, lines 529–538.**

The blind manual set, pilot separation, quote evidence and attention to false negatives are strengths. However, recall measured on lexical hits is conditional on the sweep finding those hits. It does not measure recall among implicit or differently worded mentions outside that set. Adding positives until there are 30 per code also requires a clear sampling and interval procedure. A confidence interval does not eliminate selection bias. This matters because absence is the headline outcome.

The two-of-three retention rule can discard real mentions found only once. It should be justified empirically against the recall objective rather than assumed to be a validation step. Repeated model runs are not independent human annotations. Missing evidence spans should trigger review or repair, not silently turn into evidence of absence.

**Correction:** keep separate reports for the untouched random validation set and the enriched challenge set. Manually examine a random sample outside the lexical sweep and, preferably, fully code a small set of held-out apps. Report per-code denominators and uncertainty, including when recall is unestimable. Decide what happens when validation is inadequate: further manual coding, revising the instrument, or omitting the affected quantitative claim. Route singleton positives to manual review if feasible. Assess app-level detection as well as unit-level detection because final prevalence is app-level.

“No mention found in the captured material” is defensible. “The provider never names X” is not justified by sampled surfaces plus imperfect detection. The limitations paragraph currently reverts to the stronger claim after the earlier caveat.

### 7. Reconcile the 12-app interface study with the 50-app claims

**Priority: high, straightforward fix. Location: Abstract; p. 2, lines 306–314; p. 7, lines 731–733 and 755.**

The method and Table 3 specify interface walkthroughs for 12 apps. Appendix A says all 50 apps are studied on all four surfaces, including their screens. These describe different studies. For the other 38 apps, interface evidence is unobserved, not absent.

**Correction:** consistently state “document analysis for 50 apps; interface analysis for a 12-app subset.” Define app-surface availability and denominators. Treat not collected, inaccessible, not applicable and coded-but-no-mention as separate states. RQ4's policy/interface result applies to that subset. The sampling protocol already specifies no duplicate app in the walkthrough slots; preserve this rule in the proposal or explicitly reference the protocol.

### 8. The coding examples do not consistently obey the rules

**Priority: high for instrument credibility. Location: Table 1 and Appendix A.**

Several boundary cases need a consistent decision before they are presented as a complete codebook:

- Axis A has no explicit “no relevant content” outcome, although P5 uses a dash. Ordinary policy paragraphs about contact details or rights will also need a defined treatment.
- Table 1 accepts “Your data could be used against you” as harm acknowledgement, while P3's promise to prevent “anyone using it against you” receives component only. Decide whether generic misuse is a harm mention, a separate generic-risk code, or insufficiently concrete; apply that rule regardless of whether the sentence asserts or denies it.
- The deflection example, “You are responsible for securing your phone,” does not itself name a harm, despite Axis B requiring one. Supply its context or replace the example.
- “In the unlikely event” qualifies a breach in P4; it is not direct evidence that the consequence, conditional on the breach, is unlikely. Record what the hedge qualifies. Do not equate all uncertainty language with misleading minimisation.
- Specify how multiple harms and multiple stances within a paragraph are linked. Recording only the highest level is useful as a summary, but cannot by itself count every component/capability node named.
- The appendix's “2 of 6” denominator includes nodes never established in the displayed three-node pathway. Show the full illustrative baseline or explain that the graph is only one branch of a larger tree.

## Important improvements to the design and wording

**9. Make the taxonomy choice explicit.** The proposal's seven labels match Knabenhans Appendix A; this is not simply a false attribution in the current proposal. However, Citron and Solove's original seven include relationship harms, whereas the adopted list includes societal harms. `Open-Points.md` still says the original typology is the backbone and the two models are “not merged.” Codebook v2 supersedes v1 and follows the new model, so the admin decision is stale. Explain the adaptation and how relationship harms such as damage to trust or intimate relationships will be represented. See [Citron and Solove, contents and Part V](https://www.bu.edu/bulawreview/files/2022/04/CITRON-SOLOVE.pdf).

**10. Bound “absence” to applicable harms.** A domain tree is a useful reference, but not every branch applies to every app. A sleep tracker, calorie diary and location-tracking running app need not have identical applicable pathways. Add a justified applicability decision; distinguish irrelevant harms from relevant harms left unmentioned. Do not describe the tree as “everything a provider could tell users.” It is a literature-derived reference model, with a limited scope.

**11. Clarify corpus collection and sampling.** The separate protocol supplies a cross-store weighted-ranking rule missing from the proposal. Briefly reference it. Still specify what happens if the 1,000-rating threshold yields fewer than 20 eligible fertility apps, how overlapping domains are assigned, and how identical/shared provider policies are handled. Clarify whether both store listings are captured. Log policy-inaccessible apps as exclusions with their own denominator; excluding them selects for providers that already communicate more. “Highest-rated among the retrieved eligible candidates” is more accurate than highest-rated across the German market. The claim that findings describe what users “most likely meet” is unsupported without exposure or market-share evidence.

**12. Set a language rule and collection boundary.** “German versions are coded, English ones checked against them” does not specify what happens when only English exists or when the versions disagree. Define the primary locale, English fallback, treatment of disagreements and reporting of language-specific validation. Specify which website pages/blog dates/search depth are collected. Otherwise “absent” depends on how long the researcher happens to search. Opportunistic ads need a separate availability indicator; not treating missing ads as a finding is a good existing decision.

**13. Separate surface differences from misleading inconsistency.** A short onboarding screen and a full policy serve different purposes. A missing sentence on one screen is a visibility difference, not automatically a contradiction or defect. For RQ4, distinguish contradictory claims, differences in detail and differences in availability at a defined decision point. Specify what counts as that point and whether linked/layered information counts.

**14. Remove language that anticipates the result.** “The very silence the thesis sets out to establish” (lines 491–492) makes the outcome appear predetermined. Use “silence the study seeks to assess.” Appendix P4 says a named harm “is rare,” but the example cannot establish corpus prevalence. “The most serious harms” requires a severity assessment not included in the method. Use “other harms in the reference model.” The walkthrough protocol's repeated “expected to fail” language also risks directing the researcher; rephrase as a hypothesis with explicit success criteria and equal attention to counterexamples.

**15. State what the study can infer about users.** Document/interface analysis can identify communication and availability, not demonstrate what users understand, believe, or infer causally from it. Prior user studies motivate the work; they do not measure the effect of the sampled providers' current text. In the importance section, qualify the imagined user response. Update the admin overview's implication about establishing user beliefs.

**16. Clarify expert walkthrough claims.** The separate protocol does retain Wharton's four questions, which addresses a detail compressed out of the proposal. Mention the adapted, researcher-conducted nature and link the protocol. A researcher's successful task completion is not a user-study finding about learnability or understanding. Resolve device/OS, task stopping rules, language and access to paired devices before collection.

**17. Demonstrate feasibility with the pilot.** The plan combines 50 apps, multiple languages/surfaces, 12 walkthroughs, three coding passes, 20% manual unit validation, and an enriched audit. This may be feasible, but the proposal does not demonstrate it. Replace “too large to code by hand” with a measured workload estimate after the five-app pilot: corpus units, annotation time, capture effort and model cost. Set a fallback scope. The timetable places validation and analysis around Christmas/New Year and supervisor revisions near the deadline; confirm availability and allow an earlier draft handover. Registration and the official submission date remain assumptions, not verified institutional deadlines.

**18. Resolve the submission package.** The current PDF has four content pages, one references page and two appendix pages. `Timeline.md` records a three-content-page request, and the TeX comments acknowledge a fourth page was added on 5 October. The original meeting notes list the four required sections but no page count, so the available evidence for the three-page limit comes from the tracker/source comments. Either return to the documented limit or explicitly obtain agreement to the extension. Do not silently assume the appendix is excluded by the supervisor merely because the source comment says so.

**19. Present authorship and version clearly.** The advisor is typeset as a coauthor, with only a small advisor footnote; running headers also name both authors. Unless coauthorship is intended, use a separate supervisor label. Add a proposal date/version. Verify whether ACM two-column US Letter is acceptable; it is not itself an error, but no official template requirement was demonstrated.

## Language, clarity and scientific tone

The English is generally fluent, readable and consistent in British spelling: “minimise,” “behaviour,” “analysed,” and “personalise” fit together. The German degree title is an institutional name, not a language error. The plain-language explanation of coding is useful. No wholesale language rewrite is necessary.

The main style weakness is categorical and sometimes prosecutorial phrasing. Scientific tone comes from bounded claims and operational definitions, not from making the prose more complicated. The opening legal argument is unusually prominent and too confident; it currently distracts from the empirical contribution.

| Current wording | Recommended direction |
|---|---|
| “whether providers tell the truth” | “consistency between disclosed and observed data practices” |
| “The model transfers directly” | “We adapt the harm-tree method to tracker communication” |
| “no PET can remove that capability” | distinguish intended user functionality from a specified adversary's access |
| “the promise cannot be kept” | “the claim may exceed the protection supported by the stated threat model” |
| “ships with its quote” | “is accompanied by its supporting quotation” |
| “so no judgement is left” | describe the fixed rule and the remaining human/model interpretation |
| “a harm is named, which is rare” | remove the unsupported prevalence statement |
| “most serious harms” | “other harms represented in the reference model” |
| “the provider does not mention” | “no mention was identified in the captured material” |
| “health trackers” / “fertility” / “period” used interchangeably | define umbrella and subgroup terms once and preserve them |

Keep future tense consistent for planned collection and analysis. Clearly label illustrative results as constructed throughout the appendix. Avoid treating a helpful explanation of the coding procedure as evidence that the procedure has been validated.

## Reference and factual audit

All 28 citation keys resolve to bibliography entries; no undefined citations were found in the existing build. All 15 cited DOIs returned matching work identities in Crossref after retrying initial rate limits. This does not mean every publication field or substantive claim was fully audited.

| PDF ref. | Work | Check and action |
|---|---|---|
| 1 | Bitkom Research, Digital Health 2025 | The 73% claim and stated survey size/method are supported by the [primary page](https://bitkom-research.de/news/digital-health-2025). Keep its population as smartphone users, not all Germans. Its visible headline differs from the bibliography's broad report title; consider using the exact page title. |
| 2 | GDPR | Genuine regulation; interpretation needs correction as described above. Official pages intermittently returned anti-bot responses. |
| 3 | Knabenhans et al., 2026/867 | Genuine preprint; local source supports the three-level framework and its seven adapted categories. The tracker application is the proposal's own extension. Pin the version: the [record](https://eprint.iacr.org/2026/867) reports a revision on 16 September 2026. |
| 4 | Citron & Solove, Privacy Harms | Published 2022, pp. 793–863, consistent with local PDF and publisher. Keeping a 2021 citation key is harmless. Original taxonomy contains relationship harms. |
| 5 | Wearable Activity Trackers survey | DOI identity verified; local abstract explicitly supports 236 studies and personality inference. Article 183 is in the bibliography source but not visibly rendered in the current style. |
| 6 | No Cookies For You! | Local published PDF supports the three-principle discussion and 1–64 page range. Do not strengthen its critique into a universal tracker impossibility claim. |
| 7 | Unfair Commercial Practices Directive | Identifiable legal source; no provision-by-provision current legal audit completed. Its general role does not establish that only one communication surface has prescribed content. |
| 8 | WP29 transparency guidelines | Endorsement and identity confirmed on the [EDPB landing page](https://www.edpb.europa.eu/documents/guideline/transparency_en). The cited direct PDF link returned 404, including when followed from EDPB. Use a functioning official record and archive the source before relying on fine-grained wording. Full original guidance text was not retrieved in this review. |
| 9 | Huckvale et al. | DOI/title verified; disclosure statistic is wrong as compressed in the proposal. Correct both prose and bibliography comment. |
| 10 | Arkalakis et al. | [USENIX record](https://www.usenix.org/conference/usenixsecurity24/presentation/arkalakis) confirms nearly 5,000 apps, 81%, authors and pp. 5645–5662. |
| 11 | Li et al., iOS labels | DOI/title/year/pages verified; identify it as CHI Extended Abstracts, as the entry already does. |
| 12 | Shipp & Blasco | DOI/title/year/pages verified. Direct full-paper interpretation was not re-audited here. |
| 13 | Malki et al. | DOI/title/year/pages verified; local PDF available and checked for the study's identity and role. |
| 14 | Hudig & Singh | DOI/title/year/pages verified; local PDF available and checked for the study's identity and role. |
| 15 | Gabriele & Chiasson | DOI identity verified against Crossref despite differing DOI printed in the stored PDF footer; retain the corrected bibliography DOI. Local abstract supports the plausibility/unlikelihood interpretation. |
| 16 | Cao et al. | DOI/title/year/pages verified; local paper supports the US post-Roe concern context. It is not proof of German prosecution pathways. |
| 17 | Zou et al. | DOI identity and pp. 1–14 verified; [author manuscript](https://yixinzou.github.io/publications/pdf/chi2019-zou.pdf) confirms 161 notifications and downplaying/obscuring risks. Add the missing page range. The proposal's four-way stance scheme is an adaptation that still needs validation. |
| 18 | Solove, A Taxonomy of Privacy | **Page range error:** the [published article copy](https://zoo.cs.yale.edu/classes/cs457/fall13/SoloveTaxonomy.pdf) ends at printed p. 560. Change `477--564` to `477--560`. DOI `10.2307/40041279` also resolves to the work. |
| 19 | Calo, The Boundaries of Privacy Harm | Work identity supported by the [author's university profile](https://www.law.uw.edu/directory/faculty/calo-ryan). The full original paper was not successfully retrieved; final page and detailed interpretation remain unverified here. |
| 20 | Wilson et al., OPP-115 | DOI/title/year/pages verified. A methods precedent, not evidence that the new harm codes are reliable. |
| 21 | Zimmeck et al., MAPS | DOI/title/year/pages verified. |
| 22 | Krippendorff, Content Analysis, 4th ed. | [SAGE](https://us2.sagepub.com/en-us/nam/content-analysis/book258450) confirms edition and ISBN; lists May 2018 release while 2019 copyright citations also exist. Cite the year of the edition actually consulted, not an inferred typo. |
| 23 | Wharton et al. | Chapter identity matches the original supervisor input and stored edited volume. Calling it an adapted cognitive walkthrough is reasonable if the four questions in the protocol are actually used. |
| 24 | Polisis | [USENIX](https://www.usenix.org/conference/usenixsecurity18/presentation/harkous) confirms record/pages and data-practice classification. It is a neural/deep-learning precedent, not a modern generative-LLM system. |
| 25 | Rodriguez et al. | DOI/title/year/pages verified; relevant LLM data-practice-analysis precedent. |
| 26 | Cohen | DOI/title/year/pages verified. Kappa is model–author agreement here, not independent human-coder reliability. |
| 27 | Feinstein & Cicchetti | DOI/title/year/pages verified. Reporting prevalence alongside kappa is sensible. |
| 28 | McDonald et al. | DOI identity/year/pages verified. No second human coder is present in the current proposal; the explicit limitation is appropriate. |

Bibliographic polish: add stable links for accessible papers lacking them, distinguish publication records from preprints, use consistent title capitalization and article identifiers, and avoid relying on broad source citations for a specific legal or conceptual proposition when a pinpoint section is available. These are secondary to the factual and inferential corrections.

## Visual and LaTeX inspection

The current PDF is seven US Letter pages. Fonts and text are readable; tables have sensible rules and alignment; no replacement glyphs or unresolved citation markers were detected. The existing log has no overfull boxes or missing-citation errors. It does contain underfull vertical boxes and float-placement warnings, consistent with some uneven spacing. I inspected the existing output rather than treating a successful compilation as visual proof.

| Page | Observation | Action |
|---|---|---|
| 1 | Strong title hierarchy, clear two-column layout; author block makes the supervisor resemble a coauthor. The bold legal claim attracts attention to the weakest assertion. | Fix legal wording and authorship presentation; add date/version. |
| 2 | Readable but dense. Main RQ and RQ1–RQ4 are easy to locate. | Preserve the clear RQ structure; shorten repeated motivation if restoring the page limit. |
| 3 | Pipeline is sharp, aligned and legible; all five boxes and arrows render correctly. | Define the 30/20 domains in the graphic if it must stand alone. Acknowledge iteration/pilot in the caption if presenting this as the complete workflow. |
| 4 | Table 1 is readable. The “C Can the protection deliver?” label is awkwardly separated vertically. Table 3 interrupts the limitations paragraph between columns; white space is uneven. | Adjust float placement and cell layout after substantive cuts; keep the limitations paragraph together if possible. Do not reduce font size to recover space. |
| 5 | All 28 references render cleanly without obvious clipping. | Correct content/links; density is acceptable for a reference page. |
| 6 | Appendix tables are readable. “makes possible” is wider than its arrow gap and crosses the adjacent node borders. The graph says “Read from the bottom up” although it runs left to right. | Increase the gap, reduce node widths or split the label; correct reading-direction text. Add a proper numbered figure/caption. The causal logic needs the larger correction described above. |
| 7 | Coding/comparison tables are legible, but appendix tables lack consistent numbers/captions and the displayed results contradict parts of the main method. | Number/caption tables where useful and reconcile the worked example. |

**Global:** printed page numbers are absent throughout. Add them for supervisor feedback. The TeX graph is a conceptual pathway, not a results plot; there are no empirical graphs or axis scales to validate. No major table/text clipping was seen, but the appendix arrow-label collision is a real local layout defect.

## Review of every file in `00_Admin`

| File | Assessment |
|---|---|
| `README.md` | Useful index. The overview asserts that providers say little/nothing about harms before the study has established it, and implies effects on beliefs the method does not measure. Examiner fields are still TODO. |
| `Open-Points.md` | Keep as a decision log. Item 2 conflicts with the new taxonomy; item 4 calls the pilot separate although it stays in the sample; item 6 requests a second human coder while the proposal uses one; introductory wording makes provisional choices sound settled. Item 1's assertion that later input “settles” scope is stronger than the evidence. |
| `Timeline.md` | Still describes a three-content-page hand-in; the PDF has four plus appendix. The 30 September send target is past as of this review. Registration/deadline are explicitly provisional and administrative checks remain open. Update statuses without pretending that drafting equals approval. |
| `Meeting-Notes/2026-09-04_Proposal-Meeting.md` | Valuable historical record. The four-section order and app/document scope are reflected in the proposal. Actions remain marked open; record subsequent completion in dated updates. The Google Doc action is still unresolved in the tracked record. Preserve what was actually said. |
| `Meeting-Notes/TEMPLATE.md` | Appropriate empty template. Its placeholders are intentional and not a delivery defect. |
| `Supervisor-Input/2026-09-05_Supervisor-Input.pdf` | Original two-page source confirms the main RQ, two domains, two stores and communication sources. It does not explicitly approve the proposed 30/20 allocation, 12-app subset, exclusion of a survey or seven-page package. Preserve the original. |
| `Supervisor-Input/2026-09-05_Supervisor-Input.md` | Useful enrichment, but “Verbatim content ... not rewritten” is too strong for a document containing added interpretations, bibliographic resolutions and later status notes. Clearly label transcription versus editorial additions. The “PDF still needed” action contradicts §11; references to proposal §7 and older §2.2/§4.6 do not match the current four-section proposal. |
| `Supervisor-Input/README.md` | Sound organizational explanation; no substantive problem. |
| `Thesis-Offer/2026-08-27_HCS-MPI_Thesis-Offer.pdf` | Original one-page offer explicitly proposes a scenario-based online user survey. The later input supports the new analysis direction, but the record still lacks explicit scope approval. This is an administrative decision to close, not proof that the current design is prohibited. |

The original PDFs are source evidence, not documents to rewrite. Clarify interpretations in the living notes. The supervisor-input filename's date discrepancy is already acknowledged, which is good provenance practice.

## Delivery checklist

- Correct the legal motivation and remove the universal voluntary-disclosure assertion.
- Repair the harm pathway and restrict the overclaim interpretation to explicit, comparable threat-model claims.
- Correct Huckvale's denominators and Solove's page range; repair the guideline link.
- Narrow and substantiate the novelty claim, including the adjacent DTC policy study.
- Reconcile 50 apps versus 12 interfaces everywhere; distinguish absence from unobserved evidence.
- Make the codebook examples internally consistent and report the enriched recall audit honestly.
- Update the active admin decisions to match codebook v2 and the current sampling/pilot plan.
- Resolve the documented page limit and the survey-to-content-analysis scope with the supervisor.
- Add page numbers/date, fix the appendix arrow label and tidy page 4, then recompile and visually inspect the revised PDF.

The central idea does not need to be discarded. A focused revision can preserve the RQ, domains, cross-surface comparison, quote-grounded coding and transparent validation while making the claims defensible. Sending the present version as final would expose avoidable weaknesses in precisely the methodological and factual areas a supervisor is likely to question.
