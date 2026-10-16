"""Compile the verified DOI catalogue and a practical ranked reading guide."""
import csv
from collections import Counter
import hashlib
import html
import json
from pathlib import Path
from urllib.parse import quote
from download_report import load_downloads, md_cell, html_cell, write_checklist

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]
DEST = ROOT / '01_Literature'
downloads = load_downloads()
rows = json.loads((BASE / 'metadata.json').read_text(encoding='utf-8'))
with (BASE / 'annotations.tsv').open(encoding='utf-8', newline='') as stream:
    notes = {int(r['id']): r for r in csv.DictReader(stream, delimiter='\t')}
assert len(rows) == len(notes) == 83
assert all(r['verification'] == 'verified' for r in rows)
assert len({r['doi'].lower() for r in rows}) == 83
first = [1,2,3,11,82,12,9,4,6,7,5,8,16,17,10,13,14,15,18,19,20,76,80,81]
order = first + [r['id'] for r in rows if r['priority']=='B'] + [r['id'] for r in rows if r['priority']=='C']
assert len(order) == len(set(order)) == 83
ranks = {identifier: rank for rank,identifier in enumerate(order,1)}
existing = (ROOT / '_shared/references.bib').read_text(encoding='utf-8').lower()
for r in rows:
    r.update({k:v for k,v in notes[r['id']].items() if k!='id'})
    r['rank'] = ranks[r['id']]
    r['download'] = downloads.get(str(r['id']))
    r['title'] = r.get('display_title') or r['registered_title']
    names = [a.get('family') or a.get('familyName') or a.get('name','Unknown') for a in r['authors']]
    r['author_label'] = names[0] + (' & '+names[1] if len(names)==2 else ' et al.' if len(names)>2 else '')
    r['doi_url'] = 'https://doi.org/' + quote(r['doi'],safe='/.:')
    r['already_in_bibliography'] = r['doi'].lower() in existing
    r['version'] = 'SSRN record' if r['id'] in {80,81} else 'arXiv preprint record' if r['id'] in {68,69} else 'electronic book' if r['id'] in {76,77} else 'government report' if r['id']==79 else 'published article/paper'
    r['evidence_scope'] = 'Verified registration identity; available publisher/author metadata and abstracts. Use recommendation, not full-text critical appraisal.'
    if r['id']==1:
        r['evidence_scope'] = 'DOI verified; project-held published PDF Methods, especially page 4, inspected.'
    if r['id']==11:
        r['evidence_scope'] = 'DOI verified; publisher full-text Methods, screening and independent app assessment inspected.'
rows.sort(key=lambda r:r['rank'])

extras = [
('N1','A','Knabenhans et al. (2026), On the (Privacy) Harms of the European Digital Identity Framework','https://eprint.iacr.org/2026/867','H/C; RQ1/RQ3','Essential harm-tree method: components, capabilities, AND/OR conditions, origins and mitigation limits. No DOI located for the cited ePrint version. Specify May versus September revision; do not mix section/figure numbers.'),
('N2','A',"Wharton et al. (1994), The Cognitive Walkthrough Method: A Practitioner's Guide",'https://ics.uci.edu/~redmiles/ics203b-SQ05/papers/Whartonetal99.pdf','W; RQ4','Original practical CW and four questions, pp. 105–140 of Usability Inspection Methods, ISBN 9780471018773; full book already in local PDFs. No chapter DOI located; do not substitute another CW paper or the entire book.'),
('N3','A','Schaub et al. (2015), A Design Space for Effective Privacy Notices','https://www.usenix.org/conference/soups2015/proceedings/presentation/schaub','D/W/C; RQ4','Notice timing, channel, modality and control: where information appears and whether it is available at decision points. Official SOUPS record gives URL/ISBN, not DOI; accessibility is different from measured understanding.'),
('N4','A','Habib et al. (2019), An Empirical Analysis of Data Deletion and Opt-Out Choices on 150 Websites','https://www.usenix.org/conference/soups2019/presentation/habib','W/D; RQ4','Content/heuristic assessment of end-to-end deletion and opt-out paths. Adapt visible links, broken paths, missing instructions and task barriers to apps. No DOI in official SOUPS record.'),
('N5','B',"Arkalakis et al. (2024), Abandon All Hope Ye Who Enter Here: A Dynamic, Longitudinal Investigation of Android's Data Safety Section",'https://www.usenix.org/conference/usenixsecurity24/presentation/arkalakis','D/R; RQ4','Separate declarations from observed behaviour and snapshot capture from longitudinal changes. Technical verification is outside communication-only scope. No DOI in the official USENIX record.'),
('N6','B','Harkous et al. (2018), Polisis: Automated Analysis and Presentation of Privacy Policies Using Deep Learning','https://www.usenix.org/conference/usenixsecurity18/presentation/harkous','L/C; RQ1–RQ3','Pre-LLM hierarchical policy classification and querying. Compare structured labels/evidence retrieval, not transferable harm-detection accuracy. No DOI in official USENIX conference record; repository versions are separate.'),
('N7','B','American Psychiatric Association, The App Evaluation Model','https://www.psychiatry.org/psychiatrists/practice/mental-health-apps/the-app-evaluation-model','S/A/W','Assessment framework for access/background, privacy/security, evidence, usability and interoperability. Useful checklist or best-app comparison; not a validated harm-communication scale. Living guidance.'),
('N8','B','Article 29 Working Party / EDPB, Guidelines on transparency under Regulation 2016/679','https://www.edpb.europa.eu/documents/guideline/transparency_en','D/W/C','Reference for accessible and layered information, helping decide which notices to capture. Legal guidance without a DOI; limited captures alone cannot establish provider non-compliance.'),
('N9','B','Association of Internet Researchers, Internet Research: Ethical Guidelines 3.0','https://aoir.org/reports/ethics3.pdf','D/W/R','Ethical reflection before collecting material/screenshots, including sensitive or third-party context. Use official guidance and institutional review; public availability alone does not settle ethics.'),
('N10','C','BfArM, The Fast-Track Process for Digital Health Applications (DiGA)','https://www.bfarm.de/SharedDocs/Downloads/EN/MedicalDevices/DiGA_Guide.pdf?__blob=publicationFile','S/A','German regulated/reimbursable-app boundary and local relevance. Record guideline version/date; it does not automatically settle whether your consumer-tracker sample includes DiGA.')
]

intro = """# Ranked methodology reading list — privacy harm communication in health apps

Prepared **14 October 2026**, based on the **13 October supervisor meeting**.

**83 verified DOI records + 10 essential official/non-DOI resources.** This is a research and methodological-inspiration list, not a requirement to cite every item, an exhaustive systematic review, or a claim that every full paper has been read. The thesis bibliography has not been enlarged.

## Ranking and use

The global rank prioritizes direct health-app comparison, decisions raised in the meeting, fit to app/document/inspection research and practical procedure detail. It is an **editorial reading priority**, not a bibliometric or scientific quality score. Absence of a DOI does not reduce the priority of an essential method.

- **A:** essential before finalizing the relevant procedure.
- **B:** strong supporting method/comparator; read relevant sections when making that decision.
- **C:** optional or adjacent inspiration; use if it fits the final scope.

| Stage | At which point it helps | What you should produce |
|---|---|---|
| S | Scope and definitions | Functional health-tracker definition, mental health/sleep/fertility boundaries, German relevance |
| A | App search and selection | Queries, storefront/date, ranking, duplicates, eligibility, payment/access and stopping rule |
| D | Material capture | Source-specific protocol; availability, language, date/version and evidence locations |
| W | Walkthrough | Goals, start state, actions, checklist, four questions, outcomes and barriers |
| C | Codebook and pilot | Units, definitions, examples/counter-examples, evidence spans and revision log |
| I | Two-coder comparison | Training, independent labels, agreement sample, per-code measures and later adjudication |
| L | LLM feasibility | Human reference labels, prompts/model/settings, held-out evaluation and stability |
| H | Harm tree | Literature-derived capabilities, actors/access assumptions, applicability and mitigation limits |
| R | Reporting | Methods transparency, denominators, limitations and evidence-linked interpretation |

RQ1 = coverage; RQ2 = stance; RQ3 = protection framing; RQ4 = surfaces. These retain the existing RQ labels, without assuming the old sampling plan is still current.

## First reading route

"""
parts = [intro,'Download ticks, local files and obstacles are recorded in the [complete download checklist](Download-Checklist.md). A tick means available locally, not read. HTML full text is distinguished from PDF.\n\n','| Global rank | Source | Start here / helps with | Download |\n|---:|---|---|---|\n']
for r in rows[:20]:
    parts.append(f"| {r['rank']} | **{r['author_label']} ({r['year']})** — [{r['title']}]({r['doi_url']}) | {r['when']} | {md_cell(r['download'])} |\n")
parts.append("""

Read **N1 (harm trees), N2 (practical CW guide) and N3–N4 (privacy notices and controls)** alongside the corresponding DOI papers.

## Meeting decision → reading → extraction target

| Decision from the meeting | Start with | Record while reading |
|---|---|---|
| Define health trackers, mental health, sleep and fertility | Hutton; Robillard; O'Loughlin; Simon; Dehling; APA model | Tracking/derivation functions versus information/intervention only; store categories do not define the domain |
| German/English store search; first 50 without quotas | Malki; Alfawzan; Schultchen; Sunyaev; PRISMA-S | Exact queries, market/platform/date, candidate ordering, duplicates, eligibility and stopping |
| Ratings/downloads and sample-size justification | Malki; Alfawzan; Sunyaev; MARS-G; Simon | Which popularity signal and why; threshold rationale; pilot workload/coverage |
| Apps without privacy policies | Sunyaev; Robillard; O'Loughlin; Parker | Policy availability as an outcome and separate denominators for policy-text analysis |
| Payment, trial, account and native/platform apps | Alfawzan; Schultchen; Simon; APA model | Free installation versus usable functions; account/card/pairing barriers; one consistent native-app rule |
| English first, German fallback | MARS-G; European app reviews; PRISMA-S | Rule per material type, fallback reason, comparable interpretation across languages |
| Policies, stores, sites and marketing | Malki; Alfawzan; Parker; Light; N3 | Systematic search/capture boundary, dates/versions, unavailable sources and quotation locations |
| Cognitive walkthrough checklist | Polson; Wharton/N2; Mahatody; Spencer; Hutton; Habib/N4 | Goal, start state, user knowledge, action visibility, goal connection, feedback and outcome |
| Two coders | O'Connor/Joffe; McDonald; Campbell; MacQueen; Hayes/Krippendorff | Same material independently coded under a frozen manual before discussion |
| Agreement statistics | Hallgren; Cohen; Hayes/Krippendorff; Artstein/Poesio; Gwet; Feinstein | Nominal/ordinal/unit/span distinctions, per-code positives/negatives, missingness and prevalence |
| LLM pilot | Rodriguez; Törnberg; Pangakis; Baumann; Mayring 2025 | Independent human reference set, task/code-specific precision/recall, stability and missed mentions |
| Capabilities, harm tree and the 'best app' | N1; Citron/Solove; Martin et al.; Niksirat; Deng; NISTIR | Source for each capability, actor/access conditions, consequence and definition of 'best' |
| Post-harm responses and accessibility | Zou; Habib; LaMonica; N3 | Candidate response/contact/deletion mechanisms, notice location and access burden. Meeting wording remains ambiguous; do not invent an outcome criterion |
| Clear RQ–method–justification links | SRQR; app Methods sections; PRISMA-S/ScR | RQ → method → collected data → analysis → rationale → limits |

### Method distinctions to keep explicit

1. **No universal '50 apps' rule:** similar sample sizes are precedents, not statistical proof. Justify a fixed stopping rule through scope, coverage and pilot workload.
2. **Popularity versus privacy quality:** stars, rating counts, download bands and recent reviews measure different things. Malki selects the top 20 by reviews in the previous 12 months, not average stars. Your German-market criterion needs its own rationale.
3. **Iterative discussion versus independent double coding:** Malki develops a codebook through iterative independent coding/discussion and subsequent first-author coding in batches. That is not automatically a two-coder reliability study on the same frozen validation material. Measure agreement before adjudication.
4. **Different walkthrough traditions:** Light studies app context and lifecycle; Polson/Wharton analyse goal/action learning and feedback; Hutton provides privacy heuristics. Malki explicitly combines cognitive walkthrough and heuristic evaluation. Name the component you adopt.
5. **Different coding traditions:** structured, reproducible content coding and reflexive thematic interpretation need different quality criteria. Do not claim reflexive thematic analysis while describing consensus coding and kappa without explaining the distinction.
6. **Human agreement versus LLM validity:** coder agreement supports label reproducibility; model evaluation needs independent reference labels, precision/recall and evidence-span checks. Neither alone proves the truth of absence claims.

## Full ranked catalogue by methodological use

Ranks are global; grouping helps you find the stage currently being designed. Each item has a verified DOI record, concrete use and transfer limit.

""")
categories = ['App reviews','App appraisal','Walkthrough','Coding','Agreement','Review/reporting','Policy annotation','Privacy interfaces','LLM annotation','Context/harm']
for category in categories:
    parts += [f'### {category}\n\n','| Rank / priority | Source and DOI | When / what it helps with | Transfer limit | Download |\n|---|---|---|---|---|\n']
    for r in [x for x in rows if x['category']==category]:
        tag = '' if r['version']=='published article/paper' else f" **[{r['version']}]**"
        if r['id']==80:
            tag += ' [2022 law-review version](https://www.bu.edu/bulawreview/files/2022/04/CITRON-SOLOVE.pdf).'
        if r['id']==81:
            tag += ' [2025 law-review version](https://georgetownlawtechreview.org/wp-content/uploads/2025/01/No_Cookies_For_You_Martin_Nissenbaum_Shmatikov-2025.pdf).'
        parts.append(f"| **{r['rank']} / {r['priority']}** | **{r['author_label']} ({r['year']})** — {r['title']}.{tag}<br>[{r['doi']}]({r['doi_url']}) | **{r['when']}**<br>{r['use']} | {r['caution']} | {md_cell(r['download'])} |\n")
    parts.append('\n')
parts += ['## Important sources with no DOI for the cited version or living official guidance\n\n','| ID / priority | Source | When | Use / version limit | Download |\n|---|---|---|---|---|\n']
for identifier,priority,title,url,when,use in extras:
    parts.append(f'| **{identifier} / {priority}** | [{title}]({url}) | {when} | {use} | {md_cell(downloads.get(identifier))} |\n')
parts.append("""

## App-review comparison sheet

Use the same extraction headings for Malki, Hutton, Shipp, Alfawzan, O'Loughlin, Robillard, Sunyaev, Schultchen, Simon and the recent mental-health studies:

| Extract | Questions to answer |
|---|---|
| Domain | What makes an app eligible? Tracking versus intervention/information-only? |
| Sampling frame | Which stores, countries, platforms, dates and discovery route? |
| Search | Exact queries/categories, candidate order and result boundaries? |
| Selection | Duplicates, ranking signal, threshold rationale, stopping and exclusion reasons? |
| Access | Payment/trial/card/account/pairing/language/device barriers? |
| Sample unit | App, store listing, provider, shared policy or text unit? |
| Missing policy | Exclusion, outcome or unavailable source? Which denominator? |
| Corpus | Policies, labels, stores, websites, screens, ads or technical measurements? |
| Walkthrough | Tasks, initial state, evaluator assumptions, synthetic data, capture and outcomes? |
| Coding | Analysis tradition, units, labels, evidence, pilot and codebook iterations? |
| Coders | Same versus different material, independence, training and reconciliation? |
| Agreement | Statistic, sample/codes/units, prevalence and pre-adjudication labels? |
| Claims | What does absence/discrepancy/risk mean, and what cannot be concluded? |
| Borrow/adapt/reject | Fits the last meeting, needs adaptation, or would expand scope? |

## Verification and limits

- All **83 DOI records** were matched against Crossref or DataCite on 14 October 2026. This verifies bibliographic identity, not quality or applicability.
- Registry/publisher subtitle differences were reconciled. FQS 2025 has a German registered title and an English publisher version; they were matched manually.
- **Version matters:** Citron/Solove = 2021 SSRN record / 2022 law-review publication; Martin et al. = 2023 SSRN record / 2025 law-review publication; Moniz/Almeida = online 2025 / issue 2026; Doan = registered 2025 proceedings volume although the project key says 2024. The Krippendorff DOI identifies the fourth-edition electronic book.
- Malki's Methods were inspected in the project-held published PDF, and Alfawzan's full-text Methods/screening/assessment were inspected on the publisher page. Other recommendations draw on registration metadata, available abstracts/landing pages and method descriptions. **This is not a full-text critical appraisal of every work.** Read Methods and supplements before adopting a procedure.
- Some publisher pages were access-blocked. Inaccessible procedures are not presented as inspected. The use/adaptation judgments are this assistant's recommendations.
- This is a targeted broad search across app reviews, HCI/CSCW, privacy research and methodological literature, using existing project references, publisher/author searches and reference follow-up. No exhaustive database coverage or formal PRISMA adherence is claimed.
- Raw DOI-registration evidence, candidates, annotations and compilation scripts are retained under output/research/2026-10-14_methodology-literature/. The original thesis/proposals and shared bibliography were not changed.
""")
document = ''.join(parts)
(DEST/'Methods-Reading-List.md').write_text(document,encoding='utf-8')
(DEST/'ranked-dois.txt').write_text('\n'.join(r['doi'] for r in rows)+'\n',encoding='utf-8')
data = {'prepared_on':'2026-10-14','meeting_date':'2026-10-13','ranked_doi_records':rows,'official_or_no_doi_resources':[dict(zip(['id','priority','title','url','when','use'],e)) for e in extras]}
for r in data['official_or_no_doi_resources']:
    r['download'] = downloads.get(r['id'])
write_checklist(rows,data['official_or_no_doi_resources'],downloads)
(DEST/'methodology-literature.json').write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8')

# Search/filter view of the same local dataset; no server or remote scripts.
cards = []
for r in rows:
    text = f"{r['author_label']} ({r['year']})"
    tag = '' if r['version']=='published article/paper' else '<br><em>'+html.escape(r['version'])+'</em>'
    download_kind = "HTML" if (r["download"] or {}).get("status")=="available_html" else "PDF" if (r["download"] or {}).get("downloaded") else "missing"
    cards.append(f'<tr data-category="{html.escape(r["category"])}" data-priority="{r["priority"]}" data-download="{download_kind}"><td>{r["rank"]}</td><td>{r["priority"]}</td><td><strong>{html.escape(text)}</strong><br>{html.escape(r["title"])}<br><a target="_blank" rel="noopener" href="{r["doi_url"]}">{html.escape(r["doi"])}</a>{tag}</td><td>{html.escape(r["category"])}<br><strong>{html.escape(r["when"])}</strong></td><td>{html.escape(r["use"])}<details><summary>Adaptation limit</summary>{html.escape(r["caution"])}</details></td><td>{html_cell(r["download"])}</td></tr>')
options = ''.join('<option>'+html.escape(c)+'</option>' for c in categories)
page = """<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Thesis methodology literature</title><style>
body{font:15px/1.5 system-ui,sans-serif;margin:0;color:#18334b;background:#f4f7fb}main{max-width:1450px;margin:32px auto;padding:0 24px}h1{font-size:30px;line-height:1.2}a{color:#075d96}p{max-width:1000px}.controls{display:flex;flex-wrap:wrap;gap:12px;margin:24px 0;position:sticky;top:0;padding:12px;background:#f4f7fb;z-index:3}input,select{padding:10px;border:1px solid #91a3b6;border-radius:6px;font:inherit}input{min-width:250px;flex:1}table{border-collapse:collapse;width:100%;background:white}th,td{text-align:left;vertical-align:top;border-bottom:1px solid #d2dee8;padding:12px}th{background:#12384e;color:white}td:nth-child(3){width:30%}td:nth-child(4){width:17%}td:nth-child(5){width:43%}details{margin-top:10px;color:#63421f}summary{cursor:pointer;font-weight:600}.scroll{overflow-x:auto}.legend{background:#e1edf5;padding:16px;border-radius:8px}
</style><main><h1>Ranked methodology literature</h1><p>Privacy harm communication in health apps · Based on the meeting of 13 October 2026. <strong>83 verified DOI records</strong> plus 10 official/non-DOI resources in the companion reading guide.</p><p>A = essential; B = strong support; C = optional/adjacent. Ranking is an editorial assessment for this thesis. DOI verification is bibliographic verification, not a full-text appraisal of every work.</p><p class="legend"><strong>Stages:</strong> S scope · A app selection · D capture · W walkthrough · C codebook · I coder comparison · L LLM pilot · H harm tree · R reporting.<br><a href="Methods-Reading-List.md">Full reading guide, non-DOI sources and decision map</a> · <a href="ranked-dois.txt">DOIs for reference-manager import</a> · <a href="Download-Checklist.md">Download checklist: all 93 items and obstacles</a></p><div class="controls"><input id="search" type="search" aria-label="Search literature" placeholder="Search title, author, DOI or methodological use"><select id="category" aria-label="Category"><option value="">All categories</option>""" + options + """</select><select id="priority" aria-label="Priority"><option value="">All priorities</option><option>A</option><option>B</option><option>C</option></select><select id="availability" aria-label="Download status"><option value="">All download statuses</option><option value="PDF">PDF available</option><option value="HTML">HTML full text available</option><option value="missing">Missing / obstacle</option></select><span id="count" aria-live="polite"></span></div><div class="scroll"><table><thead><tr><th>Rank</th><th>Priority</th><th>Source / DOI</th><th>Category / stage</th><th>What to extract</th><th>Download / obstacle</th></tr></thead><tbody>""" + ''.join(cards) + """</tbody></table></div><script>const search=document.querySelector('#search'),category=document.querySelector('#category'),priority=document.querySelector('#priority'),availability=document.querySelector('#availability'),rows=[...document.querySelectorAll('tbody tr')];function filter(){const q=search.value.toLowerCase();let n=0;for(const r of rows){const ok=r.textContent.toLowerCase().includes(q)&&(!category.value||r.dataset.category===category.value)&&(!priority.value||r.dataset.priority===priority.value)&&(!availability.value||r.dataset.download===availability.value);r.hidden=!ok;if(ok)n++;}document.querySelector('#count').textContent=n+' / '+rows.length+' records';}for(const e of [search,category,priority,availability])e.addEventListener('input',filter);filter();</script></main></html>"""
(DEST/'Methods-Reading-List.html').write_text(page,encoding='utf-8')
checks = {'doi_records':83,'no_doi_resources':len(extras),'priorities':dict(Counter(r['priority'] for r in rows)),'unique_dois':True,'all_registrations_verified':True,'all_records_annotated':True,'bib_sha256':hashlib.sha256((ROOT/'_shared/references.bib').read_bytes()).hexdigest(),'outputs':['01_Literature/Methods-Reading-List.md','01_Literature/Methods-Reading-List.html','01_Literature/ranked-dois.txt','01_Literature/methodology-literature.json']}
(BASE/'verification.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
print(json.dumps(checks,indent=2))
