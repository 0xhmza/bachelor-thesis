"""App Store keyword search. Usage: python scraper.py input.json > output/run.json"""
import json, sys, time
from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import urlopen

cfg = json.load(open(sys.argv[1], encoding="utf-8"))  # keywords, region, limit
fields = {"App Name": "trackName", "ID": "trackId", "Genre": "primaryGenreName",
          "Dev. Name": "artistName", "Released": "releaseDate", "Updated": "currentVersionReleaseDate",
          "Average Rating": "averageUserRating", "Rating Count": "userRatingCount",
          "Price": "price", "Languages": "languageCodesISO2A", "App URL": "trackViewUrl"}
out = {"region": cfg["region"], "timestamp": datetime.now(timezone.utc).isoformat(), "results": {}}
for i, keyword in enumerate(cfg["keywords"]):
    time.sleep(3.2 * (i > 0))  # stay under the API rate limit
    query = urlencode(dict(term=keyword, country=cfg["region"], media="software",
                           entity="software", limit=cfg["limit"]))
    apps = json.load(urlopen("https://itunes.apple.com/search?" + query, timeout=30))["results"]
    out["results"][keyword] = [
        {**{name: a[key] for name, key in fields.items() if key in a}, "API Position": n}
        for n, a in enumerate(apps, 1)
        if any(d.startswith("iPhone") for d in a.get("supportedDevices", []))]
json.dump(out, sys.stdout, indent=1)
