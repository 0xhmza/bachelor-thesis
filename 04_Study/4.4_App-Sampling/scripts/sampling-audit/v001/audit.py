"""Read-only audit of the archived v003 sample; never alters its inputs/outputs.

Run from any directory: python 04_Study/4.4_App-Sampling/scripts/sampling-audit/v001/audit.py
Audit artifacts and an isolated replay are written only to this version's output/.
Counterfactuals are diagnostic scenarios, not adopted screening decisions.
"""
import contextlib
import csv
import hashlib
import importlib.util
import io
import json
import os
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent / 'output'
RANKING = ROOT / '04_Study/4.4_App-Sampling/scripts/app-ranking/v003'


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def read_csv(path):
    with Path(path).open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_csv(name, rows):
    if not rows:
        return
    with (OUT / name).open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    os.chdir(ROOT)
    OUT.mkdir(parents=True, exist_ok=True)
    spec = importlib.util.spec_from_file_location('audited_ranking_v003', RANKING / 'rank.py')
    rank = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rank)
    cfg = read_json(RANKING / 'config.json')
    source_files = [Path(cfg[s]) for s in ('apple', 'play')]
    source_files += [Path(cfg[k]) for k in ('keywords', 'screening', 'table')]
    source_files += [RANKING / 'rank.py', RANKING / 'config.json']
    source_files += list((RANKING / 'output').glob('*'))
    before = {str(p): digest(p) for p in source_files if p.is_file()}
    checks = []

    def check(name, ok, detail):
        checks.append({'check': name, 'passed': bool(ok), 'detail': detail})

    raw = {s: read_json(cfg[s]) for s in ('apple', 'play')}
    raw_rows = {s: [row for rows in raw[s]['results'].values() for row in rows] for s in raw}
    unique = {s: {str(x['ID']): x for x in rows} for s, rows in raw_rows.items()}
    keywords = read_csv(cfg['keywords'])
    queries = {x['query'] for x in keywords}
    screening_rows = read_csv(cfg['screening'])
    screening = {(x['store'], x['id']): x for x in screening_rows}
    listings = {s: rank.load(cfg[s], s, cfg['aliases'])[1] for s in raw}
    pools = {s: {k: x for k, x in rank.pool(listings[s], cfg['depth'], queries).items()
                 if k not in cfg['preinstalled'][s]} for s in raw}
    candidates = rank.candidates(pools['apple'], pools['play'], cfg['pairs'])
    preinstalled = {rank.provider_key(x, cfg['aliases']) for x in cfg['preinstalled_providers']}

    def evaluate(pairs=None, screen=None):
        cs = rank.candidates(pools['apple'], pools['play'], pairs or cfg['pairs'])
        ratios = [x['v']/x['r'] for x in cs if x['apple'] and x['play'] and x['r'] > 0 and x['v'] > 0]
        c = statistics.median(ratios) * cfg['os_share']['ios'] / cfg['os_share']['android']
        ordered = sorted(cs, key=lambda x: (-(x['v'] + c*x['r']), x['key']))
        result = rank.select(ordered, screening if screen is None else screen, cfg['n'], preinstalled)
        return cs, c, len(ratios), ordered, result

    candidates, c, pairs_n, ordered, result = evaluate()
    selected, skipped, excluded, pending = result
    stored = read_json(RANKING / 'output/report.json')
    check('query coverage', queries == set(raw['apple']['results']) == set(raw['play']['search']), len(queries))
    check('German storefront settings', raw['apple']['region'] == raw['play']['region'] == 'de'
          and raw['play']['language'] == 'de', {s: raw[s]['region'] for s in raw})
    check('no missing Play search IDs', not raw['play']['hits_without_id'], raw['play']['hits_without_id'])
    check('no final Play page errors', not raw['play']['errors'], raw['play']['errors'])
    check('unique screening keys', len(screening_rows) == len(screening), len(screening_rows))
    check('screening IDs exist in collections', all(x['id'] in unique[x['store']] for x in screening_rows), len(screening_rows))
    check('screening schema', all(x['decision'] in ('eligible', 'excluded') and x['reason']
          and (x['category'] if x['decision'] == 'eligible' else x['criterion'] in ('E1','E2','E3','E4','E5'))
          for x in screening_rows), Counter(x['decision'] for x in screening_rows))
    check('47 ranked apps and unique providers', len(selected) == len({x['provider'] for x in selected}) == 47, len(selected))
    check('preinstalled providers excluded from ranking selection', not preinstalled & {x['provider'] for x in selected}, sorted(preinstalled))
    check('no provisional main selections', not pending, [x['key'] for x in pending])
    check('calibration reproduced', abs(c-stored['calibration']['c']) < 1e-14 and pairs_n == 114, {'c': c, 'pairs': pairs_n})
    check('cascade reproduced', len(selected)+len(skipped)+len(excluded) == stored['reached'] == 70,
          {'selected': len(selected), 'provider_skips': len(skipped), 'excluded': len(excluded)})
    check('selected listings free to install', all(unique[s][x[s]['id']].get('Price') == 0
          for x in selected for s in ('apple','play') if x[s]), '79 store listings')
    check('selected feedback counts observed', all(('Rating Count' if s == 'apple' else 'Review Count') in unique[s][x[s]['id']]
          for x in selected for s in ('apple','play') if x[s]), '79 store listings')
    check('selected Play policy URLs present', all(unique['play'][x['play']['id']].get('Privacy Policy URL')
          for x in selected if x['play']), '41 Play listings')
    for s in ('apple', 'play'):
        ids = [str(unique[s][x[s]['id']].get('Dev. ID')) for x in selected if x[s]]
        check(s+' selected developer IDs unique', len(ids) == len(set(ids)), len(ids))

    # Replay production code with output/table paths redirected into this audit folder.
    replay_cfg = dict(cfg, out=str(OUT / 'replayed-v003'), table=str(OUT / 'replayed-app-sample.tex'))
    replay_path = OUT / 'replay-config.json'
    replay_path.write_text(json.dumps(replay_cfg, indent=2), encoding='utf-8')
    with contextlib.redirect_stdout(io.StringIO()):
        rank.main(str(replay_path))
    for name in ('selection.csv','excluded.csv','sensitivity.csv','screening-sheet.csv'):
        expected = read_csv(RANKING / 'output' / name)
        actual = read_csv(OUT / 'replayed-v003' / name)
        check('exact replay '+name, actual == expected, len(actual))
    check('exact replay report.json', read_json(OUT / 'replayed-v003/report.json') == stored, 'all fields')
    check('generated sample table reproduced', (OUT/'replayed-app-sample.tex').read_text(encoding='utf-8')
          == Path(cfg['table']).read_text(encoding='utf-8'), 'all 50 rows')

    cache_path = Path('04_Study/4.4_App-Sampling/scripts/googleplay-scraper/v004/output/pages-2026-10-24.jsonl')
    cache_rows = [json.loads(line) for line in cache_path.read_text(encoding='utf-8').split('\n') if line]
    cache = {x['id']: x for x in cache_rows}
    check('cache unique and covers all 645 pages', len(cache_rows) == len(cache) == 645 and set(cache) == set(unique['play']), len(cache))
    check('final Play rows match cache', all({k:v for k,v in x.items() if k!='Search Position'} == cache[str(x['ID'])]['row']
          for x in raw_rows['play']), len(raw_rows['play']))
    progress = re.findall(r'^page (\d+)/(\d+) (\S+)$', Path('04_Study/4.4_App-Sampling/scripts/googleplay-scraper/v004/output/run-2026-10-25-all.log').read_text().strip(), re.M)
    check('final Play progress log covers 645 pages', len(progress) == 645 and {x[2] for x in progress} == set(cache)
          and [int(x[0]) for x in progress] == list(range(1,646)), len(progress))
    request_ids = set()
    for f in Path('04_Study/4.4_App-Sampling/scripts/googleplay-scraper/v004/output').glob('*.json'):
        doc = read_json(f)
        for url, meta in doc.get('requests', {}).items():
            if '/store/apps/details?' in url and re.fullmatch('[0-9a-f]{64}', meta.get('sha256','')):
                request_ids.update(parse_qs(urlparse(url).query).get('id', []))
    request_coverage = sorted(request_ids & set(cache))
    missing = [{'id': x['ID'], 'name': x['App Name'], 'installs': x.get('Embedded Install Count'),
                'review_count_present': 'Review Count' in x, 'rating_count_present': 'Rating Count' in x,
                'score_contribution_in_v003': 0} for x in unique['play'].values() if 'Review Count' not in x]
    write_csv('missing-play-review-counts.csv', missing)

    trace, taken = [], set(preinstalled)
    for n, x in enumerate(ordered, 1):
        if len([z for z in trace if z['outcome']=='selected']) >= 47:
            break
        d = rank.decision(x, screening)
        outcome = 'provider already selected' if x['provider'] in taken else (
            'pending' if d is None else 'excluded' if d['decision'] != 'eligible' else 'selected')
        if outcome in ('selected','pending'):
            taken.add(x['provider'])
        trace.append({'rank': n, 'key': x['key'], 'name': x['name'], 'provider': x['provider'],
                      'apple_id': x['apple']['id'] if x['apple'] else '', 'play_id': x['play']['id'] if x['play'] else '',
                      'r': x['r'], 'v': x['v'], 'score': x['v']+c*x['r'], 'outcome': outcome,
                      'criterion': d.get('criterion','') if d else '', 'reason': d.get('reason','') if d else ''})
    write_csv('main-cascade.csv', trace)
    write_csv('matched-listings.csv', [{'apple_id': x['apple']['id'], 'apple_name': x['apple']['name'],
              'play_id': x['play']['id'], 'play_name': x['play']['name'], 'r': x['r'], 'v': x['v']}
              for x in candidates if x['apple'] and x['play']])

    # Identity reference cases are anchored in distinct archived product names/IDs.
    reference_pairs = {'com.nike.plusgps':'387771637', 'com.nike.ntc':'301521403',
        'com.babycenter.pregnancytracker':'386022579',
        'menloseweight.loseweightappformen.weightlossformen':'1460546771',
        'loseweightapp.loseweightappforwomen.womenworkoutathome':'1502526521'}
    identity_issues = []
    for pid, aid in reference_pairs.items():
        found = next(x for x in candidates if x['play'] and x['play']['id']==pid)
        actual = found['apple']['id'] if found['apple'] else None
        if actual != aid:
            identity_issues.append({'play_id':pid, 'play_name':pools['play'][pid]['name'],
                'actual_apple_id':actual, 'actual_apple_name':pools['apple'][actual]['name'] if actual else None,
                'proposed_apple_id':aid, 'proposed_apple_name':pools['apple'][aid]['name']})

    def scenario(name, pairs=None, screen=None):
        cs, factor, nn, _, (ss, _, _, pp) = evaluate(pairs, screen)
        old = {x['provider']:x for x in selected}
        new = {x['provider']:x for x in ss}
        return {'scenario':name, 'c':factor, 'calibration_pairs':nn, 'candidates':len(cs),
            'provider_entries':[new[k]['name'] for k in sorted(new.keys()-old.keys())],
            'provider_exits':[old[k]['name'] for k in sorted(old.keys()-new.keys())],
            'order_positions_changed':sum(a['key']!=b['key'] for a,b in zip(selected,ss)),
            'selected_apple_ids_changed':sum((a['apple']['id'] if a['apple'] else None)!=(b['apple']['id'] if b['apple'] else None)
                for a,b in zip(selected,ss)), 'pending':[x['key'] for x in pp]}

    scenarios = [scenario('five proposed identity corrections', cfg['pairs'] | reference_pairs)]
    for name, key, category in [('Kinomap eligible', ('apple','611177969'), 'activity'),
                                 ('Lady Pill Reminder eligible', ('play','com.baviux.pillreminder'), 'cycle')]:
        altered = {k:dict(v) for k,v in screening.items()}
        altered[key].update(decision='eligible', criterion='', category=category)
        scenarios.append(scenario(name+' (counterfactual only)', screen=altered))
    check('original artifacts remain unchanged', all(digest(p)==h for p,h in before.items()), len(before))
    summary = {'scope':'Archived v003 collection, ranking, log and screening audit; no live collection or adopted corrections',
        'checks':checks, 'checks_passed':sum(x['passed'] for x in checks),
        'checks_failed':[x for x in checks if not x['passed']],
        'query_count':len(queries), 'apple_first30_hits':sum(x['API Position']<=30 for x in raw_rows['apple']),
        'apple_first30_distinct':len(rank.pool(listings['apple'],30,queries)),
        'play_search_hits':sum(len(x) for x in raw['play']['search'].values()),
        'play_first30_hits':sum(x['Search Position']<=30 for z in raw['play']['search'].values() for x in z),
        'screening':{'total':len(screening_rows), 'decisions':Counter(x['decision'] for x in screening_rows),
                     'excluded_criteria':Counter(x['criterion'] for x in screening_rows if x['decision']=='excluded')},
        'missing_play_review_counts':len(missing), 'explicit_zero_play_review_counts':sum(x.get('Review Count')==0 for x in unique['play'].values()),
        'archived_page_hash_coverage':{'page_ids_with_hash':len(request_coverage),'total_pages':len(cache),
                                      'page_ids_without_hash':len(set(cache)-request_ids)},
        'cache_capture_dates':Counter(x['captured_at'][:10] for x in cache_rows),
        'identity_reference_mismatches':identity_issues, 'diagnostic_scenarios':scenarios,
        'input_sha256':before}
    (OUT/'audit.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('input_sha256','checks')},indent=2,ensure_ascii=True))


if __name__ == '__main__':
    main()
