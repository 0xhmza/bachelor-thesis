# Study Materials

Everything needed to make the empirical part reproducible. If someone else could
not rerun the study from this folder alone, something is missing.

The study domain is health trackers overall ([D15](../00_Admin/Decisions/D15_health-tracker-domain.md)). Categories from the source papers explain the scope and keywords and describe the apps; they impose no allocations on the pilot, validation, walkthroughs or analysis. The current codebook is [v4](Codebook/codebook_v4.md), and the walkthrough protocol is version 3. Earlier codebook versions preserve the historical design.

| Folder | Contents |
|---|---|
| `App-Sample/` | Search keywords, inclusion/exclusion criteria, the resulting app list, and the date each app was captured. |
| `Instrument/` | The data-collection instruments. Currently `walkthrough_protocol.md`; survey drafts go here too if the scenario-based survey is added back to scope. |
| `Ethics/` | Ethics application, approval, consent and information sheets. |
| `Codebook/` | The coding scheme: every category with definition, examples, and counter-examples. Version it. |
| `Prompts/` | Every LLM prompt, versioned. See `Prompts/README.md`. |

## Non-negotiables

1. **Record the capture date and app version** for every piece of material you collect.
   Store listings and policies change; without a date your data is not verifiable.
2. **Never edit a collected artefact in place.** Raw goes to `05_Data/raw/`, read-only.
3. **Version every prompt and every codebook change**, with a one-line reason.
4. **Validate the LLM.** Hand-code a random subsample and report agreement.
