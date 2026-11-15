# Risks

L = likelihood, I = impact (L / M / H). Review weekly.

| # | Risk | L | I | Mitigation | Status |
|---|---|---|---|---|---|
| R1 | Open decisions delay the freeze and collection | M | H | One batched email; propose a default for each decision | open |
| R2 | No second coder | M | H | Ask the chair / MPI-SP; fallback: supervisor reviews a sample, limitation reported | open |
| R3 | Store or policy pages change during collection | H | M | Archive every source with URL, date, hash, app version | open |
| R4 | Scraping blocked or against store terms | M | M | Check terms; manual capture for blocked sources | open |
| R5 | LLM output not reproducible | M | M | Freeze model and settings; keep raw outputs | open |
| R6 | Reading backlog blocks evidence for decisions | H | M | Read by decision, core papers first | open |
| R7 | Ethics review required after all | L | H | Written confirmation before collection | open |
| R8 | Late registration compresses the plan | M | M | Keep to the minimum feasible study | open |
| R9 | Data loss | L | H | Git remote for sources; raw data backed up outside the repository | occurred 2026-10-25 (git-ignored raw data deleted with `output/`) |
| R10 | No pilot (D20): instrument problems appear during collection | M | H | Watch the first apps; log every change and recode | open |
