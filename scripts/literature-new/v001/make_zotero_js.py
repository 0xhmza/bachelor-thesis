"""Generate a Zotero 'Run JavaScript' snippet that links each PDF in
literature_new/references/ to a Zotero item as a linked file (a pointer, the
PDF is not copied into Zotero storage).

Existing items are matched by DOI or title (catalogue.py); the others are created
as 'document' items with the metadata of the reference index, and every item is
added to the collection "Methodology literature". Re-running is safe: items and
attachments that already exist are reused.

Usage: python make_zotero_js.py      (after build.py)
Output: output/link_pdfs.js (git-ignored)
"""
import json, pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from names import surname

here = pathlib.Path(__file__).parent
root = here.parents[2]
refs = root / 'literature_new' / 'references'
idx = json.loads((here / 'output/references-index.json').read_text(encoding='utf-8'))

def creators(e):
    a = e['authors']
    if a and 'et al' not in a and ',' not in a and a.count(' ') >= 3:  # organisation
        return [{'name': a, 'creatorType': 'author'}]
    if a and 'et al' not in a and e['label'].split()[0] in ('BfArM', 'APA', 'Article'):
        return [{'name': a or e['label'], 'creatorType': 'author'}]
    names = [x.strip() for x in re.split(r',\s*', a) if x.strip() and x.strip() != 'None'] if a and 'et al' not in a else []
    if not names:  # only the label is known: first author surname, rest on the PDF
        first = re.split(r' et al\.| &', e['label'].rsplit(' ', 1)[0])[0]
        return [{'firstName': '', 'lastName': first, 'creatorType': 'author'}]
    out = []
    for n in names:
        last = surname(n)
        first = n[: len(n) - len(last)].strip() if n.endswith(last) else ''
        out.append({'firstName': first, 'lastName': last, 'creatorType': 'author'})
    return out

data = []
for e in idx:
    data.append({
        'file': e['file'], 'title': e['title'], 'year': e['year'], 'doi': e['doi'],
        'key': e['zotero'], 'creators': creators(e),
        'extra': ('' if e['authors'] and 'et al' not in e['authors'] else
                  'Author list incomplete: first author only; see the PDF.')
    })

(here / 'output/zotero-data.json').write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding='utf-8')
base = str(refs).replace('/', '\\') + '\\'
js = r"""// Links each PDF in literature_new/references as a linked-file attachment (pointer).
const base = %s;
const data = %s;
const lib = Zotero.Libraries.userLibraryID;
const collName = 'Methodology literature';
let coll = Zotero.Collections.getByLibrary(lib).find(c => c.name === collName);
if (!coll) { coll = new Zotero.Collection({ name: collName, libraryID: lib }); await coll.saveTx(); }
const norm = s => (s || '').toLowerCase().replace(/[^a-z0-9]+/g, '');
let created = 0, reused = 0, linked = 0, had = 0, failed = [];
for (const d of data) {
  try {
    let item = d.key ? Zotero.Items.getByLibraryAndKey(lib, d.key) : null;
    if (!item) {
      const s = new Zotero.Search(); s.libraryID = lib;
      s.addCondition('title', 'is', d.title); s.addCondition('itemType', 'isNot', 'attachment');
      const ids = await s.search();
      item = ids.length ? Zotero.Items.get(ids[0]) : null;
    }
    if (item) reused++;
    else {
      item = new Zotero.Item('document'); item.libraryID = lib;
      item.setField('title', d.title);
      if (d.year) item.setField('date', String(d.year));
      if (d.doi) { item.setField('url', 'https://doi.org/' + d.doi); item.setField('extra', ['DOI: ' + d.doi, d.extra].filter(Boolean).join('\n')); }
      else if (d.extra) item.setField('extra', d.extra);
      item.setCreators(d.creators);
      await item.saveTx(); created++;
    }
    if (!item.inCollection(coll.id)) { item.addToCollection(coll.id); await item.saveTx(); }
    const path = base + d.file;
    const already = item.getAttachments().map(id => Zotero.Items.get(id)).some(a => a.attachmentLinkMode === Zotero.Attachments.LINK_MODE_LINKED_FILE && a.attachmentPath === path);
    if (already) { had++; continue; }
    await Zotero.Attachments.linkFromFile({ file: Zotero.File.pathToFile(path), parentItemID: item.id });
    linked++;
  } catch (e) { failed.push(d.file + ': ' + e); }
}
return `items created ${created}, existing reused ${reused}; PDFs linked ${linked}, already linked ${had}; failed ${failed.length}\n` + failed.join('\n');
""" % (json.dumps(base), json.dumps(data, ensure_ascii=False, indent=0))
(here / 'output/link_pdfs.js').write_text(js, encoding='utf-8')
print(len(data), 'entries;', sum(1 for d in data if d['key']), 'existing items;', len(js), 'chars')
