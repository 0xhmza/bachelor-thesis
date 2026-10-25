"""Generate a Zotero 'Run JavaScript' snippet that pins the keys of
_shared/references.bib into each matched item's Extra field
("Citation Key: <key>"), which Better BibTeX honours over its own formula.

Usage: python make_pin_script.py <copy-of-zotero.sqlite>
Matches by DOI, then by title. Output: output/pin_keys.js (git-ignored).
"""
import re, sqlite3, sys, json, pathlib

here = pathlib.Path(__file__).parent
root = here.parents[2]
db = sqlite3.connect(f'file:{sys.argv[1]}?mode=ro', uri=True)
Q = """select i.itemID, i.key,
 max(case when f.fieldName='title' then v.value end),
 max(case when f.fieldName='DOI' then v.value end)
 from items i join itemTypes it using(itemTypeID)
 left join itemData d on d.itemID=i.itemID left join fields f using(fieldID)
 left join itemDataValues v using(valueID)
 where i.itemID not in (select itemID from deletedItems)
   and it.typeName not in ('attachment','note','annotation')
 group by i.itemID"""
rows = db.execute(Q).fetchall()

def norm(s): return re.sub(r'[^a-z0-9]+', '', (s or '').lower())

bib = (root / '_shared/references.bib').read_text(encoding='utf-8')
mapping, problems = {}, []
for m in re.finditer(r'^@(\w+)\{([^,]+),(.*?)(?=^@|\Z)', bib, re.S | re.M):
    key, body = m.group(2).strip(), m.group(3)
    def fld(n):
        mm = re.search(r'^\s*' + n + r'\s*=\s*[{"](.*?)[}"],?\s*$', body, re.S | re.M | re.I)
        return mm.group(1).replace('{', '').replace('}', '') if mm else None
    doi, title = fld('doi'), norm(fld('title'))
    hit = next((r for r in rows if doi and r[3] and doi.lower() == r[3].lower()), None)
    if not hit:
        hit = next((r for r in rows if title and norm(r[2]) and
                    (title == norm(r[2]) or (len(norm(r[2])) >= 30 and title.startswith(norm(r[2])[:40])))), None)
    if not hit:
        problems.append(f'no Zotero item for {key}'); continue
    if hit[1] in mapping:
        problems.append(f'{key} and {mapping[hit[1]]} hit the same item {hit[1]}'); continue
    mapping[hit[1]] = key

js = r"""// Pins the thesis citation keys into Extra ("Citation Key: ...").
const map = %s;
const lib = Zotero.Libraries.userLibraryID;
let done = 0, same = 0, missing = [];
for (const [itemKey, ck] of Object.entries(map)) {
  const item = Zotero.Items.getByLibraryAndKey(lib, itemKey);
  if (!item) { missing.push(ck); continue; }
  const lines = item.getField('extra').split('\n').filter(l => !/^citation key\s*:/i.test(l));
  lines.unshift('Citation Key: ' + ck);
  const extra = lines.join('\n');
  if (extra === item.getField('extra')) { same++; continue; }
  item.setField('extra', extra);
  await item.saveTx();
  done++;
}
return `pinned ${done}, unchanged ${same}, missing ${missing.length}: ${missing.join(', ')}`;
""" % json.dumps(mapping, indent=1)
out = here / 'output'; out.mkdir(exist_ok=True)
(out / 'pin_keys.js').write_text(js, encoding='utf-8')
print(len(mapping), 'mapped;', len(problems), 'problems'); print(*problems, sep='\n')
