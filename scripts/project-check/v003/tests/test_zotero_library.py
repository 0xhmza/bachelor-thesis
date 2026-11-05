"""The project check warns when the Zotero library file does not match references.bib."""
import hashlib
import importlib.util
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "project_check", Path(__file__).resolve().parents[1] / "check_project.py")
BIB_TEXT = "@misc{a2020b,\n  title = {T}\n}\n"


class ZoteroLibraryCheck(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        (root / "_shared").mkdir()
        self.check = importlib.util.module_from_spec(SPEC)
        SPEC.loader.exec_module(self.check)
        self.check.BIB = root / "_shared/references.bib"
        self.check.ZOTERO = root / "_shared/references-zotero.rdf"
        self.check.BIB.write_bytes(BIB_TEXT.encode("utf-8"))

    def rdf(self, digest):
        self.check.ZOTERO.write_text(f"<?xml version='1.0'?>\n<!-- bib-sha256={digest} -->\n<rdf:RDF/>\n", encoding="utf-8")

    def test_missing_file_warns(self):
        self.check.check_zotero_library()
        self.assertIn("missing", self.check.warnings[0])

    def test_current_file_is_silent_even_with_windows_line_endings(self):
        self.rdf(hashlib.sha256(BIB_TEXT.encode("utf-8")).hexdigest())
        self.check.BIB.write_bytes(BIB_TEXT.replace("\n", "\r\n").encode("utf-8"))
        self.check.check_zotero_library()
        self.assertEqual(self.check.warnings, [])

    def test_stale_file_warns_with_the_command(self):
        self.rdf("0" * 64)
        self.check.check_zotero_library()
        self.assertEqual(len(self.check.warnings), 1)
        self.assertIn("build_zotero_library.py", self.check.warnings[0])


if __name__ == "__main__":
    unittest.main()
