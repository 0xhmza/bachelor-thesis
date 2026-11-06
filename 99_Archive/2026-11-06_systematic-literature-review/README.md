# Systematic literature review (archived 2026-11-06)

The thesis used to carry a PRISMA-style scoping review of the literature: Boolean term
groups, four search strands, eight venues listed in full, four databases, screening
rules R1–R8, a flow diagram and four review sub-questions (LQ1–LQ4). At the supervisor
meeting of 6 November 2026 this was judged to belong to review papers, not to this
thesis; a brief review of at most ten papers replaces it
([D21](../../00_Admin/Decisions/D21_brief-literature-review.md)).

These files are the removed thesis text, kept so that nothing is lost and so that the
evidence can feed the Related Work chapter:

| File | What it was |
|---|---|
| `methodology_section_literature-review-procedure.tex` | Methodology Section 4.2 (procedure, term groups, strands, venues, screening rules, extraction) |
| `results_section_literature-review.tex` | Results Section 5.1 (search flow, screening counts, evidence map, findings per sub-question LQ1–LQ4, gaps) |
| `appendix_F_literature.tex` | Appendix F (term groups, venues, syntax, databases, search strings, corpus inventory) |

The data, scripts and generated tables are unchanged and stay where they were:
`scripts/literature-search/` (v002 run, v003 method), `05_Data/Literature Search/28. Oct/`,
`01_Literature/review/`, `03_Thesis/tables/literature-*.tex` and `03_Thesis/figures/literature-*`.
The `\input` of Appendix F was removed from `thesis.tex`; the chapter texts here refer to
labels that no longer exist in the thesis, so these files do not compile on their own.

To restore: copy a section back into its chapter and the `\input{appendix/F_literature}` line
back into `thesis.tex`. Git history before the commit of 2026-11-06 holds the same text.

The analysis in `results_section_literature-review.tex` (LQ2: no study codes which harms
communication names; LQ4: only one study analyses a health provider's own privacy text) is
the evidence for the gap statements the Related Work chapter still has to state.
