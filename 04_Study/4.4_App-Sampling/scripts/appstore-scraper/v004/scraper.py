import argparse, html, json, re, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

parser = argparse.ArgumentParser()
parser.add_argument("keywords", nargs="+")
parser.add_argument("-r", "--region", default="de", type=str.lower)
parser.add_argument("--downloads", action="store_true", help="Add Sensor Tower's estimated last-month download ranges")
args = parser.parse_args()
if not re.fullmatch(r"[a-z]{2}", args.region) or any(not k.strip() for k in args.keywords):
    parser.error("Use nonempty keywords and a two-letter region, e.g. de or us.")
stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
data = {"region": args.region, "timestamp": stamp, "results": {}}
fields = {"App Name": "trackName", "ID": "trackId", "Genre": "primaryGenreName",
          "Dev. Name": "artistName", "Released": "releaseDate",
          "Average Rating": "averageUserRating", "Rating Count": "userRatingCount", "Version": "version",
          "Updated": "currentVersionReleaseDate", "Price": "price", "Currency": "currency",
          "Seller": "sellerName", "App URL": "trackViewUrl", "Developer URL": "artistViewUrl"}
try:
    for i, keyword in enumerate(dict.fromkeys(args.keywords)):
        if i: time.sleep(3.2)
        query = urlencode(dict(term=keyword, country=args.region, media="software", entity="software", limit=200, lang="en_us"))
        with urlopen("https://itunes.apple.com/search?" + query, timeout=30) as response:
            data["results"][keyword] = [{name: a[key] for name, key in fields.items() if a.get(key) is not None} for a in json.load(response)["results"] if any(d.startswith("iPhone") for d in a.get("supportedDevices", []))]
    if args.downloads:
        estimates = {}
        for app in (app for apps in data["results"].values() for app in apps):
            if app["ID"] not in estimates:
                time.sleep(4)
                source = f"https://app.sensortower.com/overview/{app['ID']}?country=US"
                try:
                    with urlopen(Request(source, headers={"User-Agent": "Mozilla/5.0"}), timeout=30) as response:
                        page = response.read().decode("utf-8")
                    meta = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', page)
                    match = re.search(r"Last month['’]s estimates were (.+?) downloads", html.unescape(meta[1]) if meta else "")
                    if not match: raise ValueError("No monthly download estimate found")
                    estimates[app["ID"]] = {"Range": match[1], "Period": "Last month", "Source": source, "Retrieved": datetime.now(timezone.utc).isoformat()}
                except (OSError, ValueError) as error:
                    estimates[app["ID"]] = None
                    data.setdefault("estimate_errors", []).append({"ID": app["ID"], "Error": str(error)})
                    if getattr(error, "code", None) == 429:
                        data["estimate_collection_stopped"] = "Provider rate limit (HTTP 429)"
                        break
            if estimates[app["ID"]]: app["Estimated Downloads"] = estimates[app["ID"]]
    keywords = re.sub(r"[^a-z0-9]+", "-", "-".join(args.keywords).lower()).strip("-")[:100] or "keywords"
    output = Path(__file__).with_name("output") / f"appstore-scraper-{args.region}-{keywords}-{stamp}.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(output.resolve())
except (OSError, ValueError) as error:
    parser.exit(1, f"Could not collect apps: {error}\n")
