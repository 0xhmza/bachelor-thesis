"""Google Play keyword search for sampling. Usage: python scraper.py input.json > output/run.json

1. Reads the first search page per keyword and records every hit with its position,
   title, developer and the install band the page shows. The app ID of a highlighted
   top result is read from its details URL, which the parser's own field misses.
2. Ranks the distinct apps found within `depth` (default 30) by install band (ties:
   best position, then package ID) and opens the product pages of the first `pages` apps.
   With `search_from`, the search hits of an earlier output are reused instead of searching. Each page is appended to the
   `cache` file as it arrives, so an interrupted run resumes, and progress goes to
   stderr. TLS verification is restored and every request must keep the storefront.
"""
import hashlib, importlib, json, re, ssl, sys, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from google_play_scraper import app
from google_play_scraper.constants.element import ElementSpecs
from google_play_scraper.constants.regex import Regex
from google_play_scraper.utils import nested_lookup

ssl._create_default_https_context = ssl.create_default_context  # library disables TLS checks
cfg = json.load(open(sys.argv[1], encoding="utf-8"))  # keywords, region, language, depth, pages, cache, search_from
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

def details_id(node):
    """First package ID in a details URL anywhere inside a search card."""
    if isinstance(node, str):
        m = re.search(r"details\?id=([\w.]+)", node)
        return m and m.group(1)
    for child in node if isinstance(node, list) else []:
        found = details_id(child)
        if found: return found
    return None

def search(keyword):  # one search response; order is page order, not native store rank
    page = fetch("https://play.google.com/store/search?" + urlencode(dict(q=keyword, c="apps", hl=hl, gl=gl)))
    datasets = {}
    for block in Regex.SCRIPT.findall(page):
        key, value = Regex.KEY.findall(block), Regex.VALUE.findall(block)
        if key and value: datasets[key[0]] = json.loads(value[0])
    hits = []
    for section in datasets["ds:4"][0][1]:
        top, regular = at(section, [23, 16]), at(section, [22, 0])
        if top:
            hit = {k: s.extract_content(top) for k, s in ElementSpecs.SearchResultOnTop.items()}
            hits.append(dict(hit, appId=hit.get("appId") or details_id(top)))
        if regular:
            hits.extend({k: s.extract_content(row) for k, s in ElementSpecs.SearchResult.items()}
                        for row in regular)
            break
    return [{"Search Position": n, "ID": h.get("appId"), "App Name": h.get("title"),
             "Dev. Name": h.get("developer"), "Downloads": h.get("installs"), "Average Rating": h.get("score")}
            for n, h in enumerate(hits, 1)]

def band(text):  # "10.000.000+" -> 10000000
    digits = re.sub(r"\D", "", text or "")
    return int(digits) if digits else 0

fields = {"App Name": "title", "ID": "appId", "Genre": "genre", "Genre ID": "genreId",
          "Dev. Name": "developer", "Dev. ID": "developerId", "Released": "released",
          "Updated": "lastUpdatedOn", "Updated Timestamp": "updated", "Version": "version",
          "Downloads": "installs", "Minimum Installs": "minInstalls",
          "Embedded Install Count": "realInstalls", "Average Rating": "score",
          "Rating Count": "ratings", "Review Count": "reviews", "Rating Histogram": "histogram",
          "Price": "price", "Currency": "currency", "Free to Download": "free",
          "Offers IAP": "offersIAP", "IAP Price Range": "inAppProductPrice",
          "Contains Ads": "containsAds", "Content Rating": "contentRating",
          "Summary": "summary", "Description": "description",
          "Privacy Policy URL": "privacyPolicy", "Developer Website": "developerWebsite",
          "App URL": "url"}
started = datetime.now(timezone.utc).isoformat()
depth = cfg.get("depth", 30)
if cfg.get("search_from"):
    previous = json.load(open(cfg["search_from"], encoding="utf-8"))
    search_hits, started = previous["search"], previous["timestamp"]
    assert list(search_hits) == cfg["keywords"], "keywords differ from the reused search"
else:
    search_hits = {}
    for i, keyword in enumerate(cfg["keywords"], 1):
        search_hits[keyword] = search(keyword)
        print(f"search {i}/{len(cfg['keywords'])} {keyword}: {len(search_hits[keyword])} hits", file=sys.stderr, flush=True)

best = {}
for keyword, hits in search_hits.items():
    for h in hits:
        if h["ID"] and h["Search Position"] <= depth:
            b = best.setdefault(h["ID"], {"band": band(h["Downloads"]), "position": h["Search Position"]})
            b["position"] = min(b["position"], h["Search Position"])
order = sorted(best, key=lambda i: (-best[i]["band"], best[i]["position"], i))
chosen = order[:cfg["pages"]]
cutoff = best[chosen[-1]]["band"] if chosen else 0

cache_path = Path(cfg["cache"])
cache = {}
if cache_path.exists():
    for line in cache_path.read_text(encoding="utf-8").split("\n"):  # not splitlines(): texts hold U+2028
        if not line: continue
        entry = json.loads(line)
        cache[entry["id"]] = entry
with open(cache_path, "a", encoding="utf-8") as sink:
    for n, app_id in enumerate(chosen, 1):
        if app_id not in cache:
            try:
                a = app(app_id, lang=hl, country=gl)
                entry = {"id": app_id, "row": {k: a[f] for k, f in fields.items() if a.get(f) is not None}}
            except Exception as error:
                entry = {"id": app_id, "error": str(error)}
            entry["captured_at"] = datetime.now(timezone.utc).isoformat()
            sink.write(json.dumps(entry, ensure_ascii=False) + "\n")
            sink.flush()
            cache[app_id] = entry
        print(f"page {n}/{len(chosen)} {app_id}", file=sys.stderr, flush=True)

results = {k: [dict(cache[h["ID"]]["row"], **{"Search Position": h["Search Position"]})
               for h in hits if h["ID"] in chosen and "row" in cache[h["ID"]]]
           for k, hits in search_hits.items()}
out = {"region": gl, "language": hl, "timestamp": started, "finished": datetime.now(timezone.utc).isoformat(),
       "search_from": cfg.get("search_from"), "depth": depth, "pages": cfg["pages"], "distinct_apps": len(best), "page_band_cutoff": cutoff,
       "apps_at_cutoff_without_page": sum(1 for i in order[cfg["pages"]:] if best[i]["band"] == cutoff),
       "hits": {k: len(v) for k, v in search_hits.items()},
       "hits_without_id": {k: sum(1 for h in v if not h["ID"]) for k, v in search_hits.items() if any(not h["ID"] for h in v)},
       "search": search_hits, "results": results,
       "errors": {i: cache[i]["error"] for i in chosen if "error" in cache[i]}, "requests": requests}
json.dump(out, sys.stdout, indent=1, ensure_ascii=False)
