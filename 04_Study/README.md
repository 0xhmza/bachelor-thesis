# Study materials

One folder per section of Chapter 4 (Methodology). A reader who has the thesis can find
each instrument by its section number. Domain: health trackers overall
([D15](../00_Admin/Decisions/D15_health-tracker-domain.md)).

| Folder | Section | Contents |
|---|---|---|
| `4.1_Study-Design/` | 4.1 | One-page method flowcharts (HTML, PDF), full and simple |
| `4.3_Analytical-Framework/` | 4.3 | Reference model v1, v2 and the use-case cards (YAML) |
| `4.4_App-Sampling/` | 4.4 | Sampling protocol, keywords, screening, identity register, identity evidence |
| `4.5_Data-Collection/` | 4.5 | Walkthrough protocol |
| `4.6_Coding/` | 4.6 | `Codebook/` (v1–v7), `Prompts/` (stages 1–3, run log) |
| `4.7_Validation/` | 4.7 | Human coding sheets, decision forms, validation manifest template, `Instrument-Test/` (D16, superseded by D20) |
| `4.8_Ethics/` | 4.8 | Ethics notes |

4.2 (literature review) lives in `../01_Literature/`.

**Frozen bundle (D20):** codebook [v7](4.6_Coding/Codebook/codebook_v7.md), reference model
[v2](4.3_Analytical-Framework/reference_model_v2.yaml), prompts `stage1_coverage_v2`,
`stage1_coverage_v2p`, `stage2_stance_v2`, `stage3_protection_v2`
([Prompts](4.6_Coding/Prompts/README.md)), walkthrough protocol v9,
[coding sheets](4.7_Validation/human_coding_sheet_v2.md),
[decision forms](4.7_Validation/decision_forms_v1.md). The validation draw is in
`scripts/validation-sample/v001/`.

## Rules

1. Record capture date and app version for every collected item.
2. Never edit a collected artefact in place; raw data goes to `05_Data/raw/` (read-only).
3. Version every prompt and codebook change with a one-line reason.
4. Validate the LLM against a hand-coded random subsample.
