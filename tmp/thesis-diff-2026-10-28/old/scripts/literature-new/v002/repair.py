"""Clean Zotero: link every PDF of literature_new/references to ONE item, no duplicates.

Replaces v001/apply_links.py. Zotero MUST be closed; a backup is made first.
  1. Remove what v001 added (items whose key is not in the pre-v001 backup, and its collection rows).
  2. PDFs that match an existing item (match.py) are attached to it as linked files.
  3. Thesis items (collection "Bachelor Thesis References") get the full author list from
     _shared/references.bib and an abstract where the repo holds one.
  4. PDFs without an existing item become new items in the collection "Methodology literature"
     (never in the thesis collection), with type, venue, DOI, authors and abstract where known.
Usage: python repair.py <zotero.sqlite> <pre-v001-backup.sqlite> [--dry]
"""
import csv, json, pathlib, random, re, shutil, sqlite3, sys, time, unicodedata
from datetime import datetime, timezone

here = pathlib.Path(__file__).parent
root = here.parents[2]
sys.path.insert(0, str(here))
sys.path.insert(0, str(here.parent / 'v001'))
from match import norm
from names import surname

refs = root / 'literature_new' / 'references'
idx = json.loads((here.parent / 'v001/output/references-index.json').read_text(encoding='utf-8'))
matches = json.loads((here / 'output/matches.json').read_text(encoding='utf-8'))
dbp, bakp, dry = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), '--dry' in sys.argv

if not dry:
    bak = dbp.with_name(f'{dbp.name}.before-repair-{time.strftime("%Y%m%d-%H%M%S")}')
    shutil.copy2(dbp, bak); print('backup:', bak)
db = sqlite3.connect(dbp)
db.execute('pragma foreign_keys=on')
old = sqlite3.connect(f'file:{bakp}?mode=ro', uri=True)
now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
ALPHA = '23456789ABCDEFGHIJKLMNPQRSTUVWXYZ'

# ---- sources of metadata inside the repo -------------------------------------------------
registry = {norm(e['title']): e for e in json.loads((root / '01_Literature/Methods-Digest/registry.json').read_text(encoding='utf-8'))}
meth = {}
for r in json.loads((root / '01_Literature/methodology-literature.json').read_text(encoding='utf-8'))['ranked_doi_records']:
    meth[(r['doi'] or '').lower()] = r
records = {}
for r in csv.DictReader(open(root / '05_Data/Literature Search/26. Oct/records.csv', encoding='utf-8')):
    records[norm(r['title'])] = r
    if r['doi']:
        records[r['doi'].lower()] = r
lit_index = {}
for it in json.loads((root / '01_Literature/literature-index.json').read_text(encoding='utf-8'))['items']:
    if it.get('abstract'):
        lit_index[(it.get('doi') or '').lower()] = it['abstract']
        lit_index[norm(it['title'])] = it['abstract']

def clean(s):
    return unicodedata.normalize('NFC', s or '').replace('�', '').strip()

def abstract_for(title, doi):
    for k in ((doi or '').lower(), norm(title)):
        if k and k in lit_index:
            return clean(lit_index[k])
    r = records.get((doi or '').lower()) or records.get(norm(title))
    if r and r.get('abstract'):
        return clean(r['abstract'])
    m = meth.get((doi or '').lower())
    return clean(m['abstract']) if m and m.get('abstract') else ''

# ---- bib parsing ---------------------------------------------------------------------------
def split_top(s, sep=' and '):
    out, depth, cur, i = [], 0, '', 0
    while i < len(s):
        if s[i] == '{': depth += 1
        elif s[i] == '}': depth -= 1
        if depth == 0 and s[i:i + len(sep)] == sep:
            out.append(cur); cur = ''; i += len(sep); continue
        cur += s[i]; i += 1
    return out + [cur]

def bib_authors(body):
    m = re.search(r'^\s*author\s*=\s*\{', body, re.M)
    if not m: return []
    i, depth, j = m.end(), 1, m.end()
    while depth:
        depth += {'{': 1, '}': -1}.get(body[j], 0); j += 1
    raw = re.sub(r'\s+', ' ', body[i:j - 1]).strip()
    out = []
    for a in split_top(raw):
        a = a.strip()
        if a in ('others', ''): continue
        if a.startswith('{') and a.endswith('}'):
            out.append(dict(name=a[1:-1].strip()))
        else:
            parts = [p.strip().replace('{', '').replace('}', '') for p in a.split(',')]
            out.append(dict(last=parts[0], first=parts[1] if len(parts) > 1 else '') if len(parts) > 1 else
                       dict(last=a.replace('{', '').replace('}', ''), first=''))
    return out

bib = (root / '_shared/references.bib').read_text(encoding='utf-8')
bib_by_key = {m.group(2).strip(): bib_authors(m.group(3)) for m in re.finditer(r'^@(\w+)\{([^,]+),(.*?)(?=^@|\Z)', bib, re.S | re.M)}

# ---- helpers -------------------------------------------------------------------------------
def newkey():
    while True:
        k = ''.join(random.choice(ALPHA) for _ in range(8))
        if not db.execute('select 1 from items where key=? and libraryID=1', (k,)).fetchone() and \
           not db.execute('select 1 from collections where key=? and libraryID=1', (k,)).fetchone():
            return k

fid = {n: db.execute('select fieldID from fields where fieldName=?', (n,)).fetchone()[0]
       for n in ('title', 'date', 'url', 'extra', 'DOI', 'publicationTitle', 'proceedingsTitle', 'abstractNote', 'citationKey')}
tid = {n: db.execute('select itemTypeID from itemTypes where typeName=?', (n,)).fetchone()[0]
       for n in ('document', 'attachment', 'journalArticle', 'conferencePaper')}
author_t = db.execute("select creatorTypeID from creatorTypes where creatorType='author'").fetchone()[0]

def setfield(iid, name, value):
    v = db.execute('select valueID from itemDataValues where value=?', (value,)).fetchone()
    vid = v[0] if v else db.execute('insert into itemDataValues(value) values(?)', (value,)).lastrowid
    db.execute('insert or replace into itemData(itemID, fieldID, valueID) values(?,?,?)', (iid, fid[name], vid))

def getfield(iid, name):
    r = db.execute('select v.value from itemData x join itemDataValues v using(valueID) where x.itemID=? and x.fieldID=?', (iid, fid[name])).fetchone()
    return r[0] if r else None

def newitem(type_id):
    return db.execute('insert into items(itemTypeID, dateAdded, dateModified, clientDateModified, libraryID, key, synced) values(?,?,?,?,1,?,0)',
                      (type_id, now, now, now, newkey())).lastrowid

def touch(iid):
    db.execute('update items set dateModified=?, clientDateModified=?, synced=0 where itemID=?', (now, now, iid))

def set_creators(iid, creators):
    db.execute('delete from itemCreators where itemID=?', (iid,))
    for n, c in enumerate(creators):
        first, last, mode = (None, c['name'], 1) if 'name' in c else (c['first'], c['last'], 0)
        r = db.execute('select creatorID from creators where lastName=? and firstName is ? and fieldMode=?', (last, first, mode)).fetchone()
        cid = r[0] if r else db.execute('insert into creators(firstName, lastName, fieldMode) values(?,?,?)', (first, last, mode)).lastrowid
        db.execute('insert into itemCreators(itemID, creatorID, creatorTypeID, orderIndex) values(?,?,?,?)', (iid, cid, author_t, n))

def creators_of(iid):
    return [(r[0], r[1]) for r in db.execute('select lastName, firstName from itemCreators ic join creators c using(creatorID) where itemID=? order by orderIndex', (iid,))]

def person(n):
    n = clean(n)
    if ',' in n:
        last, first = [p.strip() for p in n.split(',', 1)]
        return dict(first=first, last=last)
    last = surname(n)
    if last != n:
        return dict(first=n[:len(n) - len(last)].strip(), last=last)
    parts = n.rsplit(' ', 1)
    return dict(first=parts[0], last=parts[1]) if len(parts) == 2 else dict(first='', last=n)

CONF = re.compile(r'proceedings|conference|symposium|workshop|\bCHI\b|usenix|popets|\bACL\b|emnlp|naacl|neurips|\bCCS\b|usec|hcomp|lrec|\bSOUPS\b|companion', re.I)

stats = dict(removed=0, linked=0, enriched_creators=0, abstracts=0, created=0, incomplete=0)
with db:
    # 1. undo v001 ------------------------------------------------------------------------------
    keep = {r[0] for r in old.execute('select key from items')}
    gone = [r[0] for r in db.execute('select itemID, key from items') if r[1] not in keep] if False else \
           [r[0] for r in db.execute('select itemID from items where key not in (%s)' % ','.join('?' * len(keep)), list(keep))]
    for i in gone:
        db.execute('delete from items where itemID=?', (i,))
    stats['removed'] = len(gone)
    db.execute("delete from collectionItems where collectionID in (select collectionID from collections where collectionName='Methodology literature')")
    db.execute('delete from creators where creatorID not in (select creatorID from itemCreators)')
    db.execute('delete from itemDataValues where valueID not in (select valueID from itemData)')
    thesis = db.execute("select collectionID from collections where collectionName='Bachelor Thesis References'").fetchone()[0]
    row = db.execute("select collectionID from collections where collectionName='Methodology literature'").fetchone()
    mcoll = row[0] if row else db.execute('insert into collections(collectionName, clientDateModified, libraryID, key, synced) values(?,?,1,?,0)',
                                          ('Methodology literature', now, newkey())).lastrowid

    def add_to(coll, iid):
        if not db.execute('select 1 from collectionItems where collectionID=? and itemID=?', (coll, iid)).fetchone():
            nxt = db.execute('select coalesce(max(orderIndex)+1,0) from collectionItems where collectionID=?', (coll,)).fetchone()[0]
            db.execute('insert into collectionItems(collectionID, itemID, orderIndex) values(?,?,?)', (coll, iid, nxt))

    def attach(iid, fname):
        path = str(refs / fname)
        aid = newitem(tid['attachment'])
        db.execute('insert into itemAttachments(itemID, parentItemID, linkMode, contentType, path, syncState) values(?,?,2,?,?,0)',
                   (aid, iid, 'application/pdf', path))
        setfield(aid, 'title', fname[:-4])
        touch(iid)
        stats['linked'] += 1

    # 2./4. link or create -------------------------------------------------------------------
    for e in idx:
        hit = matches[e['file']]
        assert len(hit) <= 1, (e['file'], hit)
        if hit:
            iid = db.execute('select itemID from items where key=?', (hit[0][0],)).fetchone()[0]
        else:
            reg = registry.get(norm(e['title']))
            rec = records.get(norm(e['title'])) or records.get((e['doi'] or '').lower())
            venue = clean((reg or {}).get('venue') or (rec or {}).get('venue') or '')
            doi = (e['doi'] or (rec or {}).get('doi') or '').lower()
            typ = 'document'
            if venue and 'arxiv' not in venue.lower() and 'ssrn' not in venue.lower():
                typ = 'conferencePaper' if CONF.search(venue) else 'journalArticle'
            iid = newitem(tid[typ])
            setfield(iid, 'title', clean(e['title']))
            if e['year']: setfield(iid, 'date', f"{e['year']}-00-00 {e['year']}")
            extra = []
            if doi:
                if typ == 'document': extra.append('DOI: ' + doi)
                else: setfield(iid, 'DOI', doi)
                setfield(iid, 'url', 'https://doi.org/' + doi)
            if venue:
                if typ == 'conferencePaper': setfield(iid, 'proceedingsTitle', venue)
                elif typ == 'journalArticle': setfield(iid, 'publicationTitle', venue)
                else: extra.append('Venue: ' + venue)
            ab = abstract_for(e['title'], doi)
            if ab: setfield(iid, 'abstractNote', ab)
            cr = None
            m = meth.get(doi)
            if m and isinstance(m.get('authors'), list) and m['authors']:
                cr = [dict(first=a['given'], last=a['family']) if a.get('family') else person(a['name']) for a in m['authors'] if a.get('family') or a.get('name')]
            elif e['authors'] and 'et al' not in e['authors'] and 'None' not in e['authors']:
                names = [x.strip() for x in re.split(r',\s*', e['authors']) if x.strip()]
                cr = [person(n) for n in names]
            if not cr and e['authors'] and ' ' in e['authors'] and 'et al' not in e['authors'] and ',' not in e['authors'] and 'None' not in e['authors']:
                cr = [person(e['authors'])]
            if not cr or (len(cr) == 1 and e['label'].split(' ')[0] != cr[0]['last'].split(' ')[0] and ' et al' in e['label']):
                first = re.split(r' et al\.| &', e['label'].rsplit(' ', 1)[0])[0]
                cr = [dict(first='', last=first)]
                extra.append('Author list incomplete: first author only; see the PDF.')
                stats['incomplete'] += 1
            if re.match(r'(APA|BfArM|Article 29)', e['label']):
                cr = [dict(name={'APA': 'American Psychiatric Association', 'BfArM': 'Bundesinstitut für Arzneimittel und Medizinprodukte (BfArM)',
                                 'Article': 'Article 29 Data Protection Working Party'}[e['label'].split(' ')[0]])]
                extra = [x for x in extra if not x.startswith('Author list')]
            set_creators(iid, cr)
            if extra: setfield(iid, 'extra', '\n'.join(extra))
            stats['created'] += 1
            add_to(mcoll, iid)
        if not db.execute('select 1 from itemAttachments where parentItemID=? and linkMode=2 and path=?', (iid, str(refs / e['file']))).fetchone():
            attach(iid, e['file'])
        if hit:
            add_to(mcoll, iid)  # the methods collection lists every item that has a PDF here

    # 3. enrich thesis items from the bib --------------------------------------------------------
    for iid, key in db.execute('select i.itemID, v.value from collectionItems ci join items i using(itemID) join itemData x on x.itemID=i.itemID '
                               'join itemDataValues v using(valueID) where ci.collectionID=? and x.fieldID=?', (thesis, fid['citationKey'])).fetchall():
        auth = bib_by_key.get(key)
        if auth:
            cur = creators_of(iid)
            if len(cur) != len(auth) or any(a.get('last', a.get('name')) != c[0] for a, c in zip(auth, cur)):
                set_creators(iid, auth); touch(iid); stats['enriched_creators'] += 1
        if not getfield(iid, 'abstractNote'):
            ab = abstract_for(getfield(iid, 'title'), getfield(iid, 'DOI'))
            if ab:
                setfield(iid, 'abstractNote', ab); touch(iid); stats['abstracts'] += 1
    if dry:
        db.rollback()
print(stats)
