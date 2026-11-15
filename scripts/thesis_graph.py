"""Project integration: Graphify AST/semantics plus LaTeX/BibTeX structure.

Refresh is local and makes no API calls. Outdated semantic nodes are excluded,
not silently retained. `prepare` lists sources for the installed Graphify skill.
The methodology literature corpus (catalogue, download state, stage and RQ links)
is rebuilt deterministically from its JSON on every refresh.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

from graphify.analyze import god_nodes, surprising_connections, suggest_questions
from graphify.build import build_from_json
from graphify.cache import check_semantic_cache, save_semantic_cache
from graphify.cluster import cluster, score_all
from graphify.detect import detect
from graphify.diagnostics import diagnose_extraction
from graphify.export import to_json
from graphify.extract import extract
from graphify.report import generate

import literature_index

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'graphify-out'
SPEC = Path(sys.prefix) / 'Lib/site-packages/graphify/skills/codex/references/extraction-spec.md'


def read_json(path, default=None):
    return json.loads(path.read_text(encoding='utf-8-sig')) if path.exists() else default


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path):
    p = Path(path)
    return p.resolve().relative_to(ROOT).as_posix() if p.is_absolute() else p.as_posix()


def slug(value):
    return re.sub(r'[^a-z0-9]+', '_', value.lower()).strip('_')


def corpus():
    d = detect(ROOT)
    # Native Graphify supports Markdown, but not the thesis's LaTeX/BibTeX.
    tex = [p for folder in ('03_Thesis', '06_Presentation')
           for p in (ROOT / folder).rglob('*.tex')
           if 'proposal' not in p.parts and 'sync-conflict' not in p.name]
    tex.sort()
    d['files']['document'] += [str(p.resolve()) for p in tex]
    d['total_files'] += len(tex)
    d['total_words'] += sum(len(p.read_text(encoding='utf-8').split()) for p in tex)
    return d


def prepare():
    OUT.mkdir(exist_ok=True)
    (OUT / '.graphify_python').write_text(sys.executable, encoding='utf-8')
    (OUT / '.graphify_root').write_text(str(ROOT), encoding='utf-8')
    d = corpus()
    write_json(OUT / '.graphify_detect.json', d)
    files = [f for cat in ('document', 'paper', 'image') for f in d['files'].get(cat, [])
             if relative(f) not in CATALOGUE_DRIVEN]
    nodes, edges, hyperedges, uncached = check_semantic_cache(files, root=ROOT, prompt_file=SPEC)
    write_json(OUT / '.graphify_cached.json', {'nodes': nodes, 'edges': edges, 'hyperedges': hyperedges})
    (OUT / '.graphify_uncached.txt').write_text('\n'.join(uncached), encoding='utf-8')
    print(f"Corpus: {d['total_files']} files, ~{d['total_words']:,} words; {len(uncached)} semantic sources need extraction.")
    return d


def import_semantic():
    """Validate ALL extraction artifacts before writing either persistent cache."""
    chunks = sorted(OUT.glob('.graphify_chunk_[0-9][0-9].json'))
    if not chunks:
        raise ValueError('No semantic chunks. Run prepare and the Graphify extraction skill first.')
    nodes, edges, hyperedges, hashes = [], [], [], {}
    valid_types = {'code', 'document', 'paper', 'image', 'rationale', 'concept'}
    for path in chunks:
        d = read_json(path)
        if not isinstance(d, dict) or not isinstance(d.get('nodes'), list) or not isinstance(d.get('edges'), list):
            raise ValueError(f'Invalid chunk: {path}')
        fragment_hashes = read_json(path.with_name(path.stem + '_hashes.json'))
        if not isinstance(fragment_hashes, dict):
            raise ValueError(f'Missing source hashes: {path}')
        for source, value in fragment_hashes.items():
            if digest(Path(source)) != value:
                raise ValueError(f'Source changed during extraction: {source}')
            hashes[relative(source)] = value
        ids = {n['id'] for n in d['nodes']}
        for n in d['nodes']:
            if not re.fullmatch(r'[a-z0-9_]+', n['id']) or n.get('file_type') not in valid_types:
                raise ValueError(f'Invalid semantic node: {n}')
            if relative(n['source_file']) not in hashes:
                raise ValueError(f'Unhashed node source: {n["source_file"]}')
        for e in d['edges']:
            if e['source'] not in ids or e['target'] not in ids:
                raise ValueError(f'Dangling chunk edge: {e}')
            if e.get('confidence') not in {'EXTRACTED', 'INFERRED', 'AMBIGUOUS'} or 'confidence_score' not in e:
                raise ValueError(f'Missing edge confidence: {e}')
            if e['confidence'] == 'EXTRACTED' and e['confidence_score'] != 1.0:
                raise ValueError(f'Invalid explicit confidence: {e}')
        nodes += d['nodes']; edges += d['edges']; hyperedges += d.get('hyperedges', [])
    uncached = set((OUT / '.graphify_uncached.txt').read_text(encoding='utf-8').splitlines())
    if not {relative(p) for p in uncached} <= hashes.keys():
        raise ValueError('Some requested sources are missing from chunk hash manifests.')
    # Preserve exact absolute sources for the upstream cache; persisted project
    # fragments below use relative paths so a clone is portable.
    save_semantic_cache(nodes, edges, hyperedges, root=ROOT,
                        allowed_source_files=list(uncached), prompt_file=SPEC)
    for item in nodes + edges + hyperedges:
        if item.get('source_file'):
            item['source_file'] = relative(item['source_file'])
        item['_origin'] = 'semantic'
    previous = read_json(OUT / 'semantic.json', {'nodes': [], 'edges': [], 'hyperedges': [], 'source_hashes': {}})
    keep_sources = {source for source, value in previous.get('source_hashes', {}).items()
                    if source not in hashes and (ROOT / source).is_file()
                    and digest(ROOT / source) == value}
    old_nodes = [n for n in previous['nodes'] if n.get('source_file') in keep_sources]
    nodes = list({n['id']: n for n in old_nodes + nodes}.values())
    merged_ids = {n['id'] for n in nodes}
    edges = [e for e in previous['edges'] if e.get('source_file') in keep_sources
             and e['source'] in merged_ids and e['target'] in merged_ids] + edges
    hyperedges = [h for h in previous.get('hyperedges', []) if h.get('source_file') in keep_sources
                  and set(h.get('nodes', [])) <= merged_ids] + hyperedges
    hashes = {**{source: previous['source_hashes'][source] for source in keep_sources}, **hashes}
    data = {'nodes': nodes, 'edges': edges, 'hyperedges': hyperedges,
            'source_hashes': hashes, 'token_usage': None,
            'token_usage_note': 'Host-agent usage is unavailable; placeholder zeros are not measured costs.'}
    write_json(OUT / 'semantic.json', data)
    print(f'Imported {len(chunks)} semantic chunks: {len(nodes)} nodes, {len(edges)} edges.')


LITERATURE = ROOT / '01_Literature'
CATALOGUE = LITERATURE / 'catalog' / 'methods-corpus.json'
DOWNLOADS = ROOT / '01_Literature/catalog/download-status.json'
GUIDE = LITERATURE / 'catalog' / 'Methods-Reading-List.md'
# Generated from the catalogue and parsed by `literature()`; semantic extraction
# would only duplicate those nodes, so these are never queued or reused.
CATALOGUE_DRIVEN = {'01_Literature/catalog/Methods-Reading-List.md'}
LIT_STATS = {}
LIT_INDEX = {}   # filled by refresh(): abstracts and reading status per work


def abstract_text(item, limit=900):
    """Verbatim abstract excerpt for a node description, or a note that none was found."""
    if not item:
        return ''
    if item.get('abstract'):
        text = item['abstract']
        return ' Abstract (verbatim from the PDF): ' + (text[:limit] + '…' if len(text) > limit else text)
    return ''


def status_nodes(node, edge, root):
    """One concept node per reading status, so 'still to read' is a queryable neighbourhood."""
    ids = {}
    for status in literature_index.STATUSES:
        ids[status] = node('index_lit_status_' + slug(status), f'Reading status: {status}',
                           literature_index.STATUS, 1, file_type='concept',
                           description=f'Works marked "{status}" in 01_Literature/catalog/reading-status.csv.')
        edge(root, ids[status], 'contains', literature_index.STATUS)
    return ids


def family_names(work):
    """Lower-case slugs of a catalogued work's first three author surnames."""
    authors = work.get('authors') if isinstance(work.get('authors'), list) else []
    names = [slug(a.get('family') or a.get('familyName') or a.get('name', '')) for a in authors[:3]]
    return [n for n in names if n] or [slug(re.split(r'[ ,(&]', work.get('author_label') or work['title'])[0])]


def guide_rationale(node, edge, root, works, guide):
    """Meeting-decision map and method distinctions of the reading guide, as nodes.

    Hand-written rationale in the guide that the catalogue does not hold. Links
    to recommended papers are INFERRED from author names in the "Start with"
    cell; a name pair such as Hayes/Krippendorff must match one work.
    """
    section = None
    for number, line in enumerate(guide.splitlines(), 1):
        if line.startswith('#'):
            section = ('decision' if line.startswith('## Meeting decision') else
                       'distinction' if line.startswith('### Method distinctions') else None)
            continue
        if section == 'decision' and line.startswith('| ') and not line.startswith(('| Decision', '|---')):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if len(cells) < 3:
                continue
            decision = node('index_lit_decision_' + slug(cells[0])[:60], f'Meeting decision: {cells[0]}', GUIDE,
                            number, file_type='rationale', description=f'Start with: {cells[1]}. Record while reading: {cells[2]}')
            edge(root, decision, 'contains', GUIDE, number)
            for token in (t.strip() for t in cells[1].split(';')):
                ids = re.findall(r'\bN\d+\b', token)
                token = re.sub(r'\s+et al\.?|\s+\d{4}$', '', token)
                if ids:
                    targets = [w for w in works if str(w['id']) in ids]
                else:
                    parts = [slug(p) for p in re.split(r'/| and ', token) if re.match(r"[A-Z][\w'’-]+$", p.strip())]
                    targets = [w for w in works if not str(w['id']).startswith('N') and parts and
                               (all(p in family_names(w) for p in parts) if len(parts) > 1
                                else parts[0] == family_names(w)[0])]
                for target in targets:
                    edge(decision, 'index_lit_' + slug(str(target['id'])), 'recommended_reading', GUIDE, number,
                         confidence='INFERRED', score=0.75)
        elif section == 'distinction':
            match = re.match(r'(\d+)\. \*\*(.+?)\*\*:? ?(.*)', line)
            if match:
                item = node('index_lit_distinction_' + match[1], f'Method distinction: {match[2].rstrip(":")}', GUIDE,
                            number, file_type='rationale', description=match[3].strip())
                edge(root, item, 'contains', GUIDE, number)


def literature(node, edge, file_ids, bib_nodes, bib_dois):
    """Index the methodology literature corpus from its catalogue and download manifest.

    Deterministic and local: titles, ranks, stages and download state come
    straight from the maintained JSON, so they are never stale and need no
    model extraction. Paper full text is not indexed; local copies are an
    inventory only.
    """
    catalogue, manifest = read_json(CATALOGUE), read_json(DOWNLOADS)
    if not catalogue or not manifest:
        return
    records = {str(r['id']): r for r in manifest['records']}
    works = catalogue['ranked_doi_records'] + catalogue['official_or_no_doi_resources']
    guide = GUIDE.read_text(encoding='utf-8') if GUIDE.exists() else ''
    stage_names = {m[1]: m[2].strip() for m in re.finditer(r'^\| ([SADWCILHR]) \| (.+?) \|', guide, re.M)}
    rq_names = {m[1]: m[2].strip() for m in re.finditer(r'RQ(\d) = ([^;.]+)', guide)}
    root = node('index_lit_corpus', f'Methodology literature corpus ({len(works)} works)', CATALOGUE, 1,
                file_type='paper', description='Ranked methodology reading list with local reading copies and '
                'download gaps. Catalogue-driven; paper full text is not indexed.')
    for name in ('catalog/Methods-Reading-List.md', 'README.md'):
        owner = file_ids.get(f'01_Literature/{name}')
        if owner:
            edge(owner, root, 'indexes', LITERATURE / name)
    gaps = {
        'open_access_blocked': node('index_lit_gap_open_access_blocked',
            'Literature gap: free to read but blocked for scripts (save by hand)', DOWNLOADS, 1, file_type='concept',
            description='Open-access copy exists; the publisher or repository refuses automated downloads. '
                        'Save it from a browser into 01_Literature/library/, named Author_Year_ShortTitle.pdf.'),
        'paywalled': node('index_lit_gap_paywalled', 'Literature gap: paywalled, no open-access copy found',
            DOWNLOADS, 1, file_type='concept',
            description='No open-access copy located in Unpaywall, OpenAlex, Europe PMC or repository checks; '
                        'needs library access or an author copy.'),
        'web_only': node('index_lit_gap_web_only', 'Literature note: living web resource, no PDF',
            DOWNLOADS, 1, file_type='concept', description='Official web page; cite the dated page, not a PDF.')}
    for target in gaps.values():
        edge(root, target, 'contains', DOWNLOADS)
    by_bib, by_work = literature_index.lookup(LIT_INDEX) if LIT_INDEX else ({}, {})
    statuses = status_nodes(node, edge, root)
    for key, bib_id in bib_nodes.items():
        if key in by_bib:
            edge(bib_id, statuses[by_bib[key]['status']], 'reading_status', literature_index.STATUS)
    stats = {'pdf': 0, 'html': 0, 'open_access_blocked': 0, 'paywalled': 0, 'web_only': 0}
    categories, stages, rqs = {}, {}, {}
    for work in works:
        identifier = str(work['id'])
        record = records.get(identifier, {})
        category = work.get('category', 'Official and non-DOI resources')
        if category not in categories:
            categories[category] = node('index_lit_topic_' + slug(category), f'Methods literature topic: {category}',
                                        CATALOGUE, 1, file_type='concept',
                                        description=f'{category} works in the methodology reading list.')
            edge(root, categories[category], 'contains', CATALOGUE)
        if record.get('downloaded'):
            kind = 'HTML' if record.get('status') == 'available_html' else 'PDF'
            stats[kind.lower()] += 1
            state = f'local {kind}'
        elif record.get('status') == 'web_resource':
            stats['web_only'] += 1; state = 'web page only'
        elif record.get('status') == 'free_but_blocked':
            stats['open_access_blocked'] += 1; state = 'NO LOCAL COPY, open access but blocked'
        else:
            stats['paywalled'] += 1; state = 'NO LOCAL COPY, paywalled'
        who = f"{work['author_label']} ({work.get('year', '')}) — " if work.get('author_label') else ''
        rank = f"rank {work['rank']}/{work['priority']}" if work.get('rank') else f"{identifier}/{work['priority']}"
        label = f"{who}{work['title']} [{rank} · {category} · {state}]"
        doi = (work.get('doi') or '').lower()
        in_bib = bib_dois.get(doi)
        extra = {'doi': doi} if doi else {}
        item = by_work.get(identifier)
        if item:
            extra['reading_status'] = item['status']
            if item.get('keywords'):
                extra['keywords'] = item['keywords']
        work_id = node('index_lit_' + slug(identifier), label, CATALOGUE, 1, file_type='paper',
                       description=(f"When: {work.get('when', '')}. Use: {work.get('use', '')} "
                                    f"Limit: {work.get('caution', '')}".strip() + abstract_text(item)),
                       download_state=state, in_thesis_bibliography=bool(in_bib), **extra)
        edge(categories[category], work_id, 'contains', CATALOGUE)
        if item:
            edge(work_id, statuses[item['status']], 'reading_status', literature_index.STATUS)
        if in_bib:
            edge(work_id, bib_nodes[in_bib], 'same_work_as', CATALOGUE)
        head, _, tail = work.get('when', '').partition(';')
        for letter in sorted(set(re.findall(r'\b[SADWCILHR]\b', head))):
            if letter not in stages:
                stages[letter] = node('index_lit_stage_' + letter.lower(),
                                      f'Method stage {letter}: {stage_names.get(letter, letter)}', GUIDE, 1,
                                      file_type='concept', description='Stage letter used by the reading guide.')
                edge(root, stages[letter], 'contains', GUIDE)
            edge(work_id, stages[letter], 'supports_stage', CATALOGUE)
        for first, last in re.findall(r'RQ(\d)(?:\s*[–-]\s*(?:RQ)?(\d))?', tail):
            for number in range(int(first), int(last or first) + 1):
                key = str(number)
                if key not in rqs:
                    rqs[key] = node('index_lit_rq' + key, f'RQ{key}: {rq_names.get(key, "research question")}',
                                    GUIDE, 1, file_type='concept',
                                    description='Research-question label used by the reading guide.')
                    edge(root, rqs[key], 'contains', GUIDE)
                edge(work_id, rqs[key], 'informs_rq', CATALOGUE)
        if record.get('downloaded'):
            copy = ROOT / record['file']
            copy_id = node('index_lit_copy_' + slug(identifier), copy.name, copy, 1, file_type='paper',
                           description=f'Local reading copy ({kind}); inventory only, read the paper for evidence. '
                                       f"Version: {record.get('version') or 'not recorded'}.")
            edge(work_id, copy_id, 'has_local_copy', DOWNLOADS)
        elif record.get('status') == 'web_resource':
            edge(work_id, gaps['web_only'], 'lacks_local_copy', DOWNLOADS)
        elif record.get('status') == 'free_but_blocked':
            edge(work_id, gaps['open_access_blocked'], 'lacks_local_copy', DOWNLOADS)
        else:
            edge(work_id, gaps['paywalled'], 'lacks_local_copy', DOWNLOADS)
    guide_rationale(node, edge, root, works, guide)
    LIT_STATS.update(stats, works=len(works), checked_on=manifest.get('checked_on'),
                     catalogue_sha256=digest(CATALOGUE), manifest_sha256=digest(DOWNLOADS))


def structural(files):
    nodes, edges, ids = [], [], set()
    def node(identifier, label, file, line=None, **attrs):
        if identifier in ids:
            return identifier
        ids.add(identifier)
        nodes.append({'id': identifier, 'label': label, 'file_type': 'document',
                      'source_file': relative(file), 'source_location': f'L{line}' if line else None,
                      '_origin': 'semantic', 'extraction_method': 'local structure', **attrs})
        return identifier
    def edge(a, b, rel, file, line=None, confidence='EXTRACTED', score=1.0):
        if a == b:
            return
        edges.append({'source': a, 'target': b, 'relation': rel, 'source_file': relative(file),
                      'source_location': f'L{line}' if line else None, 'confidence': confidence,
                      'confidence_score': score, 'weight': 1.0, '_origin': 'semantic'})

    bib = ROOT / '03_Thesis/references.bib'
    body = bib.read_text(encoding='utf-8')
    entries = list(re.finditer(r'@\w+\s*\{\s*([^,]+),', body))
    citations, bib_dois = {}, {}
    for index, match in enumerate(entries):
        key = match[1].strip()
        entry = body[match.end():entries[index + 1].start() if index + 1 < len(entries) else len(body)]
        doi = re.search(r'\bdoi\s*=\s*[{"]\s*(?:https?://(?:dx\.)?doi\.org/)?([^}"\s,]+)', entry, re.I)
        if doi:
            bib_dois[doi[1].lower()] = key
        title = re.search(r'\btitle\s*=\s*\{(.*?)\}\s*,', entry, re.S | re.I)
        label = key + (': ' + re.sub(r'[{}\n]+', ' ', title[1]).strip() if title else '')
        item = literature_index.lookup(LIT_INDEX)[0].get(key) if LIT_INDEX else None
        status = {'reading_status': item['status']} if item else {}
        citations[key] = node('index_bib_' + slug(key), label, bib, body[:match.start()].count('\n') + 1,
                              file_type='paper', description='Bibliography entry; verify claims in the original paper.'
                              + abstract_text(item), **status)
    file_ids = {}
    for f in files:
        p = Path(f); rel = relative(p)
        file_ids[rel] = node('index_' + slug(rel) + '_file', rel, p, 1)
    bibliography_id = node('index_shared_bibliography_file', 'Shared bibliography', bib, 1)
    for citation_id in citations.values():
        edge(bibliography_id, citation_id, 'contains', bib)
    for f in files:
        p = Path(f); rel = relative(p); file_id = file_ids[rel]
        if p.suffix not in {'.tex', '.md', '.txt'}:
            continue
        content = p.read_text(encoding='utf-8', errors='replace')
        current = file_id
        for number, line in enumerate(content.splitlines(), 1):
            heading = (re.search(r'\\(?:chapter|section|subsection)\*?\{([^}]+)\}', line)
                       if p.suffix == '.tex' else re.match(r'#{1,6}\s+(.+)', line))
            if heading:
                label = heading[1].strip()
                current = node('index_' + slug(rel) + '_section_' + slug(label) + '_' + str(number),
                               label, p, number, description=f'{label} in {rel}')
                edge(file_id, current, 'contains', p, number)
            for citation in re.finditer(r'\\(?:[a-zA-Z]*cite)[^\{\n]*\{([^}]+)\}', line):
                for key in citation[1].split(','):
                    if key.strip() in citations:
                        edge(current, citations[key.strip()], 'cites', p, number)
            for include in re.finditer(r'\\(?:input|include)\{([^}]+)\}', line):
                target = p.parent / include[1]
                if not target.suffix:
                    target = target.with_suffix('.tex')
                target_rel = relative(target)
                if target_rel in file_ids:
                    edge(file_id, file_ids[target_rel], 'inputs', p, number)
    # PDF inventory only: no text content or paper conclusions claimed here.
    for p in sorted((ROOT / '01_Literature/library').glob('*.pdf')):
        pdf_id = node('index_pdf_' + slug(p.stem), p.stem, p, file_type='paper',
                      description='Original PDF file, inventory only; read the paper for evidence.')
        name = slug(p.stem)
        for key, target in citations.items():
            author = re.match(r'[a-z]+', key.lower())
            year = re.search(r'\d{4}', key)
            if author and year and name.startswith(author[0]) and year[0] in name:
                edge(target, pdf_id, 'likely_original_pdf', bib, confidence='INFERRED', score=0.85)
    literature(node, edge, file_ids, citations, bib_dois)
    return nodes, edges


def refresh():
    OUT.mkdir(exist_ok=True)
    LIT_INDEX.clear()
    LIT_INDEX.update(literature_index.update())
    d = corpus()
    files = [f for group in d['files'].values() for f in group]
    ast = extract([Path(f) for f in d['files']['code']], cache_root=ROOT, root=ROOT, parallel=False)
    semantic = read_json(OUT / 'semantic.json', {'nodes': [], 'edges': [], 'hyperedges': [], 'source_hashes': {}})
    active = {relative(f) for f in files} - CATALOGUE_DRIVEN
    valid = {f for f, value in semantic.get('source_hashes', {}).items()
             if f in active and (ROOT / f).is_file() and digest(ROOT / f) == value}
    sem_nodes = [deepcopy(n) for n in semantic['nodes'] if n['source_file'] in valid]
    sem_ids = {n['id'] for n in sem_nodes}
    sem_edges = [deepcopy(e) for e in semantic['edges']
                 if e['source'] in sem_ids and e['target'] in sem_ids and e.get('source_file') in valid]
    sem_hyperedges = [deepcopy(h) for h in semantic.get('hyperedges', [])
                     if h.get('source_file') in valid and set(h.get('nodes', [])) <= sem_ids]
    local_nodes, local_edges = structural(files)
    nodes = {n['id']: n for n in ast['nodes'] + sem_nodes + local_nodes}
    for n in sem_nodes:
        owner = 'index_' + slug(n['source_file']) + '_file'
        if owner in nodes and owner != n['id']:
            local_edges.append({'source': owner, 'target': n['id'], 'relation': 'documents',
                                'source_file': n['source_file'], 'source_location': n.get('source_location'),
                                'confidence': 'EXTRACTED', 'confidence_score': 1.0, 'weight': 1.0,
                                '_origin': 'semantic'})
    # Repeated citations can be on multiple source lines. Retain all locations
    # on a single exact-relation edge, avoiding redundant edge collapse.
    unique_edges = {}
    for e in ast['edges'] + sem_edges + local_edges:
        if e['source'] not in nodes or e['target'] not in nodes or e['source'] == e['target']:
            continue
        key = (e['source'], e['target'], e.get('relation'), e.get('confidence'))
        if key in unique_edges:
            prior = unique_edges[key]
            prior.setdefault('evidence_locations', [prior.get('source_location')])
            if e.get('source_location') not in prior['evidence_locations']:
                prior['evidence_locations'].append(e.get('source_location'))
        else:
            unique_edges[key] = e
    extraction = {'nodes': list(nodes.values()), 'edges': list(unique_edges.values()), 'hyperedges': sem_hyperedges}
    diagnostic = diagnose_extraction(extraction, directed=False, root=ROOT)
    write_json(OUT / 'health.json', diagnostic)
    dangling = diagnostic.get('dangling_endpoint_edges', 0)
    missing = diagnostic.get('missing_endpoint_edges', 0)
    if dangling or missing:
        raise ValueError(f'Graph integrity failed: {dangling} dangling and {missing} missing endpoints.')
    print('Graph integrity: no missing or dangling endpoints; details in graphify-out/health.json.')
    graph = build_from_json(extraction, root=ROOT, directed=False)
    if not graph.number_of_nodes():
        raise ValueError('Empty extraction; existing graph not overwritten.')
    communities = cluster(graph)
    cohesion = score_all(graph, communities)
    labels = {}
    names = {'00_Notes': 'Supervisor Decisions', '01_Literature': 'Literature and Evidence',
             '03_Thesis': 'Thesis Writing and Methods', '04_Study': 'Study Instruments',
             '06_Presentation': 'Presentation', 'output': 'Sampling Research',
             'scripts': 'Graphify Integration'}
    for cid, members in communities.items():
        family = Counter(str(graph.nodes[n].get('source_file', '')).split('/')[0] for n in members).most_common(1)[0][0]
        labels[cid] = names.get(family, 'Project Navigation') + f' {cid}'
    gods = god_nodes(graph)
    surprises = surprising_connections(graph, communities)
    questions = suggest_questions(graph, communities, labels)
    if not to_json(graph, communities, str(OUT / 'graph.json'), force=True, community_labels=labels,
                   original_links=extraction['edges']):
        raise ValueError('Graph export failed.')
    report = generate(graph, communities, cohesion, labels, gods, surprises, d,
                      {'input': 0, 'output': 0}, str(ROOT), suggested_questions=questions)
    report = report.replace('- Token cost: 0 input · 0 output',
                            '- Token cost: host semantic extraction unmeasured; local refresh makes no model calls')
    stale = sorted(relative(f) for f in d['files']['document']
                   if relative(f) not in valid and relative(f) not in CATALOGUE_DRIVEN)
    scope = ('\n## Project extraction scope and cost\n\n'
             'AST and structure refreshes are local and make no model calls. Semantic extraction used host agents; '
             'their token usage is unavailable, so displayed upstream zero counters are placeholders, not measured costs. '
             'No actual session token saving has been measured.\n\n'
             'LaTeX sections, inputs, citations and bibliography entries are indexed by the project adapter. '
             'PDF nodes describe file inventory only; full paper text, archives and raw/processed data are excluded.\n\n'
             + (f"Methodology literature corpus: {LIT_STATS['works']} catalogued works from the ranked catalogue and download "
                f"manifest (checked {LIT_STATS['checked_on']}): {LIT_STATS['pdf']} local PDFs, {LIT_STATS['html']} local HTML "
                f"full-text copies, {LIT_STATS['open_access_blocked']} open access but blocked for scripts, "
                f"{LIT_STATS['paywalled']} paywalled, {LIT_STATS['web_only']} web-only. Rebuilt from the JSON on every "
                'refresh, so it is never semantically stale; availability is not reading status.\n\n' if LIT_STATS else '')
             + f'Fresh semantic sources: {len(valid)}. Sources needing semantic extraction: {len(stale)}. '
             'Local structure remains available for changed files.\n')
    collapsed = diagnostic.get('undirected_same_endpoint_collapsed_edges', 0)
    if collapsed:
        scope += (f'\nGraph health warning: {collapsed} parallel relation variants are simplified by '
                  'Graphify\'s simple graph during clustering/traversal. All original relation links '
                  'and their source evidence are preserved in graph.json via original_links; '
                  'consult health.json for details. No dangling or missing endpoints are permitted.\n')
        print(f'Graphify traversal simplifies {collapsed} parallel relations; graph.json preserves the full links.')
    if stale:
        scope += '\n' + '\n'.join('- `' + p + '`' for p in stale) + '\n'
    (OUT / 'GRAPH_REPORT.md').write_text(report + scope, encoding='utf-8')
    write_json(OUT / '.graphify_labels.json', {str(k): v for k, v in labels.items()})
    write_json(OUT / 'freshness.json', {'built_at_utc': datetime.now(timezone.utc).isoformat(),
               'fresh_semantic_files': sorted(valid), 'needs_semantic_extraction': stale,
               'source_hashes': {relative(f): digest(Path(f)) for f in files},
               'literature_corpus': LIT_STATS or None,
               'nodes': graph.number_of_nodes(), 'edges': graph.number_of_edges(),
               'communities': len(communities), 'semantic_token_usage': None,
               'actual_token_savings_measured': False})
    write_json(OUT / 'cost.json', {'local_refresh_api_tokens': 0, 'host_semantic_tokens': None,
                                  'note': 'Host-agent token counts unavailable; no savings claim.'})
    write_json(OUT / '.graphify_build.json', {'gitignore': True, 'excludes': []})
    (OUT / '.graphify_python').write_text(sys.executable, encoding='utf-8')
    (OUT / '.graphify_root').write_text(str(ROOT), encoding='utf-8')
    subprocess.run([sys.executable, '-m', 'graphify', 'export', 'html'], cwd=ROOT, check=True)
    literature_index.build_map(OUT / 'graph.json')
    print(f'Graph: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges, {len(communities)} communities.')
    print(f'{len(stale)} files need semantic extraction; see graphify-out/freshness.json.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['prepare', 'import-semantic', 'refresh'])
    args = parser.parse_args()
    {'prepare': prepare, 'import-semantic': import_semantic, 'refresh': refresh}[args.command]()
