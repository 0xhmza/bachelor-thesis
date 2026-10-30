"""Deduplication and provenance of the literature review v003 (D14).

    python scripts/literature-search/v003/merge.py

Reads the hits of search.py (output/hits-*.jsonl), the IEEE Xplore results (output/ieee-raw.json), the thesis
citations (_shared/references.bib, keys cited in 03_Thesis), the Methods Digest registry and the citation-searching
hits (output/hits-citations.jsonl, if present). Hits are merged when they share a DOI, an arXiv ID or a normalised
title with publication years at most one apart (the earliest year is kept). Each record lists every route that
found it. Writes output/records.csv and output/merge.json (counts per source before and after deduplication).
Standard library only.
"""
import csv, json, re
from pathlib import Path

import lit

ROOT = lit.HERE.parents[2]
OUT = lit.HERE / 'output'
DIGEST = ROOT / 'literature_new' / 'literature methodology analysis' / 'tex' / 'registry.json'
BIB = ROOT / '_shared' / 'references.bib'
SOURCES = ['PubMed', 'IEEE Xplore', 'arXiv', 'ACL Anthology', 'PoPETs', 'USENIX Security', 'SOUPS', 'CCS', 'IEEE S&P',
           'NDSS', 'CHI', 'CSCW', 'Citation searching', 'Thesis citation', 'Methods Digest']
ROUTE = {'PubMed': 'database', 'IEEE Xplore': 'database', 'arXiv': 'database', 'ACL Anthology': 'database',
         'Citation searching': 'citation', 'Thesis citation': 'thesis', 'Methods Digest': 'digest'}


def read_jsonl(path):
    return [json.loads(line) for line in open(path, encoding='utf-8')] if path.exists() else []


def search_hits():
    hits = []
    for name in ('pubmed', 'arxiv', 'acl', 'venues', 'citations'):
        hits += read_jsonl(OUT / f'hits-{name}.jsonl')
    ieee = OUT / 'ieee-raw.json'
    if ieee.exists():
        for r in json.loads(ieee.read_text(encoding='utf-8'))['records']:
            for s in r['strands']:
                hits.append({'source': 'IEEE Xplore', 'route': 'database', 'strand': s, 'ieee': r['id'],
                             'doi': lit.norm_doi(r['doi']), 'title': r['title'], 'abstract': r['abstract'],
                             'year': int(r['year']) if str(r['year']).isdigit() else None, 'venue': r['venue'],
                             'type': r['type'], 'authors': [r['first'].split()[-1]] if r['first'] else [],
                             'url': f"https://ieeexplore.ieee.org/document/{r['id']}"})
    return hits


def bib_entries():
    text = BIB.read_text(encoding='utf-8')
    for m in re.finditer(r'@(\w+)\s*\{\s*([^,\s]+)\s*,(.*?)\n\}', text, flags=re.S):
        body = m.group(3)
        def field(name):
            f = re.search(r'\b' + name + r'\s*=\s*[{"](.*?)[}"]\s*,?\s*\n', body, flags=re.S | re.I)
            return ' '.join(re.sub(r'[{}\\]', '', f.group(1)).split()) if f else ''
        year = re.search(r'\d{4}', field('year') or field('date'))
        yield {'key': m.group(2), 'type': m.group(1).lower(), 'title': field('title'), 'doi': lit.norm_doi(field('doi')),
               'year': int(year.group()) if year else None,
               'venue': field('journaltitle') or field('journal') or field('booktitle') or field('publisher') or field('organization'),
               'authors': [a.split(',')[0].strip() for a in field('author').split(' and ') if a], 'url': field('url'),
               'eprint': field('eprint')}


def cited_keys():
    keys = set()
    for f in list((ROOT / '03_Thesis' / 'chapters').glob('*.tex')) + list((ROOT / '03_Thesis' / 'appendix').glob('*.tex')):
        for line in f.read_text(encoding='utf-8').splitlines():
            line = re.sub(r'(?<!\\)%.*', '', line)
            for m in re.finditer(r'\\[A-Za-z]*cite[a-z]*\*?(?:\[[^\]]*\])*\{([^}]+)\}', line):
                keys.update(k.strip() for k in m.group(1).split(','))
    return keys


def provenance_hits():
    hits = []
    # The route "thesis citation" is the literature cited before this review; works cited since (found by the review
    # itself, or reporting guidelines) keep their own routes and are only linked to their key in main().
    keys = set(lit.load_config()['thesis_citations_before_d14']['keys'])
    for e in bib_entries():
        if e['key'] in keys:
            hits.append({'source': 'Thesis citation', 'route': 'thesis', 'strand': '', 'bibkey': e['key'],
                         'doi': e['doi'], 'arxiv': lit.arxiv_id(e['eprint']), 'title': e['title'], 'abstract': '',
                         'year': e['year'], 'venue': e['venue'], 'type': e['type'], 'authors': e['authors'], 'url': e['url']})
    for d in json.loads(DIGEST.read_text(encoding='utf-8')):
        hits.append({'source': 'Methods Digest', 'route': 'digest', 'strand': '', 'digest': d['num'],
                     'doi': lit.norm_doi(d.get('doi')), 'arxiv': lit.arxiv_id(d.get('venue') or ''),
                     'title': d['title'], 'abstract': '', 'year': d.get('year'), 'venue': d.get('venue') or '',
                     'type': d.get('category') or '', 'authors': [d['authors'].split(',')[0].split()[-1]] if d.get('authors') else [],
                     'url': d.get('url') or ''})
    return hits, keys


def keys_of(hit):
    doi = lit.norm_doi(hit.get('doi'))
    aid = hit.get('arxiv') or (lit.arxiv_id(doi) if doi.startswith('10.48550') else '')
    out = []
    if doi and not doi.startswith('10.48550'):
        out.append('doi:' + doi)
    if aid:
        out.append('arxiv:' + aid)
    return out


def merge(hits):
    parent = list(range(len(hits)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i, j):
        parent[find(i)] = find(j)

    seen = {}
    for i, h in enumerate(hits):
        for k in keys_of(h):
            if k in seen:
                union(i, seen[k])
            seen[k] = i
    by_title = {}
    for i, h in enumerate(hits):
        t = lit.norm_title(h['title'])
        if len(t) < 12:
            continue
        for j in by_title.get(t, []):
            gap = 3 if 'arXiv' in (h['source'], hits[j]['source']) else 1  # a preprint may precede its paper by years
            if h.get('year') is None or hits[j].get('year') is None or abs(h['year'] - hits[j]['year']) <= gap:
                union(i, j)
        by_title.setdefault(t, []).append(i)
    for a, b in lit.load_config().get('manual_duplicates', {}).get('titles', []):  # checked by hand
        same = [i for i, h in enumerate(hits) if lit.norm_title(h['title']) in (lit.norm_title(a), lit.norm_title(b))]
        for i in same[1:]:
            union(i, same[0])
    groups = {}
    for i in range(len(hits)):
        groups.setdefault(find(i), []).append(hits[i])
    return list(groups.values())


def identifiers(group):
    """Every identifier of the merged hits; decisions are keyed by one of them, so they survive a new merge."""
    ids = []
    for h in group:
        for prefix, value in (('doi', lit.norm_doi(h.get('doi'))), ('pmid', h.get('pmid')), ('ieee', h.get('ieee')),
                              ('arxiv', h.get('arxiv')), ('acl', h.get('acl')), ('bib', h.get('bibkey')),
                              ('digest', h.get('digest'))):
            if value:
                ids.append(f'{prefix}:{value}')
        if h['route'] == 'venue' and not h.get('doi'):
            ids.append('url:' + h['url'])
    ids.append('title:' + lit.norm_title(group[0]['title']).replace(' ', '-')[:80])
    return sorted(set(ids), key=lambda x: (['doi', 'pmid', 'ieee', 'arxiv', 'acl', 'url', 'bib', 'digest', 'title'].index(x.split(':')[0]), x))


def record(group):
    def pref(h):  # a database or venue hit with an abstract first, then the longest abstract
        return (h['route'] in ('database', 'venue'), len(h.get('abstract') or ''))
    best = max(group, key=pref)
    years = [h['year'] for h in group if h.get('year')]
    dois = sorted({lit.norm_doi(h.get('doi')) for h in group if h.get('doi')})
    sources = sorted({h['source'] for h in group}, key=SOURCES.index)
    routes = sorted({h['route'] for h in group})
    return {'title': best['title'], 'year': min(years) if years else '',
            'first_author': next((h['authors'][0] for h in group if h.get('authors')), ''),
            'venue': next((h['venue'] for h in sorted(group, key=lambda h: (h['route'] != 'venue', (h.get('venue') or '').lower() in ('arxiv', '')))
                           if h.get('venue')), ''),  # a venue hit first, a preprint server last
            'type': ';'.join(sorted({h.get('type') or '' for h in group} - {''})),
            'doi': next((d for d in dois if not d.startswith('10.48550')), dois[0] if dois else ''),
            'arxiv': next((h.get('arxiv') for h in group if h.get('arxiv')), ''),
            'pmid': next((h.get('pmid') for h in group if h.get('pmid')), ''),
            'ieee': next((h.get('ieee') for h in group if h.get('ieee')), ''),
            'bibkey': next((h.get('bibkey') for h in group if h.get('bibkey')), ''),
            'digest': next((str(h.get('digest')) for h in group if h.get('digest')), ''),
            'sources': ';'.join(sources), 'routes': ';'.join(routes),
            'strands': ';'.join(sorted({h['strand'] for h in group if h.get('strand')})), 'hits': len(group),
            'url': best.get('url') or (('https://doi.org/' + dois[0]) if dois else ''),
            'ids': ' '.join(identifiers(group)),
            'abstract': max((h.get('abstract') or '' for h in group), key=len)}


def main():
    hits = search_hits()
    prov, keys = provenance_hits()
    groups = merge(hits + prov)
    records = sorted((record(g) for g in groups), key=lambda r: (str(r['year']), lit.norm_title(r['title'])))
    extra = OUT / 'abstracts-openalex.json'  # enrich.py: abstracts for screening only, by DOI
    extra = json.loads(extra.read_text(encoding='utf-8')) if extra.exists() else {}
    for r in records:
        r['abstract_source'] = 'source' if len(r['abstract']) >= 80 else ''
        if not r['abstract_source'] and extra.get(r['doi']):
            r['abstract'], r['abstract_source'] = extra[r['doi']], 'OpenAlex (by DOI)'
    cited_now = cited_keys()  # link records to keys cited in the thesis now (for the inventory and the contextual flag)
    by_doi = {e['doi']: e['key'] for e in bib_entries() if e['key'] in cited_now and e['doi']}
    by_title = {lit.norm_title(e['title']): e['key'] for e in bib_entries() if e['key'] in cited_now}
    for r in records:
        r['bibkey'] = r['bibkey'] or by_doi.get(r['doi']) or by_title.get(lit.norm_title(r['title']), '')
    for i, r in enumerate(records, 1):
        r['id'] = f'R{i:04d}'
    fields = ['id', 'title', 'year', 'first_author', 'venue', 'type', 'doi', 'arxiv', 'pmid', 'ieee', 'bibkey', 'digest',
              'sources', 'routes', 'strands', 'hits', 'url', 'ids', 'abstract_source', 'abstract']
    with open(OUT / 'records.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(records)
    per_source = {}
    for s in SOURCES:
        src_hits = [h for h in hits + prov if h['source'] == s]
        per_source[s] = {'hits': len(src_hits), 'records': len(merge(src_hits)) if src_hits else 0,
                         'in_merged': sum(1 for r in records if s in r['sources'].split(';')),
                         'only_here': sum(1 for r in records if r['sources'] == s)}
    search = [r for r in records if set(r['routes'].split(';')) & {'database', 'venue'}]
    summary = {'hits': len(hits), 'provenance_hits': len(prov), 'records': len(records),
               'records_from_searches': len(search), 'cited_keys': len(keys), 'per_source': per_source}
    (OUT / 'merge.json').write_text(json.dumps(summary, indent=1), encoding='utf-8')
    print(json.dumps(summary, indent=1))


if __name__ == '__main__':
    main()
