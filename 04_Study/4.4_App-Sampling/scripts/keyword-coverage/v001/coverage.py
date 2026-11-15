"""Keyword-category coverage of the ranked sample (Results 5.2).

For each keyword category of keywords.csv, count the ranked (not preinstalled)
apps of the sample that appear within the first 30 positions of at least one
query of that category, in either store, and the apps whose primary category
belongs to it. Reads the frozen collections; writes output/coverage.csv and
prints a summary.

Usage: python coverage.py
"""
import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
DATA = ROOT / "05_Data" / "App Sampling" / "26. Oct"
KEYWORDS = ROOT / "04_Study" / "4.4_App-Sampling" / "keywords.csv"
DEPTH = 30


def load_keywords(path=KEYWORDS):
    with open(path, encoding="utf-8") as f:
        return {row["query"]: row["category"] for row in csv.DictReader(f)}


def load_sample(path=DATA / "Processed" / "apps.csv"):
    with open(path, encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["preinstalled"] == "False"]


def hits_by_query(appstore, googleplay, depth=DEPTH):
    """Map query -> set of ('apple', id) / ('play', id) within the first `depth` positions."""
    hits = defaultdict(set)
    for query, rows in appstore["results"].items():
        for row in rows[:depth]:
            hits[query].add(("apple", str(row["ID"])))
    for query, rows in googleplay["search"].items():
        for row in rows:
            if int(row["Search Position"]) <= depth:
                hits[query].add(("play", str(row["ID"])))
    return hits


def coverage(sample, keywords, hits):
    """Return {category: set of app orders found by a query of that category}."""
    found = defaultdict(set)
    for app in sample:
        ids = set()
        if app["apple_id"]:
            ids.add(("apple", app["apple_id"]))
        if app["play_id"]:
            ids.add(("play", app["play_id"]))
        for query, category in keywords.items():
            if ids & hits.get(query, set()):
                found[category].add(app["order"])
    return found


def main():
    keywords = load_keywords()
    sample = load_sample()
    with open(DATA / "Raw" / "appstore_2026-10-23.json", encoding="utf-8") as f:
        appstore = json.load(f)
    with open(DATA / "Raw" / "googleplay_2026-10-24.json", encoding="utf-8") as f:
        googleplay = json.load(f)
    found = coverage(sample, keywords, hits_by_query(appstore, googleplay))
    categories = sorted(set(keywords.values()))
    out = Path(__file__).parent / "output"
    out.mkdir(exist_ok=True)
    with open(out / "coverage.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["category", "ranked_apps_found", "app_orders"])
        for c in categories:
            orders = sorted(found[c], key=int)
            w.writerow([c, len(orders), " ".join(orders)])
            print(f"{c:22s} {len(orders):3d}")
    primary = defaultdict(int)
    for app in sample:
        primary[app["category"]] += 1
    print("primary categories:", dict(primary), "ranked apps:", len(sample))


if __name__ == "__main__":
    main()
