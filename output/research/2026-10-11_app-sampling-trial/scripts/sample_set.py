"""Build a clearly provisional app-level working set and fail-closed final set.

Review decisions live in config/app_review.json. The working set illustrates the
proposal ranking on this trial frame; it is not an eligible or final sample.
"""
import argparse
import hashlib
import json
from collections import defaultdict
from decimal import Decimal
from pathlib import Path
from process import BASE, load, write_csv, write_json

CHECKS = ['tracking_function', 'free_install', 'interface_DE_EN', 'policy_reachable',
          'not_DiGA', 'not_duplicate', 'German_available', 'store_UI_membership', 'identity_verified']

def rank_apps(listings, screen, review, protocol):
    numerical = {s['listing_id'] for s in screen if s['numeric_status'] == 'passes_numeric'}
    groups = defaultdict(list)
    mapping = review.get('listing_to_app', {})
    decisions = review.get('apps', {})
    for row in listings:
        groups[mapping.get(row['listing_id'], row['listing_id'])].append(row)
    ranked = []
    for key, rows in groups.items():
        eligible_numeric = [r for r in rows if r['listing_id'] in numerical]
        if not eligible_numeric:
            continue
        decision = decisions.get(key, {})
        hints = {r['domain_provisional'] for r in rows}
        domain = decision.get('domain', 'fertility' if 'fertility' in hints else ('fitness' if hints == {'fitness'} else 'unresolved'))
        count = sum(r['rating_count'] for r in eligible_numeric)
        score = sum(Decimal(str(r['rating'])) * r['rating_count'] for r in eligible_numeric) / count
        pending = [c for c in CHECKS if decision.get(c) is not True]
        # Evidence references and complete discovery are mandatory for final eligibility.
        final = not pending and bool(decision.get('evidence')) and review.get('discovery_complete') is True
        ranked.append({'app_id': key, 'name': decision.get('name', rows[0]['name']), 'domain': domain,
                       'platforms': sorted({r['platform'] for r in rows}), 'listing_ids': sorted(r['listing_id'] for r in rows),
                       'ranking_listing_ids': sorted(r['listing_id'] for r in eligible_numeric),
                       'weighted_score': str(score), 'eligible_rating_count': count,
                       'identity_status': decision.get('identity_status', 'unreviewed'),
                       'pending_checks': pending, 'final_eligible': final,
                       'realInstalls': max((r.get('realInstalls') or 0 for r in rows), default=0) or None,
                       'source_urls': [r['url'] for r in rows], 'status': 'provisional_numeric_working_set'})
    return sorted(ranked, key=lambda r: (-Decimal(r['weighted_score']), -r['eligible_rating_count'], r['app_id']))

def select(ranked, targets, final=False):
    chosen = []
    for domain, n in targets.items():
        candidates = [r for r in ranked if r['domain'] == domain and (not final or r['final_eligible'])]
        for i, row in enumerate(candidates[:n], 1):
            chosen.append({**row, 'domain_rank': i, 'status': 'final_eligible' if final else row['status']})
    return chosen

def main(run):
    out = BASE / 'processed' / run.name
    protocol = load(run / 'inputs/protocol.json')
    review_path = BASE / 'config/app_review.json'
    review = load(review_path) if review_path.exists() else {}
    ranked = rank_apps(load(out / 'listings.json'), load(out / 'screening.json'), review, protocol)
    working = select(ranked, protocol['targets'])
    final = select(ranked, protocol['targets'], final=True)
    fields = ['domain', 'domain_rank', 'app_id', 'name', 'platforms', 'weighted_score', 'eligible_rating_count',
              'realInstalls', 'listing_ids', 'ranking_listing_ids', 'identity_status', 'pending_checks', 'final_eligible', 'status', 'source_urls']
    for name, rows in [('trial_working_set', working), ('all_app_rankings', ranked), ('final_sample', final)]:
        write_csv(out / (name + '.csv'), rows, fields)
        write_json(out / (name + '.json'), rows)
    summary = {domain: {'target': target, 'working_set': sum(r['domain'] == domain for r in working),
                        'numeric_candidate_apps': sum(r['domain'] == domain for r in ranked),
                        'final_eligible_selected': sum(r['domain'] == domain for r in final)}
               for domain, target in protocol['targets'].items()}
    write_json(out / 'selection_summary.json', summary)
    write_json(out / 'selection_provenance.json', {'review_sha256': hashlib.sha256(review_path.read_bytes()).hexdigest() if review_path.exists() else None,
                                                'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                                                'note': 'No current decision has the complete evidence required for final eligibility.'})
    print(json.dumps(summary, indent=2))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('run', type=Path)
    main(parser.parse_args().run.resolve())
