"""Google Play keyword search or app-ID lookup. Usage: python scraper.py input.json > output/run.json"""
import hashlib, importlib, json, ssl, sys, time
from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from google_play_scraper import app
from google_play_scraper.constants.element import ElementSpecs
from google_play_scraper.constants.regex import Regex
from google_play_scraper.utils import nested_lookup

ssl._create_default_https_context = ssl.create_default_context  # library disables TLS checks
cfg = json.load(open(sys.argv[1], encoding="utf-8"))  # keywords and/or ids, region, language, limit
gl, hl = cfg["region"], cfg["language"]
for spec in (*ElementSpecs.Detail.values(), *ElementSpecs.SearchResult.values(),
             *ElementSpecs.SearchResultOnTop.values()):
    spec.fallback_value = None  # a failed parse stays missing instead of becoming 0 or ""
requests = {}

def fetch(url):
    if f"gl={gl}" not in url: raise ValueError("country parameter removed: " + url)
    time.sleep(1)
    with urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30) as response:
        body = response.read()
    if f"gl={gl}" not in response.url: raise ValueError("left the storefront: " + response.url)
    requests[url] = {"sha256": hashlib.sha256(body).hexdigest(),
                     "captured_at": datetime.now(timezone.utc).isoformat()}
    return body.decode("utf-8")

importlib.import_module("google_play_scraper.features.app").get = fetch

def at(value, path):
    try: return nested_lookup(value, path)
    except (IndexError, KeyError, TypeError): return None

def search(keyword):  # one search response; order is page order, not native store rank
    url = "https://play.google.com/store/search?"
    page = fetch(url + urlencode(dict(q=keyword, c="apps", hl=hl, gl=gl)))
    datasets = {}
    for block in Regex.SCRIPT.findall(page):
        key, value = Regex.KEY.findall(block), Regex.VALUE.findall(block)
        if key and value: datasets[key[0]] = json.loads(value[0])
    hits = []
    for section in datasets["ds:4"][0][1]:
        top, regular = at(section, [23, 16]), at(section, [22, 0])
        if top:
            hits.append({k: s.extract_content(top) for k, s in ElementSpecs.SearchResultOnTop.items()})
        if regular:
            hits.extend({k: s.extract_content(row) for k, s in ElementSpecs.SearchResult.items()}
                        for row in regular)
            break
    return [hit["appId"] for hit in hits[:cfg.get("limit", 20)]]

fields = {"App Name": "title", "ID": "appId", "Genre": "genre", "Dev. Name": "developer",
          "Released": "released", "Updated": "lastUpdatedOn", "Downloads": "installs",
          "Embedded Install Count": "realInstalls", "Average Rating": "score",
          "Rating Count": "ratings", "Review Count": "reviews", "Price": "price",
          "Free to Download": "free", "Contains Ads": "containsAds",
          "Privacy Policy URL": "privacyPolicy", "App URL": "url"}
queries = {keyword: search(keyword) for keyword in cfg.get("keywords", [])}
if "ids" in cfg: queries["ids"] = cfg["ids"]
out = {"region": gl, "language": hl, "timestamp": datetime.now(timezone.utc).isoformat(),
       "results": {}, "errors": {}, "requests": requests}
cache = {}
for query, ids in queries.items():
    out["results"][query] = []
    for position, app_id in enumerate(ids, 1):
        try:
            if app_id not in cache: cache[app_id] = app(app_id, lang=hl, country=gl)
            a = cache[app_id]
            row = {n: a[k] for n, k in fields.items() if a.get(k) is not None}
            out["results"][query].append({**row, "Search Position": position})
        except Exception as error:
            out["errors"][app_id] = str(error)
json.dump(out, sys.stdout, indent=1)
