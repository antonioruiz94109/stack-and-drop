#!/usr/bin/env python3
"""Read-only discovery and source-change monitor. Never writes shoes.json."""
from release_watch import review as review_release_holds
from completion_watch import sources as completion_sources, review as review_completion
import argparse, concurrent.futures, datetime as dt, hashlib, json, re, urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit

BRANDS = {
 'Altra': ['https://www.altrarunning.com/en-us/collections/mens-new-arrivals', 'https://www.altrarunning.com/en-us/collections/womens-new-arrivals'],
 'New Balance': ['https://www.newbalance.com/men/shoes/running/', 'https://www.newbalance.com/women/shoes/running/'],
 'Topo Athletic': ['https://www.topoathletic.com/men/mens-shoes/promo/New-Arrival', 'https://www.topoathletic.com/women/womens-shoes/promo/New-Arrival'],
 'ASICS': ['https://www.asics.com/us/en-us/mens-running-shoes/c/aa10201000/', 'https://www.asics.com/us/en-us/womens-running-shoes/c/aa20201000/'],
 'Brooks': ['https://www.brooksrunning.com/en_us/mens/shoes/', 'https://www.brooksrunning.com/en_us/womens/shoes/'],
 'HOKA': ['https://www.hoka.com/en/us/mens-running/', 'https://www.hoka.com/en/us/womens-running/'],
 'Nike': ['https://www.nike.com/w/mens-running-shoes-37v7jznik1zy7ok', 'https://www.nike.com/w/womens-running-shoes-37v7jz5e1x6zy7ok'],
 'PUMA': ['https://us.puma.com/us/en/men/shoes/running', 'https://us.puma.com/us/en/women/shoes/running'],
 'Saucony': ['https://www.saucony.com/en/mens-running/', 'https://www.saucony.com/en/womens-running/'],
 'adidas': ['https://www.adidas.com/us/men-running-shoes', 'https://www.adidas.com/us/women-running-shoes'],
}
class Page(HTMLParser):
 def __init__(self):
  super().__init__(); self.skip=0; self.parts=[]; self.links=[]; self.href=None; self.label=[]
 def handle_starttag(self, tag, attrs):
  a=dict(attrs)
  if tag in ('script','style','noscript'): self.skip+=1
  if tag=='a': self.href=a.get('href'); self.label=[]
 def handle_endtag(self,tag):
  if tag in ('script','style','noscript'): self.skip=max(0,self.skip-1)
  if tag=='a' and self.href: self.links.append((self.href,' '.join(self.label)));self.href=None
 def handle_data(self,s):
  if not self.skip:
   self.parts.append(s)
   if self.href: self.label.append(s.strip())

def canonical(url):
 p=urlsplit(url);return urlunsplit((p.scheme,p.netloc,p.path.rstrip('/'),'',''))
def identity(url):
 p=urlsplit(url).path.lower()
 if '/pd/' in p: return p.split('/pd/')[1].split('/')[0] # model, not color/size SKU
 return re.sub(r'-al0[a-z0-9]+$','',p.split('/')[-1])
def product_link(brand,path):
 patterns={
  'Altra':r'/products/(?:mens|womens)-', 'New Balance':r'/pd/',
  'Topo Athletic':r'^/(?:mens|womens)-', 'Nike':r'^/t/',
  'ASICS':r'/p/[^/]+\.html$', 'Brooks':r'/shoes/.+\.html$',
  'HOKA':r'/[^/]+/\d+[^/]*\.html$', 'PUMA':r'/pd/[^/]+/\d+',
  'Saucony':r'/[^/]+/\d+[^/]*\.html$', 'adidas':r'/[^/]+/[A-Z0-9]+\.html$'}
 return bool(re.search(patterns[brand],path,re.I))

def fetch(url):
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'CadenceIndexCatalogChecker/1.0 (+https://github.com/antonioruiz94109/CadenceIndex)'})
  with urllib.request.urlopen(req,timeout=25) as r:
   body=r.read(20_000_001)
   if len(body)>20_000_000: raise ValueError('page exceeds 20 MB limit')
   page=Page();page.feed(body.decode('utf-8','replace'));text=re.sub(r'\s+',' ',' '.join(page.parts)).strip()
   if len(text)<300 or re.search(r'access denied|verify you are human|just a moment',text[:700],re.I): raise ValueError('blocked or incomplete page')
   return {'ok':True,'url':r.url,'text':text,'links':page.links}
 except Exception as e: return {'ok':False,'error':str(e)[:250]}

def evidence(text):
 # Focus on labelled specifications; never treat scraped values as verified changes.
 patterns=[r'heel[ -]to[ -]toe(?: drop)?\s*:?\s*\d+(?:\.\d+)?\s*mm',r'(?:stack height|weight|midsole|support|footshape[^:]{0,12})\s*:\s*.{1,100}']
 return sorted(set(m.group(0).strip() for p in patterns for m in re.finditer(p,text,re.I)))[:20]
def date_bounds(value):
 try:
  if len(value)==4: return dt.date(int(value),1,1),dt.date(int(value),12,31)
  if len(value)==7:
   import calendar
   y,m=map(int,value.split('-'));return dt.date(y,m,1),dt.date(y,m,calendar.monthrange(y,m)[1])
  d=dt.date.fromisoformat(value);return d,d
 except (ValueError,TypeError): return None

def run(catalog,previous,output):
 today=dt.datetime.now(dt.timezone.utc).date();cutoff=today.replace(year=today.year-2,day=min(today.day,28)) if today.month==2 and today.day==29 else today.replace(year=today.year-2)
 shoes=[s for s in json.loads(Path(catalog).read_text())['shoes'] if s['brand'] in BRANDS]
 previous_path=Path(previous)
 if not previous_path.exists(): previous_path=Path(__file__).with_name('catalog-baseline.json')
 old=json.loads(previous_path.read_text()) if previous_path.exists() else {'sources':{},'candidates':[]}
 urls=sorted(set([u for s in shoes for u in completion_sources(s)]+[s['source_url'] for s in shoes]+[u for us in BRANDS.values() for u in us]))
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: pages=dict(zip(urls,pool.map(fetch,urls)))
 snapshot={'checked_at':str(today),'sources':dict(old.get('sources',{})),'candidates':[]}; problems=[];changes=[];baseline=[];age=[];candidates={}
 for s in shoes:
  u=s['source_url'];p=pages[u];key=s['id']
  if not p['ok']: problems.append(f"{s['brand']} {s['model']} ({s['gender']}): {p['error']} — {u}");continue
  ev=evidence(p['text']);prior=old.get('sources',{}).get(key)
  if not ev: problems.append(f"{key}: no labelled specs extracted; manual source check required — {u}");continue
  current={'url':u,'evidence':ev,'checked_at':str(today)};snapshot['sources'][key]=current
  if prior and prior['evidence']!=ev:changes.append({'id':key,'url':u,'before':prior['evidence'],'after':ev})
  elif not prior:baseline.append({'id':key,'url':u,'evidence':ev,'catalog':{k:s.get(k) for k in ['drop_mm','weight_oz','stack_heel_mm','stack_forefoot_mm','foam','manufacturer_support']}})
 for s in shoes:
  bounds=date_bounds(s.get('release_date',''))
  if not bounds:age.append(f"{s['id']}: release evidence missing or invalid; advisory only, not an automatic exclusion")
  elif bounds[1]<cutoff:age.append(f"{s['id']}: outside preferred two-year window ({s['release_date']})")
  elif bounds[0]<cutoff+dt.timedelta(days=60):age.append(f"{s['id']}: near or straddling cutoff ({s['release_date']}); review precision")
 for brand,listing_urls in BRANDS.items():
  known={identity(s['source_url']) for s in shoes if s['brand']==brand}
  known.update(identity(pages[s['source_url']]['url']) for s in shoes if s['brand']==brand and pages[s['source_url']]['ok'])
  for u in listing_urls:
   p=pages[u]
   if not p['ok']:problems.append(f"Discovery {brand}: {p['error']} — {u}");continue
   found=0
   for href,label in p['links']:
    link=canonical(urljoin(u,href));path=urlsplit(link).path
    if urlsplit(link).netloc!=urlsplit(u).netloc:continue
    valid=product_link(brand,path)
    if not valid:continue
    found+=1;key=brand+'|'+identity(link)
    if identity(link) not in known:candidates.setdefault(key,{'brand':brand,'url':link,'label':label[:160] or identity(link),'status':'Unverified candidate: confirm running shoe, gender, model identity, sources and duplicates. Release recency is advisory.'})
   if not found:problems.append(f"Discovery {brand}: zero product links extracted (possibly JavaScript-only); coverage incomplete — {u}")
 snapshot['candidates']=sorted(candidates);prior_candidates=set(old.get('candidates',[]));new=[v for k,v in sorted(candidates.items()) if k not in prior_candidates]
 coverage={}
 for brand,listing_urls in BRANDS.items():
  entries=[s for s in shoes if s['brand']==brand]
  coverage[brand]={'entries':len(entries),'pages_fetched':sum(pages[s['source_url']]['ok'] for s in entries),'specs_extracted':sum(pages[s['source_url']]['ok'] and bool(evidence(pages[s['source_url']]['text'])) for s in entries),'discovery_pages_fetched':sum(pages[u]['ok'] for u in listing_urls),'discovery_pages':len(listing_urls),'pending_candidates':sum(v['brand']==brand for v in candidates.values())}
 report={'checked_at':str(today),'brand_coverage':coverage,'comparison_baseline':old.get('checked_at','none'),'scope':{b:sum(s['brand']==b for s in shoes) for b in BRANDS},'source_checks':len(shoes),'successful_fetches':sum(pages[s['source_url']]['ok'] for s in shoes),'new_candidates':new,'pending_candidates':list(candidates.values()),'possible_spec_changes':changes,'initial_baselines':baseline,'age_flags':age,'coverage_problems':problems}
 completion,completion_state=review_completion(shoes,old,pages,str(today))
 report['data_completion']=completion;snapshot['completion_watch']=completion_state
 held_review,held_snapshot=review_release_holds(shoes,old,fetch)
 snapshot['release_watch']=held_snapshot;report['held_release_review']=held_review
 out=Path(output);out.mkdir(parents=True,exist_ok=True);(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');(out/'snapshot.json').write_text(json.dumps(snapshot,indent=2)+'\n')
 lines=['# CadenceIndex weekly review — '+str(today),'','REPORT ONLY. No catalog edits, commits or publication. Candidates are not verified releases.','',f"Scope: {len(shoes)} existing entries; {len(new)} newly observed candidate links; {len(changes)} possible spec changes; {len(problems)} coverage problems.",'','First successful checks establish a baseline; they do not prove existing specs match. Blocked pages are unknown, never unchanged or discontinued. New colors/widths can still require manual deduplication.','']
 lines+=['## Coverage by brand','','Brand | Entries | Pages fetched | Specs extracted | Discovery pages fetched | Pending candidates','--- | ---: | ---: | ---: | ---: | ---:']
 for brand,c in coverage.items(): lines.append(f"{brand} | {c['entries']} | {c['pages_fetched']} | {c['specs_extracted']} | {c['discovery_pages_fetched']}/{c['discovery_pages']} | {c['pending_candidates']}")
 lines+=['']
 for title,items in [('Candidates requiring verification',[f"{v['brand']}: [{v['label'].replace('[','').replace(']','')}]({v['url']})" for v in candidates.values()]),('Possible specification changes',[f"{v['id']}: {v['url']}\n  - Before: {'; '.join(v['before'])}\n  - After: {'; '.join(v['after'])}" for v in changes]),('Release age review',age),('Coverage problems',problems),('Initial source baselines',[f"{v['id']}: {'; '.join(v['evidence'])}" for v in baseline])]:
  lines+=['## '+title,'']+(['- '+s for s in items] or ['None.'])+['']
 lines+=['## Prices and missing details','',completion['policy'],'', 'Missing fields: '+json.dumps(completion['missing_counts']), 'Full existing values, evidence excerpts, failures and follow-up queries for every entry are in report.json.','']
 for row in completion['entries']:
  statuses=[x['status'] for x in row['sources']]
  if row['missing_fields'] or any(x!='unchanged_excerpt' for x in statuses):
   lines.append('- '+row['id']+': missing '+(', '.join(row['missing_fields']) or 'none')+'; sources '+', '.join(statuses))
 lines+=['']
 lines+=['## Held release evidence watch','', 'Known sources only; not an exhaustive web search. Unpublished entries require source and identity review. Missing release dates alone do not block reliable running shoes. A new date or changed text is not automatic clearance.','']
 for h in held_review:
  lines += [f"- {h['brand']} {h['model']} ({h['gender']}): {h['missing_evidence']}",'  - Follow-up search: '+h['research_query']]
  for source in h['sources']:
   lines.append(f"  - {source['status']}: {source['url']}")
 lines+=['Full excerpts and fetch failures are in report.json.','']
 lines+=['Review policy: verify manufacturer specifications, gender/reference size and duplicates before publication under standing approval. Two years is a preference, not a hard cutoff; reliable running shoes may have unknown release dates. Never infer release date from discovery date. Check report.json for catalog values alongside initial source evidence.','Coverage is limited to the configured listing pages; pagination and JavaScript-only listings may hide products. Missing results are not proof that no new shoes exist.']
 (out/'report.md').write_text('\n'.join(lines)+'\n');print(json.dumps({k:v for k,v in report.items() if k in ['scope','source_checks','successful_fetches']}));print(f'Candidates {len(new)}; possible changes {len(changes)}; coverage problems {len(problems)}')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--catalog',default='shoes.json');p.add_argument('--previous',default='.checker-state/snapshot.json');p.add_argument('--output',default='checker-report');a=p.parse_args();run(a.catalog,a.previous,a.output)
