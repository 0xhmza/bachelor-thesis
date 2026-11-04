# LLM Prompts

The prompts are part of the method, so they get the same treatment as code:
one file per prompt, versioned, never silently edited.

**Naming:** `<task>_v<N>.md` — e.g. `policy_inference_coding_v1.md`

**Every prompt file starts with this header:**

```markdown
---
task: what this prompt is supposed to extract or classify
version: 1
date: YYYY-MM-DD
model: exact model name and version
input: what is fed in (e.g. a full privacy policy, one paragraph, a store description)
output: expected output format (e.g. JSON with fields x, y, z)
changes: what changed vs. the previous version, and why
---
```

**Log every run** in `run_log.md`: date, prompt version, model, number of documents,
and anything that went wrong. This is what you cite in the thesis appendix.

## Current versions (instrument bundle of 4 November 2026)

| Stage | Prompt | Paraphrase (validation sample only) |
|---|---|---|
| 1 Coverage | `stage1_coverage_v2.md` | `stage1_coverage_v2p.md` |
| 2 Stance | `stage2_stance_v2.md` | — |
| 3 Protection | `stage3_protection_v2.md` | — |

Version 1 files are the prompts of the instrument test (D16) and stay unchanged.
Both models get the same prompt; the pilot fixes the two models and the number of
repeated runs, and both go into `run_log.md`.
