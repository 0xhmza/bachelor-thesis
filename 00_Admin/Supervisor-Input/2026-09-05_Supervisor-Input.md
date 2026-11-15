# Supervisor Input — Reading List, Research Gap, Scope

- **From:** Kavous Salehzadeh Niksirat (MPI-SP)
- **Received:** 2026-09-05
- **Source:** [`2026-09-05_Supervisor-Input.pdf`](2026-09-05_Supervisor-Input.pdf)
  (original filename `Supervisor's input 05.08.2026.pdf` — the date in the title
  does not match the day it arrived; treat 2026-09-05 as the received date)
- **Follows:** [`2026-09-04_Proposal-Meeting.md`](../Meeting-Notes/2026-09-04_Proposal-Meeting.md)

Verbatim content is reorganised below, not rewritten. The PDF gave bare URLs;
every reference has since been resolved, downloaded to `01_Literature/library/`,
and entered in `03_Thesis/references.bib`.

---

## 1. Relevant papers on privacy harm

| # | Reference | PDF | Why the supervisor sent it |
|---|---|---|---|
| P1 | Knabenhans, C., Veitch, S., Raynal, M., Stadler, T., Chatel, S., Lueks, W., & Troncoso, C. (2026). *On the (Privacy) Harms of the European Digital Identity Framework.* Cryptology ePrint Archive, Paper [2026/867](https://eprint.iacr.org/2026/867). Key `knabenhans2026harms` | [`Knabenhans_2026_PrivacyHarms-EUDigitalIdentity.pdf`](../../01_Literature/library/Knabenhans_2026_PrivacyHarms-EUDigitalIdentity.pdf) | From colleagues at MPI-SP. The paper itself is technical, but its **definition of harm** and its **harm model** are useful for understanding privacy harms. |
| P2 | Martin, K., Nissenbaum, H., & Shmatikov, V. (2025). *No Cookies For You!: Evaluating the Promises of Big Tech's 'Privacy-Enhancing' Techniques.* Georgetown Law Technology Review, 9(1). [SSRN 4655228](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4655228). Key `martin2025cookies` | [`Martin_2025_NoCookiesForYou.pdf`](../../01_Literature/library/Martin_2025_NoCookiesForYou.pdf) | Shows that modern privacy risks are **inference-centric rather than collection-centric**: even when companies claim not to share raw data, avoid third-party access, or keep processing on-device, they can still derive and use sensitive inferences about individuals — violating privacy and creating harms. |
| P3 | Citron, D. K., & Solove, D. J. (2022). *Privacy Harms.* Boston University Law Review, 102, 793. [SSRN 3782222](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3782222). Key `citron2021harms` | [`Citron_2022_PrivacyHarms.pdf`](../../01_Literature/library/Citron_2022_PrivacyHarms.pdf) | "The famous taxonomy with seven categories of harm." |

> **Confirmed:** P3 *is* the Citron & Solove paper already listed as action item 1
> from the 2026-09-04 meeting. Note the year: SSRN posting 2021, published 2022.
> The BibTeX key stays `citron2021harms`; the entry now carries the correct 2022
> Boston University Law Review details.

## 2. Example papers — period and fertility trackers

| # | Reference | PDF |
|---|---|---|
| F1 | Hudig, A. I., & Singh, J. (2025). *Intimate Data Sharing: Enhancing Transparency and Control in Fertility Tracking.* CHI '25. [doi:10.1145/3706598.3714089](https://dl.acm.org/doi/full/10.1145/3706598.3714089). Key `hudig2025intimate` | [`Hudig_2025_IntimateDataSharing-FertilityTracking.pdf`](../../01_Literature/library/Hudig_2025_IntimateDataSharing-FertilityTracking.pdf) |
| F2 | Malki, L. M., Kaleva, I., Patel, D., Warner, M., & Abu-Salma, R. (2024). *Exploring Privacy Practices of Female mHealth Apps in a Post-Roe World.* CHI '24. [doi:10.1145/3613904.3642521](https://dl.acm.org/doi/abs/10.1145/3613904.3642521). Key `malki2024exploring` | [`Malki_2024_PrivacyPractices-FemaleMHealthApps.pdf`](../../01_Literature/library/Malki_2024_PrivacyPractices-FemaleMHealthApps.pdf) |
| F3 | Cao, J., Laabadli, H., Mathis, C. H., Stern, R. D., & Emami-Naeini, P. (2024). *"I Deleted It After the Overturn of Roe v. Wade": Understanding Women's Privacy Concerns Toward Period-Tracking Apps in the Post Roe v. Wade Era.* CHI '24. [doi:10.1145/3613904.3642042](https://dl.acm.org/doi/full/10.1145/3613904.3642042). Key `cao2024deleted` | [`Cao_2024_PeriodTrackingApps-PostRoe.pdf`](../../01_Literature/library/Cao_2024_PeriodTrackingApps-PostRoe.pdf) |

## 3. Fitness trackers — collected literature

| # | Reference | PDF |
|---|---|---|
| T1 | Salehzadeh Niksirat, K., Velykoivanenko, L., Zufferey, N., Cherubini, M., Huguenin, K., & Humbert, M. (2024). *Wearable Activity Trackers: A Survey on Utility, Privacy, and Security.* ACM Computing Surveys, 56(7), 1–40. [doi:10.1145/3645091](https://dl.acm.org/doi/10.1145/3645091). Key `niksirat2024wearable` | [`SalehzadehNiksirat_2024_WearableActivityTrackers-Survey.pdf`](../../01_Literature/library/SalehzadehNiksirat_2024_WearableActivityTrackers-Survey.pdf) |

**Confirmed:** the DOI matches the survey that was already in `01_Literature/library/` —
the advisor's own paper. Nothing new to download.

## 4. Methodology reference

- **[1]** Wharton, C., Rieman, J., Lewis, C., & Polson, P. (1994). *The cognitive
  walkthrough method: A practitioner's guide.* In J. Nielsen & R. L. Mack (Eds.),
  **Usability Inspection Methods** (pp. 105–140). John Wiley & Sons.
  Key `wharton1994cognitive`. No DOI (predates DOI registration); ISBN
  0-471-01877-5. PDF: the full volume is at
  [`Nielsen_1994_UsabilityInspectionMethods-Book.pdf`](../../01_Literature/library/Nielsen_1994_UsabilityInspectionMethods-Book.pdf),
  chapter at pp. 105–140.

---

## 5. Research gap (supervisor's wording)

> We lack a systematic account of **what harms service providers communicate**.
> Prior studies examine security and privacy of health trackers, including fitness
> and fertility trackers, but none map which harm types are acknowledged,
> minimized, or ignored, nor how PETs are framed (e.g., secrecy vs. harm
> prevention).

## 6. Research question

> **RQ.** What types of downstream privacy harms do health tracker service
> providers explicitly acknowledge or downplay when describing their privacy
> practices or PETs, and how do they frame the protection these technologies
> offer?

This is a single RQ covering three things: (a) which harm types appear, (b)
whether they are acknowledged vs. downplayed, and (c) how PET protection is
framed. Sub-questions are not yet split out.

## 7. Scope

**Domains**
- Fitness trackers
- Fertility / period trackers

**Devices**
- Wearables such as smart watches
- Smartphones
- Mobile apps

**Sources of privacy communication**
- App sample: identify the **highest-rated apps in Germany** using keyword search
  - Google Play Store
  - iOS App Store
- Privacy policies — *check existing LLM tools for analysing privacy policies*
- App descriptions
- Advertisements
- Privacy blogs
- Cognitive / UI walkthrough, see **[1]** above

Note that this settles part of the open scope question from the 2026-09-04
meeting (§8): the material is **document and interface analysis** across the
sources listed, not a user survey.

## 8. Supervisor's comment (verbatim)

> I provide example papers, but at the end of the day, part of the thesis is
> literature review to understand and identify the research gaps. So please
> actively search for papers and read them in these areas:
>
> - privacy harms
> - health tracker security and privacy
> - methodologies, e.g., how to analyze privacy policies, how to do cognitive
>   walkthrough

---

## 9. Action items arising

| # | Action | Owner | Status |
|---|--------|-------|--------|
| 1 | ~~Retrieve P1–P3, F1–F3, T1 and resolve their bibliographic details~~ — done 2026-09-05; PDFs in `01_Literature/library/`, entries in `03_Thesis/references.bib` | Hamza | done |
| 2 | ~~Add Wharton et al. (1994) to `03_Thesis/references.bib`~~ — done; **PDF still needed** via RUB library | Hamza | partly done |
| 3 | Run own literature search on **privacy harms** beyond the three sent | Hamza | done 2026-09-18 — Solove 2006 taxonomy, Calo 2011 subjective/objective harm added |
| 4 | Run own literature search on **health tracker security and privacy** | Hamza | done 2026-09-18 — Shipp & Blasco 2020, Huckvale et al. 2019, Arkalakis et al. 2024, Li et al. 2022 added |
| 5 | Run own literature search on **methodologies**: privacy-policy analysis, cognitive walkthrough | Hamza | done 2026-09-18 — OPP-115, Polisis, MAPS, McDonald & Cranor, Nielsen 1994, Braun & Clarke, Cohen, McDonald et al. 2019 added |
| 6 | Survey existing **LLM tools for privacy-policy analysis** | Hamza | partly done — Polisis and Rodriguez et al. 2024 reviewed in proposal §4.6; their schemes code *data practices*, not harms, so a purpose-built prompt pipeline is used |
| 7 | Define the keyword search and inclusion criteria for the German app sample (Play Store + App Store) → `04_Study/` | Hamza | done 2026-09-18 — `04_Study/4.4_App-Sampling/sampling_protocol.md` |
| 8 | Fold the RQ and scope above into the proposal (now `99_Archive/2026-10-14_cleanup-recovery.zip` (legacy member `99_Archive/_junk/02_Proposal/proposal.tex`); the hand-in is `03_Thesis/proposal/proposal.tex`) | Hamza | done 2026-09-18 — RQ verbatim in §2.2, split into RQ1–RQ4; scope in §2.3 |
| 9 | Confirm the scope question in the 2026-09-04 notes (§8) can be closed as "document/interface analysis" | Hamza | pending advisor — proposal §7 item 1 |

## 10. Open questions

All four are answered provisionally in the proposal and listed for the advisor to
confirm or overturn in its §7, *Open Points for Confirmation*.

| Question | Proposal's answer | Where |
|---|---|---|
| Which harm taxonomy is the coding backbone — Citron & Solove's seven categories (P3), the harm model from P1, or a merge? | Citron & Solove as the backbone; the P1 harm-tree stages as a *pathway annotation* on top. Used together, not merged. | §4.5, §7 item 2 |
| "Highest rated" — by rating value, review count, or store ranking? What cutoff, how many apps? | Top 20 per keyword, filtered to ≥ 1,000 ratings, ranked by average rating, rating count as tie-break. 50 apps, 30 fitness / 20 fertility. | §4.2, §7 items 3–4 |
| Are advertisements and privacy blogs in the core corpus or a secondary pass? | Secondary. Coded where found; absence is not a finding, because ad delivery cannot be reproduced. | §4.3, §7 item 6 |
| Does the cognitive walkthrough cover every sampled app or a subset? | A balanced subset of 12: 6 fitness / 6 fertility, 3 Android / 3 iOS per domain. | §4.4, §7 item 5 |

## 11. Obtained outside open access

Both gaps were closed by Hamza on 2026-09-05.

| Reference | File | Note |
|---|---|---|
| Wharton et al. (1994), *The Cognitive Walkthrough Method* | `Nielsen_1994_UsabilityInspectionMethods-Book.pdf` | The full 439-page Wiley volume, not just the chapter. No DOI exists; cite by ISBN 0-471-01877-5, pp. 105–140. |
| Gabriele & Chiasson (2020), *Fitness Tracker Users' Knowledge & Attitudes* | `Gabriele_2020_FitnessTrackerUsers-KnowledgeAttitudes.pdf` | [doi:10.1145/3313831.3376651](https://doi.org/10.1145/3313831.3376651). On the pre-existing reading list, not the advisor's list. |
