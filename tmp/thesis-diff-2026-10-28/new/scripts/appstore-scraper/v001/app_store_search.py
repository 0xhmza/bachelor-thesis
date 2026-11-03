#!/usr/bin/env python3
"""Collect iPhone App Store keyword candidates as JSON (Python 3.10+, no deps).

See README_app_store_search.md for usage, provenance and sampling limitations.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import hashlib
from html.parser import HTMLParser
import json
import math
from pathlib import Path
import re
import socket
import sys
import threading
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen

SEARCH_URL = "https://itunes.apple.com/search"
API_DOCS = "https://performance-partners.apple.com/search-api"
USER_AGENT = "Mozilla/5.0 (compatible; ThesisAppStoreCollector/1.0)"


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, data):
    """Replace a checkpoint atomically; never leave a half-written JSON file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # Indexers, sync tools and readers can briefly lock a Windows destination.
    for attempt in range(6):
        try:
            temporary.replace(path)
            return
        except PermissionError:
            if attempt == 5:
                raise
            time.sleep(0.2 * (attempt + 1))


class FetchError(RuntimeError):
    def __init__(self, message, source=None):
        super().__init__(message)
        self.source = source


class Client:
    def __init__(self, timeout=30, retries=2, page_delay=1.0, raw_dir=None):
        self.timeout = timeout
        self.retries = retries
        self.page_delay = page_delay
        self.raw_dir = Path(raw_dir) if raw_dir else None
        self.lock = threading.Lock()
        self.next_request = {}
        if self.raw_dir:
            # Each collection needs a fresh archive to protect earlier evidence.
            self.raw_dir.mkdir(parents=True, exist_ok=False)

    def throttle(self, url):
        host = urlsplit(url).hostname
        interval = 3.2 if host == "itunes.apple.com" else self.page_delay
        with self.lock:
            now = time.monotonic()
            start = max(now, self.next_request.get(host, now))
            self.next_request[host] = start + interval
        time.sleep(max(0, start - now))

    def get(self, url, label, accept="application/json"):
        attempts = []
        for attempt in range(self.retries + 1):
            self.throttle(url)
            requested_at = utc_now()
            headers = {"User-Agent": USER_AGENT, "Accept": accept,
                       "Accept-Language": "en-US,en;q=0.9,de;q=0.7"}
            try:
                with urlopen(Request(url, headers=headers), timeout=self.timeout) as response:
                    body = response.read()
                    meta = {"requested_url": url, "final_url": response.url,
                            "requested_at_utc": requested_at, "received_at_utc": utc_now(),
                            "http_status": response.status, "headers": dict(response.headers),
                            "body_sha256": sha256(body), "body_bytes": len(body),
                            "charset": response.headers.get_content_charset() or "utf-8"}
            except HTTPError as error:
                body = error.read()
                meta = {"requested_url": url, "final_url": error.url,
                        "requested_at_utc": requested_at, "received_at_utc": utc_now(),
                        "http_status": error.code, "headers": dict(error.headers),
                        "body_sha256": sha256(body), "body_bytes": len(body)}
            except (URLError, TimeoutError, socket.timeout, OSError) as error:
                body = b""
                meta = {"requested_url": url, "requested_at_utc": requested_at,
                        "received_at_utc": utc_now(), "http_status": None, "error": str(error)}
            if self.raw_dir:
                stem = f"{label}_attempt{attempt + 1}"
                body_path = self.raw_dir / (stem + ".body")
                body_path.write_bytes(body)
                meta["archive_body"] = body_path.resolve().as_posix()
                write_json(self.raw_dir / (stem + ".json"), meta)
            attempts.append(meta)
            if meta["http_status"] == 200:
                return body, {**meta, "attempts": attempts}
            status = meta["http_status"]
            if attempt == self.retries or (status is not None and status not in {429, 500, 502, 503, 504}):
                raise FetchError(f"GET {url}: {status or meta.get('error')}", {**meta, "attempts": attempts})
            delay = 2 ** (attempt + 1)
            retry_after = next((v for k, v in meta.get("headers", {}).items()
                                if k.lower() == "retry-after"), None)
            if retry_after:
                try:
                    delay = max(delay, float(retry_after))
                except ValueError:
                    try:
                        delay = max(delay, (parsedate_to_datetime(retry_after) - datetime.now(timezone.utc)).total_seconds())
                    except (TypeError, ValueError):
                        pass
            # A very long Retry-After is reported instead of waiting indefinitely.
            if delay > 60:
                raise FetchError(f"GET {url}: server requested a retry after {delay:.0f}s; rerun later",
                                 {**meta, "attempts": attempts})
            time.sleep(delay)
        raise FetchError(f"GET {url}: exhausted retries")


class PageParser(HTMLParser):
    """Read Apple's embedded JSON without executing any page JavaScript."""
    def __init__(self):
        super().__init__()
        self.scripts = []
        self.current = None
        self.html_language = None
        self.canonical_url = None

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == "html":
            self.html_language = attrs.get("lang")
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical_url = attrs.get("href")
        if tag == "script" and attrs.get("type") in {"application/json", "application/ld+json"}:
            self.current = {"id": attrs.get("id"), "type": attrs["type"], "text": ""}

    def handle_data(self, text):
        if self.current is not None:
            self.current["text"] += text

    def handle_endtag(self, tag):
        if tag == "script" and self.current is not None:
            self.scripts.append(self.current)
            self.current = None


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def without_metrics(value):
    if isinstance(value, dict):
        return {key: without_metrics(child) for key, child in value.items()
                if "metrics" not in key.lower() and key != "userTokenHash"}
    if isinstance(value, list):
        return [without_metrics(child) for child in value]
    return value


def check_storefront(url, country, app_id):
    parts = urlsplit(url)
    segments = parts.path.strip("/").split("/")
    if parts.hostname != "apps.apple.com" or not segments or segments[0].lower() != country.lower():
        raise ValueError(f"Product page changed storefront: {url}")
    if not re.search(rf"/(?:id)?{re.escape(str(app_id))}(?:/|$)", parts.path):
        raise ValueError(f"Product page changed app identity: {url}")


def parse_product_page(html, app_id, country, final_url):
    check_storefront(final_url, country, app_id)
    parser = PageParser()
    parser.feed(html)
    if parser.canonical_url:
        check_storefront(parser.canonical_url, country, app_id)
    embedded = None
    structured = []
    for script in parser.scripts:
        if script["id"] == "serialized-server-data":
            embedded = json.loads(script["text"])
        elif script["type"] == "application/ld+json":
            try:
                structured.append(json.loads(script["text"]))
            except json.JSONDecodeError:
                pass
    if not isinstance(embedded, dict):
        raise ValueError("Product page has no supported serialized-server-data; raw HTML retained if enabled")
    entry = next((item for item in embedded.get("data", [])
                  if str(item.get("intent", {}).get("id")) == str(app_id)), None)
    if not entry or entry.get("intent", {}).get("storefront", "").lower() != country.lower():
        raise ValueError("Embedded product identity/storefront could not be verified")
    data = without_metrics(entry["data"])
    lockup = data.get("lockup", {})
    if str(lockup.get("adamId")) != str(app_id):
        raise ValueError("Embedded primary app ID does not match requested app")
    shelves = data.get("shelfMapping", {})
    # Related apps are not properties of the app being collected.
    for key in list(shelves):
        if key.startswith(("similarItems", "moreByDeveloper", "featuredIn")):
            del shelves[key]
    links = []
    seen = set()
    for node in walk(data):
        url = node.get("url")
        if node.get("$kind") == "ExternalUrlAction" and isinstance(url, str) and url.startswith(("https://", "http://")):
            pair = (node.get("title"), url)
            if pair not in seen:
                seen.add(pair)
                links.append({"title": pair[0], "url": url})
    policy_urls = list(dict.fromkeys(link["url"] for link in links
                      if re.search(r"privacy policy|datenschutz", link["title"] or "", re.I)))
    privacy = shelves.get("privacyHeader", {}).get("seeAllAction") or {}
    detail_shelves = (privacy.get("pageData") or {}).get("shelves", [])
    annotations = shelves.get("information", {}).get("items", [])
    purchases = next((item for item in annotations
                      if re.fullmatch(r"In-App Purchases|In-App-Käufe", item.get("title", ""), re.I)), None)
    recent = shelves.get("mostRecentVersion") or {}
    history = ((recent.get("seeAllAction") or {}).get("pageData") or {}).get("shelves")
    return {"status": "ok", "language": parser.html_language,
            "intent": entry["intent"], "canonical_url": parser.canonical_url,
            "subtitle": lockup.get("subtitle"),
            "offer": data.get("titleOfferDisplayProperties"),
            "privacy_policy_urls": policy_urls,
            "privacy_policy_link_status": "found" if policy_urls else "not_found_in_supported_page_fields",
            "external_links": links,
            "privacy_summary": shelves.get("privacyTypes"),
            "privacy_details": detail_shelves or None,
            "information": shelves.get("information"),
            "in_app_purchases": purchases or shelves.get("inAppPurchases"),
            "version_history": history or shelves.get("versionHistory"),
            "latest_update": recent or shelves.get("whatsNew"),
            "ratings": shelves.get("productRatings"),
            "displayed_reviews": shelves.get("allProductReviews"),
            "structured_data": structured,
            "product_page_data": data}


def normalize_app(raw, position):
    devices = raw.get("supportedDevices")
    iphone = (any(str(device).lower().startswith("iphone") for device in devices)
              if isinstance(devices, list) and devices else None)
    price = raw.get("price")
    try:
        size = int(raw["fileSizeBytes"])
    except (KeyError, ValueError, TypeError):
        size = None
    return {"api_result_position": position, "app_id": raw.get("trackId"),
            "name": raw.get("trackName"), "bundle_id": raw.get("bundleId"),
            "app_store_url": raw.get("trackViewUrl"), "developer": raw.get("artistName"),
            "developer_id": raw.get("artistId"), "developer_url": raw.get("artistViewUrl"),
            "seller": raw.get("sellerName"), "developer_website": raw.get("sellerUrl"),
            "description": raw.get("description"), "genres": raw.get("genres"),
            "genre_ids": raw.get("genreIds"), "primary_genre": raw.get("primaryGenreName"),
            "price": price, "formatted_price": raw.get("formattedPrice"),
            "currency": raw.get("currency"),
            "free_to_download": price == 0 if isinstance(price, (int, float)) else None,
            "average_rating": raw.get("averageUserRating"), "rating_count": raw.get("userRatingCount"),
            "current_version_average_rating": raw.get("averageUserRatingForCurrentVersion"),
            "current_version_rating_count": raw.get("userRatingCountForCurrentVersion"),
            "version": raw.get("version"), "release_date": raw.get("releaseDate"),
            "current_version_release_date": raw.get("currentVersionReleaseDate"),
            "release_notes": raw.get("releaseNotes"), "minimum_ios_version": raw.get("minimumOsVersion"),
            "file_size_bytes": size, "languages": raw.get("languageCodesISO2A"),
            "content_rating": raw.get("contentAdvisoryRating"), "advisories": raw.get("advisories"),
            "iphone_compatible": iphone, "supported_devices": devices,
            "features": raw.get("features"), "screenshots": raw.get("screenshotUrls"),
            "ipad_screenshots": raw.get("ipadScreenshotUrls"),
            "appletv_screenshots": raw.get("appletvScreenshotUrls"),
            "artwork": {key: value for key, value in raw.items() if key.startswith("artworkUrl")},
            "downloads": None, "downloads_status": "not_provided_by_public_search_api",
            "raw_api_data": raw}


def enrich_app(client, app, country):
    url = f"https://apps.apple.com/{country}/app/id{app['app_id']}?l=en&platform=iphone"
    provenance = {"requested_url": url}
    try:
        body, provenance = client.get(url, f"app_{app['app_id']}", "text/html")
        result = parse_product_page(body.decode(provenance["charset"]), app["app_id"], country, provenance["final_url"])
        return {**result, "source": provenance}
    except (FetchError, ValueError, KeyError, TypeError) as error:
        return {"status": "error", "error": str(error),
                "source": (error.source if isinstance(error, FetchError) else None) or provenance}


def collect(keyword, *, country="de", limit=200, enrich=True, timeout=30,
            retries=2, workers=4, page_delay=1, raw_dir=None, checkpoint=None):
    if not keyword.strip():
        raise ValueError("Keyword must not be empty")
    if not re.fullmatch(r"[a-zA-Z]{2}", country):
        raise ValueError("Country must be a two-letter storefront code")
    if not 1 <= limit <= 200:
        raise ValueError("Limit must be between 1 and 200")
    if not 1 <= workers <= 8 or not 0 <= retries <= 5:
        raise ValueError("Workers must be 1..8 and retries must be 0..5")
    if not math.isfinite(timeout) or not math.isfinite(page_delay) or timeout <= 0 or page_delay < 0:
        raise ValueError("Timeout must be positive and page delay nonnegative (finite numbers)")
    country = country.lower()
    params = {"term": keyword.strip(), "country": country, "media": "software",
              "entity": "software", "limit": limit, "lang": "en_us", "version": 2, "explicit": "Yes"}
    url = SEARCH_URL + "?" + urlencode(params)
    started_at = utc_now()
    client = Client(timeout, retries, page_delay, raw_dir)
    body, source = client.get(url, "search")
    payload = json.loads(body)
    if not isinstance(payload, dict) or not isinstance(payload.get("results"), list):
        raise ValueError("Search response has no results array")
    apps, excluded, seen = [], [], set()
    for position, raw in enumerate(payload["results"], 1):
        if not isinstance(raw, dict):
            raise ValueError(f"Search result {position} is not an object")
        app = normalize_app(raw, position)
        app_id = app["app_id"]
        reason = None
        if raw.get("kind") != "software" or not str(app_id).isdigit():
            reason = "not_an_identifiable_ios_app"
        elif app_id in seen:
            reason = "duplicate_app_id"
        elif app["iphone_compatible"] is not True:
            reason = "no_iphone_device_in_supportedDevices" if app["iphone_compatible"] is False else "iphone_compatibility_unknown"
        if reason:
            excluded.append({"api_result_position": position, "reason": reason, "raw_api_data": raw})
        else:
            seen.add(app_id)
            app["app_store"] = {"status": "pending" if enrich else "not_requested"}
            apps.append(app)
    result = {"schema_version": "1.0", "collection": {
                "status": "collecting", "started_at_utc": started_at, "finished_at_utc": None,
                "keyword": keyword.strip(), "country": country, "device": "iphone",
                "parameters": params, "source": source, "api_documentation": API_DOCS,
                "script_sha256": sha256(Path(__file__).read_bytes()), "python_version": sys.version,
                "settings": {"enrich": enrich, "timeout": timeout, "retries": retries,
                             "workers": workers, "page_delay": page_delay},
                "api_reported_result_count": payload.get("resultCount"),
                "api_returned_result_count": len(payload["results"]), "app_count": len(apps),
                "excluded_count": len(excluded), "page_success_count": 0, "page_error_count": 0,
                "requested_limit_reached": len(payload["results"]) >= limit,
                "limitations": [
                    "API result position is not verified iPhone App Store UI rank or popularity.",
                    "The API documents limits of 1..200 and no pagination; this is not an exhaustive app census.",
                    "country is the requested storefront, not evidence of German users or downloads.",
                    "English is requested; actual product-page language is recorded and API text may vary.",
                    "Privacy labels are developer declarations; a missing extracted policy link is not proof of no policy.",
                    "Only reviews/version history/IAP entries embedded in the page are captured, not complete histories.",
                    "Missing values remain null; no eligibility, rating floor or final sample selection is applied."]},
              "apps": apps, "excluded_results": excluded,
              "api_response_metadata": {key: value for key, value in payload.items() if key != "results"}}
    if checkpoint:
        write_json(checkpoint, result)
    print(f"Found {len(apps)} iPhone apps from {len(payload['results'])} API results ({country}, {keyword!r}).", file=sys.stderr)
    if enrich:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {pool.submit(enrich_app, client, app, country): app for app in apps}
            for completed, future in enumerate(as_completed(futures), 1):
                app = futures[future]
                app["app_store"] = future.result()
                key = "page_success_count" if app["app_store"]["status"] == "ok" else "page_error_count"
                result["collection"][key] += 1
                if checkpoint:
                    write_json(checkpoint, result)
                if completed % 10 == 0 or completed == len(apps):
                    print(f"Product pages {completed}/{len(apps)}; errors: {result['collection']['page_error_count']}", file=sys.stderr)
    result["collection"]["status"] = "partial" if result["collection"]["page_error_count"] else "complete"
    result["collection"]["finished_at_utc"] = utc_now()
    if checkpoint:
        write_json(checkpoint, result)
    return result


def reparse_capture(source_path, output_path):
    """Rebuild page fields from an archived run, without making network calls."""
    source_path, output_path = Path(source_path), Path(output_path)
    if output_path.exists():
        raise ValueError(f"Output already exists: {output_path}")
    result = json.loads(source_path.read_text(encoding="utf-8"))
    if result.get("schema_version") != "1.0":
        raise ValueError("Reparse requires a version 1.0 collection")
    # A checkpoint may predate the last downloaded pages. Recover from the
    # archived per-request metadata instead of discarding or refetching them.
    search_archive = result["collection"].get("source", {}).get("archive_body")
    archive_dir = Path(search_archive).parent if search_archive else None
    for app in result["apps"]:
        page = app["app_store"]
        provenance = page.get("source", {})
        archive = provenance.get("archive_body")
        if not archive and archive_dir:
            candidates = []
            for path in archive_dir.glob(f"app_{app['app_id']}_attempt*.json"):
                candidate = json.loads(path.read_text(encoding="utf-8"))
                if candidate.get("http_status") == 200 and candidate.get("archive_body"):
                    candidates.append(candidate)
            if candidates:
                provenance = max(candidates, key=lambda candidate: candidate["received_at_utc"])
                archive = provenance["archive_body"]
        if not archive:
            if page["status"] in {"ok", "pending"}:
                raise ValueError(f"App {app['app_id']} has no raw archive; use --raw-dir when collecting")
            continue
        body = Path(archive).read_bytes()
        if sha256(body) != provenance.get("body_sha256"):
            raise ValueError(f"Archive hash mismatch for app {app['app_id']}")
        try:
            app["app_store"] = {**parse_product_page(body.decode(provenance.get("charset", "utf-8")),
                app["app_id"], result["collection"]["country"], provenance["final_url"]), "source": provenance}
        except (ValueError, KeyError, TypeError) as error:
            app["app_store"] = {"status": "error", "error": str(error), "source": provenance}
    info = result["collection"]
    info["page_success_count"] = sum(app["app_store"]["status"] == "ok" for app in result["apps"])
    info["page_error_count"] = sum(app["app_store"]["status"] == "error" for app in result["apps"])
    info["status"] = "partial" if info["page_error_count"] else "complete"
    if not info.get("finished_at_utc"):
        timestamps = [app["app_store"].get("source", {}).get("received_at_utc", "") for app in result["apps"]]
        info["finished_at_utc"] = max(timestamps) or None
    result["derivation"] = {"reparsed_at_utc": utc_now(), "source_json": source_path.resolve().as_posix(),
                            "source_json_sha256": sha256(source_path.read_bytes()),
                            "parser_script_sha256": sha256(Path(__file__).read_bytes())}
    write_json(output_path, result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("keyword", nargs="?", help='Search term, for example "fitness" or "sleep tracker"')
    parser.add_argument("--reparse", type=Path, help="Reparse a saved JSON's archived product pages offline; requires -o")
    parser.add_argument("--country", default="de", help="Two-letter storefront code (default: de)")
    parser.add_argument("--limit", type=int, default=200, help="Requested API result limit, 1..200 (default: 200)")
    parser.add_argument("-o", "--output", type=Path, help="Save JSON here; otherwise print JSON to stdout")
    parser.add_argument("--raw-dir", type=Path, help="New directory for exact HTTP responses and provenance")
    parser.add_argument("--api-only", action="store_true", help="Skip product-page enrichment")
    parser.add_argument("--timeout", type=float, default=30)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--page-delay", type=float, default=1, help="Minimum seconds between page requests (default: 1)")
    args = parser.parse_args()
    if args.output and args.output.exists():
        parser.error(f"Output already exists; choose a new snapshot path: {args.output}")
    if args.reparse and (args.keyword or not args.output):
        parser.error("Use --reparse INPUT -o OUTPUT without a keyword")
    if not args.reparse and not args.keyword:
        parser.error("A search keyword is required")
    try:
        if args.reparse:
            result = reparse_capture(args.reparse, args.output)
        else:
            result = collect(args.keyword, country=args.country, limit=args.limit, enrich=not args.api_only,
                         timeout=args.timeout, retries=args.retries, workers=args.workers,
                         page_delay=args.page_delay, raw_dir=args.raw_dir, checkpoint=args.output)
    except (FetchError, ValueError, OSError) as error:
        print(f"Collection failed: {error}", file=sys.stderr)
        return 1
    if args.output:
        print(f"Saved {args.output.resolve()}", file=sys.stderr)
    else:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if result["collection"]["status"] == "partial" else 0


if __name__ == "__main__":
    raise SystemExit(main())
