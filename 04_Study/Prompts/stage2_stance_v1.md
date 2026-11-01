---
task: Stage 2. Code the stance toward each named harm (Axis B)
version: 1
date: 2026-11-01
model: instrument test only; claude-sonnet-5-5 through fresh Claude Code subagents (temperature and seed cannot be set). The pilot selects the study model.
input: units for which stage 1 returned L-HRM, with the harm code and span, and their neighbouring units
output: JSON, see the end of this prompt
changes: first version
---
You will read units from the privacy communication of a health-tracking app. For
each one, stage 1 found a named harm. Code how the text presents that harm. Judge
the wording only, never the intent of the provider.

One harm may carry several stances.
S-ACK acknowledged: the harm is presented as possible.
S-QUA qualified: uncertainty or likelihood language. Record "target": "likelihood
of the event" if it concerns whether the event happens, "severity" if it concerns
how bad the consequence is. Qualification alone is not minimisation.
S-MIN minimised: the harm is dismissed without a reason in the unit or next to it.
If a reason is given, code S-QUA instead.
S-RSP responsibility shifted: responsibility for the harm is placed on the user.
S-DEN denied or prevented: the harm is presented as impossible or prevented.
If stage 1 was wrong and no concrete harm is named, return "stances": [] and
"reject": true.

Every stance needs "span" (an exact copy of the shortest supporting words, at most
25 words) and "reason" (at most 12 words). If unsure, keep it and add "unsure": true.

EXAMPLE (constructed)
Unit: "In the unlikely event that an unauthorised party accessed your backup, you might experience unwanted contact."
{"unit":"X2","harm":"H-PSY","stances":[{"code":"S-ACK","span":"you might experience unwanted contact","reason":"presented as possible"},{"code":"S-QUA","target":"likelihood of the event","span":"In the unlikely event","reason":"likelihood of the breach, not the harm"}]}

OUTPUT
Return one JSON object and nothing else: {"harms":[ ...one object per unit and harm, as shown... ]}.
