# Study Materials

Everything needed to make the empirical part reproducible. If someone else could
not rerun the study from this folder alone, something is missing.

The study domain is health trackers overall ([D15](../00_Admin/Decisions/D15_health-tracker-domain.md)). Categories from the source papers explain the scope and keywords and describe the apps; they impose no allocations on validation, walkthroughs or analysis. The instrument bundle of 5 November 2026 is: codebook [v7](Codebook/codebook_v7.md); reference model [v2](Reference-Model/reference_model_v2.yaml); prompts `stage1_coverage_v2`, `stage1_coverage_v2p`, `stage2_stance_v2`, `stage3_protection_v2` ([Prompts](Prompts/README.md)); walkthrough protocol version 9; [human coding sheets](Instrument/human_coding_sheet_v2.md); [decision forms](Instrument/decision_forms_v1.md); and the validation draw and estimator in `scripts/validation-sample/v001/`. It is frozen before main collection and applied to all apps (D20). Earlier versions preserve the historical design.

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
