# D10 — Which walkthrough, with which checklist and outputs?

- **Status:** proposed (2026-11-01). Starting points and time limits stay open until the pilot.
- **Affects:** RQ4, applicability · [`walkthrough_protocol.md`](../../04_Study/Instrument/walkthrough_protocol.md) · Methodology, App Walkthroughs
- **Options considered:**
  1. Heuristic walkthrough (cognitive walkthrough plus Nielsen's heuristics), as Malki et al. 2024, p. 5. Yields design problems, not outcomes that attach to tree nodes.
  2. The app-studies walkthrough of Light et al. 2018. Good for capturing screens, but it is a different tradition without task questions.
  3. **Cognitive walkthrough with Wharton et al.'s four questions on privacy tasks (chosen).** Light et al.'s stages (entry, everyday use, leaving) inform the task order only.
- **Evidence:**
  - Wharton et al. 1994, Table 5.1, p. 106: inputs (users, tasks, action sequences, interface), four questions, recording; the walkthrough may be done by one person (p. 109).
  - Mahatody et al. 2010, manuscript pp. 15, 20–22: all variants ask about goals, actions, feedback and completion; results depend on evaluator expertise; variants are thinly validated, so an adaptation must be stated; recording is recommended.
  - Malki et al. 2024, p. 5: first-time user as target, fresh install, step-by-step tasks; two authors inspected independently.
  - Habib et al. 2020, p. 4: minimum number of user actions per privacy control.
  - Meeting 2026-10-13, §6: use a checklist and explain the data it produces.
- **Choice:** the four questions at every step of tasks T1–T7, four neutral outcomes, and a count of taps. Each task is tied to tree nodes, so the walkthrough gives three outputs: evidence for applicability, interface text for the codebook, and findability. The author inspects; a second inspection of a subset is open (D8).
- **Update 2026-11-02 (author's instruction):** the walkthrough covers all 50 apps, not a subsample of 12. The six-and-six platform balance and the rank-order slots fall away. Access exclusions stay. Open for the pilot: the platform for the 36 apps listed in both stores, and the time one session takes.
- **Update 2026-11-03 (author's request: walkthrough coherent with the policy analysis):** the methodology's App Walkthroughs section is written out. No new method; it states how the three outputs enter the steps the policy also passes: findability → task record per tree node (RQ4); interface text → same unit script, the three LLM stages of D9 with span check, human decision, blind validation on both surfaces; applicability evidence → applicability record (Step 1) and offered controls (Step 3, claim still evaluated as written). The model takes no part in the walkthrough itself. Session sequence taken from protocol v5. Still open: device and OS version; a second inspection of a subset (with D8); and a **proposal** not yet adopted: walk each app through before its policy's model codes are reviewed, so the policy does not steer the search (marked in the thesis).
- **Would change if:** the pilot shows that the tasks do not reach the tree nodes; the supervisor clarifies the "post-harm reaction" point of the meeting.
