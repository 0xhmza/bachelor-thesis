"""Identification stage of the literature review v003 (D14): database searches and venue enumerations.

    python scripts/literature-search/v003/search.py [pubmed] [arxiv] [acl] [venues]   # default: all four
    python -I -m unittest discover -s scripts/literature-search/v003/tests

Databases (native search of titles and abstracts): PubMed (E-utilities, [tiab]), arXiv (API, ti/abs) and the ACL
Anthology (the anthology's own BibTeX file with abstracts, searched locally). Venues (complete enumeration of the
period, then the local Boolean of lit.py on title and abstract): PoPETs, CCS, IEEE S&P, NDSS, CHI and CSCW from
Crossref metadata, USENIX Security and SOUPS from usenix.org. IEEE Xplore is searched in its web interface; its
results are imported by import_ieee.py. ACM Digital Library, dblp, Scopus, Web of Science and Google Scholar could not
be queried (see the README).

Writes output/hits-<source>.jsonl (one line per hit and strand), output/venues.jsonl (every enumerated venue paper,
for the venue counts) and output/run-<source>.json (exact strings, dates, counts). Standard library only.
"""
import gzip, hashlib, http.client, json, re, sys, time, urllib.error, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

import lit

OUT = lit.HERE / 'output'
UA = {'User-Agent': 'bachelor-thesis-literature-search/2.0 (mailto:shamza5568@gmail.com)'}


CACHE = OUT / 'cache' / 'http'


def fetch(url, data=None, tries=6, raw=False):
    """GET or POST with retries; GET responses are cached in output/cache/http so that an interrupted run resumes."""
    key = CACHE / (hashlib.sha1(url.encode()).hexdigest() + '.bin')
    if data is None and key.exists():
        body = key.read_bytes()
        return body if raw else body.decode('utf-8')
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, data=data, headers=UA)
            with urllib.request.urlopen(req, timeout=120) as response:
                body = response.read()
            if data is None:
                CACHE.mkdir(parents=True, exist_ok=True)
                key.write_bytes(body)
            return body if raw else body.decode('utf-8')
        except (urllib.error.URLError, TimeoutError, ConnectionError, http.client.HTTPException) as error:
            code = getattr(error, 'code', None)
            if attempt < tries - 1 and code in (None, 429, 500, 502, 503, 504):
                time.sleep(5 * (attempt + 1))
                continue
            raise


def write_jsonl(path, rows):
    with open(path, 'w', encoding='utf-8') as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + '\n')


def stamp():
    return time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())


# --- PubMed ----------------------------------------------------------------------------------------------------------

EUTILS = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'


def pubmed_records(pmids):
    rows = []
    for i in range(0, len(pmids), 200):
        body = urllib.parse.urlencode({'db': 'pubmed', 'id': ','.join(pmids[i:i + 200]), 'retmode': 'xml'}).encode()
        root = ET.fromstring(fetch(EUTILS + 'efetch.fcgi', data=body))
        for art in root.iter('PubmedArticle'):
            cit = art.find('MedlineCitation')
            a = cit.find('Article')
            text = lambda el: ''.join(el.itertext()).strip() if el is not None else ''
            year = text(a.find('Journal/JournalIssue/PubDate/Year')) or text(a.find('Journal/JournalIssue/PubDate/MedlineDate'))[:4]
            doi = next((text(e) for e in art.iter('ArticleId') if e.get('IdType') == 'doi'), '')
            rows.append({'pmid': text(cit.find('PMID')), 'title': text(a.find('ArticleTitle')),
                         'abstract': ' '.join(text(e) for e in a.iter('AbstractText')),
                         'year': int(year) if year.isdigit() else None, 'venue': text(a.find('Journal/Title')),
                         'type': ';'.join(text(e) for e in a.iter('PublicationType')),
                         'language': ';'.join(text(e) for e in a.iter('Language')), 'doi': lit.norm_doi(doi),
                         'authors': [text(e.find('LastName')) for e in a.iter('Author') if e.find('LastName') is not None],
                         'url': f"https://pubmed.ncbi.nlm.nih.gov/{text(cit.find('PMID'))}/"})
        time.sleep(0.4)
    return rows


def run_pubmed(config):
    until = config['period']['until']
    hits, log = [], {'platform': 'PubMed', 'searched_at': stamp(), 'field': 'Title/Abstract [tiab]',
                     'filters': 'publication date (pdat) from strand start to ' + until + '; no language or type filter',
                     'queries': {}}
    for s in config['strands']:
        query = lit.pubmed_query(config, s['id'])
        params = {'db': 'pubmed', 'term': query, 'retmode': 'json', 'retmax': 10000, 'datetype': 'pdat',
                  'mindate': s['from'].replace('-', '/'), 'maxdate': until.replace('-', '/')}
        res = json.loads(fetch(EUTILS + 'esearch.fcgi', data=urllib.parse.urlencode(params).encode()))['esearchresult']
        pmids = res['idlist']
        log['queries'][s['id']] = {'query': query, 'from': s['from'], 'count': int(res['count']),
                                   'translation': res.get('querytranslation', '')}
        for row in pubmed_records(pmids):
            hits.append(dict(row, source='PubMed', route='database', strand=s['id']))
        print('PubMed', s['id'], res['count'], flush=True)
    return hits, log


# --- arXiv -----------------------------------------------------------------------------------------------------------

ATOM = '{http://www.w3.org/2005/Atom}'


def arxiv_fetch(query):
    """Every arXiv entry for one simple query, as a dict by arXiv ID."""
    found, start, total = {}, 0, None
    while total is None or start < total:
        url = 'https://export.arxiv.org/api/query?' + urllib.parse.urlencode(
            {'search_query': query, 'start': start, 'max_results': 500, 'sortBy': 'submittedDate'})
        root = ET.fromstring(fetch(url))
        total = int(root.find('{http://a9.com/-/spec/opensearch/1.1/}totalResults').text)
        entries = root.findall(ATOM + 'entry')
        for e in entries:
            aid = lit.arxiv_id(e.find(ATOM + 'id').text)
            doi = e.find('{http://arxiv.org/schemas/atom}doi')
            journal = e.find('{http://arxiv.org/schemas/atom}journal_ref')
            found[aid] = {'source': 'arXiv', 'route': 'database', 'arxiv': aid,
                          'title': ' '.join(e.find(ATOM + 'title').text.split()),
                          'abstract': ' '.join(e.find(ATOM + 'summary').text.split()),
                          'date': e.find(ATOM + 'published').text[:10], 'year': int(e.find(ATOM + 'published').text[:4]),
                          'venue': journal.text if journal is not None else 'arXiv', 'type': 'preprint',
                          'doi': lit.norm_doi(doi.text) if doi is not None else '',
                          'authors': [a.find(ATOM + 'name').text.split()[-1] for a in e.findall(ATOM + 'author')],
                          'url': f'https://arxiv.org/abs/{aid}'}
        start += 500
        time.sleep(3.5)  # arXiv asks for one request every three seconds
        if not entries:
            break
    return found, total


def run_arxiv(config):
    """The arXiv API loses results on long nested Boolean queries (a test query of the full S3 string returned 34
    records, while 'privacy policy' AND LLM alone returned 62). Each strand is therefore retrieved with short anchor
    queries (S1/S2: every pair of a domain and a privacy term; S3/S4: every privacy-text term), and the complete strand
    Boolean is then applied locally to title and abstract, as for the venue enumerations."""
    start, until = config['period']['from'], config['period']['until']
    window = f" AND submittedDate:[{start.replace('-', '')}0000 TO {until.replace('-', '')}2359]"
    hits, log = [], {'platform': 'arXiv', 'searched_at': stamp(), 'field': 'title (ti) and abstract (abs)',
                     'filters': f'submittedDate {start} to {until}; S3 from 2022-01-01 (applied locally)',
                     'anchors': {}, 'queries': {}}
    pool = {}
    a = config['arxiv_anchors']
    anchors = {'D&P': [f'({lit.arxiv_term(k)}) AND ({lit.arxiv_term(p)})' for k in a['domain_words'] for p in a['privacy']],
               'T': [' AND '.join(f'({lit.arxiv_term(w)})' for w in pair) for pair in a['privacy_text']]}
    for name, queries in anchors.items():
        for q in queries:
            found, total = arxiv_fetch(q + window)
            log['anchors'][q] = total
            for aid, row in found.items():
                pool.setdefault(aid, row)
        print('arXiv anchors', name, len(pool), flush=True)
    log['pool'] = len(pool)
    for s in config['strands']:
        if 'platforms' in s:
            continue
        n = 0
        for row in pool.values():
            if row['date'] >= s['from'] and lit.strand_match(config, s['id'], row['title'] + ' ' + row['abstract']):
                hits.append(dict(row, strand=s['id']))
                n += 1
        log['queries'][s['id']] = {'query': ' AND '.join(s['groups']) + ' (local, on the anchor pool)', 'from': s['from'], 'count': n}
        print('arXiv', s['id'], n, flush=True)
    return hits, log


# --- ACL Anthology -----------------------------------------------------------------------------------------------------

ACL_BIB = 'https://aclanthology.org/anthology+abstracts.bib.gz'


def acl_entries(path):
    text = gzip.open(path, 'rt', encoding='utf-8').read()
    for chunk in text.split('\n@')[1:]:
        fields = dict(re.findall(r'^\s*(\w+)\s*=\s*"(.*)",?\s*$', chunk, flags=re.M))
        key = chunk[chunk.find('{') + 1:chunk.find(',')]
        yield key, chunk.split('{', 1)[0], fields


def run_acl(config):
    cache = OUT / 'cache'
    cache.mkdir(parents=True, exist_ok=True)
    path = cache / 'anthology+abstracts.bib.gz'
    path.write_bytes(fetch(ACL_BIB, raw=True))
    hits, log = [], {'platform': 'ACL Anthology', 'searched_at': stamp(), 'field': 'title and abstract (local Boolean)',
                     'file': ACL_BIB, 'queries': {}}
    entries = [(k, t, f) for k, t, f in acl_entries(path) if t.strip() != 'proceedings']
    log['entries'] = len(entries)
    for s in config['strands']:
        if 'platforms' in s:
            continue
        n = 0
        for key, kind, f in entries:
            year = int(f['year']) if f.get('year', '').isdigit() else None
            if not year or year < int(s['from'][:4]):
                continue
            text = f.get('title', '') + ' ' + f.get('abstract', '')
            if lit.strand_match(config, s['id'], text):
                n += 1
                hits.append({'source': 'ACL Anthology', 'route': 'database', 'strand': s['id'], 'acl': key,
                             'title': re.sub(r'[{}]', '', f.get('title', '')), 'abstract': f.get('abstract', ''),
                             'year': year, 'venue': re.sub(r'[{}]', '', f.get('booktitle', f.get('journal', ''))),
                             'type': kind.strip(), 'doi': lit.norm_doi(f.get('doi')),
                             'authors': [a.split(',')[0].strip() for a in f.get('author', '').split(' and ') if a],
                             'url': f.get('url', '')})
        log['queries'][s['id']] = {'query': ' AND '.join(s['groups']), 'from': s['from'], 'count': n}
        print('ACL', s['id'], n, flush=True)
    return hits, log


# --- Venue enumerations ------------------------------------------------------------------------------------------------

CROSSREF = 'https://api.crossref.org/works'
SELECT = 'DOI,title,abstract,container-title,issued,type,author,issue,ISSN'


def crossref_all(filters):
    cursor, items = '*', []
    while True:
        params = {'filter': filters, 'rows': 1000, 'cursor': cursor, 'select': SELECT, 'mailto': UA['User-Agent']}
        msg = json.loads(fetch(CROSSREF + '?' + urllib.parse.urlencode(params)))['message']
        items.extend(msg['items'])
        if len(msg['items']) < 1000:
            return items
        cursor = msg['next-cursor']
        time.sleep(1)


def container_titles(venue, start, until):
    """Exact container titles of the venue, found with Crossref's container-title facet one year at a time."""
    names = set()
    for year in range(int(start[:4]), int(until[:4]) + 1):
        params = {'query.container-title': venue['query'], 'rows': 0, 'facet': 'container-title:1000',
                  'filter': f"prefix:{venue['prefix']},from-pub-date:{year}-01-01,until-pub-date:{year}-12-31"}
        facet = json.loads(fetch(CROSSREF + '?' + urllib.parse.urlencode(params)))['message']['facets']
        for name in facet.get('container-title', {}).get('values', {}):
            low = lit.norm_text(name).strip()
            if re.search(venue['pattern'], low) and not any(x in low for x in venue['exclude']):
                names.add(name)
        time.sleep(0.5)
    return sorted(names)


def crossref_paper(item, venue_id):
    year = ((item.get('issued') or {}).get('date-parts') or [[None]])[0][0]
    return {'venue_id': venue_id, 'doi': lit.norm_doi(item.get('DOI')), 'title': ' '.join((item.get('title') or [''])[0].split()),
            'abstract': ' '.join(re.sub(r'<[^>]+>', ' ', item.get('abstract') or '').split()), 'year': year,
            'venue': (item.get('container-title') or [''])[0], 'type': item.get('type', ''),
            'authors': [a.get('family', '') for a in item.get('author') or []], 'issue': item.get('issue', ''),
            'url': 'https://doi.org/' + item.get('DOI', ''), 'platform': 'Crossref'}


def lit_year(item):
    return ((item.get('issued') or {}).get('date-parts') or [[0]])[0][0] or 0


def enumerate_crossref(venue, start, until):
    papers, used = [], []
    if 'issn' in venue:
        used.append(f"issn:{venue['issn']}")
        papers += [crossref_paper(i, venue['id']) for i in
                   crossref_all(f"issn:{venue['issn']},from-pub-date:{start},until-pub-date:{until}")]
    else:
        for name in container_titles(venue, start, until):
            used.append(name)
            papers += [crossref_paper(i, venue['id']) for i in crossref_all(
                f"container-title:{name},from-pub-date:{start},until-pub-date:{until}")]
    if 'pacm_issn' in venue:  # CSCW papers appear in PACM HCI from 2017, in the issues marked CSCW
        used.append(f"issn:{venue['pacm_issn']} issue {venue['pacm_issue']}*")
        papers += [crossref_paper(i, venue['id']) for i in
                   crossref_all(f"issn:{venue['pacm_issn']},from-pub-date:{start},until-pub-date:{until}")
                   if (i.get('issue') or '').upper().startswith(venue['pacm_issue'])
                   or (lit_year(i) >= 2025 and (i.get('issue') or '').isdigit())]  # from 2025 issues are numbered
    papers = [p for p in papers if p['type'] in ('journal-article', 'proceedings-article') and p['title']]
    return papers, used


def enumerate_usenix(venue, start, until):
    papers, used = [], []
    for year in range(int(start[:4]), int(until[:4]) + 1):
        slug = venue['slug'].replace('{yy}', str(year)[2:]).replace('{yyyy}', str(year))
        url = f'https://www.usenix.org/conference/{slug}/technical-sessions'
        try:
            page = fetch(url)
        except urllib.error.HTTPError:
            continue
        used.append(url)
        for block in re.split(r'<(?:article|div)[^>]+class="node node-paper', page)[1:]:  # 2014-2016 pages use div
            title = re.search(r'<h2[^>]*>\s*<a href="([^"]+)">(.*?)</a>', block, flags=re.S)
            if not title:
                continue
            abstract = re.search(r'field-name-field-paper-description-long[^>]*>(.*?)</div>', block, flags=re.S)
            papers.append({'venue_id': venue['id'], 'doi': '', 'title': ' '.join(lit.html.unescape(re.sub('<[^>]+>', '', title.group(2))).split()),
                           'abstract': ' '.join(lit.html.unescape(re.sub('<[^>]+>', ' ', abstract.group(1) if abstract else '')).split()),
                           'year': year, 'venue': venue['name'] + f' {year}', 'type': 'proceedings-article', 'authors': [],
                           'url': 'https://www.usenix.org' + title.group(1), 'platform': 'usenix.org'})
        time.sleep(1)
    keynotes = re.compile(r'^(keynote|panel|lightning talks?|opening remarks|closing remarks|invited talk)', re.I)
    return [p for p in papers if not keynotes.match(p['title'])], used


def venue_matches(config, venue, paper):
    rules = config['venue_rules'][venue['kind']]
    has_abstract = len(paper['abstract']) > 80
    text = paper['title'] + ' ' + (paper['abstract'] if has_abstract else '')
    found = []
    for rule in rules['abstract' if has_abstract else 'title_only']:
        if (rule == 'S3' or 'L' in rule.split('&')) and (paper['year'] or 0) < 2022:  # S3 starts in 2022
            continue
        if lit.rule_match(config, rule, text):
            found.append(rule)
    return found, has_abstract


def run_venues(config):
    start, until = config['period']['from'], config['period']['until']
    hits, catalogue, log = [], [], {'platform': 'venue enumeration', 'searched_at': stamp(), 'venues': {}}
    for venue in config['venues']:
        if venue['platform'] == 'usenix.org':
            papers, used = enumerate_usenix(venue, start, until)
        else:
            papers, used = enumerate_crossref(venue, start, until)
        n_abs = 0
        for p in papers:
            found, has_abstract = venue_matches(config, venue, p)
            n_abs += has_abstract
            p['match'] = found
            catalogue.append(p)
            for rule in found:
                hits.append(dict(p, source=venue['id'], route='venue', strand=rule))
        log['venues'][venue['id']] = {'platform': venue['platform'], 'containers_or_pages': used, 'papers': len(papers),
                                      'with_abstract': n_abs, 'matched': sum(1 for p in papers if p['match'])}
        print(venue['id'], len(papers), 'papers,', n_abs, 'with abstract,', log['venues'][venue['id']]['matched'], 'matched', flush=True)
    return hits, log, catalogue


def main(argv):
    config = lit.load_config()
    OUT.mkdir(exist_ok=True)
    for name in (argv or ['pubmed', 'arxiv', 'acl', 'venues']):
        if name == 'venues':
            hits, log, catalogue = run_venues(config)
            write_jsonl(OUT / 'venues.jsonl', catalogue)
        else:
            hits, log = {'pubmed': run_pubmed, 'arxiv': run_arxiv, 'acl': run_acl}[name](config)
        write_jsonl(OUT / f'hits-{name}.jsonl', hits)
        (OUT / f'run-{name}.json').write_text(json.dumps(log, indent=1, ensure_ascii=False), encoding='utf-8')


if __name__ == '__main__':
    main(sys.argv[1:])
