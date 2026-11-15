"""Import the Zotero library file into a THROWAWAY Zotero and compare the result with references.bib.

    python scripts/zotero-library/v001/verify/verify_in_zotero.py [--base-dir] [--copy]

Starts the installed Zotero with its own temporary profile and data folder (under verify/run/, git-ignored), so
the real library is never touched; a test plugin imports 03_Thesis/references-zotero.rdf the way File > Import does
("Link to files" unless --copy), writes every imported item to result.json and quits. Then every .bib entry is
compared with its item: title, creators, DOI, URL, pages, volume, issue, date, citation key, reference number,
unmapped fields (kept in Extra), comment note, and the linked PDFs (present on disk, stored relative to the base
directory when --base-dir sets it). Close Zotero's own window first only if it is the same profile (it is not).
Exit code 1 when anything differs. Needs Zotero installed (C:\\Program Files\\Zotero\\zotero.exe or --exe).
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import build_zotero_library as b   # noqa: E402

RUN = HERE / 'run'


def run_zotero(exe, rdf, base_dir, copy):
    if RUN.exists():
        shutil.rmtree(RUN)
    prof, data, plugin = RUN / 'profile', RUN / 'data', RUN / 'plugin'
    out = RUN / 'result.json'
    for d in (prof, data):
        d.mkdir(parents=True)
    shutil.copytree(HERE / 'plugin', plugin)
    cfg = {'rdf': str(rdf), 'out': str(out), 'linkFiles': not copy, 'baseDir': str(b.ROOT) if base_dir else ''}
    boot = (plugin / 'bootstrap.js').read_text(encoding='utf-8').replace('__CONFIG__', json.dumps(cfg))
    (plugin / 'bootstrap.js').write_text(boot, encoding='utf-8')
    (prof / 'extensions').mkdir()
    (prof / 'extensions' / 'importtest@example.org').write_text(str(plugin), encoding='utf-8')
    prefs = {'extensions.zotero.useDataDir': True, 'extensions.zotero.dataDir': str(data),
             'extensions.autoDisableScopes': 0, 'extensions.enabledScopes': 15, 'xpinstall.signatures.required': False,
             'extensions.zotero.httpServer.enabled': False, 'extensions.zotero.firstRun2': False,
             'extensions.zotero.automaticScraperUpdates': False, 'app.update.auto': False, 'app.update.enabled': False,
             'extensions.zotero.sync.autoSync': False}
    (prof / 'user.js').write_text(''.join(f'user_pref("{k}", {json.dumps(v)});\n' for k, v in prefs.items()),
                                  encoding='utf-8')
    proc = subprocess.Popen([exe, '-profile', str(prof), '-no-remote', '-purgecaches'])
    t0 = time.time()
    while time.time() - t0 < 300 and not out.exists():
        time.sleep(2)
    time.sleep(3)
    try:
        proc.wait(timeout=30)
    except subprocess.TimeoutExpired:
        proc.kill()
    if not out.exists():
        sys.exit('Zotero produced no result.json (did the test plugin load?)')
    return json.loads(out.read_text(encoding='utf-8'))


def compare(result, base_dir):
    """List of differences between the imported items and the .bib entries."""
    problems = []
    if result.get('fatal') or result.get('err'):
        return [f'import failed: {result.get("fatal") or result.get("err")}']
    bib_text = b.BIB.read_text(encoding='utf-8')
    entries = b.parse_bib(bib_text)
    bbl = b.read_text(b.BBL)
    numbers = b.reference_numbers(entries, bbl, b.read_text(b.AUX))[0] if bbl else {}
    items = result['items']
    by_key = {i['json'].get('citationKey'): i for i in items if i['type'] not in ('attachment', 'note')}
    children = {}
    for i in items:
        if i['parent']:
            children.setdefault(i['parent'], []).append(i)
    pdfs = b.assign_pdfs(entries, sorted(p.name for p in b.LIBRARY.glob('*.pdf')), b.read_overrides())
    if len(by_key) != len(entries):
        problems.append(f'{len(by_key)} items for {len(entries)} entries')
    for e in entries:
        it = by_key.get(e.key)
        if not it:
            problems.append(f'{e.key}: not imported')
            continue
        j = it['json']
        ztype, fields, used = b.zotero_fields(e)
        if j['itemType'] != ztype:
            problems.append(f'{e.key}: type {j["itemType"]} != {ztype}')
        for name, value in fields.items():
            have = j.get(name, '')
            if name == 'accessDate':
                have = have[:10]
                value = value[:10]
            if have != value:
                problems.append(f'{e.key}: {name} {have!r} != {value!r}')
        people = [c for c in j.get('creators', []) if c['creatorType'] in ('author', 'programmer')]
        want = b.split_names(e.get('author'))
        if len(people) != len(want):
            problems.append(f'{e.key}: {len(people)} authors != {len(want)}')
        elif want and (people[0].get('lastName') or people[0].get('name')) != want[0][0] and people[0].get('name') != want[0][0]:
            problems.append(f'{e.key}: first author {people[0]}')
        editors = [c for c in j.get('creators', []) if c['creatorType'] == 'editor']
        if len(editors) != len(b.split_names(e.get('editor'))):
            problems.append(f'{e.key}: editors {len(editors)}')
        n = numbers.get(e.key)
        want_num = f'[{n}]' if n else ''
        if j.get('rights', '') != want_num:
            problems.append(f'{e.key}: Rights {j.get("rights")!r} != {want_num!r}')
        if n and ztype in b.HAS_CALL_NUMBER and j.get('callNumber', '') != want_num:
            problems.append(f'{e.key}: Call Number {j.get("callNumber")!r} != {want_num!r}')
        tags = {t['tag'] for t in j.get('tags', [])}
        if ('thesis:cited' in tags) != bool(n) or ('thesis:uncited' in tags) == bool(n):
            problems.append(f'{e.key}: cited/uncited tag {sorted(tags)}')
        for name in set(e.fields) - used:
            if f'BibTeX {name}: {b.latex_to_text(e.fields[name])}' not in j.get('extra', ''):
                problems.append(f'{e.key}: field {name} lost')
        kids = children.get(it['key'], [])
        notes = [k for k in kids if k['type'] == 'note']
        if bool(notes) != bool(e.comment):
            problems.append(f'{e.key}: comment note {len(notes)} vs {len(e.comment)} comment lines')
        atts = [k for k in kids if k['type'] == 'attachment']
        want_files = pdfs[e.key]
        got = sorted(Path(a['filePath'] or '').name for a in atts)
        if got != sorted(want_files):
            problems.append(f'{e.key}: files {got} != {sorted(want_files)}')
        for a in atts:
            if not a['exists'] or a['linkMode'] != 2:
                problems.append(f'{e.key}: attachment {a["rawPath"]} missing or not a linked file')
            relative = (a['rawPath'] or '').startswith('attachments:')
            if relative != bool(base_dir):
                problems.append(f'{e.key}: path {a["rawPath"]} {"is not" if base_dir else "is"} relative')
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base-dir', action='store_true', help='set the Linked Attachment Base Directory to the project root first')
    ap.add_argument('--copy', action='store_true', help='import with "copy files" instead of linking (shows the difference)')
    ap.add_argument('--exe', default=r'C:\Program Files\Zotero\zotero.exe')
    ap.add_argument('--rdf', type=Path, default=b.OUT)
    args = ap.parse_args()
    result = run_zotero(args.exe, args.rdf.resolve(), args.base_dir, args.copy)
    problems = compare(result, args.base_dir and not args.copy)
    atts = [i for i in result.get('items', []) if i['type'] == 'attachment']
    print(f'{sum(1 for i in result["items"] if i["type"] not in ("attachment", "note"))} items, {len(atts)} attachments, '
          f'{sum(1 for a in atts if a["exists"])} files found, {len(problems)} differences')
    for p in problems[:60]:
        print(' ', p)
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
