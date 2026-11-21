contract_role: eic
## Dimension Scores

### D1: methodology_rigor
score: not_assessed

### D2: domain_accuracy
score: not_assessed

### D3: argumentative_coherence
score: not_assessed

### D4: cross_disciplinary_relevance
score: not_assessed

### D5: writing_and_structure
score: pass

### D6: venue_fit_and_contribution
score: warn
trigger: "a scope restriction is acknowledged but its effect on the claims is not argued"

## Review Body

### Reviewer Identity, Confidence and Scope

Journal-Fit Reviewer (eic): examiner of IT-security bachelor's theses and program-committee member at usable-privacy venues. The PoPETs/SOUPS level is used only as a quality bar, not as a target venue. This is an unbound run, so the card makes no venue-alignment claim. Overall confidence: 4 (usable privacy and thesis examination are within my competence; technical scraping detail is a stated blind spot and is not judged here). Calibration status: `NOT_CALIBRATED`.

Following the author's scope notes, I do not penalise the missing parts as such: Chapter 1 is empty on purpose, there is no abstract, Discussion or Conclusion yet, and the methodology covers only the app sampling. I review what is written and whether it fits RQ1 to RQ4. I checked the counts in Section 5.1 against the frozen collection (`05_Data/App Sampling/21. Nov/`): 54 queries, 1,220 results, 704 distinct apps, 8 to 30 results per query, 43 of the 49 ranked apps in a top-ten position, 40 developers, and the rank gaps in Table A.1. All of them match. I took chapter page spans from the compiled `03_Thesis-v2/thesis.pdf`.

### Summary Assessment

The draft sets up a study of what health tracker providers tell users about privacy harms and protection on two surfaces, the privacy policy and the app interface. It asks four sub-questions: coverage, stance, protection and differences between surfaces. Background and Related Work are short, plain and to the point. The legal section shows that the GDPR asks for a description of data practices but only recommends explaining consequences. Harm trees supply the lens: a protection claim can be true and still leave a harm possible. Each Related Work section ends in a gap that leads to an RQ. The contribution, applying harm-pathway reasoning to provider communication and comparing policy with interface, is original for a bachelor's thesis and reaches the usable-privacy quality bar in its design. The written methodology covers only the sample: 49 Google Play apps from the German storefront, ranked by German review count, plus Samsung Health. The sample is reported openly, including what the search misses. Two framing problems matter at this stage. First, the Android-only restriction is stated but not argued. iOS, about 28 % of German mobile page views by the cited source, and Apple's preinstalled Health app fall outside the study, and the interface surface in RQ4 depends on the platform. Yet the title and the overarching question speak of health trackers in general. Second, the questions are framed around providers while the sample counts apps, and one developer has eight apps that link one policy page. Both can be fixed with text and a reporting rule, without new data.

### Criterion-Bound Judgements

| Dimension / criterion | Criterion source | Judgement | Evidence anchors | Rationale | Uncertainty or scope limit | Decision bearing? |
|---|---|---|---|---|---|---|
| D5 writing_and_structure | Sprint contract D5; Phase 1 scoring plan | MEETS | See S1, S5, S6 and W5, W6, W8, W9, W10 (anchors there) | Logical order, plain English, defined terms, tables introduced and captioned; only minor clarity issues | The methodology budget may become a problem once later steps are written (W5) | No: normal priority, minor issues only |
| D6 venue_fit_and_contribution | Sprint contract D6; Phase 1 scoring plan; Reviewer Configuration Card | PARTLY_MEETS | See S2, S3, S4 and W1, W2, W3, W4, W7 (anchors there) | The contribution can be stated before results and fits the thesis setting; the platform scope and the unit of analysis are not argued | Intro, Discussion and Conclusion are not written yet and may later add the missing scope arguments | Yes: mandatory dimension, warn |

These judgements are not totalled, weighted or mapped to a recommendation.

### S1: The research questions grow out of the related work

Related Work is built as three lines of research. Each ends in the gap that motivates an RQ, and Section 3.4 then gives the overarching question and four sub-questions with one-word labels (Coverage, Stance, Protection, Surfaces). A reader can trace every RQ to a cited gap. This is the strongest structural feature of the draft.

**Evidence Anchor**: text: Chapter 3 opening "Three lines of research lead to the questions of this thesis: the privacy"

### S2: An original combination with a clear lens

Section 2.3 takes harm-tree reasoning (from data flows through capabilities to harms), used before on a digital identity framework, and applies it to what health tracker providers communicate. It states the key insight in one sentence: a protection claim can be true and still leave a harm possible. The prior work in Section 3.2 compares policies with app behaviour. Examining provider texts for harms, for stance and for whether claimed protections cut the pathways to harm, on two surfaces, is a new angle. Its ambition suits a bachelor's thesis.

**Evidence Anchor**: text: §2.3 From Data Practices to Harms "The thesis builds on this idea and compares"

### S3: The legal background shows why the questions matter

Section 2.2 shows that, outside automated decisions, the GDPR requires a description of practices, while the Article 29 Working Party guidance only recommends explaining consequences. This sets a precise baseline: the thesis studies communication beyond the legal minimum, so a missing harm statement is not in itself a violation. This framing protects the later results from over-claiming.

**Evidence Anchor**: text: §2.2 What Providers Must Tell Users "an explanation of what could follow from them is a"

### S4: The sampling report is open, including what the search misses

Section 5.1 gives the date and time window of the collection, the generic terms tried and kept, all four exclusions with their rule, and the fact that Polar Flow is missed although it would have qualified. The counts match the frozen collection (see the scope section above). Appendix B prints the settings and the script that drew the sample. For a reader judging whether the sample can carry RQ1 to RQ4, this openness is valuable.

**Evidence Anchor**: text: §5.1 Sample "so the search misses at least this companion app of sports"

### S5: Plain English, terms defined first, balanced chapters

A short Key Terms list defines every term before it is used. Sentences are short and concrete, as a thesis in plain academic English should be. In the compiled draft, Background and Related Work take two pages each, Methodology two and Results one, which matches the author's page targets. The bibliography has 11 entries, in line with the request for few citations.

**Evidence Anchor**: text: Chapter 2 opening "This chapter defines the terms used in the thesis and gives the legal and"

### S6: Tables are well placed and captioned

Table 4.1 comes right after the paragraph that introduces it, has a caption and label, and fits all inclusion and exclusion rules into a few lines. The body keeps the rules, and the full sample and query list are in the appendices.

**Evidence Anchor**: table: Table 4.1 (tab:eligibility), §4.3 Eligibility

### W1: The Android-only scope is stated, but its effect on the claims is not argued

Section 4.1 limits the study to Android apps offered in Germany and gives one reason: Android has the larger share. That reason explains why Android is chosen if only one platform can be studied. It does not explain why only one platform is studied, and the text never says what the restriction leaves out. Three consequences need to be argued.

(a) Market coverage. The cited StatCounter source puts iOS at 27.7 % of German mobile page views (addendum of `statcounter2026os`), but the text gives only Android's figure. Trackers that exist only on iOS, above all Apple's preinstalled Health app, fall outside the frame. Section 4.4 adds Samsung Health because preinstalled apps "reach users without a download". The same reason applies to Apple Health, and the text limits it to Android without saying so. The known-app check leaves out apps that Google Play does not offer in Germany and then says it tests whether the queries "reach the market". Here "the market" can only mean the German Google Play store.

(b) Dependence on the surface. Cross-platform providers often use one privacy policy for both stores, so findings on the policy surface (RQ1 to RQ3) may carry over to iOS. The thesis must argue this instead of leaving it to the reader. The interface surface depends on the platform: permission, tracking and health-data permission screens differ between Android and iOS, and providers may word in-app notices differently in each build. RQ4 findings will therefore describe Android builds.

(c) Framing. The title ("in Health Tracking Apps") and the overarching question ("health tracker providers") have no platform or market qualifier.

Minimum remedy: add one or two sentences to Section 4.1 that give the real reason for studying a single platform and name what is excluded (the iOS share, iOS-only trackers and Apple's preinstalled tracker). Qualify the overarching question, or the claims drawn from the results, as concerning Android apps on the German market. In the later Discussion, argue the limitation separately for each surface. Stronger, costlier option (the author's choice, since the decision log fixes the study to Android): check whether the App Store listings of the sampled cross-platform apps link the same policy, which would support the carry-over argument for the policy surface. Adding Apple Health as a second preinstalled tracker would also work, but it reopens the platform decision.

**Severity**: Major
**Evidence Anchor**: text: §4.1 Sampling Frame "The study covers Android apps offered in Germany. Android is the larger mobile"
**Confidence**: 4 — background in usable privacy and mobile platforms; platform shares checked in references.bib; effects on the coding not tested

### W2: The questions ask about providers, the sample counts apps, and one provider holds eight places

The overarching question asks what "health tracker providers" acknowledge or downplay, but the sampling unit is the app. The 50 apps come from 40 developers: Leap Fitness Group holds eight places (16 % of the sample, and seven of the 22 activity apps), Simple Design three and Google two (Section 5.1). Section 4.4 justifies counting each app separately because each has its own store page and interface. That holds for the interface surface, but not clearly for the policy surface. In the frozen collection, all eight Leap apps link the same policy page and differ only in a package parameter (field `privacyPolicy` in `pages.jsonl`). I did not check whether the text of the page changes with the parameter. If it does not, policy counts such as "n of 50 apps mention harm X" would count one document up to eight times, and in the activity category one provider would dominate. The thesis should say, before results exist, what is counted on each surface.

Minimum remedy: state the unit of analysis for each surface (the app for the interface; the distinct policy document, or the provider, for the policy). Report policy findings per distinct policy as well as per app, and make the wording of the overarching question ("providers" or "apps") match that unit. No resampling is needed. Stronger option (the author's choice, because it changes the sample): allow one app per developer and fill the freed places from further down the ranking.

**Severity**: Major
**Evidence Anchor**: text: §4.4 Ranking and Selection "Apps from the same developer count as separate apps, because each"
**Confidence**: 3 — the unit-of-analysis reasoning is within my competence; whether the policies are identical was inferred from their URLs, not from their text

### W3: The overarching question does not cover all four sub-questions

The overarching question covers harms that are acknowledged or downplayed (RQ1, RQ2) and the framing of protection (RQ3). It has no counterpart for RQ4, the comparison of policy and interface, which is half of the study's design. It uses "downstream" once without defining it; Key Terms defines privacy harm and pathway to harm, but not downstream harm. RQ1 also asks which "harms identified for the app" stay unmentioned, but no sentence says where that reference set comes from. The gap in Section 3.1 suggests that the thesis builds it, but the text does not say so. Remedy: name the two surfaces in the overarching question, define or drop "downstream", and add one sentence to Section 3.4 saying that the reference harms come from harm trees built in the study, pointing ahead to the methodology still to be written.

**Severity**: Minor
**Evidence Anchor**: text: §3.4 Research Questions "downstream privacy harms do health tracker providers acknowledge or downplay"
**Confidence**: 4 — structural reading of the RQ set

### W4: Absolute claims of novelty rest on a deliberately small bibliography

Section 3.2 limits its gap claim carefully ("the studies reviewed here"), but Sections 3.1 and 3.3 make absolute claims: the evidence "has not been collected into a list", the wording of harms "has not been studied", and "no study" relates a claimed protection to pathways to harm. With 11 references and a deliberate policy of few citations, an examiner will test these claims first, and they carry the originality case. Remedy: phrase them the way Section 3.2 does, or add one sentence saying which search supports them. I make no claim that such studies exist.

**Severity**: Minor
**Evidence Anchor**: text: §3.3 Wording of Risk and Protection "For health trackers, the wording of harms has not been studied, and no study"
**Confidence**: 3 — I did not run my own literature search

### W5: The sampling account already fills the whole methodology page budget

The author's target is at most two pages of methodology. In the compiled draft, Chapter 4 fills both pages (pp. 6 and 7) with the sampling alone. The opening sentence says that data collection, coding and the other later steps are still to come. Harm-tree construction, the coding scheme and the walkthrough of all 50 apps will not fit beside the current text. Remedy: keep only the rules in the body (frame, queries by source, eligibility, ranking, preinstalled app) and move the procedure of the known-app check and the selection mechanics (tie-breaks, unreadable pages) to Appendix B. Otherwise the two-page target cannot be met.

**Severity**: Minor
**Evidence Anchor**: text: Chapter 4 opening "The later steps of the study, from data collection to coding, build on"
**Confidence**: 4 — page spans read from the compiled PDF; I assume the two-page target applies to the whole methodology

### W6: The RQ labels are used before they are defined

Sections 3.1 to 3.3 end with "This leads to RQ1", "RQ1 and RQ4", "RQ2" and "RQ3", but the questions are first stated in Section 3.4. The chapter opening says that each section ends with an open question, which helps, but the reader still meets labels with no content. Remedy: end each section with the question in words and attach the label in Section 3.4, or preview the four labels in the chapter opening. The Introduction, once written, may also take this role.

**Severity**: Minor
**Evidence Anchor**: text: §3.1 Harms of Health Tracking "compared with what providers tell their users. This leads to RQ1."
**Confidence**: 4 — reading-order check

### W7: Calm is excluded while Headspace is included, and the text gives no reason

Section 5.1 excludes Calm because it "records only meditation time" (X4). Table A.1 includes Headspace ("Schlaf & Meditation") as a mood app, with no word of explanation. A reader will see two similar meditation apps treated differently. The screening file records a reason for Headspace (it tracks mental health with goals and progress), but that reason refers to the App Store listing, while Section 4.3 says the rules are checked on the German Google Play page. Remedy: add one clause to Section 5.1 saying what Headspace records that Calm does not, based on the Google Play page.

**Severity**: Minor
**Evidence Anchor**: text: §5.1 Sample "The meditation app Calm records only meditation"
**Confidence**: 3 — the screening record was read; neither app's store page was checked again

### W8: The base of the Xiaomi share is unclear

Section 5.1 says that Samsung's 39.3 % of all German mobile page views is 54 % of the Android share, "ahead of Xiaomi with 30 %". The 30 % can only be a share of Android, since 30 % of all page views would not fit beside Samsung and iOS, but the sentence switches bases without saying so. Remedy: write "with 30 % of the Android share" or give both figures on the same base.

**Severity**: Minor
**Evidence Anchor**: text: §5.1 Sample "of the Android share, ahead of Xiaomi with"
**Confidence**: 4 — arithmetic on the reported figures

### W9: The gaps in the Rank column are not explained

The Rank column of Table A.1 skips 3, 8, 23, 37 and 50. In the frozen data, four of these are the excluded apps and rank 8 is Samsung Health, which the search also found. The table shows Samsung Health with a dash. The caption explains neither point, so a reader cannot match the table to the text "53 apps were screened before 49 eligible apps were found". Remedy: add one caption sentence saying that missing ranks are excluded apps and that Samsung Health holds rank 8 among the apps found.

**Severity**: Minor
**Evidence Anchor**: table: Table A.1 (tab:sample), Appendix A, Rank column
**Confidence**: 5 — checked against candidates.csv

### W10: The same heading appears at two levels

Section 4.2 is titled "Search" and contains a run-in paragraph that is also titled "Search", next to "Keywords" and "Check with well-known apps". Remedy: rename the paragraph, for example "Store search" or "Result pages", or rename the section "Search Strategy".

**Severity**: Minor
**Evidence Anchor**: text: §4.2 Search "\paragraph{Search.}"
**Confidence**: 5 — direct reading

### Detailed Comments

#### Journal Fit (thesis setting)

The setting is an IT-security bachelor's thesis in usable privacy, with no confirmed venue. The topic is squarely in scope: transparency duties under the GDPR, harm taxonomies, health data as a special category, and the gap between what is disclosed and what follows from it. The rule-first, plain style suits a thesis and its examiners. Measured against the usable-privacy quality bar, the conception is sound. Whether the execution reaches that bar depends on the coding method, which is not written yet.

#### Originality

See S2. The idea is the strength. The risk to the originality case is not the idea but the unsupported absolute gap claims (W4).

#### Significance

If the planned analysis works out, the thesis will show whether health tracker providers explain consequences or only describe practices, and whether their protection claims cut the pathways to harm. Regulators applying the transparency guidance and designers of privacy notices would both care about this. As drafted, the significance is limited to Android apps on the German market, and the thesis should say so plainly (W1).

#### Structural Coherence

The topic is consistent from the title to the RQs. The overarching question misses RQ4 (W3). So far the methodology serves the RQs only through the sampling, as intended, and several sampling choices visibly serve them: rule I7 (German or English) makes coding possible, the size of 50 apps is chosen so that every policy can be coded and every app inspected, and both surfaces needed for RQ4 are named in Key Terms. The open points are the unit of analysis (W2), the platform scope (W1) and how companion apps will be inspected (Question 2).

#### Title & Abstract

There is no abstract yet, which I do not penalise. The title matches the topic but has no platform or market qualifier. If the Android-only scope stays, a subtitle such as "Android apps on the German market" would set the reader's expectations correctly (W1).

#### Conclusion

Not written yet, so there is nothing to assess. When it is written, statements about "health trackers" should carry the Android and Germany scope and the per-surface limitation from W1.

### Questions for the Author

1. What is the real reason for studying a single platform (effort, a comparable popularity measure across stores, or something else), and will Section 4.1 state it?
2. Eight sampled apps are companion apps of wearables or scales. How will their interfaces be inspected without the paired device, given the statement in Section 4.1 that every app can be inspected by hand?
3. Is the Google Play Data Safety section part of the interface surface, excluded, or used only as context? Malki et al. used it, and under an Android-only design it is the store's own privacy surface.
4. On the policy surface, will apps that link one developer policy be coded once, or once per app?

### Overall Quality Signal (baseline for the synthesizer only)

Between minor and major revision of the written chapters, leaning minor. The two Major findings (W1, W2) are problems of framing and of the counting rule. Both can be fixed by rewriting and by stating a reporting rule, without new data or resampling. The other findings are minor clarity issues. The contribution can be stated and judged before any coding results exist, and it suits the thesis setting.
