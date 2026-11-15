# Run Log

| Date | Prompt file | Model | # documents | Notes |
|---|---|---|---|---|
| 2026-11-01 | stage1_coverage_v1 (three runs), stage1_coverage_v1p (one run), stage2_stance_v1 (three runs), stage3_protection_v1 (three runs) | claude-sonnet-5-5 through fresh Claude Code subagents; temperature and seed cannot be set | 1 policy (178 units) and 9 invented interface units | Instrument test (D16). The CLI was not logged in, so the author chose subagents. Each stage 1 run split into two calls at unit U093. 656 and 242 spans, none failed the check. Raw output in `05_Data/raw/policy-test_2026-11-01/llm/` |
