import sys, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import report  # noqa: E402


class TexTest(unittest.TestCase):
    def test_escape_and_quotes(self):
        self.assertEqual(report.tex('"privacy risk" & 50% R_1'), r'\enquote{privacy risk} \& 50\% R\_1')
        self.assertEqual(report.thousands(5667), '5{,}667')
        self.assertEqual(report.tex('a\\b{c}'), r'a\textbackslash{}b\{c\}')

    def test_clean_title(self):
        self.assertEqual(report.clean_title('"“My data\\": User Risk"'), '“My data": User Risk')
        self.assertEqual(report.clean_title('Plain  title'), 'Plain title')


class RowsTest(unittest.TestCase):
    def test_included_rows_sorted_and_linked(self):
        screening = [
            {'decision': 'include', 'code': 'I2', 'year': '2019', 'first_author': 'Kirsten Huckvale', 'title': 'A & B',
             'doi': '10.1/x_y', 'url': ''},
            {'decision': 'exclude', 'code': 'E1', 'year': '2020', 'first_author': 'X', 'title': 'C', 'doi': '', 'url': ''},
            {'decision': 'include', 'code': 'I1', 'year': '2025', 'first_author': '', 'title': 'D',
             'doi': '', 'url': 'https://example.org/p'},
        ]
        rows = report.included_rows(screening)
        self.assertEqual(len(rows), 2)
        self.assertTrue(rows[0].startswith(r'1 & I1 & -- & 2025 & D & \href{https://example.org/p}{example.org}'))
        self.assertIn(r'Huckvale & 2019 & A \& B & \href{https://doi.org/10.1/x_y}{\nolinkurl{10.1/x\_y}}', rows[1])


if __name__ == '__main__':
    unittest.main()
