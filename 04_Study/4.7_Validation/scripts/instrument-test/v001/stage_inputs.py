"""Check the stage 1 output and write the inputs of stages 2 and 3.

    python stage_inputs.py <llm_dir>

A code without an exact span is discarded (codebook rule 4). A unit goes to stage 2
if any of the three stage 1 runs returned a named harm, and to stage 3 if any run set
the protection flag: a label returned once is reviewed, not discarded.
"""
import json
import re
import sys
from pathlib import Path


def norm(text):
    return re.sub(r'\s+', ' ', text).strip()


def load_units(llm):
    units = {}
    for part in ('part1', 'part2'):
        for line in open(llm / 'input' / f'{part}.jsonl', encoding='utf-8'):
            row = json.loads(line)
            units[row['unit']] = row
    return units


def load_stage1(llm, folder, run):
    """Return {unit: entry} of one run, across both parts."""
    out = {}
    for part in ('part1', 'part2'):
        with open(llm / folder / f'run{run}_{part}.json', encoding='utf-8') as f:
            data = json.load(f)
        for entry in data['units']:
            out[entry['unit']] = entry
    return out


def span_ok(span, text):
    return bool(span) and norm(span) in norm(text)


def main(llm_dir):
    llm = Path(llm_dir)
    units = load_units(llm)
    harm, protection = {}, set()
    for folder, run in (('stage1', 1), ('stage1', 2), ('stage1', 3), ('stage1p', 1)):
        total = bad = 0
        for unit, entry in load_stage1(llm, folder, run).items():
            for code in entry.get('codes', []):
                total += 1
                if not span_ok(code.get('span'), units[unit]['text']):
                    bad += 1
                    continue
                if folder == 'stage1' and code.get('code') == 'L-HRM':
                    harm.setdefault(unit, set()).add(code.get('harm'))
            if folder == 'stage1' and entry.get('flags', {}).get('protection'):
                protection.add(unit)
        print(folder, run, 'codes', total, 'spans not found', bad)
    keys = list(units)
    def with_context(unit):
        i = keys.index(unit)
        row = dict(units[unit])
        row['previous'] = units[keys[i - 1]]['text'] if i else ''
        row['next'] = units[keys[i + 1]]['text'] if i + 1 < len(keys) else ''
        return row
    with open(llm / 'input' / 'stage2.jsonl', 'w', encoding='utf-8') as f:
        for unit in keys:
            if unit in harm:
                row = with_context(unit)
                row['harms'] = sorted(h for h in harm[unit] if h)
                f.write(json.dumps(row, ensure_ascii=False) + '\n')
    with open(llm / 'input' / 'stage3.jsonl', 'w', encoding='utf-8') as f:
        for unit in keys:
            if unit in protection:
                f.write(json.dumps(with_context(unit), ensure_ascii=False) + '\n')
    print('stage 2 units', len(harm), sorted(harm))
    print('stage 3 units', len(protection))


if __name__ == '__main__':
    main(sys.argv[1])
