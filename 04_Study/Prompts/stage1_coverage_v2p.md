---
task: Stage 1, paraphrased wording, to test whether the wording of the prompt changes the counts
version: 2p
date: 2026-11-04
model: two models of different families, fixed before coding and then frozen (D20); versions and parameters are logged in run_log.md. The same prompt is used for both.
input: as stage1_coverage_v2.md
output: as stage1_coverage_v2.md
changes: paraphrase of stage1_coverage_v2.md (same codes, examples and output; reworded instructions); run on the validation sample only, to measure how much the wording changes the labels
---
Below you get paragraphs ("units") taken from what a health-tracking app tells its
users about privacy. Treat the units around a unit as background. Report only what
the words of a unit state. Do not guess at intentions or at what will probably
happen. Skip any unit in which you find nothing from the lists below.

SYSTEM PARTS. Use code L-CMP plus one of these ids when the text states the part.
CO1 the app logs or senses health records. CO2 it derives predictions or insights
from them. CO3 it keeps a long history. CX1 someone else can use the phone. CX2
device data or the IP address arrive at a server. CX3 a device, push or advertising
identifier is in use. IM1 an account ties records to a person. IM2 servers hold a
copy. IM3 an outside analytics or monitoring service gets data. IM4 an advertising
or attribution partner gets identifiers or events. IM5 a processor such as a
messaging, support or AI service gets tracked health data. IM6 de-identified or
pseudonymised data goes to research or other partners. IM7 tracked data is sold or
feeds offers, recommendations or partner products. IM8 the app records precise
location or routes. IM9 data or profiles can be shared with other people. IM10
personal data may leave the EU or EEA. IM11 a function works only if the user
accepts extra sharing. IM12 there is no usable way, in the app or by asking the
provider, to delete the account and the server copy. IM13 a third-party flow cannot
be switched off. IM14 there is no usable way, in the app or by asking the provider,
to get a copy of the data. Deletion or a copy offered on request is not IM12 or IM14.

WHAT SOMEONE CAN OR CANNOT DO. Use code L-CAP plus one of these ids. A mere list of
data types or recipients does not count.
K1 find homes, routes or places. K2 work out personal traits the user never
entered. K4 re-identify or link people. K5 recognise or profile users across
sessions, apps or services. K6 attackers read stored or intercepted data. K7
authorities get the data. K8 insurers or employers use the data against the user.
K9 a partner, relative or someone nearby reads the entries. K10 put users into
classes. I1 the user cannot use a function without agreeing. I2 the user cannot
delete or take out the data. I3 the user cannot stop a flow.

NAMED CONSEQUENCES. Use code L-HRM plus one category when a concrete bad outcome for
a person or society is named.
H-ECO money or livelihood (fraud, prices, job, insurance). H-PHY body and safety
(injury, stalking, reduced access to care). H-PSY mind (anxiety, distress, fear of
being watched). H-AUT freedom of choice (coercion, manipulation, restricted choices
or freedoms). H-DSC unequal treatment on health or demographic traits. H-REP
reputation or dignity. H-SOC society (chilling effects, surveillance of groups).
Add "tag": "T-REL" when trust or a close relationship is damaged.

UNSPECIFIC RISK. Use L-GEN when misuse or risk is mentioned but no consequence is
named. With a consequence, use L-HRM.

USER'S JOB WITHOUT A HARM. Use S-GRS when the text makes the user responsible for
privacy or safety but names no consequence ("keep your password safe, that is up to
you"). With a named consequence, use L-HRM.

INCIDENTS. P-BRC what would follow for the user if data were exposed. P-INC specific
steps for detecting, handling or reporting an incident. P-NOT a plain promise of
notification, for example as the law requires.

For each node or consequence give "status": "asserted" for a stated fact, "possible"
for something that may happen, "denied" for something ruled out. Something ruled out
is still reported, with "denied".

For each returned unit give "flags": "harm" true when L-HRM is present; "protection"
true when the unit claims a measure or commitment limiting exposure or misuse, or
uses broad safety language.

Requirements. Each code carries "span", the shortest word-for-word extract from the
unit that supports it, 25 words at most, never reworded, and "reason", 12 words at
most. If in doubt, keep the code and add "unsure": true; it is checked, never dropped. A prediction offered as a
feature keeps "asserted" and is not a harm; it counts as K2 only if the text says
something is derived that the user did not enter.

Constructed examples:
Unit: "We share device identifiers and usage data with analytics partners to improve our services. We never sell your health data."
{"unit":"X1","codes":[{"code":"L-CMP","node":"IM3","status":"asserted","span":"We share device identifiers and usage data with analytics partners","reason":"names recipient and data"},{"code":"L-CMP","node":"CX3","status":"asserted","span":"device identifiers","reason":"identifier used"},{"code":"L-CMP","node":"IM7","status":"denied","span":"We never sell your health data","reason":"sale is denied"}],"flags":{"harm":false,"protection":true}}
Unit: "In the unlikely event that an unauthorised party accessed your backup, you might experience unwanted contact."
{"unit":"X2","codes":[{"code":"L-CAP","node":"K6","status":"possible","span":"an unauthorised party accessed your backup","reason":"attacker reads stored data"},{"code":"L-HRM","harm":"H-PSY","status":"possible","span":"you might experience unwanted contact","reason":"names a consequence"},{"code":"P-BRC","status":"possible","span":"you might experience unwanted contact","reason":"consequence of exposure"}],"flags":{"harm":true,"protection":false}}

Answer with a single JSON object only: {"units":[ ...one object per unit with at least one code, shaped like the examples... ]}.
