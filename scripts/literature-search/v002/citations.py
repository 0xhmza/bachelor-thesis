"""Citation searching of the literature review v002 (D14): one round of backward and forward citations.

    python scripts/literature-search/v002/citations.py

Seeds are the four health-tracker papers the supervisor sent on 5 September 2026 (config.json, "citation_seeds").
References (backward) and citing works (forward) come from the OpenCitations Index (API v2, which merges COCI and
the other open citation sources); the metadata of every new DOI comes from Crossref. Writes
output/hits-citations.jsonl and output/run-citations.json. Standard library only.
"""
import json, time, urllib.error, urllib.parse

import lit
from search import OUT, fetch, stamp, write_jsonl

OC = 'https://api.opencitations.net/index/v2/'


def dois_in(field):
    return [lit.norm_doi(x[4:]) for x in field.split() if x.startswith('doi:')]


def neighbours(doi):
    refs = json.loads(fetch(OC + 'references/doi:' + doi))
    time.sleep(1)
    cites = json.loads(fetch(OC + 'citations/doi:' + doi))
    time.sleep(1)
    return ([d for r in refs for d in dois_in(r['cited'])], [d for c in cites for d in dois_in(c['citing'])])


def crossref(doi):
    try:
        item = json.loads(fetch('https://api.crossref.org/works/' + urllib.parse.quote(doi), tries=3))['message']
    except urllib.error.HTTPError:
        return None
    year = ((item.get('issued') or {}).get('date-parts') or [[None]])[0][0]
    import re
    return {'doi': doi, 'title': ' '.join((item.get('title') or [''])[0].split()),
            'abstract': ' '.join(re.sub(r'<[^>]+>', ' ', item.get('abstract') or '').split()), 'year': year,
            'venue': (item.get('container-title') or [''])[0], 'type': item.get('type', ''),
            'authors': [a.get('family', '') for a in item.get('author') or []], 'url': 'https://doi.org/' + doi}


def main():
    config = lit.load_config()
    log = {'platform': 'OpenCitations Index API v2 + Crossref', 'searched_at': stamp(), 'seeds': {}}
    hits, meta = [], {}
    for seed in config['citation_seeds']:
        back, forward = neighbours(seed['doi'])
        log['seeds'][seed['doi']] = {'label': seed['label'], 'backward': len(back), 'forward': len(forward)}
        print(seed['label'], 'backward', len(back), 'forward', len(forward), flush=True)
        for direction, dois in (('backward', back), ('forward', forward)):
            for doi in dois:
                if doi not in meta:
                    meta[doi] = crossref(doi)
                    time.sleep(0.2)
                if meta[doi] and meta[doi]['title']:
                    hits.append(dict(meta[doi], source='Citation searching', route='citation',
                                     strand=f"{direction}:{seed['label']}"))
    log['dois'] = len(meta)
    log['without_metadata'] = sum(1 for m in meta.values() if not m or not m['title'])
    write_jsonl(OUT / 'hits-citations.jsonl', hits)
    (OUT / 'run-citations.json').write_text(json.dumps(log, indent=1), encoding='utf-8')


if __name__ == '__main__':
    main()
