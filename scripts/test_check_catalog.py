import unittest,tempfile,json
from pathlib import Path
from unittest.mock import patch
import check_catalog as c
class CheckerTests(unittest.TestCase):
 def test_precision_and_identity(self):
  self.assertEqual(str(c.date_bounds('2024-10')[1]),'2024-10-31')
  self.assertEqual(str(c.date_bounds('2025')[0]),'2025-01-01')
  self.assertEqual(c.identity('https://www.newbalance.com/pd/rebel-v5/RED-09.html'),c.identity('https://www.newbalance.com/pd/rebel-v5/BLUE-10.html'))
 def test_review_only_changes_and_failure_preserve_baseline(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp);cat=p/'shoes.json';prior=p/'prior.json'
   shoe={'id':'test','brand':'Altra','model':'Test','gender':'women','source_url':'https://www.altrarunning.com/en-us/products/test','release_date':'2025'}
   cat.write_text(json.dumps({'shoes':[shoe]}));before=cat.read_bytes()
   prior.write_text(json.dumps({'sources':{'test':{'evidence':['Weight: 8 oz']}},'candidates':[]}))
   page={'ok':True,'url':shoe['source_url'],'text':'Weight: 9 oz','links':[]}
   with patch.object(c,'fetch',return_value=page):c.run(cat,prior,p/'out')
   report=json.loads((p/'out/report.json').read_text());self.assertEqual(len(report['possible_spec_changes']),1);self.assertEqual(cat.read_bytes(),before)
   with patch.object(c,'fetch',return_value={'ok':False,'error':'HTTP 403'}):c.run(cat,prior,p/'blocked')
   snapshot=json.loads((p/'blocked/snapshot.json').read_text());self.assertEqual(snapshot['sources']['test']['evidence'],['Weight: 8 oz'])
   self.assertTrue(json.loads((p/'blocked/report.json').read_text())['coverage_problems'])
if __name__=='__main__':unittest.main()
