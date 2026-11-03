"""Google Play keyword search for sampling. Usage: python scraper.py input.json > output/run.json

Reads the first search page per keyword, then opens the product page of every app found
within `depth`, appending each to `cache` so that an interrupted run resumes. TLS checks
are restored, and every request must keep the storefront.
"""
import hashlib, importlib, json, re, ssl, sys, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from google_play_scraper import app
from google_play_scraper.constants.element import ElementSpecs as Specs
from google_play_scraper.constants.regex import Regex
from google_play_scraper.utils import nested_lookup

ssl._create_default_https_context = ssl.create_default_context  # library disables TLS checks
for spec in (*Specs.Detail.values(), *Specs.SearchResult.values(), *Specs.SearchResultOnTop.values()):
    spec.fallback_value = None  # a failed parse stays missing instead of becoming 0 or ""
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
requests = {}
now = lambda: datetime.now(timezone.utc).isoformat()

def fetch(url, gl):
    if f"gl={gl}" not in url: raise ValueError("country parameter removed: " + url)
    time.sleep(1)
    with urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30) as response:
        body = response.read()
    if f"gl={gl}" not in response.url: raise ValueError("left the storefront: " + response.url)
    requests[url] = {"sha256": hashlib.sha256(body).hexdigest(), "captured_at": now()}
    return body.decode("utf-8")

def at(value, path):
    try: return nested_lookup(value, path)
    except (IndexError, KeyError, TypeError): return None

def search(keyword, gl, hl):  # one search response, in page order (not verified as store rank)
    page = fetch("https://play.google.com/store/search?"
                 + urlencode(dict(q=keyword, c="apps", hl=hl, gl=gl)), gl)
    data = {Regex.KEY.findall(b)[0]: json.loads(Regex.VALUE.findall(b)[0])
            for b in Regex.SCRIPT.findall(page) if Regex.KEY.findall(b) and Regex.VALUE.findall(b)}
    hits = []
    for section in data["ds:4"][0][1]:
        if top := at(section, [23, 16]):  # highlighted top result; ID read from its details URL
            hit = {k: s.extract_content(top) for k, s in Specs.SearchResultOnTop.items()}
            url = re.search(r"details\?id=([\w.]+)", json.dumps(top))
            hits.append(dict(hit, appId=hit.get("appId") or (url and url.group(1))))
        if regular := at(section, [22, 0]):
            hits += [{k: s.extract_content(r) for k, s in Specs.SearchResult.items()} for r in regular]
            break
    return [{"Search Position": n, "ID": h.get("appId"), "App Name": h.get("title"),
             "Dev. Name": h.get("developer"), "Downloads": h.get("installs"),
             "Average Rating": h.get("score")} for n, h in enumerate(hits, 1)]

def main(cfg):
    gl, hl, depth, started = cfg["region"], cfg["language"], cfg.get("depth", 30), now()
    importlib.import_module("google_play_scraper.features.app").get = lambda u: fetch(u, gl)
    hits = {k: search(k, gl, hl) for k in cfg["keywords"]}
    ids = sorted({h["ID"] for v in hits.values() for h in v if h["ID"] and h["Search Position"] <= depth})
    path, cache = Path(cfg["cache"]), {}
    if path.exists():  # split("\n"), not splitlines(): listing texts contain U+2028
        cache = {e["id"]: e for e in map(json.loads, filter(None, path.read_text("utf-8").split("\n")))}
    with open(path, "a", encoding="utf-8") as sink:
        for i in (i for i in ids if i not in cache):
            try:
                a = app(i, lang=hl, country=gl)
                cache[i] = {"id": i, "row": {k: a[f] for k, f in FIELDS.items() if a.get(f) is not None}}
            except Exception as error:
                cache[i] = {"id": i, "error": str(error)}
            cache[i]["captured_at"] = now()
            sink.write(json.dumps(cache[i], ensure_ascii=False) + "\n"); sink.flush()
    results = {k: [dict(cache[h["ID"]]["row"], **{"Search Position": h["Search Position"]})
                   for h in v if h["ID"] in ids and "row" in cache[h["ID"]]] for k, v in hits.items()}
    return {"region": gl, "language": hl, "timestamp": started, "finished": now(), "depth": depth,
            "distinct_apps": len(ids), "search": hits, "results": results, "requests": requests,
            "errors": {i: cache[i]["error"] for i in ids if "error" in cache[i]}}

if __name__ == "__main__":
    json.dump(main(json.load(open(sys.argv[1], encoding="utf-8"))), sys.stdout, indent=1, ensure_ascii=False)
