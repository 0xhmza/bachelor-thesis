"""Coverage of the 95 % intervals on a constructed corpus, with and without the variance floor.

    python check_coverage.py [repetitions]

The corpus is the one of tests/test_design.py: 40 policies of 60 units, 3 % positives,
two correlated models, policies on which both models miss more often, 5 % uncertain answers.
Writes output/coverage.md."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / 'tests'))
import design as d  # noqa: E402
from test_design import corpus  # noqa: E402


def main(reps=1000):
    units, g, truth = corpus(7)
    T = sum(truth.values())
    lines = ['| V5 units | other strata | plain coverage | with floor | mean half-width with floor |',
             '|---|---|---|---|---|']
    for v5 in (150, 200, 300):
        alloc = {'V1': 120, 'V2': 80, 'V3': 40, 'V4': 60, 'V5': v5}
        plain = floor = 0
        width = 0.0
        for s in range(reps):
            m = d.draw(units, alloc, seed=s)
            y = {r['unit']: truth[r['unit']] for r in m if r['selected']}
            a = d.estimate_total(g, y, m, floor=False)
            b = d.estimate_total(g, y, m)
            plain += a['low'] <= T <= a['high']
            floor += b['low'] <= T <= b['high']
            width += (b['high'] - b['low']) / 2
        lines.append(f'| {v5} | 300 | {plain / reps:.3f} | {floor / reps:.3f} | {width / reps:.1f} (true total {T}) |')
    out = Path(__file__).parent / 'output'
    out.mkdir(exist_ok=True)
    text = '\n'.join(lines) + '\n'
    (out / 'coverage.md').write_text(text, encoding='utf-8')
    print(text)


if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 1000)
