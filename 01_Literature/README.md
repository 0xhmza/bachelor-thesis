# Literature

**One rule:** every paper you cite must have (a) a PDF in `PDFs/`, (b) a row in the
table below, and (c) an entry in `../_shared/references.bib`. No exceptions —
that is what stops the bibliography from rotting.

- **PDF naming:** `Author_YEAR_ShortTitle.pdf` — e.g. `Citron_2022_PrivacyHarms.pdf`.
  `Author` is the **first** author's surname; `YEAR` is the year of the version
  in the file.
- **BibTeX key:** `lastnameYEARfirstword` — e.g. `citron2021harms`. The key's year
  may differ from the filename's when a preprint and the published version differ
  (Citron & Solove: SSRN 2021, published 2022). The key never changes once cited.
- **Notes:** one Markdown file per paper in `Notes/`, same name as the PDF.
- **Edited volumes** are named after the editor, not the chapter author, because
  the file is the whole book — see `Nielsen_1994_UsabilityInspectionMethods-Book.pdf`.

## Reading list

### Harm theory and frameworks

| Status | PDF | BibTeX key              | Author (Year)                         | Short title                                          | Why it matters                                                                                                                                          |
| :----: | :-: | ----------------------- | ------------------------------------- | ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
|   ☐    |  ☑  | `citron2021harms`       | Citron & Solove (2022)                | Privacy Harms                                        | The harm taxonomy the whole thesis leans on — seven categories. **Read first.**                                                                         |
|   ☐    |  ☑  | `knabenhans2026harms`   | Knabenhans et al. (2026)              | (Privacy) Harms of the EU Digital Identity Framework | Advisor's colleagues. Technical, but the **harm definition and harm model** are the reusable part.                                                      |
|   ☐    |  ☑  | `martin2025cookies`     | Martin, Nissenbaum & Shmatikov (2025) | No Cookies For You!                                  | Privacy risk is **inference-centric, not collection-centric** — the argument that PET claims can be true and still not protect. Directly frames the RQ. |
|   ☐    |  ☒  | `nissenbaum2009privacy` | Nissenbaum (2009)                     | Privacy in Context                                   | Contextual integrity — the theoretical frame. Book, no PDF.                                                                                             |

### Health, fitness and fertility trackers

| Status | PDF | BibTeX key | Author (Year) | Short title | Why it matters |
|:---:|:---:|---|---|---|---|
| ☑ | ☑ | `niksirat2024wearable` | Salehzadeh Niksirat et al. (2024) | Wearable Activity Trackers: A Survey | Advisor's own survey — utility, privacy, security. The entry point to the fitness-tracker literature. |
| ☐ | ☑ | `hudig2025intimate` | Hudig & Singh (2025) | Intimate Data Sharing in Fertility Tracking | Network analysis of eight fertility trackers + co-designed transparency mechanisms. |
| ☐ | ☑ | `malki2024exploring` | Malki et al. (2024) | Privacy Practices of Female mHealth Apps | Post-Roe privacy-practice analysis — closest existing method to this thesis. |
| ☐ | ☑ | `cao2024deleted` | Cao et al. (2024) | "I Deleted It After the Overturn of Roe v. Wade" | User-side privacy concerns toward period trackers. |
| ☐ | ☑ | `gabriele2020understanding` | Gabriele & Chiasson (2020) | Fitness Tracker Users' Knowledge & Attitudes | What users already know and do. |

### Method

| Status | PDF | BibTeX key | Author (Year) | Short title | Why it matters |
|:---:|:---:|---|---|---|---|
| ☐ | ☑ | `wharton1994cognitive` | Wharton et al. (1994) | The Cognitive Walkthrough Method | The walkthrough method the advisor pointed at. The PDF is the **whole edited volume**, `Nielsen_1994_UsabilityInspectionMethods-Book.pdf`; the chapter is Ch. 5, pp. 105–140 (PDF viewer p. 130). |

Legend — **Status:** ☐ not read · ◐ skimmed · ☑ read and noted · **PDF:** ☑ in `PDFs/` · ☒ missing

## Note template

Copy this into `Notes/<same-name-as-pdf>.md`:

```markdown
# <Author> (<Year>) — <Title>
**Key:** `<bibtexkey>`

## Research question
## Method
## Findings
## What I take from it
## What I disagree with / what is missing
## Quotes worth citing (page numbers!)
```
