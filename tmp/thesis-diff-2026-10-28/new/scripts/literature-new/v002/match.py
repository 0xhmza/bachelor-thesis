"""Match each PDF of literature_new/references to an existing Zotero item.

A PDF matches an item when the DOIs are equal, or the normalised titles are equal
or one is a prefix of the other (at least 15 characters), or the title words overlap
by 80 percent and the first-author surname and year (+-1) agree.
Usage: python match.py <zotero.sqlite> [--show]   -> output/matches.json
"""
import json, pathlib, re, sqlite3, sys, unicodedata

here = pathlib.Path(__file__).parent
v1 = here.parent / 'v001'

def norm(s):
    s = unicodedata.normalize('NFKD', re.sub(r'<[^>]+>', '', s or '')).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '', s)

def words(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower()
    return set(w for w in re.findall(r'[a-z0-9]+', s) if len(w) > 2)

def load_items(db):
    rows = db.execute("""select i.itemID, i.key,
      max(case when f.fieldName='title' then v.value end), max(case when f.fieldName='DOI' then v.value end),
      max(case when f.fieldName='date' then v.value end),
      (select c.lastName from itemCreators ic join creators c using(creatorID) where ic.itemID=i.itemID order by ic.orderIndex limit 1)
      from items i join itemTypes it using(itemTypeID)
      left join itemData x on x.itemID=i.itemID left join fields f using(fieldID) left join itemDataValues v using(valueID)
      where it.typeName not in ('attachment','note','annotation') and i.itemID not in (select itemID from deletedItems)
      group by i.itemID""").fetchall()
    return [dict(id=r[0], key=r[1], title=r[2] or '', doi=(r[3] or '').lower(), year=(r[4] or '')[:4], first=r[5] or '') for r in rows]

def match(e, items):
    t, d = norm(e['title']), (e['doi'] or '').lower()
    year = str(e.get('year') or '')
    hits = []
    for it in items:
        ti = norm(it['title'])
        if d and it['doi'] and d == it['doi']:
            hits.append((it, 'doi')); continue
        if ti and t and (ti == t or (min(len(ti), len(t)) >= 15 and (ti.startswith(t) or t.startswith(ti)))):
            hits.append((it, 'title')); continue
        wa, wb = words(e['title']), words(it['title'])
        fa = norm(e['label'].split(' et al')[0].split(' &')[0].rsplit(' ', 1)[0])
        if wa and wb and len(wa & wb) / max(len(wa), len(wb)) >= 0.8 and norm(it['first']) and norm(it['first']) in fa + norm(e['label']) \
           and year.isdigit() and it['year'].isdigit() and abs(int(year) - int(it['year'])) <= 1:
            hits.append((it, 'fuzzy'))
    return hits

if __name__ == '__main__':
    db = sqlite3.connect(f'file:{sys.argv[1]}?mode=ro', uri=True)
    items = load_items(db)
    idx = json.loads((v1 / 'output/references-index.json').read_text(encoding='utf-8'))
    out = {}
    for e in idx:
        h = match(e, items)
        out[e['file']] = [(i['key'], how) for i, how in h]
        if '--show' in sys.argv:
            print(('1' if len(h) == 1 else str(len(h))), e['file'][:60], '=>', [(i['title'][:40], how) for i, how in h])
    (here / 'output').mkdir(exist_ok=True)
    (here / 'output/matches.json').write_text(json.dumps(out, indent=1), encoding='utf-8')
    from collections import Counter
    print(Counter(len(v) for v in out.values()))
