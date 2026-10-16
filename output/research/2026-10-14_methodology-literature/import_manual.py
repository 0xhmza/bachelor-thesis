"""File PDFs saved by hand (browser or library access) into the methodology corpus.

Drop PDFs into 01_Literature/PDFs/Methods-Reading/_Inbox/ and run this script.
Each file is matched to a still-missing catalogue entry by DOI/title using the
same checks as the automated downloader; unidentifiable files are left in the
inbox. Scanned PDFs without a text layer can be filed with --assume.
"""
from __future__ import annotations
import argparse
from difflib import SequenceMatcher
import hashlib
import io
import shutil
import subprocess
import sys

from pypdf import PdfReader

import download_open_access as oa

INBOX = oa.FOLDER / '_Inbox'
OBSOLETE = ('reason', 'oa_status', 'oa_landing_url', 'obstacle', 'display_status')

def catalogue_rows():
    data = oa.load(oa.CATALOGUE)
    extras = [{**r, 'author_label': r['title'].split(' (')[0].split(',')[0], 'category': 'Official',
               'year': '', 'rank': None} for r in data['official_or_no_doi_resources']]
    return data['ranked_doi_records'] + extras

def front_page_confirms(body, row, info):
    """Stricter than the downloader: a document that merely mentions a title must not pass.

    Page 1 must carry a first-author surname (a study guide's contents list does
    not) and either open with the paper's own title, show its DOI, or embed a
    closely matching PDF title.
    """
    reader = PdfReader(io.BytesIO(body), strict=False)
    first = oa.normalize(reader.pages[0].extract_text() or '')
    title = oa.normalize(row['title'])
    embedded = oa.normalize(str(reader.metadata.title or '') if reader.metadata else '')
    names = [oa.normalize(a.get('family') or a.get('familyName') or '') for a in row.get('authors', [])]
    names = [n for n in names if len(n) > 2]
    author_ok = not names or any(n in first for n in names[:3])
    title_ok = (info['doi_in_front_pages'] or title[:45] in first[:900]
                or SequenceMatcher(None, embedded, title).ratio() > .85)
    return author_ok and title_ok

def identify(body, candidates):
    matches = []
    for row in candidates:
        try:
            info = oa.validate(body, row)
            if front_page_confirms(body, row, info):
                matches.append((row, info))
        except Exception:
            continue
    matches.sort(key=lambda m: (m[1]['doi_in_front_pages'], m[1]['title_word_coverage']), reverse=True)
    if len(matches) > 1 and (matches[0][1]['doi_in_front_pages'], matches[0][1]['title_word_coverage']) == \
            (matches[1][1]['doi_in_front_pages'], matches[1][1]['title_word_coverage']):
        raise ValueError('ambiguous: matches ' + ', '.join(str(m[0]['id']) for m in matches[:3]) + '; use --assume ID')
    if not matches:
        raise ValueError('no still-missing catalogue entry matches its title/DOI; use --assume ID for scans')
    return matches[0]

def assume(body, row):
    reader = PdfReader(io.BytesIO(body), strict=False)
    if not len(reader.pages):
        raise ValueError('PDF has no pages')
    return row, {'pages': len(reader.pages), 'title_word_coverage': None, 'doi_in_front_pages': False,
                 'validation_method': 'identity asserted by user (--assume); only readability checked',
                 'sha256': hashlib.sha256(body).hexdigest(), 'bytes': len(body)}

def run(forced=None, compile_after=True):
    INBOX.mkdir(parents=True, exist_ok=True)
    manifest = oa.load(oa.MANIFEST)
    records = {str(r['id']): r for r in manifest['records']}
    rows = {str(r['id']): r for r in catalogue_rows()}
    pdfs = sorted(INBOX.glob('*.pdf'))
    if not pdfs:
        print(f'No PDFs in {INBOX.relative_to(oa.ROOT)}.')
        return
    imported = 0
    for path in pdfs:
        missing = [rows[i] for i, r in records.items() if not r.get('downloaded') and i in rows]
        try:
            body = path.read_bytes()
            if forced:
                if len(pdfs) > 1:
                    raise ValueError('--assume applies to a single inbox file')
                row, info = assume(body, rows[str(forced)])
            else:
                row, info = identify(body, missing)
            dest = oa.FOLDER / oa.GROUPS.get(row.get('category'), '11_Official-and-Methods') / oa.name_for(row)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(path, dest)
        except Exception as e:
            print(f'SKIPPED {path.name}: {e}')
            continue
        record = {k: v for k, v in records[str(row['id'])].items() if k not in OBSOLETE}
        records[str(row['id'])] = {**record, **info, 'downloaded': True, 'status': 'available',
                                   'file': dest.relative_to(oa.ROOT).as_posix(),
                                   'source_url': 'user-supplied', 'checked_on': oa.TODAY,
                                   'source_kind': 'user-supplied PDF (browser or library download)',
                                   'version': 'user-supplied; version not recorded — compare with the DOI record'}
        imported += 1
        print(f"FILED {path.name} -> {dest.relative_to(oa.ROOT).as_posix()} "
              f"(catalogue ID {row['id']}, rank {row.get('rank') or row['id']})")
    ordered = [records[str(r['id'])] for r in manifest['records']]
    from collections import Counter
    oa.save(oa.MANIFEST, {'checked_on': oa.TODAY, 'records': ordered,
                          'summary': dict(Counter(r['status'] for r in ordered))})
    print(f'Imported {imported} of {len(pdfs)} inbox file(s).')
    if imported and compile_after:
        subprocess.run([sys.executable, str(oa.BASE / 'compile_list.py')], check=True, cwd=oa.BASE)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--assume', help='Catalogue ID for a single inbox file whose text layer cannot identify it')
    parser.add_argument('--no-compile', action='store_true', help='Skip regenerating the guide and checklist')
    args = parser.parse_args()
    run(args.assume, not args.no_compile)
