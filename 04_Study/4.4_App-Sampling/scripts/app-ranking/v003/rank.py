"""Rank the candidates of both stores on one German scale and select the sample (D1, D2, D3, D6).

    python 04_Study/4.4_App-Sampling/scripts/app-ranking/v003/rank.py 04_Study/4.4_App-Sampling/scripts/app-ranking/v003/config.json
    python -I -m unittest discover -s 04_Study/4.4_App-Sampling/scripts/app-ranking/v003/tests

German measures: r = App Store rating count in the German storefront, v = Google Play review
count in the German storefront. The same app in both stores is one candidate. Both counts are
put on one scale with the apps listed in both stores: c = median(v / r) * s_iOS / s_Android,
and German exposure E = v + c * r (units of German Google Play reviews). Candidates are ranked by
E; a candidate is skipped when its developer is already in the sample (preinstalled vendors
count); selection stops at n. Unscreened candidates count as eligible and are reported as
pending; the selection is final only when nothing is pending. Standard library only.
"""
import csv, json, re, statistics, sys, unicodedata
from collections import Counter
from pathlib import Path

LEGAL = {'inc', 'llc', 'ltd', 'limited', 'gmbh', 'co', 'corp', 'corporation', 'company', 'ag', 'sa',
         'sas', 'srl', 'bv', 'plc', 'pty', 'ug', 'kg', 'se', 'oy', 'ab', 'as', 'sl', 'spa', 'the', 'group',
         'uk', 'usa', 'europe', 'international', 'global'}  # legal forms and regional entities of one provider


DOTTED = [['sp', 'z', 'o', 'o'], ['j', 'd', 'o', 'o'], ['d', 'o', 'o'], ['s', 'r', 'l'], ['s', 'r', 'o'],
          ['b', 'v'], ['s', 'l'], ['s', 'a'], ['pte'], ['ou'], ['too']]  # legal forms written with dots


def provider_key(developer, aliases):
    plain = ''.join(ch for ch in unicodedata.normalize('NFKD', developer or '') if not unicodedata.combining(ch))
    words = [w for w in re.sub(r'[\W_]+', ' ', plain.lower().replace('&', ' and ')).split() if w not in LEGAL]
    stripped = True
    while stripped:
        stripped = False
        for suffix in DOTTED:
            if len(words) > len(suffix) and words[-len(suffix):] == suffix:
                words, stripped = words[:-len(suffix)], True
    key = ' '.join(words) or (developer or '').strip().lower()
    return aliases.get(key, key)


def words(name):
    return re.sub(r'[\W_]+', ' ', (name or '').lower()).split()


def same_app(a, b):
    """Same provider and a similar title: equal without spaces, half the words shared, or the same first word."""
    wa, wb = words(a['name']), words(b['name'])
    sa, sb = set(wa), set(wb)
    similar = (''.join(wa) == ''.join(wb) or len(sa & sb) / max(1, len(sa | sb)) >= 0.5
               or (wa[:1] == wb[:1] and wa and len(wa[0]) >= 3))
    return a['provider'] == b['provider'] and similar


def load(path, store, aliases):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    listings = {}
    for query, rows in data['results'].items():
        for row in rows:
            lid = str(row['ID'])
            l = listings.setdefault(lid, {
                'store': store, 'id': lid, 'name': row.get('App Name'), 'developer': row.get('Dev. Name'),
                'provider': provider_key(row.get('Dev. Name'), aliases), 'genre': row.get('Genre'),
                'price': row.get('Price'), 'world': row.get('Rating Count') or 0,
                'german': (row.get('Rating Count') if store == 'apple' else row.get('Review Count')) or 0,
                'description': (row.get('Summary') or '') + ' | ' + (row.get('Description') or ''),
                'positions': {}})
            l['positions'][query] = int(row.get('API Position') or row.get('Search Position'))
    return data, listings


def pool(listings, depth, queries):
    out = {}
    for lid, l in listings.items():
        hits = [p for q, p in l['positions'].items() if q in queries and p <= depth]
        if hits:
            out[lid] = dict(l, best=min(hits), found_by=sorted(q for q in queries if l['positions'].get(q, 10 ** 6) <= depth))
    return out


def candidates(apple, play, pairs=None):
    """One candidate per app: Google Play apps matched to their App Store listing, the rest alone.
    `pairs` maps a Play ID to an App Store ID for the same app under a translated title."""
    pairs = pairs or {}
    taken, out = set(), []
    for p in sorted(play.values(), key=lambda l: (-l['german'], l['id'])):
        fixed = pairs.get(p['id'])
        match = ([apple[fixed]] if fixed in apple and fixed not in taken else
                 [a for a in apple.values() if a['id'] not in taken and same_app(a, p)])
        a = max(match, key=lambda l: (l['german'], l['id'])) if match else None
        if a:
            taken.add(a['id'])
        out.append({'play': p, 'apple': a})
    out += [{'play': None, 'apple': a} for a in apple.values() if a['id'] not in taken]
    for c in out:
        main = c['play'] or c['apple']
        c.update(provider=main['provider'], name=main['name'], developer=main['developer'],
                 key=('play:' + c['play']['id']) if c['play'] else ('apple:' + c['apple']['id']),
                 r=c['apple']['german'] if c['apple'] else 0, v=c['play']['german'] if c['play'] else 0,
                 rw=c['apple']['german'] if c['apple'] else 0, vw=c['play']['world'] if c['play'] else 0)
    return out


def calibration(cands, s_ios, s_android, field='v'):
    ratios = [c[field] / c['r'] for c in cands if c['play'] and c['apple'] and c[field] > 0 and c['r'] > 0]
    return statistics.median(ratios) * s_ios / s_android, len(ratios)


def decision(c, screening):
    found = [screening[(l['store'], l['id'])] for l in (c['play'], c['apple']) if l and (l['store'], l['id']) in screening]
    if not found:
        return None
    bad = [d for d in found if d['decision'] != 'eligible']
    return bad[0] if bad else found[0]


def select(ranked, screening, n, providers, provider_rule=True):
    taken, sel, skipped, excluded, pending = set(providers), [], [], [], []
    for c in ranked:
        if len(sel) == n:
            break
        if provider_rule and c['provider'] in taken:
            skipped.append(c)
            continue
        d = decision(c, screening)
        if d is None:
            pending.append(c)
        elif d['decision'] != 'eligible':
            excluded.append((c, d))
            continue
        sel.append(c)
        taken.add(c['provider'])
    return sel, skipped, excluded, pending


def spearman(x, y):
    def ranks(v):
        order = sorted(range(len(v)), key=v.__getitem__)
        r, i = [0.0] * len(v), 0
        while i < len(v):
            j = i
            while j + 1 < len(v) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2 + 1
            i = j + 1
        return r
    rx, ry = ranks(x), ranks(y)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    cov = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    return cov / (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5


def tex(value):
    s = str(value if value is not None else '').replace('™', '').replace('®', '')
    s = unicodedata.normalize('NFKC', s).replace('—', '--').replace('–', '--')
    s = ''.join(ch for ch in s if ord(ch) < 256).strip()
    return re.sub(r'([&%$#_{}])', r'\\\1', s).replace('~', r'\textasciitilde{}').replace('^', r'\textasciicircum{}')


def num(n):
    return f'{n:,}'.replace(',', '{,}') if n else '--'


def write(path, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        if rows:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)


def main(config_path):
    cfg = json.loads(Path(config_path).read_text(encoding='utf-8'))
    aliases, out = cfg.get('aliases', {}), Path(cfg['out'])
    out.mkdir(parents=True, exist_ok=True)
    keywords = list(csv.DictReader(open(cfg['keywords'], encoding='utf-8')))
    queries = {k['query'] for k in keywords}
    screening = {(r['store'], r['id']): r for r in csv.DictReader(open(cfg['screening'], encoding='utf-8'))}
    raw, listings = {}, {}
    for store in ('apple', 'play'):
        raw[store], listings[store] = load(cfg[store], store, aliases)
    removed = {s: set(cfg['preinstalled'].get(s, [])) for s in ('apple', 'play')}
    providers = {provider_key(p, aliases) for p in cfg['preinstalled_providers']}
    s_ios, s_and, n = cfg['os_share']['ios'], cfg['os_share']['android'], cfg['n']

    def build(depth=cfg['depth'], apple_depth=None, qs=queries):
        pools = {s: {k: l for k, l in pool(listings[s], apple_depth if s == 'apple' and apple_depth else depth, qs).items()
                     if k not in removed[s]} for s in ('apple', 'play')}
        return candidates(pools['apple'], pools['play'], cfg.get('pairs')), pools

    def ranked(cands, score):
        return sorted(cands, key=lambda c: (-score(c), c['key']))

    def german(cands, si=s_ios, sa=s_and):
        c, _ = calibration(cands, si, sa)
        return lambda x: x['v'] + c * x['r']

    def run(score_of=german, provider_rule=True, **kw):
        cands, pools = build(**kw)
        return select(ranked(cands, score_of(cands)), screening, n, providers, provider_rule), cands, pools

    (sel, skipped, excluded, pending), cands, pools = run()
    c_main, n_pairs = calibration(cands, s_ios, s_and)
    score = german(cands)

    def pool_share(cs):
        R, V = sum(x['r'] for x in cs), sum(x['v'] for x in cs)
        return lambda x: s_ios * x['r'] / R + s_and * x['v'] / V

    def worldwide(cs):
        c, _ = calibration(cs, s_ios, s_and, field='vw')
        return lambda x: x['vw'] + c * x['r']

    variants = {'no developer rule': dict(provider_rule=False),
                'equal platform weights': dict(score_of=lambda cs: german(cs, 0.5, 0.5)),
                'pool-sum scale (first formula)': dict(score_of=pool_share),
                'worldwide Play rating count instead of German reviews': dict(score_of=worldwide),
                'depth 20': dict(depth=20), 'App Store depth 200': dict(apple_depth=200),
                'English keywords only': dict(qs={k['query'] for k in keywords if 'en' in k['language']}),
                'German keywords only': dict(qs={k['query'] for k in keywords if 'de' in k['language']})}
    variants.update({f'without "{q}"': dict(qs=queries - {q}) for q in sorted(queries)})
    base = {c['provider'] for c in sel}
    rows, all_pending = [], {c['key']: c for c in pending}
    for name, kw in variants.items():
        (vsel, _, _, vpend), _, _ = run(**kw)
        all_pending.update({c['key']: c for c in vpend})
        rows.append({'variant': name, 'selected': len(vsel), 'providers': len({c['provider'] for c in vsel}),
                     'differ_from_main': len(base - {c['provider'] for c in vsel}), 'pending': len(vpend)})
    if cfg.get('compare_selection') and Path(cfg['compare_selection']).exists():
        old = list(csv.DictReader(open(cfg['compare_selection'], encoding='utf-8')))
        oldp = {provider_key(r['developer'], aliases) for r in old}
        rows.append({'variant': 'previous method (store alternation, worldwide Play count)', 'selected': len(old),
                     'providers': len(oldp), 'differ_from_main': len(base - oldp), 'pending': 0})

    both = [c for c in cands if c['play'] and c['apple'] and c['r'] > 0 and c['v'] > 0]
    play_all = [c for c in cands if c['play']]
    selection = []
    for i, c in enumerate(sel, 1):
        d = decision(c, screening) or {}
        selection.append({'order': i, 'name': c['name'], 'developer': c['developer'],
                          'stores': '+'.join(s for s in ('apple', 'play') if c[s]),
                          'apple_id': c['apple']['id'] if c['apple'] else '', 'play_id': c['play']['id'] if c['play'] else '',
                          'german_ratings_app_store': c['r'], 'german_reviews_google_play': c['v'],
                          'exposure': round(score(c)), 'category': d.get('category', 'PENDING'),
                          'best_position': min(l['best'] for l in (c['play'], c['apple']) if l)})
    report = {'snapshot': {s: raw[s]['timestamp'] for s in raw}, 'n': n, 'depth': cfg['depth'],
              'os_share': cfg['os_share'], 'calibration': {'c': c_main, 'pairs': n_pairs,
              'median_v_over_r': c_main * s_and / s_ios},
              'spearman_r_v_both_stores': {'n': len(both), 'rho': spearman([c['r'] for c in both], [c['v'] for c in both])},
              'spearman_german_vs_worldwide_play': {'n': len(play_all), 'rho': spearman([c['v'] for c in play_all], [c['vw'] for c in play_all])},
              'candidates': {'total': len(cands), 'both_stores': sum(1 for c in cands if c['play'] and c['apple']),
                             'app_store_only': sum(1 for c in cands if not c['play']), 'google_play_only': sum(1 for c in cands if not c['apple'])},
              'pool': {s: len(pools[s]) for s in pools}, 'selected': len(sel), 'pending': len(all_pending),
              'reached': len(sel) + len(skipped) + len(excluded), 'skipped_developer': len(skipped),
              'excluded': dict(Counter(d['criterion'] for _, d in excluded)),
              'selected_stores': dict(Counter(r['stores'] for r in selection)),
              'categories': dict(Counter(r['category'] for r in selection)),
              'best_position': dict(Counter('1-10' if r['best_position'] <= 10 else '11-20' if r['best_position'] <= 20 else '21-30' for r in selection)),
              'lowest_selected_exposure': min((r['exposure'] for r in selection), default=None)}
    write(out / 'selection.csv', selection)
    write(out / 'sensitivity.csv', rows)
    write(out / 'excluded.csv', [{'name': c['name'], 'developer': c['developer'], 'criterion': d['criterion'],
                                  'reason': d['reason']} for c, d in excluded])
    sheet = []
    for c in sorted(all_pending.values(), key=lambda c: -score(c)):
        for l in (c['play'], c['apple']):
            if l:
                sheet.append({'store': l['store'], 'id': l['id'], 'name': l['name'], 'developer': l['developer'],
                              'genre': l['genre'], 'price': l['price'], 'german': l['german'], 'exposure': round(score(c)),
                              'found_by': '; '.join(l['found_by'][:6]), 'description': l['description'][:400].replace('\n', ' ')})
                break
    write(out / 'screening-sheet.csv', sheet)
    (out / 'report.json').write_text(json.dumps(report, indent=1, ensure_ascii=False, default=str), encoding='utf-8')
    if cfg.get('table') and not all_pending:
        store = {'apple': 'App Store', 'play': 'Google Play', 'apple+play': 'both'}
        lines = [f"% Generated by 04_Study/4.4_App-Sampling/scripts/app-ranking/v003/rank.py from the collections of {report['snapshot']['apple'][:10]} "
                 f"and {report['snapshot']['play'][:10]}; do not edit by hand."]
        for r in selection:
            lines.append(f"{r['order']} & {tex(r['name'])} & {tex(r['developer'])} & {store[r['stores']]} & {tex(r['category'])} & "
                         f"{num(r['german_ratings_app_store'])} & {num(r['german_reviews_google_play'])} \\\\")
        for i, (s, ids) in enumerate(((s, i) for s, apps in cfg['preinstalled_table'].items() for i in apps.items()), len(selection) + 1):
            l = listings[s][ids[0]]
            lines.append(f"{i} & {tex(l['name'])} & {tex(l['developer'])} & preinstalled & {tex(ids[1])} & -- & -- \\\\")
        Path(cfg['table']).write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps({k: report[k] for k in ('selected', 'pending', 'calibration', 'spearman_r_v_both_stores',
                                             'selected_stores', 'categories')}, indent=1, default=str))


if __name__ == '__main__':
    main(sys.argv[1])
