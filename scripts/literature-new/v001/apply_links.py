"""Link the PDFs in literature_new/references/ to Zotero items directly in
zotero.sqlite (linked-file attachments, so Zotero keeps pointers, not copies).
Zotero MUST be closed. A timestamped backup of the database is made first.

Existing items (matched by catalogue.py) are reused, the others are created as
'document' items; all go into the collection "Methodology literature".
Re-running is safe.

Usage: python apply_links.py <path-to-zotero.sqlite>   (after make_zotero_js.py)
"""
import json, pathlib, random, shutil, sqlite3, sys, time
from datetime import datetime, timezone

here = pathlib.Path(__file__).parent
root = here.parents[2]
refs = root / 'literature_new' / 'references'
data = json.loads((here / 'output/zotero-data.json').read_text(encoding='utf-8'))

dbp = pathlib.Path(sys.argv[1])
bak = dbp.with_name(f'{dbp.name}.before-links-{time.strftime("%Y%m%d-%H%M%S")}')
shutil.copy2(dbp, bak); print('backup:', bak)
db = sqlite3.connect(dbp)
now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
ALPHA = '23456789ABCDEFGHIJKLMNPQRSTUVWXYZ'

def newkey():
    while True:
        k = ''.join(random.choice(ALPHA) for _ in range(8))
        if not db.execute('select 1 from items where key=? and libraryID=1', (k,)).fetchone() and \
           not db.execute('select 1 from collections where key=? and libraryID=1', (k,)).fetchone():
            return k

fid = {n: db.execute('select fieldID from fields where fieldName=?', (n,)).fetchone()[0] for n in ('title', 'date', 'url', 'extra')}
doc_type = db.execute("select itemTypeID from itemTypes where typeName='document'").fetchone()[0]
att_type = db.execute("select itemTypeID from itemTypes where typeName='attachment'").fetchone()[0]
author = db.execute("select creatorTypeID from creatorTypes where creatorType='author'").fetchone()[0]

def setfield(iid, name, value):
    v = db.execute('select valueID from itemDataValues where value=?', (value,)).fetchone()
    vid = v[0] if v else db.execute('insert into itemDataValues(value) values(?)', (value,)).lastrowid
    db.execute('insert or replace into itemData(itemID, fieldID, valueID) values(?,?,?)', (iid, fid[name], vid))

def newitem(type_id):
    return db.execute('insert into items(itemTypeID, dateAdded, dateModified, clientDateModified, libraryID, key, synced) values(?,?,?,?,1,?,0)',
                      (type_id, now, now, now, newkey())).lastrowid

created = reused = linked = had = 0
with db:
    row = db.execute("select collectionID from collections where collectionName='Methodology literature' and libraryID=1").fetchone()
    coll = row[0] if row else db.execute('insert into collections(collectionName, clientDateModified, libraryID, key, synced) values(?,?,1,?,0)',
                                         ('Methodology literature', now, newkey())).lastrowid
    for d in data:
        iid = None
        if d['key']:
            r = db.execute('select itemID from items where key=? and libraryID=1', (d['key'],)).fetchone()
            iid = r[0] if r else None
        if iid is None:
            r = db.execute("""select i.itemID from items i join itemData x on x.itemID=i.itemID and x.fieldID=? join itemDataValues v using(valueID)
                              where v.value=? and i.itemTypeID<>? and i.itemID not in (select itemID from deletedItems)""",
                           (fid['title'], d['title'], att_type)).fetchone()
            iid = r[0] if r else None
        if iid is not None:
            reused += 1
        else:
            iid = newitem(doc_type)
            setfield(iid, 'title', d['title'])
            if d['year']:
                setfield(iid, 'date', f"{d['year']}-00-00 {d['year']}")
            extra = '\n'.join(x for x in (f"DOI: {d['doi']}" if d['doi'] else '', d['extra']) if x)
            if d['doi']:
                setfield(iid, 'url', 'https://doi.org/' + d['doi'])
            if extra:
                setfield(iid, 'extra', extra)
            for n, c in enumerate(d['creators']):
                if 'name' in c:
                    first, last, mode = None, c['name'], 1
                else:
                    first, last, mode = c['firstName'], c['lastName'], 0
                r = db.execute('select creatorID from creators where lastName=? and firstName is ? and fieldMode=?', (last, first, mode)).fetchone()
                cid = r[0] if r else db.execute('insert into creators(firstName, lastName, fieldMode) values(?,?,?)', (first, last, mode)).lastrowid
                db.execute('insert into itemCreators(itemID, creatorID, creatorTypeID, orderIndex) values(?,?,?,?)', (iid, cid, author, n))
            created += 1
        if not db.execute('select 1 from collectionItems where collectionID=? and itemID=?', (coll, iid)).fetchone():
            nxt = db.execute('select coalesce(max(orderIndex)+1,0) from collectionItems where collectionID=?', (coll,)).fetchone()[0]
            db.execute('insert into collectionItems(collectionID, itemID, orderIndex) values(?,?,?)', (coll, iid, nxt))
        path = str(refs / d['file'])
        if db.execute('select 1 from itemAttachments where parentItemID=? and linkMode=2 and path=?', (iid, path)).fetchone():
            had += 1; continue
        aid = newitem(att_type)
        db.execute('insert into itemAttachments(itemID, parentItemID, linkMode, contentType, path, syncState) values(?,?,2,?,?,0)',
                   (aid, iid, 'application/pdf', path))
        setfield(aid, 'title', d['file'][:-4])
        linked += 1
        db.execute('update items set dateModified=?, clientDateModified=?, synced=0 where itemID=?', (now, now, iid))
print(f'items created {created}, existing reused {reused}; PDFs linked {linked}, already linked {had}')
