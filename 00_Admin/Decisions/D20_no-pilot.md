# D20 — The method is applied to all apps without a pilot or instrument test

- **Status:** confirmed by the author for the removal (2026-11-05, chat: "remove everything in the methodology related to piloting or instruments testing. the methodology is assumed complete and will be applied for all apps."; extended the same day to Results, Discussion, Appendix H and the protocols: "Yes, remove it all"). The replacement rules below are proposed by the AI assistant; those in the thesis are marked orange until the author confirms them.
- **Affects:** Methodology (overview, workflow figure, walkthrough, LLM coding, Instrument Freeze and Validation, feasibility, limitations) · Results (section on the test) · Discussion (section on the test) · Appendix B (rules, and the prompt versions it prints), Appendix G (introductory note), Appendix H (removed), AI Appendix · walkthrough protocol v9, codebook v7, human coding sheet v2, prompts header and README, sampling protocol amendment · D8, D9, D10, D15, D16 (their pilot clauses no longer hold).
- **Supersedes:** D16 as a step of the method and as a part of the thesis, and the clause of the 13 October meeting notes that methodological choices should be informed by the pilot.

## Choice

The thesis has no pilot, no preliminary instrument test and no development apps. The methodology is taken as complete and applied to all sampled apps. All coding units form one corpus, which is the target of the validation sample.

## Kept, because they are not piloting

- The freeze of the instruments as one versioned bundle before main collection, with later changes logged and the affected material recoded.
- The second person's check of every pathway of the reference trees before the freeze. It moves from the pilot section to its own subsection.
- The unit tests of the scripts and the check of the estimator on constructed corpora: they test software, not the instruments on apps.
- The trial collection of 22 October 2026 (Section on provider rules, Appendix C). It is the evidence for the one-app-per-provider rule, not a test of an instrument.

## Rules that used to be settled by the pilot

Each value is the assistant's proposal and a study rule, not a published threshold.

| What the pilot settled | Rule now | Reason |
|---|---|---|
| The two language models | Fixed before coding and frozen, versions and parameters reported; an open-weight model is preferred for one of them (Törnberg 2024). The condition "if it performs close to a hosted one" is dropped, because no candidate comparison remains | **Still open: the two model names have to be entered.** |
| Repeated runs for stability | Each model codes the validation sample three times | D9 already places repeated runs on the validation sample; three runs show whether a label is stable and add little cost on 500 units |
| Allocation of the validation sample | Neyman allocation with assumed spreads: 0.5 in V1 and V2, 0.4 in V3, 0.1 in V4, 0.07 in V5, under the existing floors | Unbiasedness does not depend on the allocation, only efficiency does (Lohr 2021, ch. 3), so an assumed spread cannot bias the estimate. The values are those of `scripts/validation-sample/v001/tests/test_design.py`; they are assumptions, not measurements |
| Time per unit, for the 12-hour limit | Measured in the second coder's training, which comes before the draw | Training is the remaining occasion to measure it before the size is fixed |
| Vocabulary of stratum V3 | The list in the codebook, fixed before the draw | The list exists since codebook v6 |
| Training units of the second coder | 20 units from the policy of an app outside the sample | With no development apps, units of the corpus would have been seen by the coder before the blind coding |
| Device image and OS version | Those of the first collection day | D10 treats them as a measurement recorded once |
| Whether the five-minute search limit is too short | No check; the limit stands | It stays a study rule (D10); a limit reached is a bounded non-finding |
| Starting state of a task | Fresh install on the clean device state; each task from the home screen in the state the previous task left; T1–T4 change no setting | Follows the fixed task order of D10 |
| Route preparation and search boundaries | One search per task within the limit, then evaluation; the app's screens, help pages and the documents its links open; no web search or contact with the provider; an external route is recorded and not carried out | Keeps the search within what a first-time user meets in the app, and sends nothing to providers |
| Completion of a subgoal | The interface shows the information or confirms the action; the search stops at completion, at evidence that the function is not offered, at a barrier or at the limit | Restates the outcome table of the protocol as a stopping rule |
| Synthetic profile | Alex Muster; new throwaway e-mail per app; 15 June 1990; Germany; no address or phone; 170 cm, 70 kg; gender "not specified" where offered, otherwise what the tracked function needs; one week of invented entries | The ethics rule demands synthetic data only; one profile keeps sessions comparable |
| Consent and permission choices | Record all options, take the primary action and leave pre-set choices untouched; deny an OS permission unless the app or task cannot proceed | T5 then meets the state of a first-time user who follows the app; a denied permission gives the app the least |

## Removal from the thesis, and what stays outside it

- Results, Discussion and Appendix H no longer report the test on Clue. The generated files `03_Thesis/tables/test-*.tex` and `03_Thesis/figures/test-*.tex`, and the `\synthtag` macro, went with them.
- Appendix B now prints the current prompts (version 2 and its paraphrase), because version 1 was only used in the test.
- The AI Appendix keeps the disclosure that Claude drafted the generic model and the methodology text on it; the uses that belonged to the test left with it.
- Kept as an archive, outside the thesis: `04_Study/4.7_Validation/Instrument-Test/`, `05_Data/raw/policy-test_2026-11-01/`, `scripts/instrument-test/` (v002 also holds the current evaluator and the generator of the reference-model tables), the version 1 prompts, codebook v6, coding sheet v1.
- The historical draft in `04_Study/4.4_App-Sampling/sampling_protocol.md` below the current amendment is left as it is.

## Would change if

The author reinstates a pilot, or a model pair fails on the validation sample so that the frozen instruments have to change; the second case is a new instrument version and the affected material is recoded.
