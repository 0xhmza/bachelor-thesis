# Literature review v002 — screening protocol and log

Procedure: [D14](../../00_Admin/Decisions/D14_literature-review-v2.md). Search scripts:
[`scripts/literature-search/v002`](../../scripts/literature-search/v002/). Frozen search results:
`05_Data/Literature Search/28. Oct/`.

The criteria below were fixed on 28 October 2026 before any record was screened.

## Review question

What is known about the privacy harms and capabilities associated with health tracking apps, about how
their privacy communication has been analysed and what it says, about how language models have been
used and validated for coding privacy text, and about how privacy texts frame risk and protection?

| Sub-question | Focus | Serves |
|---|---|---|
| LQ1 | Privacy harms, risks, threats and inference capabilities that concern users of health tracking apps or their wearables | Reference harm trees; RQ1, RQ3 |
| LQ2 | Analyses of the privacy communication of health tracking apps (policies, labels, store listings, notices, settings and consent interfaces, marketing) | Sampling, material and coding decisions; RQ1–RQ4; research gap |
| LQ3 | Large language models used to annotate, classify, extract from or assess privacy policies or similar privacy text, with an empirical evaluation | LLM-assisted coding and its validation |
| LQ4 | How privacy texts in any domain word or present risks, harms or protections (vagueness, hedging, reassurance, downplaying, misleading claims, risk communication) | Stance and protection coding; RQ2, RQ3 |

*Health tracking apps*: apps that let users record their own health or body data over time (activity,
fitness, nutrition, sleep, heart rate, mood and mental health, menstrual cycle, fertility, pregnancy),
including the companion apps of wearables (thesis, Section 1.2).

## Eligibility criteria

A record is **eligible** if all of the following hold.

| | Criterion |
|---|---|
| C1 | It is a research article: a journal article, a conference or workshop paper, or an archival preprint, reporting original empirical or analytical work or a systematic or scoping review. |
| C2 | It is written in English or German. |
| C3 | It was published between 1 January 2014 and 28 October 2026 (LQ3: from 1 January 2022). |
| C4 | It answers at least one of LQ1–LQ4 as defined above. |

## Exclusion rules, in the order applied

Each excluded record receives one **primary** reason: the first rule in this order that applies.
Rules R1–R6 are applied to the title, and to the abstract where the title does not decide; R7–R8 to the full text.

| Rule | Excludes | Stage |
|---|---|---|
| R1 | Not a research article: editorial, commentary, letter, news, erratum, abstract or poster only, keynote, panel, book or book chapter, thesis, proceedings front matter, narrative overview without a systematic method, position paper | title/abstract |
| R2 | Outside the language or period of C2–C3 | title/abstract |
| R3 | Outside the domain: neither health tracking apps or wearables (LQ1, LQ2) nor privacy text (LQ3, LQ4) — e.g. hospital systems, electronic health records, telemedicine, clinical sensor networks, smart homes, vehicles, general apps | title/abstract |
| R4 | In the domain but answering neither LQ1 nor LQ2: quality, usability, clinical effect, features, accuracy; adoption or attitude studies in which privacy is a factor but no harm is named; quality evaluations in which the privacy policy is one criterion among many; legal or regulatory analyses without an analysis of apps | title/abstract |
| R5 | A technical system or protocol (encryption, authentication, anonymisation, federated learning, blockchain, detection model) whose evaluation documents neither harms or capabilities nor communication | title/abstract |
| R6 | Privacy-text or language-model work outside health tracking apps that answers neither LQ3 nor LQ4 — e.g. language models as a privacy risk, generating or summarising policies, readability, legal compliance or label accuracy without an analysis of how risks or protections are worded | title/abstract |
| R7 | Full text not retrievable through open access, the repository or the university library | full text |
| R8 | On reading the full text, C1 or C4 does not hold | full text |

Duplicates are removed before screening and are not an exclusion rule.

**Conventions and clarifications (28 October 2026).** R4 was worded more precisely while the
first batch of 160 PubMed records was screened (`pm01`); the new wording spells out cases that
batch had already coded R4 and changed no decision. Two conventions keep the rules apart:
systems for hospitals, health records, telemedicine or the Internet of Things in general fall
under R3, systems for wearables, body-area networks or health apps under R5; adoption, attitude
and concern studies fall under R4 unless they name specific harms or actors (then LQ1).
Study protocols without results fall under R1.

## Provenance

Every record lists the routes that found it: database search (PubMed, IEEE Xplore, arXiv, ACL Anthology),
venue search (PoPETs, USENIX Security, SOUPS, CCS, IEEE S&P, NDSS, CHI, CSCW), citation searching, thesis
citation, Methods Digest. A record found by several routes is one record.

A thesis citation that fails a rule stays in the corpus as **contextual** (`collection = contextual`)
with its rule. It is not counted as review evidence.

## Files

- `decisions/raw/*.txt` — title-and-abstract decisions as entered, one batch per file:
  `number code [note]` (code R1–R6, or `ft:LQ…` for records passed to full text);
  `decisions/batches/*.json` maps each batch number to the record identifier.
- `decisions/title.csv` — generated from the two (`show.py expand`), keyed by record identifier.
- `decisions/fulltext.csv` — full-text decisions: `in` with the sub-questions, `ex` with R7/R8,
  or `pending` while the full text is missing; the note names the file read.
- `decisions/extraction-hand.csv` — parts of the thesis RQ and capability coded by hand for the
  review evidence.
- `screening.csv` — generated by `scripts/literature-search/v002/screening.py`: every record with its
  provenance, decision, primary reason, stage, collection and full-text status.
- `corpus.csv` — generated: the eligible studies and the contextual collection with their extraction fields.

The screening decisions were prepared by an AI assistant (Claude) from titles, abstracts and, where held,
full texts. The author must check them before the thesis states who screened.
