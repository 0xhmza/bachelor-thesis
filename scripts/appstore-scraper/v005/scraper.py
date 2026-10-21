import argparse, json, re, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

parser = argparse.ArgumentParser()
parser.add_argument("keywords", nargs="+")
parser.add_argument("-r", "--region", default="de", type=str.lower)
parser.add_argument("-n", "--limit", type=int, default=200)
args = parser.parse_args()
if not re.fullmatch(r"[a-z]{2}", args.region) or not 1 <= args.limit <= 200 or any(not k.strip() for k in args.keywords):
    parser.error("Use nonempty keywords, a two-letter region and a limit of 1–200.")
stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
data = {"region": args.region, "timestamp": stamp, "limit": args.limit, "language_requested": "en_us", "requests": {}, "results": {}}
fields = {"App Name": "trackName", "ID": "trackId", "Genre": "primaryGenreName", "Genres": "genres",
          "Dev. Name": "artistName", "Seller": "sellerName", "Released": "releaseDate", "Version": "version",
          "Updated": "currentVersionReleaseDate", "Average Rating": "averageUserRating", "Rating Count": "userRatingCount",
          "Current Version Average Rating": "averageUserRatingForCurrentVersion", "Current Version Rating Count": "userRatingCountForCurrentVersion",
          "Price": "price", "Formatted Price": "formattedPrice", "Currency": "currency", "Languages": "languageCodesISO2A",
          "Age Rating": "contentAdvisoryRating", "Content Advisories": "advisories", "Description": "description",
          "Release Notes": "releaseNotes", "Minimum iOS": "minimumOsVersion", "Features": "features",
          "Screenshots": "screenshotUrls", "Icon URL": "artworkUrl512", "App URL": "trackViewUrl",
          "Developer URL": "artistViewUrl", "Developer Website": "sellerUrl"}
try:
    for i, keyword in enumerate(dict.fromkeys(k.strip() for k in args.keywords)):
        if i: time.sleep(3.2)
        url = "https://itunes.apple.com/search?" + urlencode(dict(term=keyword, country=args.region, media="software", entity="software", limit=args.limit, lang="en_us", explicit="Yes"))
        with urlopen(url, timeout=30) as response: payload = json.load(response)
        data["requests"][keyword] = {"url": url, "captured_at": datetime.now(timezone.utc).isoformat(), "returned_count": len(payload["results"])}
        data["results"][keyword] = [{**{name: a[key] for name, key in fields.items() if a.get(key) is not None}, "API Position": position} for position, a in enumerate(payload["results"], 1) if any(d.startswith("iPhone") for d in a.get("supportedDevices", []))]
    keywords = re.sub(r"[^a-z0-9]+", "-", "-".join(data["results"]).lower()).strip("-")[:100] or "keywords"
    output = Path(__file__).with_name("output") / f"appstore-scraper-{args.region}-{keywords}-{stamp}.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(output.resolve())
except (OSError, ValueError) as error:
    parser.exit(1, f"Could not collect apps: {error}\n")
