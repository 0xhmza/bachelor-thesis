"""Check a Google Play candidate pool against the proposed selection rule (D1, D2).

Reports, for the apps a rating-count ranking would select: the domain mix, how
many places one developer takes, shared policy URLs, how deep in the search
results the selected apps were found, and how far the selection depends on
single keywords. Used for 00_Admin/App-Selection-Evaluation_2026-10-23.md.

    python scripts/sampling-checks/v001/check_pool.py scripts/googleplay-scraper/v002/output/pilot-de-19kw.json

INPUT is a googleplay-scraper v002 JSON. Standard library only. Domain is read
from the keywords that found an app; genre "Eltern" is reported as pregnancy.
"""
import argparse
import collections
import json
from pathlib import Path

FITNESS_KEYWORDS = {'Fitness', 'Fitness Tracker', 'Schrittzähler', 'Aktivitätstracker', 'Schlaf-Tracker',
    'Herzfrequenz', 'Kalorienzähler', 'Ernährungstagebuch', 'Workout'}
PREINSTALLED = {'com.sec.android.app.shealth'}  # Samsung Health moves to the D6 group


def pool(results, floor, skip=None):
    """Distinct listings at or above the floor, most ratings first; skip drops one keyword."""
    apps = {}
    for keyword, rows in results.items():
        if keyword == skip:
            continue
        for r in rows:
            a = apps.setdefault(r['ID'], dict(r, keywords=set(), positions={}))
            a['keywords'].add(keyword)
            a['positions'][keyword] = int(r['Search Position'])
    out = []
    for a in apps.values():
        try:
            a['ratings'] = int(a.get('Rating Count'))
        except (TypeError, ValueError):
            continue
        if a['ratings'] >= floor and a['ID'] not in PREINSTALLED:
            out.append(a)
    return sorted(out, key=lambda a: (-a['ratings'], a['ID']))


def domain(a):
    if a.get('Genre') == 'Eltern':
        return 'pregnancy'
    return 'fitness' if a['keywords'] <= FITNESS_KEYWORDS else 'fertility'


def one_per_developer(ranked, n):
    seen, out = set(), []
    for a in ranked:
        if a['Dev. Name'] not in seen:
            seen.add(a['Dev. Name'])
            out.append(a)
        if len(out) == n:
            break
    return out


def depth(a):
    best = min(a['positions'].values())
    return '1-5' if best <= 5 else '6-10' if best <= 10 else '11-15' if best <= 15 else '16-20'


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('input')
    ap.add_argument('--floor', type=int, default=1000)
    ap.add_argument('--top', type=int, nargs='+', default=[24, 47],
        help='selection sizes to check; 24 is the Play half under alternation, 47 the whole ranked sample')
    args = ap.parse_args(argv)
    data = json.loads(Path(args.input).read_text(encoding='utf-8'))
    results = data['results']
    ranked = pool(results, args.floor)
    print(f"{args.input}: snapshot {data.get('timestamp')}, {len(results)} keywords, "
          f"{len(ranked)} listings with >= {args.floor} ratings (preinstalled removed)")
    print('results per keyword:', {k: len(v) for k, v in results.items()})
    total = sum(a['ratings'] for a in ranked)
    for n in args.top:
        top = ranked[:n]
        devs = collections.Counter(a['Dev. Name'] for a in top)
        policies = collections.Counter((a.get('Privacy Policy URL') or '').split('?')[0] for a in top)
        alt = one_per_developer(ranked, n)
        print(f'\n== top {n} by rating count (smallest count {top[-1]["ratings"]:,}) ==')
        print('share of all ratings in the pool:', round(sum(a['ratings'] for a in top) / total, 3))
        print('domain mix:', dict(collections.Counter(domain(a) for a in top)))
        print('distinct developers:', len(devs), '| most places:', devs.most_common(3))
        print('policy URLs shared by several apps:', {u: c for u, c in policies.items() if c > 1 and u})
        print('best search position:', dict(collections.Counter(depth(a) for a in top)))
        print('found by one keyword only:', sum(len(a['keywords']) == 1 for a in top))
        print('one app per developer: mix', dict(collections.Counter(domain(a) for a in alt)),
              '| apps that differ from the main list:', len({a['ID'] for a in alt} - {a['ID'] for a in top}))
        ids = {a['ID'] for a in top}
        loko = sorted(((len(ids - {a['ID'] for a in pool(results, args.floor, k)[:n]}), k) for k in results), reverse=True)
        print('leave one keyword out, apps leaving the top list:', [f'{k}: {c}' for c, k in loko if c][:5])


if __name__ == '__main__':
    main()
