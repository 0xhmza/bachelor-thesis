"""Read-only sampling audit. All writes go to this ignored audit directory."""
import csv, json, hashlib, importlib.util, statistics, subprocess, sys, re, contextlib, io
from pathlib import Path
from collections import Counter, defaultdict
from urllib.parse import urlparse, parse_qs

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'tmp'/'sampling-peer-audit-2026-10-28'
OUT.mkdir(parents=True, exist_ok=True)
sys.stdout.reconfigure(encoding='utf-8')
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def rows(p): return list(csv.DictReader(Path(p).open(encoding='utf-8',newline='')))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(name,value): (OUT/name).write_text(json.dumps(value,indent=2,ensure_ascii=False,default=str)+'\n',encoding='utf-8')
def csvout(name,rr):
    if rr:
        with (OUT/name).open('w',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)

spec=importlib.util.spec_from_file_location('audit_rank',ROOT/'scripts/app-ranking/v004/rank.py')
rank=importlib.util.module_from_spec(spec);spec.loader.exec_module(rank)
cfg=read(ROOT/'scripts/app-ranking/v004/config.json')
rawdir=ROOT/'05_Data/App Sampling/26. Oct/Raw'
actual={'apple':rawdir/'appstore_2026-10-23.json','play':rawdir/'googleplay_2026-10-24.json'}
protected=list((ROOT/'03_Thesis').rglob('*.tex'))+list(rawdir.glob('*'))+[ROOT/'04_Study/App-Sample/screening.csv',ROOT/'04_Study/App-Sample/keywords.csv',ROOT/'05_Data/App Sampling/26. Oct/Processed/apps.csv']+list((ROOT/'scripts/app-ranking/v004/output').glob('*'))
before={str(p.relative_to(ROOT)):sha(p) for p in protected if p.is_file()}
raw={s:read(p) for s,p in actual.items()}
unique={s:{} for s in raw};dup_conflicts=[]
for s,data in raw.items():
    for q,rr in data['results'].items():
        for r in rr:
            clean={k:v for k,v in r.items() if k not in ['API Position','Search Position']}
            lid=str(r['ID'])
            if lid in unique[s] and unique[s][lid]!=clean: dup_conflicts.append((s,lid,q))
            unique[s].setdefault(lid,clean)
keywords=rows(ROOT/cfg['keywords']);qs={x['query'] for x in keywords}
screenrows=rows(ROOT/cfg['screening']);screen={(x['store'],x['id']):x for x in screenrows}
listings={s:rank.load(p,s,cfg['aliases'])[1] for s,p in actual.items()}
providers={rank.provider_key(p,cfg['aliases']) for p in cfg['preinstalled_providers']}
def evaluate(pairs=None,screening=None,factor=None,depth=30,apple_depth=None):
    pools={s:{k:v for k,v in rank.pool(listings[s],apple_depth if s=='apple' and apple_depth else depth,qs).items() if k not in cfg['preinstalled'][s]} for s in raw}
    cs=rank.candidates(pools['apple'],pools['play'],cfg['pairs'] if pairs is None else pairs)
    cc,nn=rank.calibration(cs,cfg['os_share']['ios'],cfg['os_share']['android'])
    if factor is not None: cc=factor
    ordered=sorted(cs,key=lambda c:(-(c['v']+cc*c['r']),c['key']))
    return cs,pools,cc,nn,ordered,rank.select(ordered,screen if screening is None else screening,47,providers)
cs,pools,cc,nn,ordered,(sel,skip,exc,pending)=evaluate()
base={x['provider'] for x in sel}
def scenario(name,**kw):
    cs1,_,c1,n1,_,(ss,_,_,pp)=evaluate(**kw)
    new={x['provider'] for x in ss}
    return dict(name=name,factor=c1,pairs=n1,candidates=len(cs1),entries=[x['name'] for x in ss if x['provider'] not in base],exits=[x['name'] for x in sel if x['provider'] not in new],order_changes=sum(a['key']!=b['key'] for a,b in zip(sel,ss)),listing_changes=[dict(provider=x['provider'],old_apple=next((a['apple']['id'] if a['apple'] else None for a in sel if a['provider']==x['provider']),None),new_apple=x['apple']['id'] if x['apple'] else None) for x in ss if x['provider'] in base and next((a['apple']['id'] if a['apple'] else None for a in sel if a['provider']==x['provider']),None)!=(x['apple']['id'] if x['apple'] else None)],pending=[x['key'] for x in pp])
reference={'com.nike.plusgps':'387771637','com.nike.ntc':'301521403','com.babycenter.pregnancytracker':'386022579','menloseweight.loseweightappformen.weightlossformen':'1460546771','loseweightapp.loseweightappforwomen.womenworkoutathome':'1502526521'}
scenarios=[scenario('five identity reference corrections',pairs=cfg['pairs']|reference)]
for name,key,category in [('Kinomap',('apple','611177969'),'activity'),('Lady Pill Reminder',('play','com.baviux.pillreminder'),'cycle')]:
    altered={k:dict(v) for k,v in screen.items()};altered[key].update(decision='eligible',criterion='',category=category)
    scenarios.append(scenario(name+' eligible (diagnostic)',screening=altered))
for factor in [0,0.02,0.05,cc,statistics.median([x['v']/x['r'] for x in cs if x['r']>0 and x['v']>0]),0.5,1]:
    scenarios.append(scenario('factor '+str(factor),factor=factor))
matches=[]
for c in cs:
    if c['apple'] and c['play']:
        a,p=c['apple'],c['play']
        matches.append(dict(provider=c['provider'],play_id=p['id'],play_name=p['name'],apple_id=a['id'],apple_name=a['name'],bundle=unique['apple'][a['id']].get('Bundle ID'),r=c['r'],v=c['v'],selected=c in sel,screened_apple=('apple',a['id']) in screen,screened_play=('play',p['id']) in screen))
csvout('all-matched-pairs.csv',matches)
trace=[];taken=set(providers)
for i,c in enumerate(ordered,1):
    d=rank.decision(c,screen)
    status='provider-skip' if c['provider'] in taken else 'unscreened' if d is None else d['decision']
    if status in ['eligible','unscreened']: taken.add(c['provider'])
    trace.append(dict(rank=i,key=c['key'],name=c['name'],provider=c['provider'],r=c['r'],v=c['v'],score=c['v']+cc*c['r'],status=status,category=(d or {}).get('category'),reason=(d or {}).get('reason')))
    if sum(t['status'] in ['eligible','unscreened'] for t in trace)==47:break
csvout('main-cascade.csv',trace)
cachep=rawdir/'googleplay-pages_2026-10-24.jsonl'
cachelist=[json.loads(l) for l in cachep.read_text(encoding='utf-8').split('\n') if l]
cache={e['id']:e for e in cachelist}
requests={}
for f in (ROOT/'scripts/googleplay-scraper/v004/output').glob('*.json'):
    for u,m in read(f).get('requests',{}).items():
        if '/store/apps/details?' in u and re.fullmatch('[0-9a-f]{64}',m.get('sha256','')):
            for lid in parse_qs(urlparse(u).query).get('id',[]):requests[lid]=m
missing=[dict(id=i,name=r.get('App Name'),installs=r.get('Embedded Install Count'),capture=cache.get(i,{}).get('captured_at'),screen=screen.get(('play',i))) for i,r in unique['play'].items() if 'Review Count' not in r]
csvout('missing-play-counts.csv',missing)
both=[c for c in cs if c['r']>0 and c['v']>0]
observed=[c for c in cs if c['play'] and 'Review Count' in unique['play'][c['play']['id']] and 'Rating Count' in unique['play'][c['play']['id']]]
ratios=[c['v']/c['r'] for c in both]
observed_rho=rank.spearman([c['v'] for c in observed],[c['vw'] for c in observed])
history_raw=subprocess.run(['git','show','HEAD^:05_Data/raw/README.md'],cwd=ROOT,capture_output=True,text=True,encoding='utf-8').stdout
(OUT/'historical-raw-readme.txt').write_text(history_raw,encoding='utf-8')
manifest={m.group(1):m.group(2) for m in re.finditer(r'`([^`]+\.(?:jsonl|json|log))`\s*\|[^\n]*?`([0-9a-f]{64})`',history_raw)}
manifest_checks={str(p.name):dict(sha256=sha(p),historical_matches=[k for k,v in manifest.items() if v==sha(p)]) for p in rawdir.glob('*') if p.is_file()}
summary=dict(commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),configured_paths={k:dict(path=cfg[k],exists=(ROOT/cfg[k]).exists()) for k in ['apple','play','keywords','screening','dataset','compare_selection']},actual_inputs={s:str(p.relative_to(ROOT)) for s,p in actual.items()},duplicate_content_conflicts=dup_conflicts,raw_counts={s:dict(distinct=len(unique[s]),rows=sum(len(x) for x in d['results'].values()),queries=len(d['results'])) for s,d in raw.items()},apple_first30_hits=sum(x['API Position']<=30 for rr in raw['apple']['results'].values() for x in rr),play_search_hits=sum(len(x) for x in raw['play']['search'].values()),play_depth30_hits=sum(x['Search Position']<=30 for rr in raw['play']['search'].values() for x in rr),pool={s:len(p) for s,p in pools.items()},candidates=len(cs),matched=len(matches),calibration=dict(c=cc,n=nn,ratio_median=statistics.median(ratios),ratio_min=min(ratios),ratio_max=max(ratios),quartiles=statistics.quantiles(ratios,n=4)),selection=dict(n=len(sel),providers=len(base),reached=len(trace),skipped=len(skip),excluded=len(exc),pending=len(pending),categories=Counter((rank.decision(c,screen) or {}).get('category') for c in sel)),screening=dict(n=len(screenrows),unique=len(screen),counts=Counter(x['decision'] for x in screenrows),exclusions=Counter(x['criterion'] for x in screenrows if x['decision']=='excluded'),invalid_ids=[x for x in screenrows if x['id'] not in unique[x['store']]],matched_both_screened=sum(m['screened_apple'] and m['screened_play'] for m in matches),matched_one_screened=sum(m['screened_apple'] != m['screened_play'] for m in matches),selected_both_screened=sum(m['selected'] and m['screened_apple'] and m['screened_play'] for m in matches)),missing_play_reviews=len(missing),explicit_zero_reviews=sum(r.get('Review Count')==0 for r in unique['play'].values()),observed_correlation=dict(n=len(observed),rho=observed_rho),cache=dict(rows=len(cachelist),unique=len(cache),dates=Counter(e['captured_at'][:10] for e in cachelist),id_coverage=set(cache)==set(unique['play']),rows_equal=all(unique['play'][i]==cache[i].get('row') for i in unique['play']),hash_coverage=len(set(cache)&set(requests)),hash_missing=len(set(cache)-set(requests))),manifest=manifest_checks,scenarios=scenarios,selected_checks=dict(free=all(unique[s][c[s]['id']].get('Price')==0 for c in sel for s in raw if c[s]),play_free_flag=all(unique['play'][c['play']['id']].get('Free to Download') is True for c in sel if c['play']),counts_observed=all(('Rating Count' if s=='apple' else 'Review Count') in unique[s][c[s]['id']] for c in sel for s in raw if c[s]),play_policies=sum(bool(unique['play'][c['play']['id']].get('Privacy Policy URL')) for c in sel if c['play'])))
write('evidence-pre-replay.json',summary)
# Redirect every output, including all three TeX tables, away from production.
replay=dict(cfg,**{s:str(p) for s,p in actual.items()},out=str(OUT/'replay'),table=str(OUT/'app-sample.replay.txt'),developer_table=str(OUT/'developer-rule.replay.txt'),alias_table=str(OUT/'developer-aliases.replay.txt'),dataset=str(OUT/'apps.replay.csv'))
write('replay-config.json',replay)
with contextlib.redirect_stdout(io.StringIO()):rank.main(str(OUT/'replay-config.json'))
summary['replay']={n:read(OUT/'replay'/n)==read(ROOT/'scripts/app-ranking/v004/output'/n) if n.endswith('.json') else rows(OUT/'replay'/n)==rows(ROOT/'scripts/app-ranking/v004/output'/n) for n in ['report.json','selection.csv','excluded.csv','sensitivity.csv']}
summary['replay']['processed_dataset']=rows(OUT/'apps.replay.csv')==rows(ROOT/'05_Data/App Sampling/26. Oct/Processed/apps.csv')
for key,name in [('table','app-sample.replay.txt'),('developer_table','developer-rule.replay.txt'),('alias_table','developer-aliases.replay.txt')]:summary['replay'][key]=(OUT/name).read_text(encoding='utf-8')==(ROOT/cfg[key]).read_text(encoding='utf-8')
summary['originals_unchanged']=all(sha(ROOT/p)==v for p,v in before.items())
summary['protected_sha256']=before
write('evidence.json',summary)
print(json.dumps({k:v for k,v in summary.items() if k not in ['protected_sha256','manifest','duplicate_content_conflicts']},indent=2,ensure_ascii=False,default=str))
