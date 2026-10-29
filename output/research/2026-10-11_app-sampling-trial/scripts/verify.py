"""Meaningful checks for a collection pipeline used for research selection."""
import argparse
import hashlib
import json
import unittest
from pathlib import Path
from process import load, parse_play, validate, BASE
from sample_set import rank_apps, select, CHECKS

class LogicTests(unittest.TestCase):
    def test_embedded_number_is_preserved(self):
        detail = [None] * 52
        detail[0] = ['Synthetic fixture']
        detail[13] = ['1,000+', 1000, 1732]
        text = "<script>AF_initDataCallback({key: 'ds:5', data:" + json.dumps([None, [None, None, detail]]) + ", sideChannel: {}});</script>"
        result = parse_play(text)
        self.assertEqual(result['realInstalls'], 1732)
        self.assertIsNone(result['rating_count'])

    def test_missing_dataset_is_failure(self):
        with self.assertRaises(ValueError):
            parse_play('<html>consent or error page</html>')

    def test_impossible_count_rejected(self):
        with self.assertRaises(ValueError):
            validate({'name': 'fixture', 'rating': 4, 'minInstalls': 1000, 'realInstalls': 100})

    def test_weighting_only_eligible_listings_and_deduplication(self):
        rows = [{'listing_id': k, 'name': 'fixture', 'platform': 'apple' if k == 'a' else 'play',
                 'domain_provisional': 'fitness', 'rating': rating, 'rating_count': n, 'url': 'https://example.invalid'}
                for k, rating, n in [('a', 4, 1000), ('b', 5, 3000), ('c', 1, 999)]]
        screen = [{'listing_id': k, 'numeric_status': status} for k, status in
                  [('a', 'passes_numeric'), ('b', 'passes_numeric'), ('c', 'exclude_listing')]]
        ranked = rank_apps(rows, screen, {'listing_to_app': {'a': 'one', 'b': 'one', 'c': 'one'}}, {})
        self.assertEqual(len(ranked), 1)
        self.assertEqual(ranked[0]['weighted_score'], '4.75')
        self.assertEqual(ranked[0]['eligible_rating_count'], 4000)
        self.assertEqual(len(ranked[0]['listing_ids']), 3)
        self.assertFalse(ranked[0]['final_eligible'])
        self.assertEqual(select(ranked, {'fitness': 30}, final=True), [])

def main(run):
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(LogicTests))
    if not result.wasSuccessful():
        raise SystemExit(1)
    verified = 0
    for path in sorted(run.rglob('*.meta.json')):
        meta = load(path)
        body = path.parent / meta['file']
        if hashlib.sha256(body.read_bytes()).hexdigest() != meta['sha256']:
            raise ValueError('Raw integrity mismatch: ' + str(body))
        verified += 1
    out = BASE / 'processed' / run.name
    listings = load(out / 'listings.json')
    assert len({r['listing_id'] for r in listings}) == len(listings)
    for row in listings:
        validate(row)
        assert hashlib.sha256((run / row['raw_file']).read_bytes()).hexdigest() == row['source_sha256']
    working = load(out / 'trial_working_set.json')
    assert len({r['app_id'] for r in working}) == len(working)
    assert not load(out / 'final_sample.json'), 'This trial must not claim a final approved sample'
    for domain, limit in {'fitness': 30, 'fertility': 20}.items():
        assert sum(r['domain'] == domain for r in working) <= limit
    report = {'logic_tests': result.testsRun, 'logic_tests_passed': result.wasSuccessful(),
              'raw_response_hashes_verified': verified, 'unique_listing_ids': len(listings),
              'working_set_app_ids_unique': True, 'final_sample_correctly_withheld': True}
    (out / 'verification.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('run', type=Path)
    main(p.parse_args().run.resolve())
