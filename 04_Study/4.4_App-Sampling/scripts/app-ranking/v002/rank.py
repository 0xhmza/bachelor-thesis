"""Rank the store candidates and select the sample (D1, D2, D3, D6). Standard library only.

    python 04_Study/4.4_App-Sampling/scripts/app-ranking/v002/rank.py 04_Study/4.4_App-Sampling/scripts/app-ranking/v002/config.json
    python -I -m unittest discover -s 04_Study/4.4_App-Sampling/scripts/app-ranking/v002/tests

Reads one App Store and one Google Play collector output, the keyword table and the
screening decisions. Within each store, listings in the first `depth` results of any
keyword with at least `floor` ratings are ranked by rating count (ties by listing ID).
Apps are taken alternately from the two lists, starting with `start`; a listing is
skipped when its developer is already in the sample (the preinstalled vendors count).
Listings without a screening decision are treated as eligible and reported as pending;
the selection is final only when no decision is pending. Writes the selection, the
cascade, the sensitivity checks and a screening sheet to `out`.
"""
import csv, json, math, re, sys, unicodedata
from collections import Counter
from datetime import date, datetime
from pathlib import Path

LEGAL = {'inc', 'llc', 'ltd', 'limited', 'gmbh', 'co', 'corp', 'corporation', 'company', 'ag', 'sa',
         'sas', 'srl', 'bv', 'plc', 'pty', 'ug', 'kg', 'se', 'oy', 'ab', 'as', 'sl', 'spa', 'the', 'group',
         'uk', 'usa', 'europe', 'international', 'global'}  # legal forms and regional entities of one provider
MONTHS = {m: i for i, m in enumerate(['jan', 'feb', 'mär', 'apr', 'mai', 'jun', 'jul', 'aug', 'sep', 'okt', 'nov', 'dez'], 1)}


def provider_key(developer, aliases):
    plain = ''.join(c for c in unicodedata.normalize('NFKD', developer or '') if not unicodedata.combining(c))
    words = re.sub(r'[\W_]+', ' ', plain.lower().replace('&', ' and ')).split()
    key = ' '.join(w for w in words if w not in LEGAL) or (developer or '').strip().lower()
    return aliases.get(key, key)


def name_key(name):
    return set(re.sub(r'[\W_]+', ' ', (name or '').lower()).split())


def released(value):
    """Release date from an ISO string (Apple) or a German Play string such as '12.03.2015' or '12. März 2015'."""
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00')).date()
    except ValueError:
        pass
    m = re.match(r'(\d{1,2})\.\s*(\d{1,2}|[A-Za-zäÄ]+)\.?\s*(\d{4})', value)
    if m:
        month = int(m[2]) if m[2].isdigit() else MONTHS.get(m[2][:3].lower())
        return date(int(m[3]), month, int(m[1])) if month else None
    return None


def load(path, store, aliases):
    """Distinct listings of one collector output, with every keyword's position."""
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    listings = {}
    for query, rows in data['results'].items():
        for r in rows:
            lid = str(r['ID'])
            l = listings.setdefault(lid, {
                'store': store, 'id': lid, 'name': r.get('App Name'), 'developer': r.get('Dev. Name'),
                'provider': provider_key(r.get('Dev. Name'), aliases), 'genre': r.get('Genre'),
                'price': r.get('Price'), 'ratings': r.get('Rating Count'), 'rating': r.get('Average Rating'),
                'installs': r.get('Embedded Install Count'), 'min_installs': r.get('Minimum Installs'),
                'released': released(r.get('Released')), 'policy': r.get('Privacy Policy URL'),
                'description': (r.get('Summary') or '') + ' | ' + (r.get('Description') or ''),
                'positions': {}})
            l['positions'][query] = int(r.get('API Position') or r.get('Search Position'))
    return data, listings


def pool(listings, depth, queries):
    """Listings found within `depth` by at least one of `queries`, with their best position."""
    out = []
    for l in listings.values():
        hits = [p for q, p in l['positions'].items() if q in queries and p <= depth]
        if hits:
            out.append(dict(l, best=min(hits), found_by=sorted(q for q in queries if l['positions'].get(q, 99999) <= depth)))
    return out


def ranked(candidates, floor, removed, score=None):
    eligible = [l for l in candidates if (l['ratings'] or 0) >= floor and l['id'] not in removed]
    return sorted(eligible, key=score or (lambda l: (-l['ratings'], l['id'])))


def same_app(a, b):
    """Same provider and a similar name: half the words shared, or the same first word (store titles vary)."""
    na, nb = name_key(a['name']), name_key(b['name'])
    first = [re.sub(r'[\W_]+', ' ', (x['name'] or '').lower()).split()[:1] for x in (a, b)]
    return a['provider'] == b['provider'] and (len(na & nb) / max(1, len(na | nb)) >= 0.5
                                               or (first[0] == first[1] and len(first[0][0] if first[0] else '') >= 3))


def select(lists, screening, n, start, providers, provider_rule=True):
    """Alternate between the two ranked lists; return (selected, skipped, excluded, pending)."""
    order = [start, 'apple' if start == 'play' else 'play']
    pos, selected, skipped, excluded, pending = {s: 0 for s in order}, [], [], [], []
    taken = set(providers)
    turn = 0
    while len(selected) < n and any(pos[s] < len(lists[s]) for s in order):
        store = order[turn % 2] if pos[order[turn % 2]] < len(lists[order[turn % 2]]) else order[(turn + 1) % 2]
        turn += 1
        while pos[store] < len(lists[store]):
            l = lists[store][pos[store]]
            pos[store] += 1
            if (provider_rule and l['provider'] in taken) or (not provider_rule and any(same_app(l, s) for s in selected)):
                skipped.append(l)
                continue
            decision = screening.get((store, l['id']))
            if decision is None:
                pending.append(l)
            elif decision['decision'] != 'eligible':
                excluded.append((l, decision))
                continue
            selected.append(l)
            taken.add(l['provider'])
            break
    return selected, skipped, excluded, pending


def spearman(x, y):
    def ranks(v):
        order = sorted(range(len(v)), key=v.__getitem__)
        r = [0.0] * len(v)
        i = 0
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
    return cov / math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))


def counterpart(l, listings):
    """The same app in the other store's search results (any depth), most ratings first."""
    match = [o for o in listings.values() if same_app(o, l)]
    return max(match, key=lambda o: o['ratings'] or 0) if match else None


def main(config_path):
    cfg = json.loads(Path(config_path).read_text(encoding='utf-8'))
    aliases = cfg.get('aliases', {})
    out = Path(cfg['out'])
    out.mkdir(parents=True, exist_ok=True)
    keywords = list(csv.DictReader(open(cfg['keywords'], encoding='utf-8')))
    queries = {k['query'] for k in keywords}
    screening = {}
    if Path(cfg['screening']).exists():
        for r in csv.DictReader(open(cfg['screening'], encoding='utf-8')):
            screening[(r['store'], r['id'])] = r
    raw, listings = {}, {}
    for store in ('apple', 'play'):
        raw[store], listings[store] = load(cfg[store], store, aliases)
    assert set(raw['apple']['results']) == set(raw['play']['results']) == queries, 'keyword sets differ'
    removed = {s: set(cfg['preinstalled'].get(s, [])) for s in ('apple', 'play')}
    providers = {provider_key(p, aliases) for p in cfg['preinstalled_providers']}
    n, floor, today = cfg['n'], cfg['floor'], date.fromisoformat(raw['play']['timestamp'][:10])

    def run(depth=cfg['depth'], apple_depth=None, qs=queries, start=cfg['start'], provider_rule=True, score=None):
        lists = {s: ranked(pool(listings[s], apple_depth if s == 'apple' and apple_depth else depth, qs),
                           floor, removed[s], score and score(s)) for s in ('apple', 'play')}
        return select(lists, screening, n, start, providers, provider_rule), lists

    (sel, skipped, excluded, pending), lists = run()
    variants = {'no developer rule': dict(provider_rule=False), 'start with App Store': dict(start='apple'),
                'depth 20': dict(depth=20), 'App Store depth 200': dict(apple_depth=200),
                'English keywords only': dict(qs={k['query'] for k in keywords if 'en' in k['language']}),
                'German keywords only': dict(qs={k['query'] for k in keywords if 'de' in k['language']})}
    variants.update({f'without "{q}"': dict(qs=queries - {q}) for q in sorted(queries)})

    def per_year(store):
        return lambda l: (-(l['ratings'] / max(1.0, (today - l['released']).days / 365.25) if l['released'] else l['ratings']), l['id'])

    def blend(store, w=0.5):
        cands = ranked(pool(listings[store], cfg['depth'], queries), floor, removed[store])
        mean = sum(l['rating'] or 0 for l in cands) / max(1, len(cands))
        q = {l['id']: ((l['ratings'] * (l['rating'] or 0)) + floor * mean) / (l['ratings'] + floor) for l in cands}
        re_ = {l['id']: i for i, l in enumerate(cands, 1)}
        rq = {lid: i for i, lid in enumerate(sorted(q, key=lambda k: -q[k]), 1)}
        return lambda l: (w * re_.get(l['id'], 1e9) + (1 - w) * rq.get(l['id'], 1e9), -l['ratings'], l['id'])

    variants['rating count per year since release'] = dict(score=per_year)
    variants['blend with shrunk average rating (w = 0.5)'] = dict(score=blend)
    base = {l['provider'] for l in sel}
    rows, all_pending = [], {(l['store'], l['id']): l for l in pending}
    for name, kw in variants.items():
        (vsel, _, _, vpend), _ = run(**kw)
        for l in vpend:
            all_pending[(l['store'], l['id'])] = l
        rows.append({'variant': name, 'selected': len(vsel), 'providers': len({l['provider'] for l in vsel}),
                     'differ_from_main': len(base - {l['provider'] for l in vsel}), 'pending': len(vpend)})

    # Proxy check on the Google Play pool (D2), German exposure check and counterparts.
    play_pool = [l for l in pool(listings['play'], cfg['depth'], queries) if l['ratings'] is not None and l['installs']]
    proxy = {'n': len(play_pool), 'spearman_installs': spearman([l['ratings'] for l in play_pool], [l['installs'] for l in play_pool]),
             'spearman_band': spearman([l['ratings'] for l in play_pool], [l['min_installs'] or 0 for l in play_pool])}
    big = [l for l in play_pool if l['ratings'] >= floor]
    proxy.update({'n_floor': len(big), 'spearman_installs_floor': spearman([l['ratings'] for l in big], [l['installs'] for l in big])})
    selection = []
    for i, l in enumerate(sel, 1):
        other = counterpart(l, listings['apple' if l['store'] == 'play' else 'play'])
        d = screening.get((l['store'], l['id']), {})
        selection.append({'order': i, 'store': l['store'], 'id': l['id'], 'name': l['name'], 'developer': l['developer'],
                          'ratings': l['ratings'], 'rating': l['rating'], 'category': d.get('category', 'PENDING'),
                          'best_position': l['best'], 'keywords': len(l['found_by']), 'price': l['price'],
                          'policy_listed': bool(l['policy']) if l['store'] == 'play' else '',
                          'other_store_id': other['id'] if other else '', 'other_store_ratings': other['ratings'] if other else ''})
    cascade = {}
    for s in ('apple', 'play'):
        at_depth = pool(listings[s], cfg['depth'], queries)
        cascade[s] = {'queries': len(raw[s]['results']),
                      'hits_at_depth': sum(1 for l in listings[s].values() for p in l['positions'].values() if p <= cfg['depth']),
                      'distinct_at_depth': len(at_depth), 'preinstalled_removed': sum(l['id'] in removed[s] for l in at_depth),
                      'below_floor': sum((l['ratings'] or 0) < floor and l['id'] not in removed[s] for l in at_depth),
                      'ranked': len(lists[s]), 'selected': sum(l['store'] == s for l in sel),
                      'skipped_developer': sum(l['store'] == s for l in skipped),
                      'excluded': dict(Counter(d['criterion'] for l, d in excluded if l['store'] == s)),
                      'reached': lists_reached(lists[s], sel + skipped + [l for l, _ in excluded])}
    report = {'snapshot': {s: raw[s]['timestamp'] for s in raw}, 'n': n, 'floor': floor, 'depth': cfg['depth'],
              'selected': len(sel), 'pending': len(all_pending), 'cascade': cascade, 'proxy': proxy,
              'best_position': dict(Counter('1-10' if l['best'] <= 10 else '11-20' if l['best'] <= 20 else '21-30' for l in sel)),
              'one_keyword_only': sum(len(l['found_by']) == 1 for l in sel),
              'categories': dict(Counter(r['category'] for r in selection)),
              'play_selected_without_app_store_listing': sum(1 for r in selection if r['store'] == 'play' and not r['other_store_id']),
              'play_hits_without_id': raw['play'].get('hits_without_id', {}), 'play_errors': len(raw['play'].get('errors', {})),
              'play_search_hits': sum(raw['play'].get('hits', {}).values()), 'play_distinct_apps': raw['play'].get('distinct_apps'),
              'play_pages': raw['play'].get('pages'), 'play_band_cutoff': raw['play'].get('page_band_cutoff'),
              'play_apps_at_cutoff_without_page': raw['play'].get('apps_at_cutoff_without_page'),
              'play_selected_lowest_band': min((l['min_installs'] or 0 for l in sel if l['store'] == 'play'), default=None),
              'apple_hits_returned': sum(r['returned'] for r in raw['apple'].get('requests', {}).values()),
              'empty_queries': {s: [q for q, r in raw[s]['results'].items() if not r] for s in raw}}
    write(out / 'selection.csv', selection)
    write(out / 'sensitivity.csv', rows)
    write(out / 'excluded.csv', [{'store': l['store'], 'id': l['id'], 'name': l['name'], 'ratings': l['ratings'],
                                  'criterion': d['criterion'], 'reason': d['reason']} for l, d in excluded])
    write(out / 'screening-sheet.csv', [{'store': l['store'], 'id': l['id'], 'name': l['name'], 'developer': l['developer'],
                                         'genre': l['genre'], 'price': l['price'], 'ratings': l['ratings'],
                                         'found_by': '; '.join(l['found_by'][:6]), 'description': l['description'][:400].replace('\n', ' ')}
                                        for l in sorted(all_pending.values(), key=lambda l: (l['store'], -l['ratings']))])
    (out / 'report.json').write_text(json.dumps(report, indent=1, ensure_ascii=False, default=str), encoding='utf-8')
    if cfg.get('table') and not all_pending:
        pre = [dict(listings[s][i], category=c) for s, apps in cfg['preinstalled_table'].items() for i, c in apps.items()]
        write_table(Path(cfg['table']), selection, pre, raw['play']['timestamp'][:10])
    print(json.dumps({k: report[k] for k in ('selected', 'pending', 'proxy', 'categories')}, indent=1, default=str))


def tex(value):
    s = str(value if value is not None else '').replace('™', '').replace('®', '')
    s = unicodedata.normalize('NFKC', s).replace('—', '--').replace('–', '--')
    s = ''.join(c for c in s if ord(c) < 256).strip()
    return re.sub(r'([&%$#_{}])', r'\\\1', s).replace('~', r'\textasciitilde{}').replace('^', r'\textasciicircum{}')


def write_table(path, selection, preinstalled, day):
    """Longtable rows of the sample for the thesis appendix (generated; do not edit by hand)."""
    store = {'play': 'Google Play', 'apple': 'App Store'}
    lines = [f'% Generated by 04_Study/4.4_App-Sampling/scripts/app-ranking/v002/rank.py from the collection of {day}; do not edit by hand.']
    for r in selection:
        count = f"{r['ratings']:,}".replace(',', '{,}')
        lines.append(f"{r['order']} & {tex(r['name'])} & {tex(r['developer'])} & {store[r['store']]} & "
                     f"{tex(r['category'])} & {count} \\\\")
    for i, l in enumerate(preinstalled, len(selection) + 1):
        lines.append(f"{i} & {tex(l['name'])} & {tex(l['developer'])} & preinstalled & {tex(l['category'])} & -- \\\\")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def lists_reached(lst, seen):
    ids = {l['id'] for l in seen}
    return max((i for i, l in enumerate(lst, 1) if l['id'] in ids), default=0)


def write(path, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        if rows:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)


if __name__ == '__main__':
    main(sys.argv[1])
