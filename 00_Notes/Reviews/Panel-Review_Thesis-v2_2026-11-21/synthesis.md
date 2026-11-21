## Sprint Contract Synthesis

Unbound run: all five cards disclose criteria_binding_unavailable or make no venue-alignment claim.

Step 1 role-scoped matrix: D1 methodology=block(repairable); D2 domain=warn; D3 methodology=warn, da=block(repairable); D4 perspective=warn; D5 eic=pass; D6 eic=warn.
Step 2: F1 false (no fatal block); F2 true (D1, D3 block); F3 true (D1, D2, D3, D6 warn or worse under majority per dimension); F4 false (D4 warn, not block); F5 true; F0 false.
Step 3: highest-severity fired condition is F2 (severity 90).

dimension_verdicts: [D1=block, D2=warn, D3=block, D4=warn, D5=pass, D6=warn]
fired_conditions: [F2, F3, F5]
da_critical_adjudications: []
editorial_decision=major_revision
