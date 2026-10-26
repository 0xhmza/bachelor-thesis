import sys, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import search  # noqa: E402


def hit(**kw):
    base = {'source': 'OpenAlex', 'source_id': 'x', 'doi': '', 'arxiv': '', 'title': '', 'year': 2020, 'date': '',
            'venue': '', 'type': '', 'language': '', 'citations': 0, 'authors': [], 'url': '', 'abstract': '',
            'query': 'Q1'}
    base.update(kw)
    return base


class QueryTest(unittest.TestCase):
    def test_expand_and_s2_syntax(self):
        q = search.expand('{domain} AND (harm OR "privacy risk")', '("a" OR b)')
        self.assertEqual(q, '("a" OR b) AND (harm OR "privacy risk")')
        self.assertEqual(search.to_s2(q), '("a" | b) + (harm | "privacy risk")')


class NormaliseTest(unittest.TestCase):
    def test_doi(self):
        self.assertEqual(search.norm_doi('https://doi.org/10.1145/ABC'), '10.1145/abc')
        self.assertEqual(search.norm_doi('doi:10.1/X'), '10.1/x')
        self.assertEqual(search.norm_doi(None), '')

    def test_title(self):
        self.assertEqual(search.norm_title('“I Deleted It”: Période-Tracking'), 'i deleted it periode tracking')

    def test_abstract(self):
        self.assertEqual(search.abstract_from_index({'world': [1], 'hello': [0], 'again': [2]}), 'hello world again')
        self.assertEqual(search.abstract_from_index(None), '')


class CitationFilterTest(unittest.TestCase):
    def test_rate(self):
        self.assertEqual(search.citations_per_year(30, 2016, 2026), 3.0)
        self.assertEqual(search.citations_per_year(5, 2026, 2026), 5.0)  # at least one year
        self.assertEqual(search.citations_per_year(5, None, 2026), 0.0)

    def test_threshold_and_exemption(self):
        self.assertTrue(search.passes_citation_filter(30, 2016, 2026, 3, 2026))
        self.assertFalse(search.passes_citation_filter(29, 2016, 2026, 3, 2026))
        self.assertTrue(search.passes_citation_filter(0, 2026, 2026, 3, 2026))
        self.assertFalse(search.passes_citation_filter(2, 2025, 2026, 3, 2026))


class MergeTest(unittest.TestCase):
    def test_doi_arxiv_and_title(self):
        hits = [hit(doi='10.1/a', title='A study of fitness tracker privacy policies'),
                hit(source='Semantic Scholar', doi='10.1/a', arxiv='2101.00001', title='Other spelling'),
                hit(arxiv='2101.00001', doi='10.48550/arxiv.2101.00001', title='Preprint title'),
                hit(doi='10.1/b', title='A STUDY of fitness-tracker privacy policies!', year=2021),
                hit(doi='10.1/c', title='A study of fitness tracker privacy policies', year=2024),
                hit(title='Privacy', year=2020), hit(title='Privacy', year=2020)]
        sizes = sorted(len(g) for g in search.merge(hits))
        self.assertEqual(sizes, [1, 1, 1, 4])  # same title three years apart and short titles stay apart

    def test_record_prefers_published_doi_and_max_citations(self):
        group = [hit(doi='10.48550/arxiv.1', citations=40, year=2022, title='T', authors=['A']),
                 hit(source='Semantic Scholar', doi='10.1/pub', citations=55, year=2023, title='T', abstract='long text')]
        r = search.record(group, 2026, 3, 2026)
        self.assertEqual(r['doi'], '10.1/pub')
        self.assertEqual(r['other_dois'], '10.48550/arxiv.1')
        self.assertEqual(r['citations'], 55)
        self.assertEqual(r['abstract'], 'long text')
        self.assertTrue(r['passes_citation_filter'])
        self.assertEqual(r['first_author'], 'A')


if __name__ == '__main__':
    unittest.main()
