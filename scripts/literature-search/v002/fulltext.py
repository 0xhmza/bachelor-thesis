"""Open-access full texts for the full-text stage of the literature review v002 (D14).

    python scripts/literature-search/v002/fulltext.py

For every record awaiting its full text (01_Literature/Literature-Review/decisions/fulltext.csv, decision `pending`),
candidate open-access locations are tried in this order: arXiv (by arXiv ID), Europe PMC full-text XML (PMID ->
PMCID), the paper page on usenix.org, the PoPETs site (by DOI), and the open-access locations OpenAlex lists for the
DOI. A file counts only if it is a PDF (or, for Europe PMC, an XML article body). Files are saved to
output/fulltexts/<record id>.pdf|.xml (outside Git); output/fulltexts.json records the URL used or why none was found.
Standard library only.
"""
import csv, json, re, time, urllib.error, urllib.parse, urllib.request

import lit
from search import OUT, UA

LR = lit.HERE.parents[2] / '01_Literature' / 'Literature-Review'
DIR = OUT / 'fulltexts'


def get(url, tries=2):
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read(), r.headers.get('Content-Type', '')
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and attempt < tries - 1:
                time.sleep(5)
                continue
            return None, f'HTTP {e.code}'
        except Exception as e:  # timeouts, resets, TLS errors: try the next location
            return None, type(e).__name__
    return None, 'failed'


def openalex_locations(dois):
    out = {}
    for i in range(0, len(dois), 40):
        chunk = dois[i:i + 40]
        params = {'filter': 'doi:' + '|'.join(chunk), 'per-page': 50, 'select': 'doi,locations',
                  'mailto': 'shamza5568@gmail.com'}
        body, _ = get('https://api.openalex.org/works?' + urllib.parse.urlencode(params))
        for w in json.loads(body or b'{"results": []}')['results']:
            urls = [l.get('pdf_url') for l in w.get('locations') or [] if l.get('is_oa') and l.get('pdf_url')]
            out[lit.norm_doi(w['doi'])] = urls
        time.sleep(1)
    return out


def pmcid(pmid):
    body, _ = get('https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?' +
                  urllib.parse.urlencode({'ids': pmid, 'format': 'json', 'tool': 'thesis', 'email': 'shamza5568@gmail.com'}))
    try:
        return json.loads(body)['records'][0].get('pmcid')
    except Exception:
        return None


def candidates(r, oa):
    urls = []
    if r['arxiv']:
        urls.append(('arXiv', f"https://arxiv.org/pdf/{r['arxiv']}"))
    if r['pmid']:
        pid = pmcid(r['pmid'])
        time.sleep(0.4)
        if pid:
            urls.append(('Europe PMC', f'https://www.ebi.ac.uk/europepmc/webservices/rest/{pid}/fullTextXML'))
    if 'usenix.org' in (r['url'] or ''):
        page, _ = get(r['url'])
        m = re.search(rb'href="(https://www\.usenix\.org/system/files/[^"]+\.pdf)"', page or b'')
        if m:
            urls.append(('usenix.org', m.group(1).decode()))
    m = re.match(r'10\.(?:56553|2478)/popets-(\d{4})-(\d{4})', r['doi'] or '')
    if m:
        urls.append(('PoPETs', f'https://petsymposium.org/popets/{m.group(1)}/popets-{m.group(1)}-{m.group(2)}.pdf'))
    for u in oa.get(r['doi'], []):
        urls.append(('OpenAlex OA location', u))
    return urls


def main():
    DIR.mkdir(parents=True, exist_ok=True)
    records = {r['id']: r for r in csv.DictReader(open(OUT / 'records.csv', encoding='utf-8'))}
    owner = {k: rid for rid, r in records.items() for k in r['ids'].split()}
    pending = [owner[row[0]] for row in csv.reader(open(LR / 'decisions' / 'fulltext.csv', encoding='utf-8'))
               if len(row) > 1 and row[1] == 'pending' and row[0] in owner]
    log_path = OUT / 'fulltexts.json'
    log = json.loads(log_path.read_text(encoding='utf-8')) if log_path.exists() else {}
    oa = openalex_locations(sorted({records[p]['doi'] for p in pending if records[p]['doi']}))
    for n, rid in enumerate(pending, 1):
        if log.get(rid, {}).get('file'):
            continue
        r, entry = records[rid], {'tried': []}
        for source, url in candidates(r, oa):
            body, ctype = get(url)
            ok_pdf = body is not None and body[:5] == b'%PDF-'
            ok_xml = body is not None and source == 'Europe PMC' and b'<body' in body
            entry['tried'].append(f'{source}: {url} -> ' + ('ok' if ok_pdf or ok_xml else (ctype or 'not a PDF')))
            if ok_pdf or ok_xml:
                path = DIR / f"{rid}.{'pdf' if ok_pdf else 'xml'}"
                path.write_bytes(body)
                entry.update(file=path.name, source=source, url=url)
                break
            time.sleep(1)
        log[rid] = entry
        time.sleep(1 if r['arxiv'] else 0.5)
        if n % 20 == 0:
            log_path.write_text(json.dumps(log, indent=1), encoding='utf-8')
            print(n, 'done;', sum(1 for e in log.values() if e.get('file')), 'files', flush=True)
    log_path.write_text(json.dumps(log, indent=1), encoding='utf-8')
    print(len(pending), 'pending;', sum(1 for p in pending if log.get(p, {}).get('file')), 'full texts obtained')


if __name__ == '__main__':
    main()
