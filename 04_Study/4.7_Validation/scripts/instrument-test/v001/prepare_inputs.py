"""Write the model inputs of the instrument test.

    python prepare_inputs.py <units.jsonl> <walkthrough.yaml> <out_dir>

Policy units go into two consecutive parts so that each model call keeps its
neighbouring units as context. The interface units join the second part and carry
no sign that they are synthetic, so that the model codes them like any other text.
"""
import json
import sys
from pathlib import Path

import yaml

SPLIT = 'U093'  # section 3.6 starts a new block of the policy


def main(units_path, walkthrough_path, out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    units = [json.loads(line) for line in open(units_path, encoding='utf-8')]
    with open(walkthrough_path, encoding='utf-8') as f:
        walkthrough = yaml.safe_load(f)
    rows = [{'unit': u['unit'], 'heading': u['heading'], 'text': u['text']} for u in units]
    first = [r for r in rows if r['unit'] < SPLIT]
    second = [r for r in rows if r['unit'] >= SPLIT]
    second += [{'unit': w['unit'], 'heading': w['screen'], 'text': w['text']}
               for w in walkthrough['interface_units']]
    for name, part in (('part1', first), ('part2', second)):
        with open(out / f'{name}.jsonl', 'w', encoding='utf-8') as f:
            for row in part:
                f.write(json.dumps(row, ensure_ascii=False) + '\n')
        print(name, len(part), 'units')


if __name__ == '__main__':
    main(*sys.argv[1:4])
