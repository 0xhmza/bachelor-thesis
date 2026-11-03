"""Put the thesis reference numbers [n] into Zotero's Rights and Call Number fields.

[n] is the number printed in the thesis bibliography: the position of the entry in
03_Thesis/thesis.bbl (biblatex numeric, sorted by name, year, title), so only the works the
thesis cites get a number (compile the thesis first so thesis.bbl is current). Items are found
by their Zotero Citation Key. Rights is valid for every item type, so it shows all numbers in one
column; Call Number is also set where the item type has it (not Web Page). Values of the form "[n]" set earlier (the digest numbers of
v002) are removed first from both fields; any other value is left alone. Safe to run again.

Zotero MUST be closed; a backup is made first.
Usage: python set_thesis_numbers.py <path-to-zotero.sqlite> [--dry]
"""
import pathlib, re, shutil, sqlite3, sys, time
from datetime import datetime, timezone

root = pathlib.Path(__file__).resolve().parents[3]
dbp, dry = pathlib.Path(sys.argv[1]), '--dry' in sys.argv
keys = re.findall(r'^\s*\\entry\{([^}]+)\}', (root / '03_Thesis/thesis.bbl').read_text(encoding='utf-8'), re.M)
if not dry:
    bak = dbp.with_name(f'{dbp.name}.before-thesis-numbers-{time.strftime("%Y%m%d-%H%M%S")}')
    shutil.copy2(dbp, bak); print('backup:', bak)
db = sqlite3.connect(dbp)
call = db.execute("select fieldID from fields where fieldName='callNumber'").fetchone()[0]
rights = db.execute("select fieldID from fields where fieldName='rights'").fetchone()[0]
has_call = {r[0] for r in db.execute('select itemTypeID from itemTypeFields where fieldID=?', (call,))}
ckey = db.execute("select fieldID from fields where fieldName='citationKey'").fetchone()[0]
now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

def touch(i):
    db.execute('update items set dateModified=?, clientDateModified=?, synced=0 where itemID=?', (now, now, i))

with db:
    old = db.execute("select x.itemID, x.fieldID from itemData x join itemDataValues v using(valueID) where x.fieldID in (?,?) and v.value glob '[[][0-9]*]*'", (call, rights)).fetchall()
    for i, f in old:
        db.execute('delete from itemData where itemID=? and fieldID=?', (i, f)); touch(i)
    done, missing = 0, []
    for n, k in enumerate(keys, 1):
        r = db.execute('select x.itemID from itemData x join itemDataValues v using(valueID) join items i using(itemID) '
                       'where x.fieldID=? and v.value=? and i.itemID not in (select itemID from deletedItems)', (ckey, k)).fetchone()
        if not r:
            missing.append(k); continue
        value = f'[{n}]'
        v = db.execute('select valueID from itemDataValues where value=?', (value,)).fetchone()
        vid = v[0] if v else db.execute('insert into itemDataValues(value) values(?)', (value,)).lastrowid
        fields = [rights] + ([call] if db.execute('select itemTypeID from items where itemID=?', (r[0],)).fetchone()[0] in has_call else [])
        for f in fields:
            db.execute('insert or replace into itemData(itemID, fieldID, valueID) values(?,?,?)', (r[0], f, vid))
        touch(r[0]); done += 1
    if dry:
        db.rollback()
print(f'removed {len(old)} old numbers; numbered {done} of {len(keys)} cited works; missing in Zotero: {missing}')
