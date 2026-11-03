"""Extraction for the evidence map of the literature review v002 (D14).

    python scripts/literature-search/v002/extract.py

For every record that passed title-and-abstract screening (review evidence and records awaiting their full text),
the app domain, the surfaces or material studied and the venue type are coded from title, abstract and venue with
the fixed keyword rules of config.json ("extraction_rules"). The parts of the thesis RQ a study bears on are coded by
hand, from the full text, for the review evidence only (decisions/extraction-hand.csv). Writes
01_Literature/Literature-Review/extraction.csv. Standard library only.
"""
import csv

import lit

ROOT = lit.HERE.parents[2]
LR = ROOT / '01_Literature' / 'Literature-Review'


def codes(rules, text):
    norm = lit.norm_text(text)
    found = []
    for label, terms in rules.items():
        if label.startswith('_'):
            continue
        if any(lit.term_regex(t).search(norm) for t in terms):
            found.append(label)
    return found


def main():
    config = lit.load_config()
    rules = config['extraction_rules']
    rows = [r for r in csv.DictReader(open(LR / 'screening.csv', encoding='utf-8'))
            if r['decision'] in ('include', 'pending')]
    records = {r['id']: r for r in csv.DictReader(open(lit.HERE / 'output' / 'records.csv', encoding='utf-8'))}
    hand = {r['id']: r for r in csv.DictReader(open(LR / 'decisions' / 'extraction-hand.csv', encoding='utf-8'))}
    out = []
    for r in rows:
        rec = records[r['id']]
        text = rec['title'] + ' ' + rec['abstract']
        domain = codes(rules['domain'], text)
        if not domain:
            domain = ['Health apps in general'] if lit.group_match(config, 'D', text) else ['Outside health']
        surface = codes(rules['surface'], text) or ['Not stated']
        vtype = None
        for venue in ([rec['venue']] if rec['venue'] else [rec['sources']]):  # the venue; the source only if none
            vtype = vtype or next((v for v, terms in rules['venue_type'].items() if not v.startswith('_')
                                   and any(lit.term_regex(t).search(lit.norm_text(venue)) for t in terms)), None)
        vtype = vtype or 'Other computing venue'
        out.append({'id': r['id'], 'status': 'review' if r['decision'] == 'include' else 'awaiting full text',
                    'lq': r['code'], 'year': r['year'], 'domain': ';'.join(domain), 'surface': ';'.join(surface),
                    'venue_type': vtype, 'rq': hand.get(r['id'], {}).get('rq', ''),
                    'harms': hand.get(r['id'], {}).get('harms', ''), 'title': r['title']})
    with open(LR / 'extraction.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    print(len(out), 'records coded;', sum(1 for o in out if o['rq']), 'with hand-coded RQ parts')


if __name__ == '__main__':
    main()
