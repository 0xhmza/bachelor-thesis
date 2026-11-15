# Related Work search, 12 November 2026

Purpose: find literature for Chapter 3 (Related Work) and Chapter 2 (Background)
of the thesis. Chapter 3 is organised as literature → open question → research
question. This was a targeted web search, not a systematic review (see
[D21](../../00_Notes/Archive/Decisions/D21_brief-literature-review.md)). It does not
change the ten papers of the literature review in Methodology 4.2.

## How the search was run

Five search agents (Claude) ran web searches in parallel on 12 November 2026,
one per strand:

| Strand | Focus |
|---|---|
| A | Harms and capabilities of health trackers and wearables (inference, re-identification, brokers, law enforcement, femtech harms, harm taxonomies and harm trees) |
| B | Privacy communication of health apps (policies, Data Safety and privacy labels, store listings, consent and interface, multi-surface comparisons) |
| C | Wording of risk and protection in privacy texts (vagueness, hedging, privacy washing, PET and differential-privacy claims, risk communication) |
| D | Language models for privacy-text analysis with evaluation against human annotation |
| E | Novelty check (studies close to the thesis RQs) and background facts (EU law, EHDS) |

The venues and sources searched were PoPETs, USENIX Security, SOUPS, ACM CCS,
IEEE S&P, NDSS, WPES, CHI, CSCW, IMWUT, FAccT, WWW, ACL/EMNLP, JMIR and JMIR
mHealth, npj Digital Medicine, Lancet Digital Health, BMJ, arXiv, SSRN and Google
Scholar. The list follows the venues recorded in the meeting notes of 13 October
2026. Each agent's web-search budget ran out before it finished. Coverage of
CHI 2026, SOUPS 2025/26 and USENIX Security 2026 is therefore incomplete.

**Verification.**
- Every DOI cited was checked against Crossref (29 records) and, where needed,
  OpenAlex, Semantic Scholar or the arXiv API.
- Numbers stated in the chapters come from an abstract, a full text or a PDF
  that was read. This was checked in the PDF for Malki et al. (§4.2.5, p. 8;
  §4.2.7, pp. 8–9) and Huckvale et al. 2015, and in the PMC full text for
  LaMonica et al. (Table 4) and Zadushlivy et al.
- The legal provisions were read on EUR-Lex: EHDS Arts. 2(2)(ab), 47, 51(1)(i)
  and 105; C-184/20 paras. 120 and 125; C-21/23 para. 90.

## Closest studies (novelty check)

No study found codes the harms that health-app providers name, omit or downplay
against a structured harm reference, or relates their protection claims to harm
pathways. The nearest are:

- **Malki et al. 2024 (CHI).** Policy, Data Safety section and usability
  inspection of 20 female health apps. Its single findings bear on harms: law
  enforcement (13/19 policies), responsibility shifting (9/19) and breach
  disclaimers.
- **LaMonica et al. 2021 (JMIR).** One checklist item asks whether the policy
  warns of third-party risks: 8 of 34 do, explicitly.
- **Zadushlivy et al. 2025 (JMIR).** Four reproductive apps scored with the
  THESIS tool. The risks discussed are the authors' own.
- **Pybus et al. 2026 (Internet Policy Review).** Manifests, policies, Data
  Safety sections and walkthroughs of 14 baby trackers. It looks at practices,
  not harm statements.
- **Bahrini et al. 2025 (ESORICS).** mHealth apps in Germany: policies, data
  sharing, consent dark patterns.
- **Hammond & Burdon 2024 (CLSR).** Policies of 20 menstrual apps under the
  Australian Privacy Act, arguing for intimate harms.
- **Ebert et al. 2026 (Telecommunications Policy).** Calls for "risk
  transparency"; conceptual, with no measurement.

## Not cited, and why

- **Doherty et al. 2025, npj Digital Medicine 8:363.** Europe PMC reports that
  the article was withdrawn from public view for legal reasons.
- **Bahrini et al. 2025, figures** (third countries, English-only policies).
  They come only from a university press release.
- **Krumbholz et al. 2024, findings.** Only the aim was seen, and only the aim
  is cited.
- **FTC cases (Flo, GoodRx, BetterHelp).** ftc.gov did not answer automated
  requests, so the pages could not be checked here.
- **Posters and work in progress** (SOUPS posters, ConPro 2026
  work-in-progress papers). Left out as not archival.
- **LLM studies that are not cited** (PolicyGPT, PAPEL, PolicyLR, PolicyGapper,
  DeceptiLens, PRISMe and others). Listed in the agent notes; candidates for
  Methodology 4.6.2 if needed.
