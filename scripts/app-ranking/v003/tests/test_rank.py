import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import rank  # noqa: E402


def listing(store, lid, german, developer, name, world=0):
    return {'store': store, 'id': lid, 'name': name, 'developer': developer, 'german': german, 'world': world,
            'provider': rank.provider_key(developer, {}), 'best': 1}


class RankTests(unittest.TestCase):
    def test_same_app_in_both_stores_becomes_one_candidate(self):
        apple = {'a1': listing('apple', 'a1', 100, 'Flo Health UK Limited', 'Flo Perioden- & Zyklus-Tracker')}
        play = {'p1': listing('play', 'p1', 300, 'Flo Health Inc.', 'Flo Zyklus- & Periodenkalender'),
                'p2': listing('play', 'p2', 50, 'Other', 'Steps')}
        cands = rank.candidates(apple, play)
        self.assertEqual(len(cands), 2)
        flo = next(c for c in cands if c['play'] and c['play']['id'] == 'p1')
        self.assertEqual((flo['r'], flo['v']), (100, 300))

    def test_dotted_legal_forms_and_compact_titles(self):
        self.assertEqual(rank.provider_key('Virtuagym B.V.', {}), rank.provider_key('Virtuagym', {}))
        self.assertEqual(rank.provider_key('BLATT sp. z o.o.', {}), 'blatt')
        ww = listing('apple', 'a', 1, 'WW International, Inc.', 'WeightWatchers Programm')
        self.assertTrue(rank.same_app(ww, listing('play', 'p', 1, 'WW INTERNATIONAL, INC', 'Weight Watchers Programm')))

    def test_manual_pair_merges_translated_titles(self):
        apple = {'a': listing('apple', 'a', 10, 'X', 'Monitor Your Weight')}
        play = {'p': listing('play', 'p', 5, 'X', 'Überwache dein Gewicht')}
        self.assertEqual(len(rank.candidates(apple, play)), 2)
        self.assertEqual(len(rank.candidates(apple, play, {'p': 'a'})), 1)

    def test_calibration_uses_median_ratio_and_os_shares(self):
        cands = [{'play': 1, 'apple': 1, 'r': 10, 'v': 20}, {'play': 1, 'apple': 1, 'r': 10, 'v': 40},
                 {'play': 1, 'apple': 1, 'r': 10, 'v': 60}, {'play': 1, 'apple': None, 'r': 0, 'v': 99}]
        c, pairs = rank.calibration(cands, 0.25, 0.75)
        self.assertEqual(pairs, 3)
        self.assertAlmostEqual(c, 4 * 0.25 / 0.75)

    def test_select_skips_taken_providers_and_reports_pending(self):
        a = {'key': 'a', 'provider': 'x', 'play': {'store': 'play', 'id': 'a'}, 'apple': None}
        b = {'key': 'b', 'provider': 'x', 'play': {'store': 'play', 'id': 'b'}, 'apple': None}
        c = {'key': 'c', 'provider': 'y', 'play': {'store': 'play', 'id': 'c'}, 'apple': None}
        d = {'key': 'd', 'provider': 'z', 'play': {'store': 'play', 'id': 'd'}, 'apple': None}
        screening = {('play', 'a'): {'decision': 'eligible', 'criterion': ''},
                     ('play', 'c'): {'decision': 'excluded', 'criterion': 'E1'}}
        sel, skipped, excluded, pending = rank.select([a, b, c, d], screening, 2, set())
        self.assertEqual([x['key'] for x in sel], ['a', 'd'])
        self.assertEqual([x['key'] for x in skipped], ['b'])
        self.assertEqual([x['key'] for x, _ in excluded], ['c'])
        self.assertEqual([x['key'] for x in pending], ['d'])

    def test_preinstalled_vendor_blocks_its_apps(self):
        a = {'key': 'a', 'provider': rank.provider_key('Samsung Electronics Co., Ltd.', {}), 'play': {'store': 'play', 'id': 'a'}, 'apple': None}
        sel, skipped, *_ = rank.select([a], {}, 1, {'samsung electronics'})
        self.assertEqual((sel, [x['key'] for x in skipped]), ([], ['a']))

    def test_excluded_listing_in_either_store_excludes_the_candidate(self):
        c = {'play': {'store': 'play', 'id': 'p'}, 'apple': {'store': 'apple', 'id': 'a'}}
        screening = {('play', 'p'): {'decision': 'eligible'}, ('apple', 'a'): {'decision': 'excluded', 'criterion': 'E3'}}
        self.assertEqual(rank.decision(c, screening)['decision'], 'excluded')

    def test_spearman_and_tex(self):
        self.assertAlmostEqual(rank.spearman([1, 2, 3], [3, 2, 1]), -1.0)
        self.assertEqual(rank.tex('A & B™ 100%'), r'A \& B 100\%')


if __name__ == '__main__':
    unittest.main()
