"""Write each paper's digest number as "[n]" into the Zotero field Call Number, so it can be
shown as a column ("Call #") and sorted. The number is `num` in
01_Literature/Methods-Digest/registry.json (the [n] used in the digest PDFs).

Items are matched to registry entries by DOI or title (match.py). Zotero MUST be closed;
a backup is made first. Safe to run again.
Usage: python set_call_numbers.py <path-to-zotero.sqlite>
"""
import json, pathlib, shutil, sqlite3, sys, time
from datetime import datetime, timezone

here = pathlib.Path(__file__).parent
sys.path.insert(0, str(here))
from match import load_items, match, norm

root = here.parents[2]
dbp = pathlib.Path(sys.argv[1])
bak = dbp.with_name(f'{dbp.name}.before-callnumbers-{time.strftime("%Y%m%d-%H%M%S")}')
shutil.copy2(dbp, bak); print('backup:', bak)
db = sqlite3.connect(dbp)
reg = json.loads((root / '01_Literature/Methods-Digest/registry.json').read_text(encoding='utf-8'))
items = load_items(db)
fid = db.execute("select fieldID from fields where fieldName='callNumber'").fetchone()[0]
now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
nums = {}
for e in reg:
    hits = match(dict(title=e['title'], doi=e.get('doi') or '', year=e.get('year'), label=e['label']), items)
    if len(hits) > 1:  # prefer a DOI match, then an exact title
        exact = [h for h in hits if h[1] == 'doi'] or [h for h in hits if norm(h[0]['title']) == norm(e['title'])]
        hits = exact or hits
    if len(hits) == 1:
        nums.setdefault(hits[0][0]['id'], []).append(e['num'])
    elif hits:
        print('ambiguous', e['num'], e['label'], len(hits))
    else:
        print('no item for', e['num'], e['label'])
done = 0
with db:
    for iid, ns in nums.items():
        value = ', '.join(f'[{n}]' for n in sorted(ns))
        v = db.execute('select valueID from itemDataValues where value=?', (value,)).fetchone()
        vid = v[0] if v else db.execute('insert into itemDataValues(value) values(?)', (value,)).lastrowid
        db.execute('insert or replace into itemData(itemID, fieldID, valueID) values(?,?,?)', (iid, fid, vid))
        db.execute('update items set dateModified=?, clientDateModified=?, synced=0 where itemID=?', (now, now, iid))
        done += 1
print(f'{done} items numbered of {len(reg)} registry entries')
