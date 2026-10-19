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

class ExpandedBrandsTests(unittest.TestCase):
 def test_all_ten_brands_and_product_routes(self):
  examples={'Altra':'/en-us/products/mens-test-al0a123','New Balance':'/pd/rebel-v5/MFCX.html','Topo Athletic':'/mens-specter','Nike':'/t/pegasus/ABC-001','ASICS':'/us/en-us/novablast/p/ANA_123.html','Brooks':'/en_us/mens/shoes/road-running-shoes/ghost/110.html','HOKA':'/en/us/mens-running/clifton/1162030.html','PUMA':'/us/en/pd/velocity/311140','Saucony':'/en/ride/59943M.html','adidas':'/us/supernova/IH2504.html'}
  self.assertEqual(set(c.BRANDS),set(examples))
  for brand,path in examples.items():
   self.assertTrue(c.product_link(brand,path),brand)
   self.assertFalse(c.product_link(brand,'/account/login'),brand)
