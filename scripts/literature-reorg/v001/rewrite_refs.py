"""Rewrite every reference to the old 01_Literature layout: exact file paths (mapping.csv), folder prefixes and
relative Markdown links. Usage: python rewrite_refs.py [--dry]"""
import csv, os, re, subprocess, sys, urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
os.chdir(ROOT)
dry = '--dry' in sys.argv
L = '01_Literature/'
mapping = {r['old']: r['new'] for r in csv.DictReader(open(Path(__file__).parent / 'mapping.csv', encoding='utf-8'))}

ROOTMOVE = {
    'reading-status.csv': 'catalog/reading-status.csv', 'literature-index.json': 'catalog/literature-index.json',
    'Literature-Map.html': 'catalog/Literature-Map.html', 'methodology-literature.json': 'catalog/methods-corpus.json',
    'Methods-Reading-List.md': 'catalog/Methods-Reading-List.md', 'Literature-Gap-Search_2026-10-23.md': 'review/Gap-Search_2026-10-23.md',
}
PREFIX = [(L + 'PDFs/Methodology-Audit_2026-11-04/README.md', L + 'catalog/Audit-Sources_2026-11-04.md'),
          (L + 'Methods-Digest', L + 'digest'), (L + 'Literature-Review', L + 'review'), (L + 'Notes', L + 'notes'),
          (L + 'PDFs/AI Literature Analysis', L + 'digest/volumes'), (L + 'PDFs/Methods-Reading', L + 'library'),
          (L + 'PDFs', L + 'library'), ('literature_new/references', L + 'library')]
PREFIX += [(L + k, L + v) for k, v in ROOTMOVE.items()]
DROPPED = {L + 'Download-Checklist.md', L + 'Methods-Reading-List.html', L + 'ranked-dois.txt'}


def new_of(old):
    """Old repo-relative path -> new repo-relative path (unchanged when not affected)."""
    if old in mapping and mapping[old]:
        return mapping[old]
    for a, b in PREFIX:
        if old == a or old.startswith(a + '/'):
            return b + old[len(a):]
    return old


def old_of(cur):
    """Current location of a file -> where it lived before (for resolving its relative links)."""
    for new, old in ((L + 'digest', L + 'Methods-Digest'), (L + 'review', L + 'Literature-Review')):
        if cur.startswith(new + '/') and not cur.startswith(L + 'digest/volumes/') and cur != L + 'review/Gap-Search_2026-10-23.md':
            return old + cur[len(new):]
    for k, v in list(ROOTMOVE.items()) + [('PDFs/Methodology-Audit_2026-11-04/README.md', 'catalog/Audit-Sources_2026-11-04.md')]:
        if cur == L + v: return L + k
    return cur


files = subprocess.run(['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'], capture_output=True, text=True).stdout.split('\0')
EXT = ('.md', '.tex', '.py', '.ps1', '.yml', '.yaml', '.txt', '.json', '.bib', '.csv', '.gitignore', '.graphifyignore')
SKIP = ('graphify-out/', '99_Archive/', 'Claude outputs/', '03_Thesis/proposal/', '.venv', '/output/', 'output/', 'tmp/', '05_Data/raw/',
        '05_Data/processed/', '01_Literature/library/', 'scripts/literature-reorg/', '03_Thesis/tables/',
        'scripts/literature-new/', 'scripts/literature-search/v001/', 'scripts/literature-search/v002/', 'scripts/project-check/v001/')
LINK = re.compile(r'(\]\()(<?)([^)\s>#][^)>]*?)(>?)(#[^)]*)?(\))')
exact = sorted((k for k, v in mapping.items() if v and k.startswith((L, 'literature_new/'))), key=len, reverse=True)
changed = []
for f in files:
    if not f or not (f.endswith(EXT) or Path(f).name in ('.gitignore', '.graphifyignore')) or f.startswith(SKIP) or any(s in f for s in ('/output/',)):
        continue
    p = Path(f)
    if not p.exists() or p.stat().st_size > 3_000_000:
        continue
    try:
        text = p.read_bytes().decode('utf-8')
    except UnicodeDecodeError:
        continue
    orig = text
    # 1 + 2: path strings
    for k in exact:
        if k in text:
            text = text.replace(k, mapping[k])
    for a, b in PREFIX:
        if a in text:
            text = re.sub(re.escape(a) + r'(?=/|\b|$)', b, text)
    # 3: relative Markdown links, resolved from the file's old location, written for its new one
    if f.endswith('.md'):
        here_old = Path(old_of(f)).parent
        def fix(m):
            t = urllib.parse.unquote(m.group(3))
            if re.match(r'[a-z][a-z0-9+.-]*:', t, re.I) or t.startswith('/'):
                return m.group(0)
            old_abs = os.path.normpath((here_old / t).as_posix()).replace('\\', '/')
            new_abs = new_of(old_abs)
            if new_abs == old_abs and f == old_of(f):
                return m.group(0)
            rel = os.path.relpath(new_abs, Path(f).parent.as_posix()).replace('\\', '/')
            if rel == t:
                return m.group(0)
            rel = urllib.parse.quote(rel, safe='/._-~()') if ' ' in rel else rel
            return f"{m.group(1)}{m.group(2)}{rel}{m.group(4)}{m.group(5) or ''}{m.group(6)}"
        text = LINK.sub(fix, text)
    if text != orig:
        changed.append(f)
        if not dry:
            p.write_bytes(text.encode('utf-8'))
print(len(changed), 'files changed')
for c in changed: print(' ', c)
