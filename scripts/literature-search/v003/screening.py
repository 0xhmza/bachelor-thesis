"""Screening log of the literature review v003 (D14): joins the records with the decisions and counts each rule.

    python scripts/literature-search/v003/screening.py

Reads output/records.csv and 01_Literature/Literature-Review/decisions/*.csv (id,decision,code,note; `title.csv`
for the title-and-abstract stage, `fulltext.csv` for the full-text stage, `extraction.csv` for the coding of the
included studies). Writes 01_Literature/Literature-Review/screening.csv (every record) and corpus.csv (review
evidence and the contextual collection), and output/screening.json with the counts per rule in the order of the
protocol. Fails if a record lacks a decision or a decision names an unknown record or rule. Standard library only.
"""
import csv, json, sys
from pathlib import Path

import lit

ROOT = lit.HERE.parents[2]
LR = ROOT / '01_Literature' / 'Literature-Review'
OUT = lit.HERE / 'output'
RULES = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8']
RULE_TEXT = {'R1': 'not a research article', 'R2': 'outside language or period', 'R3': 'outside the domain',
             'R4': 'domain without privacy focus', 'R5': 'technical system without harms or communication',
             'R6': 'privacy text outside LQ3 and LQ4', 'R7': 'full text not retrievable', 'R8': 'fails C1 or C4 on full text'}
LQS = ['LQ1', 'LQ2', 'LQ3', 'LQ4']


def read_decisions(name):
    path = LR / 'decisions' / name
    out = {}
    if not path.exists():
        return out
    for row in csv.reader(open(path, encoding='utf-8')):
        if not row or ':' not in row[0] or row[0].startswith('#'):
            continue
        rid, decision, code = row[0].strip(), row[1].strip(), row[2].strip()
        note = ','.join(row[3:]).strip()
        if rid in out:
            raise SystemExit(f'{name}: {rid} entered twice')
        if decision == 'ex' and code not in RULES:
            raise SystemExit(f'{name}: {rid} unknown rule {code}')
        if decision == 'in' and code and not set(code.split(';')) <= set(LQS):
            raise SystemExit(f'{name}: {rid} unknown sub-question {code}')
        out[rid] = (decision, code, note)
    return out


def main():
    records = list(csv.DictReader(open(OUT / 'records.csv', encoding='utf-8')))
    owner = {k: r['id'] for r in records for k in r['ids'].split()}
    title, full = {}, {}
    for name, target in (('title.csv', title), ('fulltext.csv', full)):
        for key, value in read_decisions(name).items():  # decisions are keyed by any identifier of the record
            if key not in owner:
                raise SystemExit(f'{name}: no record has the identifier {key}')
            if owner[key] in target and target[owner[key]] != value:
                raise SystemExit(f'{name}: conflicting decisions for {owner[key]} ({key})')
            target[owner[key]] = value
    rows, missing = [], []
    for r in records:
        t = title.get(r['id'])
        if not t:
            missing.append(r['id'])
            continue
        if t[0] == 'ex':
            if t[1] in ('R7', 'R8'):
                raise SystemExit(f"{r['id']}: {t[1]} is a full-text rule")
            decision, code, stage, note = 'exclude', t[1], 'title/abstract', t[2]
        else:
            f = full.get(r['id'])
            if not f:
                missing.append(r['id'] + ' (full text)')
                continue
            stage = 'full text'
            if f[0] == 'pending':  # passed title and abstract; full text not yet obtained
                decision, code, note, stage = 'pending', t[1], f[2], 'awaiting full text'
            else:
                decision, code, note = ('exclude', f[1], f[2]) if f[0] == 'ex' else ('include', f[1], f[2] or t[2])
        cited = bool(r['bibkey'])
        collection = ('review' if decision == 'include' else 'awaiting full text' if decision == 'pending'
                      else 'contextual' if cited else 'excluded')
        rows.append(dict(r, decision=decision, code=code, reason=RULE_TEXT.get(code, 'meets C1-C4'), stage=stage,
                         collection=collection, note=note))
    if missing:
        raise SystemExit(f'{len(missing)} records without a decision, e.g. {missing[:8]}')
    fields = ['id', 'decision', 'code', 'reason', 'stage', 'collection', 'note', 'title', 'year', 'first_author', 'venue',
              'doi', 'arxiv', 'pmid', 'ieee', 'bibkey', 'digest', 'sources', 'routes', 'strands', 'url']
    with open(LR / 'screening.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        w.writeheader()
        w.writerows(rows)
    remaining, funnel = len(rows), []
    pending = [r for r in rows if r['decision'] == 'pending']
    for rule in RULES:
        if rule == 'R7':  # records awaiting their full text leave the funnel before the full-text rules
            remaining -= len(pending)
        n = sum(1 for r in rows if r['decision'] == 'exclude' and r['code'] == rule)
        funnel.append({'rule': rule, 'text': RULE_TEXT[rule], 'assessed': remaining, 'excluded': n,
                       'remaining': remaining - n, 'percent': round(100 * n / remaining, 1) if remaining else 0.0})
        remaining -= n
    included = [r for r in rows if r['decision'] == 'include']
    counts = {'records': len(rows), 'funnel': funnel, 'included': len(included),
              'per_lq': {q: sum(1 for r in included if q in r['code'].split(';')) for q in LQS},
              'pending': len(pending),
              'pending_per_lq': {q: sum(1 for r in pending if q in r['code'].split(';')) for q in LQS},
              'contextual': sum(1 for r in rows if r['collection'] == 'contextual'),
              'title_stage_passed': sum(1 for r in rows if r['stage'] != 'title/abstract'),
              'fulltext_assessed': sum(1 for r in rows if r['stage'] == 'full text')}
    assert remaining == len(included)
    (OUT / 'screening.json').write_text(json.dumps(counts, indent=1), encoding='utf-8')
    print(json.dumps(counts, indent=1))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
