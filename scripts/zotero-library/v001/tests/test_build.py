"""Unit tests: python -m unittest discover -s scripts/zotero-library/v001/tests"""
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_zotero_library as b   # noqa: E402

BIB = r'''% =====
%  banner
% =====

% First comment line
% second comment line
@article{doe2020first,
  author  = {Doe, Jane and van der Berg, Jan and {Org Name}},
  title   = {A {Nested} Title with
             a line break: R{\"o}ttger and Do{\u g}an --- \S~60d \& more},
  journal = {Journal of Tests},
  volume  = {3},
  number  = {2},
  pages   = {1--10},
  year    = {2020},
  doi     = {10.1/abc},
  note    = {Art.~4},
  articleno = {7}
}

@misc{roe2021arxiv,
  author       = {Roe, Richard},
  title        = {A Preprint},
  year         = {2021},
  howpublished = {arXiv preprint arXiv:2101.00001},
  doi          = {10.48550/arXiv.2101.00001}
}

@online{web2026page,
  author  = {{Web Org}},
  title   = {A Page},
  date    = {2026-09-29},
  url     = {https://example.org/page},
  urldate = {2026-11-01}
}

@software{prog2024tool,
  author  = {{JoMingyu}},
  title   = {tool},
  version = {1.2},
  year    = {2024}
}
'''

BBL = r'''\datalist[entry]{nyt/global//global/global/global}
  \entry{doe2020first}{article}{}{}
  \endentry
  \entry{roe2021arxiv}{misc}{}{}
  \endentry
  \entry{web2026page}{online}{}{}
  \endentry
'''
AUX = r'''\abx@aux@cite{0}{doe2020first}
\abx@aux@segm{0}{0}{doe2020first}
\abx@aux@cite{0}{roe2021arxiv}
\abx@aux@cite{0}{web2026page}
'''


class Parsing(unittest.TestCase):
    def setUp(self):
        self.entries = b.parse_bib(BIB)

    def test_entries_and_comments(self):
        self.assertEqual([e.key for e in self.entries], ['doe2020first', 'roe2021arxiv', 'web2026page', 'prog2024tool'])
        self.assertEqual(self.entries[0].comment, ['First comment line', 'second comment line'])
        self.assertEqual(self.entries[1].comment, [])   # the banner above is not a comment of the first entry

    def test_fields(self):
        e = self.entries[0]
        self.assertEqual(e.get('pages'), '1--10')
        self.assertIn('line break', e.get('title'))
        self.assertNotIn('\n', e.get('title'))

    def test_latex(self):
        self.assertEqual(b.latex_to_text(self.entries[0].get('title')),
                         'A Nested Title with a line break: Röttger and Doğan — § 60d & more')
        self.assertEqual(b.latex_to_text('Art.~4 1--10'), 'Art. 4 1–10')
        self.assertEqual(b.latex_to_text(r'{\ss}'), 'ß')

    def test_names(self):
        self.assertEqual(b.split_names(self.entries[0].get('author')),
                         [('Doe', 'Jane'), ('van der Berg', 'Jan'), ('Org Name', '')])
        self.assertEqual(b.split_names('Jane Q. Public'), [('Public', 'Jane Q.')])


class Numbers(unittest.TestCase):
    def setUp(self):
        self.entries = b.parse_bib(BIB)

    def test_numbers_follow_bbl(self):
        nums, msgs = b.reference_numbers(self.entries, BBL, AUX)
        self.assertEqual(nums, {'doe2020first': 1, 'roe2021arxiv': 2, 'web2026page': 3})
        self.assertEqual(msgs, [])   # agrees with a name-year-title sort

    def test_stale_bbl_is_refused(self):
        with self.assertRaises(ValueError):
            b.reference_numbers(self.entries, BBL, AUX + r'\abx@aux@cite{0}{prog2024tool}')

    def test_unknown_key_is_refused(self):
        with self.assertRaises(ValueError):
            b.reference_numbers(self.entries, BBL + r'\entry{ghost}{misc}{}{}', None)

    def test_disagreement_with_sort_is_reported_not_hidden(self):
        swapped = BBL.replace('doe2020first', 'TMP').replace('roe2021arxiv', 'doe2020first').replace('TMP', 'roe2021arxiv')
        nums, msgs = b.reference_numbers(self.entries, swapped, None)
        self.assertEqual(nums['roe2021arxiv'], 1)
        self.assertTrue(msgs)


class Pdfs(unittest.TestCase):
    FILES = ['Doe_2020_NestedTitleLineBreak.pdf', 'Doe_2020_NestedTitleLineBreak_supplement.pdf',
             'Doe_2019_SomethingElse.pdf', 'Roe_2021_Preprint_manuscript.pdf', 'Roe_2021_Preprint_published.pdf',
             'VanDerBerg_2020_Other.pdf', 'WebOrg_2026_Page_web-capture.pdf']

    def test_parse_name(self):
        info = b.parse_pdf_name('Roe_2021_Preprint_manuscript.pdf')
        self.assertEqual((info['author'], info['year'], info['suffix']), ('roe', 2021, 'manuscript'))
        self.assertEqual(b.parse_pdf_name('De_2016_PrivacyHarm-SmartGrids.pdf')['author'], 'de')

    def test_matching_and_order(self):
        entries = b.parse_bib(BIB)
        got = b.assign_pdfs(entries, self.FILES)
        self.assertEqual(got['doe2020first'], ['Doe_2020_NestedTitleLineBreak.pdf', 'Doe_2020_NestedTitleLineBreak_supplement.pdf'])
        self.assertEqual(got['roe2021arxiv'], ['Roe_2021_Preprint_published.pdf', 'Roe_2021_Preprint_manuscript.pdf'])
        self.assertEqual(got['prog2024tool'], [])

    def test_overrides_win_and_exclude_others(self):
        entries = b.parse_bib(BIB)
        got = b.assign_pdfs(entries, self.FILES, {'web2026page': ['Doe_2019_SomethingElse.pdf'],
                                                  'roe2021arxiv': ['-']})
        self.assertEqual(got['web2026page'], ['Doe_2019_SomethingElse.pdf'])
        self.assertEqual(got['roe2021arxiv'], [])


class Output(unittest.TestCase):
    def build(self, **kw):
        files = ['Doe_2020_NestedTitleLineBreak.pdf']
        return b.build(BIB, BBL, AUX, files, ({}, {}), {}, **kw)

    def setUp(self):
        self.rdf, self.report = self.build()
        self.root = ET.fromstring(self.rdf)
        self.ns = {'rdf': b.NS['rdf'], 'z': b.NS['z'], 'dc': b.NS['dc'], 'bib': b.NS['bib'], 'link': b.NS['link']}

    def item(self, key):
        return next(d for d in self.root.findall('rdf:Description', self.ns)
                    if d.get('{%s}about' % b.NS['rdf']) == f'#item_{key}')

    def test_well_formed_and_counts(self):
        self.assertEqual(len(self.root.findall('rdf:Description', self.ns)), 4)
        self.assertEqual(self.report['entries'], 4)
        self.assertEqual(self.report['cited'], 3)
        self.assertEqual(self.report['no_pdf'], ['roe2021arxiv', 'web2026page', 'prog2024tool'])

    def test_reference_number_columns(self):
        d = self.item('doe2020first')
        self.assertEqual(d.find('z:rights', self.ns).text, '[1]')
        self.assertEqual(d.find('z:callNumber', self.ns).text, '[1]')
        web = self.item('web2026page')   # web pages have no Call Number field in Zotero
        self.assertEqual(web.find('z:rights', self.ns).text, '[3]')
        self.assertIsNone(web.find('z:callNumber', self.ns))

    def test_uncited_entry_is_marked_not_numbered(self):
        d = self.item('prog2024tool')
        self.assertIsNone(d.find('z:rights', self.ns))
        self.assertIsNone(d.find('z:callNumber', self.ns))
        self.assertIn('thesis:uncited', [t.text for t in d.findall('dc:subject', self.ns)])
        self.assertIn('Thesis reference: not cited in the thesis', d.find('z:extra', self.ns).text)

    def test_attachment_is_a_relative_linked_file(self):
        att = self.root.find('z:Attachment', self.ns)
        self.assertEqual(att.find('rdf:resource', self.ns).get('{%s}resource' % b.NS['rdf']),
                         '../01_Literature/library/Doe_2020_NestedTitleLineBreak.pdf')
        self.assertEqual(att.find('z:linkMode', self.ns).text, '2')
        self.assertEqual(len(self.root.findall('z:Attachment', self.ns)), 1)   # entries without a PDF get none

    def test_fields_mapped(self):
        d = self.item('doe2020first')
        self.assertEqual(d.find('z:pages', self.ns).text, '1–10')
        self.assertEqual(d.find('z:DOI', self.ns).text, '10.1/abc')
        self.assertEqual(d.find('z:citationKey', self.ns).text, 'doe2020first')
        extra = d.find('z:extra', self.ns).text
        self.assertIn('BibTeX note: Art. 4', extra)        # no Zotero field: kept in Extra
        self.assertIn('BibTeX articleno: 7', extra)
        p = self.item('roe2021arxiv')
        self.assertEqual(p.find('z:itemType', self.ns).text, 'preprint')
        self.assertEqual(p.find('z:archiveID', self.ns).text, 'arXiv:2101.00001')
        w = self.item('web2026page')
        self.assertEqual(w.find('z:accessDate', self.ns).text, '2026-11-01 00:00:00')
        self.assertEqual(w.find('z:date', self.ns).text, '2026-09-29')

    def test_comment_becomes_note(self):
        d = self.item('doe2020first')
        note = d.find('dcterms:isReferencedBy', {**self.ns, 'dcterms': b.NS['dcterms']})
        self.assertIn('First comment line', note.find('bib:Memo/rdf:value', self.ns).text)

    def test_header_records_the_bib_hash_and_output_is_deterministic(self):
        self.assertIn('bib-sha256=' + b.bib_digest(BIB), self.rdf)
        self.assertEqual(self.rdf, self.build()[0])
        self.assertEqual(b.bib_digest(BIB), b.bib_digest(BIB.replace('\n', '\r\n')))   # same on Windows checkouts

    def test_no_numbers_without_bbl(self):
        rdf, report = b.build(BIB, None, None, [], ({}, {}), {})
        self.assertNotIn('<z:rights>', rdf)
        self.assertEqual(report['cited'], 0)


class RealBibliography(unittest.TestCase):
    def test_every_entry_converts_without_leftover_latex(self):
        entries = b.parse_bib(b.BIB.read_text(encoding='utf-8'))
        self.assertGreater(len(entries), 90)
        self.assertEqual(len({e.key for e in entries}), len(entries))
        for e in entries:
            for name, value in e.fields.items():
                text = b.latex_to_text(value)
                self.assertNotIn('\\', text, f'{e.key}.{name}')
                self.assertNotIn('{', text, f'{e.key}.{name}')


class SourceCheck(unittest.TestCase):
    def test_sources_scan_ignores_comments_and_reads_tables(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            thesis = Path(tmp)
            (thesis / 'chapters').mkdir()
            (thesis / 'tables').mkdir()
            (thesis / 'thesis.tex').write_text('\\parencite[p.~3]{a2020b, c2021d} % \\cite{hidden2020x}\n', encoding='utf-8')
            (thesis / 'chapters' / 'one.tex').write_text('\\textcite{e2022f}\n\\thesiscite{notakey}\n', encoding='utf-8')
            (thesis / 'tables' / 't.tex').write_text('\\citeauthor*{g2023h}\n', encoding='utf-8')
            self.assertEqual(b.source_citations(thesis), {'a2020b', 'c2021d', 'e2022f', 'g2023h'})

    def test_note_only_when_sources_and_last_compile_differ(self):
        self.assertIsNone(b.stale_note({'a': 1, 'b': 2}, {'a', 'b'}))
        self.assertIsNone(b.stale_note({'a': 1}, None))
        note = b.stale_note({'a': 1, 'b': 2}, {'a', 'c'})
        self.assertIn('b', note)
        self.assertIn('newly cited: c', note)


if __name__ == '__main__':
    unittest.main()
