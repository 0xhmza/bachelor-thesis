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

## HTML-to-PDF upgrade — 16 October 2026

The 15 works that were only held as Europe PMC full-text HTML were retried for real
PDFs. The retired PMC package service (`oa.fcgi`, HTTP 404) is replaced in
`download_open_access.py` by NLM's official PMC Open Access dataset on AWS
(`pmc-oa-opendata`), which carries the deposited article PDF for CC-licensed articles.
Only the article's own `PMC<id>.<version>.pdf` is taken, never supplementary files.

Twelve works were upgraded and their HTML and XML fallbacks removed: eleven from the
AWS dataset and the BMJ medicines-apps paper (Grundy 2019) from bmj.com, which answered
this time. Every file's page-1 text was read to confirm it is the article and not a
supplement or web appendix. The record keeps `PMC dataset` or `bmj.com` as the source and
the checklist shows the new version label.

Three remain HTML because no PDF could be fetched without passing a bot check:

| Work | Obstacle |
|---|---|
| Hutton et al. 2018 (JMIR mHealth) | PDF route answers with an empty HTTP 202 (AWS WAF challenge) |
| Tangari et al. 2021 (BMJ) | Cloudflare "Just a moment" challenge |
| Huckvale et al. 2019 (JAMA Netw Open) | HTTP 403; not in the AWS dataset |

All three are gold open access, so a normal browser can save them. Put the PDF in
`_Inbox/` and run `import_manual.py`: it now also replaces an HTML-only copy and deletes
the superseded HTML and XML. The earlier HTML versions remain in git history (commit
`c259e9b`). No typeset rendering of the HTML was substituted for a real PDF. All three were later fetched in the browser-assisted pass below.

## Browser-assisted pass — 16 October 2026

At the user's request the built-in browser pane was used for the works that scripts could
not fetch. No credentials were typed and no verification check was completed by the
assistant: where Cloudflare showed a "Verify you are human" box, the user completed it
or the request was retried later. The pane saves downloads to the user's Downloads
folder; each file was copied into `_Inbox/` and filed by `import_manual.py`, whose
title, first-author and DOI check identified every one (first page also read by hand).
SAGE pages listed the user's university link resolver, so no separate login was needed
there; that is an observation, not an access guarantee.

Fifteen works were added: Cohen 1960, MacQueen 1998, Hruschka 2004, Wharton 1992, Deng
2011, Moniz & Almeida 2026, Feinstein & Cicchetti 1990 and Lombard 2002 (previously
paywalled for scripts); Light 2018, Duguay & Gold-Apel 2023, Sunyaev 2015 and Braun &
Clarke 2021 (open access, blocked for scripts); and Hutton 2018, Tangari 2021 and
Huckvale 2019 (the last three HTML-only copies, now replaced by the real PDFs). Lombard
2002 came as two files with different hashes; one was filed. The corpus is now 89 PDFs
and no HTML copies; the superseded HTML and XML are removed and remain in git history.

Four items are still without a local copy:

| Work | Why |
|---|---|
| Parker et al. 2019 | ScienceDirect article not retrieved: the pane refused navigation to the site's search page and the article's page address (PII) was not found |
| Krippendorff 2019, Nissenbaum 2009 | Books: no licensed whole-book file (per-chapter PDFs or a paid e-book only); a library e-book or loan is the route. Not filed into the corpus or repository |
| APA App Evaluation Model | Living web page, cited as a dated page |
