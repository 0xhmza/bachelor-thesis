"""Write 'Citation Key: <key>' into the Extra field of each Zotero item in
output/mapping.json, directly in zotero.sqlite. Zotero MUST be closed.

Usage: python apply_pins.py <path-to-zotero.sqlite>
A timestamped backup of the database is made first.
"""
import json, pathlib, shutil, sqlite3, sys, time
from datetime import datetime, timezone

dbp = pathlib.Path(sys.argv[1])
mapping = json.loads((pathlib.Path(__file__).parent / 'output/mapping.json').read_text(encoding='utf-8'))
bak = dbp.with_name(f'{dbp.name}.before-pin-{time.strftime("%Y%m%d-%H%M%S")}')
shutil.copy2(dbp, bak); print('backup:', bak)

db = sqlite3.connect(dbp)
extra_id = db.execute("select fieldID from fields where fieldName='extra'").fetchone()[0]
now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
changed = same = 0
with db:
    for item_key, ck in mapping.items():
        row = db.execute("select itemID from items where key=? and libraryID=1", (item_key,)).fetchone()
        if not row: print('missing item', item_key, ck); continue
        iid = row[0]
        cur = db.execute("select v.value from itemData d join itemDataValues v using(valueID) where d.itemID=? and d.fieldID=?", (iid, extra_id)).fetchone()
        lines = [l for l in (cur[0].split('\n') if cur else []) if not l.lower().startswith('citation key')]
        new = '\n'.join(['Citation Key: ' + ck] + lines)
        if cur and cur[0] == new: same += 1; continue
        v = db.execute("select valueID from itemDataValues where value=?", (new,)).fetchone()
        vid = v[0] if v else db.execute("insert into itemDataValues(value) values(?)", (new,)).lastrowid
        db.execute("insert or replace into itemData(itemID, fieldID, valueID) values(?,?,?)", (iid, extra_id, vid))
        db.execute("update items set dateModified=?, clientDateModified=?, synced=0 where itemID=?", (now, now, iid))
        changed += 1
print(f'pinned {changed}, unchanged {same}')
