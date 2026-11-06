# Supervisor meeting — shared methodology feedback

- **Date:** 2026-11-06
- **Context:** Hamza's notes from the supervisor meeting on the shared methodology chapter (`Methodology-Share/`, Google Doc "HCS Thesis Proposal"). In the shared version, "Table 4.7" is the eligibility table (E1–E5) and "Table B.1" is the table of search keywords; both numbers are those of that document, not of the full thesis.
- **Original:** [Raw notes](2026-11-06_Supervisor-Meeting_Raw.md)
- **Status:** Organized record of the supplied notes. The four points the author marked "apply now" were applied the same day (§7); everything else is recorded and open. Where a note could be read in more than one way, the reading is marked *interpretation* and has to be confirmed before it changes the study.

## 1. Administrative

- Prof. Dr. Carmela Troncoso is a professor officially from **9 November 2026**. The examiner can therefore be entered on the registration form for the examination office (Prüfungsamt) from that date. Until then the form stays a draft (`../Registration/2026-10-19_Anmeldung-Abschlussarbeit_draft.pdf`); the second examiner is still open (see [Timeline](../Timeline.md), administrative checklist).

## 2. Structure of the thesis

| Chapter | Feedback | Applied now? |
|---|---|---|
| Related work | Present the literature, state the open question or gap it leaves, and connect that gap to the research questions. | No — see §6 |
| Related work | Justify the research questions with the related-work sections. | No — see §6 |
| Literature (any section) | Literature about the *method* of a problem belongs in the methodology section that deals with that problem, not in the literature review. | Partly — see §3 (the brief review no longer carries method precedents) |
| Discussion | Cite previous work and compare the findings with the findings of earlier literature. | No — the discussion is written after the results |

## 3. Literature review: brief, not systematic

- A Systematisation of Knowledge (SoK) or scoping review needs PRISMA, a Boolean search protocol and a screening log. These belong to *review papers*. The thesis is **not a review paper**.
- A **brief literature review section** is enough, with two topics: (1) the relevant literature, and (2) the ground for building the reference harm tree, as Knabenhans et al. did.
- **At most 10 papers.**
- Consequence recorded as [D21](../Decisions/D21_brief-literature-review.md): the systematic procedure (term groups, strands, venue listing, screening rules, PRISMA flow) leaves the thesis; the full record is archived in [`99_Archive/2026-11-06_systematic-literature-review/`](../../99_Archive/2026-11-06_systematic-literature-review/README.md).

## 4. Research questions

- Write the research questions **in full, as questions with question marks, not in a table**, and make them clear. *(Applied, §7.)*
- **New question (open):** "What are the actual harms that are not covered by these companies?" *Interpretation:* the omission half of RQ1 (applicable harms the text does not mention) already asks this; the open point is whether it becomes a question of its own and how it differs from RQ1.
- **Which questions are answered by which material (open):** RQ1, RQ3 and RQ4 are answered through app analysis and the walkthrough; **RQ2 (stance) is postponed.** *Interpretation:* RQ2 would leave the main analysis. Today RQ2 is a coding axis (Axis B) of the same policy and interface text as RQ1 and RQ3, so postponing it changes the coding scheme, the validation sample and the results chapter. It is not applied; see [D22](../Decisions/D22_research-questions.md).

## 5. Study design and sampling

### Harm trees

- Building a harm tree for every one of the 50 apps could be exhausting. *Harm trees for 3 apps could be enough.* The question is whether system components can be understood and checked at that scale.
- *Interpretation (unconfirmed):* the reference harm tree is built **once** on a generic health tracker ([D12](../Decisions/D12_reference-model.md)) and only checked per app (applicability). The note may mean that the tree should be grounded in three concrete apps instead of a generic tracker, or only that per-app trees are not expected. Not applied.

### Sample size and categories

- **Why 50?** The population is all apps in health tracking, so the number has to be justified as a sample of that population. Open: the current text cites 20 to 64 apps in earlier studies ([D01](../Decisions/D01_sample-size.md)).
- Some categories overlap (exercise and heart rate). *Is that a problem?* **Answer applied now:** the paper has no subcategories of health apps; the categories of Hutton et al. and Malki et al. are **search keywords only**, so an overlap is harmless. An app is eligible once it meets E1, whichever keyword found it ([D15](../Decisions/D15_health-tracker-domain.md)).
- After the first 50 apps are picked, check in the **results** whether a keyword category of Table B.1 is missed by the sample. Open until the sample is frozen.

### Eligibility criteria

- Expand criterion **E1** (Table 4.7) into sub-items, explain Hutton et al., and make it as clear as E3. *(Applied, §7.)*
- Keep working on the criteria table so each criterion has a clear check.

### Keywords

- Use **reverse engineering** to expand the search keywords. *Interpretation (unconfirmed):* start from apps that are certainly health trackers and read which terms, categories or related-app lists their store listings give, then add those terms to the keyword set.
- The keywords should give a **manageable number of results** per query. Today the first 30 results of each query are kept in both stores ([D03](../Decisions/D03_scope-keywords-function.md)); the 49 queries of 23 October are not re-run by this note.
- **Test the keywords and the store API** (App Store Search API, Google Play search page) and pick **3 apps that must be included** in the sample. Open; the three apps are not named.

## 6. Open points (not applied now)

| # | Point | Where it would land | Needs |
|---|---|---|---|
| 1 | Related work: gap per topic and link to RQ1–RQ4; justify the RQs with it | Chapter 3 | Author; the archived literature results hold the evidence |
| 2 | Method literature moved out of the literature review into the methodology sections | Chapters 3–4 | Author |
| 3 | Discussion compares findings with earlier literature | Chapter 6 | Results |
| 4 | Additional RQ on harms not covered by the companies | Intro, Methodology 4.1.1 | Author decision ([D22](../Decisions/D22_research-questions.md)) |
| 5 | RQ2 postponed; RQ1, RQ3, RQ4 through app analysis and walkthrough | Whole study | Author decision ([D22](../Decisions/D22_research-questions.md)) |
| 6 | Harm trees for 3 apps | Methodology 4.3 | Reading confirmed ([D12](../Decisions/D12_reference-model.md)) |
| 7 | Why 50 | Methodology 4.4 | Justification text ([D01](../Decisions/D01_sample-size.md)) |
| 8 | Check which Table B.1 categories the 50 apps miss | Results 5.2 | Frozen sample |
| 9 | Reverse engineering, manageable result counts, three must-include apps, keyword and API test | Sampling protocol | Author ([D03](../Decisions/D03_scope-keywords-function.md)) |
| 10 | "Make all parts of the Google Doc editable" | Google Doc | *Interpretation:* give the advisor edit rights or replace non-editable parts (images, pasted tables) with editable text. The doc is generated from the review copy and is now out of date with the thesis; it is not touched here. |

## 7. Applied now (2026-11-06)

| Meeting point | Change | Where |
|---|---|---|
| Brief literature review, at most 10 papers, no PRISMA or Boolean search | Section replaced by a brief literature basis with a ten-paper selection rule; results shortened to the ten papers; search record archived | Methodology 4.2, Results 5.1, Appendix F removed, [D21](../Decisions/D21_brief-literature-review.md) |
| RQs as full questions, not in a table | Four questions rewritten as self-contained questions with question marks, stated in the introduction and in the methodology text | Introduction 1.2, Methodology 4.1.1, [D22](../Decisions/D22_research-questions.md) |
| Expand E1 | E1 split into sub-items E1a–E1d, each with the check on the listing and the source (Hutton et al., Malki et al., Robillard et al.) | Methodology, eligibility table; [D03](../Decisions/D03_scope-keywords-function.md) |
| Categories overlap | Text states that the categories are search keywords, not subcategories | Methodology, Domain paragraph; Appendix C keywords table; [D15](../Decisions/D15_health-tracker-domain.md) |

## 8. Action items

| # | Action | Owner | Due | Status |
|---|---|---|---|---|
| 1 | Enter Prof. Troncoso on the registration form and send it to the Prüfungsamt | Hamza | from 2026-11-09 | open |
| 2 | Confirm the ten papers of the literature basis (Methodology 4.2) | Hamza | | proposed, marked orange |
| 3 | Decide: separate RQ on uncovered harms? RQ2 postponed? ([D22](../Decisions/D22_research-questions.md)) | Hamza | | open |
| 4 | Confirm the reading of "harm trees for 3 apps" ([D12](../Decisions/D12_reference-model.md)) | Hamza | | open |
| 5 | Write the justification for 50 apps | Hamza | | open |
| 6 | Try reverse engineering on three apps that must be included; test keywords and the store API for result counts | Hamza | | open |
| 7 | After the sample is frozen: report which Table B.1 categories are missed | Hamza | | open |
| 8 | Restructure Related Work: literature → gap → RQ link | Hamza | | open |
| 9 | Regenerate the Google Doc from the review copy and make all tabs editable | Hamza | | open |

## 9. Questions for the next meeting

- Is "harm trees for 3 apps" meant to replace the generic reference tree, or only to relieve per-app tree building?
- Is "RQ2 postponed" meant as removed from this thesis, or as answered after RQ1, RQ3 and RQ4?
- Which three apps must be included, and is the reverse-engineering step meant to run on them?
