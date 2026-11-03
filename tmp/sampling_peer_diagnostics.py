"""Additional offline diagnostics; no production files are written."""
import ast, copy, csv, hashlib, importlib, importlib.util, json, random, statistics, sys
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'tmp/sampling-peer-audit-2026-10-28'
sys.stdout.reconfigure(encoding='utf-8')
spec=importlib.util.spec_from_file_location('rank',ROOT/'scripts/app-ranking/v004/rank.py')
rank=importlib.util.module_from_spec(spec);spec.loader.exec_module(rank)
cfg=json.loads((ROOT/'scripts/app-ranking/v004/config.json').read_text(encoding='utf-8'))
rawdir=ROOT/'05_Data/App Sampling/26. Oct/Raw'
raw={s:json.loads((rawdir/name).read_text(encoding='utf-8')) for s,name in [('apple','appstore_2026-10-23.json'),('play','googleplay_2026-10-24.json')]}
listings={s:rank.load(rawdir/name,s,cfg['aliases'])[1] for s,name in [('apple','appstore_2026-10-23.json'),('play','googleplay_2026-10-24.json')]}
qs={x['query'] for x in csv.DictReader(open(ROOT/cfg['keywords'],encoding='utf-8'))}
screen={(x['store'],x['id']):x for x in csv.DictReader(open(ROOT/cfg['screening'],encoding='utf-8'))}
providers={rank.provider_key(p,cfg['aliases']) for p in cfg['preinstalled_providers']}
def getcs(depth=30):
 pools={s:{i:l for i,l in rank.pool(ls,depth,qs).items() if i not in cfg['preinstalled'][s]} for s,ls in listings.items()}
 return rank.candidates(pools['apple'],pools['play'],cfg['pairs'])
cs=getcs();cc,n=rank.calibration(cs,.277,.723)
def select(factor,screening=screen,cs=cs):
 return rank.select(sorted(cs,key=lambda x:(-(x['v']+factor*x['r']),x['key'])),screening,47,providers)
sel,*_=select(cc);base={x['provider'] for x in sel}
ratios=[x['v']/x['r'] for x in cs if x['v']>0 and x['r']>0]
rng=random.Random(20261028)
factors=sorted(statistics.median(rng.choices(ratios,k=len(ratios)))*.277/.723 for _ in range(2000))
samples=[select(f) for f in factors[::10]]
bootstrap=dict(seed=20261028,repetitions=2000,percentile_2_5=factors[49],percentile_97_5=factors[1949],selection_repetitions=len(samples),provider_changes=Counter(len(base-{c['provider'] for c in s[0]}) for s in samples),runs_with_pending=sum(bool(s[3]) for s in samples),interpretation='Resampling the current uncorrected matched-pair ratios; diagnostic only, no inference for the market population; correlated provider rows not adjusted.')
both=[x for x in cs if x['r']>0 and x['v']>0]
eligible=[x for x in both if rank.decision(x,screen) and rank.decision(x,screen)['decision']=='eligible']
calibration_groups=dict(all_positive_pairs=len(both),eligible_positive_pairs=len(eligible),excluded_positive_pairs=sum(rank.decision(x,screen) is not None and rank.decision(x,screen)['decision']!='eligible' for x in both),unscreened_positive_pairs=sum(rank.decision(x,screen) is None for x in both),eligible_only_factor=statistics.median(x['v']/x['r'] for x in eligible)*.277/.723)
adjusted={k:dict(v) for k,v in screen.items()}
for k in [('apple','571800810'),('play','com.calm.android')]:adjusted[k].update(decision='eligible',criterion='',category='mood')
ss,_,_,pending=select(cc,adjusted)
calm=dict(entries=[x['name'] for x in ss if x['provider'] not in base],exits=[x['name'] for x in sel if x['provider'] not in {z['provider'] for z in ss}],pending=[x['key'] for x in pending],interpretation='Counterfactual only: this does not decide whether meditation/sleep sessions satisfy the domain rule.')
# Execute only the unchanged main function of collector v005 with network-free search and cache.
tree=ast.parse((ROOT/'scripts/googleplay-scraper/v005/scraper.py').read_text(encoding='utf-8'))
fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
events=[]
class Adapter:
 def __init__(self):self.get=None
adapter=Adapter()
class Imports:
 @staticmethod
 def import_module(name):return adapter
cachecopy=OUT/'pages.replay.jsonl';cachecopy.write_bytes((rawdir/'googleplay-pages_2026-10-24.jsonl').read_bytes())
env=dict(Path=Path,json=json,requests={},now=lambda:'AUDIT-TIME',importlib=Imports,fetch=lambda *a:events.append(a),search=lambda k,gl,hl:raw['play']['search'][k],app=lambda *a,**kw:(_ for _ in ()).throw(AssertionError('unexpected network detail call')),FIELDS={})
exec(compile(ast.Module(body=[fn],type_ignores=[]),'unchanged-v005-main','exec'),env)
rcfg=dict(region='de',language='de',depth=30,cache=str(cachecopy),keywords=list(raw['play']['search']))
replay=env['main'](rcfg)
same_results=replay['results']==raw['play']['results']
us=env['main'](rcfg|{'region':'us','language':'en'})
cache_hazard=dict(offline_v005_results_equal=same_results,result_rows=sum(len(v) for v in replay['results'].values()),us_labeled_run_reuses_identical_de_rows=us['results']==raw['play']['results'],us_reported_region=us['region'],network_calls=events,interpretation='Synthetic offline replay: package-ID-only cache accepts German rows for another requested region/language. It does not establish the historical DE run had wrong-country rows.')
changes=[];seen={}
for q,rr in raw['apple']['results'].items():
 for r in rr:
  i=str(r['ID']);clean={k:v for k,v in r.items() if k!='API Position'}
  if i in seen and seen[i][1]!=clean:changes.append(dict(id=i,name=r['App Name'],first_query=seen[i][0],later_query=q,changes={k:[seen[i][1].get(k),clean.get(k)] for k in set(clean)|set(seen[i][1]) if seen[i][1].get(k)!=clean.get(k)}))
  seen.setdefault(i,(q,clean))
deep=getcs(200)
deep_bad=[dict(play=x['play']['name'],apple=x['apple']['name'],play_id=x['play']['id'],apple_id=x['apple']['id']) for x in deep if x['play'] and x['apple'] and x['provider']=='google']
summary=dict(bootstrap=bootstrap,calibration_groups=calibration_groups,calm_counterfactual=calm,collector_replay=cache_hazard,repeated_apple_listing_conflicts=changes,deep_google_pairs=deep_bad)
(OUT/'diagnostics.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k!='repeated_apple_listing_conflicts'},ensure_ascii=False,indent=2))

