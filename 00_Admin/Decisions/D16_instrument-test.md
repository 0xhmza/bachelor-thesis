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
- **Would change if:** the supervisor prefers a randomly drawn test app; the author replaces the synthetic record with a real session.
