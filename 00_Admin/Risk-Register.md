# Risk register

Reviewed weekly with the weekly log. Likelihood and impact: L / M / H.
Close a risk only when its trigger can no longer occur.

| # | Risk | L | I | Early sign | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|
| R1 | Open decisions (D1–D20) delay the instrument freeze and the start of collection | M | H | No supervisor answer to the question email within a week | Send one batched email; propose a default with evidence for each decision so silence can be read as consent where acceptable | Hamza | open |
| R2 | Second coder not available | M | H | No name by the instrument freeze, which needs the second coder's tree check | Ask the chair / MPI-SP now; fallback: supervisor reviews a sample, limitation reported | Hamza | open |
| R3 | Store or policy pages change during collection | H | M | Different text on re-visit | Archive every source with URL, date, hash and app version at capture | Hamza | open |
| R4 | Scraping blocked or against store terms | M | M | Rate limits, CAPTCHAs | Check terms first; manual capture protocol for blocked sources | Hamza | open |
| R5 | LLM output not reproducible (model updates) | M | M | Same prompt, different labels | Freeze model identifier and settings; keep raw outputs; prefer an open-weight model | Hamza | open |
| R6 | Reading backlog (92 works marked "to read") blocks evidence for decisions | H | M | Decision records without citations | Read by decision: start with the "Start with" column of the reading guide | Hamza | open |
| R7 | Ethics review turns out to be required | L | H | Reply from the ethics contact | Ask for written confirmation before collection | Hamza | open |
| R8 | Registration later than 2026-11-02 compresses the 12-week plan | M | M | Proposal not approved by 10-30 | Keep to the minimum feasible study and cut order of the methodology (Ethical Considerations and Feasibility) | Hamza | open |
| R9 | Data loss | L | H | — | Git + GitHub remote for sources; raw data backed up outside the repository | Hamza | **occurred 2026-10-25:** deleting the old `output/` folder also removed its git-ignored `raw/` data (11 October sampling trial, download-sampling test); recover from Syncthing `.stversions` on another device |
| R10 | With no pilot (D20), the instruments first meet real apps during collection, and a problem found late forces recoding; session time, time per unit and the allocation's spreads are unmeasured estimates | M | H | First sessions run well over an hour; second coder's training takes well over a minute per unit; the models return many invalid spans | Watch the first apps for these signs; log every change and recode the affected material (methodology, instrument freeze); if time runs short, use the methodology's cut order | Hamza | open |
