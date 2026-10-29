"""Germany sampling instance 2. Standard library; no fabricated download data.

Commands: fetch; summarize RUN; rank RUN.
The complete source is also embedded in sampling_report.tex.
"""
import argparse
import csv
import hashlib
import json
import re
import ssl
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser

BASE = Path(__file__).resolve().parent
FITNESS = ['Fitness', 'Fitness Tracker', 'Schrittz\u00e4hler',
 'Aktivit\u00e4tstracker', 'Schlaf-Tracker', 'Herzfrequenz',
 'Kalorienz\u00e4hler', 'Ern\u00e4hrungstagebuch', 'Workout']
FERTILITY = ['Periode', 'Zyklus', 'Zyklustracker', 'Menstruation',
 'Eisprung', 'Fruchtbarkeit', 'Kinderwunsch', 'period tracker',
 'ovulation', 'fertility']
KEYWORDS = [(f'{prefix}{i}', domain, term)
 for prefix, domain, terms in [('F', 'fitness', FITNESS),
 ('P', 'fertility', FERTILITY)] for i, term in enumerate(terms, 1)]
START, END = '2025-10-01', '2026-09-30'
UA = 'BachelorThesisGermanySampling/2.0'

def load(path):
    return json.loads(path.read_text(encoding='utf-8'))

def save(path, value):
    with path.open('x', encoding='utf-8') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def table(path, rows, fields):
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        w.writeheader()
        for row in rows:
            output = {k: row.get(k) for k in fields}
            for k, v in output.items():
                if isinstance(v, list):
                    output[k] = json.dumps(v, ensure_ascii=False)
                elif isinstance(v, str) and v.startswith(('=', '+', '-', '@')):
                    output[k] = "'" + v
            w.writerow(output)

def fetch():
    run = BASE / 'raw' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    run.mkdir(parents=True)
    save(run / 'protocol.json', {'keywords': KEYWORDS, 'country': 'DE',
        'period_start': START, 'period_end': END, 'targets': [30, 20],
        'ranking': 'sum comparable DE downloads across verified product listings',
        'collection_source_sha256': digest(Path(__file__)),
        'store_ui_discovery_complete': False,
        'supplemental_coverage_check': 'Samsung Health; user requested',
        'network': 'no account; no cookie persistence; IP country not verified'})
    with (run / 'sampling.py').open('xb') as f:
        f.write(Path(__file__).read_bytes())
    requests, stopped, last = [], set(), 0.0
    def get(url, name, **context):
        nonlocal last
        host = url.split('/')[2]
        time.sleep(max(0, 3.5 - (time.monotonic() - last)))
        last = time.monotonic()
        meta = {'requested_url': url, 'file': name, **context,
            'captured_utc': datetime.now(timezone.utc).isoformat(),
            'status': None, 'error': None}
        body = b''
        try:
            if host in stopped:
                raise RuntimeError('Host stopped after 403/429')
            req = Request(url, headers={'User-Agent': UA,
                'Accept-Language': 'de-DE,de;q=0.9,en;q=0.7'})
            with urlopen(req, timeout=30, context=ssl.create_default_context()) as r:
                body = r.read()
                meta.update(status=r.status, final_url=r.url,
                    content_type=r.headers.get('Content-Type'))
        except HTTPError as e:
            body = e.read()
            meta.update(status=e.code, error=f'HTTP {e.code}')
            if e.code in (403, 429):
                stopped.add(host)
        except Exception as e:
            meta['error'] = f'{type(e).__name__}: {e}'
        with (run / name).open('xb') as f:
            f.write(body)
        meta.update(sha256=digest(run / name), bytes=len(body))
        save(run / (name + '.meta.json'), meta)
        requests.append(meta)
        print(json.dumps({'file': name, 'status': meta['status'],
            'error': meta['error']}), flush=True)
        return body, meta
    for name, url in [
        ('apple_api_docs.html', 'https://performance-partners.apple.com/search-api'),
        ('estimates_docs.html', 'https://docs.appfigures.com/api/reference/v2/estimates'),
        ('keyword_inspector_docs.html', 'https://help.appfigures.com/en/article/keyword-inspector-1jy20tk/'),
        ('google_terms.html', 'https://policies.google.com/terms?hl=en&gl=de')]:
        get(url, name, kind='documentation')
    for key, domain, term in KEYWORDS:
        params = {'term': term, 'country': 'de', 'media': 'software',
            'entity': 'software', 'limit': 20, 'lang': 'en_us'}
        get('https://itunes.apple.com/search?' + urlencode(params),
            f'apple_{key}.json', kind='keyword_api', keyword_id=key,
            keyword=term, domain_hint=domain)
    get('https://itunes.apple.com/lookup?id=1224541484&country=de',
        'samsung_apple_lookup.json', kind='coverage_lookup')
    robots, robots_meta = get('https://play.google.com/robots.txt',
        'play_robots.txt', kind='robots')
    robot = RobotFileParser()
    robot.parse(robots.decode('utf-8', errors='replace').splitlines())
    samsung_url = 'https://play.google.com/store/apps/details?' + urlencode({
        'id': 'com.sec.android.app.shealth', 'hl': 'de', 'gl': 'de'})
    if robots_meta['status'] == 200 and robot.can_fetch(UA, samsung_url):
        get(samsung_url, 'samsung_play.html', kind='coverage_lookup')
    save(run / 'requests.json', requests)
    save(run / 'completion.json', {'completed_utc': datetime.now(timezone.utc).isoformat(),
        'play_keyword_searches_completed': 0,
        'reason': 'Automated Play search path disallowed; no licensed replacement access available yet'})
    print('RUN=' + str(run), flush=True)

def summarize(run):
    out = BASE / 'processed' / run.name
    out.mkdir(parents=True, exist_ok=True)
    observations, unique, sessions = [], {}, []
    for req in load(run / 'requests.json'):
        if req['kind'] not in ['keyword_api', 'coverage_lookup']:
            continue
        body = run / req['file']
        if digest(body) != req['sha256']:
            raise ValueError('Source hash mismatch: ' + req['file'])
        if req['file'] == 'samsung_play.html':
            datasets = {}
            for block in re.findall(r'AF_initDataCallback[\s\S]*?</script>', body.read_text(encoding='utf-8')):
                key = re.search(r"key:\s*'([^']+)'", block)
                data = re.search(r'\bdata:\s*', block)
                if key and data:
                    datasets[key[1]] = json.JSONDecoder().raw_decode(block[data.end():])[0]
            detail = datasets['ds:5'][1][2]
            row = {'listing_id': 'play:com.sec.android.app.shealth',
                'name': detail[0][0], 'platform': 'play',
                'rating': detail[51][0][1], 'rating_count': detail[51][2][1],
                'play_embedded_global_proxy': detail[13][2],
                'installs_label': detail[13][0], 'german_downloads': None,
                'discovery': 'user_requested_coverage_audit', 'raw_file': req['file']}
            unique[row['listing_id']] = row
            continue
        if req['status'] != 200:
            sessions.append({'keyword_id': req.get('keyword_id'), 'status': req['status'], 'count': None})
            continue
        data = load(body)
        results = data['results']
        if req['kind'] == 'keyword_api':
            sessions.append({'keyword_id': req['keyword_id'], 'keyword': req['keyword'],
                'status': req['status'], 'count': len(results), 'raw_file': req['file']})
        for position, app in enumerate(results, 1):
            key = 'apple:' + str(app['trackId'])
            row = {'listing_id': key, 'name': app['trackName'], 'platform': 'apple',
                'rating': app.get('averageUserRating'), 'rating_count': app.get('userRatingCount'),
                'free_install': app.get('price') == 0, 'languages': app.get('languageCodesISO2A'),
                'german_downloads': None, 'raw_file': req['file'],
                'discovery': 'keyword_api' if req['kind'] == 'keyword_api' else 'user_requested_coverage_audit'}
            unique.setdefault(key, row)
            if req['kind'] == 'keyword_api':
                observations.append({'listing_id': key, 'keyword_id': req['keyword_id'],
                    'api_position': position, 'store_ui_position': None})
    for name, value in [('listings.json', list(unique.values())),
        ('sessions.json', sessions), ('appearances.json', observations)]:
        (out / name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    table(out / 'listings.csv', unique.values(), ['listing_id', 'name', 'platform',
        'rating', 'rating_count', 'free_install', 'languages', 'german_downloads',
        'play_embedded_global_proxy', 'installs_label', 'discovery', 'raw_file'])
    estimates = [{'listing_id': key, 'country': 'DE', 'start': START, 'end': END,
        'provider': '', 'metric': '', 'downloads': '', 'evidence_file': '',
        'evidence_sha256': '', 'retrieved_utc': ''} for key in unique]
    target = out / 'download_input_template.csv'
    if not target.exists():
        table(target, estimates, list(estimates[0]))
    summary = {'distinct_listings': len(unique), 'api_appearances': len(observations),
        'apple_queries_successful': sum(s['status'] == 200 for s in sessions),
        'samsung_in_keyword_queries': [a['keyword_id'] for a in observations if a['listing_id'] == 'apple:1224541484'],
        'german_download_values_available': 0, 'final_sample_size': 0}
    (out / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps(summary, indent=2))

def rank(run):
    out = BASE / 'processed' / run.name
    required = [out / n for n in ['downloads.csv', 'products.json', 'frame_review.json']]
    if not all(p.exists() for p in required):
        raise ValueError('Cannot rank: need downloads.csv, products.json and frame_review.json with verified evidence')
    frame = load(required[2])
    if frame.get('discovery_complete') is not True:
        raise ValueError('Cannot rank: two-store discovery incomplete')
    sessions = frame.get('sessions', [])
    expected = {(store, k[0]) for store in ['play', 'apple'] for k in KEYWORDS}
    found = {(s['platform'], s['keyword_id']) for s in sessions}
    if len(sessions) != 38 or found != expected:
        raise ValueError('Need all 38 store-keyword evidence records')
    for s in sessions:
        proof = run / s['evidence_file']
        if s.get('storefront') != 'DE' or digest(proof) != s['evidence_sha256']:
            raise ValueError('Unverified search-session evidence')
        if s.get('method') not in ['store_ui_capture', 'licensed_keyword_report']:
            raise ValueError('API discovery not validated as store UI frame')
        if len(s['result_listing_ids']) != 20 and s.get('exhausted') is not True:
            raise ValueError('Truncated search session without exhaustion evidence')
    with required[0].open(encoding='utf-8-sig', newline='') as f:
        values = list(csv.DictReader(f))
    downloads, comparable = {}, set()
    for v in values:
        if (v['country'], v['start'], v['end']) != ('DE', START, END):
            raise ValueError('Different country or time period')
        if not v['provider'] or not v['metric'] or not v['retrieved_utc']:
            raise ValueError('Incomplete metric provenance')
        comparable.add((v['provider'], v['metric']))
        evidence = run / v['evidence_file']
        if not evidence.is_file() or digest(evidence) != v['evidence_sha256']:
            raise ValueError('Missing or mismatched estimate evidence')
        number = int(v['downloads'])
        if number < 0 or v['listing_id'] in downloads:
            raise ValueError('Negative count or duplicate listing estimate')
        downloads[v['listing_id']] = number
    if len(comparable) != 1:
        raise ValueError('Mixed providers or metric definitions')
    products, used, ranked = load(required[1]), set(), []
    checks = ['tracking', 'free_install', 'DE_EN_interface', 'policy_reachable',
        'not_DiGA', 'not_duplicate', 'identity_verified', 'counterpart_coverage_verified',
        'minimum_1000_ratings', 'German_store_available']
    for p in products:
        if not all(p.get(c) is True for c in checks) or not p.get('evidence'):
            raise ValueError('Unverified eligibility/product coverage: ' + p['app_id'])
        if p['domain'] not in ['fitness', 'fertility']:
            raise ValueError('Unresolved domain')
        for e in p['evidence']:
            if digest(run / e['file']) != e['sha256']:
                raise ValueError('Unverified product-screening evidence')
        ids = p['listing_ids']
        if not ids or used.intersection(ids) or len(ids) != len(set(ids)):
            raise ValueError('Duplicate or empty product listing set')
        used.update(ids)
        if any(i not in downloads for i in ids):
            raise ValueError('Missing platform downloads, never substitute zero')
        ranked.append({**p, 'combined_DE_downloads': sum(downloads[i] for i in ids)})
    ranked.sort(key=lambda p: (-p['combined_DE_downloads'], p['app_id']))
    for i, p in enumerate(ranked, 1):
        p['overall_rank'] = i
    selected = [p for domain, limit in [('fitness', 30), ('fertility', 20)]
        for p in [a for a in ranked if a['domain'] == domain][:limit]]
    table(out / 'all_download_rankings.csv', ranked, ['overall_rank', 'app_id', 'name',
        'domain', 'listing_ids', 'combined_DE_downloads'])
    table(out / 'final_sample.csv', sorted(selected, key=lambda p: p['overall_rank']),
        ['overall_rank', 'app_id', 'name', 'domain', 'listing_ids', 'combined_DE_downloads'])
    print(f'Final verified sample: {len(selected)}; stratum shortfalls must be reported')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['fetch', 'summarize', 'rank'])
    parser.add_argument('run', nargs='?', type=Path)
    args = parser.parse_args()
    if args.command == 'fetch':
        fetch()
    elif args.run is None:
        parser.error('A raw run path is required')
    elif args.command == 'summarize':
        summarize(args.run.resolve())
    else:
        rank(args.run.resolve())
