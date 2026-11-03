import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import rank  # noqa: E402


def app(store, lid, ratings, developer, name=None):
    return {'store': store, 'id': lid, 'ratings': ratings, 'developer': developer, 'name': name or lid,
            'provider': rank.provider_key(developer, {})}


def eligible(*listings):
    return {(l['store'], l['id']): {'decision': 'eligible', 'criterion': ''} for l in listings}


class SelectionTests(unittest.TestCase):
    def test_provider_key_drops_legal_forms_and_case(self):
        self.assertEqual(rank.provider_key('Leap Fitness Group', {}), rank.provider_key('LEAP FITNESS', {}))
        self.assertEqual(rank.provider_key('Flo Health, Inc.', {}), 'flo health')
        self.assertEqual(rank.provider_key('X Ltd', {'x': 'y'}), 'y')
        self.assertNotEqual(rank.provider_key('帆 杨', {}), rank.provider_key('李 明', {}))
        self.assertNotEqual(rank.provider_key('帆 杨', {}), '')
        self.assertEqual(rank.provider_key('The Pokémon Company', {}), rank.provider_key('The Pokemon Company', {}))

    def test_alternation_starts_with_given_store(self):
        play = [app('play', 'p1', 900, 'A'), app('play', 'p2', 800, 'B')]
        apple = [app('apple', 'a1', 50, 'C'), app('apple', 'a2', 40, 'D')]
        sel, *_ = rank.select({'play': play, 'apple': apple}, eligible(*play, *apple), 3, 'play', set())
        self.assertEqual([l['id'] for l in sel], ['p1', 'a1', 'p2'])

    def test_developer_already_in_sample_is_skipped_across_stores(self):
        play = [app('play', 'p1', 900, 'Leap Fitness Group'), app('play', 'p2', 800, 'Leap Fitness'), app('play', 'p3', 10, 'B')]
        apple = [app('apple', 'a1', 50, 'LEAP FITNESS GROUP LIMITED'), app('apple', 'a2', 40, 'C')]
        sel, skipped, *_ = rank.select({'play': play, 'apple': apple}, eligible(*play, *apple), 3, 'play', set())
        self.assertEqual([l['id'] for l in sel], ['p1', 'a2', 'p3'])
        self.assertEqual({l['id'] for l in skipped}, {'p2', 'a1'})

    def test_preinstalled_vendor_blocks_its_store_apps(self):
        play = [app('play', 'p1', 900, 'Samsung Electronics Co., Ltd.'), app('play', 'p2', 10, 'B')]
        sel, *_ = rank.select({'play': play, 'apple': []}, eligible(*play), 1, 'play', {'samsung electronics'})
        self.assertEqual([l['id'] for l in sel], ['p2'])

    def test_excluded_listing_is_passed_and_pending_is_reported(self):
        play = [app('play', 'p1', 900, 'A'), app('play', 'p2', 800, 'B')]
        screening = {('play', 'p1'): {'decision': 'excluded', 'criterion': 'E1'}}
        sel, _, excluded, pending = rank.select({'play': play, 'apple': []}, screening, 1, 'play', set())
        self.assertEqual([l['id'] for l in sel], ['p2'])
        self.assertEqual([l['id'] for l, _ in excluded], ['p1'])
        self.assertEqual([l['id'] for l in pending], ['p2'])

    def test_exhausted_store_lets_the_other_continue(self):
        play = [app('play', 'p1', 900, 'A')]
        apple = [app('apple', 'a1', 50, 'C'), app('apple', 'a2', 40, 'D')]
        sel, *_ = rank.select({'play': play, 'apple': apple}, eligible(*play, *apple), 3, 'play', set())
        self.assertEqual([l['id'] for l in sel], ['p1', 'a1', 'a2'])

    def test_same_app_across_store_titles(self):
        self.assertTrue(rank.same_app(app('play', 'p', 1, 'Flo Health Inc.', 'Flo Zyklus- & Periodenkalender'),
                                      app('apple', 'a', 1, 'FLO HEALTH UK LIMITED', 'Flo Perioden- & Zyklus-Tracker')))
        self.assertFalse(rank.same_app(app('play', 'p', 1, 'A', 'Flo Zyklus'), app('apple', 'a', 1, 'B', 'Flo Zyklus')))

    def test_spearman_with_ties(self):
        self.assertAlmostEqual(rank.spearman([1, 2, 3, 4], [10, 20, 30, 40]), 1.0)
        self.assertAlmostEqual(rank.spearman([1, 2, 3, 4], [4, 3, 2, 1]), -1.0)
        self.assertAlmostEqual(rank.spearman([1, 1, 2], [1, 1, 2]), 1.0)

    def test_tex_escapes_and_drops_unsupported_characters(self):
        self.assertEqual(rank.tex('Clover － Perioden & Zyklus™ 100%'), r'Clover - Perioden \& Zyklus 100\%')
        self.assertEqual(rank.tex('Apple Fitness'), 'Apple Fitness')

    def test_release_dates(self):
        self.assertEqual(rank.released('2015-03-12T07:00:00Z'), date(2015, 3, 12))
        self.assertEqual(rank.released('12.03.2015'), date(2015, 3, 12))
        self.assertEqual(rank.released('12. März 2015'), date(2015, 3, 12))


if __name__ == '__main__':
    unittest.main()
