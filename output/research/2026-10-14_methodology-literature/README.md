# Methodology literature research — 14 October 2026

The deliverable is 01_Literature/Methods-Reading-List.md, with a searchable HTML
view, ranked DOI import list and structured JSON catalogue alongside it.

The selection follows the supervisor meeting of 13 October: app-focused reviews,
German/English store selection, no fixed domain quotas, missing policies,
mental-health/sleep/fertility scope, systematic capture, checklist walkthrough,
two coders, an LLM feasibility test and literature-derived harm trees.

## Evidence and reproducibility

- candidates.tsv: 83 candidate DOI/version identities and priority categories.
- annotations.tsv: stage, concrete methodological use and transfer limits.
- evidence/01.json through 83.json: raw Crossref/DataCite registration records.
- evidence/publisher-checks.json: publisher reconciliation of the FQS 2025 title.
- metadata.json: reconciled titles, authors, years, available abstracts and URLs.
- verification.json: final count, uniqueness, priorities and bibliography hash.

Run the project interpreter on verify_metadata.py, then compile_list.py to
reproduce the catalogue from cached evidence. DOI identity is checked before
compilation. Early title mismatch/HTTP diagnostics were resolved before the
final pass, which matched all 83 records, including publisher reconciliation.

## Search coverage and limits

The starting set was the project bibliography and latest meeting notes.
Targeted publisher/author searches covered mHealth privacy app reviews,
female/mental-health/sleep apps, European store reviews, cognitive and critical
walkthroughs, content-analysis codebooks, intercoder reliability, reporting
guidelines and LLM validation. Reference follow-up identified additional
methodological and official resources. This is a broad, curated reading
resource, not an exhaustive systematic review or a completed PRISMA exercise.

Malki's Methods were inspected in the local published PDF and Alfawzan's Methods
on the full publisher page. Other entries use bibliographic records, available
abstracts/landing pages and method descriptions. What to borrow is an editorial
judgment; read full Methods and supplements before adopting a protocol.

The interactive table was checked for row count and search, priority, category
and no-result behaviour. Markdown tables, DOI uniqueness, contiguous rank,
annotations and Unicode were checked. No thesis or bibliography edits were
made by this research task.
