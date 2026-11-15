# Harm trees by use case, version 1

Decision D23 (`00_Admin/Decisions/D23_use-case-subtrees.md`). Builds the harm trees of Chapter 5
the way Knabenhans et al. 2026 (§4) built theirs: use case by use case, one subtree after each,
common sub-trees defined once.

| Input | Content |
|---|---|
| `04_Study/4.3_Analytical-Framework/use_cases_v1.yaml` | One card per use case: six questions (record, derive, phone, leaves, asks, outside), each with components, basis and page evidence |
| `04_Study/4.3_Analytical-Framework/reference_model_v2.yaml` | Definitions of components, capabilities (typed AND/OR formulas) and pathways |

`build_usecases.py` adds the components of each card to those already known, evaluates which
capabilities and pathways become possible, and records what is new: components, capabilities,
routes (new minimal sufficient sets for an existing capability) and pathways. It stops with an
error unless the final state equals the reference model, every component has evidence with a
page and a citation key from `03_Thesis/references.bib`, the check cases (role `check`) add
nothing, and the last two use cases are check cases.

| Step | Command | Result |
|---|---|---|
| Tables and figures of Chapter 5 and Appendix G | `python build_usecases.py <repo root>` | `03_Thesis/tables/usecase-*.tex` |
| Test | `python -m pytest tests` | 14 tests: formulas, closure, order independence, rejection of bad cards |

Needs PyYAML (and pytest for the tests). The cards were drafted by the AI assistant from the
ten papers of the literature review; see D23 for what that does and does not show.
