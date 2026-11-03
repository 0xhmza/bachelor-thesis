"""Catalogue every reading PDF in 01_Literature/PDFs: sha256, metadata
(registry.json, records.csv, filename) and the matching Zotero item.

Usage: python catalogue.py <copy-of-zotero.sqlite>
Writes output/catalogue.json (git-ignored).
"""
import csv, hashlib, json, pathlib, re, sqlite3, sys, unicodedata

here = pathlib.Path(__file__).parent
root = here.parents[2]
lit = root / '01_Literature'

def norm(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '', s)

def words(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower()
    return set(w for w in re.findall(r'[a-z0-9]+', s) if len(w) > 3)

registry = {pathlib.PureWindowsPath(e['pdf']).as_posix(): e for e in
            json.loads((lit / 'Methods-Digest/registry.json').read_text(encoding='utf-8')) if e.get('pdf')}
records = list(csv.DictReader(open(root / '05_Data/Literature Search/26. Oct/records.csv', encoding='utf-8')))

db = sqlite3.connect(f'file:{sys.argv[1]}?mode=ro', uri=True)
zrows = db.execute("""select i.key, it.typeName,
 max(case when f.fieldName='title' then v.value end),
 max(case when f.fieldName='DOI' then v.value end)
 from items i join itemTypes it using(itemTypeID)
 left join itemData d on d.itemID=i.itemID left join fields f using(fieldID)
 left join itemDataValues v using(valueID)
 where i.itemID not in (select itemID from deletedItems)
   and it.typeName not in ('attachment','note','annotation')
 group by i.itemID""").fetchall()

def zmatch(doi, title):
    for k, t, ti, zd in zrows:
        if doi and zd and doi.lower() == zd.lower():
            return k
    n = norm(title)
    for k, t, ti, zd in zrows:
        if n and len(n) > 25 and norm(ti)[:40] == n[:40]:
            return k
    return None

out = []
for p in sorted((lit / 'PDFs').rglob('*.pdf')):
    rel = p.relative_to(root).as_posix()
    e = registry.get(rel)
    m = dict(path=rel, sha=hashlib.sha256(p.read_bytes()).hexdigest(), size=p.stat().st_size)
    if e:
        m.update(src='registry', authors=e['authors'], year=e['year'], title=e['title'], doi=e.get('doi'), num=e['num'])
    else:
        parts = p.stem.split('_')
        sur = parts[1] if parts[0] in ('X', ) or re.match(r'N?\d', parts[0]) else parts[0]
        yr = next((x for x in parts if re.fullmatch(r'\d{4}', x)), None)
        fw = words(p.stem)
        best, bs = None, 0
        for r in records:
            if yr and r['year'] == yr and norm(sur) in norm(r['first_author']):
                s = len(fw & words(r['title']))
                if s > bs: best, bs = r, s
        m.update(src='records' if best and bs >= 2 else 'filename')
        if m['src'] == 'records':
            m.update(authors=best['first_author'], nauthors=best['authors'], year=int(best['year']), title=best['title'], doi=best['doi'] or None)
        else:
            m.update(year=int(yr) if yr else None, title=None, doi=None)
    m['zotero'] = zmatch(m.get('doi'), m.get('title'))
    out.append(m)

o = here / 'output'; o.mkdir(exist_ok=True)
(o / 'catalogue.json').write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding='utf-8')
from collections import Counter
print(len(out), 'pdfs,', len({m['sha'] for m in out}), 'unique;', Counter(m['src'] for m in out), '; zotero matched', sum(1 for m in out if m['zotero']))
