import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import evaluate as ev  # noqa: E402

ROOT = HERE.parents[3]
MODEL = ROOT / '04_Study/4.3_Analytical-Framework/reference_model_v2.yaml'
P, A, U = ev.PRESENT, ev.ABSENT, ev.UNCERTAIN


@pytest.mark.parametrize('values,expected', [
    ((P, P), P), ((P, U), U), ((P, A), A), ((U, U), U), ((U, A), A), ((A, A), A)])
def test_and(values, expected):
    states = {'a': values[0], 'b': values[1]}
    assert ev.evaluate({'and': ['a', 'b']}, states) == expected


@pytest.mark.parametrize('values,expected', [
    ((P, P), P), ((P, U), P), ((P, A), P), ((U, U), U), ((U, A), U), ((A, A), A)])
def test_or(values, expected):
    states = {'a': values[0], 'b': values[1]}
    assert ev.evaluate({'or': ['a', 'b']}, states) == expected


def test_orplus_is_rejected():
    with pytest.raises(ValueError):
        ev.evaluate({'orplus': ['a', 'b']}, {'a': P, 'b': A})


def test_unknown_operator():
    with pytest.raises(ValueError):
        ev.evaluate({'xor': ['a']}, {'a': P})


def model():
    return ev.load(MODEL)


def all_states(state):
    return {c: state for c in model()['components']}


def test_model_is_consistent_and_has_no_orplus():
    assert ev.check_model(model())


def test_check_model_rejects_orplus():
    m = model()
    m['capabilities']['K10']['needs'] = {'orplus': ['IM4', 'IM7', 'CO2']}
    with pytest.raises(ValueError):
        ev.check_model(m)


def test_model_keeps_the_review_capabilities():
    m = model()
    review = {f'K{i}' for i in range(1, 9)}
    assert review == (set(m['capabilities']) | set(m['excluded_capabilities'])) & review


def test_all_present_opens_every_harm():
    assert set(ev.harm_states(model(), all_states(P)).values()) == {P}


def test_all_absent_closes_every_harm():
    assert set(ev.harm_states(model(), all_states(A)).values()) == {A}


def test_on_device_insight_alone_gives_no_class():
    """v1 read IM4 OR+ IM7 OR+ CO2 like OR, so CO2 alone opened K10. In v2 it does not."""
    states = all_states(A)
    states.update(CO1=P, CO2=P)
    assert ev.capability_states(model(), states)['K10'] == A


@pytest.mark.parametrize('present', [('CO2', 'IM7'), ('IM4', 'CX3')])
def test_each_sufficient_combination_opens_k10(present):
    states = all_states(A)
    states.update({c: P for c in present})
    assert ev.capability_states(model(), states)['K10'] == P


def test_unknown_partner_identifier_keeps_k10_uncertain():
    states = all_states(A)
    states.update(IM4=P, CX3=U)
    assert ev.capability_states(model(), states)['K10'] == U


@pytest.mark.parametrize('delete,export,expected', [
    (A, A, A), (P, A, P), (A, P, P), (U, A, U), (A, U, U)])
def test_deletion_and_export_are_judged_separately(delete, export, expected):
    states = all_states(A)
    states.update(IM12=delete, IM14=export)
    assert ev.capability_states(model(), states)['I2'] == expected


def test_one_open_pathway_makes_a_harm_apply():
    states = all_states(A)
    states.update(CO1=P, CX1=P)  # K9: a person nearby reads the entries
    harms = ev.harm_states(model(), states)
    assert harms['H-PHY'] == P and harms['H-REP'] == P and harms['H-ECO'] == A


def test_test_app_record_matches_model_v2():
    record = ev.load(ROOT / '04_Study/4.7_Validation/Instrument-Test/applicability_clue_v2.yaml')
    assert set(record['components']) == set(model()['components'])
    states = {k: v['state'] for k, v in record['components'].items()}
    caps = ev.capability_states(model(), states)
    assert caps['K10'] == P and caps['I2'] == A
