"""Stage 0 of the literature review (D13): database search, deduplication and citation filter.

    python scripts/literature-search/v001/search.py scripts/literature-search/v001/config.json [--reuse-hits]
    python -I -m unittest discover -s scripts/literature-search/v001/tests

The procedure follows Baumann et al. (2025, Appendix A): Boolean queries in titles and abstracts,
duplicates removed, then works with fewer than `min_citations_per_year` citations per year
removed. Citations per year = highest citation count of the merged record / max(1, search year -
publication year), with no exemption for recent works, as in the source procedure. Databases: OpenAlex and Semantic Scholar (both open; Scopus, Web of Science
and Google Scholar need institutional access or block automated queries).

Writes to output/: hits.jsonl (every hit, per database and query), records.csv (merged records with
the filter result), manual-hits.jsonl (works added by hand from manual.json) and run.json (counts). --reuse-hits rebuilds records.csv and run.json from the saved
hits.jsonl without querying the databases again. Standard library only.
"""
import csv, json, re, sys, time, unicodedata, urllib.error, urllib.parse, urllib.request
from pathlib import Path

OPENALEX = 'https://api.openalex.org/works'
S2_BULK = 'https://api.semanticscholar.org/graph/v1/paper/search/bulk'
S2_PAPER = 'https://api.semanticscholar.org/graph/v1/paper'
S2_FIELDS = 'title,year,publicationDate,externalIds,citationCount,venue,abstract,url,authors,publicationTypes'
OA_SELECT = ('id,doi,display_name,publication_year,publication_date,cited_by_count,type,language,'
             'primary_location,abstract_inverted_index,authorships,ids')


def expand(query, domain):
    return query.replace('{domain}', domain)


def to_s2(query):
    """Semantic Scholar bulk syntax: + for AND, | for OR; phrases and parentheses are kept."""
    return query.replace(' AND ', ' + ').replace(' OR ', ' | ')


def norm_doi(doi):
    if not doi:
        return ''
    doi = doi.strip().lower()
    return re.sub(r'^(https?://(dx\.)?doi\.org/|doi:)', '', doi)


def norm_title(title):
    title = unicodedata.normalize('NFKD', title or '').encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', ' ', title).strip()


def abstract_from_index(index):
    if not index:
        return ''
    words = sorted((pos, word) for word, positions in index.items() for pos in positions)
    return ' '.join(word for _, word in words)


def citations_per_year(citations, year, search_year):
    if year is None:
        return 0.0
    return (citations or 0) / max(1, search_year - year)


def passes_citation_filter(citations, year, search_year, threshold):
    return citations_per_year(citations, year, search_year) >= threshold


def get_json(url, tries=8):
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'thesis-literature-search/1'}),
                                        timeout=90) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            if error.code in (429, 500, 502, 503, 504) and attempt < tries - 1:
                time.sleep(3 * (attempt + 1))
                continue
            raise
        except (urllib.error.URLError, TimeoutError):
            if attempt < tries - 1:
                time.sleep(3 * (attempt + 1))
                continue
            raise


def openalex_hit(work, source_name='OpenAlex'):
    source = (work.get('primary_location') or {}).get('source') or {}
    authors = [a['author']['display_name'] for a in work.get('authorships') or [] if a.get('author')]
    landing = (work.get('primary_location') or {}).get('landing_page_url') or ''
    match = re.search(r'arxiv\.org/abs/([^v\s]+)', landing)
    return {'source': source_name, 'source_id': work['id'], 'doi': norm_doi(work.get('doi')),
            'arxiv': match.group(1) if match else '', 'title': work.get('display_name') or '',
            'year': work.get('publication_year'), 'date': work.get('publication_date') or '',
            'venue': source.get('display_name') or '', 'type': work.get('type') or '',
            'language': work.get('language') or '', 'citations': work.get('cited_by_count') or 0, 'authors': authors,
            'url': work.get('doi') or landing or work['id'],
            'abstract': abstract_from_index(work.get('abstract_inverted_index'))}


def openalex_hits(query, start, until, mailto):
    page, hits = 1, []
    while page:  # page numbers, not cursors: cursor paging needs an API key (results capped at 10,000)
        params = {'filter': f'title_and_abstract.search:{query},from_publication_date:{start},to_publication_date:{until}',
                  'per-page': 200, 'page': page, 'select': OA_SELECT, 'mailto': mailto}
        data = get_json(OPENALEX + '?' + urllib.parse.urlencode(params))
        hits.extend(openalex_hit(work) for work in data['results'])
        page = page + 1 if len(data['results']) == 200 else None
        time.sleep(1.2)  # OpenAlex allows one request per second for queries with many operators
    return hits


def manual_hits(works, mailto):
    """Works added by hand, looked up in OpenAlex by DOI, or in Semantic Scholar by paper ID when OpenAlex lacks them."""
    hits = []
    for entry in works:
        if entry.get('doi'):
            work = get_json(f"{OPENALEX}/doi:{entry['doi']}?" + urllib.parse.urlencode({'select': OA_SELECT, 'mailto': mailto}))
            hit = openalex_hit(work, 'Manual')
        else:
            paper = get_json(f"{S2_PAPER}/{entry['s2']}?" + urllib.parse.urlencode({'fields': S2_FIELDS}))
            hit = s2_hit(paper, 'Manual')
        hit['query'] = 'M'
        hits.append(hit)
        time.sleep(1.5)
    return hits


def s2_hit(paper, source_name='Semantic Scholar'):
    ids = paper.get('externalIds') or {}
    doi = norm_doi(ids.get('DOI'))
    return {'source': source_name, 'source_id': paper['paperId'], 'doi': doi,
            'arxiv': ids.get('ArXiv') or '', 'title': paper.get('title') or '', 'year': paper.get('year'),
            'date': paper.get('publicationDate') or '', 'venue': paper.get('venue') or '',
            'type': ';'.join(paper.get('publicationTypes') or []), 'language': '',
            'citations': paper.get('citationCount') or 0,
            'authors': [a.get('name') for a in paper.get('authors') or [] if a.get('name')],
            'url': f'https://doi.org/{doi}' if doi else (paper.get('url') or ''),
            'abstract': paper.get('abstract') or ''}


def s2_hits(query, start, until):
    token, hits = None, []
    while True:
        params = {'query': to_s2(query), 'fields': S2_FIELDS, 'publicationDateOrYear': f'{start}:{until}'}
        if token:
            params['token'] = token
        data = get_json(S2_BULK + '?' + urllib.parse.urlencode(params))
        hits.extend(s2_hit(paper) for paper in data.get('data') or [])
        token = data.get('token')
        time.sleep(1.5)
        if not token:
            return hits


def merge(hits):
    """Group hits that share a DOI, an arXiv ID or a normalised title (with a year at most one apart)."""
    parent = list(range(len(hits)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i, j):
        parent[find(i)] = find(j)

    seen = {}
    for i, hit in enumerate(hits):
        keys = []
        if hit['doi']:
            keys.append(('doi', hit['doi']))
        if hit['arxiv']:
            keys.append(('arxiv', hit['arxiv'].lower()))
        title = norm_title(hit['title'])
        if len(title) >= 25:
            keys.append(('title', title))
        for key in keys:
            if key in seen:
                j = seen[key]
                if key[0] != 'title' or abs((hits[j]['year'] or 0) - (hit['year'] or 0)) <= 1:
                    union(i, j)
            else:
                seen[key] = i
    groups = {}
    for i in range(len(hits)):
        groups.setdefault(find(i), []).append(hits[i])
    return list(groups.values())


def record(group, search_year, threshold):
    def preference(hit):  # a published DOI over an arXiv DOI, then OpenAlex, then the longer abstract
        return (bool(hit['doi']) and 'arxiv' not in hit['doi'], hit['source'] == 'OpenAlex', len(hit['abstract']))
    best = max(group, key=preference)
    citations = max(h['citations'] for h in group)
    years = [h['year'] for h in group if h['year']]
    year = best['year'] or (min(years) if years else None)
    dois = sorted({h['doi'] for h in group if h['doi']})
    authors = best['authors'] or next((h['authors'] for h in group if h['authors']), [])
    return {'title': best['title'], 'first_author': authors[0] if authors else '', 'authors': len(authors),
            'year': year, 'venue': best['venue'] or next((h['venue'] for h in group if h['venue']), ''),
            'type': best['type'], 'language': next((h['language'] for h in group if h['language']), ''),
            'doi': best['doi'] or (dois[0] if dois else ''), 'other_dois': ';'.join(d for d in dois if d != best['doi']),
            'arxiv': next((h['arxiv'] for h in group if h['arxiv']), ''), 'url': best['url'],
            'citations': citations, 'citations_per_year': round(citations_per_year(citations, year, search_year), 2),
            'passes_citation_filter': passes_citation_filter(citations, year, search_year, threshold),
            'queries': ';'.join(sorted({h['query'] for h in group})),
            'sources': ';'.join(sorted({h['source'] for h in group})), 'hits': len(group),
            'abstract': max((h['abstract'] for h in group), key=len)}


def main(config_path, reuse_hits=False):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    out = Path(config_path).parent / 'output'
    out.mkdir(exist_ok=True)
    until = config['searched_until']
    search_year = int(until[:4])
    hits, counts, searched_on = [], {}, time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())
    if reuse_hits:
        hits = [json.loads(line) for line in open(out / 'hits.jsonl', encoding='utf-8')]
        previous = json.loads((out / 'run.json').read_text(encoding='utf-8'))
        counts, searched_on = previous['hits_per_query_and_database'], previous['searched_on']
    for q in ([] if reuse_hits else config['queries']):
        query = expand(q['query'], config['domain'])
        for name, fetch in (('OpenAlex', lambda: openalex_hits(query, q['from'], until, config['mailto'])),
                            ('Semantic Scholar', lambda: s2_hits(query, q['from'], until))):
            found = fetch()
            for hit in found:
                hit['query'] = q['id']
            counts[f"{q['id']} {name}"] = len(found)
            print(q['id'], name, len(found), flush=True)
            hits.extend(found)
    if not reuse_hits:
        with open(out / 'hits.jsonl', 'w', encoding='utf-8') as f:
            for hit in hits:
                f.write(json.dumps(hit, ensure_ascii=False) + '\n')
    manual_file = out / 'manual-hits.jsonl'
    if manual_file.exists() and reuse_hits:
        manual = [json.loads(line) for line in open(manual_file, encoding='utf-8')]
    else:
        manual = manual_hits(json.loads((Path(config_path).parent / 'manual.json').read_text(encoding='utf-8'))['works'],
                             config['mailto'])
        with open(manual_file, 'w', encoding='utf-8') as f:
            for hit in manual:
                f.write(json.dumps(hit, ensure_ascii=False) + '\n')
    counts['Manually added'] = len(manual)
    hits = hits + manual
    records = [record(g, search_year, config['min_citations_per_year'])
               for g in merge(hits)]
    records.sort(key=lambda r: (not r['passes_citation_filter'], -(r['citations_per_year'] or 0), r['title']))
    for n, r in enumerate(records, 1):
        r['rid'] = f'R{n:04d}'
    fields = ['rid', 'title', 'first_author', 'authors', 'year', 'venue', 'type', 'language', 'doi', 'other_dois',
              'arxiv', 'url', 'citations', 'citations_per_year', 'passes_citation_filter', 'queries', 'sources',
              'hits', 'abstract']
    with open(out / 'records.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fields)
        writer.writeheader()
        writer.writerows(records)
    kept = sum(r['passes_citation_filter'] for r in records)
    summary = {'searched_on': searched_on, 'searched_until': until,
               'hits_per_query_and_database': counts, 'hits': len(hits), 'records_after_deduplication': len(records),
               'duplicates_removed': len(hits) - len(records), 'removed_by_citation_filter': len(records) - kept,
               'records_for_screening': kept}
    (out / 'run.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main(sys.argv[1], '--reuse-hits' in sys.argv[2:])
