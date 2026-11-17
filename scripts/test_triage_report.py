"""ChatGPT-authored acceptance tests; temporary inputs, no catalog mutations."""
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).with_name('triage_report.py')


class IdentityAcceptance(unittest.TestCase):
    def run_case(self, entries, specs=(), candidates=()):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            report = {'source_checks': len(entries), 'successful_fetches': 0,
                      'brand_coverage': {}, 'coverage_problems': [],
                      'new_candidates': list(candidates),
                      'possible_spec_changes': [{'id': x, 'url': '', 'before': [], 'after': []} for x in specs]}
            (root/'report.json').write_text(json.dumps(report))
            (root/'catalog.json').write_text(json.dumps({'shoes': entries}))
            cmd = [sys.executable, str(SCRIPT), '--report', str(root/'report.json'),
                   '--catalog', str(root/'catalog.json'), '--output', str(root/'result.json')]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            return json.loads((root/'result.json').read_text())

    def entries(self):
        return [
            {'id': 'pegasus-42-men', 'brand': 'Nike', 'model': 'Pegasus 42', 'gender': 'men', 'weight_oz': 10.59},
            {'id': 'pegasus-42-women', 'brand': 'Nike', 'model': 'Pegasus 42', 'gender': 'women', 'weight_oz': 8.6},
            {'id': 'pegasus-41-men', 'brand': 'Nike', 'model': 'Pegasus 41', 'gender': 'men', 'weight_oz': 9.9},
            {'id': 'pegasus-42-gtx-men', 'brand': 'Nike', 'model': 'Pegasus 42 GTX', 'gender': 'men', 'weight_oz': 11.7}]

    def test_exact_identity_retains_gender_generation_and_variant(self):
        entries = self.entries()
        res = self.run_case(entries, specs=[e['id'] for e in entries])
        for expected, result in zip(entries, res['possible_spec_changes']):
            self.assertEqual(result['catalog_entry_raw'], expected)

    def test_unknown_id_is_hold(self):
        res = self.run_case(self.entries(), specs=['pegasus-42', 'pegasus-420-men', 'missing'])
        for result in res['possible_spec_changes']:
            self.assertTrue(result['verdict'].startswith('HOLD'))
            self.assertIsNone(result.get('catalog_entry_raw'))

    def test_ambiguous_duplicate_id_is_hold(self):
        entries = self.entries()
        entries.append(dict(entries[0], gender='women', weight_oz=7.0))
        result = self.run_case(entries, specs=['pegasus-42-men'])['possible_spec_changes'][0]
        self.assertTrue(result['verdict'].startswith('HOLD'))
        self.assertIsNone(result.get('catalog_entry_raw'))

    def test_candidate_name_and_slug_never_clear_identity(self):
        candidates = [{'brand': 'Nike', 'label': 'Pegasus 42', 'url': 'https://example.invalid/pegasus-42-womens'}]
        result = self.run_case(self.entries(), candidates=candidates)['new_candidates_triage'][0]
        self.assertTrue(result['verdict'].startswith('HOLD'))

    def test_spikes_stay_excluded(self):
        candidates = [{'brand': 'Nike', 'label': 'Sprint spikes', 'url': ''}]
        result = self.run_case(self.entries(), candidates=candidates)['new_candidates_triage'][0]
        self.assertTrue(result['verdict'].startswith('EXCLUDE'))

    def test_candidate_ambiguous_id_is_hold(self):
        entries = self.entries()
        entries.append(dict(entries[0], gender='women'))
        result = self.run_case(entries, candidates=[{'id': entries[0]['id']}])['new_candidates_triage'][0]
        self.assertTrue(result['verdict'].startswith('HOLD'))

    def test_missing_spec_id_never_matches_missing_catalog_id(self):
        result = self.run_case([{'brand': 'Nike', 'model': 'Unknown'}], specs=[''])['possible_spec_changes'][0]
        self.assertTrue(result['verdict'].startswith('HOLD'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
