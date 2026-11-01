---
task: Stage 1. Find every tree node, harm and risk that each unit mentions (Axis A), and flag units for stages 2 and 3
version: 1
date: 2026-11-01
model: instrument test only; claude-sonnet-5-5 through fresh Claude Code subagents (temperature and seed cannot be set). The pilot selects the study model.
input: consecutive coding units of one document, as JSON lines with fields unit, heading, text
output: JSON, see the end of this prompt
changes: first version
---
You will read coding units from the privacy communication of a health-tracking
app. A unit is one paragraph or one block of interface text. Neighbouring units
are there for context. Code only what a unit says, never what the provider may
mean or what is likely to happen.

For every unit, record each of the following that the unit mentions. Most units
mention few or none. A unit with nothing relevant is left out of the output.

COMPONENTS (code L-CMP with the node id). Parts of the system that the text
states.
CO1 health records are logged or sensed. CO2 insights or predictions are derived
from the records. CO3 a long history is kept. CX1 another person can use the
phone. CX2 IP address or device data reach a server. CX3 a device, push or
advertising identifier is used. IM1 an account links records to a person. IM2 a
copy is stored on servers. IM3 a third-party analytics or monitoring service
receives data. IM4 an advertising or attribution partner receives identifiers or
events. IM5 a processor (messaging, support, AI, other) receives tracked health
data. IM6 de-identified or pseudonymised data goes to research or other partners.
IM7 tracked data is sold or drives offers, recommendations or partner products.
IM8 precise location or routes are recorded. IM9 data or profiles can be shared
with other people. IM10 personal data can go outside the EU or EEA. IM11 a
function is available only if the user agrees to extra data sharing. IM12 the
user has no usable way to delete or export the data. IM13 a flow to a third party
has no opt-out.

CAPABILITIES (code L-CAP with the node id). What someone could do, or cannot do.
Listing data types or recipients is not a capability.
K1 locate homes, routes or places. K2 infer personal attributes the user did not
enter. K4 re-identify or link individuals. K5 recognise or profile users across
sessions, apps or services. K6 attackers read stored or intercepted data. K7
authorities obtain the data. K8 insurers or employers use the data against the
user. K9 a partner, family member or person nearby reads the entries. K10 sort
users into classes. I1 the user cannot use a function without agreeing. I2 the
user cannot delete or take out the data. I3 the user cannot stop a data flow.

HARMS (code L-HRM with the category). A concrete negative consequence for a person
or for society.
H-ECO economic (fraud, higher prices, lost job or insurance). H-PHY physical
(injury, stalking, reduced access to care). H-PSY psychological (anxiety, distress,
fear of being watched). H-AUT autonomy (coercion, manipulation, restricted choices
or freedoms). H-DSC discrimination (unequal treatment on health or demographic
traits). H-REP reputational (damage to reputation or dignity). H-SOC societal
(chilling effects, surveillance of groups). Add "tag": "T-REL" if the harm damages
trust or a close relationship.

GENERIC RISK (code L-GEN). Possible misuse or risk without a concrete consequence.
If a consequence is named, code L-HRM instead.

INCIDENT DETAILS. P-BRC what would happen to the user if data were exposed. P-INC
concrete steps to detect, respond to or report incidents. P-NOT only a general
promise to notify, for example as the law requires.

STATUS of each node or harm: "asserted" (stated as fact), "possible", or "denied"
(stated as not happening or not done).

FLAGS for each unit you return: "harm" is true if you coded L-HRM. "protection" is
true if the unit claims a measure or a commitment that limits exposure or misuse,
or offers broad safety language.

RULES
- Every code needs "span": an exact copy of the shortest words in the unit that
  support it, at most 25 words. Never paraphrase a span.
- "reason": at most 12 words.
- If you are unsure, still return the code and set "unsure": true. Do not drop it.
- A prediction made for the user is K2 only if the text says it derives something
  the user did not enter. Presented as a feature it has status "asserted" and is
  not a harm.

EXAMPLES (constructed)
Unit: "We share device identifiers and usage data with analytics partners to improve our services. We never sell your health data."
{"unit":"X1","codes":[{"code":"L-CMP","node":"IM3","status":"asserted","span":"We share device identifiers and usage data with analytics partners","reason":"names recipient and data"},{"code":"L-CMP","node":"CX3","status":"asserted","span":"device identifiers","reason":"identifier used"},{"code":"L-CMP","node":"IM7","status":"denied","span":"We never sell your health data","reason":"sale is denied"}],"flags":{"harm":false,"protection":true}}
Unit: "In the unlikely event that an unauthorised party accessed your backup, you might experience unwanted contact."
{"unit":"X2","codes":[{"code":"L-CAP","node":"K6","status":"possible","span":"an unauthorised party accessed your backup","reason":"attacker reads stored data"},{"code":"L-HRM","harm":"H-PSY","status":"possible","span":"you might experience unwanted contact","reason":"names a consequence"},{"code":"P-BRC","status":"possible","span":"you might experience unwanted contact","reason":"consequence of exposure"}],"flags":{"harm":true,"protection":false}}

OUTPUT
Return one JSON object and nothing else: {"units":[ ... one object per unit that has at least one code, in the form shown above ... ]}.
