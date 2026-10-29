"""Offline derivation. Raw bytes are never modified. No third-party dependencies.

Play field paths are informed by JoMingyu/google-play-scraper commit
ce1df6d67e6d8c39826daac2f668808fc025f284 constants/element.py.
Independent parser uses JSONDecoder.raw_decode, never executes page scripts.
"""
import argparse
import csv
import hashlib
import html
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
PATHS = {'name': [0, 0], 'installs_label': [13, 0], 'minInstalls': [13, 1],
         'realInstalls': [13, 2], 'rating': [51, 0, 1], 'rating_count': [51, 2, 1],
         'written_review_count': [51, 3, 1], 'price_micros': [57, 0, 0, 0, 0, 1, 0, 0],
         'currency': [57, 0, 0, 0, 0, 1, 0, 1], 'developer': [68, 0],
         'provider_url': [69, 0, 5, 2], 'privacy_policy_url': [99, 0, 5, 2],
         'category': [79, 0, 0, 0], 'version': [140, 0, 0, 0]}

def at(data, path):
    try:
        for i in path:
            data = data[i]
        return data
    except (TypeError, IndexError, KeyError):
        return None

def parse_play(source):
    dataset = {}
    for block in re.findall(r'AF_initDataCallback[\s\S]*?</script>', source):
        key = re.search(r"key:\s*['\"](ds:\d+)['\"]", block)
        data = re.search(r'\bdata:\s*', block)
        if key and data:
            dataset[key.group(1)] = json.JSONDecoder().raw_decode(block[data.end():])[0]
    detail = at(dataset.get('ds:5'), [1, 2])
    if not isinstance(detail, list):
        raise ValueError('Missing ds:5 detail array; do not treat as an empty successful listing')
    result = {key: at(detail, path) for key, path in PATHS.items()}
    desc = at(detail, [12, 0, 0, 1]) or at(detail, [72, 0, 1])
    result['description'] = html.unescape(re.sub('<[^>]+>', ' ', desc)) if isinstance(desc, str) else None
    result['free_install'] = result['price_micros'] == 0 if isinstance(result['price_micros'], (int, float)) else None
    validate(result)
    return result

def validate(row):
    if not isinstance(row.get('name'), str) or not row['name'].strip():
        raise ValueError('Missing app name')
    rating = row.get('rating')
    if rating is not None and (not isinstance(rating, (int, float)) or not math.isfinite(rating) or not 0 <= rating <= 5):
        raise ValueError('Invalid rating')
    for field in ['rating_count', 'written_review_count', 'minInstalls', 'realInstalls']:
        value = row.get(field)
        if value is not None and (type(value) is not int or value < 0):
            raise ValueError('Invalid count: ' + field)
    if row.get('realInstalls') is not None and row.get('minInstalls') is not None and row['realInstalls'] < row['minInstalls']:
        raise ValueError('Embedded install count below displayed lower bound')

def load(path):
    return json.loads(path.read_text(encoding='utf-8'))

def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')

def write_csv(path, rows, fields):
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        for row in rows:
            output = {k: row.get(k) for k in fields}
            for k, value in output.items():
                if isinstance(value, (dict, list)):
                    output[k] = json.dumps(value, ensure_ascii=False)
                elif isinstance(value, str) and value.startswith(('=', '+', '-', '@')):
                    output[k] = "'" + value
            writer.writerow(output)

def build(run):
    protocol = load(run / 'inputs/protocol.json')
    out = BASE / 'processed' / run.name
    out.mkdir(parents=True, exist_ok=True)
    listings, appearances, errors, sessions = {}, [], [], []
    for search in load(run / 'searches.json'):
        session = {'keyword_id': search['id'], 'keyword': search['term'], 'platform': 'apple',
                   'source': 'official_search_api_trial', 'status': search['status'],
                   'captured_utc': search['started_utc'], 'raw_file': search['file'], 'returned': None}
        try:
            if search['status'] != 200:
                raise ValueError(search['error'])
            payload = load(run / search['file'])
            result = payload['results']
            session['returned'] = len(result)
            if not isinstance(result, list) or payload['resultCount'] != len(result):
                raise ValueError('Unexpected search response shape')
            for rank, app in enumerate(result[:20], 1):
                key = 'apple:' + str(app['trackId'])
                appearances.append({'listing_id': key, 'keyword_id': search['id'], 'keyword': search['term'],
                                    'domain_hint': search['domain'], 'source_rank': rank,
                                    'rank_type': 'API response position, not verified store UI rank',
                                    'store_ui_rank': None, 'raw_file': search['file'], 'captured_utc': search['started_utc']})
                row = {'listing_id': key, 'platform': 'apple', 'store_id': str(app['trackId']),
                       'name': app['trackName'], 'developer': app.get('artistName'),
                       'bundle_id': app.get('bundleId'), 'rating': app.get('averageUserRating'),
                       'rating_count': app.get('userRatingCount'), 'price': app.get('price'),
                       'free_install': app['price'] == 0 if isinstance(app.get('price'), (int, float)) else None,
                       'currency': app.get('currency'), 'languages': app.get('languageCodesISO2A', []),
                       'category': app.get('primaryGenreName'), 'version': app.get('version'),
                       'provider_url': app.get('sellerUrl'), 'privacy_policy_url': None,
                       'description': app.get('description'), 'url': app.get('trackViewUrl'),
                       'raw_file': search['file'], 'source_sha256': search['sha256'],
                       'captured_utc': search['started_utc'], 'discovery_source': 'official_search_api_trial'}
                validate(row)
                # First observation is deterministic; every occurrence stays in appearances.
                listings.setdefault(key, row)
        except Exception as e:
            errors.append({'stage': 'apple_parse', 'source': search['file'], 'error': str(e)})
        sessions.append(session)
    for request in load(run / 'play_requests.json'):
        try:
            if request['status'] != 200:
                raise ValueError(request.get('error', 'No successful response'))
            row = parse_play((run / request['file']).read_text(encoding='utf-8'))
            key = 'play:' + request['app_id']
            row.update(listing_id=key, platform='play', store_id=request['app_id'],
                       domain_hint=request['domain_hint'], url=request['requested_url'],
                       raw_file=request['file'], source_sha256=request['sha256'],
                       captured_utc=request['started_utc'], discovery_source=request['discovery'])
            listings[key] = row
        except Exception as e:
            errors.append({'stage': 'play_parse', 'source': request['app_id'], 'error': str(e)})
    hints = defaultdict(set)
    for a in appearances:
        hints[a['listing_id']].add(a['domain_hint'])
    screening = []
    for key, row in sorted(listings.items()):
        reasons, pending = [], ['tracking_function', 'reachable_policy', 'DiGA_status', 'duplicate_product', 'store_UI_search_membership']
        if row.get('rating_count') is None or row.get('rating') is None:
            pending.append('rating_data_missing')
        elif row['rating_count'] < protocol['minimum_ratings_per_listing']:
            reasons.append('E01_fewer_than_1000_ratings')
        if row['free_install'] is False:
            reasons.append('E02_paid_installation')
        elif row['free_install'] is None:
            pending.append('installation_price_missing')
        if row['platform'] == 'apple':
            language = bool(set(row['languages']) & {'DE', 'EN'}) if row['languages'] else None
            if language is False:
                reasons.append('E03_no_DE_or_EN_interface_declared')
            elif language is None:
                pending.append('interface_language')
        else:
            language = None
            pending += ['interface_language', 'German_installability']
        if row.get('domain_hint'):
            hints[key].add(row['domain_hint'])
        title = row['name'].lower()
        cycle_title = bool(re.search(r'period|zyklus|menstru|ovulat|fertil|eisprung|fruchtbar|clue|flo:|flo ', title))
        domain = 'fertility' if cycle_title else ('fitness' if hints[key] == {'fitness'} else 'unresolved')
        row.update(domain_provisional=domain, domain_hints=sorted(hints[key]))
        screening.append({'listing_id': key, 'name': row['name'], 'platform': row['platform'],
                          'domain_provisional': domain, 'domain_basis': 'title heuristic and discovery hints; review required',
                          'numeric_status': 'exclude_listing' if reasons else ('pending_numeric' if row.get('rating_count') is None or row.get('rating') is None or row['free_install'] is None else 'passes_numeric'),
                          'exclusion_codes': reasons, 'pending_checks': pending, 'language_declared_DE_EN': language,
                          'final_eligible': False})
    fields = ['listing_id', 'platform', 'store_id', 'name', 'developer', 'domain_provisional', 'domain_hints',
              'rating', 'rating_count', 'free_install', 'languages', 'category', 'version',
              'installs_label', 'minInstalls', 'realInstalls', 'privacy_policy_url', 'provider_url',
              'url', 'captured_utc', 'raw_file', 'source_sha256', 'discovery_source']
    write_json(out / 'listings.json', list(listings.values()))
    write_csv(out / 'listings.csv', listings.values(), fields)
    write_json(out / 'screening.json', screening)
    write_csv(out / 'screening.csv', screening, ['listing_id', 'name', 'platform', 'domain_provisional', 'numeric_status', 'exclusion_codes', 'pending_checks', 'language_declared_DE_EN', 'final_eligible'])
    write_csv(out / 'search_appearances.csv', appearances, ['listing_id', 'keyword_id', 'keyword', 'domain_hint', 'source_rank', 'rank_type', 'store_ui_rank', 'raw_file', 'captured_utc'])
    write_csv(out / 'search_sessions.csv', sessions, ['keyword_id', 'keyword', 'platform', 'source', 'status', 'returned', 'captured_utc', 'raw_file'])
    write_json(out / 'errors.json', errors)
    numeric_ids = {s['listing_id'] for s in screening if s['numeric_status'] == 'passes_numeric'}
    ranked = sorted((r for r in listings.values() if r['listing_id'] in numeric_ids), key=lambda r: (-r['rating'], -r['rating_count'], r['listing_id']))
    for rank, row in enumerate(ranked, 1):
        row['listing_review_priority'] = rank
    write_csv(out / 'review_queue.csv', ranked, ['listing_review_priority'] + fields)
    installs = sorted((r for r in ranked if r['platform'] == 'play' and r.get('realInstalls') is not None), key=lambda r: (-r['realInstalls'], r['listing_id']))
    for rank, row in enumerate(installs, 1):
        row['install_proxy_rank'] = rank
    write_csv(out / 'play_install_comparison.csv', installs, ['install_proxy_rank', 'listing_review_priority'] + fields)
    summary = {'run': run.name, 'apple_queries_attempted': len(sessions),
               'apple_queries_successful': sum(s['status'] == 200 and s['returned'] is not None for s in sessions),
               'apple_search_appearances': len(appearances), 'distinct_listings': len(listings),
               'platform_counts': dict(Counter(r['platform'] for r in listings.values())),
               'screening_numeric': dict(Counter(s['numeric_status'] for s in screening)),
               'numeric_pass_domain_hints': dict(Counter(r['domain_provisional'] for r in ranked)),
               'error_count': len(errors), 'final_sample_size': 0,
               'final_status': 'Not frozen: proposal search frame and human eligibility checks incomplete',
               'exclusion_code_counts_nonexclusive': dict(Counter(c for s in screening for c in s['exclusion_codes']))}
    write_json(out / 'summary.json', summary)
    write_json(out / 'derivation.json', {'run': run.name, 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                                      'protocol_sha256': hashlib.sha256((run / 'inputs/protocol.json').read_bytes()).hexdigest(),
                                      'input_policy': 'First observation per listing; all search appearances preserved'})
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return out

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('run', type=Path)
    build(parser.parse_args().run.resolve())
