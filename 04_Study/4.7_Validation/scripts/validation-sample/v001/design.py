"""Validation sample and corrected estimates (methodology, Validation Sample; D9).

Strata are a priority partition: each unit goes to the first stratum it meets,
V1 the two models disagree on any code, V2 a model returned an uncertain label,
V3 harm vocabulary but no high-stakes label, V4 interface text, V5 every other
unit. Units are drawn by simple random sampling without replacement within each
stratum; a stratum smaller than its allocation is taken whole. A unit's selection
probability is then n_h / N_h exactly (Lohr 2021, ch. 3).

For one code, g_i is the mean of the two models' indicators (0, 1/2 or 1; an
uncertain answer counts 1/2) and y_i the reference label of a sampled unit. The
total over the corpus U is estimated by the difference estimator

    T_hat = sum_{i in U} g_i + sum_{i in S} (y_i - g_i) / pi_i,

the Horvitz-Thompson estimator of the model's errors (Egami et al. 2023, s4;
Angelopoulos et al. 2023), with the stratified variance of the errors.
"""
import math
import random
from collections import defaultdict

STRATA = ('V1', 'V2', 'V3', 'V4', 'V5')


def stratum(unit):
    """unit: dict with 0/1 flags 'disagree', 'uncertain', 'vocab_no_high_stakes', 'interface'."""
    if unit['disagree']:
        return 'V1'
    if unit['uncertain']:
        return 'V2'
    if unit['vocab_no_high_stakes']:
        return 'V3'
    if unit['interface']:
        return 'V4'
    return 'V5'


def draw(units, allocation, seed):
    """Return the sampling manifest: one row per unit with stratum, N_h, n_h, pi, selected.

    allocation: {stratum: n_h}. A non-empty stratum must get n_h >= 1 (positivity)."""
    by = defaultdict(list)
    for u in units:
        by[stratum(u)].append(u['unit'])
    rng = random.Random(seed)
    manifest = []
    for h in STRATA:
        ids = sorted(by.get(h, []))
        if not ids:
            continue
        n = allocation.get(h, 0)
        if n < 1:
            raise ValueError(f'stratum {h} has {len(ids)} units but no allocation: positivity fails')
        n = min(n, len(ids))
        chosen = set(rng.sample(ids, n))
        for i in ids:
            manifest.append({'unit': i, 'stratum': h, 'N_h': len(ids), 'n_h': n,
                             'pi': n / len(ids), 'selected': i in chosen, 'seed': seed})
    return manifest


def estimate_total(g, y, manifest, z=1.96, floor=True):
    """g: {unit: model value} for every unit of U; y: {unit: reference 0/1} for the sample.

    Returns the estimate, its standard error and a normal interval. The interval describes
    the uncertainty of the audit within this fixed corpus (finite-population inference).

    floor: a stratum whose sample shows few or no errors must not count as error-free.
    Its error variance is at least p(1 - p) m^2, with p = (k + 1/2) / (n + 1) the Jeffreys
    estimate of the share of units with an error (k of n sampled units) and m the mean size
    of the observed errors (1 if none). Study rule, checked in check_coverage.py."""
    rows = {r['unit']: r for r in manifest}
    total = sum(g.values())
    resid = defaultdict(list)
    info = {}
    for u, r in rows.items():
        info[r['stratum']] = (r['N_h'], r['n_h'])
        if r['selected']:
            resid[r['stratum']].append(y[u] - g[u])
    correction = sum(sum(d) * N / n for h, d in resid.items() for N, n in [info[h]])
    var = 0.0
    for h, d in resid.items():
        N, n = info[h]
        if n >= N:
            continue                      # census: no sampling error
        mean = sum(d) / n
        s2 = sum((x - mean) ** 2 for x in d) / (n - 1) if n > 1 else 0.0
        if floor:
            errors = [abs(x) for x in d if x != 0]
            p = (len(errors) + 0.5) / (n + 1)
            m = sum(errors) / len(errors) if errors else 1.0
            s2 = max(s2, p * (1 - p) * m * m)
        var += N * N * (1 - n / N) * s2 / n
    est = total + correction
    se = math.sqrt(var)
    return {'estimate': est, 'model_total': total, 'correction': correction, 'se': se,
            'low': est - z * se, 'high': est + z * se}


def neyman(sizes, sds, n, floors):
    """Neyman allocation n_h proportional to N_h * S_h (Lohr 2021, ch. 3), with minimum
    sample sizes; a stratum smaller than its share is taken whole."""
    alloc = {h: min(sizes[h], floors.get(h, 0)) for h in sizes}
    rest = n - sum(alloc.values())
    weight = {h: sizes[h] * sds[h] for h in sizes}
    for _ in range(len(sizes)):
        open_ = [h for h in sizes if alloc[h] < sizes[h]]
        w = sum(weight[h] for h in open_)
        if rest <= 0 or not w:
            break
        extra = {h: rest * weight[h] / w for h in open_}
        for h in open_:
            alloc[h] = min(sizes[h], alloc[h] + extra[h])
        rest = n - sum(alloc.values())
    return {h: int(round(v)) for h, v in alloc.items()}


def joint_misses(g, y, manifest):
    """Estimated number of reference positives that both models missed (g = 0), from every stratum."""
    return sum(1 / r['pi'] for r in manifest
               if r['selected'] and y[r['unit']] == 1 and g[r['unit']] == 0)


def jeffreys(x, n, level=0.95):
    """Jeffreys interval for a binomial proportion, for small counts (Webber 2013)."""
    from scipy.stats import beta
    a = (1 - level) / 2
    low = 0.0 if x == 0 else beta.ppf(a, x + 0.5, n - x + 0.5)
    high = 1.0 if x == n else beta.ppf(1 - a, x + 0.5, n - x + 0.5)
    return low, high
