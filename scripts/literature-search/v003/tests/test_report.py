import sys, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import lit  # noqa: E402
import report  # noqa: E402

CONFIG = lit.load_config()


class StringsTest(unittest.TestCase):
    def strings(self):
        written = {}
        original = report.write
        report.write = lambda path, body: written.update({path.name: body})
        try:
            report.strings_appendix(*report.load_search(), CONFIG)
        finally:
            report.write = original
        return written['literature-strings.tex']

    def test_only_config_strands(self):
        self.assertEqual([s['id'] for s in CONFIG['strands']], ['S1', 'S2', 'S3', 'S4'])
        text = self.strings()
        self.assertNotIn('S5', text)
        self.assertNotIn('gesundheits', text)
        for s in ('S1', 'S2', 'S3', 'S4'):
            self.assertIn(f'PubMed, {s}.', text)
            self.assertIn(f'IEEE Xplore, {s}.', text)

    def test_headings_are_set(self):
        text = self.strings()
        self.assertEqual(text.count('\\paragraph{'), text.count('}\\leavevmode\n\\begin{lstlisting}'))


if __name__ == '__main__':
    unittest.main()
