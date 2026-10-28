import csv
import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import rank  # noqa: E402

REGISTER = Path(__file__).resolve().parents[4] / '04_Study' / 'App-Sample' / 'identity.csv'


def listing(store, lid, german, developer, name, bundle='', description='', world=0):
    return {'store': store, 'id': lid, 'name': name, 'developer': developer, 'german': german, 'world': world,
            'developer_key': rank.provider_key(developer, {}), 'bundle': bundle if store == 'apple' else lid,
            'description': description, 'best': 1}


def nike():
    """The review's Nike case: the App Store listing of Nike Training Club has more ratings."""
    apple = {'301521403': listing('apple', '301521403', 40450, 'Nike, Inc', 'Nike Training Club', 'com.nike.niketrainingclub'),
             '387771637': listing('apple', '387771637', 36896, 'Nike, Inc', 'Nike Run Club: Laufcoach', 'com.nike.nikeplus-gps')}
    play = {'com.nike.plusgps': listing('play', 'com.nike.plusgps', 6305, 'Nike, Inc.', 'Nike Run Club: Laufen & Cardio'),
            'com.nike.ntc': listing('play', 'com.nike.ntc', 2587, 'Nike, Inc.', 'Nike Training Club')}
    same = {('com.nike.plusgps', '387771637'), ('com.nike.ntc', '301521403')}
    return apple, play, same


def pairs(cands):
    return sorted((c['play']['id'], c['apple']['id']) for c in cands if c['play'] and c['apple'])


def row(p, a, decision, evidence='name', rationale='checked', reviewer='r', date='2026-10-28'):
    return {'play_id': p, 'apple_id': a, 'decision': decision, 'evidence': evidence, 'rationale': rationale,
            'reviewer': reviewer, 'review_date': date}


class IdentityTests(unittest.TestCase):
    def test_nike_run_club_pairs_with_run_club_not_training_club(self):
        apple, play, same = nike()
        self.assertEqual(pairs(rank.candidates(apple, play, same)),
                         [('com.nike.ntc', '301521403'), ('com.nike.plusgps', '387771637')])

    def test_babycenter_is_not_what_to_expect(self):
        apple = {'289560144': listing('apple', '289560144', 648, 'Everyday Health, Inc.', 'Pregnancy Tracker App - WTE'),
                 '386022579': listing('apple', '386022579', 6928, 'Everyday Health, Inc.', 'BabyCenter Pregnancy Tracker')}
        play = {'com.babycenter.pregnancytracker': listing('play', 'com.babycenter.pregnancytracker', 15132, 'BabyCenter',
                                                           'Pregnancy App & Baby Tracker')}
        cands = rank.candidates(apple, play, {('com.babycenter.pregnancytracker', '386022579')})
        self.assertEqual(pairs(cands), [('com.babycenter.pregnancytracker', '386022579')])
        wte = next(c for c in cands if c['apple'] and c['apple']['id'] == '289560144')
        self.assertIsNone(wte['play'])

    def test_mens_app_is_not_paired_with_the_womens_app(self):
        apple = {'1502526521': listing('apple', '1502526521', 619, 'Leap Health', 'Abnehmen für Frauen'),
                 '1460546771': listing('apple', '1460546771', 368, 'Leap Health', 'Abnehmen für Männer zu Hause')}
        play = {'men': listing('play', 'men', 16125, 'Leap Fitness Group', 'Abnehmen für Männer-30 Tagen'),
                'women': listing('play', 'women', 5569, 'Leap Fitness Group', 'Abnehm-App für Frauen')}
        self.assertEqual(pairs(rank.candidates(apple, play, {('men', '1460546771'), ('women', '1502526521')})),
                         [('men', '1460546771'), ('women', '1502526521')])

    def test_rating_counts_and_input_order_do_not_change_identity(self):
        apple, play, same = nike()
        expected = pairs(rank.candidates(apple, play, same))
        rng = random.Random(1)
        for _ in range(20):
            a = {k: dict(v, german=rng.randint(0, 10 ** 6)) for k, v in rng.sample(sorted(apple.items()), len(apple))}
            p = {k: dict(v, german=rng.randint(0, 10 ** 6)) for k, v in rng.sample(sorted(play.items()), len(play))}
            self.assertEqual(pairs(rank.candidates(a, p, list(same)[::-1])), expected)

    def test_only_same_product_decisions_merge_listings(self):
        apple, play, _ = nike()
        self.assertEqual(pairs(rank.candidates(apple, play)), [])  # a shared developer and first word decide nothing
        self.assertEqual(len(rank.candidates(apple, play)), 4)

    def test_proposals_suggest_pairs_without_deciding(self):
        apple, play, _ = nike()
        apple['9'] = listing('apple', '9', 5, 'Someone Else', 'Lose It! – Calorie Counter', 'com.fitnow.loseit')
        apple['8'] = listing('apple', '8', 5, 'Other Studio', 'Schrittzähler', 'x.y')
        apple['7'] = listing('apple', '7', 5, 'Third', 'Unrelated', 'a.b', ' '.join(f'w{i}' for i in range(30)))
        play['com.fitnow.loseit'] = listing('play', 'com.fitnow.loseit', 5, 'FitNow, Inc.', 'Lose It! - Kalorienzähler')
        play['s'] = listing('play', 's', 5, 'Yet Another', 'Schrittzähler')
        play['t'] = listing('play', 't', 5, 'Fourth', 'Also unrelated', description=' '.join(f'w{i}' for i in range(30)))
        found = rank.proposals(apple, play)
        self.assertEqual(found[('com.nike.plusgps', '301521403')]['reasons'], ['developer'])
        self.assertEqual(found[('com.fitnow.loseit', '9')]['reasons'], ['app-id'])
        self.assertEqual(found[('s', '8')]['reasons'], ['title'])
        self.assertEqual(found[('t', '7')]['reasons'], ['text'])
        self.assertNotIn(('s', '9'), found)
        self.assertEqual(pairs(rank.candidates(apple, play)), [])

    def test_one_product_joins_its_developers_into_one_provider(self):
        listings = {'play': {'p': listing('play', 'p', 1, 'Simple Design Ltd.', 'Period Tracker'),
                             'q': listing('play', 'q', 1, 'Leap Fitness Group', 'Home Workout')},
                    'apple': {'a': listing('apple', 'a', 1, 'ABISHKKING LIMITED.', 'Period Calendar'),
                              'b': listing('apple', 'b', 1, 'Leap Fitness Group', 'Step Counter')}}
        find = rank.merge_providers(listings, [('p', 'a')])
        self.assertEqual(find('simple design'), find('abishkking'))
        self.assertNotEqual(find('simple design'), find('leap fitness'))
        find = rank.merge_providers(listings, [('p', 'a'), ('p', 'b')])
        self.assertEqual(len({find(k) for k in ('simple design', 'abishkking', 'leap fitness')}), 1)

    def test_register_errors_block_the_run(self):
        listings = {'play': {'p': {}, 'q': {}}, 'apple': {'a': {}, 'b': {}}}
        self.assertEqual(rank.identity_errors([row('p', 'a', 'same'), row('q', 'b', 'different', '')], listings), [])
        bad = rank.identity_errors([row('p', 'a', 'same'), row('p', 'b', 'same'), row('q', 'a', 'same', ''),
                                    row('q', 'b', 'maybe'), row('x', 'a', 'different', ''),
                                    row('q', 'b', 'same', 'provider'), row('p', 'a', 'same', rationale='')], listings)
        text = ' | '.join(bad)
        for part in ('pair listed twice', 'play_id p in 3 same-product pairs', 'without product-specific evidence',
                     "decision 'maybe'", 'listing not in the collections', "unknown evidence ['provider']",
                     'rationale, reviewer or review date missing'):
            self.assertIn(part, text)


class RegisterTests(unittest.TestCase):
    """The decisions of review F01 (28 October 2026) as recorded in the identity register."""
    expected = {('com.nike.plusgps', '387771637'): 'same', ('com.nike.plusgps', '301521403'): 'different',
                ('com.nike.ntc', '301521403'): 'same', ('com.nike.ntc', '387771637'): 'different',
                ('com.babycenter.pregnancytracker', '386022579'): 'same',
                ('com.babycenter.pregnancytracker', '289560144'): 'different',
                ('menloseweight.loseweightappformen.weightlossformen', '1460546771'): 'same',
                ('menloseweight.loseweightappformen.weightlossformen', '1502526521'): 'different',
                ('loseweightapp.loseweightappforwomen.womenworkoutathome', '1502526521'): 'same',
                ('loseweightapp.loseweightappforwomen.womenworkoutathome', '1460546771'): 'different'}

    @unittest.skipUnless(REGISTER.exists(), 'identity register not found')
    def test_reference_pairs(self):
        with open(REGISTER, encoding='utf-8') as f:
            rows = {(r['play_id'], r['apple_id']): r for r in csv.DictReader(f)}
        for k, d in self.expected.items():
            self.assertEqual(rows[k]['decision'], d, k)
        for r in rows.values():
            if r['decision'] == 'same':
                self.assertTrue(r['evidence'].strip(), r)


class RankTests(unittest.TestCase):
    def test_dotted_legal_forms(self):
        self.assertEqual(rank.provider_key('Virtuagym B.V.', {}), rank.provider_key('Virtuagym', {}))
        self.assertEqual(rank.provider_key('BLATT sp. z o.o.', {}), 'blatt')
        self.assertEqual(rank.provider_key('Relaxio s.r.o.', {'relaxio': 'habitics'}), rank.provider_key('Habitics', {}))
        self.assertEqual(rank.provider_key('MEETYOU PTE.LTD.', {}), 'meetyou')

    def test_calibration_uses_median_ratio_and_os_shares(self):
        cands = [{'play': 1, 'apple': 1, 'r': 10, 'v': 20}, {'play': 1, 'apple': 1, 'r': 10, 'v': 40},
                 {'play': 1, 'apple': 1, 'r': 10, 'v': 60}, {'play': 1, 'apple': None, 'r': 0, 'v': 99}]
        c, n = rank.calibration(cands, 0.25, 0.75)
        self.assertEqual(n, 3)
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

    def test_excluded_listing_in_either_store_excludes_the_candidate(self):
        c = {'play': {'store': 'play', 'id': 'p'}, 'apple': {'store': 'apple', 'id': 'a'}}
        screening = {('play', 'p'): {'decision': 'eligible'}, ('apple', 'a'): {'decision': 'excluded', 'criterion': 'E3'}}
        self.assertEqual(rank.decision(c, screening)['decision'], 'excluded')

    def test_domain_keeps_the_registered_domain(self):
        self.assertEqual(rank.domain('https://www.helloclue.com/privacy.html'), 'helloclue.com')
        self.assertEqual(rank.domain('http://shop.example.co.uk/x'), 'example.co.uk')

    def test_one_account_under_two_developer_keys_is_reported(self):
        listings = {'apple': {'1': {'account': '9', 'developer_key': 'leap health'}, '2': {'account': '9', 'developer_key': 'leap'}},
                    'play': {'p': {'account': '9', 'developer_key': 'other'}}}
        self.assertEqual(rank.account_conflicts(listings), {('apple', '9'): ['leap', 'leap health']})

    def test_listings_of_a_selection(self):
        sel = [{'play': {'store': 'play', 'id': 'p'}, 'apple': {'store': 'apple', 'id': 'a'}},
               {'play': None, 'apple': {'store': 'apple', 'id': 'b'}}]
        self.assertEqual(rank.listings_of(sel), {('play', 'p'), ('apple', 'a'), ('apple', 'b')})

    def test_spearman_and_tex(self):
        self.assertAlmostEqual(rank.spearman([1, 2, 3], [3, 2, 1]), -1.0)
        self.assertEqual(rank.tex('A & B™ 100%'), r'A \& B 100\%')


if __name__ == '__main__':
    unittest.main()
