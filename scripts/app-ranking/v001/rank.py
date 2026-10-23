"""Rank eligible apps by exposure (rating count), optionally blended with rating quality.

Method (Decision D2, proposed): within each store, rank the apps on rating count
(log10 scale) and merge stores by within-store percentile. The default weight 1
ranks on exposure alone. Lower weights blend in a Bayesian-shrunk average rating;
the script reports them as sensitivity variants. Downloads are not used.
Rating counts are storefront-specific on the App Store but global on Google Play.

    python scripts/app-ranking/v001/rank.py INPUT [INPUT ...] --domain fitness

INPUT is a v005 App Store scraper JSON, or a CSV with columns
id, name, store, rating, rating_count[, released, keywords].
Standard library only. Eligibility beyond the rating floor (function, language,
payment) is a manual decision: list excluded IDs in --exclude.
"""
import argparse
import csv
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

VERSION = 'v001'
HERE = Path(__file__).resolve().parent


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def parse_date(text):
    try:
        return datetime.fromisoformat(str(text).replace('Z', '+00:00'))
    except ValueError:
        return None


def load_json(path):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    snapshot = parse_date(data.get('timestamp'))
    rows = []
    for keyword, apps in data['results'].items():
        for a in apps:
            rows.append({'id': 'apple:' + str(a.get('ID')), 'name': a.get('App Name'),
                'store': 'apple', 'rating': a.get('Average Rating'),
                'rating_count': a.get('Rating Count'), 'released': a.get('Released'),
                'keywords': [keyword]})
    return rows, snapshot


def load_csv(path):
    with Path(path).open(encoding='utf-8-sig', newline='') as f:
        rows = []
        for r in csv.DictReader(f):
            rows.append({'id': r['id'], 'name': r.get('name'), 'store': r['store'],
                'rating': float(r['rating']) if r.get('rating') else None,
                'rating_count': int(r['rating_count']) if r.get('rating_count') else None,
                'released': r.get('released'),
                'keywords': [k for k in (r.get('keywords') or '').split('|') if k]})
    return rows, None


def collect(paths):
    """Merge inputs; one record per listing, keeping every keyword that found it."""
    unique, loaded, snapshots = {}, 0, []
    for p in paths:
        rows, snap = (load_json(p) if str(p).lower().endswith('.json') else load_csv(p))
        if snap:
            snapshots.append(snap)
        for r in rows:
            loaded += 1
            have = unique.get(r['id'])
            if have is None:
                unique[r['id']] = r
            else:
                have['keywords'] = sorted(set(have['keywords']) | set(r['keywords']))
    return list(unique.values()), loaded, (max(snapshots) if snapshots else datetime.now(timezone.utc))


def avg_ranks(values, descending=True):
    """Rank 1 = best; ties share the mean of the positions they occupy."""
    order = sorted(range(len(values)), key=lambda i: values[i], reverse=descending)
    ranks, i = [0.0] * len(values), 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        for k in range(i, j + 1):
            ranks[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return ranks


def exposure(row, snapshot, age_adjusted):
    count = row['rating_count']
    if not age_adjusted:
        return math.log10(count)
    born = parse_date(row.get('released'))
    years = max(1.0, (snapshot - born).days / 365.25) if born else 1.0
    return math.log10(count / years)


def rank_store(rows, weight, m, snapshot, age_adjusted=False):
    """Order one store's eligible apps; returns new dicts sorted best first."""
    pool_mean = sum(r['rating'] for r in rows) / len(rows)
    out = []
    for r in rows:
        v = r['rating_count']
        shrunk = (v / (v + m)) * r['rating'] + (m / (v + m)) * pool_mean
        out.append(dict(r, shrunk_rating=shrunk, exposure=exposure(r, snapshot, age_adjusted)))
    rank_e = avg_ranks([r['exposure'] for r in out])
    rank_q = avg_ranks([r['shrunk_rating'] for r in out])
    for r, e, q in zip(out, rank_e, rank_q):
        r.update(rank_exposure=e, rank_quality=q, combined_rank=weight * e + (1 - weight) * q)
    out.sort(key=lambda r: (r['combined_rank'], -r['exposure'], r['id']))
    for pos, r in enumerate(out, 1):
        r['store_position'] = pos
        r['store_percentile'] = (pos - 0.5) / len(out)
    return out


def rank_all(rows, weight, m, snapshot, age_adjusted=False):
    """Rank each store separately, then merge by within-store percentile."""
    merged = []
    for store in sorted({r['store'] for r in rows}):
        merged += rank_store([r for r in rows if r['store'] == store], weight, m, snapshot, age_adjusted)
    merged.sort(key=lambda r: (r['store_percentile'], r['store'], r['id']))
    for pos, r in enumerate(merged, 1):
        r['position'] = pos
    return merged


def spearman(a, b):
    n = len(a)
    if n < 2:
        return None
    ma, mb = sum(a) / n, sum(b) / n
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    den = math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b))
    return num / den if den else None


def compare(base, variant, top):
    ids_b = [r['id'] for r in base[:top]]
    ids_v = [r['id'] for r in variant[:top]]
    pos_v = {r['id']: r['position'] for r in variant}
    shared = set(ids_b) & set(ids_v)
    return {'top_n': top, 'shared_with_main': len(shared),
        'left_top_n': sorted(set(ids_b) - shared), 'entered_top_n': sorted(set(ids_v) - shared),
        'spearman_positions': spearman([r['position'] for r in base], [pos_v[r['id']] for r in base])}


def sensitivity(eligible, args, m, snapshot, base):
    """Re-rank under changed choices; blends add the shrunk average rating to the score."""
    main = args.weight_exposure
    variants = {f'blend_weight_exposure_{w}': dict(weight=w, m=m)
        for w in (0.75, 0.5, 0.25) if w != main}
    if main < 1:  # the prior weight only matters once quality enters the score
        variants.update(prior_weight_x2=dict(weight=main, m=m * 2),
            **{'prior_weight_x0.5': dict(weight=main, m=m / 2)})
    variants['exposure_per_year_since_release'] = dict(weight=main, m=m, age_adjusted=True)
    return {name: compare(base, rank_all(eligible, snapshot=snapshot, **kw), args.top)
        for name, kw in variants.items()}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('inputs', nargs='+')
    ap.add_argument('--domain', required=True, help='label for this pool, e.g. fitness or fertility')
    ap.add_argument('--floor', type=int, default=1000, help='minimum rating count (default 1000)')
    ap.add_argument('--m', type=float, help='prior weight of the shrinkage (default: the floor)')
    ap.add_argument('--weight-exposure', type=float, default=1.0,
        help='weight of the exposure rank; 1 = exposure only (default), below 1 blends in the shrunk rating')
    ap.add_argument('--top', type=int, default=20, help='N used for the sensitivity comparison')
    ap.add_argument('--exclude', help='text file of listing IDs (e.g. apple:123) removed by manual eligibility')
    ap.add_argument('--out-dir', default=str(HERE / 'output'))
    args = ap.parse_args(argv)
    if not 0 <= args.weight_exposure <= 1:
        ap.error('--weight-exposure must be between 0 and 1')
    m = args.m if args.m is not None else float(args.floor)

    rows, loaded, snapshot = collect(args.inputs)
    excluded_ids = set()
    if args.exclude:
        excluded_ids = {l.strip() for l in Path(args.exclude).read_text(encoding='utf-8').splitlines()
            if l.strip() and not l.startswith('#')}
    missing = [r for r in rows if r['rating'] is None or r['rating_count'] is None]
    usable = [r for r in rows if r not in missing]
    manual = [r for r in usable if r['id'] in excluded_ids]
    usable = [r for r in usable if r['id'] not in excluded_ids]
    below = [r for r in usable if r['rating_count'] < args.floor]
    eligible = [r for r in usable if r['rating_count'] >= args.floor]
    if not eligible:
        raise SystemExit('No listing passes the rating floor.')

    ranked = rank_all(eligible, args.weight_exposure, m, snapshot)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    stem = f'ranking-{args.domain}-{stamp}'
    columns = ['position', 'id', 'name', 'store', 'rating', 'rating_count', 'shrunk_rating',
        'exposure', 'rank_exposure', 'rank_quality', 'combined_rank', 'store_position',
        'store_percentile', 'in_top_n', 'keywords']
    with (out / (stem + '.csv')).open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, columns)
        w.writeheader()
        for r in ranked:
            row = {c: r.get(c) for c in columns}
            row['in_top_n'] = r['position'] <= args.top
            row['keywords'] = '|'.join(r['keywords'])
            w.writerow(row)
    manifest = {'script_version': VERSION, 'created_utc': stamp, 'domain': args.domain,
        'snapshot_utc': snapshot.isoformat(),
        'parameters': {'floor': args.floor, 'prior_weight_m': m,
            'weight_exposure': args.weight_exposure, 'top_n': args.top,
            'exposure': 'log10(rating_count)', 'quality': 'shrunk average rating (pool mean per store)',
            'merge': 'within-store percentile'},
        'inputs': [{'file': str(p), 'sha256': sha256(p)} for p in args.inputs],
        'cascade': {'records_loaded': loaded, 'distinct_listings': len(rows),
            'missing_rating_data': len(missing), 'excluded_manually': len(manual),
            'below_floor': len(below), 'ranked': len(eligible),
            'ranked_per_store': {s: sum(r['store'] == s for r in eligible) for s in sorted({r['store'] for r in eligible})}},
        'sensitivity': sensitivity(eligible, args, m, snapshot, ranked),
        'notes': ['API order is not used. Downloads are not used. Rating count measures ratings, not downloads.']}
    (out / (stem + '.json')).write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')
    print(out / (stem + '.csv'))
    print(out / (stem + '.json'))


if __name__ == '__main__':
    main()
