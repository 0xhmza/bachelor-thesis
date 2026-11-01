# Privacy-Focused Cognitive Walkthrough Protocol

**Version:** 4 · **Date:** 2026-11-01 · Operational version of the methodology's
App Walkthroughs section, of [D10](../../00_Admin/Decisions/D10_walkthrough.md) and of D15's single health-tracker domain.
Method: Wharton, Rieman, Lewis & Polson (1994), *The Cognitive
Walkthrough Method: A Practitioner's Guide*, in Nielsen & Mack (eds.),
*Usability Inspection Methods*, pp. 105–140. The four questions below are from
Table 5.1, p. 106.

Walkthroughs are done **manually** — this is the part of the study that is not
automated. The point is to make every walkthrough identical, so differences you
find are differences between apps and not between sessions.

**Subsample:** 12 health-tracking apps, six on Android and six on iOS. Fill
the slots in rank order, **alternating** Android and
iOS, without reusing an app. The balance serves coverage, not platform
comparison. Apps that need an unavailable paired device, payment, or identity
verification are skipped with a recorded reason; unfilled slots are reported.

## Setup

- Device / emulator: TODO
- OS version: TODO
- Fresh install for every app, no restored backup, no existing account
- Region set to Germany, system language: TODO
- Screen recording on for the whole session

## The adaptation: the tasks are privacy tasks

A standard cognitive walkthrough asks whether a user can complete the app's own
tasks. Here the tasks are the user's **privacy** goals. For each task, walk the
action sequence and ask Wharton et al.'s four questions at every step:

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
| T2 | Find out what the app or provider **derives** from that data | RQ1 capability `K-INF`; nodes CO2, K2, K10 (codebook v5) |
| T3 | Find out what happens if the data is exposed, and how incidents are handled | RQ1 details `P-BRC`, `P-INC`, `P-NOT`; node K6 (codebook v5) |
| T4 | Reach the privacy policy from inside the app | cross-surface link (RQ4) |
| T5 | Turn off sharing with third parties | control, and how it is framed; nodes IM3, IM4, IM13, I3 |
| T6 | Export the data | control; nodes IM12, I2 |
| T7 | Delete the account and the data | control; nodes IM12, CO3, I2 |

**Do not anticipate outcomes.** Record every task in one of four neutral
categories — **completed**, **information not found**, **task unsupported**,
**access barrier** — together with *where* in the action sequence it stopped
and against which of the four questions. The pilot fixes each task's starting
point and time limit; "not found" means not found within that limit.

## Fixed session sequence

Do these steps in this order, every time:

1. **Store listing** — screenshot the full listing, including the data-safety /
   privacy-label section, before installing.
2. **Install and first launch** — capture every screen shown before any account
   exists.
3. **Onboarding** — capture each screen. Note every consent, permission request,
   and pre-ticked checkbox.
4. **Account creation** — note what is mandatory vs. optional. Do not enter real
   personal data.
5. **Permission prompts** — record each one verbatim, and what the app says the
   permission is for.
6. **Run T1–T7** in order, recording each step against the four questions.
7. **Privacy settings** — record how many taps from the home screen, and the
   defaults *before* changing anything.
8. **Ads** — note any ad shown during the session and whether it says anything
   privacy-related.

## Recorded per app

| Field | Value |
|---|---|
| App ID (from sampling protocol) | |
| App | |
| Version | |
| Platform | |
| App category / relevant features | descriptive metadata; no category stratum |
| Date of walkthrough | |
| T1 outcome | completed / not found / unsupported / access barrier; where it stopped |
| T2 outcome | completed / not found / unsupported / access barrier; where it stopped |
| T3 outcome | completed / not found / unsupported / access barrier; where it stopped |
| T4 taps to privacy policy | |
| T5 outcome + default state before change | |
| T6 outcome | |
| T7 outcome | |
| Taps to privacy settings | |
| Permissions requested | |
| Consent screens shown | |
| Anything about inference / breaches / incidents shown in the UI? | verbatim quote if yes |
| Ads seen, privacy-related content in them | |
| Screen recording file | |

## Notes discipline

Write observations in the moment, not from memory afterwards. Distinguish
clearly between **what the screen said** (quote it) and **what you concluded**
(mark it as interpretation). Only the first goes into the results chapter as
data.

Any privacy-relevant text captured here enters the corpus as source
`in_app_ui` and is coded with the same codebook as the documents.

## Ethics rules that bind every session

Throwaway accounts and synthetic data only. No real name, address, health data,
or payment details. Apps that require identity verification or payment stay in
the document sample but are skipped here. See
[`../Ethics/README.md`](../Ethics/README.md).

## Version history

| Version | Date | Change | Reason |
|---|---|---|---|
| 1 | 2026-09-18 | Added the seven privacy tasks, the four Wharton et al. questions, and the per-task record fields | Aligns the instrument with §4.4 of the proposal |
| 2 | 2026-10-05 | "Expected to fail" removed; four neutral outcome categories; alternating Android/iOS slot filling; payment/ID-verification apps skipped here, not excluded from the sample; codebook v3 codes | Anticipated outcomes risk steering an analyst-based inspection; alignment with the current proposal |
| 3 | 2026-10-28 | Twelve apps across the health-tracker sample, six per platform without category slots; descriptive feature metadata; codebook v4 | Author's clarification of one study domain, D15; totals and task procedures retained |
| 4 | 2026-11-01 | Each task tied to nodes of the reference model; count of taps kept for every task; codebook v5 | D10, D12: walkthrough outcomes must attach to tree nodes |
