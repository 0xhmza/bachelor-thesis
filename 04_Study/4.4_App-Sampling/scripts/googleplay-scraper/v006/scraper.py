"""Usage: python scraper.py input.json > output/run.json"""
import hashlib, json, re, ssl, sys, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlsplit
from urllib.request import Request, urlopen
from google_play_scraper.constants.element import ElementSpecs as Specs
from google_play_scraper.constants.regex import Regex
from google_play_scraper.features.app import parse_dom
ssl._create_default_https_context = ssl.create_default_context  # undo the library's TLS override
BASE = "https://play.google.com/store/"
FIELDS = {"App Name": "title", "ID": "appId", "Genre": "genre", "Genre ID": "genreId",
    "Dev. Name": "developer", "Dev. ID": "developerId", "Released": "released",
    "Updated": "lastUpdatedOn", "Updated Timestamp": "updated", "Version": "version",
    "Downloads": "installs", "Minimum Installs": "minInstalls", "Embedded Install Count": "realInstalls",
    "Average Rating": "score", "Rating Count": "ratings", "Review Count": "reviews",
    "Rating Histogram": "histogram", "Price": "price", "Currency": "currency",
    "Free to Download": "free", "Offers IAP": "offersIAP", "IAP Price Range": "inAppProductPrice",
    "Contains Ads": "containsAds", "Content Rating": "contentRating", "Summary": "summary",
    "Description": "description", "Privacy Policy URL": "privacyPolicy",
    "Developer Website": "developerWebsite", "App URL": "url"}
SEARCH_FIELDS = ("ID", "App Name", "Dev. Name", "Downloads", "Average Rating")

def now(): return datetime.now(timezone.utc).isoformat()

def at(section, outer, inner):
    try: return section[outer][inner]
    except (IndexError, KeyError, TypeError): return None

def search(page):
    data = next(Regex.VALUE.search(block)[1] for block in Regex.SCRIPT.findall(page)
                if (key := Regex.KEY.search(block)) and key[1] == "ds:4")
    hits = []
    for section in json.loads(data)[0][1]:
        if top := at(section, 23, 16):
            hit = {key: spec.extract_content(top) for key, spec in Specs.SearchResultOnTop.items()}
            match = re.search(r"details\?id=([\w.]+)", json.dumps(top))
            hit["appId"] = hit.get("appId") or (match and match[1])
            hits.append(hit)
        if regular := at(section, 22, 0):
            hits.extend({key: spec.extract_content(row) for key, spec in Specs.SearchResult.items()}
                        for row in regular)
            break
    return [{**{key: hit.get(FIELDS[key]) for key in SEARCH_FIELDS}, "Search Position": pos}
            for pos, hit in enumerate(hits, 1)]

def collect(cfg):
    region, language, depth = cfg["region"], cfg["language"], cfg.get("depth", 30)
    started, requests = now(), {}
    for spec in Specs.Detail.values(): spec.fallback_value = None

    def fetch(route, **params):
        url = BASE + route + "?" + urlencode(dict(params, hl=language, gl=region))
        time.sleep(1)
        with urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30) as response:
            if parse_qs(urlsplit(response.url).query).get("gl") != [region]:
                raise ValueError("left the storefront: " + response.url)
            body = response.read()
        requests[url] = dict(sha256=hashlib.sha256(body).hexdigest(), captured_at=now())
        return body.decode("utf-8"), url

    hits = {k: search(fetch("search", q=k, c="apps")[0]) for k in cfg["keywords"]}
    ids = {h["ID"] for rows in hits.values() for h in rows[:depth] if h["ID"]}
    path = Path(cfg["cache"])
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+", encoding="utf-8") as sink:
        sink.seek(0)
        cache = {entry["id"]: entry for entry in map(json.loads, filter(str.strip, sink))}
        for app_id in sorted(ids - cache.keys()):
            try:
                page, url = fetch("apps/details", id=app_id)
                app = parse_dom(page, app_id, url)
                entry = dict(row={key: app[field] for key, field in FIELDS.items() if app.get(field) is not None})
            except Exception as error:
                entry = dict(error=str(error))
            cache[app_id] = dict(id=app_id, captured_at=now(), **entry)
            print(json.dumps(cache[app_id], ensure_ascii=False), file=sink, flush=True)
    rows = {i: cache[i]["row"] for i in ids if "row" in cache[i]}
    results = {k: [dict(rows[h["ID"]], **{"Search Position": h["Search Position"]})
                   for h in group if h["ID"] in rows] for k, group in hits.items()}
    return dict(region=region, language=language, timestamp=started, finished=now(), depth=depth,
                distinct_apps=len(ids), search=hits, results=results, requests=requests,
                errors={i: cache[i]["error"] for i in sorted(ids) if "error" in cache[i]})

if __name__ == "__main__":
    with Path(sys.argv[1]).open(encoding="utf-8") as source:
        json.dump(collect(json.load(source)), sys.stdout, indent=1, ensure_ascii=False)
