"""Check the boundary between project documentation and raw evidence."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location(
    "project_check", Path(__file__).resolve().parents[1] / "check_project.py")


class LinkScopeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.check = importlib.util.module_from_spec(SPEC)
        SPEC.loader.exec_module(self.check)
        self.check.ROOT = self.root

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def test_raw_vendor_docs_are_untouched_but_project_errors_are_reported(self):
        self.write("05_Data/raw/vendor/README.md", "[upstream](MISSING.md)")
        self.write("00_Admin/current.md", "[decision](MISSING.md)")
        self.check.check_links()
        self.assertEqual(len(self.check.errors), 1)
        self.assertIn("00_Admin/current.md", self.check.errors[0])

    def test_project_links_to_missing_raw_evidence_still_fail(self):
        self.write("README.md", "[evidence](05_Data/raw/missing.csv)")
        self.check.check_links()
        self.assertEqual(len(self.check.errors), 1)

    def test_project_links_to_existing_raw_evidence_pass(self):
        self.write("05_Data/raw/frozen/evidence.csv", "app_id\nexample\n")
        self.write("README.md", "[evidence](05_Data/raw/frozen/evidence.csv)")
        self.check.check_links()
        self.assertEqual(self.check.errors, [])


if __name__ == "__main__":
    unittest.main()
