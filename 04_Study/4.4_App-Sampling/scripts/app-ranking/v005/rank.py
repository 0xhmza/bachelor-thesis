"""Rank the candidates of both stores on one German scale and select the sample (D1, D2, D3, D6).

    python 04_Study/4.4_App-Sampling/scripts/app-ranking/v005/rank.py 04_Study/4.4_App-Sampling/scripts/app-ranking/v005/config.json
    python -I -m unittest discover -s 04_Study/4.4_App-Sampling/scripts/app-ranking/v005/tests

German measures: r = App Store rating count in the German storefront, v = Google Play review
count in the German storefront. The same app in both stores is one candidate. Both counts are
put on one scale with the apps listed in both stores: c = median(v / r) * s_iOS / s_Android,
and the German-market popularity score P = v + c * r (units of German Google Play reviews).
Candidates are ranked by P; a candidate is skipped when its provider is already in the sample
(preinstalled vendors count); selection stops at n. Unscreened candidates count as eligible and
are reported as pending.

Product identity (D2, 28 October 2026): a Google Play and an App Store listing are one app only
where the identity register records them as the same product. Pairs of listings that share the
developer, the app identifier, the normalised title or rare passages of description text are
proposed for review; a proposal decides nothing, and rating counts and input order play no part.
Both listings of one product belong to one provider. The run is final, and writes the thesis
tables and the dataset, only when nothing is pending: every candidate reached is screened, every
proposal in every frame has a decision, and counting the unresolved pairs as the same product
changes no selected listing in the main selection or any check.

Provider identity (D2): listings of one store developer account must share a provider; names
are compared after normalisation; other spellings are matched by hand in `aliases`, each with
its evidence. Distinct providers whose reached listings name the same web domain are listed
for review and must be merged by an alias or recorded in `distinct`. Standard library only.
"""
import csv, json, re, statistics, sys, unicodedata
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from urllib.parse import urlsplit

LEGAL = {'inc', 'llc', 'ltd', 'limited', 'gmbh', 'co', 'corp', 'corporation', 'company', 'ag', 'sa',
         'sas', 'srl', 'bv', 'plc', 'pty', 'ug', 'kg', 'se', 'oy', 'ab', 'as', 'sl', 'spa', 'the', 'group',
         'uk', 'usa', 'europe', 'international', 'global'}  # legal forms and regional entities of one provider


DOTTED = [['sp', 'z', 'o', 'o'], ['j', 'd', 'o', 'o'], ['d', 'o', 'o'], ['s', 'r', 'l'], ['s', 'r', 'o'],
          ['b', 'v'], ['s', 'l'], ['s', 'a'], ['pte'], ['ou'], ['too']]  # legal forms written with dots

DECISIONS = {'same', 'different', 'unresolved'}
EVIDENCE = {'web', 'id', 'name', 'en-name', 'text', 'listing'}
# web: an official page links both store IDs; id: identical app identifier; name: the same product
# name in both titles; en-name: the same product name in both English store names; text: shared
# passages of description text; listing: one listing names the product of the other.


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


HOSTS = {'google.com', 'github.io', 'firebaseapp.com', 'web.app', 'notion.site', 'wixsite.com',
         'blogspot.com', 'wordpress.com', 'termly.io', 'iubenda.com', 'privacypolicies.com',
         'freeprivacypolicy.com', 'app-privacy-policy.com', 'apple.com', 'facebook.com', 'linktr.ee'}
# hosting and policy-generator domains used by many unrelated developers


def domain(url):
    """Registered domain of a listing link: www.helloclue.com/privacy -> helloclue.com."""
    host = (urlsplit(url if '//' in url else '//' + url).hostname or '').removeprefix('www.')
    parts = host.split('.')
    n = 3 if len(parts) > 2 and parts[-2] in ('co', 'com', 'org', 'net', 'ac', 'gov') and len(parts[-1]) == 2 else 2
    return '.'.join(parts[-n:])


def account_conflicts(listings):
    """Store developer accounts whose listings fall under more than one developer key."""
    keys = defaultdict(set)
    for store in listings:
        for l in listings[store].values():
            if l['account']:
                keys[(store, l['account'])].add(l['developer_key'])
    return {k: sorted(v) for k, v in keys.items() if len(v) > 1}


def shared_domains(cands):
    """Pairs of distinct providers whose listings name the same web domain."""
    owners = defaultdict(set)
    for c in cands:
        for l in (c['play'], c['apple']):
            for d in (l['domains'] if l else ()):
                owners[d].add(c['provider'])
    return sorted((a, b, d) for d, ps in owners.items() for a, b in combinations(sorted(ps), 2))


def words(name):
    return re.sub(r'[\W_]+', ' ', (name or '').lower()).split()


def passages(text, k=4):
    """The sequences of k words in a listing text, markup removed."""
    w = re.findall(r'\w+', re.sub(r'<[^>]+>', ' ', text or '').lower())
    return {' '.join(w[i:i + k]) for i in range(len(w) - k + 1)}


def proposals(apple, play, min_shared=20, max_listings=10):
    """Pairs of listings to review for product identity, with the reasons for proposing them: the same
    developer key, the same app identifier (bundle ID = package name), the same normalised title, or at
    least `min_shared` passages of description text that occur in at most `max_listings` listings.
    A proposal decides nothing."""
    text = {(l['store'], l['id']): passages(l['description']) for s in (apple, play) for l in s.values()}
    df = Counter(p for v in text.values() for p in v)
    rare, by_dev, by_id, by_title = defaultdict(set), defaultdict(set), defaultdict(set), defaultdict(set)
    for a in apple.values():
        for p in text[('apple', a['id'])]:
            if df[p] <= max_listings:
                rare[p].add(a['id'])
        by_dev[a['developer_key']].add(a['id'])
        if a['bundle']:
            by_id[a['bundle'].lower()].add(a['id'])
        by_title[' '.join(words(a['name']))].add(a['id'])
    out = {}
    for p in play.values():
        shared = Counter(a for t in text[('play', p['id'])] if df[t] <= max_listings for a in rare[t])
        reasons = defaultdict(list)
        for why, found in (('developer', by_dev.get(p['developer_key'], ())), ('app-id', by_id.get(p['id'].lower(), ())),
                           ('title', by_title.get(' '.join(words(p['name'])), ())),
                           ('text', [a for a, k in shared.items() if k >= min_shared])):
            for a in found:
                reasons[a].append(why)
        for a, why in reasons.items():
            out[(p['id'], a)] = {'reasons': why, 'shared_passages': shared.get(a, 0)}
    return out


def identity_errors(rows, listings):
    """Register rows that cannot be used: unknown listings, invalid decisions or evidence, missing
    rationale or reviewer, a pair listed twice, or one listing in more than one same-product pair."""
    errors = [f'pair listed twice: {k}' for k, n in Counter((r['play_id'], r['apple_id']) for r in rows).items() if n > 1]
    for r in rows:
        k, codes = (r['play_id'], r['apple_id']), {e.strip() for e in r['evidence'].split(';') if e.strip()}
        if r['play_id'] not in listings['play'] or r['apple_id'] not in listings['apple']:
            errors.append(f'{k}: listing not in the collections')
        if r['decision'] not in DECISIONS:
            errors.append(f'{k}: decision {r["decision"]!r}')
        if codes - EVIDENCE:
            errors.append(f'{k}: unknown evidence {sorted(codes - EVIDENCE)}')
        if r['decision'] == 'same' and not codes:
            errors.append(f'{k}: same product without product-specific evidence')
        if not (r['rationale'].strip() and r['reviewer'].strip() and r['review_date'].strip()):
            errors.append(f'{k}: rationale, reviewer or review date missing')
    for col in ('play_id', 'apple_id'):
        errors += [f'{col} {i} in {n} same-product pairs' for i, n in
                   Counter(r[col] for r in rows if r['decision'] == 'same').items() if n > 1]
    return errors


def merge_providers(listings, pairs):
    """Both listings of one product belong to one provider: join their developer keys. Returns the
    function that maps a developer key to its provider (the alphabetically first key of its group)."""
    parent = {}

    def find(k):
        while parent.get(k, k) != k:
            k = parent[k]
        return k
    for p, a in sorted(pairs):
        x, y = sorted((find(listings['play'][p]['developer_key']), find(listings['apple'][a]['developer_key'])))
        if x != y:
            parent[y] = x
    return find


def load(path, store, aliases):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    listings = {}
    for query, rows in data['results'].items():
        for row in rows:
            lid = str(row['ID'])
            l = listings.setdefault(lid, {
                'store': store, 'id': lid, 'name': row.get('App Name'), 'developer': row.get('Dev. Name'),
                'developer_key': provider_key(row.get('Dev. Name'), aliases), 'genre': row.get('Genre'),
                'price': row.get('Price'), 'world': row.get('Rating Count') or 0,
                'german': (row.get('Rating Count') if store == 'apple' else row.get('Review Count')) or 0,
                'description': (row.get('Summary') or '') + ' | ' + (row.get('Description') or ''),
                'bundle': (row.get('Bundle ID') or '') if store == 'apple' else lid,
                'account': str(row.get('Dev. ID') or ''), 'positions': {},
                'domains': {domain(u) for u in (row.get('Seller URL'), row.get('Developer Website'),
                                                row.get('Privacy Policy URL')) if u} - HOSTS})
            l['positions'][query] = int(row.get('API Position') or row.get('Search Position'))
    return data, listings


def pool(listings, depth, queries):
    out = {}
    for lid, l in listings.items():
        hits = [p for q, p in l['positions'].items() if q in queries and p <= depth]
        if hits:
            out[lid] = dict(l, best=min(hits), found_by=sorted(q for q in queries if l['positions'].get(q, 10 ** 6) <= depth))
    return out


def candidates(apple, play, same=(), find=lambda k: k):
    """One candidate per app: listings recorded as one product are merged, every other listing stands
    alone. Rating counts and the order of the listings play no part."""
    pairs = sorted((p, a) for p, a in same if p in play and a in apple)
    out = [{'play': play[p], 'apple': apple[a]} for p, a in pairs]
    paired = {('play', p) for p, _ in pairs} | {('apple', a) for _, a in pairs}
    out += [{'play': l, 'apple': None} for k, l in sorted(play.items()) if ('play', k) not in paired]
    out += [{'play': None, 'apple': l} for k, l in sorted(apple.items()) if ('apple', k) not in paired]
    for c in out:
        main = c['play'] or c['apple']
        c.update(provider=find(main['developer_key']), name=main['name'], developer=main['developer'],
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


def listings_of(sel):
    """The store listings of selected candidates, as (store, id)."""
    return {(l['store'], l['id']) for c in sel for l in (c['play'], c['apple']) if l}


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


def write(path, rows, fields=None):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        if rows or fields:
            w = csv.DictWriter(f, fieldnames=fields or list(rows[0]))
            w.writeheader()
            w.writerows(rows)


def main(config_path):
    cfg = json.loads(Path(config_path).read_text(encoding='utf-8'))
    aliases, out = cfg.get('aliases', {}), Path(cfg['out'])
    out.mkdir(parents=True, exist_ok=True)
    keywords = list(csv.DictReader(open(cfg['keywords'], encoding='utf-8')))
    queries = {k['query'] for k in keywords}
    screening = {(r['store'], r['id']): r for r in csv.DictReader(open(cfg['screening'], encoding='utf-8'))}
    register = list(csv.DictReader(open(cfg['identity'], encoding='utf-8'))) if Path(cfg['identity']).exists() else []
    raw, listings = {}, {}
    for store in ('apple', 'play'):
        raw[store], listings[store] = load(cfg[store], store, aliases)
    names = {provider_key(l['developer'], {}) for s in listings for l in listings[s].values()}
    unused, conflicts = sorted(set(aliases) - names), account_conflicts(listings)
    if unused or conflicts:
        raise SystemExit(f'aliases that match no developer: {unused}; accounts under several providers: {conflicts}')
    errors = identity_errors(register, listings)
    if errors:
        raise SystemExit('identity register: ' + '; '.join(errors[:20]))
    decided = {(r['play_id'], r['apple_id']): r for r in register}
    same = {k for k, r in decided.items() if r['decision'] == 'same'}
    unresolved = {k for k, r in decided.items() if r['decision'] == 'unresolved'}
    removed = {s: set(cfg['preinstalled'].get(s, [])) for s in ('apple', 'play')}
    s_ios, s_and, n = cfg['os_share']['ios'], cfg['os_share']['android'], cfg['n']

    variants = {'no developer rule': dict(provider_rule=False),
                'equal platform weights': dict(score='equal'),
                'pool-sum scale (first formula)': dict(score='pool'),
                'worldwide Play rating count instead of German reviews': dict(score='worldwide'),
                'depth 20': dict(depth=20), 'App Store depth 200': dict(apple_depth=200),
                'English keywords only': dict(qs={k['query'] for k in keywords if 'en' in k['language']}),
                'German keywords only': dict(qs={k['query'] for k in keywords if 'de' in k['language']})}
    variants.update({f'without "{q}"': dict(qs=queries - {q}) for q in sorted(queries)})

    # Every pair that any run could merge is proposed for review, in the union of the frames used.
    frames = [(kw.get('depth', cfg['depth']), kw.get('apple_depth') or kw.get('depth', cfg['depth']))
              for kw in [{}] + list(variants.values())]
    union = {s: {k: l for k, l in pool(listings[s], max(f[s == 'apple'] for f in frames), queries).items()
                 if k not in removed[s]} for s in ('play', 'apple')}
    proposed = proposals(union['apple'], union['play'])
    undecided = sorted(k for k in proposed if k not in decided)
    main_frame = {s: set(pool(listings[s], cfg['depth'], queries)) for s in ('play', 'apple')}
    write(out / 'identity-review.csv', [
        {'play_id': p, 'apple_id': a, 'play_name': union['play'][p]['name'], 'apple_name': union['apple'][a]['name'],
         'play_developer': union['play'][p]['developer'], 'apple_developer': union['apple'][a]['developer'],
         'bundle': union['apple'][a]['bundle'], 'reasons': '+'.join(proposed[(p, a)]['reasons']),
         'shared_passages': proposed[(p, a)]['shared_passages'], 'main_frame': p in main_frame['play'] and a in main_frame['apple'],
         'v': union['play'][p]['german'], 'r': union['apple'][a]['german']}
        for p, a in sorted(undecided, key=lambda k: (-(union['play'][k[0]]['german'] + union['apple'][k[1]]['german']), k))],
        ['play_id', 'apple_id', 'play_name', 'apple_name', 'play_developer', 'apple_developer', 'bundle', 'reasons',
         'shared_passages', 'main_frame', 'v', 'r'])
    if not same:
        raise SystemExit(f'no same-product pairs in the identity register; {len(undecided)} proposals in identity-review.csv')

    def build(ident, find, depth=cfg['depth'], apple_depth=None, qs=queries):
        pools = {s: {k: l for k, l in pool(listings[s], apple_depth if s == 'apple' and apple_depth else depth, qs).items()
                     if k not in removed[s]} for s in ('apple', 'play')}
        return candidates(pools['apple'], pools['play'], ident, find), pools

    def ranked(cands, score):
        return sorted(cands, key=lambda c: (-score(c), c['key']))

    def scorer(cands, score='german'):
        if score == 'pool':
            R, V = sum(x['r'] for x in cands), sum(x['v'] for x in cands)
            return lambda x: s_ios * x['r'] / R + s_and * x['v'] / V
        if score == 'worldwide':
            c, _ = calibration(cands, s_ios, s_and, field='vw')
            return lambda x: x['vw'] + c * x['r']
        c, _ = calibration(cands, *((0.5, 0.5) if score == 'equal' else (s_ios, s_and)))
        return lambda x: x['v'] + c * x['r']

    def scenario(ident):
        find = merge_providers(listings, ident)
        providers = {find(provider_key(p, aliases)) for p in cfg['preinstalled_providers']}

        def run(score='german', provider_rule=True, **kw):
            cands, pools = build(ident, find, **kw)
            return select(ranked(cands, scorer(cands, score)), screening, n, providers, provider_rule), cands, pools
        return run, find, providers

    run, find, providers = scenario(same)
    (sel, skipped, excluded, pending), cands, pools = run()
    c_main, n_pairs = calibration(cands, s_ios, s_and)
    score = scorer(cands)
    base, base_listings = {c['provider'] for c in sel}, listings_of(sel)
    rows, all_pending, results = [], {c['key']: c for c in pending}, {'main': listings_of(sel)}
    for name, kw in variants.items():
        (vsel, _, _, vpend), _, _ = run(**kw)
        all_pending.update({c['key']: c for c in vpend})
        results[name] = listings_of(vsel)
        rows.append({'variant': name, 'selected': len(vsel), 'providers': len({c['provider'] for c in vsel}),
                     'differ_from_main': len(base - {c['provider'] for c in vsel}),
                     'listings_differ': len(base_listings - results[name]),
                     'order_changes': sum(a['key'] != b['key'] for a, b in zip(sel, vsel)) + abs(len(sel) - len(vsel)),
                     'pending': len(vpend)})
    if cfg.get('compare_selection') and Path(cfg['compare_selection']).exists():
        old = list(csv.DictReader(open(cfg['compare_selection'], encoding='utf-8')))
        oldp = {find(provider_key(r['developer'], aliases)) for r in old}
        oldl = {(r['store'], r['id']) for r in old} | {('apple' if r['store'] == 'play' else 'play', r['other_store_id'])
                                                      for r in old if r.get('other_store_id')}
        rows.append({'variant': 'previous method (store alternation, worldwide Play count)', 'selected': len(old),
                     'providers': len(oldp), 'differ_from_main': len(base - oldp), 'listings_differ': len(base_listings - oldl),
                     'order_changes': '', 'pending': 0})

    # Unresolved pairs: repeat every run with them counted as the same product.
    used = {p for p, _ in same} | {a for _, a in same}
    testable = sorted(k for k in unresolved if not ({k[0], k[1]} & used))
    clash = [k for k, m in Counter(x for k in testable for x in k).items() if m > 1]
    untested = sorted(set(k for k in unresolved if k not in testable) | {k for k in testable if set(k) & set(clash)})
    affected = []
    if unresolved:
        alt_run, _, _ = scenario(same | (set(testable) - set(untested)))
        for name, kw in [('main', {})] + list(variants.items()):
            (asel, _, _, apend), _, _ = alt_run(**kw)
            all_pending.update({c['key']: c for c in apend})
            if listings_of(asel) != results[name]:
                affected.append(name)

    both = [c for c in cands if c['play'] and c['apple'] and c['r'] > 0 and c['v'] > 0]
    play_all = [c for c in cands if c['play']]
    selection = []
    for i, c in enumerate(sel, 1):
        d = decision(c, screening) or {}
        selection.append({'order': i, 'name': c['name'], 'developer': c['developer'],
                          'stores': '+'.join(s for s in ('apple', 'play') if c[s]),
                          'apple_id': c['apple']['id'] if c['apple'] else '', 'play_id': c['play']['id'] if c['play'] else '',
                          'german_ratings_app_store': c['r'], 'german_reviews_google_play': c['v'],
                          'popularity': round(score(c)), 'category': d.get('category', 'PENDING'),
                          'best_position': min(l['best'] for l in (c['play'], c['apple']) if l), 'provider': c['provider']})
    reached = ranked(cands, score)[:len(sel) + len(skipped) + len(excluded)]
    review = [{'provider_a': a, 'provider_b': b, 'domain': d, 'decision': cfg.get('distinct', {}).get(f'{a} | {b}', 'PENDING')}
              for a, b, d in shared_domains(reached)]
    unreviewed = [r for r in review if r['decision'] == 'PENDING']
    (nodev, _, _, _), _, _ = run(provider_rule=False)
    joined = sorted({(listings['play'][p]['developer'], listings['apple'][a]['developer'], p, a) for p, a in same
                     if listings['play'][p]['developer_key'] != listings['apple'][a]['developer_key']},
                    key=lambda j: (listings['play'][j[2]]['name'].casefold(), j[2], j[3]))
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
              'lowest_selected_popularity': min((r['popularity'] for r in selection), default=None),
              'selected_ranges': {'r': [min((x['r'] for x in sel if x['apple']), default=None), max((x['r'] for x in sel if x['apple']), default=None)],
                                  'v': [min((x['v'] for x in sel if x['play']), default=None), max((x['v'] for x in sel if x['play']), default=None)]},
              'identity': {'register_rows': len(register), 'decisions': dict(Counter(r['decision'] for r in register)),
                           'proposals': len(proposed), 'proposal_reasons': dict(Counter('+'.join(v['reasons']) for v in proposed.values())),
                           'undecided': len(undecided), 'unresolved': len(unresolved), 'unresolved_untested': len(untested),
                           'runs_changed_by_unresolved': affected, 'same_pairs_joining_developers': len(joined),
                           'union_frame': {s: len(union[s]) for s in union}},
              'provider_review': {'pairs': len(review), 'pending': len(unreviewed), 'aliases': len(aliases)},
              'no_developer_rule': {'providers': len({c['provider'] for c in nodev}),
                                    'providers_with_several_apps': {p: k for p, k in Counter(c['provider'] for c in nodev).items() if k > 1}}}
    write(out / 'selection.csv', selection)
    write(out / 'provider-review.csv', review, ['provider_a', 'provider_b', 'domain', 'decision'])
    write(out / 'sensitivity.csv', rows)
    write(out / 'excluded.csv', [{'name': c['name'], 'developer': c['developer'], 'criterion': d['criterion'],
                                  'reason': d['reason']} for c, d in excluded], ['name', 'developer', 'criterion', 'reason'])
    sheet = []
    for c in sorted(all_pending.values(), key=lambda c: -score(c)):
        for l in (c['play'], c['apple']):
            if l:
                sheet.append({'store': l['store'], 'id': l['id'], 'name': l['name'], 'developer': l['developer'],
                              'genre': l['genre'], 'price': l['price'], 'german': l['german'], 'popularity': round(score(c)),
                              'found_by': '; '.join(l['found_by'][:6]), 'description': l['description'][:400].replace('\n', ' ')})
                break
    write(out / 'screening-sheet.csv', sheet, ['store', 'id', 'name', 'developer', 'genre', 'price', 'german', 'popularity', 'found_by', 'description'])
    (out / 'report.json').write_text(json.dumps(report, indent=1, ensure_ascii=False, default=str), encoding='utf-8')
    problems = [m for m, k in ((f'{len(all_pending)} unscreened candidates (screening-sheet.csv)', all_pending),
                               (f'{len(unreviewed)} provider pairs to review (provider-review.csv)', unreviewed),
                               (f'{len(undecided)} identity proposals without a decision (identity-review.csv)', undecided),
                               (f'{len(untested)} unresolved identities that cannot be tested', untested),
                               (f'unresolved identities change the selected listings of: {", ".join(affected)}', affected)) if k]
    print(json.dumps({k: report[k] for k in ('selected', 'pending', 'calibration', 'spearman_r_v_both_stores', 'candidates',
                                             'selected_stores', 'categories', 'identity', 'provider_review', 'no_developer_rule')},
                     indent=1, default=str))
    if problems:
        raise SystemExit('not final, thesis tables and dataset not written: ' + '; '.join(problems))
    store = {'apple': 'App Store', 'play': 'Google Play', 'apple+play': 'both'}
    head = (f"% Generated by 04_Study/4.4_App-Sampling/scripts/app-ranking/v005/rank.py from the collections of {report['snapshot']['apple'][:10]} "
            f"and {report['snapshot']['play'][:10]}; do not edit by hand.")
    preinstalled = [(s, i, cat) for s, apps in cfg['preinstalled_table'].items() for i, cat in apps.items()]
    lines = [head]
    for r in selection:
        lines.append(f"{r['order']} & {tex(r['name'])} & {tex(r['developer'])} & {store[r['stores']]} & {tex(r['category'])} & "
                     f"{num(r['german_ratings_app_store'])} & {num(r['german_reviews_google_play'])} & {num(r['popularity'])} \\\\")
    for i, (s, lid, cat) in enumerate(preinstalled, len(selection) + 1):
        l = listings[s][lid]
        lines.append(f"{i} & {tex(l['name'])} & {tex(l['developer'])} & preinstalled & {tex(cat)} & -- & -- & -- \\\\")
    Path(cfg['table']).write_text('\n'.join(lines) + '\n', encoding='utf-8')
    # Without the developer rule: shaded rows belong to a provider with several apps.
    several, kept = Counter(c['provider'] for c in nodev), {c['key']: i for i, c in enumerate(sel, 1)}
    lines = [head]
    for i, c in enumerate(nodev, 1):
        d = decision(c, screening) or {}
        lines.append(('\\rowcolor{devshade}' if several[c['provider']] > 1 else '') +
                     f"{i} & {tex(c['name'])} & {tex(c['developer'])} & {store['+'.join(s for s in ('apple', 'play') if c[s])]} & "
                     f"{tex(d.get('category'))} & {num(c['r'])} & {num(c['v'])} & {num(round(score(c)))} & {kept.get(c['key'], '--')} \\\\")
    Path(cfg['developer_table']).write_text('\n'.join(lines) + '\n', encoding='utf-8')
    named = defaultdict(set)
    for s in listings:
        for l in listings[s].values():
            named[provider_key(l['developer'], {})].add((s, l['developer']))
    lines = [head]
    for alias, target in sorted(aliases.items(), key=lambda a: a[1]):
        show = lambda key: '; '.join(f"{tex(d)} ({store[s]})" for s, d in sorted(named[key]))
        lines.append(f"{show(alias)} & {show(target)} & {tex(cfg['alias_evidence'][alias])} \\\\")
    Path(cfg['alias_table']).write_text('\n'.join(lines) + '\n', encoding='utf-8')
    # Same app under two developer names: the register joins the two developers into one provider.
    lines = [head]
    for pdev, adev, p, a in joined:
        r = decided[(p, a)]
        lines.append(f"{tex(listings['play'][p]['name'])} & {tex(pdev)} & {tex(listings['apple'][a]['name'])} & {tex(adev)} & "
                     f"{tex(r['evidence'])} \\\\")
    Path(cfg['identity_table']).write_text('\n'.join(lines) + '\n', encoding='utf-8')
    labels = {'no developer rule': f"No developer rule (the 47 places go to {report['no_developer_rule']['providers']} providers)",
              'equal platform weights': 'Equal weights for iOS and Android',
              'pool-sum scale (first formula)': "Alternative scale (share of each store's total count)",
              'worldwide Play rating count instead of German reviews': 'Worldwide Google Play rating count instead of German reviews',
              'previous method (store alternation, worldwide Play count)': 'Earlier selection: store alternation with the worldwide Google Play count',
              'depth 20': 'Depth 20 instead of 30', 'App Store depth 200': 'App Store searched to depth 200',
              'English keywords only': 'English keywords only', 'German keywords only': 'German keywords only'}
    by_name = {r['variant']: r for r in rows}
    lines = [head] + [f"{text} & {by_name[v]['differ_from_main']} & {by_name[v]['listings_differ']} \\\\"
                      for v, text in labels.items() if v in by_name]
    left = [r for r in rows if r['variant'].startswith('without "')]
    lines.append(f"One keyword left out ({len(left)} runs; largest change) & {max(r['differ_from_main'] for r in left)} & "
                 f"{max(r['listings_differ'] for r in left)} \\\\")
    lines.append('\\bottomrule')  # inside tabularx, a \bottomrule after \input is misplaced
    Path(cfg['sensitivity_table']).write_text('\n'.join(lines) + '\n', encoding='utf-8')
    dataset = [dict(r, preinstalled=False) for r in selection] + [
        {'order': i, 'name': listings[s][lid]['name'], 'developer': listings[s][lid]['developer'], 'stores': s,
         'apple_id': lid if s == 'apple' else '', 'play_id': lid if s == 'play' else '', 'category': cat,
         'provider': find(listings[s][lid]['developer_key']), 'preinstalled': True}
        for i, (s, lid, cat) in enumerate(preinstalled, len(selection) + 1)]
    Path(cfg['dataset']).parent.mkdir(parents=True, exist_ok=True)
    with open(cfg['dataset'], 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(dataset[0]), restval='')
        w.writeheader()
        w.writerows(dataset)


if __name__ == '__main__':
    main(sys.argv[1])
