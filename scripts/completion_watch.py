"""Read-only evidence watch. Excerpts are review leads, never verified values."""
import re
from urllib.parse import urlsplit
FIELDS = ('price_usd', 'weight_oz', 'drop_mm', 'stack_heel_mm', 'stack_forefoot_mm', 'foam', 'verdict', 'toe_box', 'manufacturer_support')
DOMAINS = {'Altra':'altrarunning.com','Topo Athletic':'topoathletic.com','New Balance':'newbalance.com','ASICS':'asics.com','Nike':'nike.com','Brooks':'brooksrunning.com','HOKA':'hoka.com','Saucony':'saucony.com','PUMA':'puma.com','adidas':'adidas.com'}
def official(url, brand):
 p=urlsplit(url);domain=DOMAINS.get(brand,'')
 return bool(domain and p.scheme=='https' and (p.hostname==domain or (p.hostname or '').endswith('.'+domain)))
def sources(shoe):
 urls=[shoe['source_url']]+[x['url'] for x in shoe.get('completion_review',{}).get('sources',[])]
 return sorted({u for u in urls if official(u,shoe['brand'])})
def missing(shoe):
 return [k for k in FIELDS if shoe.get(k) in (None,'') or (k=='verdict' and str(shoe.get(k,'')).startswith('See the manufacturer source'))]
def excerpts(text):
 patterns={'price':r'(?:US\s*\$|USD\s*\$?|\$)\s*\d+(?:[,.]\d+)*', 'details':r'\b(?:stack(?: height)?|heel.to.toe|drop|weight|midsole|foam|cushioning|toe.box|support)\b'}
 result={}
 for kind,pattern in patterns.items():
  matches=list(re.finditer(pattern,text,re.I));result[kind]=sorted({text[max(0,m.start()-90):m.end()+180].strip() for m in matches})[:40]
  result[kind+'_truncated']=len(matches)>40
 return result

def review(shoes, old, pages, checked_at):
 state=dict(old.get('completion_watch',{}));rows=[]
 for shoe in shoes:
  row={'id':shoe['id'],'brand':shoe['brand'],'model':shoe['model'],'gender':shoe['gender'],'missing_fields':missing(shoe),'catalog':{k:shoe.get(k) for k in FIELDS},'price_type':shoe.get('price_type'),'sources':[], 'research_query':f"{shoe['brand']} {shoe['model']} {shoe['gender']} manufacturer US price stack height midsole weight"}
  for url in sources(shoe):
   key=shoe['id']+'|'+url;p=pages[url];prior=state.get(key)
   item={'url':url}
   if not p['ok'] or not official(p.get('url',url),shoe['brand']):
    item.update(status='unavailable',error=p.get('error','Redirect outside manufacturer domain'))
   else:
    ev=excerpts(p['text'])
    if not ev['price'] and not ev['details']:
     item.update(status='no_evidence',note='Incomplete extraction; preserve previous successful evidence.')
    else:
     status='baseline_for_review' if not prior else ('changed_for_review' if ev!=prior['evidence'] else 'unchanged_excerpt')
     item.update(status=status,evidence=ev,resolved_url=p.get('url',url))
     if prior and status=='changed_for_review':item['before']=prior['evidence']
     state[key]={'evidence':ev,'checked_at':checked_at}
   row['sources'].append(item)
  rows.append(row)
 totals={k:sum(k in r['missing_fields'] for r in rows) for k in FIELDS}
 return {'missing_counts':totals,'entries':rows,'policy':'Excerpts may include sale prices, non-US currencies, other products or sizes. Verify exact model, gender, variant, currency and price basis against manufacturer before changing catalog. Unchanged excerpts do not prove values are current. Research missing fields beyond known URLs.'},state
