import sys, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import lit  # noqa: E402

CONFIG = lit.load_config()


class BooleanTest(unittest.TestCase):
    def test_truncation_and_hyphens(self):
        self.assertEqual(lit.group_match(CONFIG, 'D', 'A study of M-Health tools'), ['m-health'])
        self.assertEqual(lit.group_match(CONFIG, 'D', 'Studying mhealth'), ['mhealth'])
        self.assertIn('fitness track*', lit.group_match(CONFIG, 'D', 'Fitness Tracking Social Networks'))
        self.assertIn('privacy polic*', lit.group_match(CONFIG, 'T', 'privacy policies of apps'))

    def test_word_boundaries(self):
        self.assertEqual(lit.group_match(CONFIG, 'L', 'a llama-based model'), ['llama'])
        self.assertEqual(lit.group_match(CONFIG, 'L', 'a cellmate'), [])
        self.assertEqual(lit.group_match(CONFIG, 'F', 'a new framework'), [])

    def test_strands(self):
        title = 'Exploring Privacy Practices of Female mHealth Apps in a Post-Roe World'
        self.assertTrue(lit.rule_match(CONFIG, 'D&P', title))
        self.assertFalse(lit.strand_match(CONFIG, 'S1', title))
        self.assertTrue(lit.strand_match(CONFIG, 'S1', 'Inference attacks on fitness trackers threaten privacy'))
        self.assertTrue(lit.strand_match(CONFIG, 'S3', 'Using large language models to annotate privacy policies'))
        self.assertTrue(lit.strand_match(CONFIG, 'S4', 'Vague words in privacy policies'))

    def test_translations(self):
        self.assertIn('"health app*"[tiab]', lit.pubmed_query(CONFIG, 'S1'))
        self.assertEqual(lit.arxiv_term('privacy polic*'), 'ti:"privacy polic" OR abs:"privacy polic"')
        self.assertEqual(lit.arxiv_term('wearable*'), 'ti:wearable* OR abs:wearable*')
        self.assertIn('"Abstract":"privacy polic*"', lit.ieee_query(CONFIG, 'S3'))

    def test_ids(self):
        self.assertEqual(lit.norm_doi('https://doi.org/10.1145/ABC'), '10.1145/abc')
        self.assertEqual(lit.arxiv_id('http://arxiv.org/abs/2509.08825v2'), '2509.08825')


if __name__ == '__main__':
    unittest.main()
