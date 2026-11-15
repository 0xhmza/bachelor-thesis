import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import rank  # noqa: E402

SNAP = datetime(2026, 10, 20, tzinfo=timezone.utc)


def app(i, rating, count, store='apple', released='2020-01-01T00:00:00Z'):
    return {'id': f'{store}:{i}', 'name': f'app{i}', 'store': store, 'rating': rating,
        'rating_count': count, 'released': released, 'keywords': ['k']}


class RankingTests(unittest.TestCase):
    def test_average_ranks_share_tied_positions(self):
        self.assertEqual(rank.avg_ranks([5, 3, 3, 1]), [1.0, 2.5, 2.5, 4.0])

    def test_shrinkage_pulls_small_counts_toward_pool_mean(self):
        rows = [app(1, 5.0, 1000), app(2, 4.0, 1000000), app(3, 3.0, 1000)]
        out = {r['id']: r for r in rank.rank_store(rows, 0.5, 1000, SNAP)}
        self.assertAlmostEqual(out['apple:1']['shrunk_rating'], 0.5 * 5.0 + 0.5 * 4.0)
        self.assertGreater(out['apple:2']['shrunk_rating'], 3.99)

    def test_large_app_beats_marginally_better_rated_small_app(self):
        rows = [app(1, 4.8, 1100), app(2, 4.6, 1200000), app(3, 4.4, 5000)]
        order = [r['id'] for r in rank.rank_store(rows, 0.5, 1000, SNAP)]
        self.assertEqual(order[0], 'apple:2')

    def test_weight_extremes_follow_single_criterion(self):
        rows = [app(1, 4.9, 1500), app(2, 4.0, 900000), app(3, 4.7, 200000)]
        by_exposure = [r['id'] for r in rank.rank_store(rows, 1.0, 1000, SNAP)]
        # a large prior weight lets the 1,500-rating 4.9 fall behind the well-evidenced 4.7
        by_quality = [r['id'] for r in rank.rank_store(rows, 0.0, 5000, SNAP)]
        self.assertEqual(by_exposure, ['apple:2', 'apple:3', 'apple:1'])
        self.assertEqual(by_quality[0], 'apple:3')

    def test_stores_are_ranked_separately_then_merged_by_percentile(self):
        apple = [app(i, 4.5, 2000 + i) for i in range(4)]
        play = [app(i, 4.5, 5000000 + i, store='play') for i in range(2)]
        merged = rank.rank_all(apple + play, 0.5, 1000, SNAP)
        self.assertEqual(merged[0]['store_position'], 1)
        # Play's best sits at percentile 0.25, apple's best at 0.125: apple first, then play
        self.assertEqual([r['store'] for r in merged[:2]], ['apple', 'play'])
        self.assertEqual([r['position'] for r in merged], list(range(1, 7)))

    def test_ordering_is_deterministic_on_full_ties(self):
        rows = [app(2, 4.5, 3000), app(1, 4.5, 3000)]
        self.assertEqual([r['id'] for r in rank.rank_store(rows, 0.5, 1000, SNAP)], ['apple:1', 'apple:2'])

    def test_compare_reports_entries_and_exits(self):
        rows = [app(i, 4.0 + i / 10, 2000 * (i + 1)) for i in range(6)]
        base = rank.rank_all(rows, 0.5, 1000, SNAP)
        same = rank.compare(base, base, 3)
        self.assertEqual(same['shared_with_main'], 3)
        self.assertAlmostEqual(same['spearman_positions'], 1.0)

    def test_cli_writes_cascade_and_respects_floor_and_exclusions(self):
        payload = {'timestamp': '2026-10-20T19:00:00+00:00', 'results': {'fitness': [
            {'ID': 1, 'App Name': 'A', 'Average Rating': 4.5, 'Rating Count': 5000, 'Released': '2019-01-01T00:00:00Z'},
            {'ID': 2, 'App Name': 'B', 'Average Rating': 4.9, 'Rating Count': 50},
            {'ID': 3, 'App Name': 'C', 'Average Rating': 4.2, 'Rating Count': 90000},
            {'ID': 4, 'App Name': 'D', 'Average Rating': 4.4, 'Rating Count': 8000},
            {'ID': 5, 'App Name': 'E'}]}}
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / 'in.json'
            src.write_text(json.dumps(payload), encoding='utf-8')
            excl = Path(tmp) / 'ex.txt'
            excl.write_text('apple:4\n', encoding='utf-8')
            rank.main([str(src), '--domain', 'fitness', '--exclude', str(excl),
                '--out-dir', str(Path(tmp) / 'out'), '--top', '2'])
            manifest = json.loads(next((Path(tmp) / 'out').glob('*.json')).read_text(encoding='utf-8'))
        c = manifest['cascade']
        self.assertEqual((c['distinct_listings'], c['missing_rating_data'], c['excluded_manually'],
            c['below_floor'], c['ranked']), (5, 1, 1, 1, 2))
        self.assertIn('exposure_per_year_since_release', manifest['sensitivity'])
        self.assertNotIn('prior_weight_x2', manifest['sensitivity'])  # irrelevant at weight 1
        self.assertEqual(manifest['parameters']['weight_exposure'], 1.0)

    def test_default_weight_orders_purely_by_rating_count(self):
        rows = [app(1, 5.0, 1500), app(2, 3.0, 900000), app(3, 4.5, 20000)]
        order = [r['id'] for r in rank.rank_store(rows, 1.0, 1000, SNAP)]
        self.assertEqual(order, ['apple:2', 'apple:3', 'apple:1'])


if __name__ == '__main__':
    unittest.main()
