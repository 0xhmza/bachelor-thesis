"""App Store keyword search for sampling. Usage: python scraper.py input.json > output/run.json

Calls Apple's iTunes Search API once per keyword for one storefront and keeps the
iPhone-compatible results in API order. "API Position" is the position before the
iPhone filter. Each request is logged with its URL, time, result count and SHA-256.
"""
import hashlib, json, sys, time
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

cfg = json.load(open(sys.argv[1], encoding="utf-8"))  # keywords, region, limit (1-200)
fields = {"App Name": "trackName", "ID": "trackId", "Bundle ID": "bundleId",
          "Genre": "primaryGenreName", "Genres": "genres", "Dev. Name": "artistName",
          "Dev. ID": "artistId", "Seller": "sellerName", "Released": "releaseDate",
          "Updated": "currentVersionReleaseDate", "Version": "version",
          "Average Rating": "averageUserRating", "Rating Count": "userRatingCount",
          "Price": "price", "Currency": "currency", "Languages": "languageCodesISO2A",
          "Content Rating": "contentAdvisoryRating", "Description": "description",
          "App URL": "trackViewUrl", "Seller URL": "sellerUrl"}


def get(url):
    for attempt in range(4):  # back off on rate limits and server errors
        try:
            with urlopen(url, timeout=30) as response:
                return response.read()
        except (HTTPError, URLError) as error:
            if attempt == 3 or getattr(error, "code", 500) not in (403, 429, 500, 502, 503, 504):
                raise
            time.sleep(30 * (attempt + 1))


out = {"region": cfg["region"], "limit": cfg["limit"],
       "timestamp": datetime.now(timezone.utc).isoformat(), "requests": {}, "results": {}}
for i, keyword in enumerate(cfg["keywords"]):
    time.sleep(3.2 * (i > 0))  # stay under the documented rate limit of about 20 calls per minute
    url = "https://itunes.apple.com/search?" + urlencode(dict(
        term=keyword, country=cfg["region"], media="software", entity="software", limit=cfg["limit"]))
    body = get(url)
    apps = json.loads(body)["results"]
    out["requests"][keyword] = {"url": url, "captured_at": datetime.now(timezone.utc).isoformat(),
                                "returned": len(apps), "sha256": hashlib.sha256(body).hexdigest()}
    out["results"][keyword] = [
        {**{name: a[key] for name, key in fields.items() if key in a}, "API Position": n}
        for n, a in enumerate(apps, 1)
        if any(d.startswith("iPhone") for d in a.get("supportedDevices", []))]
json.dump(out, sys.stdout, indent=1, ensure_ascii=False)
