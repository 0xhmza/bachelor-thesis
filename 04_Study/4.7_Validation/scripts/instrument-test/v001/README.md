# Instrument test, version 1

Runs the method once on one app (Decision D16). Results are in the thesis, Section "Instrument Test: One App".

| Step | Command | Result |
|---|---|---|
| Split the policy into units | `python segment_policy.py <policy.html> <units.jsonl>` | `units.jsonl` |
| Write the model inputs | `python prepare_inputs.py <units.jsonl> <walkthrough.yaml> <llm>/input` | `part1.jsonl`, `part2.jsonl` |
| Run stage 1 | fresh agents apply `04_Study/4.6_Coding/Prompts/stage1_*` | `<llm>/stage1/`, `<llm>/stage1p/` |
| Check spans, write later inputs | `python stage_inputs.py <llm>` | `stage2.jsonl`, `stage3.jsonl` |
| Run stages 2 and 3 | fresh agents apply `stage2_*`, `stage3_*` | `<llm>/stage2/`, `<llm>/stage3/` |
| Generate tables and figures | `python build_tables.py <repo root>` | `03_Thesis/tables/{reference,test}-*`, `03_Thesis/figures/test-*`, `output/summary.json` |
| Test the evaluator | `python -m pytest tests` | |

## Data

`05_Data/raw/policy-test_2026-11-01/` is excluded from Git; back it up with the other raw collections.

- `clue_privacy.html`: https://helloclue.com/privacy, captured 2026-11-01 22:11 UTC, 251,242 bytes,
  SHA-256 `09d9b47967cbd91323afea152892fd8d415e7ec059713ddda1a9d91a95dc1321`.
- `units.jsonl`: 178 units. `llm/`: inputs and raw model output, including the verbatim evidence spans.

The thesis locates evidence by unit and heading and does not reproduce the spans. `build_tables.py` needs PyYAML;
`segment_policy.py` needs BeautifulSoup.
