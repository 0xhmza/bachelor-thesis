"""Apply the 01_Literature reorganisation planned by plan.py. Writes mapping.csv (old path -> new path / deleted).

Usage: python apply.py plan.csv [--dry]
Target layout:
  01_Literature/{README.md, library/, notes/, catalog/, review/, digest/}
"""
import csv, os, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
os.chdir(ROOT)
plan_file, dry = sys.argv[1], '--dry' in sys.argv
L = '01_Literature/'
HERE = Path(__file__).parent

tracked = subprocess.run(['git', 'ls-files', '-z', L, 'literature_new'], capture_output=True, text=True).stdout.split('\0')
tracked = [t for t in tracked if t]
all_files = [str(p).replace('\\', '/') for base in (L, 'literature_new') for p in Path(base).rglob('*') if p.is_file()]

mapping = {}   # old -> new path, or None when the file is dropped
ops = []       # (kind, src, dst)

# ---- library -----------------------------------------------------------------------------------------
plan = list(csv.DictReader(open(plan_file, encoding='utf-8')))
for r in plan:
    if not r['new_name']:                       # wrong paper
        for p in r['remove'].split('|') + [r['keep']]:
            if p: mapping[p] = None
        continue
    dst = L + 'library/' + r['new_name']
    keep = r['keep']
    if r['new_name'].startswith('Krippendorff_2019'):
        ops.append(('copy', keep, dst))         # the digest build still needs its own private copy
        mapping[keep] = dst
    else:
        ops.append(('move', keep, dst)); mapping[keep] = dst
    for p in r['remove'].split('|'):
        if p:
            mapping[p] = dst
            ops.append(('delete', p, None))

# ---- digest volumes (kept once, in digest/volumes) -----------------------------------------------------------
VOL = {'00_Methods-Digest_complete.pdf': 'MethodsDigest_Complete.pdf'}
for p in all_files:
    if p.startswith(L + 'AI Literature Analysis/') and p.endswith('.pdf'):
        b = Path(p).name
        m = re.match(r'(\d)_([A-Z])_(.+)\.pdf$', b)
        new = VOL.get(b) or (f"MethodsDigest_Stage{m.group(1)}{m.group(2)}_{''.join(w.capitalize() for w in m.group(3).split('-'))}.pdf")
        mapping[p] = L + 'digest/volumes/' + new
        ops.append(('move', p, L + 'digest/volumes/' + new))
        for q in all_files:
            if q.endswith('.pdf') and (q.startswith(L + 'PDFs/AI Literature Analysis/') or q.startswith('literature_new/literature methodology analysis/')) \
               and re.search(re.escape(b[:3]) if False else '', q) is None:
                pass
# duplicates of the volumes elsewhere are dropped below by prefix

# ---- non-PDF files -------------------------------------------------------------------------------------------
ROOTMOVE = {
    L + 'README.md': L + 'README.md',
    L + 'reading-status.csv': L + 'catalog/reading-status.csv',
    L + 'literature-index.json': L + 'catalog/literature-index.json',
    L + 'Literature-Map.html': L + 'catalog/Literature-Map.html',
    L + 'methodology-literature.json': L + 'catalog/methods-corpus.json',
    L + 'Methods-Reading-List.md': L + 'catalog/Methods-Reading-List.md',
    L + 'Literature-Gap-Search_2026-10-23.md': L + 'review/Gap-Search_2026-10-23.md',
    L + 'PDFs/Methodology-Audit_2026-11-04/README.md': L + 'catalog/Audit-Sources_2026-11-04.md',
    L + 'Notes/.gitkeep': L + 'notes/.gitkeep',
}
DROPPED_PREFIX = (L + '.tex/', L + '#_Junk_Backup/', 'literature_new/', L + 'AI Literature Analysis/README.md',
                  L + 'PDFs/')
DROPPED_FILES = {L + 'Download-Checklist.md', L + 'Methods-Reading-List.html', L + 'ranked-dois.txt'}
for p in all_files:
    if p in mapping:
        continue
    if p in ROOTMOVE:
        mapping[p] = ROOTMOVE[p]
        if p != ROOTMOVE[p]: ops.append(('move', p, ROOTMOVE[p]))
    elif p.startswith(L + 'Methods-Digest/'):
        mapping[p] = L + 'digest/' + p[len(L + 'Methods-Digest/'):]       # directory rename done at the end
    elif p.startswith(L + 'Literature-Review/'):
        mapping[p] = L + 'review/' + p[len(L + 'Literature-Review/'):]
    elif p in DROPPED_FILES or p.startswith(DROPPED_PREFIX):
        mapping[p] = None
    else:
        print('UNMAPPED', p)

unmapped = [p for p in all_files if p not in mapping]
pdf_unplanned = [p for p, v in mapping.items() if v is None and p.endswith('.pdf')
                 and not (p.startswith(L + '.tex/') or p.startswith(L + 'PDFs/AI Literature') or p.startswith('literature_new/literature methodology')
                          or p.startswith(L + 'PDFs/Methods-Reading/04_Coding/74_Braun'))]
print(len(all_files), 'files;', len(unmapped), 'unmapped;', 'PDFs dropped without a planned copy:', pdf_unplanned)
if unmapped or pdf_unplanned:
    sys.exit('stop: unmapped files')

with open(HERE / 'mapping.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh); w.writerow(['old', 'new'])
    for k in sorted(mapping):
        if k.endswith('.pdf') or not (k.startswith(L + 'Methods-Digest/') or k.startswith(L + 'Literature-Review/') or k.startswith('literature_new/') or k.startswith(L + '.tex/') or k.startswith(L + '#_Junk')):
            w.writerow([k, mapping[k] or ''])
print('mapping.csv written;', len(ops), 'file operations')
if dry:
    sys.exit(0)

# ---- execute ---------------------------------------------------------------------------------------------------
def mk(p): Path(p).parent.mkdir(parents=True, exist_ok=True)
for kind, src, dst in ops:
    if kind in ('move', 'copy'):
        mk(dst)
        if Path(dst).exists(): sys.exit('exists: ' + dst)
        (shutil.move if kind == 'move' else shutil.copy2)(src, dst)
    elif kind == 'delete' and Path(src).exists():
        os.remove(src)
# audit README before PDFs/ goes
for old, new in ROOTMOVE.items():
    if old != new and Path(old).exists():
        mk(new); shutil.move(old, new)
for d in (L + '.tex', L + '#_Junk_Backup', L + 'PDFs', L + 'AI Literature Analysis', 'literature_new'):
    if Path(d).exists(): shutil.rmtree(d)
for f in DROPPED_FILES:
    if Path(f).exists(): os.remove(f)
for old, new in ((L + 'Methods-Digest', L + 'digest'), (L + 'Literature-Review', L + 'review')):
    if Path(new).exists():                       # digest/volumes was created by the moves above
        for item in Path(old).iterdir():
            shutil.move(str(item), str(Path(new) / item.name))
        Path(old).rmdir()
    else:
        shutil.move(old, new)
if Path(L + 'Notes').exists(): shutil.rmtree(L + 'Notes')
print('done')
