"""Retrieve registration metadata; retain raw evidence and flag title mismatches."""
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
from difflib import SequenceMatcher
import json
from pathlib import Path
import re
import time
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

BASE = Path(__file__).resolve().parent
EVIDENCE = BASE / 'evidence'
EVIDENCE.mkdir(exist_ok=True)
CHECK_FILE = EVIDENCE / 'publisher-checks.json'
PUBLISHER_CHECKS = json.loads(CHECK_FILE.read_text(encoding='utf-8')) if CHECK_FILE.exists() else {}

def request_json(url):
    request = Request(url, headers={'User-Agent': 'BachelorThesisLiteratureVerification/1.0 (academic DOI metadata audit)', 'Accept': 'application/json'})
    for retry in range(3):
        try:
            with urlopen(request, timeout=45) as response:
                return json.load(response)
        except HTTPError as error:
            if error.code not in {429, 502, 503, 504}:
                raise
            time.sleep(2 ** retry)
    raise RuntimeError('Metadata service retry limit reached')

def normalize(title):
    return re.sub(r'[^a-z0-9]+', '', title.lower())

def verify(row):
    number = row['id']
    cache = EVIDENCE / f'{int(number):02d}.json'
    url = ('https://api.datacite.org/dois/' if row['doi'].lower().startswith('10.48550/')
           else 'https://api.crossref.org/works/') + quote(row['doi'], safe='')
    try:
        data = json.loads(cache.read_text(encoding='utf-8')) if cache.exists() else None
        cached_doi = (data.get('message', {}).get('DOI') or data.get('data', {}).get('attributes', {}).get('doi')) if data else None
        if str(cached_doi).lower() != row['doi'].lower():
            try:
                data = request_json(url)
            except HTTPError as error:
                if error.code != 404:
                    raise
                url = 'https://api.datacite.org/dois/' + quote(row['doi'], safe='')
                data = request_json(url)
        cache.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        if 'data' in data:
            url = 'https://api.datacite.org/dois/' + quote(row['doi'], safe='')
            m = data['data']['attributes']
            title = max((t['title'] for t in m['titles']),
                        key=lambda candidate: SequenceMatcher(None, normalize(candidate), normalize(row['expected_title'])).ratio())
            authors = m.get('creators', [])
            year = m.get('publicationYear')
            abstract = next((d['description'] for d in m.get('descriptions', []) if d.get('descriptionType') == 'Abstract'), '')
            venue = m.get('publisher')
            source_url = m.get('url')
        else:
            m = data['message']
            title = m.get('title', [''])[0]
            subtitle = '; '.join(m.get('subtitle', []))
            if subtitle and normalize(subtitle) not in normalize(title):
                title += ': ' + subtitle
            authors = m.get('author', [])
            date = m.get('published-print') or m.get('published') or m.get('published-online') or m.get('issued')
            year = date['date-parts'][0][0] if date else None
            abstract = m.get('abstract', '')
            venue = '; '.join(m.get('container-title', []))
            source_url = m.get('resource', {}).get('primary', {}).get('URL') or m.get('URL')
        similarity = SequenceMatcher(None, normalize(title), normalize(row['expected_title'])).ratio()
        publisher_check = PUBLISHER_CHECKS.get(number)
        override = {}
        if publisher_check and publisher_check['doi'].lower() == row['doi'].lower() and normalize(publisher_check['registered_title']) == normalize(title):
            override = {'display_title': publisher_check['publisher_title'],
                        'verification_note': publisher_check['reason'],
                        'publisher_evidence_url': publisher_check['publisher_url']}
        return {**row, 'id': int(number), 'registered_title': title, 'year': year,
                'authors': authors, 'venue': venue, 'abstract': abstract,
                'primary_url': source_url, 'registry_url': url,
                'metadata_verified_on': '2026-10-14', 'title_match': round(similarity, 3),
                'verification': 'verified' if similarity >= .88 or override else 'check_title', **override}
    except Exception as error:
        return {**row, 'id': int(number), 'verification': 'error', 'error': str(error), 'registry_url': url}

if __name__ == '__main__':
    with (BASE / 'candidates.tsv').open(encoding='utf-8', newline='') as stream:
        rows = list(csv.DictReader(stream, delimiter='\t'))
    results = []
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(verify, row): row for row in rows}
        for future in as_completed(futures):
            result = future.result(); results.append(result)
            if result['verification'] != 'verified':
                print(json.dumps({k: result.get(k) for k in ['id', 'doi', 'registered_title', 'verification', 'title_match', 'error']}, ensure_ascii=False), flush=True)
    results.sort(key=lambda row: row['id'])
    (BASE / 'metadata.json').write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"Verified {sum(row['verification']=='verified' for row in results)}/{len(rows)} expected title matches; remaining records need inspection.", flush=True)
