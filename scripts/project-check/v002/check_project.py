"""Project health checks. Run before sending a draft, and in CI.

    python scripts/check_project.py          # report; exit 1 on errors
    python scripts/check_project.py --quiet  # errors and warnings only

Errors (fail CI):
  - a \\cite key used in the thesis that is missing from _shared/references.bib
  - a relative link in a Markdown file that points to a file that does not exist
  - a core reading-list row without its bibliography entry, or marked ☑ PDF
    while the PDF is missing
Warnings:
  - bibliography entries never cited (fine while drafting; review before submission)
  - works marked read/noted in reading-status.csv without a note file
  - the supervisor's review copy is older than the thesis sources
Info: TODO markers per chapter, reading progress.

Standard library only.
"""
import csv
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
THESIS = ROOT / '03_Thesis'
BIB = ROOT / '_shared/references.bib'
LIT = ROOT / '01_Literature'
SKIP = {'.git', '.venv', 'graphify-out', '99_Archive', 'node_modules', 'tmp'}
QUIET = '--quiet' in sys.argv

errors, warnings, info = [], [], []


def tex_files():
    return sorted(p for d in ('chapters', 'appendix', 'config') for p in (THESIS / d).glob('*.tex')) + [THESIS / 'thesis.tex']


def strip_comments(s):
    return re.sub(r'(?<!\\)%.*', '', s)


def check_citations():
    bib = BIB.read_text(encoding='utf-8')
    keys = set(re.findall(r'@\w+\s*\{\s*([^,\s]+)\s*,', bib))
    cited = {}
    for f in tex_files():
        for n, line in enumerate(strip_comments(f.read_text(encoding='utf-8')).splitlines(), 1):
            # \thesiscite{...} sets the cover's citation type (bossthesis.cls); not a citation
            for m in re.finditer(r'\\(?!thesiscite\b)[a-zA-Z]*cite[a-zA-Z]*\*?(?:\[[^\]]*\]){0,2}\{([^}]+)\}', line):
                for k in m.group(1).split(','):
                    cited.setdefault(k.strip(), f'{f.relative_to(ROOT).as_posix()}:{n}')
    for k, where in sorted(cited.items()):
        if k not in keys:
            errors.append(f'citation key "{k}" ({where}) is not in _shared/references.bib')
    unused = sorted(keys - set(cited))
    if unused:
        warnings.append(f'{len(unused)} bibliography entries are not cited in the thesis: ' + ', '.join(unused))
    info.append(f'citations: {len(cited)} distinct keys cited, {len(keys)} entries in the bibliography')
    return keys


def check_links():
    count = 0
    for md in ROOT.rglob('*.md'):
        # Raw collections can contain vendored upstream documentation. Validate
        # links TO raw evidence, but do not rewrite or audit those collections.
        if md.is_relative_to(ROOT / '05_Data' / 'raw') or SKIP & set(md.relative_to(ROOT).parts):
            continue
        text = md.read_text(encoding='utf-8', errors='replace')
        text = re.sub(r'```.*?```', '', text, flags=re.S)  # ignore code blocks (templates)
        for m in re.finditer(r'\]\(([^)\s]+)\)', text):
            target = m.group(1).split('#')[0]
            if not target or re.match(r'[a-z]+:', target) or target.startswith('<'):
                continue
            count += 1
            path = (md.parent / target.replace('%20', ' ')).resolve()
            if not path.exists():
                errors.append(f'broken link in {md.relative_to(ROOT).as_posix()}: {m.group(1)}')
    info.append(f'markdown links checked: {count}')


def check_reading(keys):
    readme = (LIT / 'README.md').read_text(encoding='utf-8')
    for m in re.finditer(r'\|\s*[☐◐☑]\s*\|\s*([☑☒])\s*\|\s*`([^`]+)`', readme):
        pdf_flag, key = m.group(1), m.group(2)
        if key not in keys:
            errors.append(f'core reading list: "{key}" has no entry in _shared/references.bib')
        if pdf_flag == '☑':
            line = readme[m.start():readme.find('\n', m.start())]
            named = re.search(r'`([^`]+\.pdf)`', line)
            # surname anywhere in the file name (double surnames), plus the year
            author = re.match(r'[a-z]+', key).group(0)
            year = re.search(r'\d{4}', key)
            found = (LIT / 'PDFs' / named.group(1)).exists() if named else any(
                author in p.stem.lower() and (not year or year.group(0)[:3] in p.stem)
                for p in (LIT / 'PDFs').glob('*.pdf'))
            if not found:
                errors.append(f'core reading list: "{key}" is marked ☑ PDF but no matching file is in 01_Literature/PDFs/')
    status_file = LIT / 'reading-status.csv'
    if status_file.exists():
        with status_file.open(encoding='utf-8', newline='') as fh:
            rows = list(csv.DictReader(fh))
        done = [r for r in rows if r['status'] in ('read', 'noted')]
        for r in done:
            if not r.get('note_file'):
                warnings.append(f'reading: "{r["id"]}" is marked {r["status"]} but has no note in 01_Literature/Notes/')
        info.append(f'reading: {len(done)} of {len(rows)} works read or noted')


def check_todos():
    total = 0
    parts = []
    for f in tex_files():
        n = len(re.findall(r'\\todo(?:\[[^\]]*\])?\{', strip_comments(f.read_text(encoding='utf-8'))))
        if n:
            parts.append(f'{f.stem} {n}')
            total += n
    info.append(f'TODO markers: {total} ({", ".join(parts)})' if total else 'TODO markers: none')


def check_review_copy():
    copy = THESIS / 'Thesis_Review-Copy.docx'
    if not copy.exists():
        warnings.append('review copy missing: run python scripts/build_review_docx.py')
        return
    newest = max(f.stat().st_mtime for f in tex_files() + [BIB])
    if copy.stat().st_mtime < newest - 1:
        warnings.append('review copy is older than the thesis sources; it is rebuilt at the next commit '
                        '(or run python scripts/build_review_docx.py)')


def main():
    keys = check_citations()
    check_links()
    check_reading(keys)
    check_todos()
    check_review_copy()
    for label, items in (('ERROR', errors), ('WARN', warnings)) + ((() if QUIET else (('INFO', info),))):
        for item in items:
            print(f'{label:5} {item}')
    print(f'\n{len(errors)} error(s), {len(warnings)} warning(s)')
    return 1 if errors else 0


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
