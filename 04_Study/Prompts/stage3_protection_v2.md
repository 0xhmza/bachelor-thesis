---
task: Stage 3. Describe each protection claim (Axis C)
version: 2
date: 2026-11-04
model: two models of different families, fixed before coding and then frozen (D20); versions and parameters are logged in run_log.md. The same prompt is used for both.
input: units for which either model set the protection flag in stage 1 (union of both models), with their neighbouring units
output: JSON, see the end of this prompt
changes: header only (two models, union of the stage 1 flags); the instructions are those of version 1
---
You will read units from the privacy communication of a health-tracking app. Stage
1 flagged them because they may claim protection. Describe each claim as written.
Do not judge whether it is true or sufficient. That is a human decision.

MEASURE. T-3RD limits what third parties can access. T-INF uses inferences instead
of raw data. T-DEV keeps or processes data on the device. T-ENC encryption. T-ANO
anonymisation, pseudonymisation or aggregation. T-SEC another security control, such
as access control or an app lock. T-OTH another named technical measure. N-COM a
non-technical commitment about practice, such as "we never sell your data".
C-REA broad safety language that names no specific measure, scope or consequence,
including dismissive wording with no named harm. A checkable measure is never C-REA.

For each measure give "actor" (who is limited or acts), "data" (which data),
"outcome" (the claimed benefit), "conditions" (limits stated). Write "unclear" where
the text does not say. Leave these out for C-REA.

FRAMING. F-FLW the claim is about data flow: less data leaving, fewer recipients.
F-HRM the claim is about preventing a specific bad outcome.
STRENGTH. partial ("reduces exposure"), scoped (a named actor or named data),
absolute ("no one", "always", "ensures").

Every claim needs "span" (an exact copy of the shortest supporting words, at most 25
words) and "reason" (at most 12 words). If unsure, keep it and add "unsure": true. If
a unit claims nothing, leave it out.

EXAMPLES (constructed)
Unit: "Your health data stays on your device unless you turn on backup. This keeps your reproductive health private and protects you from anyone using it against you."
{"unit":"X3","claims":[{"code":"T-DEV","actor":"anyone","data":"health data","outcome":"no one can use it against the user","conditions":"unless backup is on","framing":"F-HRM","strength":"absolute","span":"protects you from anyone using it against you","reason":"prevention claimed for anyone"}]}
Unit: "Your data is safe with us. We use industry-standard security."
{"unit":"X4","claims":[{"code":"C-REA","span":"Your data is safe with us","reason":"no mechanism named"}]}

OUTPUT
Return one JSON object and nothing else: {"claims":[ ...one object per unit, as shown... ]}.
