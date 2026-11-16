"""Usage: python scraper.py input.json > output/run.json"""
import hashlib, json, sys, time
from datetime import datetime, timezone
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen

FIELDS = {"App Name": "trackName", "ID": "trackId", "Bundle ID": "bundleId",
          "Genre": "primaryGenreName", "Genres": "genres", "Dev. Name": "artistName",
          "Dev. ID": "artistId", "Seller": "sellerName", "Released": "releaseDate",
          "Updated": "currentVersionReleaseDate", "Version": "version",
          "Average Rating": "averageUserRating", "Rating Count": "userRatingCount",
          "Price": "price", "Currency": "currency", "Languages": "languageCodesISO2A",
          "Content Rating": "contentAdvisoryRating", "Description": "description",
          "App URL": "trackViewUrl", "Seller URL": "sellerUrl"}

def fetch(url):
    for attempt in range(4):
        try:
            with urlopen(url, timeout=30) as response:
                return response.read()
        except URLError as error:
            if attempt == 3 or getattr(error, "code", 500) not in (403, 429, 500, 502, 503, 504):
                raise
            time.sleep(30 * (attempt + 1))

def collect(cfg):
    out = dict(region=cfg["region"], limit=cfg["limit"],
               timestamp=datetime.now(timezone.utc).isoformat(), requests={}, results={})
    for index, keyword in enumerate(cfg["keywords"]):
        time.sleep(3.2 * bool(index))
        url = "https://itunes.apple.com/search?" + urlencode(dict(
            term=keyword, country=cfg["region"], media="software", entity="software", limit=cfg["limit"]))
        body = fetch(url)
        apps = json.loads(body)["results"]
        out["requests"][keyword] = dict(url=url, captured_at=datetime.now(timezone.utc).isoformat(),
                                        returned=len(apps), sha256=hashlib.sha256(body).hexdigest())
        out["results"][keyword] = [
            {**{label: app[key] for label, key in FIELDS.items() if key in app}, "API Position": pos}
            for pos, app in enumerate(apps, 1)
            if any(device.startswith("iPhone") for device in app.get("supportedDevices", []))]
    return out

if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as source:
        json.dump(collect(json.load(source)), sys.stdout, indent=1, ensure_ascii=False)
