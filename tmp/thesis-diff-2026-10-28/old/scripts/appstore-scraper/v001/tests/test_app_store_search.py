"""Offline checks for sampling identity, order, missing data and page extraction."""
import json
from io import BytesIO
from email.message import Message
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import app_store_search as collector


def page_html(app_id="123", country="de"):
    data = {"lockup": {"adamId": app_id, "subtitle": "Track workouts"},
            "titleOfferDisplayProperties": {"hasInAppPurchases": True},
            "shelfMapping": {
                "information": {"items": [{"title": "In-App Purchases", "items": [
                    {"leadingText": "Monthly", "trailingText": "4,99 €"}]}]},
                "privacyHeader": {"seeAllAction": {"pageData": {"shelves": [{"contentType": "privacyType"}]}},
                                  "items": [{"$kind": "ExternalUrlAction", "title": "Developer’s Privacy Policy",
                                             "url": "https://example.org/privacy"}]},
                "mostRecentVersion": {"seeAllAction": {"pageData": {"shelves": [{"items": [{"text": "Fixes"}]}]}}},
                "similarItems": {"items": [{"$kind": "ExternalUrlAction", "title": "Privacy Policy",
                                            "url": "https://wrong.example/privacy"}]}}
            , "pageMetrics": {"secret": "analytics"}}
    state = {"data": [{"intent": {"id": app_id, "storefront": country}, "data": data}]}
    return '<html lang="en-GB"><script type="application/json" id="serialized-server-data">' + json.dumps(state) + '</script></html>'


class CollectionTests(unittest.TestCase):
    def test_page_privacy_purchases_and_version_history(self):
        page = collector.parse_product_page(page_html(), 123, "de", "https://apps.apple.com/de/app/test/id123?l=en")
        self.assertEqual(page["privacy_policy_urls"], ["https://example.org/privacy"])
        self.assertEqual(page["in_app_purchases"]["items"][0]["trailingText"], "4,99 €")
        self.assertEqual(page["version_history"][0]["items"][0]["text"], "Fixes")
        self.assertEqual(page["privacy_details"][0]["contentType"], "privacyType")
        self.assertEqual(page["language"], "en-GB")
        self.assertNotIn("pageMetrics", page["product_page_data"])

    def test_storefront_and_identity_changes_are_rejected(self):
        for url in ("https://apps.apple.com/us/app/id123", "https://apps.apple.com/de/app/id456"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                collector.parse_product_page(page_html(), 123, "de", url)
        with self.assertRaises(ValueError):
            collector.parse_product_page(page_html(country="us"), 123, "de", "https://apps.apple.com/de/app/id123")

    def test_embedded_identity_must_match(self):
        with self.assertRaises(ValueError):
            collector.parse_product_page(page_html(app_id="456"), 123, "de", "https://apps.apple.com/de/app/id123")

    def test_missing_serialized_data_is_reported(self):
        with self.assertRaisesRegex(ValueError, "serialized-server-data"):
            collector.parse_product_page("<html>Unavailable</html>", 123, "de", "https://apps.apple.com/de/app/id123")

    def test_missing_fields_are_unknown_and_unknown_api_fields_survive(self):
        raw = {"trackId": 123, "futureAppleField": {"a": 1}}
        app = collector.normalize_app(raw, 4)
        for field in ("price", "rating_count", "iphone_compatible", "downloads", "free_to_download"):
            self.assertIsNone(app[field])
        self.assertEqual(app["raw_api_data"], raw)
        self.assertEqual(app["api_result_position"], 4)

    def test_api_order_retained_and_exclusions_accounted_for(self):
        rows = [{"trackId": 5, "kind": "software", "trackName": "Second alphabetically", "supportedDevices": ["iPhone17"]},
                {"trackId": 6, "kind": "software", "supportedDevices": ["iPad17"]},
                {"trackId": 7, "kind": "software"},
                {"trackId": 8, "kind": "software", "trackName": "Alphabetically first", "supportedDevices": ["iPhone16"]},
                {"trackId": 5, "kind": "software", "supportedDevices": ["iPhone17"]}]
        payload = json.dumps({"resultCount": 5, "results": rows}).encode()
        with patch.object(collector.Client, "get", return_value=(payload, {})):
            result = collector.collect("fitness", enrich=False)
        self.assertEqual([a["app_id"] for a in result["apps"]], [5, 8])
        self.assertEqual([a["api_result_position"] for a in result["apps"]], [1, 4])
        self.assertEqual(len(result["excluded_results"]), 3)

    def test_page_failure_retains_candidate(self):
        payload = json.dumps({"results": [{"trackId": 1, "kind": "software", "supportedDevices": ["iPhone16"]}]}).encode()
        with patch.object(collector.Client, "get", return_value=(payload, {})), patch.object(
                collector, "enrich_app", return_value={"status": "error", "error": "HTTP 404"}):
            result = collector.collect("fitness")
        self.assertEqual(result["collection"]["status"], "partial")
        self.assertEqual(result["collection"]["app_count"], 1)
        self.assertEqual(result["collection"]["page_error_count"], 1)

    def test_invalid_input_does_not_start_network(self):
        for kwargs in ({"limit": 201}, {"country": "Germany"}, {"timeout": float("nan")}, {"workers": 0}):
            with self.subTest(kwargs=kwargs), patch.object(collector.Client, "get") as request:
                with self.assertRaises(ValueError):
                    collector.collect("fitness", **kwargs)
                request.assert_not_called()

    def test_http_rate_limit_retries_and_retains_attempts(self):
        headers = Message()
        headers["Retry-After"] = "4"
        throttled = HTTPError("https://itunes.apple.com/search", 429, "Slow down", headers, BytesIO(b"throttled"))
        response = unittest.mock.MagicMock()
        response.__enter__.return_value = response
        response.read.return_value = b'{"results": []}'
        response.url = "https://itunes.apple.com/search"
        response.status = 200
        response.headers = Message()
        with patch.object(collector, "urlopen", side_effect=[throttled, response]), patch.object(
                collector.Client, "throttle"), patch.object(collector.time, "sleep") as sleep:
            body, source = collector.Client().get(response.url, "search")
        self.assertEqual(body, b'{"results": []}')
        self.assertEqual([a["http_status"] for a in source["attempts"]], [429, 200])
        sleep.assert_called_once_with(4.0)

    def test_permanent_http_failure_has_provenance(self):
        error = HTTPError("https://apps.apple.com/de/app/id123", 404, "Missing", Message(), BytesIO(b"missing"))
        with patch.object(collector, "urlopen", side_effect=error) as request, patch.object(collector.Client, "throttle"):
            page = collector.enrich_app(collector.Client(), {"app_id": 123}, "de")
        self.assertEqual(page["status"], "error")
        self.assertEqual(page["source"]["http_status"], 404)
        request.assert_called_once()

    def test_offline_reparse_verifies_hashes(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            body = page_html().encode()
            archive = root / "page.body"
            archive.write_bytes(body)
            provenance = {"archive_body": str(archive), "body_sha256": collector.sha256(body),
                          "final_url": "https://apps.apple.com/de/app/id123"}
            data = {"schema_version": "1.0", "collection": {"status": "complete", "country": "de"},
                    "apps": [{"app_id": 123, "app_store": {"status": "ok", "source": provenance}}]}
            source, output = root / "source.json", root / "derived.json"
            collector.write_json(source, data)
            with patch.object(collector.Client, "get", side_effect=AssertionError("Offline means no HTTP")):
                rebuilt = collector.reparse_capture(source, output)
            self.assertEqual(rebuilt["apps"][0]["app_store"]["status"], "ok")
            archive.write_bytes(b"changed")
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                collector.reparse_capture(source, root / "invalid.json")

    def test_reparse_recovers_downloads_after_interrupted_checkpoint(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            body = page_html().encode()
            archive = root / "app_123_attempt1.body"
            archive.write_bytes(body)
            provenance = {"archive_body": str(archive), "body_sha256": collector.sha256(body),
                          "received_at_utc": "2026-10-20T18:00:00+00:00",
                          "http_status": 200, "final_url": "https://apps.apple.com/de/app/id123"}
            collector.write_json(root / "app_123_attempt1.json", provenance)
            source = root / "checkpoint.json"
            collector.write_json(source, {"schema_version": "1.0", "collection": {
                "status": "collecting", "country": "de", "source": {"archive_body": str(root / "search.body")}},
                "apps": [{"app_id": 123, "app_store": {"status": "pending"}}]})
            result = collector.reparse_capture(source, root / "recovered.json")
            self.assertEqual(result["collection"]["status"], "complete")
            self.assertEqual(result["collection"]["page_success_count"], 1)

    def test_atomic_save_retries_windows_file_lock(self):
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(Path, "replace", side_effect=[PermissionError("locked"), None]) as replace, patch.object(
                    collector.time, "sleep") as sleep:
                collector.write_json(Path(folder) / "result.json", {"apps": []})
            self.assertEqual(replace.call_count, 2)
            sleep.assert_called_once_with(0.2)


if __name__ == "__main__":
    unittest.main()
