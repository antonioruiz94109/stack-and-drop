#!/usr/bin/env python3
"""Read-only discovery and source-change monitor. Never writes shoes.json."""
import argparse, concurrent.futures, datetime as dt, hashlib, json, re, urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit

BRANDS = {
 'Altra': ['https://www.altrarunning.com/en-us/collections/mens-new-arrivals', 'https://www.altrarunning.com/en-us/collections/womens-new-arrivals'],
 'New Balance': ['https://www.newbalance.com/men/shoes/running/', 'https://www.newbalance.com/women/shoes/running/'],
 'Topo Athletic': ['https://www.topoathletic.com/men/mens-shoes/promo/New-Arrival', 'https://www.topoathletic.com/women/womens-shoes/promo/New-Arrival'],
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
 urls=sorted(set([s['source_url'] for s in shoes]+[u for us in BRANDS.values() for u in us]))
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
  if not bounds:age.append(f"{s['id']}: release evidence missing or invalid; review required")
  elif bounds[1]<cutoff:age.append(f"{s['id']}: outside rolling two-year window ({s['release_date']})")
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
    valid=(bool(re.search(r'/products/(mens|womens)-',path)) if brand=='Altra' else '/pd/' in path if brand=='New Balance' else bool(re.match(r'^/(mens|womens)-',path)))
    if not valid:continue
    found+=1;key=brand+'|'+identity(link)
    if identity(link) not in known:candidates.setdefault(key,{'brand':brand,'url':link,'label':label[:160] or identity(link),'status':'Unverified candidate: confirm running shoe, gender, model identity and release within two years.'})
   if not found:problems.append(f"Discovery {brand}: zero product links extracted (possibly JavaScript-only); coverage incomplete — {u}")
 snapshot['candidates']=sorted(candidates);prior_candidates=set(old.get('candidates',[]));new=[v for k,v in sorted(candidates.items()) if k not in prior_candidates]
 report={'checked_at':str(today),'comparison_baseline':old.get('checked_at','none'),'scope':{b:sum(s['brand']==b for s in shoes) for b in BRANDS},'source_checks':len(shoes),'successful_fetches':sum(pages[s['source_url']]['ok'] for s in shoes),'new_candidates':new,'pending_candidates':list(candidates.values()),'possible_spec_changes':changes,'initial_baselines':baseline,'age_flags':age,'coverage_problems':problems}
 out=Path(output);out.mkdir(parents=True,exist_ok=True);(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');(out/'snapshot.json').write_text(json.dumps(snapshot,indent=2)+'\n')
 lines=['# CadenceIndex weekly review — '+str(today),'','REPORT ONLY. No catalog edits, commits or publication. Candidates are not verified releases.','',f"Scope: {len(shoes)} existing entries; {len(new)} newly observed candidate models/versions; {len(changes)} possible spec changes; {len(problems)} coverage problems.",'','First successful checks establish a baseline; they do not prove existing specs match. Blocked pages are unknown, never unchanged or discontinued. New colors/widths can still require manual deduplication.','']
 for title,items in [('Candidates requiring verification',[f"{v['brand']}: [{v['label'].replace('[','').replace(']','')}]({v['url']})" for v in candidates.values()]),('Possible specification changes',[f"{v['id']}: {v['url']}\n  - Before: {'; '.join(v['before'])}\n  - After: {'; '.join(v['after'])}" for v in changes]),('Release age review',age),('Coverage problems',problems),('Initial source baselines',[f"{v['id']}: {'; '.join(v['evidence'])}" for v in baseline])]:
  lines+=['## '+title,'']+(['- '+s for s in items] or ['None.'])+['']
 lines+=['Review policy: confirm manufacturer specifications, gender/reference size, model-release evidence and duplicates before proposing a catalog change. Never infer release date from discovery date. Check report.json for catalog values alongside initial source evidence.','Coverage is limited to the configured listing pages; pagination and JavaScript-only listings may hide products. Missing results are not proof that no new shoes exist.']
 (out/'report.md').write_text('\n'.join(lines)+'\n');print(json.dumps({k:v for k,v in report.items() if k in ['scope','source_checks','successful_fetches']}));print(f'Candidates {len(new)}; possible changes {len(changes)}; coverage problems {len(problems)}')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--catalog',default='shoes.json');p.add_argument('--previous',default='.checker-state/snapshot.json');p.add_argument('--output',default='checker-report');a=p.parse_args();run(a.catalog,a.previous,a.output)
