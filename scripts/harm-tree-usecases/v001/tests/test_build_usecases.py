import copy
import random
import sys
from pathlib import Path

import pytest
import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import build_usecases as b  # noqa: E402

ROOT = HERE.parents[3]
MODEL = yaml.safe_load((ROOT / '04_Study/Reference-Model/reference_model_v2.yaml').read_text(encoding='utf-8'))
CASES = yaml.safe_load((ROOT / '04_Study/Reference-Model/use_cases_v1.yaml').read_text(encoding='utf-8'))['use_cases']


def run(cases):
    steps = b.accrete(MODEL, cases)
    return steps, b.check(MODEL, cases, steps, b.bib_keys(ROOT))


def test_formulas():
    expr = {'and': ['A', {'or': ['B', 'C']}]}
    assert b.holds(expr, {'A', 'C'})
    assert not b.holds(expr, {'B', 'C'})
    assert b.terms(expr, {'A', 'B', 'C'}) == {frozenset('AB'), frozenset('AC')}
    assert b.terms(expr, {'A'}) == set()
    assert b.prune(expr, {'A', 'C'}) == {'and': ['A', 'C']}
    assert b.prune(expr, {'B'}) is None


def test_terms_are_minimal():
    expr = {'or': ['A', {'and': ['A', 'B']}]}
    assert b.terms(expr, {'A', 'B'}) == {frozenset('A')}


def test_use_cases_rebuild_the_reference_model():
    steps, errors = run(CASES)
    assert errors == []
    final = steps[-1]
    assert final['avail'] == set(MODEL['components'])
    assert final['enabled'] == set(MODEL['capabilities'])
    assert len(final['paths']) == 21


def test_check_cases_add_nothing():
    steps, _ = run(CASES)
    checks = [s for s in steps if s['uc']['role'] == 'check']
    assert len(checks) >= b.STOP_RUN
    for s in checks:
        assert not (s['new_components'] or s['new_capabilities'] or s['new_pathways'] or s['widened'])


def test_every_step_is_monotone():
    steps, _ = run(CASES)
    for a, c in zip(steps, steps[1:]):
        assert a['avail'] <= c['avail'] and a['enabled'] <= c['enabled'] and a['paths'] <= c['paths']


def test_final_tree_does_not_depend_on_order():
    build = [uc for uc in CASES if uc['role'] == 'build']
    checks = [uc for uc in CASES if uc['role'] == 'check']
    rng = random.Random(1)
    for _ in range(5):
        shuffled = build[:]
        rng.shuffle(shuffled)
        steps = b.accrete(MODEL, shuffled + checks)
        assert steps[-1]['avail'] == set(MODEL['components'])
        assert steps[-1]['enabled'] == set(MODEL['capabilities'])
        assert len(steps[-1]['paths']) == 21


def test_a_check_case_that_adds_a_component_is_rejected():
    cases = copy.deepcopy(CASES)
    # move IM8 (routes) from the build case UC5 to the check case UC8: UC8 then adds something
    for uc in cases:
        if uc['id'] == 'UC5':
            uc['card'] = [s for s in uc['card'] if 'IM8' not in s['components']] or [
                {'q': 'record', 'components': ['CO1'], 'evidence': ['hudig2025intimate p. 3'], 'answer': 'x'}]
        if uc['id'] == 'UC8':
            uc['card'].append({'q': 'record', 'components': ['IM8'], 'evidence': ['niksirat2024wearable p. 12'],
                               'answer': 'routes'})
    _, errors = run(cases)
    assert any('UC8 is a check case but adds something' in e for e in errors)


def test_missing_component_is_reported():
    cases = [uc for uc in copy.deepcopy(CASES) if uc['id'] != 'UC5']
    _, errors = run(cases)
    assert any('IM8' in e for e in errors)
    assert any('K1' in e for e in errors)


def test_components_need_evidence_with_a_page():
    cases = copy.deepcopy(CASES)
    cases[0]['card'][0]['evidence'] = []
    _, errors = run(cases)
    assert any('no evidence' in e for e in errors)
    cases = copy.deepcopy(CASES)
    cases[0]['card'][0]['evidence'] = ['hudig2025intimate']
    _, errors = run(cases)
    assert any('lacks a page' in e for e in errors)


def test_unknown_citation_key_is_reported():
    cases = copy.deepcopy(CASES)
    cases[0]['card'][0]['evidence'] = ['nobody2099 p. 1']
    _, errors = run(cases)
    assert any('not in references.bib' in e for e in errors)


def test_last_cases_must_be_checks():
    cases = [uc for uc in copy.deepcopy(CASES) if uc['id'] not in ('UC9', 'UC10')]
    _, errors = run(cases)
    assert any('must be check cases' in e for e in errors)


def test_common_subtrees_are_capabilities_of_several_harms():
    common = b.common_subtrees(MODEL)
    assert set(common) == {'K5', 'K6', 'K7', 'K8', 'K9', 'K10'}
    assert all(len(v) >= 2 for v in common.values())


def test_widening_is_counted_on_enabled_capabilities():
    steps, _ = run(CASES)
    by_id = {s['uc']['id']: s for s in steps}
    assert ('K6', 1) in by_id['UC3']['widened']      # IM3 opens a new route to K6
    assert ('K8', 2) in by_id['UC6']['widened']      # IM6 and IM7 open two routes to K8


def test_layout_order_has_no_more_crossings_than_the_file_order():
    links = [(h, p['capability'], p['id']) for h, hd in MODEL['harms'].items() for p in hd['pathways']]
    harms, caps = list(MODEL['harms']), list(MODEL['capabilities'])
    before = b.crossings({h: i for i, h in enumerate(harms)}, {k: i for i, k in enumerate(caps)}, links)
    ho, co = b.least_crossing_order(harms, caps, links)
    after = b.crossings({h: i for i, h in enumerate(ho)}, {k: i for i, k in enumerate(co)}, links)
    assert sorted(ho) == sorted(harms) and sorted(co) == sorted(caps)
    assert after <= before


def test_figures_exist_for_steps_with_new_pathways(tmp_path):
    steps, _ = run(CASES)
    for s in steps:
        body = b.tikz_for_step(MODEL, s)
        assert (body is None) == (not s['new_pathways'])
        if body:
            assert 'tikzpicture' in body
