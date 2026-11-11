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

class ReleaseHoldTests(unittest.TestCase):
 def test_hold_baseline_changes_failures_and_published_skip(self):
  from release_watch import review
  with tempfile.TemporaryDirectory() as tmp:
   path=Path(tmp)/'holds.json';path.write_text(json.dumps([dict(candidate_id=1,brand='Nike',model='Test GTX',gender='women',url='https://example.com/shoe',supporting_sources=[],release_notes='Original launch unknown')]))
   page={'ok':True,'text':'Test GTX release date January 2026'}
   rows,state=review([],{},lambda u:page,path)
   self.assertEqual(rows[0]['status'],'hold_pending_human_verification')
   self.assertEqual(rows[0]['sources'][0]['status'],'baseline_for_review')
   rows,unchanged=review([],{'release_watch':state},lambda u:page,path)
   self.assertEqual(rows[0]['sources'][0]['status'],'unchanged')
   rows,_=review([],{'release_watch':state},lambda u:{'ok':True,'text':'Test GTX new color June 2026'},path)
   self.assertEqual(rows[0]['sources'][0]['status'],'changed_for_review')
   rows,preserved=review([],{'release_watch':state},lambda u:{'ok':False,'error':'403'},path)
   self.assertEqual(preserved,state);self.assertEqual(rows[0]['sources'][0]['status'],'unavailable')
   rows,_=review([dict(brand='Nike',model='Test GTX',gender='women')],{},lambda u:page,path)
   self.assertEqual(rows,[])

class CompletionTests(unittest.TestCase):
 def test_prices_missing_details_and_failed_baseline(self):
  from completion_watch import review, sources
  shoe=dict(id='test',brand='Nike',model='Test',gender='women',source_url='https://www.nike.com/t/test',price_usd=150,completion_review={'sources':[{'url':'https://www.nike.com/t/price'},{'url':'https://evil.test/price'}]})
  urls=sources(shoe);self.assertEqual(len(urls),2)
  pages={u:dict(ok=True,url=u,text='Test women Regular $150 Sale $120 Weight: 8 oz Midsole: foam') for u in urls}
  report,state=review([shoe],{},pages,'2026-10-19');self.assertEqual(report['missing_counts']['price_usd'],0);self.assertEqual(report['missing_counts']['stack_heel_mm'],1)
  self.assertEqual(report['entries'][0]['sources'][0]['status'],'baseline_for_review')
  pages={u:dict(ok=True,url=u,text='Test women Regular $160 Sale $130 Weight: 8 oz Midsole: foam') for u in urls}
  report,new=review([shoe],{'completion_watch':state},pages,'2026-10-26');self.assertEqual(report['entries'][0]['sources'][0]['status'],'changed_for_review')
  for p in pages.values():p.update(ok=False,error='403')
  report,preserved=review([shoe],{'completion_watch':new},pages,'2026-11-02');self.assertEqual(preserved,new);self.assertEqual(report['entries'][0]['sources'][0]['status'],'unavailable')
  for p in pages.values():p.update(ok=True,text='Please enable JavaScript')
  report,preserved=review([shoe],{'completion_watch':new},pages,'2026-11-02');self.assertEqual(preserved,new);self.assertEqual(report['entries'][0]['sources'][0]['status'],'no_evidence')
  self.assertEqual(shoe['price_usd'],150)

class StructuredDetailsTests(unittest.TestCase):
 def page(self, url, details):
  p=c.Page(); data={'props':{'pageProps':{'selectedProduct':{'productInfo':{'canonicalUrl':url,'productDetails':[{'body':details}]}}}}}
  p.feed('<script id="__NEXT_DATA__" type="application/json">'+json.dumps(data)+'</script>')
  return p
 def test_selected_product_only_and_labels(self):
  u='https://www.nike.com/t/vomero-premium-mens-shoes-abc'
  p=self.page(u,['Weight: Approx. 351g/12.4 oz (Men’s US 10)','Heel-to-toe drop: 10 mm'])
  rows=c.structured_details(p,u)
  self.assertEqual(len(rows),2); self.assertTrue(c.evidence(' '.join(rows)))
  self.assertEqual(c.structured_details(p,'https://www.nike.com/t/womens-shoes-xyz/SKU'),[])
  self.assertEqual(c.structured_details(p,'https://other.example/t/vomero-premium-mens-shoes-abc'),[])
 def test_malformed_json_ignored(self):
  p=c.Page();p.feed('<script id="__NEXT_DATA__">bad</script>Weight: 8 oz')
  self.assertEqual(c.structured_details(p,'https://www.nike.com/t/test'),[])
 def test_no_details_not_fabricated(self):
  p=self.page('https://www.nike.com/t/test',[])
  self.assertEqual(c.structured_details(p,'https://www.nike.com/t/test/SKU'),[])

class CoverageStatusTests(unittest.TestCase):
 def test_unavailable_and_partial_not_green(self):
  d={'HOKA':dict(entries=16,pages_fetched=0,specs_extracted=0,discovery_pages_fetched=0,discovery_pages=2), 'Nike':dict(entries=2,pages_fetched=2,specs_extracted=1,discovery_pages_fetched=2,discovery_pages=2)}
  self.assertEqual(c.coverage_summary(d,['failure']),'incomplete')
  self.assertEqual(d['HOKA']['status'],'unavailable');self.assertEqual(d['Nike']['status'],'incomplete')
 def test_empty_listing_is_incomplete(self):
  d={'Nike':dict(entries=1,pages_fetched=1,specs_extracted=1,discovery_pages_fetched=2,discovery_pages=2)}
  self.assertEqual(c.coverage_summary(d,['Discovery Nike: zero product links extracted']),'incomplete')
  self.assertEqual(d['Nike']['status'],'incomplete')

class ExactSourceTests(unittest.TestCase):
 def test_exact_sku_only(self):
  u='https://www.nike.com/t/test'
  p=StructuredDetailsTests().page(u,['Weight: 1 oz'])
  p.next_data['props']['pageProps']['productGroups']=[{'products':{'A-001':{'productInfo':{'canonicalUrl':u,'productDetails':[{'body':['Weight: 12 oz']}]}}}}]
  self.assertEqual(c.structured_details(p,u+'/A-001'),['Weight: 12 oz'])
  self.assertEqual(c.structured_details(p,u+'/B-002'),[])
 def test_announcements_separate_and_official(self):
  pages={u:{'ok':True,'links':[]} for u in c.ANNOUNCEMENTS.values()}
  pages[c.ANNOUNCEMENTS['ASICS']]['links']=[('/en/press/article/new-shoe','New shoe'),('/en/press/article/new-shoe',''),('https://other.test/en/press/article/fake','Fake')]
  rows=c.announcement_watch(pages)
  self.assertEqual(len(rows[0]['links']),1)
  self.assertEqual(rows[0]['links'][0]['label'],'New shoe')
  self.assertEqual(rows[1]['status'],'unavailable_or_empty')

class RedirectIdentityTests(unittest.TestCase):
 def test_redirect_does_not_substitute_structured_product(self):
  p=StructuredDetailsTests().page('https://www.nike.com/t/other',['Weight: 99 oz'])
  body=('<script id="__NEXT_DATA__">'+json.dumps(p.next_data)+'</script>'+('Normal product page. '*30)).encode()
  from unittest.mock import MagicMock
  response=MagicMock();response.__enter__.return_value=response;response.read.return_value=body
  response.url='https://www.nike.com/t/other'
  with patch.object(c.urllib.request,'urlopen',return_value=response):
   result=c.fetch('https://www.nike.com/t/requested/SKU')
  self.assertTrue(result['ok']);self.assertEqual(result['structured_details'],[])
