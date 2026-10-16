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

## Free-copy retrieval

`download_open_access.py` discovers public full text through OpenAlex and Europe
PMC, then tries publisher, university and author-hosted URLs. `oa-sources.json`
records manually discovered alternatives. No login or access-control bypass is
used. The runtime needs `pypdf`; the existing project environment provides it.

`download-status.json` records all 93 requested works, local paths, checksums,
page counts, version labels, retrieval URLs and individual failed attempts.
`evidence/oa/` retains discovery responses and the visual verification of the
scanned Polson report. A retrieved PDF must parse and match its title/DOI; book
previews and supplements are rejected. The Polson scan is admitted only when
its hash and page count match the visually reviewed certificate.

When PDF retrieval fails but Europe PMC supplies full text with the exact DOI,
the article body, tables and references are saved as readable HTML beside the
source XML. Figure images are not bundled. These copies are labelled HTML,
not PDF. Some project-held copies were reused. The interrupted initial batch
did not retain all retrieval URLs; affected entries state that provenance gap.

Run `.venv/Scripts/python.exe output/research/2026-10-14_methodology-literature/download_open_access.py --missing-only`
from the repository root to retry missing works, then run `compile_list.py` to
regenerate download ticks in the guide and `Download-Checklist.md`. Use
`--ids 8,75` to retry selected catalogue IDs (IDs differ from reading ranks).
`download_report.py` checks file existence and SHA-256 before marking downloads.
This status is availability, not reading completion or automatic inclusion in
the shared bibliography. Missing-source reasons describe the checked sources
and retrieval environment; they do not establish that a paper is paywalled.

## Second retrieval pass — 16 October 2026

Six more verified copies were added, bringing the corpus to 62 PDFs and 15 HTML
full texts (77 of 93 works). Five came from public hosts: Spencer 2000 (DePaul author page), Habib et al. 2020
(Usable Privacy Policy Project), Krippendorff 2004 (Penn repository, author
manuscript), Solove 2006 (Yale course-hosted copy of the Penn Law Review article)
and Doan et al. 2025 (University of Luxembourg repository). The sixth, Nowell et al.
2017 (SAGE gold open access), arrived as a browser download and was filed with
`import_manual.py`. The Solove and Doan sites
failed Python's certificate store; `download_open_access.py` now retries the same
honest request through the Windows store (`curl_get`), which still verifies the server.

The 16 still missing fall into three groups, recorded per item in
`download-status.json` and the checklist:

- **Open access but blocked for scripts (5):** Sunyaev 2015 (OUP), Light et al. 2018
  (Salford preprint, a .doc), Duguay & Gold-Apel 2023 (SAGE gold OA), Braun & Clarke
  2021 (UWE repository), Lombard et al. 2002 (Cleveland State accepted postprint).
  Publishers answer scripted requests with HTTP 403 or a verification page; Cleveland
  State serves a Cloudflare challenge, which the pipeline does not attempt to pass. The pipeline does not log in, solve
  verification checks or use shadow libraries, so these need a normal browser.
- **Paywalled (10):** no open-access copy appeared in Unpaywall, OpenAlex, Europe PMC
  (all 10), Semantic Scholar (6 of 10; rate-limited or not queried for the rest) or the repository
  and course-page web searches done by hand.
  Includes two books (Krippendorff 2019, Nissenbaum 2009), whose full text would
  need library access.
- **Web-only (1):** the APA App Evaluation Model, cited as a dated web page.

`import_manual.py` closes gaps: save a PDF from a browser or library login into
`01_Literature/PDFs/Methods-Reading/_Inbox/` and run it. A file is filed only if its
page 1 carries a first-author surname and the paper's own title (near the top), its
DOI, or a matching embedded PDF title; a study guide that merely lists the title in
a contents page is rejected (checked during testing). Scans without a text layer can
be filed with `--assume <catalogue ID>`.

A third look the same day found no further scriptable copies: the Northeastern course
link for Wharton et al. 1992 now returns 404; the KU Leuven repository files tried for
Deng et al. 2011 are different works (Wuyts' thesis; Sion et al.); for Moniz & Almeida
2026 only a related master's thesis turned up; and no free copy of Cohen 1960 surfaced.

Verification of the six new files: first-page title and author text were read
directly; each matches its work.
