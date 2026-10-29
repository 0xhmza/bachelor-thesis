"""Validate actual archives, exact source embedding and download ranking rules."""
import csv
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import sampling

BASE = Path(__file__).resolve().parent
RUN = BASE / 'raw/20261011T161853545650Z'

class RankingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.run = self.base / 'raw' / 'synthetic'
        self.run.mkdir(parents=True)
        self.out = self.base / 'processed' / 'synthetic'
        self.out.mkdir(parents=True)
        proof = self.run / 'constructed_fixture.txt'
        proof.write_text('Constructed test evidence; not study observations.', encoding='utf-8')
        self.sha = sampling.digest(proof)
        self.frame = {'discovery_complete': True, 'sessions': [
            {'platform': store, 'keyword_id': k[0], 'storefront': 'DE',
             'method': 'store_ui_capture', 'result_listing_ids': [], 'exhausted': True,
             'evidence_file': proof.name, 'evidence_sha256': self.sha}
            for store in ['play', 'apple'] for k in sampling.KEYWORDS]}
        self.product = {'app_id': 'synthetic:one', 'name': 'Constructed app',
            'domain': 'fitness', 'listing_ids': ['apple:synthetic', 'play:synthetic'],
            'evidence': [{'file': proof.name, 'sha256': self.sha}],
            **{k: True for k in ['tracking', 'free_install', 'DE_EN_interface',
            'policy_reachable', 'not_DiGA', 'not_duplicate', 'identity_verified',
            'counterpart_coverage_verified', 'minimum_1000_ratings', 'German_store_available']}}
        self.values = [{'listing_id': key, 'country': 'DE', 'start': sampling.START,
            'end': sampling.END, 'provider': 'constructed_test_provider',
            'metric': 'constructed_same_metric', 'downloads': n,
            'evidence_file': proof.name, 'evidence_sha256': self.sha,
            'retrieved_utc': '2026-10-11T00:00:00+00:00'}
            for key, n in [('apple:synthetic', 30), ('play:synthetic', 70)]]

    def tearDown(self):
        self.temp.cleanup()

    def execute(self):
        for name, value in [('frame_review.json', self.frame), ('products.json', [self.product])]:
            (self.out / name).write_text(json.dumps(value), encoding='utf-8')
        sampling.table(self.out / 'downloads.csv', self.values, list(self.values[0]))
        with patch.object(sampling, 'BASE', self.base):
            sampling.rank(self.run)

    def test_comparable_platform_counts_sum(self):
        self.execute()
        with (self.out / 'final_sample.csv').open(encoding='utf-8-sig') as f:
            row = next(csv.DictReader(f))
        self.assertEqual(row['combined_DE_downloads'], '100')

    def test_missing_counterpart_never_becomes_zero(self):
        self.values.pop()
        with self.assertRaisesRegex(ValueError, 'Missing platform downloads'):
            self.execute()

    def test_wrong_geography_is_rejected(self):
        self.values[0]['country'] = 'US'
        with self.assertRaisesRegex(ValueError, 'Different country'):
            self.execute()

    def test_mixed_provider_is_rejected(self):
        self.values[0]['provider'] = 'different_provider'
        with self.assertRaisesRegex(ValueError, 'Mixed providers'):
            self.execute()

    def test_incomplete_frame_is_rejected(self):
        self.frame['sessions'].pop()
        with self.assertRaisesRegex(ValueError, '38'):
            self.execute()

    def test_unverified_eligibility_is_rejected(self):
        self.product['not_DiGA'] = False
        with self.assertRaisesRegex(ValueError, 'Unverified eligibility'):
            self.execute()

if __name__ == '__main__':
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(RankingTests))
    assert result.wasSuccessful()
    requests = sampling.load(RUN / 'requests.json')
    for r in requests:
        assert sampling.digest(RUN / r['file']) == r['sha256']
    tex = (BASE / 'sampling_report.tex').read_text(encoding='utf-8')
    embedded = tex.split('\\begin{lstlisting}\n', 1)[1].split('\\end{lstlisting}', 1)[0]
    source = (BASE / 'sampling.py').read_text(encoding='utf-8')
    assert embedded == source + '\n', 'Embedded executable source differs'
    out = BASE / 'processed' / RUN.name
    before = sampling.digest(out / 'listings.json')
    sampling.summarize(RUN)
    assert sampling.digest(out / 'listings.json') == before
    assert not (out / 'final_sample.csv').exists()
    audit = {'tests_passed': result.testsRun, 'raw_response_hashes_verified': len(requests),
        'embedded_source_exact': True, 'offline_metadata_reproduction_identical': True,
        'final_sample_not_fabricated': True,
        'note': 'Ranking tests use temporary constructed data, never study downloads.'}
    (BASE / 'evidence/verification.json').write_text(json.dumps(audit, indent=2), encoding='utf-8')
    print(json.dumps(audit, indent=2))
