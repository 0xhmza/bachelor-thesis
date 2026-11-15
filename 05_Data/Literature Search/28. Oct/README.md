# Literature search of 28 October 2026 (frozen)

Search results of the literature review v002 ([D14](../../../00_Notes/Decisions/D14_literature-review-v2.md)),
copied unchanged from `scripts/literature-search/v002/output/` after the run. Read-only; hashes in
`SHA256SUMS` (`sha256sum -c SHA256SUMS`).

| File | Contents |
|---|---|
| `config.json` | Term groups, strands, venues, extraction rules and duplicates merged by hand, as used |
| `run-*.json` | Exact strings, fields, filters, start times and counts per platform |
| `hits-pubmed.jsonl`, `hits-arxiv.jsonl`, `hits-acl.jsonl` | Database hits, one line per hit and strand |
| `ieee-raw.json` | IEEE Xplore results retrieved through its web interface (strings and counts in `log`) |
| `hits-venues.jsonl`, `venues.jsonl.gz` | Venue papers selected by the venue rules; all enumerated venue papers |
| `hits-citations.jsonl` | Backward and forward citations of the four seed papers |
| `abstracts-openalex.json` | Abstracts looked up by DOI for screening only |
| `records.csv`, `merge.json` | Merged records with provenance; counts per source |
| `fulltexts.json` | Open-access locations tried for each record awaiting its full text, and the one used |
| `screening.json` | Counts per rule of the screening log (`01_Literature/review/screening.csv`) |

The downloaded full texts are not kept here (copyright); `fulltexts.json` names their sources.
