import argparse, hashlib, importlib, importlib.metadata, json, re, ssl, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlsplit
from urllib.request import Request, urlopen

tls_factory = ssl._create_default_https_context
from google_play_scraper import app
from google_play_scraper.constants.element import ElementSpecs
from google_play_scraper.constants.regex import Regex
from google_play_scraper.utils import nested_lookup
ssl._create_default_https_context = tls_factory
for specs in (ElementSpecs.Detail, ElementSpecs.SearchResult, ElementSpecs.SearchResultOnTop):
    for spec in specs.values(): spec.fallback_value = None
parser = argparse.ArgumentParser()
parser.add_argument("keywords", nargs="+")
parser.add_argument("-r", "--region", default="de", type=str.lower)
parser.add_argument("-n", "--limit", type=int, default=200)
parser.add_argument("-l", "--language", default="en")
args = parser.parse_args()
if not re.fullmatch(r"[a-z]{2}", args.region) or not 1 <= args.limit <= 200 or any(not k.strip() for k in args.keywords):
    parser.error("Use nonempty keywords, a two-letter region and a limit of 1–200.")
stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
data = {"region": args.region, "timestamp": stamp, "limit": args.limit, "language_requested": args.language,
        "parser": "google-play-scraper " + importlib.metadata.version("google-play-scraper"), "requests": {}, "results": {}}
def fetch(url):
    if parse_qs(urlsplit(url).query).get("gl") != [args.region]: raise ValueError("Country parameter was removed")
    time.sleep(1)
    with urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30, context=ssl.create_default_context()) as response:
        if urlsplit(response.url).hostname != "play.google.com" or parse_qs(urlsplit(response.url).query).get("gl") != [args.region]: raise ValueError("Unexpected country/host redirect")
        body = response.read()
        data["requests"][url] = {"final_url": response.url, "http_status": response.status, "captured_at": datetime.now(timezone.utc).isoformat(), "sha256": hashlib.sha256(body).hexdigest()}
    return body.decode("utf-8")
importlib.import_module("google_play_scraper.features.app").get = fetch
def at(value, path):
    try: return nested_lookup(value, path)
    except (IndexError, KeyError, TypeError): return None
def search(keyword):
    page = fetch("https://play.google.com/store/search?" + urlencode(dict(q=keyword, c="apps", hl=args.language, gl=args.region)))
    datasets = {}
    for block in Regex.SCRIPT.findall(page):
        key, value = Regex.KEY.findall(block), Regex.VALUE.findall(block)
        if key and value: datasets[key[0]] = json.loads(value[0])
    hits = []
    for section in datasets["ds:4"][0][1]:
        top, regular = at(section, [23, 16]), at(section, [22, 0])
        if top: hits.append({key: spec.extract_content(top) for key, spec in ElementSpecs.SearchResultOnTop.items()})
        if regular:
            hits.extend({key: spec.extract_content(row) for key, spec in ElementSpecs.SearchResult.items()} for row in regular)
            break
    return hits[:args.limit]
fields = {"App Name": "title", "ID": "appId", "Genre": "genre", "Genres": "categories", "Dev. Name": "developer",
          "Developer ID": "developerId", "Released": "released", "Version": "version", "Updated": "lastUpdatedOn",
          "Downloads": "installs", "Minimum Installs": "minInstalls", "Embedded Install Count": "realInstalls",
          "Average Rating": "score", "Rating Count": "ratings", "Review Count": "reviews", "Rating Distribution (1–5)": "histogram",
          "Price": "price", "Currency": "currency", "Free to Download": "free", "In-App Purchases": "offersIAP",
          "In-App Purchase Prices": "inAppProductPrice", "Contains Ads": "containsAds", "Age Rating": "contentRating",
          "Content Advisories": "contentRatingDescription", "Summary": "summary", "Description": "description",
          "Screenshots": "screenshots", "Icon URL": "icon", "Video URL": "video", "Featured Reviews": "comments",
          "App URL": "url", "Developer Website": "developerWebsite", "Privacy Policy URL": "privacyPolicy"}
cache = {}
try:
    for keyword in dict.fromkeys(k.strip() for k in args.keywords):
        hits = search(keyword)
        data["results"][keyword] = []
        for position, hit in enumerate(hits, 1):
            app_id = hit["appId"]
            if app_id not in cache:
                try:
                    cache[app_id] = app(app_id, lang=args.language, country=args.region)
                    if not cache[app_id].get("title"): raise ValueError("App details could not be parsed")
                except Exception as error:
                    cache[app_id] = hit
                    data.setdefault("detail_errors", []).append({"ID": app_id, "Error": str(error)})
            a = cache[app_id]
            data["results"][keyword].append({**{name: a[key] for name, key in fields.items() if a.get(key) is not None}, "Search Position": position})
    keywords = re.sub(r"[^a-z0-9]+", "-", "-".join(data["results"]).lower()).strip("-")[:100] or "keywords"
    output = Path(__file__).with_name("output") / f"googleplay-scraper-{args.region}-{keywords}-{stamp}.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(output.resolve())
except Exception as error:
    parser.exit(1, f"Could not collect apps: {error}\n")
