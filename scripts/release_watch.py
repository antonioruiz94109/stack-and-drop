"""Known-source release evidence watch; never approves or edits catalog entries."""
import re,json
from pathlib import Path

def review(catalog,previous,fetch,watch_path=None):
 path=Path(watch_path) if watch_path else Path(__file__).with_name('release-holds.json')
 holds=json.loads(path.read_text());known={(s['brand'],s['model'],s['gender']) for s in catalog}
 old=previous.get('release_watch',{});snapshot=dict(old);cache={};results=[]
 for h in holds:
  if (h['brand'],h['model'],h['gender']) in known:continue
  sources=[]
  for url in dict.fromkeys([h['url']]+h['supporting_sources']):
   if url not in cache:cache[url]=fetch(url)
   page=cache[url]
   if not page['ok']:
    sources.append({'url':url,'status':'unavailable','error':page.get('error','unknown')});continue
   # Nearby text is only a lead: dates may describe reviews, colors or unrelated shoes.
   pattern=re.escape(h['model']).replace(r'\ ',r'\s*').replace('GORE\\-TEX',r'(?:GORE[- ]?TEX|GTX)')
   excerpts=sorted(set(page['text'][max(0,m.start()-160):m.end()+320] for m in re.finditer(pattern,page['text'],re.I)))[:8]
   key=str(h['candidate_id'])+'|'+url
   before=old.get(key)
   status='baseline_for_review' if before is None else 'changed_for_review' if before['excerpts']!=excerpts else 'unchanged'
   snapshot[key]={'excerpts':excerpts,'url':url}
   sources.append({'url':url,'status':status,'excerpts':excerpts})
  results.append({'candidate_id':h['candidate_id'],'brand':h['brand'],'model':h['model'],'gender':h['gender'],'status':'hold_pending_human_verification','missing_evidence':h['release_notes'],'sources':sources,'research_query':h['brand']+' '+h['model']+' original release launch date '+h['gender']})
 return results,snapshot
