"""Small source audit and optional listing check; never calls search/review RPCs.

Run from the repository root. Existing raw captures are not overwritten.
This is a mechanism demonstration, not the thesis sampling collector.
"""
import argparse
import hashlib
import importlib
import json
from pathlib import Path
import ssl
import subprocess
import sys
from datetime import datetime, timezone
from urllib.parse import parse_qs, urlencode
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "05_Data/raw/2026-10-11_scraper-research"
SOURCE = RAW / "python-source"
USER_AGENT = "ThesisScraperMechanismCheck/1.0"


def save_json(path, obj):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(obj, stream, ensure_ascii=False, indent=2)


def fetch(url, path):
    captured = datetime.now(timezone.utc).isoformat()
    with urlopen(Request(url, headers={"User-Agent": USER_AGENT}),
                 timeout=30, context=ssl.create_default_context()) as response:
        body = response.read()
        metadata = {"requested_url": url, "final_url": response.url,
                    "status": response.status, "captured_utc": captured,
                    "response_headers": dict(response.headers),
                    "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}
    with path.open("xb") as stream:
        stream.write(body)
    save_json(path.with_suffix(path.suffix + ".metadata.json"), metadata)
    return body.decode("utf-8"), metadata


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--live-listings", action="store_true")
    args = parser.parse_args()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    batch = RAW / stamp
    batch.mkdir(parents=True, exist_ok=False)
    # Importing upstream request.py changes the process SSL default. Restore it
    # immediately; live downloads below always use a verified explicit context.
    original_context = ssl._create_default_https_context
    sys.path.insert(0, str(SOURCE))
    try:
        app_module = importlib.import_module("google_play_scraper.features.app")
        review_module = importlib.import_module("google_play_scraper.features.reviews")
        search_module = importlib.import_module("google_play_scraper.features.search")
        formats = importlib.import_module("google_play_scraper.constants.request").Formats
        specs = importlib.import_module("google_play_scraper.constants.element").ElementSpecs
        regex = importlib.import_module("google_play_scraper.constants.regex").Regex
        error = importlib.import_module("google_play_scraper.exceptions").NotFoundError
    finally:
        ssl._create_default_https_context = original_context

    # Artificial HTML isolates the parser from the network and demonstrates
    # the extraction route with clearly fictional values.
    detail = [None] * 146
    detail[0] = ["Synthetic app"]
    detail[13] = ["1,000,000+", 1000000, 1234567]
    data = [None, [None, None, detail]]
    synthetic = "<script>AF_initDataCallback({key: 'ds:5', data:" + json.dumps(data) + ", sideChannel: {}});</script>"
    parsed = app_module.parse_dom(synthetic, "example.synthetic", "https://example.invalid")
    expected = {"title": "Synthetic app", "installs": "1,000,000+",
                "minInstalls": 1000000, "realInstalls": 1234567}
    assert {k: parsed[k] for k in expected} == expected
    missing = app_module.parse_dom("<html>no dataset</html>", "example.synthetic", "https://example.invalid")
    assert missing["title"] is None and missing["realInstalls"] is None

    request_urls = []
    def fake_get(url):
        request_urls.append(url)
        if len(request_urls) == 1:
            raise error("Synthetic 404")
        return synthetic
    with patch.object(app_module, "get", side_effect=fake_get):
        fallback = app_module.app("example.synthetic", lang="de", country="de")
    assert "gl=de" in request_urls[0] and "gl=" not in request_urls[1]

    review_body = formats.Reviews.build_body("example.synthetic", 2, 2, "null", "null", None)
    envelope = json.loads(parse_qs(review_body.decode())["f.req"][0])
    inner_payload = json.loads(envelope[0][0][1])
    # Network failure is converted to an empty result and terminal token.
    with patch.object(review_module, "post", side_effect=RuntimeError("Synthetic transport failure")):
        failed_reviews, token = review_module.reviews("example.synthetic", count=2)
    assert failed_reviews == [] and token.token is None

    audit = {
        "python_commit": subprocess.check_output(["git", "-C", str(SOURCE), "rev-parse", "HEAD"], text=True).strip(),
        "python_runtime": sys.version,
        "synthetic_parser_result": expected,
        "synthetic_missing_dataset_result": {k: missing[k] for k in ("title", "realInstalls", "containsAds", "histogram", "version")},
        "synthetic_country_fallback_requested_urls": request_urls,
        "synthetic_country_fallback_returned_url": fallback["url"],
        "review_rpc_id": envelope[0][0][0],
        "review_inner_payload": inner_payload,
        "synthetic_failed_review_result": {"count": len(failed_reviews), "token": token.token},
        "live_observations": [],
    }

    if args.live_listings:
        robots, _ = fetch("https://play.google.com/robots.txt", batch / "robots.txt")
        rules = RobotFileParser()
        rules.parse(robots.splitlines())
        audit["robots_checks"] = {
            "search": rules.can_fetch(USER_AGENT, "https://play.google.com/store/search?q=Periode&c=apps"),
            "review_rpc": rules.can_fetch(USER_AGENT, formats.Reviews.build("de", "de")),
        }
        for country in ("de", "us"):
            url = "https://play.google.com/store/apps/details?" + urlencode({"id": "com.clue.android", "hl": "de", "gl": country})
            if not rules.can_fetch(USER_AGENT, url):
                audit["live_observations"].append({"url": url, "status": "not fetched: robots disallow"})
                continue
            try:
                html, metadata = fetch(url, batch / ("clue_" + country + ".html"))
                result = app_module.parse_dom(html, "com.clue.android", metadata["final_url"])
                values = {k: result.get(k) for k in ("title", "installs", "minInstalls", "realInstalls", "score", "ratings", "reviews", "version")}
                datasets = {}
                for match in regex.SCRIPT.findall(html):
                    keys, raw_values = regex.KEY.findall(match), regex.VALUE.findall(match)
                    if keys and raw_values:
                        datasets[keys[0]] = json.loads(raw_values[0])
                observation = {"requested_country": country, "metadata": metadata,
                               "parsed_fields": values, "embedded_dataset_keys": sorted(datasets),
                               "raw_install_array": datasets["ds:5"][1][2][13],
                               "value_matches_direct_index": values["realInstalls"] == specs.Detail["realInstalls"].extract_content(datasets)}
                audit["live_observations"].append(observation)
            except Exception as exc:
                audit["live_observations"].append({"url": url, "error": type(exc).__name__ + ": " + str(exc)})
    save_json(batch / "mechanism_check.json", audit)
    summary = {"batch": str(batch), "python_commit": audit["python_commit"],
               "offline_checks": "passed", "robots_checks": audit.get("robots_checks"),
               "live_observations": [{k: row.get(k) for k in ("requested_country", "parsed_fields", "raw_install_array", "error")}
                                     for row in audit["live_observations"]]}
    print(json.dumps(summary, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
