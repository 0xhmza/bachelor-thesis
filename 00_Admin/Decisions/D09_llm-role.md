# D9 — What does the language model do, and when is it accepted?

- **Status:** proposed (2026-11-01, author's instruction in chat: "the LLM will assist"). Model and final prompts stay open until the pilot.
- **Affects:** RQ1–RQ4 · [`04_Study/Prompts/`](../../04_Study/Prompts/README.md) · Methodology, LLM-Assisted Coding
- **Options considered:**
  1. The model codes alone. Rejected: performance depends on task and data and needs human validation (Pangakis et al. 2023, p. 1; Törnberg 2024, p. 9); configuration choices can change conclusions (Baumann et al. 2025).
  2. **The model screens and proposes; people decide (chosen).**
  3. No model. Possible, but the supervisor asked to test its usability (meeting 2026-10-13, §6).
- **Evidence (checked in the PDFs):**
  - Rodriguez et al. 2024: codebook definitions in the prompt (p. 4), two-shot examples best (p. 5), a persona did not help, temperature 0 and repeated runs to measure consistency (pp. 4–6).
  - Törnberg 2024: fixed model version (p. 3), prompt codebook (p. 7), an uncertain option (p. 8), validate only after the prompt is final and at least 20–30 examples per category (p. 10), paraphrases for prompt stability (p. 13).
  - Baumann et al. 2025: document every tested configuration (p. 18), human agreement does not license automation (p. 34).
  - Xie et al. 2025, p. 7: the prompt asks for a decision and for the supporting text. Chanenson et al. 2025, pp. 1–2: LLM annotation of privacy policies against expert labels.
  - Mayring 2025: ChatGPT reached only rough approximations of a content analysis, with gross errors (p. 1).
- **Choice:** three stages (coverage with tree nodes, stance, protection). Every code needs an exact span, which a script checks. An uncertain answer goes to manual review. Three runs per stage and one paraphrased prompt. All retained harm mentions are read by a person. Applicability and potential mismatches are decided by people only. An open-weight model is preferred if it performs close to a hosted one. Acceptance: the review triggers of the Validation section (fewer than 20 positives or recall below 0.90 means manual checking or no corpus-wide absence claim).
- **Instrument test configuration (not a model choice):** claude-sonnet-5-5 through fresh Claude Code subagents, chosen by the author on 2026-11-01 because the CLI was not logged in. Temperature and seed cannot be set in this setup.
- **Clarification 2026-11-03 (walkthrough review, D10):** the same proposed coding and blind validation apply to captured interface text and policy text. Transcripts are checked against screens before units are fixed; checking model spans cannot detect transcription errors. Report available validation units and positives by surface; policy performance alone cannot justify interface absence claims. The existing low-positive/low-recall review triggers apply to claims about interface text too. D8's second coder independently codes the captured text, which is distinct from repeating the app inspection.
- **Would change if:** the pilot shows that a stage does not reach the triggers; then that stage is coded by hand.
