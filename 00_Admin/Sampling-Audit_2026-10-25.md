# Sampling audit — 25 October 2026

**Conclusion:** the stored ranking is reproducible, but the sample should not
be frozen yet. Cross-store identity errors, missing-count handling and screening
decisions need correction or author review. Reproducing a result is not evidence
that its app identities and eligibility judgments are correct.

This audit reads the archived App Store v007, Google Play v004 and ranking v003
inputs, logs, cache, screening sheet and outputs. It makes no live store requests
and changes no production collection, matching configuration, screening decision,
generated thesis table or selected sample. Eligibility review remains the author's
responsibility; this is not a certification of all 275 judgments.

Reproduce with:

```powershell
python scripts/sampling-audit/v001/audit.py
python -I -m unittest discover -s scripts/app-ranking/v003/tests
```

The [audit script](../scripts/sampling-audit/v001/audit.py) writes its evidence
to its ignored `output/` folder: `audit.json`, `main-cascade.csv`,
`matched-listings.csv`, `missing-play-review-counts.csv` and an isolated replay.
It hashes the production inputs and outputs before and after execution.

## 1. What works mechanically

- The two collectors use the same 49 queries and German storefront settings.
- The App Store main frame contains 1,440 positions and 848 distinct listings;
  Google Play has 1,178 search hits in total, 1,138 within depth 30, and 645
  distinct product pages. The final cache contains 645 successful, distinct rows;
  the final page-progress log runs from 1/645 to 645/645.
- Removing preinstalled listings gives 846 Apple and 644 Play listings. The
  current matcher produces 1,367 candidates, including 123 matched pairs. These
  are counts under the current matching implementation, which has errors below.
- The stored calibration is reproducible: 114 positive matched pairs,
  c = 0.08958070788703418. The original 47 selected apps and their order reproduce.
- The main cascade is 70 candidates reached = 47 selected + 12 provider skips +
  11 E1 exclusions. No main candidate is pending. All selected providers are
  unique under v003's provider key, and selected developer IDs are unique within
  each store. Apple and Samsung are blocked from the ranked group as configured.
- All 79 selected store listings have observed score inputs and price zero.
  All 41 selected Play listings contain a privacy-policy URL; this checks URL
  presence, not policy validity or applicability.
- The screening sheet contains 275 unique store/ID keys: 156 eligible and 119
  excluded (E1 114, E2 1, E3 2, E4 1, E5 1). Every key exists in the collections.
  No recorded matched pair has contradictory eligible/excluded decisions.
- The eight existing ranking tests pass. Their coverage does not include the
  different-product matches documented below.

All 27 structural and replay checks pass, including exact reproduction of all
58 sensitivity rows, the full report, selection and exclusion outputs, and the
50-row generated table. Before/after hashes confirm that production artifacts
were not changed. The machine-readable checks and source hashes are in
`audit.json`. These passes do not invalidate the substantive findings below.

The 11 exclusions in the main cascade and the 119 exclusions in the screening
sheet are not conflicting counts: the latter covers listings screened for the
main selection and sensitivity variants, including listings never reached by the
main ranking. Likewise, a provider skip is not an eligibility exclusion.

## 2. P1 — Different products are merged across stores

The [matching rule](../scripts/app-ranking/v003/rank.py) accepts the same first
word (at least three characters) plus the same normalised provider. It then
greedily chooses the App Store match with the highest rating count. A shared
brand or generic first word does not identify an app.

The archived names, bundle IDs and product IDs establish these reference cases:

| Play product | App Store product paired by v003 | Proposed same-product App Store ID |
|---|---|---|
| Nike Run Club (`com.nike.plusgps`) | Nike Training Club (`301521403`) | Nike Run Club, `387771637` |
| Nike Training Club (`com.nike.ntc`) | Nike Run Club (`387771637`) | Nike Training Club, `301521403` |
| BabyCenter (`com.babycenter.pregnancytracker`) | Pregnancy Tracker App - WTE (`289560144`) | BabyCenter Pregnancy Tracker, `386022579` |
| Abnehmen für Männer (`menloseweight.loseweightappformen.weightlossformen`) | Abnehmen für Frauen (`1502526521`) | Abnehmen für Männer zu Hause, `1460546771` |
| Abnehm-App für Frauen (`loseweightapp.loseweightappforwomen.womenworkoutathome`) | No counterpart matched | Abnehmen für Frauen, `1502526521` |

Nike and BabyCenter are selected candidates. Their current rows contain an App
Store listing for a different app. For example, Nike Training Club has bundle ID
`com.nike.niketrainingclub`, whereas Run Club has `com.nike.nikeplus-gps`.
BabyCenter's archived bundle is `com.babycenter.mypregnancytoday`; WTE's is
`com.ryanbond.PregnancyTracker`. Shared developer IDs in these examples do not
make the products identical.

**Diagnostic impact:** adding the five explicit proposed identity pairs in
memory leaves the selected provider set and order unchanged, but corrects two
selected App Store IDs and changes the calibration to 115 positive pairs and
c = 0.08962630023742701. This is a scenario, not an adopted correction. Other
automatically matched pairs still require an identity audit; these five examples
do not establish that the remaining matches are correct.

**Required correction:** establish explicit, evidence-backed product pairs;
do not use a shared first word as sufficient identity evidence. Preserve v003,
put any changed matching behaviour in a new version, and regenerate all reports
and the thesis table together after reviewing the pairs.

## 3. P1 — Missing Play counts silently become zero

Of the 645 Play pages, 240 omit both `Review Count` and `Rating Count`. Only five
other pages contain an explicit review count of zero. These are different data
states, but `load()` in [v003](../scripts/app-ranking/v003/rank.py) uses `or 0`
and gives both states the same numerical value.

The missing-count group includes Periodenkalender Paula (`com.cittacode.paula`,
3,540,694 embedded worldwide installs) and iMumz (`com.pruoo.pruoo_app`, 2,166,851).
Worldwide installs do not imply German reviews; they do demonstrate why absence
of an observed German count should not be treated as proof of zero popularity.
All 240 missing-count pages are outside the initial 100-page collection. None
has an eligible Play screening record in the current sheet.

**Known:** the archived rows lack the fields and the ranking converts them to
zero. **Not established:** whether the missing fields reflect genuinely absent
storefront feedback, an interface limitation or a parsing failure. No original
HTTP bodies are archived for an independent reparse.

**Impact:** selected Play listings have observed counts, but that does not prove
the selection is unaffected. Unknown-count candidates may be ranked too low to
be reached. Missing input values are not logged as eligibility exclusions.

**Required review:** inspect representative missing-count pages, retain missing
as a distinct state and document the handling rule before treating the frame as
fully ranked. An unchanged selected set cannot be claimed until that gap is
resolved or bounded by evidence.

## 4. Screening errors and decisions needing author review

### Kinomap: exclusion reason contradicted by the archived listing

[screening.csv](../04_Study/4.4_App-Sampling/screening.csv), Apple ID `611177969`,
excludes Kinomap under E1 because its listing supposedly states no recording of
the user's data. Its archived description instead says:

> Die App zeichnet deine individuellen Einheiten auf, sodass du den Überblick behalten kannst.

The description also mentions exporting activities to Strava/adidas Running.
This is direct evidence of recording training sessions, relevant to the stated
E1 rule. The current exclusion reason is therefore factually unsupported.

**Impact:** its current score is approximately 2,066, below the selected cutoff
of 3,819. A diagnostic scenario making this candidate eligible does not change
the main sample. It still needs correction in the screening record and a rerun
of the sensitivity variants after an author decision.

### Lady Pill Reminder: a potentially sample-changing borderline exclusion

Play ID `com.baviux.pillreminder` is excluded under E1 as a reminder without
recording. The archived description states that the user can retrieve how many
pills they have already taken in the current cycle:

> Zudem kannst du jederzeit abrufen, wie viele Pillen du im aktuellen Zyklus bereits eingenommen hast.

The description alone does not establish whether this is a user-confirmed intake
record or a count inferred from the configured schedule. That distinction needs
review under the reproductive-health tracking rule. The categorical reason
"no recording" is stronger than the available evidence.

**Impact:** its observed score is 4,742. If the author determines it is eligible,
it enters the 47-app selection and Sleep Monitor leaves. This is a diagnostic
counterfactual, not a change to eligibility or the sample.

### Other decisions still requiring documented review

- Headspace is included as mood tracking, while Calm/7Mind/Insight Timer are
  excluded. A consistent boundary between tracking mood, recording reflections
  and tracking meditation activity must be applied. The audit does not resolve
  this methodological boundary.
- Oviva Direkt (`1556652646`, not a generic exclusion of every Oviva product)
  has E5 with "confirm in the BfArM directory" still in its reason. Its exact
  registry identity/verification evidence should be retained as required by the
  protocol. Current [KBV documentation](https://www.kbv.de/praxis/verordnungen/diga)
  independently names Oviva Direkt für Adipositas as a DiGA; the recorded
  classification is plausible, but that does not supply the missing registry
  audit trail or establish a historical verification date.
- The two E3 exclusions have recorded prices of EUR 9.99; the current selected
  listings are all free to install. Payment requirements after installation are
  a separate walkthrough question, as D4 states.

All screening remains an AI-prepared first pass awaiting the author. No TODO
about author review is removed by this audit.

## 5. P2 — The request-hash trail is incomplete

The final Play output contains one request record (the final Naviki fetch).
The retained Play JSON files together contain valid-format response hashes for
104 of the 645 product-page IDs. For 541 page IDs, the cached parsed row and
capture time remain, but no response hash was located in those retained files.

The collector keeps request hashes only in its process-local `requests` mapping;
its persistent cache stores rows and capture times without those hashes. A
cache-reusing rerun therefore produces a new result without the earlier request
mapping. The final progress log lists cached pages as well as new fetches and is
not evidence that every listed page was requested again in that run.

The cache dates support 100 captures on 24 October and 545 on 25 October, and
the final rows reproduce from that cache. This supports data availability, but
cannot recover the missing HTTP provenance. New collectors should persist the
source URL, response hash, effective storefront and capture time per cached row
and preserve append-only attempt/error logs. Existing hashes cannot be recreated
from parsed JSON as if they were hashes of the original HTTP response.

## 6. P2 — Protocol history and implementation descriptions diverge

- The opening of [sampling_protocol.md](../04_Study/4.4_App-Sampling/sampling_protocol.md)
  says version 2 was fixed before the collection of 23 October. The same file and
  D2 describe ranking revisions on 25 October after collection. The methodology
  now distinguishes this timing, but the protocol's opening still overstates
  what was fixed in advance.
- D2 says developers are matched by ID within a store; v003 actually uses a
  normalised developer-name key for provider grouping. Selected store developer
  IDs happen to be unique, so no current duplicate selected developer was found.
  Documentation should distinguish deduplicating listing IDs from grouping
  providers by name and aliases.
- The older sampling handout still uses E/"German exposure" and describes the
  sample as complete apart from author review. It is a dated snapshot, not a
  substitute for this audit or the current methodology.

## 7. Recommended order before freezing the sample

1. Review product identities and replace permissive automatic pairing in a new
   ranking version, with regression tests for Nike, BabyCenter and gender-specific
   Leap products. Review more than the five known cases.
2. Resolve missing-count semantics and record an explicit policy with evidence.
3. Review the full screening sheet, correcting Kinomap and adjudicating Lady Pill
   Reminder and the mood/meditation boundary; preserve old decisions and reasons
   in a dated change log. Retain the DiGA registry evidence.
4. Rerun the corrected selection and all sensitivity variants. Regenerate the
   sample table from the versioned script, update Results only from those outputs,
   and reconcile protocol history and documentation.
5. Back up the ignored source collections, cache and audit artifacts separately.

No revised methodological rule or corrected sample is adopted by this audit.
