"""Point Zotero's linked PDF attachments at their new place in 01_Literature/library/.

Why: the literature reorganisation of 5 November 2026 moved every PDF (and deleted literature_new/). Zotero stores
linked files by absolute path (itemAttachments.path, linkMode 2), so those links break until they are updated.

Usage (Zotero MUST be closed; run on the PC that holds zotero.sqlite):
    python relink_zotero.py <path to zotero.sqlite>            # dry run: counts only
    python relink_zotero.py <path to zotero.sqlite> --apply    # backs the database up, then updates

The old -> new table is mapping.csv in this folder. Paths are matched case-insensitively with either slash style
and the repository root of the machine this script runs on.
"""
import csv, pathlib, shutil, sqlite3, sys, time

here = pathlib.Path(__file__).resolve().parent
root = here.parents[2]
db_path = pathlib.Path(sys.argv[1])
apply = '--apply' in sys.argv


def norm(p):
    return str(p).replace('/', '\\').lower()


table = {}
for r in csv.DictReader(open(here / 'mapping.csv', encoding='utf-8')):
    if r['new'].endswith('.pdf'):
        table[norm(root / r['old'])] = str(root / r['new'])

if apply:
    backup = db_path.with_name(f'{db_path.name}.before-relink-{time.strftime("%Y%m%d-%H%M%S")}')
    shutil.copy2(db_path, backup)
    print('backup:', backup)
db = sqlite3.connect(db_path, timeout=2)
try:
    rows = db.execute('select itemID, path from itemAttachments where linkMode=2 and path is not null').fetchall()
except sqlite3.OperationalError as e:
    sys.exit(f'cannot read the database ({e}); close Zotero and retry')

todo, missing, other = [], [], 0
for item_id, path in rows:
    if norm(path) in table:
        todo.append((item_id, table[norm(path)]))
    elif path.lower().startswith(('attachments:', 'storage:')):
        other += 1
    elif 'bachelor-thesis' in path.lower():
        missing.append(path)
print(f'{len(rows)} linked files; {len(todo)} to update; {len(missing)} inside the repository but not in the table; '
      f'{other} stored relative to a base directory (not touched)')
for p in missing[:10]:
    print('  not in table:', p)
if apply:
    for item_id, new in todo:
        db.execute('update itemAttachments set path=? where itemID=?', (new, item_id))
    db.commit()
    print('updated', len(todo))
else:
    print('dry run: nothing written; add --apply to update')
