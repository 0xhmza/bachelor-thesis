"""Build literature_new/: polished copies of the reading PDFs, the Methods
Digest volumes and a tex backup, plus the index that links PDFs to Zotero.

Usage: python build.py            (after catalogue.py has written output/catalogue.json)
Reads only files that are already in the repository; downloads nothing.
"""
import csv, json, pathlib, shutil, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from names import OVERRIDES, label, polished, surname

here = pathlib.Path(__file__).parent
root = here.parents[2]
lit = root / '01_Literature'
dest = root / 'literature_new'
refs = dest / 'references'
ana = dest / 'literature methodology analysis'

# Known-bad file: 04_Coding/74_Braun is a different paper (a lung-cancer study from HAL);
# the correct Braun & Clarke (2006) is the copy in 12_Additions.
EXCLUDE = {'01_Literature/PDFs/Methods-Reading/04_Coding/74_Braun_2006_Using-thematic-analysis-in-psychology.pdf'}

cat = json.loads((here / 'output/catalogue.json').read_text(encoding='utf-8'))
cat = [m for m in cat if m['path'] not in EXCLUDE]

def rank(m):  # prefer the numbered Methods-Reading copy over the loose top-level duplicate
    return (0 if 'Methods-Reading' in m['path'] else 1, m['path'])

reg = json.loads((lit / 'Methods-Digest/registry.json').read_text(encoding='utf-8'))
reglabel = {pathlib.PureWindowsPath(e['pdf']).as_posix(): e['label'].replace('(', '').replace(')', '').replace('’', "'")
            for e in reg if e.get('pdf')}
unique = {}
for m in sorted(cat, key=rank):
    unique.setdefault(m['sha'], m)

krip = lit / 'Methods-Digest/private/22_Krippendorff_2019_Content-Analysis-4e.pdf'
rows, used = [], {}
items = list(unique.values())
for m in items:
    fn = pathlib.PurePosixPath(m['path']).name
    if fn in OVERRIDES:
        lbl, title = OVERRIDES[fn]
        title = title or m['title']
    elif m['src'] == 'registry':
        lbl, title = reglabel[m['path']], m['title']
    elif m['src'] == 'records':
        raise SystemExit(f'no label for {fn}')
    else:
        raise SystemExit(f'no name for {fn}')
    lbl = lbl.replace('’', "'")
    name = polished(lbl, title)
    if name in used:
        name = name[:-4] + f' ({used[name] + 1}).pdf'
    used[name] = used.get(name, 0) + 1
    rows.append(dict(file=name, label=lbl, title=title, doi=m.get('doi') or '', zotero=m.get('zotero') or '',
                     authors=m.get('authors') or '', year=m.get('year'), source=m['path']))

if krip.exists():
    lbl, title = OVERRIDES[krip.name]
    rows.append(dict(file=polished(lbl, title), label=lbl, title=title, doi='', zotero='', authors='H. Krippendorff', year=2019,
                     source=krip.relative_to(root).as_posix()))

if '--dry' in sys.argv:
    for r in sorted(rows, key=lambda r: r['file']):
        print(r['file'])
    print(len(rows))
    raise SystemExit

refs.mkdir(parents=True, exist_ok=True)
for r in rows:
    shutil.copy2(root / r['source'], refs / r['file'])

with open(here / 'output/references-index.json', 'w', encoding='utf-8') as f:
    json.dump(sorted(rows, key=lambda r: r['file']), f, indent=1, ensure_ascii=False)
print(len(rows), 'references copied')
