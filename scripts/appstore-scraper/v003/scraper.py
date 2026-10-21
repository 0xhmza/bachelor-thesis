import argparse, json, re, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

parser = argparse.ArgumentParser()
parser.add_argument("keywords", nargs="+")
parser.add_argument("-r", "--region", default="de", type=str.lower)
args = parser.parse_args()
if not re.fullmatch(r"[a-z]{2}", args.region) or any(not k.strip() for k in args.keywords):
    parser.error("Use nonempty keywords and a two-letter region, e.g. de or us.")
stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
data = {"region": args.region, "timestamp": stamp, "results": {}}
fields = {"App Name": "trackName", "ID": "trackId", "Genre": "primaryGenreName",
          "Dev. Name": "artistName", "Dev. Type": None, "Released": "releaseDate",
          "Downloads": None, "Ratings": "averageUserRating", "Rating Count": "userRatingCount",
          "Reviews": None, "Reviews (2023)": None, "Version": "version",
          "Updated": "currentVersionReleaseDate", "Price": "price", "Currency": "currency",
          "Seller": "sellerName", "App URL": "trackViewUrl", "Developer URL": "artistViewUrl"}
try:
    for i, keyword in enumerate(dict.fromkeys(args.keywords)):
        if i: time.sleep(3.2)
        query = urlencode(dict(term=keyword, country=args.region, media="software", entity="software", limit=200, lang="en_us"))
        with urlopen("https://itunes.apple.com/search?" + query, timeout=30) as response:
            data["results"][keyword] = [{name: a.get(key) for name, key in fields.items()} for a in json.load(response)["results"] if any(d.startswith("iPhone") for d in a.get("supportedDevices", []))]
    keywords = re.sub(r"[^a-z0-9]+", "-", "-".join(args.keywords).lower()).strip("-")[:100] or "keywords"
    output = Path(__file__).with_name("output") / f"appstore-scraper-{args.region}-{keywords}-{stamp}.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(output.resolve())
except (OSError, ValueError) as error:
    parser.exit(1, f"Could not collect apps: {error}\n")
