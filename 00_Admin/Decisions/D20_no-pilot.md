# D20 — The method is applied to all apps without a pilot or instrument test

- **Status:** confirmed by the author for the removal (2026-11-05, chat: "remove everything in the methodology related to piloting or instruments testing. the methodology is assumed complete and will be applied for all apps."). The replacement rules below are proposed by the AI assistant and marked orange in the thesis until the author confirms them.
- **Affects:** Methodology (overview, workflow figure, walkthrough, LLM coding, Instrument Freeze and Validation, feasibility, limitations) · Appendix B (rules of the LLM coding), Appendix G (introductory note) · D8, D9, D10, D15, D16 (their pilot clauses no longer hold).
- **Supersedes:** D16 as a step of the method, and the clause of the 13 October meeting notes that methodological choices should be informed by the pilot.

## Choice

The methodology has no pilot, no preliminary instrument test and no development apps. It is taken as complete and applied to all sampled apps. All coding units form one corpus, which is the target of the validation sample.

## Kept, because they are not piloting

- The freeze of the instruments as one versioned bundle before main collection, with later changes logged and the affected material recoded.
- The second person's check of every pathway of the reference trees before the freeze. It moves from the pilot section to its own subsection.
- The unit tests of the scripts and the check of the estimator on constructed corpora: they test software, not the instruments on apps.
- The trial collection of 22 October 2026 (Section on provider rules, Appendix C). It is the evidence for the one-app-per-provider rule, not a test of an instrument.

## Rules that used to be settled by the pilot

Allocation, repetitions and training units are the assistant's proposals; each is a study rule, not a published threshold.

| What the pilot settled | Rule now | Reason |
|---|---|---|
| The two language models | Fixed before coding and frozen, versions and parameters reported; an open-weight model is preferred for one of them (Törnberg 2024). The condition "if it performs close to a hosted one" is dropped, because no candidate comparison remains | **Still open: the two model names have to be entered.** |
| Repeated runs for stability | Each model codes the validation sample three times | D9 already places repeated runs on the validation sample; three runs show whether a label is stable and add little cost on 500 units |
| Allocation of the validation sample | Neyman allocation with assumed spreads: 0.5 in V1 and V2, 0.4 in V3, 0.1 in V4, 0.07 in V5, under the existing floors | Unbiasedness does not depend on the allocation, only efficiency does (Lohr 2021, ch. 3), so an assumed spread cannot bias the estimate. The values are those of `scripts/validation-sample/v001/tests/test_design.py`; they are assumptions, not measurements |
| Time per unit, for the 12-hour limit | Measured in the second coder's training, which comes before the draw | Training is the remaining occasion to measure it before the size is fixed |
| Vocabulary of stratum V3 | The list in the codebook, fixed before the draw | The list exists in codebook v6 |
| Training units of the second coder | 20 units from the policy of an app outside the sample | With no development apps, units of the corpus would have been seen by the coder before the blind coding |
| Device image and OS version | Those of the first collection day | D10 treats them as a measurement recorded once |
| Whether the five-minute search limit is too short | No check; the limit stands | It stays a study rule (D10); a limit reached is a bounded non-finding |
| Starting states, search boundaries, completion criteria, synthetic profile | Fixed in the walkthrough protocol before main collection | **The protocol still defers some of these to the pilot** (for example "the pilot's synthetic profile") and has to be completed |

## Not changed by this decision

- Results and Discussion still report the instrument test on one app, and Appendix H holds its records. The methodology no longer describes that test. Whether these parts stay is for the author to decide.
- `04_Study/Instrument/` (protocol, coding sheet), codebook v6 and `04_Study/Prompts/` still mention the pilot.

## Would change if

The author reinstates a pilot, or a model pair fails on the validation sample so that the frozen instruments have to change; the second case is a new instrument version and the affected material is recoded.
