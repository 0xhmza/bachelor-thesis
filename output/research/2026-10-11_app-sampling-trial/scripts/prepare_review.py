"""Create transparent, provisional identity suggestions and domain review notes."""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from process import BASE, load, write_csv
from sample_set import CHECKS

def main(run):
    rows = load(BASE / 'processed' / run.name / 'listings.json')
    by_id = {r['listing_id']: r for r in rows}
    groups = [
        ('stepsapp', 'StepsApp', 'fitness', '1037595083', 'com.stepsappgmbh.stepsapp'),
        ('ito-pedometer', 'Pedometer by ITO Technologies', 'fitness', '1027151285', 'com.tayu.tau.pedometer'),
        ('flo', 'Flo', 'fertility', '1038369065', 'org.iggymedia.periodtracker'),
        ('clue', 'Clue', 'fertility', '657189652', 'com.clue.android'),
        ('clover', 'Clover', 'fertility', '1423628793', 'com.wachanga.womancalendar'),
        ('gp-period-tracker', 'Period Tracker by GP Apps', 'fertility', '330376830', 'com.period.tracker.lite'),
        ('simple-my-calendar', 'My Calendar by SimpleInnovation', 'fertility', '1032267351', 'com.lbrc.PeriodCalendar')]
    review = {'created_utc': datetime.now(timezone.utc).isoformat(), 'reviewer': 'Codex assisted preliminary review',
              'discovery_complete': False, 'listing_to_app': {}, 'apps': {},
              'note': 'Identity suggestions use brands, developer names and provider URLs. Apple policy equivalence and exact product identity remain unverified.'}
    for slug, name, domain, apple, play in groups:
        ids = ['apple:' + apple, 'play:' + play]
        if not all(i in by_id for i in ids):
            continue
        key = 'app:' + slug
        for i in ids:
            review['listing_to_app'][i] = key
        review['apps'][key] = {'name': name, 'domain': domain, 'identity_status': 'provisional_cross_store_match',
                              'identity_verified': False, 'evidence': [by_id[i]['raw_file'] for i in ids],
                              'reason': 'Matching product brand, related developer names and provider web domains; policy equivalence not checked.'}
    notes = {
        'apple:1230124761': ('fertility', 'Listing describes ovulation, fertile phase, period and temperature tracking.', True),
        'apple:1043837948': ('fitness', 'Listing leads with sleep/activity/readiness. Cycle insights create overlap; main-function judgement needs confirmation.', True),
        'apple:1438388363': ('fitness', 'Listing explicitly describes Apple Health water, steps, sleep, exercise and calorie tracking.', True),
        'apple:1491340863': ('unresolved', 'Infant sleep and feeding tracking; allocation to this fitness/fertility study needs a scope decision.', True),
        'apple:6450744756': ('unresolved', 'Infant sleep/feeding/growth tracking; domain boundary needs review.', True),
        'apple:1275040830': ('fertility', 'Listing explicitly describes period, ovulation, temperature and cervical mucus tracking alongside pregnancy.', True),
        'apple:1064911742': ('fertility', 'Same provider and similar core function as My Calendar; duplicate-product decision requires policy/product review.', True),
        'apple:808395252': ('out_of_scope', 'EV charging app; search/name match is irrelevant to health or body tracking.', False)}
    for key, (domain, reason, tracking) in notes.items():
        if key in by_id:
            review['apps'][key] = {'domain': domain, 'tracking_function': tracking, 'reason': reason,
                                   'identity_status': 'unreviewed', 'evidence': [by_id[key]['raw_file']]}
    path = BASE / 'config/app_review.json'
    with path.open('x', encoding='utf-8') as f:
        json.dump(review, f, ensure_ascii=False, indent=2)
    template = []
    for r in rows:
        template.append({'listing_id': r['listing_id'], 'name': r['name'],
                         'suggested_app_id': review['listing_to_app'].get(r['listing_id'], r['listing_id']),
                         **{c: 'pending' for c in CHECKS}, 'reviewer': '', 'reviewed_utc': '', 'evidence_file': '', 'decision_reason': ''})
    write_csv(BASE / 'processed' / run.name / 'manual_review_register.csv', template,
              ['listing_id', 'name', 'suggested_app_id'] + CHECKS + ['reviewer', 'reviewed_utc', 'evidence_file', 'decision_reason'])
    # 38 prescribed store UI sessions are unperformed; API results are not pasted into these positions.
    protocol = load(run / 'inputs/protocol.json')
    sessions = [{'platform': store, 'keyword_id': kw['id'], 'keyword': kw['term'], 'target_organic_results': 20,
                 'status': 'not_captured', 'storefront': 'de', 'account_state': '', 'device': '',
                 'captured_utc': '', 'evidence_file': ''}
                for store in ['play', 'apple'] for kw in protocol['keywords']]
    write_csv(BASE / 'processed' / run.name / 'required_store_UI_sessions.csv', sessions, list(sessions[0]))
    print('Created 7 provisional cross-store matches, domain notes and review registers.')

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('run', type=Path)
    main(p.parse_args().run.resolve())
