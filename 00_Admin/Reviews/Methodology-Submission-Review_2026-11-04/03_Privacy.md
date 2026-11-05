# Domain/privacy review — current methodology

Calibration: NOT_CALIBRATED. This is the domain/privacy role only, with a fresh role-separated context, from the same model family as the panel. No prior reviews or peer reports were read. No sprint contract, numerical scores, or venue-specific acceptance criteria were supplied. Recommendation within this remit: substantive revision before instrument freeze; the basic framework is defensible.

## Scope and evidence receipt

Read the complete current `03_Thesis/chapters/04_methodology.tex` (2,099 lines), D12, `reference_model_v1.yaml`, and `codebook_v5.md`. Line anchors below refer to that current checkout. Methodology SHA256 at review: `86528AD0CD4C5B854E7B3823A9D4328617F5AA43BB5BA5A0D3780E3CF0874AB7`. Followed the required Graphify query first and verified the returned files. Read AGENTS.md and the installed Graphify/PDF guidance; used the requested external role guidance for domain review, without its unrequested sprint/scoring protocol. Project files were read only.

Actual primary-source inspection, via PyMuPDF text extraction (no digest cards used):

- `01_Literature/library/Knabenhans_2026_PrivacyHarms-EUDigitalIdentity.pdf`: full extracted PDF pp. 6–7, 10–12, 14–15; source-wide keyword scan with excerpts from other matching pages. The relevant evidence is §4/§4.1, §4.5, §5.1, and Appendix A. This is not a full-paper or full-version-history audit.
- `01_Literature/library/De_2016_PrivacyHarmAnalysis-SmartGrids_manuscript.pdf`: full extracted slides 7, 9, 11, 13, 14, 16, 17, 19, with opening/source scan. These are presentation slides, not the 2016 proceedings paper. The De2017 full text was initially unavailable; the later HAL author-manuscript check below supersedes that initial access status.
- Zou et al. 2019, local `62_Zou_2019_...pdf`: full extracted pp. 4 and 7, plus relevant passages on pp. 2–3, 5–6, 9–13. Checked its actual study object, hedging/no-evidence argument, and limitations. Not a complete supplementary-codebook audit.
- `01_Literature/library/Martin_2025_NoCookiesForYou.pdf`: full extracted pp. 8–9, 29, 64, opening abstract and source-wide matching excerpts. Checked the three principles and the limits on transferring them; did not reanalyse the user studies or current law.
- Salehzadeh Niksirat et al. local Methods-Reading PDF: full pp. 12 and 14; Gabriele & Chiasson local PDF: full p. 5; Hudig & Singh local PDF: full pp. 2–3. These checks support the domain's inference, discrimination, intimate-partner and access scenarios, but do not audit every pathway or source. Cao, Citron/Solove, Deng and Iwaya received the additional passage checks recorded below and in the structured ledger; Malki was not independently read for this review.

## Assessment

A shared reference framework is a sensible way to avoid treating every app's own disclosures as the full universe of possible harms. The current chapter also does a good job separating observable communication from technical effectiveness, user effects and provider intent. It explicitly recognizes that literature-based trees are incomplete and that predictions for a user do not establish disclosure to an adversary. This can support a useful incremental study of what providers communicate.

The strongest remaining problems lie in how the framework is turned into observations: category-level harm mentions are credited to distinct pathways; denials are removed from a variable described as communication coverage; and executable applicability treats an underspecified combination as sufficient. These are construct-validity problems, not demands for a larger study. They can change the direction of the reported communication gap even when the text coding is perfectly reliable. Resolve those rules and align the model/codebook before freeze. A real independent source-and-pathway check remains necessary, but it is already correctly planned rather than falsely claimed complete.

## Strengths to preserve

1. **Scope discipline is unusually explicit.** Evidence anchor: text: methodology L160–166, "The study analyses what health-tracking apps communicate"; L2097–2099, "The study cannot establish provider intent, actual harms or effects on users." The synthetic walkthrough and assistant-generated stand-ins are also clearly disclosed at L1902–1914. Do not dilute these qualifications when reporting results.

2. **The adaptation of harm trees is substantive, not just a citation.** Evidence anchor: text: methodology L875–931, "Each pathway records its source"; D12 L15; model L50–93. Components, actors, capabilities, consequences, origins, and documented/argued links are explicit. Knabenhans §4.1 PDF pp. 6–7 supports those elements and non-completeness; De slides 13/16/19 support actors, causal chains and countermeasure reasoning. Neither source makes a universal tracker model automatically valid, but both support the modelling strategy.

3. **The protection-claim boundary is appropriate.** Evidence anchor: text: methodology L1681–1687, "partial protection is not rejected merely because other risks remain"; L1831–1840; codebook L216–228. Martin pp. 8–9/64 supports distinguishing data-flow changes from meaningful privacy protection. Knabenhans §4.5 PDF p. 10 also says some PETs make exploitation harder without eliminating it. The thesis appropriately avoids converting every remaining risk into a misleading-claim allegation or importing the EUDIF-specific blanket rule that only red components can be addressed.

4. **Non-findings and uncertainty are retained.** Evidence anchor: text: methodology L1486–1497, "A limit reached is a bounded non-finding"; L1557–1568; L1782–1799; L1864–1874. The separation of task outcomes, applicability and text is valuable. The decision not to infer German-law applicability from US post-Roe concerns (L1789–1791) is also sensible; it avoids presenting documented concerns in another setting as demonstrated German pathways.

## Findings and minimum repairs

### W1 — A harm category mention is not coverage of every causal pathway in that category

Severity: Major. Confidence: high, based on the chapter's own definitions and verified primary-source context requirements.

Evidence anchor: text: methodology L1803–1809, "A named harm counts for the pathways of its category." Related anchors: codebook L248; methodology L917–920; model P05–P08 (L65–68).

The same category contains materially different harms and actors. A warning about distress after account theft can currently give harm-level coverage to partner harassment and fear of legal proceedings, because all are H-PSY. Even perfect unit coding cannot justify that attribution. The codebook instead says a mention must concern the pathway's data. Knabenhans §4 PDF p. 6 makes the recipient and the semantics of disclosed data necessary to identify harms; Appendix A is a taxonomy, not a rule that its members are interchangeable.

Minimum repair: keep category mention as a separate summary. Credit pathway coverage only where the text establishes the relevant consequence and compatible data/actor/access scope; explicitly allow a category-only or scope-unclear mention without spreading it to all pathways. Preserve the existing node/data requirement and extend it to consequence/actor matching where relevant.

Evidence needed before submission: independently checked mappings for broad warnings and warnings naming one psychological consequence, with a crosswalk showing why each received pathway credit. Include a counterexample where one H-PSY pathway is covered and another is not.

### W2 — Excluding denials from coverage conflates communication with acknowledgement

Severity: Major. Confidence: high; internal construct mismatch.

Evidence anchor: text: methodology L1806–1807, "A denied node is reported as denied and does not count as coverage." Related anchors: RQ1 L99–101; RQ2 L102–103; Axis A L1667–1669; codebook S-DEN L177.

A provider that explicitly says a harm is impossible has communicated that harm. Under the current rule it may receive the same coverage level as a provider that never names it, despite denial being one of the intended stance findings. Reporting the denial elsewhere helps, but does not make a "missing harm" or silence interpretation of that coverage variable correct. This is especially important for the research question about harms providers acknowledge or downplay.

Minimum repair: derive explicit mention independently of assertion status. Report acknowledged/possible mentions and denied/prevented mentions separately, while retaining all mentioned nodes. If the author deliberately wants an acknowledgement-only measure, name it accordingly and never equate its complement with silence or unmentioned harms. No need to redefine every denial as acknowledgement.

Evidence needed: constructed and then pilot-tested cases for silence, possible harm, outright denial, and a protection claim that prevents a named harm. The reported tables must preserve those distinctions.

### W3 — OR+ conversion and actor-free inference can make applicability too permissive

Severity: Major. Confidence: high on the logical conversion; moderate on which concrete tracker combinations should suffice.

Evidence anchor: text: methodology L1793–1796, "OR+ is read like OR". Related anchors: L884–885; model K10 L42; model P13/P16 L76/L82; codebook L72–73.

The chapter first correctly says OR+ can need several components, then evaluates it as if any single component suffices. Asking about possibility does not establish that an incomplete combination is sufficient. The checked source explicitly uses OR+ when more than one component might be needed (Knabenhans §4.1 PDF p. 6).

The current model exposes a concrete consequence: K10 is `orplus: [IM4, IM7, CO2]`. CO2 alone describes predictions or scores computed for the user, including potentially local predictions. It does not establish that either named actor (provider or advertising partner) receives the relevant attributes. Yet it can mark K10, and consequently manipulation/profile-based-price pathways, present. This conflicts with the chapter's own warning that a user-facing prediction does not establish third-party access. Knabenhans §5.1 PDF p. 11 defines distinguishing through the recipient's presentation of information; it does not supply that missing access condition for trackers.

Minimum repair: replace executable OR+ with explicitly justified sufficient combinations, or keep it uncertain until the combination is evidenced. Split actors where their required access differs. A local insight can be coded as a benign capability mention without automatically establishing a provider/advertiser's harmful capability. This does not require probabilistic risk assessment or a new domain sample.

Evidence needed: the independent pathway audit already promised at L1927–1929 must check actor/data/access sufficiency, not just whether a cited paper contains the harm label. Include an on-device-only tracker and a tracker with documented advertising disclosure as boundary cases; verify the two receive different applicability states where warranted.

### W4 — The operational export/deletion leaf contradicts the chapter's correction for alternative routes

Severity: Major for I2-based autonomy findings unless fixed before use. Confidence: high; direct instrument inconsistency.

Evidence anchor: text: model L26, "no working in-app way to delete or export the data." Related anchors: I2 L44; P10 L73; methodology L1560–1563.

IM12 can be true when there is no working in-app control, even if the provider offers a usable request route. The chapter expressly says that the missing button cannot establish I2 because another route or provider-mediated request may exist. That distinction matters: missing an in-app control measures findability or control modality, while inability to leave without losing data is the incapability that supports the autonomy/lock-in consequence.

Minimum repair: separate an absent in-app control from absence of a usable route. Set I2 from the latter, treating unexamined routes as uncertain; retain the first for walkthrough reporting. Distinguish export from deletion where one exists and the other does not.

Evidence needed: a recorded pilot case with an external request route, a case with explicit unsupported export/deletion, and coding showing no lock-in inference from a button non-finding alone. This is a fix to the existing model, not a requirement to test backend deletion effectiveness.

### W5 — The universal-model phrasing and some origins exceed the stated evidence

Severity: Minor. Confidence: high on wording, moderate on individual origin assignments.

Evidence anchor: text: methodology L628–629, "every function a health tracker can have"; D12 L15, "No completeness is claimed". Related anchors: methodology L35–36/L576–577 and L2079–2081; model CO2/CX3 L10/L14; codebook L51–54.

The bounded literature-derived model is defensible, but "every function" and "a real app is a subset" assert exhaustiveness. Later limitations cannot establish that. Origin assignments also need the stated functional boundary: derived insights are not indispensable to every tracker, and availability of an advertising/push identifier is not inherently unavoidable merely because a phone can expose it. The codebook itself recognizes this. Knabenhans' black/blue/red argument concerns a specified ideal functionality and deployment context, not any instance of an app capability.

Minimum repair: describe a reference model of functions evidenced within the study's scope. Define origins relative to the relevant function/use case and record the assumption; retain "argued" status. Do not infer that a provider cannot address an identifier simply from its context colour. Existing per-claim control assessment can remain.

Evidence needed: reviewer reasons for core/context/implementation origin decisions, including local insight and optional identifier examples. No proof of completeness is needed if no completeness claim is made.

### W6 — Downplaying remains a deliberately narrow, study-defined construct

Severity: Minor. Confidence: high on source scope; moderate on expected pilot effect.

Evidence anchor: text: codebook L175, "a stated reason makes it `S-QUA`"; methodology L1672–1679 and L1857–1860.

Zou is a good precedent for inspecting wording, but not a validated source for this entire five-label taxonomy. Its pp. 7/10 explicitly discuss "no evidence" explanations as capable of downplaying risk even when factually accurate, and p. 9 disclaims direct evidence of consumer effects. The codebook's rule that any stated reason makes a dismissal qualification can exclude precisely such language from S-MIN. Requiring a named harm is a defensible scope choice, but it excludes much general risk reassurance; the new secondary analysis helps, though generic responsibility wording still needs an explicit coding rule.

Minimum repair: state that the five stance labels are the study's adaptation and that S-MIN measures unsupported explicit dismissal, if that narrow construct is intended. Add a rule and examples for no-evidence language, reasoned dismissal, generic reassurance and generic responsibility wording. Do not claim measured psychological downplaying or intent. Broader stance coding is optional, not a requirement for this study to be useful.

Evidence needed: pilot disagreements and resolutions on these boundaries, with negative examples and independent coding. Keep secondary language findings separate from harm-specific stance rates.

## Source/provenance checkpoints already acknowledged in the draft

These are freeze/submission prerequisites, not accusations that planned empirical work has already failed:

- The De 2017 sentence at methodology L637–642 and D12 L12 remains a summary-based claim. Read the primary full text and anchor it or drop the sentence, as its existing TODO already requires. De 2016 slides substantiate the limited actor/tree/countermeasure statements above; they do not establish everything in the proceedings paper.
- For the "documented" versus "argued" status, distinguish a source documenting a harm type, documenting a hypothetical/user-concern scenario, and establishing the specific component→recipient→capability→consequence chain. Gabriele p. 5 reports perceived possibility/likelihood of scenarios, not observed prevalence of those events. Hudig pp. 2–3 and Niksirat pp. 12/14 support concrete concerns and capabilities. Knabenhans Appendix A gives EUDIF harms/examples. A tracker pathway adapted from that taxonomy may still be argued. Preserve that provenance rather than implying that "documented" means observed actual harm.
- The new second-person check of every pathway is a strong remedy already in the methodology. Its record must show actual source locations, tested sufficiency of conditions, objections, and resolutions. A check that every YAML node exists is structural validation only.
- The codebook validation section L279–300 still specifies the earlier ten-app scheme, while the current methodology L1938–2013 specifies weighted unit sampling. The parent panel's design/instrument reviewer should own the full reconciliation. From this remit, the examples and boundaries above must be in the same frozen codebook given to people and models.

## Claim boundaries for the eventual thesis

A defensible conclusion is that a specified number of providers did or did not explicitly mention specified harms in the captured, dated surfaces, relative to this literature-derived reference and its applicability assumptions. The study can describe stance toward named harms and reason about the logical scope of claims. It cannot establish legal inadequacy, technical insecurity, deception, actual user exposure, actual harm, comprehension, or behaviour. A communication gap is an operational finding, not by itself proof that every unmentioned pathway is materially risky or legally required to be disclosed. The current chapter largely already respects those limits.

No additional literature is required merely to satisfy this review. Priority is accurate use of the actual framework sources and completion of the planned independent pathway/pilot check. No suggested new references.

## Occurrence-level citation receipt requested by the parent

This receipt addresses every citation occurrence for the seven assigned keys in the parent's `inventory.json`: 20 Knabenhans, 4 De2016, 1 De2017, 1 Deng, 1 Iwaya, 2 Zou, 1 Martin. "Supported" below concerns the actual local passage and the narrow attributed claim, not validation of the thesis's derived instrument.

### Exact source identities and excerpt bank

All PDF page numbers below are one-based.

**K — Knabenhans:** `01_Literature/library/Knabenhans_2026_PrivacyHarms-EUDigitalIdentity.pdf`, 23 pages, SHA256 `c583df6b8adf3da8f5a5517a2f380a36f1baead9a6866323d1a587a64e2a50ac`. Creation and modification metadata both 4 May 2026; consistent with the bibliography's specified May version (not an independent archive-version-history verification). Printed page numbers equal PDF page numbers. Short excerpts are supplied once here and referenced by ID below, to avoid excessive quotation from one work: K1 "system components"; K2 "lack thereof"; K3 "usual context"; K4 "negative impact"; K5 "Common sub-trees"; K6 "more than one"; K7 "do not claim completeness"; K8 "distinguish between classes"; K9 "harm may be caused". These excerpts total 24 words. The table's detailed support descriptions are paraphrases.

**D16 — De2016:** `01_Literature/library/De_2016_PrivacyHarmAnalysis-SmartGrids_manuscript.pdf`, 20 slides; title slide dates it 26 May 2016. This is the authors' presentation, not the IEEE paper cited by the bibliography. Short excerpts: D1 (slide13) "An entity whose actions lead to privacy harms"; D2 (slide17) "AND" / "OR"; D3 (slide19) "counter-measures". No paper-page locator can honestly be supplied from these slides.

**D17 — De2017:** no full text inspected; no actual PDF/version/page/excerpt available. The 2017 Springer citation and the draft's search-summary provenance are not primary-text verification.

**DG — Deng:** `01_Literature/library/Deng_2011_PrivacyThreatAnalysisFrameworkSupporting.pdf`, 30 pages, typeset Requirements Engineering 16:3–32; first-page DOI 10.1007/s00766-010-0115-7. Published online 16 November 2010, issue 2011. PDF p2 = printed4, PDF p4 = printed6, PDF p5 = printed7. Short excerpts: DG1 (PDF2, §2 step5) "data flows", "data stores", "processes", "external entities"; DG2 (PDF5, continuation §3) "First of all, a data flow diagram is created".

**IW — Iwaya:** `01_Literature/library/Iwaya_2023_PrivacyMentalHealthApps.pdf`, 40-page author-style manuscript, metadata created/modified 25 January 2022. Local filename says 2023 but a final 2023 typeset edition was not independently verified here. PDF page6 = printed6, §2.3. Short excerpt IW1: "we decided to use LINDDUN to analyze and map the findings from our study". This establishes the methodological claim in this local manuscript; use its section locator or verify the final-version pagination if citing page numbers.

**Z — Zou:** `01_Literature/library/Zou_2019_YouMightBeAffectedEmpirical.pdf`, 14 pages, CHI2019 Paper194, PDF pN = printed "Page N". Short excerpts: Z1 (p7, Risk Communication subsection) "Hedge terms downplaying risks"; Z2 (p10, discussion) "We do not insinuate". Read the corresponding full passages and p9 limitations; quotes here are locator aids, not substitutes for them.

**M — Martin:** `01_Literature/library/Martin_2025_NoCookiesForYou.pdf`, 64 pages, Georgetown Law Technology Review vol9 no1; PDF pageN = printedN. This is the published-style 2025 source specified by the thesis, not the 2023-named Methods-Reading candidate in the inventory. Short excerpt M1 (p9, Part I): "simplified abstractions". The article describes the three principles and expressly says they do not fill the space of PETs. Its p64 discussion relates privacy judgments to uses/purposes as well as recipients, data forms, and storage location.

### All 20 Knabenhans occurrences

| Methodology citation line | PDF / printed page and section | Excerpt ID | Verdict on the actual occurrence | Minimum remedy / limit |
|---|---|---|---|---|
| 132 | K pp6–7, §4.1; Fig4 | K1, K9 | Partial as a bundled methodological precedent. Trees/pathways supported; policy/interface applicability records and ordinal communication coverage are the thesis's own extension. | Identify those measures as study operationalisations; the source does not validate them. |
| 142 | K p10, §4.5 | K1, K9 | Supported as conceptual precedent for tracing what PETs remove or leave; partial for the whole RQ3 row. | Human claim-scope/mismatch coding is adapted, not the source's tested coding instrument. Add §4.5 locator if desired. |
| 586 | K p6, §4.1, Tree elements and Fig4 | K1 | Supported: three element kinds. | None for the narrow attribution. |
| 592 | K p6, §4.1, System components and Capabilities | K1, K2 | Supported: leakage/interactions/requirements can enable capabilities or incapabilities. | Tracker-specific examples remain applications, not findings made by this source. |
| 607 | K p6, §4.1, Harms | K3 | Supported: cited harm definition and current-EU baseline. The thesis's shorter quoted phrase is a contiguous extract, followed by the context explanation. | The tracker counterfactual baseline is correctly identified as this study's adaptation. |
| 614 | K p6, §4.1, Harms | K4 | Supported: broad negative impacts on individuals, groups or society and enumerated rights/wellbeing dimensions. | None for the narrow attribution. |
| 618 | K pp14–15, Appendix A | K4 | Supported: the seven starting categories and their examples are present. | Taxonomy support does not by itself document every tracker pathway. |
| 636 | K p6, §4 opening | K1 | Supported: abstract functionality alone does not establish harms; semantics and recipient require concrete use cases. | This supports contextual instantiation, not the exhaustive-superset claim. |
| 637 | K p7, §4.2/Common sub-trees/Fig5; p8, §4.3 | K5 | Supported: repeated capability sub-trees and harm trees reused across age-verification/mDL cases when applicable. | Preserve the matching-conditions qualification when transferring to tracker apps. |
| 735 | K p6, §4.1 | K1, K9 | Supported for the origin and structure of the adapted method. | Label new tracker applicability rules as adaptations. |
| 811 | K p6, §4.1 and Fig4 | K1 | Supported: components→capabilities→harms structure. | None for the narrow attribution. |
| 866 | K p6, §4.1/System components | K1 | Supported: leaked information, interaction results, requirements. | Collections/stores are tracker-domain operationalisations; check who receives/reads them. |
| 878 | K p6, §4.1/Constructing trees | K9 | Supported: three-level tree capturing pathways to a harm. | Do not describe hypothetical capability availability as actual realised harm. |
| 885 | K p6, §4.1/Constructing trees | K6 | Supported for the sentence saying combinations might be necessary. | Its later executable OR interpretation at L1795 is not supported by this passage; see W3. |
| 895 | K pp6–7, §4.1/Harm origins | K1 | Supported: black core functionality, blue digital-context components, red implementation components. | Necessity is relative to the source's formal EUDIF functionality. Tracker origin judgments need their own stated functional boundary. |
| 928 | K p7, §4.1 continuation | K7 | Supported: express non-completeness disclaimer. | Does not support earlier "every function" wording; use a bounded-reference formulation. |
| 937 | K pp6–8, §§4.1–4.3, Figs4–7 | K1, K5 | Largely supported for the source column of the comparison table. | Table's "The same" operators row must distinguish source notation from the thesis's OR+ evaluator; concrete source cases differ from the generic tracker. |
| 978 | K p11, §5.1/Definition | K8 | Supported: recipient distinguishing/categorizing classes. | Does not establish provider/advertiser access to local tracker predictions; include that condition separately. |
| 980 | K p6, §4.1/Capabilities | K2 | Partial: incapability as a class is supported. | Specific deletion/export/opt-out failures come from tracker evidence (Malki separately cited), not Knabenhans. This division is already apparent; keep it explicit. |
| 1839 | K p10, §4.5 | K1, K9 | Supported in EUDIF context: PETs can leave paths, complicate exploitation, and add new components. | This does not prove a particular tracker claim misleading. The chapter's per-scope human review and no-security-verdict limits are appropriate. |

### Other assigned occurrences

| Key and methodology line | Actual source, PDF / printed page / section | Short excerpt pointer | Verdict | Minimum remedy / limit |
|---|---|---|---|---|
| de2016privacy L132 | D16 slides7/16/17/19; no paper page checked | D1–D3 | Indirect support for trees, actors and countermeasure reasoning; not verified as the cited proceedings text. No support here for ordinal communication coverage. | Read/cite paper precisely, or make the inspected presentation provenance explicit and describe coverage as this study's operationalisation. |
| de2016privacy L601 | D16 slide13; no paper page checked | D1 | The actor/risk-source definition is directly supported by slides. | Bibliographic object remains mismatched; cite slide13 or verify original paper. |
| de2016privacy L740 | D16 slides7/11/13/14/16; no paper page checked | D1 | Slides directly link weaknesses, risk sources, feared events and harms in a smart-grid example. Priority wording "introduced by" is also attributed to them in Knabenhans, but a historical-priority audit was not performed. | Avoid pretending the cited paper was read. Verify paper or identify slides and use restrained historical wording. |
| de2016privacy L889 | D16 slide17; no paper page checked | D2 | Partial. Slide17 computes likelihood using AND/OR and dependency cases. It does not use OR+. Nearby wording "same operators" can be read too broadly. | Say AND/OR, not all three, and cite slide17 or verified paper pages. The thesis's decision not to estimate probabilities remains a legitimate adaptation. |
| de2017refinement L640 | D17: unavailable/unread | none available | Unverified primary support. Current draft openly discloses this. | Obtain and read primary full text with exact section, or remove this sentence before submission, as the existing TODO instructs. |
| deng2011privacy L644 | DG PDF2/printed4, §2 step5; PDF4–5/printed6–7, §3/Fig3 | DG1–DG2 | Claim supported, locator imprecise: §2 describes STRIDE background, while §3 explicitly adopts DFD-first reasoning in LINDDUN. | Cite §3 (with §2 for the DFD notation) rather than relying on §2 alone for what LINDDUN does. This paper does not verify a generic tracker model. |
| iwaya2023privacy L645 | IW PDF6/printed6, §2.3; corroborated PDF3–4 introduction | IW1 | Supported in the inspected author manuscript: they used LINDDUN to map/discuss their mental-health-app findings. §2.3 is the correct local locator. | State/source the edition actually inspected; final 2023-version pagination not checked. This is evidence for using the taxonomy, not a claim their study performed this thesis's communication-only methodology. |
| zou2019might L137 | Z PDF/printed7, Risk Communication; pp9–10 discussion/limitations | Z1–Z2 | Partial as a broad precedent: wording/hedging/risk framing analysed in breach notices. The five stances attached exclusively to named harms are not directly supplied/validated by this article. | Identify Axis B as this study's adaptation and add relevant pp7/10 locator; pilot its boundaries. |
| zou2019might L1678 | Z PDF/printed7 and10; limitations p9 | Z1–Z2 | Supported for studying textual qualifications while avoiding intent claims. Partial for this entire paragraph's specific coding distinctions. | Reconcile "any reason→qualification" with the source's no-evidence discussion, and do not infer effects on readers from text analysis alone. |
| martin2025cookies L142 | M PDF/printed8–9, Part I introduction; p64 concluding implications | M1 | Supported as conceptual precedent for the limited value of flow/recipient/storage principles alone. Partial for the complete RQ3 coding row. | Name the thesis's claim-scope/mismatch procedure as an adaptation. Use the actual 2025 published-style file, not the inventory's 2023-named candidate without edition checking. |

The receipt covers all 30 assigned occurrence-source pairs. It makes no claim that other bibliography entries or supplementary materials have been verified.


## Supplemental primary-source check after successful De2017 retrieval

This update supersedes the earlier De2017 UNVERIFIED/UNAVAILABLE verdict and the D17 receipt row. Inspected `01_Literature/library/De_2017_RefinementApproachPrivacyRiskAnalysis_manuscript.pdf`, the 38-page HAL `hal-01671345v1` author manuscript, with cover identifying deposit on22December2017 and the APF2017 publication. The source abstract and introduction (PDF2–3), General Approach section3 (PDF6–7), generic-tree section4.6 (PDF12), and refinement sections5.4/6 (PDF18) explicitly support the generic specification-based analysis followed by architecture-specific and deployment-context refinement. Architecture refinement includes component instantiation, actor access rights and pruning; context refinement further prunes paths based on context/resources/motivation. The narrow methodology claim at L640 is now **SUPPORTED in this author manuscript**. Final Springer pagination has not been checked; use section locators and the actual manuscript provenance. This strengthens the reuse rationale, while leaving the review's OR+ and actor/access criticisms intact. It does not prove an exhaustive superset of tracker functions or mean this thesis performs the full formal risk-analysis method. No thesis/project edits were made.

The machine-readable receipt is `C:/Users/Hamza/AppData/Local/Temp/ars-citation-privacy.json`:40 rows, covering every occurrence of the original seven assigned keys (30pairs) plus every occurrence of Niksirat, Gabriele, Hudig, Cao and Citron/Solove (10pairs, not8). Additional checks used actual Cao PDF1–3, Gabriele PDF1/3–5, Hudig PDF1–3, Niksirat PDF1/12/14, and Citron/Solove PDF1/67–68 (printed859–860 PartV.G). The ledger records precise scope/version/locator, paraphrased evidence and minimum remedy for each.

Two small additional source-specific qualifications: Gabriele's scenarios were constructed by the researchers and rated by users, so the phrase users' harm scenarios at L912 should not imply user-generated scenarios or observed incident prevalence. Citron/Solove directly supports relationship harms at printed859–860; retaining this as a tag is the thesis's operationalisation. The Cao source supports post-Roe US concerns, not established German legal applicability or observed prosecution using tracker data.


### Final Iwaya edition check

The subsequently retrieved actual published `01_Literature/library/Iwaya_2023_PrivacyMentalHealthApps_published.pdf` (Empirical Software Engineering2023,28:2,42pages, DOI10.1007/s10664-022-10236-0; online8November2022) resolves the earlier version uncertainty for L645. Its section2.3 is on PDF5, printed Page5of42, and explicitly states the choice of LINDDUN to analyse/map findings and use its taxonomy. The final verdict is **SUPPORTED**, replacing the earlier VERSION_UNVERIFIED receipt for this occurrence. The older40-page manuscript places this section on PDF6 and should remain identified separately. The structured40-row ledger has been updated accordingly.


## Final De2016 published-paper replacement and De2017 version gate

The actual published IEEE De2016 paper has now been inspected at `01_Literature/library/De_2016_PrivacyHarmAnalysis-SmartGrids.pdf`,8PDFpages corresponding to printed58–65, DOI10.1109/SPW.2016.21, IEEE arnumber7527754. This supersedes all earlier slides-only access/version conclusions for its four occurrences. SectionIII-A Definition1 (PDF3/printed60) directly supports risk-source definition at methodology L601. SectionIV-A and Figs2–3 (PDF6/printed63), together with the introduction/contributions, directly support the tree/component/actor/feared-event linkage at L740. SectionIV-B (PDF7/printed64) gives likelihood-computation rules for AND/OR with dependency cases; it does not use OR+. Thus L889 remains **PARTIAL** unless same operators is explicitly confined to AND/OR. L132 remains **PARTIAL** because this conceptual tree precedent does not define the thesis's communication-coverage measure. The final structured ledger has two SUPPORTED De2016 rows (L601/L740) and two PARTIAL rows (L132/L889), with final-paper locators. No institutional intervention was needed for this retrieval.

For De2017 L640, substantive content remains supported by the inspected HAL author manuscript, but the exact cited-version gate is now explicitly separated: structured verdict **VERSION_UNVERIFIED**, `content_supported=true`, because the final Springer typeset edition was not inspected. This is a source-version disclosure, not a finding that the generic→architecture→context refinement claim lacks primary-text support. Cite the actually inspected author manuscript and its sections or verify the final Springer version. Earlier SUPPORTED statements in this report concern content, not exact-version equivalence.


## Synthesis note

This role card was committed before the panel synthesis. Use [Citation-Audit.md](Citation-Audit.md) for final source and access verdicts: the actual De2016 proceedings paper and published Iwaya/Rodriguez papers were obtained; a free De2017 manuscript was obtained. These retrievals supersede earlier access observations, but do not settle the design issues.
