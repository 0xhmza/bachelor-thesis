"""Reachability spot check for Play policy links; HTTP 200 is not policy verification."""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from collect import BASE, Collector, save
from process import load, write_csv

def main(run):
    rows = load(BASE / 'processed' / run.name / 'listings.json')
    protocol = load(run / 'inputs/protocol.json')
    dest = run / ('policy_check_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    dest.mkdir()
    c = Collector(dest, protocol)
    results = []
    for r in rows:
        if r['platform'] != 'play' or not r.get('privacy_policy_url'):
            continue
        url = r['privacy_policy_url']
        result = {'listing_id': r['listing_id'], 'url': url, 'policy_content_verified': False}
        if c.robot_allows(url):
            body, meta = c.fetch(url, 'policy_' + r['store_id'] + '.html')
            result.update(status=meta['status'], error=meta['error'], raw_file=str((dest / meta['file']).relative_to(run)),
                          sha256=meta['sha256'], final_url=meta.get('final_url'), captured_utc=meta['started_utc'])
            result['reachability'] = 'HTTP_200_content_unverified' if meta['status'] == 200 else 'retrieval_failed_not_exclusion'
        else:
            result.update(status=None, reachability='robots_denied_or_unavailable', error='Not requested')
        results.append(result)
    save(dest / 'results.json', results)
    out = BASE / 'processed' / run.name
    write_csv(out / 'policy_reachability.csv', results, ['listing_id', 'url', 'status', 'reachability', 'error', 'final_url', 'captured_utc', 'raw_file', 'sha256', 'policy_content_verified'])
    (out / 'policy_check_reference.json').write_text(json.dumps({'results': str((dest / 'results.json').relative_to(BASE))}), encoding='utf-8')
    print('POLICY_RESULTS=' + str(dest / 'results.json'))

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('run', type=Path)
    main(p.parse_args().run.resolve())
