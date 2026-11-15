# Policy analyzer, version 1

A static web page that applies the thesis method to one app: it codes a privacy policy (and,
optionally, interface text from the walkthrough) with two or more language models, using the
frozen stage prompts, checks the labels against the reference harm trees, and reports RQ1 to
RQ4 together with how far the models deviate from each other.

It is a tool for trying the instruments on single apps. It does not replace the study's
pipeline: it has no validation sample, so its figures are detection summaries, not corrected
estimates, and every high-stakes label still needs a person.

| Step | Command | Result |
|---|---|---|
| Build the data file | `python build_data.py` | `output/data.js` from `04_Study/4.3_Analytical-Framework/reference_model_v2.yaml` and the v2 prompts in `04_Study/4.6_Coding/Prompts/` |
| Open the page | `python -m http.server 8765 --directory scripts/policy-analyzer/v001` from the repo root, then http://localhost:8765 | Opening `index.html` directly also works in most browsers |
| Test the analysis code | `node --test tests` | Tree logic, combination rules, coverage levels, κ and α |

`output/` is excluded from Git; rebuild it after any change to the model or the prompts. Needs
PyYAML for the build and Node 18 or later for the tests. The page itself needs nothing.

## What it does

| Part | Rule (methodology chapter) |
|---|---|
| Units | One policy paragraph or one interface block; a short line without end punctuation in a policy is a heading |
| Stage 1–3 | The frozen prompts `stage1_coverage_v2`, `stage2_stance_v2`, `stage3_protection_v2`, the same for every model. Stage 2 gets the union of named harms, stage 3 the union of protection flags |
| Evidence | A label whose span is not in its unit is dropped and counted as a model failure |
| Combination | Routine labels (components, capabilities, measures) are *agreed* when every model returns them and none is unsure, otherwise *uncertain*. High-stakes labels are the union, *to check*. Minimisation is a *proposal* |
| Step 1 | The page proposes applicability from the coded text (CO1 and EX1 assumed present, EX2 and EX3 uncertain, non-findings uncertain). The analyst confirms or changes each component; the trees are evaluated with three-valued AND/OR |
| Step 2 | Coverage level 0–3 per pathway and surface; denials count as mentions. A named harm lifts a pathway to level 3 only if the text also reaches the pathway; otherwise it is a category-level mention. Scenario A uses agreed labels and applicable pathways, scenario B adds uncertain ones |
| Step 3 | For each measure the analyst picks the component it would remove; the page re-evaluates the trees and lists the pathways it cuts and those it leaves open |
| Deviation | Per label family and model pair: counts, raw agreement, Cohen's κ, PABAK, positive agreement, Krippendorff's α (all models too); agreement on status, framing, strength and spans; what each model adds; coverage and applicability from each model alone; run-to-run and prompt-paraphrase α |

## Providers

Anthropic (Messages API, default `claude-opus-5-5`, with server-side refusal fallback), OpenAI,
Google Gemini, and any OpenAI-compatible endpoint (OpenRouter, a local Ollama or LM Studio).
Keys are sent only to their own provider and are kept in the browser only if *remember* is
ticked. An offline demo coder (keyword rules) lets the page be tried without keys; its labels
mean nothing.

Exports: the report as HTML (or print to PDF), all data as JSON (units, raw model output,
labels, decisions, agreement), and the labels as CSV.
