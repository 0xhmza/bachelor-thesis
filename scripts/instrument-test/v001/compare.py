"""Read the model output of the instrument test and compare it with the stand-in coding.

    python compare.py <llm_dir> <standin.yaml> [<out.json>]

Labels are compared at the level of unit and node: (U102, IM4). Status, span and reason
are not part of the match. This is coarser than the correct-detection rule of the
validation, which also needs the evidence span to match. A span that does not occur in
its unit is discarded first. The stand-in is no validation reference: see its header.
"""
import json
import sys
from pathlib import Path

import yaml

from stage_inputs import load_stage1, load_units, span_ok

RUNS = (1, 2, 3)


def stage1_labels(entries, units):
    """{(unit, label)} of one run. A label is a node id, a harm code or a level code."""
    out = {}
    for unit, entry in entries.items():
        for code in entry.get('codes', []):
            if not span_ok(code.get('span'), units[unit]['text']):
                continue
            label = code.get('node') or code.get('harm') or code.get('code')
            out[(unit, label)] = code
    return out


def standin_labels(standin):
    out = set()
    for unit, row in standin.items():
        for item in row.get('n') or []:
            out.add((unit, item.split(':')[0]))
        for item in row.get('h') or []:
            out.add((unit, item.split(':')[0]))
        for item in row.get('inc') or []:
            out.add((unit, item))
        if row.get('g'):
            out.add((unit, 'L-GEN'))
    return out


def stage3_labels(llm, run, units):
    with open(llm / 'stage3' / f'run{run}.json', encoding='utf-8') as f:
        data = json.load(f)
    out = {}
    for entry in data['claims']:
        unit = entry['unit']
        for claim in entry.get('claims', []):
            if span_ok(claim.get('span'), units[unit]['text']):
                out[(unit, claim['code'])] = claim
    return out


def standin_measures(standin):
    out = set()
    for unit, row in standin.items():
        for item in row.get('m') or []:
            out.add((unit, item.split(':')[0]))
        if row.get('r'):
            out.add((unit, 'C-REA'))
    return out


def scores(found, reference):
    tp = len(found & reference)
    precision = tp / len(found) if found else 0
    recall = tp / len(reference) if reference else 0
    return {'found': len(found), 'reference': len(reference), 'shared': tp,
            'share_of_model_in_standin': round(precision, 3),
            'share_of_standin_in_model': round(recall, 3)}


def jaccard(a, b):
    return round(len(a & b) / len(a | b), 3) if a | b else 1.0


def main(llm_dir, standin_path, out_path=None):
    llm = Path(llm_dir)
    units = load_units(llm)
    with open(standin_path, encoding='utf-8') as f:
        standin = yaml.safe_load(f)
    runs = {r: stage1_labels(load_stage1(llm, 'stage1', r), units) for r in RUNS}
    para = stage1_labels(load_stage1(llm, 'stage1p', 1), units)
    sets = {r: set(runs[r]) for r in RUNS}
    union = set().union(*sets.values())
    votes = {label: sum(label in sets[r] for r in RUNS) for label in union}
    majority = {label for label, n in votes.items() if n >= 2}
    all_three = {label for label, n in votes.items() if n == 3}
    reference = standin_labels(standin)
    m_runs = {r: stage3_labels(llm, r, units) for r in RUNS}
    m_sets = {r: set(m_runs[r]) for r in RUNS}
    m_union = set().union(*m_sets.values())
    m_votes = {label: sum(label in m_sets[r] for r in RUNS) for label in m_union}
    m_majority = {label for label, n in m_votes.items() if n >= 2}
    m_reference = standin_measures(standin)
    result = {
        'stage1': {
            'per_run': {r: len(sets[r]) for r in RUNS},
            'paraphrase': len(para),
            'union': len(union),
            'votes': {str(n): sum(v == n for v in votes.values()) for n in RUNS},
            'jaccard_runs': {'1-2': jaccard(sets[1], sets[2]), '1-3': jaccard(sets[1], sets[3]),
                             '2-3': jaccard(sets[2], sets[3])},
            'jaccard_paraphrase_vs_majority': jaccard(set(para), majority),
            'unsure': sum(1 for r in RUNS for c in runs[r].values() if c.get('unsure')),
            'harm_labels_policy': sorted(l for l in union if l[1].startswith('H-') and l[0][0] == 'U'),
            'harm_labels_para_policy': sorted(l for l in para if l[1].startswith('H-') and l[0][0] == 'U'),
            'harm_labels_interface': sorted(l for l in union if l[1].startswith('H-') and l[0][0] == 'W'),
            'vs_standin_majority': scores(majority, reference),
            'vs_standin_union': scores(union, reference),
        },
        'stage3': {
            'per_run': {r: len(m_sets[r]) for r in RUNS},
            'union': len(m_union),
            'votes': {str(n): sum(v == n for v in m_votes.values()) for n in RUNS},
            'jaccard_runs': {'1-2': jaccard(m_sets[1], m_sets[2]), '1-3': jaccard(m_sets[1], m_sets[3]),
                             '2-3': jaccard(m_sets[2], m_sets[3])},
            'vs_standin_majority': scores(m_majority, m_reference),
            'vs_standin_union': scores(m_union, m_reference),
        },
        'differences': {
            'model_majority_not_standin': sorted(majority - reference),
            'standin_not_in_any_run': sorted(reference - union),
            'measure_majority_not_standin': sorted(m_majority - m_reference),
            'measure_standin_not_in_any_run': sorted(m_reference - m_union),
        },
    }
    if out_path:
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=1)
    return result


if __name__ == '__main__':
    print(json.dumps(main(*sys.argv[1:4]), indent=1))
