import json,re,sys,subprocess,glob,os
F=sys.argv[1]
titles=set()
out=subprocess.run("grep -ohP '\\\\paragraph\\*?\\{[^}]*\\}' /home/claude/b3/03_Thesis/chapters/*.tex",shell=True,capture_output=True,text=True).stdout
for t in re.findall(r'\\paragraph\*?\{([^}]*)\}',out):
    t=t.replace('~',' ').replace('--','–').replace("\\'","'")
    titles.add(t)
titles|={'LQ1 Harms and capabilities.','LQ2 Communication.','LQ3 Language models.','LQ4 Framing.'}
titles=sorted(titles,key=len,reverse=True)
ids=json.load(open('tabids.json'))
doc=json.load(open(F))['content']
def walk(ts):
    for t in ts:
        yield t
        yield from walk(t.get('childTabs',[]))
reqs=[];cnt=0
for t in walk(doc['tabs']):
    tid=t['tabProperties']['tabId']
    if tid not in ids.values(): continue
    for c in t['documentTab']['body']['content']:
        if 'paragraph' not in c: continue
        els=c['paragraph']['elements']
        txt=''.join(e.get('textRun',{}).get('content','') for e in els)
        if c['paragraph']['paragraphStyle'].get('namedStyleType','NORMAL_TEXT')!='NORMAL_TEXT': continue
        for ti in titles:
            if txt.startswith(ti+' ') or txt.startswith(ti+'\u00a0'):
                s=c['startIndex']
                reqs.append({'updateTextStyle':{'range':{'startIndex':s,'endIndex':s+len(ti),'tabId':tid},'textStyle':{'bold':True},'fields':'bold'}});cnt+=1
                break
print(cnt,file=sys.stderr)
json.dump(reqs,open('out3/runin.json','w'),ensure_ascii=False,separators=(',',':'))
