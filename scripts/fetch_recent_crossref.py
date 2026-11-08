#!/usr/bin/env python3
"""Collect up to 200 DOI-registered 2020–2026 CAPSM-related journal references.

Metadata source: Crossref REST API (https://api.crossref.org/works).  This is an
OPTIONAL companion literature pool, not a representation of citations actually
used within the 2026 thesis.  Fails closed when not enough results are found.
"""
import argparse, base64, csv, datetime, gzip, hashlib, json, re, sys, time
from collections import Counter
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

QUERIES=[
 'power system reinforcement learning control',
 'smart grid multi-agent reinforcement learning',
 'physics-informed neural network power system',
 'electrical power system digital twin',
 'electric vehicle charging scheduling reinforcement learning',
 'power system security deep learning',
 'FACTS devices voltage control optimization',
 'power system transient stability machine learning',
 'power systems explainable artificial intelligence',
 'distribution network voltage control reinforcement learning',
 'optimal power flow reinforcement learning',
 'power system state estimation graph neural network',
 'grid forming inverter stability control',
 'microgrid hierarchical multi-agent control',
 'renewable power forecasting deep learning',
 'power grid cascading failures learning',
 'power system load frequency control deep reinforcement learning',
 'electric vehicle vehicle to grid energy management',
 'power system false data injection attack detection',
 'transmission network security constrained optimal power flow',
 'power system real time hardware in loop validation',
 'power system contingency screening artificial intelligence',
 'power systems robust model predictive control',
 'power system distribution distributed energy coordination',
 'electricity forecasting transformer deep learning',
 'physics informed optimization power flow',
 'flexible AC transmission FACTS renewable energy',
 'power system cyber physical security intelligent control',
 'smart microgrids coordinated energy storage deep learning',
 'power systems safety constrained reinforcement learning',
]
DOMAINS=('power system','power grid','smart grid','microgrid','electric vehicle','power network','electricity','energy management','energy storage','distributed energy','grid-connected','grid forming','grid-forming','voltage regulation','voltage stability','transmission network','power flow','photovoltaic','wind power','renewable power','load frequency','FACTS','power converter')
METHODS=('learning','neural','agent','control','optimization','scheduling','forecast','stability','simulation','protection','cyber','security','estimation','digital twin','real-time','resilience','resilient','demand response','reinforcement','inverter','flexible','intelligent','power flow')
AVOID=('erratum','correction to','retraction','expression of concern','corrigendum','editorial:','reviewer acknowledgement','retracted')

def year_of(obj):
 for key in ('published','issued','published-online','published-print'):
  dp=obj.get(key,{}).get('date-parts',[])
  if dp and dp[0] and isinstance(dp[0][0],int):return dp[0][0]
 return None

def textclean(s):return re.sub(r'<[^>]+>','',str(s)).strip()

def accepted(obj,asof):
 yr=year_of(obj)
 if obj.get('type')!='journal-article' or not yr or not 2020<=yr<=asof.year:return False
 doi=obj.get('DOI','').lower().strip();title=textclean((obj.get('title') or [''])[0]);lt=title.lower()
 if not re.match(r'^10\.\d{4,9}/\S+$',doi) or not title or len(title)<24:return False
 if any(x in lt for x in AVOID):return False
 if not any(x.lower() in lt for x in DOMAINS):return False
 if not any(x in lt for x in METHODS):return False
 if not obj.get('author') or not obj.get('container-title'):return False
 if yr==asof.year:
  parts=(obj.get('published') or obj.get('issued') or {}).get('date-parts',[])
  if parts and parts[0]:
   p=parts[0];mm=p[1] if len(p)>1 else 1;dd=p[2] if len(p)>2 else 1
   try:
    if datetime.date(p[0],mm,dd)>asof:return False
   except ValueError:return False
 return True

def score(obj):
 lt=textclean((obj.get('title') or [''])[0]).lower()
 priorities={'reinforcement learning':9,'power system':7,'multi-agent':7,'physics-informed':6,'FACTS':7,'electric vehicle':5,'voltage control':5,'security constrained':6,'contingency':6,'real-time':3,'state estimation':3,'microgrid':2,'transient stability':5,'grid-forming':3,'digital twin':3,'optimal power flow':5,'fault':3,'controller':3}
 return sum(v for k,v in priorities.items() if k.lower() in lt)+min(10,int(obj.get('is-referenced-by-count',0))//20)

def escape(s):
 s=textclean(s).replace('\\','\\textbackslash{}')
 s=s.replace('{','\\{').replace('}','\\}')
 return re.sub(r'[\n\r\s]+',' ',s).replace('&','\\&')

def bib_entry(i,obj):
 key='CAPSMRecent%03d'%i
 a=[]
 for x in obj.get('author',[]):
  family=x.get('family','').strip();given=x.get('given','').strip();name=x.get('name','').strip()
  if name:a.append('{%s}'%escape(name))
  elif family:a.append(escape(family)+(', '+escape(given) if given else ''))
 fields=[('title',(obj.get('title') or [''])[0]),('author',' and '.join(a)),('journal',(obj.get('container-title') or [''])[0]),('year',str(year_of(obj))),('volume',obj.get('volume','')),('number',obj.get('issue','')),('pages',obj.get('page','')),('doi',obj['DOI']),('url','https://doi.org/'+obj['DOI'])]
 return '@article{%s,\n'%key+'\n'.join('  %s = {%s},'%(k,escape(v) if k not in ('author','doi','url') else v) for k,v in fields if v)+'\n}\n'

def fetch(query,asof,rows=100):
 params={'query.title':query,'rows':rows,'filter':'from-pub-date:2020-01-01,until-pub-date:%s,type:journal-article'%asof.isoformat(),'select':'DOI,title,author,published,issued,container-title,volume,issue,page,URL,type,is-referenced-by-count'}
 url='https://api.crossref.org/works?'+urlencode(params)
 for attempt in range(4):
  try:
   req=Request(url,headers={'User-Agent':'CAPSM-Thesis-2026/1.0 (research bibliography metadata; mailto:academia@example.org)','Accept':'application/json'})
   with urlopen(req,timeout=45) as resp: return json.load(resp).get('message',{}).get('items',[])
  except Exception as e:
   if attempt==3:print('FAILED',query,str(e),file=sys.stderr);return []
   time.sleep(2**attempt)
 return []

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output-dir',default='references');ap.add_argument('--limit',type=int,default=200);ap.add_argument('--asof',default='2026-11-08');ap.add_argument('--rows',type=int,default=100);args=ap.parse_args()
 asof=datetime.date.fromisoformat(args.asof);dest=Path(args.output_dir);dest.mkdir(parents=True,exist_ok=True)
 seen={};counts=Counter()
 for q in QUERIES:
  vals=fetch(q,asof,args.rows);keep=0
  for item in vals:
   if not accepted(item,asof):continue
   doi=item['DOI'].lower();score_i=score(item)
   if doi not in seen or score_i>seen[doi][0]:seen[doi]=(score_i,item,q)
   keep+=1
  counts[q]=keep;print('%s: %d accepted; %d unique'%(q,keep,len(seen)),flush=True)
  if len(seen)>=max(300,args.limit*2):break
 rows=sorted(seen.values(),key=lambda x:(-x[0],-year_of(x[1]),x[1]['DOI']))[:args.limit]
 if len(rows)<args.limit:
  raise RuntimeError('Insufficient independently registered articles: %d < %d; do not fabricate to meet quota'%(len(rows),args.limit))
 txt='% CAPSM supplemental recent-literature pool; metadata from Crossref, date %s.\n'%asof
 txt+='% %d DOI-registered journal articles. Not automatically cited by the thesis.\n\n'%len(rows)
 for i,(sc,item,q) in enumerate(rows,1):txt+=bib_entry(i,item)+'\n'
 stem='CAPSM_2020_2026_%d_crossref'%len(rows)
 bib=dest/(stem+'.bib');bib.write_text(txt,encoding='utf-8')
 (dest/(stem+'.bib.gz.b64')).write_text(base64.b64encode(gzip.compress(txt.encode(),compresslevel=9)).decode(),encoding='ascii')
 with (dest/(stem+'_index.csv')).open('w',newline='',encoding='utf-8') as fo:
  w=csv.writer(fo);w.writerow(['key','year','doi','title','journal','score','query'])
  for i,(sc,obj,q) in enumerate(rows,1):w.writerow(['CAPSMRecent%03d'%i,year_of(obj),obj['DOI'],(obj.get('title') or [''])[0],(obj.get('container-title') or [''])[0],sc,q])
 audit={'provenance':'Crossref REST API','generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'as_of':asof.isoformat(),'count':len(rows),'years':dict(Counter(year_of(x[1]) for x in rows)),'distinct_doi':len(set(x[1]['DOI'].lower() for x in rows)),'sha256':hashlib.sha256(txt.encode()).hexdigest(),'queries_checked':dict(counts),'limitation':'Pool of relevant journal literature only; not a validation of claims, fulltext access, citation usage or absence of retractions'}
 (dest/(stem+'_audit.json')).write_text(json.dumps(audit,indent=2,ensure_ascii=False),encoding='utf-8')
 print('SUCCESS',bib,len(rows),audit['sha256'])
if __name__=='__main__':main()