"""Checks on constructed corpora, run before the estimator is used (methodology, Validation)."""
import random
import statistics
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import design as d  # noqa: E402


def unit(i, **flags):
    base = {'unit': f'u{i}', 'disagree': 0, 'uncertain': 0, 'vocab_no_high_stakes': 0, 'interface': 0}
    base.update(flags)
    return base


def test_priority_partition_is_disjoint():
    u = unit(1, disagree=1, uncertain=1, interface=1)
    assert d.stratum(u) == 'V1'
    assert d.stratum(unit(2, uncertain=1, interface=1)) == 'V2'
    assert d.stratum(unit(3, interface=1)) == 'V4'
    assert d.stratum(unit(4)) == 'V5'


def test_small_stratum_is_taken_whole_and_probabilities_are_exact():
    units = [unit(i, disagree=1) for i in range(3)] + [unit(i) for i in range(3, 103)]
    m = d.draw(units, {'V1': 10, 'V5': 20}, seed=1)
    v1 = [r for r in m if r['stratum'] == 'V1']
    v5 = [r for r in m if r['stratum'] == 'V5']
    assert all(r['pi'] == 1 and r['selected'] for r in v1)
    assert all(r['pi'] == 0.2 for r in v5) and sum(r['selected'] for r in v5) == 20


def test_empty_allocation_breaks_positivity():
    with pytest.raises(ValueError):
        d.draw([unit(1, interface=1), unit(2)], {'V5': 1}, seed=1)


def test_perfect_model_needs_no_correction():
    units = [unit(i) for i in range(50)]
    g = {u['unit']: float(i % 7 == 0) for i, u in enumerate(units)}
    m = d.draw(units, {'V5': 10}, seed=2)
    y = {r['unit']: g[r['unit']] for r in m if r['selected']}
    est = d.estimate_total(g, y, m)
    assert est['estimate'] == pytest.approx(sum(g.values()))
    assert d.estimate_total(g, y, m, floor=False)['se'] == 0
    assert est['se'] > 0          # the floor never lets a sample without errors claim none


def corpus(seed, apps=40, per_app=60):
    """Rare positives, a biased pair of models and errors correlated within each policy."""
    rng = random.Random(seed)
    units, g, truth = [], {}, {}
    for a in range(apps):
        app_miss = rng.random() < 0.3          # some policies are hard for both models
        for k in range(per_app):
            i = f'a{a}u{k}'
            y = int(rng.random() < 0.03)
            miss = 0.6 if app_miss else 0.15
            m1 = y if rng.random() > miss else 1 - y if y else int(rng.random() < 0.01)
            m2 = m1 if rng.random() < 0.7 else (y if rng.random() > miss else 1 - y if y else 0)
            unc = int(rng.random() < 0.05)
            gi = 0.5 if unc else (m1 + m2) / 2
            vocab = int(y == 1 and m1 == m2 == 0 and rng.random() < 0.5)
            units.append({'unit': i, 'app': a, 'disagree': int(m1 != m2), 'uncertain': unc,
                          'vocab_no_high_stakes': vocab, 'interface': int(k >= per_app - 5)})
            g[i], truth[i] = gi, y
    return units, g, truth


def test_estimator_is_unbiased_and_intervals_cover():
    units, g, truth = corpus(7)
    T = sum(truth.values())
    alloc = {'V1': 120, 'V2': 80, 'V3': 40, 'V4': 60, 'V5': 200}
    ests, cover = [], 0  # the variance floor is on by default
    for s in range(1500):
        m = d.draw(units, alloc, seed=s)
        y = {r['unit']: truth[r['unit']] for r in m if r['selected']}
        e = d.estimate_total(g, y, m)
        ests.append(e['estimate'])
        cover += e['low'] <= T <= e['high']
    assert abs(statistics.mean(ests) - T) / T < 0.03       # design-unbiased
    assert sum(g.values()) != pytest.approx(T, rel=0.03)   # the raw model total is biased
    assert cover / 1500 > 0.90                              # close to nominal 95 % with the floor


def test_joint_misses_are_counted_in_every_stratum():
    units, g, truth = corpus(3)
    true_missed = sum(1 for i in g if truth[i] == 1 and g[i] == 0)
    m = d.draw(units, {h: 10**6 for h in d.STRATA}, seed=0)   # census
    y = {r['unit']: truth[r['unit']] for r in m}
    assert d.joint_misses(g, y, m) == pytest.approx(true_missed)


def test_unit_total_does_not_identify_app_counts():
    """Ten mentions in one app and one mention in each of ten apps: same total, different apps."""
    repeated = {f'a0u{k}': 1 for k in range(10)}
    singles = {f'a{a}u0': 1 for a in range(10)}
    apps = lambda labels: len({u.split('u')[0] for u, v in labels.items() if v})
    assert sum(repeated.values()) == sum(singles.values())
    assert apps(repeated) == 1 and apps(singles) == 10


def test_jeffreys_for_zero_events():
    low, high = d.jeffreys(0, 5)
    assert low == 0 and high == pytest.approx(0.379, abs=0.002)


def test_neyman_allocation_respects_floors_and_small_strata():
    sizes = {'V1': 300, 'V2': 200, 'V3': 20, 'V4': 500, 'V5': 5700}
    sds = {'V1': 0.5, 'V2': 0.5, 'V3': 0.4, 'V4': 0.1, 'V5': 0.07}
    a = d.neyman(sizes, sds, 500, {'V1': 30, 'V2': 30, 'V3': 30, 'V4': 30, 'V5': 150})
    assert a['V3'] == 20 and a['V5'] >= 150 and all(a[h] >= 30 for h in ('V1', 'V2', 'V4'))
    assert abs(sum(a.values()) - 500) <= 2
