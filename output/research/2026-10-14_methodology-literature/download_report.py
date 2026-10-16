"""Present verified local copies and specific retrieval obstacles in the reading guide."""
from collections import Counter
from datetime import date
import hashlib
import html
import json
from pathlib import Path
from urllib.parse import quote

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]
DEST = ROOT / '01_Literature'

def load_downloads():
    path = BASE / 'download-status.json'
    if not path.exists():
        return {}
    records = json.loads(path.read_text(encoding='utf-8'))['records']
    for r in records:
        if r.get('downloaded'):
            file = ROOT / r['file']
            assert file.is_file(), f'Marked downloaded but missing: {file}'
            assert hashlib.sha256(file.read_bytes()).hexdigest() == r['sha256'], f'Hash changed: {file}'
            r['local_url'] = quote(file.relative_to(DEST).as_posix(), safe='/')
            r['format_label'] = 'HTML full text' if r['status']=='available_html' else 'PDF'
            if r['id']==8:
                r['format_label'] = 'PDF — 1991 technical report'
            r['display_status'] = r['format_label']
        else:
            r['obstacle'] = obstacle(r)
            r['display_status'] = r['obstacle']
    return {str(r['id']):r for r in records}

def obstacle(r):
    if r['status']=='web_resource':
        return 'Web-only living framework; no paper PDF supplied. Use the official page.'
    errors = ' '.join(a.get('error','') for a in r.get('attempts',[])).lower()
    issues=[]
    if '403' in errors: issues.append('server denied automated access (HTTP 403)')
    if '404' in errors: issues.append('download/repository link is missing (HTTP 404)')
    if '500' in errors: issues.append('full-text service failed (HTTP 500)')
    if 'html/non-pdf' in errors or 'verification page' in errors:
        issues.append('link returned a webpage or verification screen instead of a PDF')
    if 'identity not established' in errors: issues.append('candidate PDF could not be matched to the requested paper')
    if 'preview/sample' in errors: issues.append('only a book preview/sample was found')
    if 'timed out' in errors or 'timeout' in errors: issues.append('source timed out')
    if 'encrypted' in errors: issues.append('candidate PDF was unreadable/encrypted')
    if r['status']=='free_but_blocked':
        why = '; '.join(issues) if issues else 'no usable direct download link was supplied'
        return f'Open access, but the publisher/repository blocks scripted downloads ({why}). Save it from a normal browser into the inbox (see the top of this page).'
    if issues:
        return 'No open-access copy retrieved (' + '; '.join(issues) + '); likely paywalled. Library access or an author copy is needed.'
    return 'No open-access copy located in the Unpaywall, OpenAlex, Europe PMC, publisher and repository sources checked; likely paywalled. Library access or an author copy is needed.'

def md_cell(r):
    if not r: return '☐ Not checked'
    if r.get('downloaded'): return f"☑ [{r['format_label']}]({r['local_url']})"
    return '☐ ' + r['obstacle'].replace('|','\\|')

def html_cell(r):
    if not r: return '☐ Not checked'
    if r.get('downloaded'):
        return '<a href="'+html.escape(r['local_url'],quote=True)+'">☑ '+html.escape(r['format_label'])+'</a>'
    return '☐ ' + html.escape(r['obstacle'])

def write_checklist(rows,extras,downloads):
    if not downloads: return
    ordered=rows+extras
    assert len(downloads)==len(ordered)==93
    counts=Counter('HTML' if r['status']=='available_html' else 'PDF' if r.get('downloaded') else 'missing' for r in downloads.values())
    checked=date.fromisoformat(max(r.get('checked_on','2026-10-14') for r in downloads.values()))
    checked_label=f"{checked.day} {checked:%B %Y}"
    html_count=f"**{counts['HTML']} full-text HTML copies**, " if counts['HTML'] else ''
    html_note=("HTML copies include source XML, tables and references; figure images are not bundled. "
               if counts['HTML'] else '')
    intro=(f"# Literature download checklist\n\nChecked **{checked_label}**: **{counts['PDF']} PDFs**, "
           f"{html_count}**{counts['missing']} items without a local full-text copy**. "
           "Covers all 83 ranked DOI records and 10 official/non-DOI resources.\n\n"
           "A checked box means a verified local copy is available, **not that the paper has been read**. "
           "Files are grouped by methodological topic under [PDFs/Methods-Reading](PDFs/Methods-Reading/README.md). "
           "Filename numbers retain the reading priority. " + html_note +
           "Manuscript, technical-report and whole-book versions are labelled below. "
           "Download failures are observations from this environment, not proof of a paywall or of no free copy existing anywhere.\n\n"
           "[Searchable ranked guide](Methods-Reading-List.html) · [Methodological relevance and stage](Methods-Reading-List.md)\n\n"
           "## Adding a missing copy\n\n"
           "Automated retrieval uses only public, honestly identified requests; it does not log in, solve verification checks or use shadow libraries. "
           "To close a gap, save the PDF from a normal browser (your own library access is fine) into "
           "`01_Literature/PDFs/Methods-Reading/_Inbox/`, then run "
           "`.venv/Scripts/python.exe output/research/2026-10-14_methodology-literature/import_manual.py`. "
           "The importer matches each file to a catalogue entry by title, first-author surname and DOI, refuses anything it cannot identify "
           "(scans without a text layer: `--assume ID`), files it under the right topic folder and regenerates this checklist.\n\n")
    parts=[intro]
    for category in dict.fromkeys(r.get('category','Official/non-DOI resources') for r in ordered):
        parts.append('## '+category+'\n\n')
        for row in [r for r in ordered if r.get('category','Official/non-DOI resources')==category]:
            r=downloads[str(row['id'])]
            label=str(row.get('rank') or row['id'])
            url=row.get('doi_url') or row['url']
            title=row['title'].replace('[','\\[').replace(']','\\]')
            parts.append(f"- [{'x' if r['downloaded'] else ' '}] **{label} / {row['priority']} — [{title}]({url})**\n")
            if r['downloaded']:
                extent = str(r['pages'])+' pages' if r.get('pages') else 'full text with source XML'
                parts.append(f"  - [{r['format_label']}]({r['local_url']}) · {extent} · version: {r.get('version') or 'not specified by source'}.\n")
                source=r.get('source_url','')
                if source.startswith(('https://','http://')): parts.append(f'  - [Download source]({source}).\n')
                elif r.get('reused_existing'): parts.append('  - Reused the verified project-held copy.\n')
                elif source=='user-supplied': parts.append('  - Saved by hand from a browser or library login and filed by the inbox importer; compare the version with the DOI record.\n')
                else: parts.append('  - File verified locally; original retrieval URL was not retained after the interrupted first batch.\n')
                if r['id'] in {80,81}: parts.append('  - Published law-review copy; the ranked DOI identifies the earlier SSRN record.\n')
                if r['id']==8: parts.append('  - Scanned 1991 report verified visually against title/authors; the ranked DOI identifies the 1992 journal article.\n')
                if r['status']=='available_html':
                    parts.append('  - PDF retrieval was blocked; complete article text saved from public Europe PMC XML. Figure images remain online.\n')
                    parts.append(f"  - **Real PDF still wanted:** open <{url}> in a browser and save the article PDF into the inbox; the importer replaces this HTML copy.\n")
            else:
                parts.append('  - **Obstacle:** '+r['obstacle']+'\n')
                if r['status']=='free_but_blocked' and r.get('oa_landing_url'):
                    parts.append(f"  - Open-access location to open in a browser: <{r['oa_landing_url']}>\n")
                elif r['status']!='web_resource':
                    parts.append(f"  - DOI / publisher page for library access: <{url}>\n")
            parts.append('\n')
    (DEST/'Download-Checklist.md').write_text(''.join(parts),encoding='utf-8')
    folder=DEST/'PDFs/Methods-Reading'
    folders=Counter(Path(r['file']).parent.name for r in downloads.values() if r.get('downloaded'))
    html_clause=f" and {counts['HTML']} HTML full-text copies" if counts['HTML'] else ''
    text=(f"# Methodology reading copies\n\n{counts['PDF']} PDFs{html_clause}, organized by topic. "
          f"Checked on {checked_label}.\n\n[Complete download checklist and obstacles](../../Download-Checklist.md) · "
          "[Ranked relevance and stage](../../Methods-Reading-List.md) · [Searchable guide](../../Methods-Reading-List.html)\n\n"
          "These are reading candidates; downloading does not mark them as read or add them to the thesis bibliography. "
          "Numbers in filenames are the global reading rank; N1–N10 are official/non-DOI resources.\n\n")
    text+='| Folder | Local works |\n|---|---:|\n'+''.join(f'| [{name}]({name}/) | {n} |\n' for name,n in sorted(folders.items()))
    text+='\n'+('HTML full text includes an adjacent original XML file. Figure images are not bundled. ' if counts['HTML'] else '')
    text+='Accepted manuscripts and technical reports can differ from final publications. The N2 file (Wharton et al. 1994) is the whole edited book; relevant chapter pp. 105–140. '
    text+='Citron and Martin files are published law-review versions of the earlier SSRN DOI records. '
    text+='Retrieval URLs, version labels, SHA-256 checksums, PDF page counts and individual failed attempts are retained in '
    text+='[the audit manifest](../../../output/research/2026-10-14_methodology-literature/download-status.json).\n'
    # From this nested folder the repository root is three levels above.
    (folder/'README.md').write_text(text,encoding='utf-8')
    (BASE/'download-verification.json').write_text(json.dumps({'checked_on':checked.isoformat(),'records':len(ordered),'counts':dict(counts),'all_local_files_exist_and_match_sha256':True,'all_missing_have_obstacles':True},indent=2)+'\n',encoding='utf-8')
