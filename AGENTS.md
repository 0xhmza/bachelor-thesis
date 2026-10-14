## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- When graphify-out/graph.json exists, run `.\graphify.ps1 query "<question>" --budget 1200` before exploring project content. Query returns source locations; open the relevant passages to verify facts. Use `.\graphify.ps1 path "<A>" "<B>"` for relationships and `.\graphify.ps1 explain "<concept>"` for focused concepts. Include this guidance in subagent prompts that explore project content.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, LaTeX or Markdown, run `.\graphify.ps1 refresh`. This project wrapper also indexes LaTeX sections, inputs and citations, which upstream Graphify does not detect. It reuses only semantic extractions whose source hash still matches. Refresh semantic content with the installed Graphify skill when reported stale; never treat an old plan as a current decision.
- A committed graphify-out/graph.json is rewritten whole on every build, so a large diff to it in a pull request is expected. Do not flag it as churn or suggest skipping the graph rebuild or its hooks.

## Thesis authority

- Main document: `03_Thesis/thesis.tex`; write in its chapters and appendices.
- `03_Thesis/proposal/` is the preserved 5 October submission snapshot. Its substantive content has been transferred to the main thesis.
- The 13 October supervisor meeting notes supersede conflicting proposal plans. Methodology flags the outstanding revisions. Do not invent results or resolve open decisions without evidence.
- Keep `_shared/references.bib` as the single bibliography.
- Graph exclusions are in `.graphifyignore`: archives, raw/processed data, PDFs and generated outputs are excluded from semantic extraction. Bibliography and literature file names remain available for navigation; read original PDFs when evidence requires them.
