# Privacy-Focused Cognitive Walkthrough Protocol

**Version:** 9 · **Date:** 2026-11-05 · Operational version of the methodology's
App Walkthroughs section, of [D10](../../00_Notes/Decisions/D10_walkthrough.md) and of D15's single health-tracker domain.
Method: Wharton, Rieman, Lewis & Polson (1994), *The Cognitive
Walkthrough Method: A Practitioner's Guide*, in Nielsen & Mack (eds.),
*Usability Inspection Methods*, pp. 105–140. The four questions below are from
Table 5.1, p. 106.

Walkthroughs are done **manually** — this is the part of the study that is not
automated. The fixed tasks reduce procedural variation. The four questions are
analyst judgments about a specified novice, not observations of participants.
Record familiarity and deviations; a fixed order cannot eliminate learning effects.

**Apps:** attempt every sampled app on one available platform.
Unavailable paired devices, payment, identity verification or technical failures
may block one task or the entire inspection. Retain accessible screens and record
each task's barrier; the app stays in the document sample.

**Platform rule (D10, 2026-11-04):** an app listed in both stores is inspected on
Android; an app listed only in the App Store, including Apple's preinstalled apps,
on iOS. Android carries 72.3 % of mobile page views in Germany (StatCounter,
September 2026), and the emulator gives every app the same clean starting state.

## Setup

- Android: Android Studio emulator, Pixel device profile, Google Play system image of
  the newest stable Android release offered on the first collection day; the same image
  (API level and build) for every app. Before each app, the clean snapshot is
  restored (the "wipe"). An app that refuses to run on the emulator is inspected on a
  physical Android phone, reset to factory state, and the deviation is recorded.
- iOS: a physical iPhone on the iOS version installed on the first collection day,
  automatic updates off for the collection period; the app is deleted after its
  session and its study account removed.
- Record the exact image, device, OS version and security patch level once, and
  again whenever one changes.
- Fresh install for every app, no restored backup, no existing account
- Region: Germany. Primary interface language: English; German only if English
  is unavailable (D7). Where both exist, capture counterparts and log differences
  in a separate pass; do not pool its routes/counts with the primary session.
- Screen recording on for the whole session
- Record installed version, date/time, platform, app ID, device/OS, account state,
  and any reset/reinstall limitation of a preinstalled app.
- **Time limits:** the route search of each task (or subgoal) stops after
  5 minutes; the evaluation of a located route is not timed. A session should take
  about 60–75 minutes. The limit applies to every app.
- **Order:** each app is walked through before the model codes of its policy are
  reviewed. Prior familiarity from sampling, capture and route preparation is
  logged.
- **Fixed before main collection (D20, proposed).** Log every deviation.
  - *Starting state:* each session starts from a fresh install on the clean device
    state above. Each task starts from the app's home screen, in the state the
    previous task left; T1–T4 change no setting.
  - *Route preparation:* the analyst searches for the route of a task once, within
    the time limit, documents the action sequence, and then evaluates it against the
    four questions.
  - *Search boundaries:* every screen and menu of the app, its help pages, and the
    documents its own links open. No general web search and no contact with the
    provider. A route the interface or a linked document states, such as a request by
    e-mail, is recorded as an external step and not carried out.
  - *Completion of a subgoal:* the interface shows the information or confirms the
    action. The search stops at completion, at explicit evidence that the function is
    not offered, at an access barrier or at the time limit, and the outcome follows
    the table below.
  - *Synthetic profile:* name Alex Muster; a new throwaway e-mail address per app;
    birth date 15 June 1990; country Germany; no street address or phone number; height
    170 cm, weight 70 kg; gender "not specified" where offered, otherwise the option
    the app's tracked function needs; invented entries for one week of the app's main
    function.
  - *Consent and permissions:* record every option on a consent screen, then take the
    action the screen presents as primary and leave pre-set choices untouched, so that
    T5 meets the state of a first-time user who follows the app. Deny an operating-system
    permission unless the app or the task cannot proceed without it, and record the
    choice.

## The adaptation: the tasks are privacy tasks

A standard cognitive walkthrough asks whether a user can complete the app's own
tasks. Here the tasks operationalise the user's **privacy** goals in the harm
trees. The user is a first-time app user with basic platform-navigation knowledge
and no prior app/policy knowledge; no technical training is this study's
assumption. Each task has a lay scenario (below): the goal in everyday words and
the privacy knowledge assumed. Q1–Q4 are answered for this persona; users with
low literacy, disabilities or a monitoring partner lie outside it. Document the action
sequence before evaluating it (Wharton et al., pp. 109–111). Evaluate the shortest
route located within the recorded search, without claiming a global minimum.
Keep discovery/backtracking separate from route taps. For deletion, prepare the
route up to confirmation; perform the final action only once, at the end.
For each action, ask Wharton et al.'s four questions:

1. Will the user try to achieve the right effect?
2. Will the user notice that the correct action is available?
3. Will the user associate the correct action with the effect they are trying to
   achieve?
4. If the correct action is performed, will the user see that progress is being
   made toward solution of the task?

### Task list — run in this order, every time

| # | Task | Why it is here |
|---|---|---|
| T1 | Find out what data the app collects | baseline: this is what communication normally covers; nodes CO1, CX2, IM1, IM2 |
| T2 | Find out what the app or provider **derives** from that data | RQ1 capability `K-INF`; nodes CO2, K2, K10 (codebook v6) |
| T3 | Find out what happens if the data is exposed, how incidents are handled, and **where to turn after a problem** | RQ1 details `P-BRC`, `P-INC`, `P-NOT`; node K6; subgoal T3c below (codebook v6) |
| T4 | Reach the privacy policy from inside the app | cross-surface link (RQ4) |
| T5 | Turn off sharing with third parties | control, and how it is framed; nodes IM3, IM4, IM13, I3; subgoals below |
| T6 | Export the data | control; nodes IM14, I2 |
| T7 | Delete the account and the data | control; nodes IM12, CO3, I2; subgoals below |

**Lay scenarios** (read before each task; the user is assumed to know that apps can
pass data to other companies, but not which ones):

| Task | Scenario |
|---|---|
| T1 | "You wonder what this app keeps about you." |
| T2 | "You wonder what the app concludes about you from your entries." |
| T3 | "You read that a health app was hacked and wonder what would happen to your data here, and whom you would contact." |
| T4 | "You want to read the rules the app follows with your data." |
| T5 | "You do not want other companies to get your data from this app." |
| T6 | "You want to move to another app and take your history with you." |
| T7 | "You want to stop using the app and leave nothing behind." |

**Subgoals** (outcomes are assigned per subgoal; each records the recipient or
purpose, the scope — phone, account or server — the action offered, the endpoint
the interface confirms and any part left undone):

| Task | Subgoals |
|---|---|
| T3 | T3a consequences of exposure; T3b incident handling and notification; T3c **after a problem**: how to report it to the provider, how to reach its data protection officer, and that a complaint to a supervisory authority is possible (GDPR Art. 13(1)(b), 13(2)(d), 77) |
| T5 | T5a one named recipient or purpose; T5b all optional third-party sharing |
| T6 | T6a a copy of the records in a usable form, in the app or by request |
| T7 | T7a local history on the phone; T7b the account; T7c the copy on the provider's servers (in the app or by request). For an app without an account, T7b is "not applicable", not failed |

The node column maps potential evidence; these tasks do not test every pathway.
Answer each question **yes / no / uncertain**, with a screen locator and reason.
Retain negative judgments even when the analyst can complete the action; analyst
completion does not establish novice success.

**Do not anticipate outcomes.** Use these categories consistently:

| Outcome | Required evidence |
|---|---|
| completed | Information reached or requested action confirmed by the interface; record the exact endpoint (e.g. request submitted versus file received) |
| information not found | Information/control not located within the frozen search and time limit; record the routes searched |
| task unsupported | Explicit evidence that this function is not offered in the relevant scope, in the app **or by another route such as a request to the provider**; a missing button alone is insufficient |
| access barrier | Access requirement or technical failure blocks inspection; record the requirement/error and screens still accessible |

Record elapsed time, stopping reason, route taps and other actions (scrolling,
text entry, external steps) separately. A confirmation does not verify backend
deletion, complete export or cessation of sharing. Non-finding does not establish
I2, IM12, IM14 or any other incapability: use Step 1's uncertain state when evidence
cannot settle a condition.

**Language counterparts:** where both versions exist, the counterpart pass is run in
the same account, consent and settings state as the primary capture and before T5;
each difference is logged with the pair, versions and jurisdictions, the state, the
differing spans, the node or claim scope and whether it is material (adds, removes
or changes a node, a stance or the scope of a protection claim; D7).

## Fixed session sequence

Do these steps in this order, every time:

1. **Identity and store listing** — record app ID and installed version; screenshot
   the current listing, including data-safety/privacy-label information. Date this
   evidence separately; do not overwrite frozen selection data or change membership.
2. **Install and first launch** — capture every screen shown before any account
   exists.
3. **Onboarding** — capture each screen. Note every consent, permission request,
   and pre-ticked checkbox.
4. **Account creation, where needed** — note mandatory/optional fields. Use the
   synthetic profile above and record consent/permission choices. Record earlier
   choices so their effects are not mistaken for untouched defaults.
5. **Baseline privacy settings** — before changing settings, capture their initial
   states and the route/taps from the home screen. Save the onboarding-before-consent
   and initial-settings evidence for RQ4 before route preparation or control tasks.
6. **Run T1–T7** in order, documenting routes and evaluating each action against the
   four questions. Record each starting state and all changes made during T5/T6.
   Prepare and capture all other evidence before T7; deletion is the final account
   action. A blocked task does not erase earlier observations or automatically block
   later tasks that remain accessible.

Capture **permission prompts and ads when they appear**, not at a later fixed
step. Record exact wording, stated purpose, screen locator and origin (provider
app, OS, linked document or third-party ad). Do not attribute OS/ad wording to the
provider. Mark screens requiring consent separately from those visible beforehand.

## Recorded per app

| Field | Value |
|---|---|
| App ID (from sampling protocol) | |
| App | |
| Version | |
| Platform | |
| App category / relevant features | descriptive metadata; no category stratum |
| Date/time, device, OS, region, primary language | |
| Setup, synthetic inputs, account/consent/permission state | |
| Initial settings and earlier changes | screen IDs; distinguish defaults from chosen values |
| Prior familiarity / route preparation / deviations | |
| T1–T7 records | complete one task record below for each, including T4 |
| Taps to privacy settings | |
| Permissions requested | |
| Consent screens shown | |
| Anything about inference / breaches / incidents shown in the UI? | verbatim quote if yes |
| Ads seen, privacy-related content in them | |
| Screen recording file | |

### Task record — repeat for each of T1–T7

| Field | Value |
|---|---|
| Task ID and related nodes/codes | |
| Starting screen, account and permission state | |
| Search/preparation routes, backtracking, elapsed time and limit | |
| Evaluated route | ordered actions, screen IDs and recording timestamps |
| Q1–Q4 at each action | yes / no / uncertain; reason and evidence |
| Outcome and exact endpoint | completed / information not found / task unsupported / access barrier |
| Evidence for outcome and stopping reason | |
| Route taps; scrolling, text entry and external steps | separate counts/record |
| Control changes, displayed feedback, pending requests | |
| Availability at onboarding before consent / initial settings | per node: direct text / visible link / not found within limit / access barrier |

### Text/evidence record — repeat for each captured block

| Field | Value |
|---|---|
| Evidence ID; app ID, platform and installed version | |
| Capture date/time; primary or counterpart language | |
| Screen ID / recording timestamp; task and decision point | |
| Origin and source type | provider UI / OS / linked policy or document / third-party ad |
| Verbatim transcript checked against screen | record corrections before coding |
| Unit IDs after segmentation | one coherent UI block; policy paragraphs separately |
| Linked document URL/version/hash where applicable | compare with archived policy |
| Observable action/state | kept apart from text |
| Analyst judgment / applicability state and reason | kept apart from observations |

## Notes discipline

Write observations in the moment, not from memory afterwards. Distinguish
clearly between **what the screen said** (quote it), **what happened** (actions
and interface states) and **what you concluded** (mark it as interpretation).
All three are retained and can be reported with their evidence type. Only checked
verbatim text enters the text-coding model. Its span check proves a quote occurs
in the transcript, not that the transcript matches the screen.

Provider-authored interface text captured here enters the corpus as source
`in_app_ui` and is coded with the same codebook as the documents. A privacy policy
opened inside the app remains policy text: record the link and path, compare its
version with the archived policy, and avoid duplicate UI mentions. Archive a
different version separately. Preserve OS/ad origin separately from provider UI.

## Where the record goes

The walkthrough is done by hand; the language model never operates the app,
answers the four questions or judges an outcome. Its three outputs enter the
study with distinct roles:

| Output | Enters |
|---|---|
| Findability (outcome, Q1–Q4 reasons, route taps, search record) | task record linked to tree nodes (RQ4); no inference about all users or unvisited routes |
| Interface text (checked transcript, unit/screen IDs, origin, language) | fixed units → D9 LLM stages 1–3 with span check → human decision; captured validation units on both surfaces coded before model output is seen |
| Applicability evidence (screens showing a component or condition) | applicability record (Step 1), with the screen as location; offered controls for Step 3 |

D8's second coder independently codes captured text; this does not establish
independent inspection of the app. The second coder also re-rates the recorded
sessions of **ten apps** drawn with a recorded seed (Q1–Q4 per action and each
subgoal's outcome, blind to the first record); this tests the interpretation of the
recorded routes, not whether a route was missed. Report
available UI validation apps/units/positives and performance where estimable;
apply D9's manual-review/withheld-absence-claim rule to interface claims too.

Where screens and policy appear to disagree, retain both locations and check
scope, version, date and language before reporting inconsistent claims. For RQ4,
keep task-specific denominators, partial access and missing/retrieval-failed
policies separate from silence. Each app is walked through **before** the model
codes of its policy are reviewed (adopted 2026-11-04, D10); record prior policy
exposure in any case.

## Ethics rules that bind every session

Throwaway accounts and synthetic data only. No real name, address, health data,
or payment details. Apps that require identity verification or payment stay in
the document sample; do not cross those barriers, but keep accessible evidence. See
[`../Ethics/README.md`](../4.8_Ethics/README.md).

## Version history

| Version | Date | Change | Reason |
|---|---|---|---|
| 1 | 2026-09-18 | Added the seven privacy tasks, the four Wharton et al. questions, and the per-task record fields | Aligns the instrument with §4.4 of the proposal |
| 2 | 2026-10-05 | "Expected to fail" removed; four neutral outcome categories; alternating Android/iOS slot filling; payment/ID-verification apps skipped here, not excluded from the sample; codebook v3 codes | Anticipated outcomes risk steering an analyst-based inspection; alignment with the current proposal |
| 3 | 2026-10-28 | Twelve apps across the health-tracker sample, six per platform without category slots; descriptive feature metadata; codebook v4 | Author's clarification of one study domain, D15; totals and task procedures retained |
| 4 | 2026-11-01 | Each task tied to nodes of the reference model; count of taps kept for every task; codebook v5 | D10, D12: walkthrough outcomes must attach to tree nodes |
| 5 | 2026-11-02 | Walkthroughs cover all 50 apps, not 12; no platform slots | Author's instruction of 2 November 2026; D10 |
| 6 | 2026-11-03 | "Where the record goes": outputs routed into the applicability record and the LLM-assisted coding; procedure unchanged | Coherence with the policy analysis; D10 update of 3 November 2026 |
| 7 | 2026-11-03 | Defaults captured before control changes, T7 last; explicit outcomes and Q1–Q4 reasons; route/search distinction; evidence/transcript fields; policy/UI separation; partial access, D7 language capture and surface-specific validation limits | Review correction in D10; repairs unsupported inferences and makes the proposed procedure reproducible |
| 9 | 2026-11-05 | No pilot: versions frozen on the first collection day; starting states, route preparation, search boundaries, completion, synthetic profile and consent/permission choices written out | D20: the method is applied to all apps without a pilot |
| 8 | 2026-11-04 | Platform rule; emulator/iPhone setup and versions frozen at the first pilot day; 5-minute search limit per task; lay scenarios and persona limits; T3c after-a-problem subgoal; T5–T7 subgoals; IM14 for export; other-route rule for "task unsupported"; matched-state language pass; ten-app re-rating; walkthrough before policy model-code review | D10 update of 4 November 2026 (submission review R9, usable-privacy card W1–W5; supervisor's post-harm point of 13 October) |
