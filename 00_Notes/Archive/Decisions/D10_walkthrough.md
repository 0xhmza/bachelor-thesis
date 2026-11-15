# D10 — Which walkthrough, with which checklist and outputs?

- **Status:** **closed (2026-11-05, author's instruction).** The walkthrough covers all 50 apps; no subsample. See "Closure 2026-11-05" at the end.
- **Affects:** RQ1–RQ4, applicability · [`walkthrough_protocol.md`](../../../04_Study/4.5_Data-Collection/walkthrough_protocol.md) · Methodology, App Walkthroughs
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
- **Review correction 2026-11-03 (author's request to assess and repair that draft):** protocol v7 and the thesis use the following operational rules. These refine the proposed D10; they do not resolve the open pilot or supervisor choices.
  - Wharton et al., pp. 109–111, require a user description and an action sequence before its cognitive evaluation. For each app, document route preparation, then evaluate the shortest route located, with no claim of a global minimum. Keep search/backtracking separate from route taps and record other actions. Q1–Q4 are reasoned analyst judgments, not observed participant behaviour; a negative answer can coexist with analyst completion.
  - Record setup choices and the initial privacy-setting states before T5 or any other control change; T7 is the final account action. Capture permission prompts and advertisements when they appear. This corrects v6's impossible sequence of recording defaults after sharing changes and account deletion. The pilot freezes starting states, synthetic inputs, consent/permission choices, route preparation and stopping rules (Wharton pp. 109–111; Malki et al., p. 5).
  - Attempt all apps and retain accessible screens and task-specific barriers. Distinguish completion, bounded non-finding, explicitly evidenced lack of support and access barriers. A missing button does not prove I2 or IM12. Apply Step 1's existing uncertain state when evidence cannot settle a condition; observing a control does not establish its technical effectiveness (D12).
  - Separate verbatim text, observable actions/interface states and analyst judgments. All three are retained with their evidence type; only text is sent to the text-coding model. Record app/version, platform/OS, timestamp, language, screen/recording locator, source origin and unit ID. Check the transcript against the screen before segmentation; an exact-span check validates the transcript span, not the transcription itself (D9; Wharton pp. 106, 113–114).
  - A policy opened inside the app remains policy text. Record its link and access path, compare its version with the archived policy and avoid duplicate interface mentions. Preserve OS prompts and third-party ads with their origin, without attributing their wording to the provider. D7's English-first/German-fallback rule includes capturing counterparts and logging language differences separately from the primary walkthrough.
  - Apply D9 and D8 to both captured text surfaces, while distinguishing coding reliability from independent repeat inspection. Report available UI validation material and its limitations; document-only validation cannot establish UI recall. RQ4 pairs like nodes and claim scopes, retains date/version/language differences and uses per-task denominators. Non-finding, unavailable material and silence are distinct; inconsistent claims require human review rather than automatic classification (Malki et al., pp. 4–5; D7–D9).
  - The proposed policy-coding order remains unresolved. Any prior familiarity from sampling, policy capture or route preparation is recorded; delaying model-code review alone cannot remove it.
  - D16's synthetic test uses protocol v5 and contains the same missing-export inference. Mark its dependent classifications/counts as historical and pending re-evaluation rather than silently rewriting the fixture or presenting it as an application of v7.
- **Would change if:** the pilot shows that the tasks do not reach the tree nodes; the supervisor clarifies the "post-harm reaction" point of the meeting.

## Update 2026-11-04 — second rating of recorded sessions

- **Status:** proposed (2026-11-04, methodology review M6). Replaces the open "second inspection" question.
- **Choice:** a second analyst (the D8 second coder) rates the recorded sessions of ten randomly drawn apps on Q1–Q4 per action and the task outcome, blind to the first record; no repeat inspection. Subset size to be confirmed.
- **Reason:** tests the analyst's judgments without needing the same device, accounts and versions; fits the existing recording protocol (Mahatody et al. 2010 on recording).

## Update 2026-11-04 (evening) — subgoals, persona, matched states

- **Status:** proposed (submission review R9, W3–W5). T5–T7 recorded as subgoals (recipient/purpose, local/account/server scope, offered action, confirmed endpoint, remainder; account deletion not applicable for apps without accounts); outcomes per subgoal. A short lay scenario and assumed privacy knowledge per task; persona limits stated. "Task unsupported" requires that no other route (e.g., a provider request) offers the function. Language counterparts captured in the same account/consent/settings state before T5–T7. Re-rating tests interpretation of recorded routes only. Evidence: Habib et al. 2019 (SOUPS); Schaffner et al. 2022 (CSCW); Wharton et al. 1994. Platform, device, OS, time limits still fixed in the pilot.

## Decision 2026-11-04 (night) — taken at the author's instruction

- **Status:** proposed — decided by the AI assistant at the author's instruction of 2026-11-04 ("finish the TODOs depending on reasoning, best practice, literature and context"); marked orange in the thesis until the author or supervisor confirms it.
- **Choices:**
  - Platform: an app listed in both stores is inspected on Android, an App-Store-only app (including Apple's preinstalled apps) on iOS. Android has 72.3 % of mobile page views in Germany (StatCounter, September 2026).
  - Device: Android Studio emulator, Pixel profile, Google Play system image of the newest stable Android release on the first pilot day, one image for all apps, clean snapshot restored per app; fallback a factory-reset Android phone if an app refuses the emulator (recorded). iOS: a physical iPhone on the iOS version of the first pilot day, updates off.
  - Time: route search stops after 5 minutes per task or subgoal; the evaluation of a located route is not timed; a session takes about 60–75 minutes. If the pilot finds a route only after the limit, the limit is raised before the freeze for all apps.
  - Second rating of recorded sessions: ten apps (a fifth; O'Connor & Joffe 2020, p. 5: 10–25 % typical).
  - Order adopted: each app is walked through before its policy's model codes are reviewed (same mechanism as the label-hidden check, Schroeder et al. 2025).
  - Supervisor's "post-harm reaction" point read as the mechanisms a user needs after something went wrong: T3 (what happened), T5 (stop flows), T6/T7 (take out, remove), and a new subgoal T3c: how to report a problem to the provider, reach the data protection officer, and that a complaint to a supervisory authority is possible (GDPR Art. 13(1)(b), 13(2)(d), 77). The supervisor can narrow this reading.
- **Protocol:** walkthrough protocol version 8.

## Closure 2026-11-05 — author's instruction

- **Status:** closed. The author instructed that the walkthrough is applied to all 50 apps, not to 10 or 12, and that every decision about it is closed so it is not reopened.
- **Final scope:** all 50 apps of the sample are walked through. No walkthrough subsample, no six-and-six platform balance, no rank-order slots (D1, sampling protocol). The only exclusions are access barriers recorded per task (payment, identity verification, paired device); the app stays in the document sample.
- **Closed with it:** the platform rule (Android for apps listed in both stores, iOS for App-Store-only apps), device, time limit and session sequence of the 2026-11-04 (night) decision, protocol v8; the walkthrough-before-model-code order; the T3c redress subgoal; the matched-state language capture; and the second rating of recorded sessions of ten apps. The second rating is a validation step on recorded sessions, not a walkthrough scope; the question of who the second coder is stays in D8.
- **Not decisions:** the exact emulator image, iOS version and patch level are recorded once on the first pilot day (protocol), as measurements. The pilot may report that a task does not reach a tree node, but that would be a finding, not a reason to reopen the scope.
- **Removed:** the open items "platform for the 36 apps listed in both stores", "time one session takes", "device and OS version" and "second inspection of a subset"; the "would change if" clause on the supervisor.

## Update 2026-11-05

The pilot clauses above no longer hold: the method has no pilot or instrument test, see [D20](D20_no-pilot.md).
