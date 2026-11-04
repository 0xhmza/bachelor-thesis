# D16 — Instrument test on one app before the pilot

- **Status:** proposed (2026-11-01, author's instruction in chat).
- **Affects:** Methodology, Instrument Test · Results, Instrument Test · Discussion · [`04_Study/Instrument-Test/`](../../04_Study/Instrument-Test/) · [`scripts/instrument-test/v001/`](../../scripts/instrument-test/v001/evaluate.py)
- **Author's instruction:** test the method against one app and its privacy policy, with a made-up walkthrough result for testing, and assess and conclude the case.
- **Options considered for the app:**
  1. Random draw with a seed. Fair, but one draw may exercise few parts of the instrument.
  2. **A purposive, information-rich app from the sample (chosen):** Clue (rank 12). A cycle tracker has sensitive data and many pathways; its provider is in Berlin; the policy is long and in English, and states that the English version prevails.
- **What is real:** the policy captured on 2026-11-01 (SHA-256 `09d9b479…1321`), the reference model, the evaluation of the trees, and the model output.
- **What is not real or not final:**
  - The walkthrough is **invented** ([`walkthrough_SYNTHETIC.yaml`](../../04_Study/Instrument-Test/walkthrough_SYNTHETIC.yaml)). It describes no real session and no real interface. Results that rest on it are marked and carry no finding about Clue.
  - The manual coding and the applicability record are **prepared by the AI assistant** as stand-ins and must be checked or redone by the author. Agreement with the model is not validation, as both come from one vendor.
- **Rule:** the test checks whether the steps connect. It yields no estimate for the sample. Clue stays in the sample, is recoded with the frozen instruments, and does not enter the validation set, like the pilot apps.
- **Walkthrough review 2026-11-03:** the invented fixture explicitly uses protocol v5. Its T6 email-only export is labelled an access barrier and its missing export button sets IM12 present/I2 open; these assignments are not established under D10's corrected v7 rules. The thesis flags the dependent synthetic classifications and counts as historical test inputs requiring re-evaluation, not evidence that the corrected method has been applied. Preserve the old fixture and generated tables for audit; any future changed evaluation uses a new script version. This review does not invent a replacement session or new results.
- **Would change if:** the supervisor prefers a randomly drawn test app; the author replaces the synthetic record with a real session.

## Decision 2026-11-04 (night) — taken at the author's instruction

- **Status:** proposed — decided by the AI assistant at the author's instruction of 2026-11-04 ("finish the TODOs depending on reasoning, best practice, literature and context"); marked orange in the thesis until the author or supervisor confirms it.
- **Choice:** the instrument test stays a historical record of protocol v5 and reference model v1, with its tables unchanged. Its re-evaluation under model v2 from the policy alone is recorded (`04_Study/Instrument-Test/applicability_clue_v2.yaml`, `scripts/instrument-test/v002/output/`): I2 and P10 no longer apply. No synthetic re-run under the frozen protocol: it would again rest on invented screens; the pilot under protocol v8 is the evidence for the frozen instruments.
