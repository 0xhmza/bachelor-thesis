"""Retrieve lawful free copies, validate PDFs, and record every success/failure."""
from __future__ import annotations
import argparse
from datetime import date
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter
from difflib import SequenceMatcher
import hashlib
import io
import html
import json
import logging
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urljoin, urlparse, quote
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

from pypdf import PdfReader
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
logging.getLogger('pypdf').setLevel(logging.ERROR)

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]
FOLDER = ROOT / '01_Literature/PDFs/Methods-Reading'
EVIDENCE = BASE / 'evidence/oa'
MANIFEST = BASE / 'download-status.json'
CATALOGUE = ROOT / '01_Literature/methodology-literature.json'
GROUPS = {'App reviews':'01_App-Reviews','App appraisal':'02_App-Appraisal',
          'Walkthrough':'03_Walkthroughs','Coding':'04_Coding',
          'Agreement':'05_Coder-Agreement','Review/reporting':'06_Review-and-Reporting',
          'Policy annotation':'07_Policy-Annotation','Privacy interfaces':'08_Privacy-Interfaces',
          'LLM annotation':'09_LLM-Annotation','Context/harm':'10_Harm-and-Context'}
LOCAL = {1:'Malki_2024_PrivacyPractices-FemaleMHealthApps.pdf',
         31:'Hudig_2025_IntimateDataSharing-FertilityTracking.pdf',
         70:'Gabriele_2020_FitnessTrackerUsers-KnowledgeAttitudes.pdf',
         71:'Cao_2024_PeriodTrackingApps-PostRoe.pdf',
         72:'SalehzadehNiksirat_2024_WearableActivityTrackers-Survey.pdf',
         80:'Citron_2022_PrivacyHarms.pdf',81:'Martin_2025_NoCookiesForYou.pdf',
         'N1':'Knabenhans_2026_PrivacyHarms-EUDigitalIdentity.pdf',
         'N2':'Nielsen_1994_UsabilityInspectionMethods-Book.pdf'}
MAX_BYTES = 60 * 1024 * 1024
TODAY = date.today().isoformat()

def load(path, default=None):
    return json.loads(path.read_text(encoding='utf-8-sig')) if path.exists() else default

def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def normalize(text):
    return re.sub(r'[^a-z0-9]+','',text.lower())

USER_AGENT = 'ThesisLiteratureRetrieval/1.0 (personal academic reading; public resources only)'

def curl_get(url, accept, timeout):
    """Same honest request through the Windows certificate store.

    Some university repositories send an incomplete certificate chain that
    Python's bundled store rejects but Windows (via curl/schannel) completes.
    The server is still verified; nothing is skipped or spoofed.
    """
    marker = b'\n--curl-meta--'
    result = subprocess.run(['curl.exe','-sSL','--max-time',str(timeout),'-A',USER_AGENT,'-H','Accept: '+accept,
                             '--max-filesize',str(MAX_BYTES),'-w',marker.decode()+'%{http_code}|%{url_effective}|%{content_type}',
                             url],capture_output=True)
    if result.returncode:
        raise ValueError('curl: '+result.stderr.decode('utf-8','replace').strip()[:200])
    body,_,meta = result.stdout.rpartition(marker)
    status,final,mime = (meta.decode('utf-8','replace').split('|',2)+['',''])[:3]
    if not status.startswith('2'):
        raise HTTPError(url,int(status or 0),'HTTP '+status,None,None)
    return body,final,mime

def get(url, accept='*/*', timeout=25):
    req = Request(url,headers={'User-Agent':USER_AGENT,'Accept':accept})
    try:
        with urlopen(req,timeout=timeout) as response:
            length = int(response.headers.get('Content-Length','0'))
            if length > MAX_BYTES:
                raise ValueError('File exceeds 60 MB retrieval limit')
            body = response.read(MAX_BYTES+1)
            if len(body)>MAX_BYTES:
                raise ValueError('Response exceeds retrieval limit')
            return body,response.geturl(),response.headers.get('Content-Type','')
    except URLError as e:
        if 'CERTIFICATE_VERIFY_FAILED' not in str(e):
            raise
        return curl_get(url,accept,timeout)

def json_url(url):
    body,_,_ = get(url,'application/json')
    return json.loads(body)

def discover(rows):
    EVIDENCE.mkdir(parents=True,exist_ok=True)
    found={}
    europe={}
    for batch_index in range(0,len(rows),20):
        subset=rows[batch_index:batch_index+20]
        cache=EVIDENCE/f'batch-{batch_index//20+1:02d}.json'
        if cache.exists():
            result=load(cache)
        else:
            query={'filter':'doi:'+'|'.join(r['doi'] for r in subset),'per-page':100,
                   'select':'id,doi,title,open_access,locations,best_oa_location'}
            result=json_url('https://api.openalex.org/works?'+urlencode(query))
            save(cache,result)
        for w in result.get('results',[]):
            if w.get('doi'):
                found[w['doi'].replace('https://doi.org/','').lower()]=w
        epcache=EVIDENCE/f'europe-pmc-{batch_index//20+1:02d}.json'
        try:
            result=load(epcache) if epcache.exists() else json_url(
                'https://www.ebi.ac.uk/europepmc/webservices/rest/search?'+
                urlencode({'query':' OR '.join('DOI:"'+r['doi']+'"' for r in subset),
                           'format':'json','resultType':'core','pageSize':1000}))
            save(epcache,result)
            for w in result.get('resultList',{}).get('result',[]):
                if w.get('doi'):
                    europe[w['doi'].lower()]=w
        except Exception as e:
            print(f'Europe PMC batch {batch_index//20+1}: {type(e).__name__}',flush=True)
    save(EVIDENCE/'openalex-index.json',found)
    save(EVIDENCE/'europe-pmc-index.json',europe)
    print(f'OA discovery: {len(found)} DOI records, {len(europe)} Europe PMC matches.',flush=True)
    return found,europe

def name_for(row):
    author=re.sub(r'[^A-Za-z0-9]+','-',row.get('author_label','Guideline').split(' et al.')[0].split(' & ')[0]).strip('-')
    title=re.sub(r'[^A-Za-z0-9]+','-',row['title']).strip('-')[:90]
    prefix=f"{row['rank']:02d}" if isinstance(row['id'],int) else row['id']
    return f"{prefix}_{author}_{row.get('year','')}_{title}.pdf"

def validate(body,row):
    if b'%PDF-' not in body[:1024]:
        text=body[:4000].decode('utf-8',errors='ignore').lower()
        if any(x in text for x in ['captcha','cloudflare','verify that','not a robot','javascript is disabled']):
            raise ValueError('Bot/JavaScript verification page returned instead of PDF')
        raise ValueError('Server returned HTML/non-PDF content')
    reader=PdfReader(io.BytesIO(body),strict=False)
    if reader.is_encrypted:
        try:
            if not reader.decrypt(''):
                raise ValueError('PDF is encrypted and cannot be read')
        except Exception:
            raise ValueError('PDF is encrypted and cannot be read')
    pages=len(reader.pages)
    if not pages:
        raise ValueError('PDF has no pages')
    text=' '.join(reader.pages[i].extract_text() or '' for i in range(min(3,pages)))
    title=row['title']
    normalized=normalize(text)
    normtitle=normalize(title)
    metadata_title=str(reader.metadata.title or '') if reader.metadata else ''
    exact=normtitle in normalized
    title_words=set(re.findall(r'[a-z]{4,}',title.lower()))-{'with','from','that','this','their','using','study'}
    text_words=set(re.findall(r'[a-z]{4,}',text.lower()))
    coverage=len(title_words & text_words)/max(len(title_words),1)
    doi_match=normalize(row.get('doi','__no_doi__')) in normalized
    scan=load(BASE/'evidence/oa/visually-verified-scans.json',{}).get(str(row['id']),{})
    visually_verified=scan.get('sha256')==hashlib.sha256(body).hexdigest() and scan.get('pages')==pages
    if row['id']=='N2':
        # Existing whole book, whose relevant chapter starts later.
        if 'usabilityinspectionmethods' not in normalized and pages<200:
            raise ValueError('Whole-book identity cannot be confirmed')
    elif not (visually_verified or exact or SequenceMatcher(None,normalize(metadata_title),normtitle).ratio()>.78
              or coverage>=.85 and len(title_words)>=5 or doi_match and coverage>=.55):
        raise ValueError(f'PDF identity not established: title word coverage {coverage:.2f}')
    if isinstance(row['id'],int) and row['id'] in {76,77}:
        if pages<30 or re.search(r'preview|sample.chapter|sample.pages',text[:2500],re.I):
            raise ValueError('Book preview/sample, not a verified complete book')
    if re.search(r'^(supplementary|multimedia appendix|supporting information)',text.strip(),re.I):
        raise ValueError('Supplement/appendix, not the main paper')
    return {'pages':pages,'title_word_coverage':round(coverage,3),'doi_in_front_pages':doi_match,
            'validation_method':'visually checked scan; exact SHA-256' if visually_verified else 'PDF parsing and title/DOI matching',
            'sha256':hashlib.sha256(body).hexdigest(),'bytes':len(body)}

def add(candidates,url,kind,version=None,license=None):
    if not url or not url.startswith(('https://','http://')):
        return
    if any(c['url']==url for c in candidates):
        return
    # Skip metadata-sourced supplementary files mislabelled as main PDFs.
    if re.search(r'(?:_app\d|supplement|multimedia)',url,re.I):
        return
    candidates.append({'url':url,'kind':kind,'version':version,'license':license})

def landing_links(url):
    body,final,mime=get(url,'text/html',timeout=20)
    if b'%PDF-' in body[:1024]:
        return [final]
    text=body.decode('utf-8',errors='replace')
    links=[]
    # Only follow links explicitly supplied by the legitimate landing page.
    for tag in re.findall(r'<meta\b[^>]*>',text,re.I):
        attrs=dict((k.lower(),v) for k,_,v in re.findall(r'([\w:-]+)\s*=\s*(["\'])(.*?)\2',tag,re.S))
        if attrs.get('name','').lower() in {'citation_pdf_url','dc.identifier.uri'} and '.pdf' in attrs.get('content','').lower():
            links.append(urljoin(final,attrs['content']))
    for href,label in re.findall(r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',text,re.I|re.S):
        if re.search(r'\.pdf(?:$|\?)|/PDF(?:$|\?)|pdf=render|/article/download/|/OutputFile/',href,re.I):
            if not re.search(r'supplement|appendix|_app\d',href+' '+label,re.I):
                links.append(urljoin(final,href.replace('&amp;','&')))
    return list(dict.fromkeys(links))[:5]

def candidates_for(row,openalex,europe):
    candidates=[]
    doi=row.get('doi','').lower()
    w=openalex.get(doi,{})
    locations=[w.get('best_oa_location')]+w.get('locations',[])
    for loc in locations:
        if loc and loc.get('is_oa'):
            add(candidates,loc.get('pdf_url'),'OA '+str((loc.get('source') or {}).get('type','location')),
                loc.get('version'),loc.get('license'))
    if isinstance(row['id'],int):
        raw=load(BASE/f"evidence/{row['id']:02d}.json",{})
        for link in raw.get('message',{}).get('link',[]):
            url=link.get('URL','')
            if 'pdf' in url.lower() or link.get('content-type')=='application/pdf':
                add(candidates,url.replace('http://','https://',1),'publisher PDF link','publishedVersion')
    # Known open publishers' canonical PDF routes.
    if doi.startswith('10.2196/') and row.get('primary_url'):
        u=row['primary_url'].rstrip('/')
        if 'jmir.org' in u:
            add(candidates,u+'/PDF','open publisher','publishedVersion')
    if doi.startswith('10.48550/arxiv.'):
        add(candidates,'https://arxiv.org/pdf/'+row['doi'].split('.')[-2]+'.'+row['doi'].split('.')[-1],'arXiv','submittedVersion')
    pm=europe.get(doi,{})
    for link in pm.get('fullTextUrlList',{}).get('fullTextUrl',[]):
        if link.get('documentStyle')=='pdf':
            add(candidates,link.get('url'),'Europe PMC linked PDF')
    pmcid=pm.get('pmcid')
    if pmcid:
        add(candidates,'https://europepmc.org/articles/'+pmcid+'?pdf=render','Europe PMC free PDF')
    return candidates,w,pmcid

def retrieve_xml(row,pmcid,dest,record):
    """Public OA full text is still useful when a publisher PDF is blocked."""
    url='https://www.ebi.ac.uk/europepmc/webservices/rest/'+pmcid+'/fullTextXML'
    xml,final,mime=get(url,'application/xml')
    article=ET.fromstring(xml)
    title=' '.join(article.findtext('.//article-title','').split())
    if not title:
        t=article.find('.//article-title')
        title=' '.join(' '.join(t.itertext()).split()) if t is not None else ''
    actual_dois=[e.text.lower() for e in article.findall('.//article-id') if e.get('pub-id-type')=='doi' and e.text]
    body=article.find('body')
    if row['doi'].lower() not in actual_dois or body is None or len(' '.join(body.itertext()))<1200:
        raise ValueError('XML is not verified article full text for the requested DOI')
    def render(el):
        tag=el.tag.split('}')[-1]
        content=html.escape(el.text or '')+''.join(render(c)+html.escape(c.tail or '') for c in el)
        tags={'p':'p','sec':'section','italic':'em','bold':'strong','sup':'sup','sub':'sub',
              'table':'table','thead':'thead','tbody':'tbody','tr':'tr','td':'td','th':'th',
              'list':'ul','list-item':'li','title':'h2','article-title':'h1','caption':'figcaption',
              'ref-list':'section','ref':'p','disp-quote':'blockquote','label':'strong'}
        if tag=='graphic':
            return '<p><em>Figure image is not bundled; see the linked original article.</em></p>'
        if tag in tags:
            t=tags[tag]
            attrs=' id="'+html.escape(el.get('id',''))+'"' if el.get('id') else ''
            return '<'+t+attrs+'>'+content+'</'+t+'>'
        return content
    label='Full-text HTML from the public Europe PMC XML; figure images are not bundled.'
    page='<!doctype html><html lang="en"><meta charset="utf-8"><title>'+html.escape(title)+'</title><style>body{font:17px/1.55 Georgia,serif;max-width:1000px;margin:40px auto;padding:0 24px;color:#182c3e}h1,h2{font-family:system-ui,sans-serif}table{border-collapse:collapse;font-size:14px}td,th{border:1px solid #bbb;padding:8px}a{color:#075c96}.source{background:#edf3f8;padding:16px}</style><h1>'+html.escape(title)+'</h1><p class="source">'+label+'<br>DOI: <a href="'+html.escape(row['doi_url'])+'">'+html.escape(row['doi'])+'</a><br>Source: <a href="'+html.escape(url)+'">Europe PMC full text XML</a></p>'
    abstract=article.find('.//abstract')
    if abstract is not None:page+='<h2>Abstract</h2>'+render(abstract)
    page+=render(body)
    back=article.find('back')
    if back is not None:page+='<h2>References and end matter</h2>'+render(back)
    license_el=article.find('.//license')
    if license_el is not None:page+='<h2>Source license notice</h2>'+render(license_el)
    page+='</html>'
    target=dest.with_suffix('.html');target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(page,encoding='utf-8')
    xmltarget=dest.with_suffix('.xml');xmltarget.write_bytes(xml)
    return {**record,'downloaded':True,'status':'available_html','file':target.relative_to(ROOT).as_posix(),
            'xml_file':xmltarget.relative_to(ROOT).as_posix(),'source_url':url,'resolved_url':final,
            'source_kind':'Europe PMC public full-text XML','version':'PMC full-text copy',
            'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'bytes':target.stat().st_size,
            'format':'HTML + source XML','note':label,'article_title':title}

def acquire(row,openalex,europe,manual):
    identifier=str(row['id'])
    group=GROUPS.get(row.get('category'),'11_Official-and-Methods')
    dest=FOLDER/group/name_for(row)
    record={'id':row['id'],'rank':row.get('rank'),'title':row['title'],'doi':row.get('doi'),
            'checked_on':TODAY,'downloaded':False,'attempts':[]}
    if dest.exists():
        try:
            info=validate(dest.read_bytes(),row)
            return {**record,**info,'downloaded':True,'status':'available','file':dest.relative_to(ROOT).as_posix(),
                    'source_url':'already downloaded','version':'see previous download manifest'}
        except Exception as e:
            record['attempts'].append({'url':str(dest),'error':str(e)})
    local=LOCAL.get(row['id'])
    if local:
        src=ROOT/'01_Literature/PDFs'/local
        if src.exists():
            try:
                info=validate(src.read_bytes(),row)
                dest.parent.mkdir(parents=True,exist_ok=True)
                shutil.copy2(src,dest)
                version='published copy already in project'
                if row['id']=='N1': version='project-held harm-tree version; compare May/September revision'
                if row['id']=='N2': version='whole edited book; relevant chapter pp. 105–140'
                return {**record,**info,'downloaded':True,'status':'available','file':dest.relative_to(ROOT).as_posix(),
                        'source_url':src.relative_to(ROOT).as_posix(),'version':version,'reused_existing':True}
            except Exception as e:
                record['attempts'].append({'url':str(src),'error':str(e)})
    candidates,w,pmcid=candidates_for(row,openalex,europe)
    for item in reversed(manual.get(identifier,[])):
        candidates.insert(0,item)
    # Existing official resources supply their direct URL; pages may offer a PDF.
    if not isinstance(row['id'],int) and '.pdf' in row.get('url','').lower():
        add(candidates,row['url'],'official resource')
    if not isinstance(row['id'],int) and 'usenix.org' in row.get('url',''):
        try:
            for u in landing_links(row['url']):add(candidates,u,'official USENIX PDF','publishedVersion')
        except Exception as e:
            record['attempts'].append({'url':row['url'],'error':str(e)})
    for c in candidates[:10]:
        try:
            body,final,mime=get(c['url'])
            info=validate(body,row)
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_bytes(body)
            return {**record,**info,'downloaded':True,'status':'available','file':dest.relative_to(ROOT).as_posix(),
                    'source_url':c['url'],'resolved_url':final,'source_kind':c['kind'],
                    'version':c.get('version') or 'version not specified by source','license':c.get('license')}
        except Exception as e:
            record['attempts'].append({'url':c['url'],'source_kind':c['kind'],'error':f'{type(e).__name__}: {e}'})
    # A public OA landing page may disclose an alternate direct PDF.
    for loc in [x for x in w.get('locations',[]) if x.get('is_oa')][:3]:
        url=loc.get('landing_page_url')
        if not url:continue
        try:
            for u in landing_links(url):
                if any(a['url']==u for a in record['attempts']):continue
                body,final,mime=get(u)
                info=validate(body,row)
                dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(body)
                return {**record,**info,'downloaded':True,'status':'available','file':dest.relative_to(ROOT).as_posix(),
                        'source_url':u,'resolved_url':final,'source_kind':'PDF linked by OA landing page',
                        'version':loc.get('version'),'license':loc.get('license')}
        except Exception as e:
            record['attempts'].append({'url':url,'source_kind':'OA landing page','error':f'{type(e).__name__}: {e}'})
    if pmcid:
        try:
            url='https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?'+urlencode({'id':pmcid})
            body,_,_=get(url)
            xml=ET.fromstring(body)
            links=xml.findall('.//link')
            for link in sorted(links,key=lambda el:el.get('format')!='pdf'):
                u=link.get('href','').replace('ftp://','https://',1)
                if not u:continue
                content,final,_=get(u,timeout=35)
                if link.get('format')=='tgz':
                    with tarfile.open(fileobj=io.BytesIO(content),mode='r:gz') as archive:
                        member=next((m for m in archive.getmembers() if m.isfile() and m.name.lower().endswith('.pdf') and 'supp' not in m.name.lower()),None)
                        if member is None:continue
                        content=archive.extractfile(member).read(MAX_BYTES+1)
                info=validate(content,row)
                dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(content)
                return {**record,**info,'downloaded':True,'status':'available','file':dest.relative_to(ROOT).as_posix(),
                        'source_url':u,'resolved_url':final,'source_kind':'PMC public OA package','version':'PMC full-text copy'}
        except Exception as e:
            record['attempts'].append({'url':'PMC OA package '+pmcid,'error':f'{type(e).__name__}: {e}'})
        try:
            return retrieve_xml(row,pmcid,dest,record)
        except Exception as e:
            record['attempts'].append({'url':'Europe PMC full-text XML '+pmcid,'error':f'{type(e).__name__}: {e}'})
    errors='; '.join(a['error'] for a in record['attempts'])
    if not isinstance(row['id'],int) and row['id']=='N7':
        reason='Living official web framework, not a paper PDF; the public webpage remains linked.'
        status='web_resource'
    elif w.get('open_access',{}).get('is_oa') or manual.get(identifier):
        reason='Free copy indexed, but retrieval failed: '+(errors or 'no usable direct PDF supplied')
        status='free_but_blocked'
    elif record['attempts']:
        reason='No verified free PDF retrieved; attempted sources returned: '+errors
        status='not_retrieved'
    else:
        reason='No free PDF located in checked OA metadata/publisher sources; library access or an author copy may be needed.'
        status='no_free_copy_located'
    return {**record,'status':status,'reason':reason,'oa_status':w.get('open_access',{}).get('oa_status'),
            'oa_landing_url':w.get('open_access',{}).get('oa_url') or next((c.get('landing') or c['url'] for c in manual.get(identifier,[])),None)}

def run(only_missing=False, identifiers=None):
    data=load(CATALOGUE)
    rows=data['ranked_doi_records']
    extras=[{**r,'author_label':r['title'].split(' (')[0].split(',')[0],'category':'Official','year':'',
             'rank':None} for r in data['official_or_no_doi_resources']]
    all_rows=rows+extras
    openalex,europe=discover(rows)
    prior=load(MANIFEST,{'records':[]})
    records={str(r['id']):r for r in prior['records']}
    manual=load(BASE/'oa-sources.json',{})
    todo=[r for r in all_rows if (not identifiers or str(r['id']) in identifiers) and
          (not only_missing or not records.get(str(r['id']),{}).get('downloaded'))]
    print(f'Retrieving {len(todo)} works; PDFs grouped under {FOLDER.relative_to(ROOT)}.',flush=True)
    with ThreadPoolExecutor(max_workers=5) as pool:
        futures={pool.submit(acquire,r,openalex,europe,manual):r for r in todo}
        for future in as_completed(futures):
            row=futures[future]
            try:result=future.result()
            except Exception as e:result={'id':row['id'],'rank':row.get('rank'),'title':row['title'],'doi':row.get('doi'),'downloaded':False,'status':'retrieval_error','reason':f'{type(e).__name__}: {e}','attempts':[]}
            records[str(row['id'])]=result
            save(MANIFEST,{'checked_on':TODAY,'records':list(records.values())})
            print(f"{row.get('rank') or row['id']}: {'OK' if result['downloaded'] else result['status']} — {row['title'][:70]}",flush=True)
    ordered=[records[str(r['id'])] for r in all_rows]
    save(MANIFEST,{'checked_on':TODAY,'records':ordered,'summary':dict(Counter(r['status'] for r in ordered))})
    print('Download summary:',json.dumps(dict(Counter(r['status'] for r in ordered))),flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--missing-only',action='store_true')
    parser.add_argument('--ids',help='Comma-separated catalogue IDs to retry')
    args=parser.parse_args()
    run(args.missing_only,set(args.ids.split(',')) if args.ids else None)
