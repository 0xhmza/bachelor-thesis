"""Abstracts for screening (D14): records whose source holds no abstract are looked up by DOI in OpenAlex.

    python scripts/literature-search/v002/enrich.py

OpenAlex is not a search source of this review; it only supplies abstracts for records already found (CHI, CCS,
IEEE S&P and NDSS titles from Crossref, citation-searching hits, thesis and digest works). Writes
output/abstracts-openalex.json (DOI -> abstract); merge.py fills empty abstracts from it and marks them.
Standard library only.
"""
import csv, json, time, urllib.parse

import lit
from search import OUT, fetch


def abstract_from_index(index):
    if not index:
        return ''
    words = sorted((pos, word) for word, positions in index.items() for pos in positions)
    return ' '.join(word for _, word in words)


def main():
    rows = list(csv.DictReader(open(OUT / 'records.csv', encoding='utf-8')))
    path = OUT / 'abstracts-openalex.json'
    found = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    want = sorted({r['doi'] for r in rows if r['doi'] and len(r['abstract']) < 80 and r['doi'] not in found})
    for i in range(0, len(want), 40):
        chunk = want[i:i + 40]
        params = {'filter': 'doi:' + '|'.join(chunk), 'per-page': 50, 'select': 'doi,abstract_inverted_index',
                  'mailto': 'shamza5568@gmail.com'}
        for w in json.loads(fetch('https://api.openalex.org/works?' + urllib.parse.urlencode(params)))['results']:
            found[lit.norm_doi(w['doi'])] = abstract_from_index(w.get('abstract_inverted_index'))
        for d in chunk:
            found.setdefault(d, '')
        time.sleep(1)
    path.write_text(json.dumps(found, indent=0, ensure_ascii=False), encoding='utf-8')
    print(len(want), 'looked up;', sum(1 for v in found.values() if v), 'abstracts held')


if __name__ == '__main__':
    main()
