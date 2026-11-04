"""Evaluate the reference harm trees for one app (version 2).

    python evaluate.py <reference_model.yaml> <applicability.yaml>

A tree records which harms are possible, not how likely they are. Every node
has one of three states. AND is absent if any child is absent and present only
if all are present; OR is present if any child is present and absent only if all
are absent; anything else stays uncertain.

Changed from v001: OR+ ("more than one input may be needed") is no longer read
like OR, because asking whether a pathway is possible does not make one input
sufficient (methodology, Steps 1 and Reference Harm-Tree Construction; D12). A
model must state each OR+ as an OR of sufficient AND-combinations; this script
rejects any remaining 'orplus'.
"""
import sys

import yaml

PRESENT, ABSENT, UNCERTAIN = 'present', 'absent', 'uncertain'
STATES = (PRESENT, ABSENT, UNCERTAIN)


def load(path):
    with open(path, encoding='utf-8') as f:
        return yaml.safe_load(f)


def evaluate(expr, states):
    """Return the state of a component id or an {and|or: [...]} expression."""
    if isinstance(expr, str):
        return states[expr]
    (op, children), = expr.items()
    if op == 'orplus':
        raise ValueError('OR+ must be rewritten as an OR of sufficient AND-combinations (D12)')
    values = [evaluate(c, states) for c in children]
    if op == 'and':
        if ABSENT in values:
            return ABSENT
        return PRESENT if all(v == PRESENT for v in values) else UNCERTAIN
    if op == 'or':
        if PRESENT in values:
            return PRESENT
        return ABSENT if all(v == ABSENT for v in values) else UNCERTAIN
    raise ValueError(f'unknown operator {op}')


def leaves(expr):
    """All component ids in an expression."""
    if isinstance(expr, str):
        return {expr}
    (_, children), = expr.items()
    return set().union(*(leaves(c) for c in children))


def operators(expr):
    if isinstance(expr, str):
        return set()
    (op, children), = expr.items()
    return {op}.union(*(operators(c) for c in children))


def capability_states(model, states):
    return {k: evaluate(c['needs'], states) for k, c in model['capabilities'].items()}


def pathway_states(model, states):
    caps = capability_states(model, states)
    return {p['id']: caps[p['capability']]
            for h in model['harms'].values() for p in h['pathways']}


def harm_states(model, states):
    """A harm applies if at least one of its pathways does (codebook, section 0)."""
    paths = pathway_states(model, states)
    out = {}
    for code, harm in model['harms'].items():
        values = [paths[p['id']] for p in harm['pathways']]
        if all(v == ABSENT for v in values):
            out[code] = ABSENT
        else:
            out[code] = PRESENT if PRESENT in values else UNCERTAIN
    return out


def after_measure(model, states, removed):
    """Pathway states if a measure really removed these components."""
    changed = dict(states)
    for component in removed:
        changed[component] = ABSENT
    return pathway_states(model, changed)


def check_model(model):
    """Every node a tree uses must exist; every component must be used; no OR+ remains."""
    used = set()
    for code, cap in model['capabilities'].items():
        if 'orplus' in operators(cap['needs']):
            raise ValueError(f'{code} still uses OR+')
        found = leaves(cap['needs'])
        unknown = found - set(model['components'])
        if unknown:
            raise ValueError(f'{code} uses unknown components {unknown}')
        used |= found
    unused = set(model['components']) - used
    if unused:
        raise ValueError(f'components in no capability: {unused}')
    seen = set()
    for harm in model['harms'].values():
        for path in harm['pathways']:
            if path['capability'] not in model['capabilities']:
                raise ValueError(f"{path['id']} uses an unknown capability")
            if path['id'] in seen:
                raise ValueError(f"duplicate pathway {path['id']}")
            seen.add(path['id'])
            if not path['sources']:
                raise ValueError(f"{path['id']} has no source")
    return True


def main(model_path, applicability_path):
    model = load(model_path)
    check_model(model)
    record = load(applicability_path)
    states = {k: v['state'] for k, v in record['components'].items()}
    for code, state in capability_states(model, states).items():
        print(code, state)
    for code, state in harm_states(model, states).items():
        print(code, state)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
