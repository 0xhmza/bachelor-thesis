# Literature

**One rule:** every paper you cite must have (a) a PDF in `PDFs/`, (b) a row in the
table below, and (c) an entry in `../_shared/references.bib`. No exceptions —
that is what stops the bibliography from rotting.

- **PDF naming:** `Author_YEAR_ShortTitle.pdf` — e.g. `Citron_2021_PrivacyHarms.pdf`
- **BibTeX key:** `lastnameYEARfirstword` — e.g. `citron2021harms`
- **Notes:** one Markdown file per paper in `Notes/`, same name as the PDF.

## Reading list

| Status | BibTeX key | Author (Year) | Short title | Why it matters |
|:---:|---|---|---|---|
| ☐ | `citron2021harms` | Citron & Solove (2021) | Privacy Harms | The harm taxonomy the whole thesis leans on. **Read first.** |
| ☑ | `niksirat2024wearable` | Salehzadeh Niksirat et al. (2024) | Wearable Activity Trackers: A Survey | Advisor's own survey — utility, privacy, security. PDF in `PDFs/`. |
| ☐ | `gabriele2020understanding` | Gabriele & Chiasson (2020) | Fitness Tracker Users' Knowledge & Attitudes | What users already know and do. |
| ☐ | `nissenbaum2009privacy` | Nissenbaum (2009) | Privacy in Context | Contextual integrity — the theoretical frame. |

Legend: ☐ not read · ◐ skimmed · ☑ read and noted

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
