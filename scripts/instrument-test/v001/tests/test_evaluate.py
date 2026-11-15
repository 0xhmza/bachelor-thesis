import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import evaluate as ev  # noqa: E402

MODEL = HERE.parents[3] / '04_Study/4.3_Analytical-Framework/reference_model_v1.yaml'
P, A, U = ev.PRESENT, ev.ABSENT, ev.UNCERTAIN


@pytest.mark.parametrize('values,expected', [
    ((P, P), P), ((P, U), U), ((P, A), A), ((U, U), U), ((U, A), A), ((A, A), A)])
def test_and(values, expected):
    states = {'a': values[0], 'b': values[1]}
    assert ev.evaluate({'and': ['a', 'b']}, states) == expected


@pytest.mark.parametrize('op', ['or', 'orplus'])
@pytest.mark.parametrize('values,expected', [
    ((P, P), P), ((P, U), P), ((P, A), P), ((U, U), U), ((U, A), U), ((A, A), A)])
def test_or(op, values, expected):
    states = {'a': values[0], 'b': values[1]}
    assert ev.evaluate({op: ['a', 'b']}, states) == expected


def test_unknown_operator():
    with pytest.raises(ValueError):
        ev.evaluate({'xor': ['a']}, {'a': P})


def all_states(state):
    return {c: state for c in ev.load(MODEL)['components']}


def test_model_is_consistent():
    assert ev.check_model(ev.load(MODEL))


def test_model_keeps_the_review_capabilities():
    model = ev.load(MODEL)
    review = {f'K{i}' for i in range(1, 9)}
    assert review == (set(model['capabilities']) | set(model['excluded_capabilities'])) & review


def test_all_present_opens_every_harm():
    model = ev.load(MODEL)
    assert set(ev.harm_states(model, all_states(P)).values()) == {P}


def test_all_absent_closes_every_harm():
    model = ev.load(MODEL)
    assert set(ev.harm_states(model, all_states(A)).values()) == {A}


def test_one_open_pathway_makes_a_harm_apply():
    model = ev.load(MODEL)
    states = all_states(A)
    states.update(CO1=P, CX1=P)  # K9: a person nearby reads the entries
    harms = ev.harm_states(model, states)
    assert harms['H-PHY'] == P and harms['H-REP'] == P and harms['H-ECO'] == A


def test_uncertain_stays_uncertain():
    model = ev.load(MODEL)
    states = all_states(A)
    states.update(EX2=U, IM2=P)  # K7
    assert ev.capability_states(model, states)['K7'] == U
    assert ev.harm_states(model, states)['H-SOC'] == U


def test_measure_cuts_only_a_necessary_condition():
    model = ev.load(MODEL)
    states = all_states(A)
    states.update(CO1=P, CX1=P, IM9=P)
    # removing CX1 leaves the sharing branch of K9 open; removing CO1 closes it
    assert ev.after_measure(model, states, ['CX1'])['P04'] == P
    assert ev.after_measure(model, states, ['CO1'])['P04'] == A
