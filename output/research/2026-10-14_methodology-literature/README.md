# Methodology literature research — 14 October 2026

The deliverable is `01_Literature/Methods-Reading-List.md`, with a searchable HTML
view, ranked DOI import list and structured JSON catalogue alongside it. The
selection follows the supervisor meeting of 13 October: app-focused reviews,
German/English store selection, no fixed domain quotas, missing policies,
mental-health/sleep/fertility scope, systematic capture, checklist walkthrough,
two coders, an LLM feasibility test and literature-derived harm trees.

## Current status (16 October 2026)

93 works: 83 ranked DOI records and 10 official/non-DOI resources. **89 are held
locally as PDFs; no HTML-only copies remain.** Local availability is not reading
status and does not add anything to the shared bibliography.

Four items have no local copy:

| Work | Why |
|---|---|
| Parker et al. 2019 | ScienceDirect article not retrieved; the browser pane refused the site's search page and the article address was not found |
| Krippendorff 2019, Nissenbaum 2009 | Books: no licensed whole-book file (per-chapter PDFs or a paid e-book only). A library e-book or loan is the route; nothing is filed in the corpus or repository |
| APA App Evaluation Model | Living web page, cited as a dated page |

Per-work links, versions and obstacles are in `01_Literature/Download-Checklist.md`.

## Files

| File | Role |
|---|---|
| `candidates.tsv`, `annotations.tsv` | 83 candidate DOI/version identities; stage, methodological use and transfer limits |
| `evidence/01.json` … `83.json`, `evidence/publisher-checks.json` | Raw Crossref/DataCite registration records; publisher reconciliation of the FQS 2025 title |
| `metadata.json`, `verification.json` | Reconciled titles, authors, years, abstracts, URLs; final counts and bibliography hash |
| `verify_metadata.py`, `compile_list.py` | Check DOI identity, then build the guide, JSON, DOI list, HTML view and checklist |
| `download_open_access.py`, `oa-sources.json` | Automated free-copy retrieval; hand-curated alternative locations |
| `import_manual.py` | Files hand-saved PDFs from `01_Literature/PDFs/Methods-Reading/_Inbox/` |
| `download_report.py` | Checks file existence and SHA-256; writes checklist and folder README |
| `download-status.json`, `download-verification.json` | Audit manifest: paths, checksums, page counts, versions, sources, failed attempts |
| `evidence/oa/` | Discovery responses; visual verification of the scanned Polson report |

## Maintaining the corpus

Run from the repository root with the project interpreter (`.venv/Scripts/python.exe`).

- **Rebuild the guide and checklist:** run `verify_metadata.py`, then `compile_list.py`
  (it also reads `download-status.json`). Then `.\graphify.ps1 refresh`.
- **Retry missing works:** `download_open_access.py --missing-only`, or `--ids 8,75`
  for selected catalogue IDs (IDs differ from reading ranks).
- **Add a PDF you obtained yourself:** save it into `_Inbox/` and run `import_manual.py`.
  A file is filed only when page 1 carries a first-author surname and the paper's own
  title (near the top), its DOI, or a matching embedded PDF title. Scans without a text
  layer need `--assume <catalogue ID>`. The importer also replaces an HTML-only copy.

## Retrieval rules

Automated retrieval uses public, honestly identified requests: OpenAlex and Europe PMC
discovery, NLM's PMC Open Access dataset on AWS (article PDFs of CC-licensed papers),
and publisher, university and author-hosted URLs. A certificate-chain failure is retried
through the Windows certificate store (`curl_get`), which still verifies the server.

It does not log in, complete verification checks or use shadow libraries. Where a
publisher blocks scripts, the item goes to a browser session run by the user: in the
16 October browser-assisted pass the assistant typed no credentials and completed no
bot check, and each downloaded file went through the importer.

A retrieved PDF must parse and match its title/DOI; book previews and supplements are
rejected, and the Polson scan is admitted only when its hash and page count match the
visually reviewed certificate. When only Europe PMC full text exists, the article is
saved as HTML beside its source XML as a fallback and labelled HTML, never PDF.

## Search coverage and limits

The starting set was the project bibliography and the latest meeting notes. Targeted
publisher/author searches covered mHealth privacy app reviews, female/mental-health/sleep
apps, European store reviews, cognitive and critical walkthroughs, content-analysis
codebooks, intercoder reliability, reporting guidelines and LLM validation; reference
follow-up added further methodological and official resources. This is a broad, curated
reading resource, not an exhaustive systematic review or a completed PRISMA exercise.

Malki's Methods were inspected in the local published PDF and Alfawzan's Methods on the
full publisher page; other entries rest on bibliographic records, abstracts, landing
pages and method descriptions. What to borrow is an editorial judgment: read the full
Methods and supplements before adopting a protocol. All 83 DOI records were matched
against Crossref or DataCite; the interactive table, Markdown tables, DOI uniqueness,
contiguous ranks, annotations and Unicode were checked. No thesis or bibliography edits
were made by this research task.

## Retrieval history

| Date | Step | Local PDFs / HTML / missing |
|---|---|---|
| 14 Oct | First batch from open sources; some HTML from Europe PMC XML. The interrupted first batch lost some retrieval URLs; affected entries say so | 56 / 15 / 22 |
| 16 Oct | Five copies from public hosts (Spencer, Habib, Krippendorff 2004, Solove, Doan); Nowell saved from a browser download | 62 / 15 / 16 |
| 16 Oct | HTML-to-PDF upgrade: 11 from the PMC Open Access dataset, 1 from bmj.com | 74 / 3 / 16 |
| 16 Oct | Browser-assisted pass: 12 missing works added (Cohen, MacQueen, Hruschka, Wharton, Deng, Moniz & Almeida, Feinstein & Cicchetti, Lombard, Light, Duguay & Gold-Apel, Sunyaev, Braun & Clarke) and 3 HTML copies replaced (Hutton, Tangari, Huckvale) | 89 / 0 / 4 |

The superseded HTML and XML copies are removed and remain in git history (commit
`c259e9b`). One testing incident shaped the importer: a study guide whose contents page
merely listed MacQueen's title passed the downloader's title-word check, so the importer
now also requires the first-author surname on page 1.

Not filed, by choice: two whole-book files for Krippendorff 2019 and Nissenbaum 2009
were not added to the corpus or repository, because no licensed whole-book source was
available.
