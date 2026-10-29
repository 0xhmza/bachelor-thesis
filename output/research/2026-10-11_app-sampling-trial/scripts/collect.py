"""Bounded public-metadata trial. Python 3.11+, standard library only.

No login, browser fingerprint tricks, country fallback, review RPC or store-search
scraping. Raw bytes and request failures are append-only and hashed.
"""
import argparse
import hashlib
import json
import shutil
import ssl
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser

BASE = Path(__file__).resolve().parents[1]
UA = 'BachelorThesisSamplingTrial/1.0'

def utc():
    return datetime.now(timezone.utc).isoformat()

def save(path, obj):
    with path.open('x', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

class Collector:
    def __init__(self, run, protocol):
        self.run, self.protocol = run, protocol
        self.last_request = 0
        self.stopped_hosts = set()
        self.robots = {}

    def fetch(self, url, name):
        host = urlsplit(url).netloc
        meta = {'requested_url': url, 'started_utc': utc(), 'user_agent': UA,
                'request_headers': {'Accept-Language': 'de-DE,de;q=0.9,en;q=0.7'},
                'status': None, 'error': None, 'tls_verified': urlsplit(url).scheme == 'https'}
        body = b''
        if host in self.stopped_hosts:
            meta['error'] = 'host_stopped_after_403_or_429'
        else:
            time.sleep(max(0, self.protocol['delay_seconds'] - (time.monotonic() - self.last_request)))
            self.last_request = time.monotonic()
            try:
                req = Request(url, headers={'User-Agent': UA, **meta['request_headers']})
                with urlopen(req, timeout=self.protocol['timeout_seconds'], context=ssl.create_default_context()) as r:
                    body = r.read()
                    meta.update(status=r.status, final_url=r.url,
                                content_type=r.headers.get('Content-Type'),
                                date_header=r.headers.get('Date'), etag=r.headers.get('ETag'),
                                last_modified=r.headers.get('Last-Modified'))
            except HTTPError as e:
                body = e.read()
                meta.update(status=e.code, final_url=e.url, error=f'HTTP {e.code}')
                if e.code in (403, 429):
                    self.stopped_hosts.add(host)
            except Exception as e:
                meta['error'] = f'{type(e).__name__}: {e}'
        meta.update(completed_utc=utc(), bytes=len(body), sha256=hashlib.sha256(body).hexdigest(), file=name)
        with (self.run / name).open('xb') as f:
            f.write(body)
        save(self.run / (name + '.meta.json'), meta)
        print(json.dumps({'file': name, 'status': meta['status'], 'bytes': len(body), 'error': meta['error']}), flush=True)
        return body, meta

    def robot_allows(self, url):
        p = urlsplit(url)
        origin = f'{p.scheme}://{p.netloc}'
        if origin not in self.robots:
            name = 'robots_' + hashlib.sha256(origin.encode()).hexdigest()[:12] + '.txt'
            body, meta = self.fetch(origin + '/robots.txt', name)
            if meta['status'] == 404:
                self.robots[origin] = True
            elif meta['status'] == 200:
                parser = RobotFileParser()
                parser.parse(body.decode('utf-8', errors='replace').splitlines())
                self.robots[origin] = parser
            else:
                self.robots[origin] = False
        rule = self.robots[origin]
        return rule if isinstance(rule, bool) else rule.can_fetch(UA, url)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apple-limit', type=int, default=19, help='Number of frozen queries to run, not results per query')
    parser.add_argument('--play-limit', type=int, default=24)
    args = parser.parse_args()
    protocol = json.loads((BASE / 'config/protocol.json').read_text(encoding='utf-8'))
    seeds = json.loads((BASE / 'config/play_seeds.json').read_text(encoding='utf-8'))
    run = BASE / 'raw' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    run.mkdir(parents=True)
    (run / 'inputs').mkdir()
    provenance = []
    for path in sorted([*BASE.glob('config/*'), *BASE.glob('scripts/*.py')]):
        shutil.copyfile(path, run / 'inputs' / path.name)
        provenance.append({'path': str(path.relative_to(BASE)), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    save(run / 'run.json', {'started_utc': utc(), 'protocol': protocol, 'inputs': provenance,
                           'python': __import__('sys').version, 'limits': vars(args),
                           'network_context': 'host network; no account; no cookie persistence; IP geolocation not verified'})
    c = Collector(run, protocol)
    c.fetch('https://performance-partners.apple.com/search-api', 'terms_apple_api.html')
    c.fetch('https://policies.google.com/terms?hl=en&gl=de', 'terms_google.html')
    c.fetch('https://play.google.com/intl/de_de/about/play-terms/index.html', 'terms_play.html')
    searches, requests = [], []
    for kw in protocol['keywords'][:args.apple_limit]:
        url = 'https://itunes.apple.com/search?' + urlencode({'term': kw['term'], 'country': 'de',
             'media': 'software', 'entity': 'software', 'limit': 20, 'lang': 'en_us'})
        _, meta = c.fetch(url, f"apple_{kw['id']}.json")
        searches.append({**kw, 'platform': 'apple', 'method': 'official_search_api_trial', **meta})
    for seed in seeds[:args.play_limit]:
        url = 'https://play.google.com/store/apps/details?' + urlencode({'id': seed['app_id'], 'hl': 'de', 'gl': 'de'})
        allowed = c.robot_allows(url)
        if allowed:
            _, meta = c.fetch(url, 'play_' + seed['app_id'] + '.html')
            requests.append({**seed, **meta, 'robots_allowed': True})
        else:
            requests.append({**seed, 'requested_url': url, 'robots_allowed': False,
                             'status': None, 'error': 'robots_denied_or_unavailable'})
    save(run / 'searches.json', searches)
    save(run / 'play_requests.json', requests)
    save(run / 'completion.json', {'completed_utc': utc(), 'apple_queries_attempted': len(searches),
                                 'play_listings_planned': len(requests), 'stopped_hosts': sorted(c.stopped_hosts)})
    print('RUN=' + str(run), flush=True)

if __name__ == '__main__':
    main()
