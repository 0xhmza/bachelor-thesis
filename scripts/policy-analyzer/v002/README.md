# Privacy Policy Analyser, version 2

*LLM coding against reference harm trees.* A local web workspace that applies the thesis method to one app. It codes a privacy policy
(and, optionally, interface text from the walkthrough) with two or more language models,
using the frozen stage prompts, checks the labels against the reference harm trees, lets a
person review every high-stakes label and decide applicability, and reports RQ1 to RQ4 with
the deviation between the models. Everything goes into one YAML record that reopens the
whole analysis.

It runs from this folder; nothing is hosted, and the only network calls are to the model
providers you configure. It has no validation sample, so its figures are detection summaries,
not corrected estimates.

| Step | Command | Result |
|---|---|---|
| Build the data file | `python build_data.py` | `output/data.js` from `04_Study/4.3_Analytical-Framework/reference_model_v2.yaml` and the v2 prompts |
| Open the workspace | `python -m http.server 8765 --directory scripts/policy-analyzer/v002` from the repo root, then http://localhost:8765 | Opening `index.html` directly also works in most browsers |
| Test | `node --test tests` | Tree logic, term parser, model check, combination rules, coverage, κ and α, YAML round trip |

`output/` is excluded from Git. Needs PyYAML for the build and Node 18 or later for the tests.

## What changed from v001

| Change | Why |
|---|---|
| Tabbed workspace (Setup, Instruments, Review, Results, Record) with autosave in the browser | One long page did not scale to review work |
| Harm trees drawn as trees (SVG), one harm at a time or all, top-down as in the thesis or left-right, paper or dark canvas, the thesis's origin colours (Knabenhans et al., Fig. 4); pan, zoom, fold, SVG and PNG export | The trees were nested lists |
| Tree editor: add or edit pathways, capabilities, components and harms; capability terms such as `(IM3 OR IM4) AND (CX2 OR CX3)` with live validation; the checks of `scripts/instrument-test/v002/evaluate.py`; every edit logged | Testing other pathways needed a YAML edit |
| Coded-text view with highlighted spans, and a review queue (accept, reject, note; keyboard A, R, J, K) whose rejections leave the results | The method has a person check every high-stakes label |
| Full YAML record (inputs with SHA-256, frozen and edited model, prompts in full with hashes, models and settings without keys, every call with time and tokens, raw output, decisions, results, agreement), which reopens the workspace | JSON and CSV left out the instruments and the human decisions |

The tree view follows ADTool (automatic layout, folding, zoom, an editable term view, value
checks); the review queue follows annotation tools such as Label Studio (model labels shown as
highlighted spans, confirmed or rejected by a person, with provenance).

## Rules applied

| Part | Rule (methodology chapter) |
|---|---|
| Units | One policy paragraph or one interface block; a short line without end punctuation in a policy is a heading |
| Stages 1–3 | Frozen prompts `stage1_coverage_v2`, `stage2_stance_v2`, `stage3_protection_v2`, the same for every model; stage 2 gets the union of named harms, stage 3 the union of protection flags; `stage1_coverage_v2p` optionally |
| Evidence | A label whose span is not in its unit is dropped and counted as a model failure |
| Combination | Routine labels agreed when every model returns them and none is unsure, else uncertain; high-stakes labels are the union and go to the review queue; minimisation is a proposal |
| Step 1 | Proposed from the coded text (CO1 and EX1 present, EX2 and EX3 uncertain, a non-finding uncertain); the analyst decides and notes the evidence |
| Step 2 | Level 0–3 per pathway and surface; denials count as mentions; a named harm reaches level 3 only on a pathway the text reaches. Scenario A: agreed labels, applicable pathways; B adds uncertain ones |
| Step 3 | The analyst picks the component a measure would remove; the trees are re-evaluated |
| Deviation | Per label family and model pair: counts, raw agreement, Cohen's κ, PABAK, positive agreement, Krippendorff's α (all models too); status, framing, strength and span agreement; what each model adds; coverage and applicability from each model alone; run-to-run and paraphrase α |

Components added in the editor are not in the frozen prompts, so the models cannot code them;
their applicability is set by hand.

## Testing with Claude Code or Codex (no API key)

`cli_bridge.py` lets the page use the command-line tools you are logged in to, so the
workspace can be tried without API keys:

```
python cli_bridge.py            # prints a bridge key; Ctrl+C stops it
```

In the Models tab choose *Local CLI bridge (testing only)*, paste the bridge key, and use
the model `codex`, `codex:<model>`, `claude-code` or `claude-code:<model>`. The bridge
listens on 127.0.0.1 only, accepts requests only from pages on this computer that send the
key, and runs each request in an empty temporary folder with tools, settings, MCP servers
and project rules off. Claude Code needs `claude auth login` in a terminal first (the
desktop app's login is separate).

For testing only. Each CLI adds its own instructions and can change models with an update,
so its output is not a frozen model call, and Codex reports only a total token count. Use
API models or a local open-weight model for the study's coding. Check your subscription
terms before relying on it for anything else.

## Providers

Anthropic (Messages API, default `claude-opus-5-5`, server-side refusal fallback), OpenAI,
Google Gemini, and any OpenAI-compatible endpoint (OpenRouter, a local Ollama or LM Studio).
Keys are sent only to their own provider and stored in the browser only if asked. An offline
demo coder (keyword rules) lets the workspace be tried without keys; its labels mean nothing.
