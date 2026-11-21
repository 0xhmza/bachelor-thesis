"""Draw the Android sample of health tracking apps from Google Play.

1. Search each keyword in the German storefront; keep the first `depth` results.
2. Read the store page of every app found and of the preinstalled apps.
3. Rank the apps by their German review count. Walk down the ranking and take
   each app that the screening file marks as eligible, until the sample is full.

Usage: python sample.py config.json
"""
import csv, json, re, ssl, sys, time
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen
from google_play_scraper import app

ssl._create_default_https_context = ssl.create_default_context  # the library disables TLS checks
COLUMNS = ["rank", "appId", "title", "developer", "genre", "reviews", "installs", "free", "found_by"]


def search(query, cfg):
    """Package IDs of the first result page, in the order Google Play shows them."""
    url = (f"https://play.google.com/store/search?q={quote(query)}&c=apps"
           f"&hl={cfg['language']}&gl={cfg['region']}")
    page = urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read().decode()
    time.sleep(1)
    return list(dict.fromkeys(re.findall(r"/store/apps/details\?id=([\w.]+)", page)))[:cfg["depth"]]


def main(config):
    cfg = json.loads(Path(config).read_text(encoding="utf-8"))
    out = Path(cfg["output"])
    out.mkdir(parents=True, exist_ok=True)

    saved = out / "search.json"  # searched once; a rerun keeps the same candidates
    if saved.exists():
        hits = json.loads(saved.read_text(encoding="utf-8"))
    else:
        hits = {query: search(query, cfg) for query in cfg["keywords"]}
        saved.write_text(json.dumps(hits, indent=1), encoding="utf-8")
    found = {}
    for query, ids in hits.items():
        for position, app_id in enumerate(ids, 1):
            found.setdefault(app_id, []).append(f"{query} ({position})")

    pages = out / "pages.jsonl"  # cache: an interrupted run resumes here
    cache = {}
    if pages.exists():
        with pages.open(encoding="utf-8") as source:  # one JSON record per line
            cache = {p["appId"]: p for p in map(json.loads, source)}
    with pages.open("a", encoding="utf-8") as sink:
        for app_id in sorted((set(found) | set(cfg["preinstalled"])) - set(cache)):
            try:
                page = app(app_id, lang=cfg["language"], country=cfg["region"])
            except Exception as error:  # e.g. not offered in this storefront
                page = {"appId": app_id, "error": str(error)}
            page.pop("comments", None)
            cache[app_id] = page
            sink.write(json.dumps(page, ensure_ascii=False, default=str) + "\n")
            time.sleep(1)

    apps = [dict(cache[i], found_by="; ".join(found[i])) for i in found if "error" not in cache[i]]
    apps.sort(key=lambda a: (-(a.get("reviews") or 0), a["appId"]))
    for rank, a in enumerate(apps, 1):
        a["rank"] = rank
    write(out / "candidates.csv", apps)

    with open(cfg["screening"], encoding="utf-8") as source:
        decision = {row["id"]: row["decision"] for row in csv.DictReader(source)}
    sample = []
    for a in apps:
        if len(sample) == cfg["size"] - len(cfg["preinstalled"]):
            break
        if a["appId"] in cfg["preinstalled"]:
            continue
        if a["appId"] not in decision:
            sys.exit(f"Screen {a['appId']} ({a['title']}) next, then run again.")
        if decision[a["appId"]] == "eligible":
            sample.append(a)
    sample += [dict(cache[i], rank="preinstalled", found_by="") for i in cfg["preinstalled"]]
    write(out / "sample.csv", sample)
    print(f"{len(hits)} keywords, {len(apps)} apps found, {len(sample)} in the sample")


def write(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as sink:
        table = csv.DictWriter(sink, COLUMNS, extrasaction="ignore")
        table.writeheader()
        table.writerows(rows)


if __name__ == "__main__":
    main(sys.argv[1])
