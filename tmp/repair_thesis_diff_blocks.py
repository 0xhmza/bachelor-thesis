from pathlib import Path
import re,hashlib,subprocess,os,json

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'tmp/thesis-diff-2026-10-28'
target={'table','table*','figure','figure*','longtable','tikzpicture','lstlisting'}
blocks={};present={}
def opaque(text,side):
 # Mask comments without shifting positions; commented old tables are not content.
 masked=[]
 for line in text.splitlines(keepends=True):
  m=re.search(r'(?<!\\)%',line)
  masked.append(line if not m else line[:m.start()]+' '*(len(line)-m.start()-1)+'\n')
 mask=''.join(masked)
 segments=[];active=None;depth=0
 for m in re.finditer(r'\\(begin|end)\{([^{}]+)\}',mask):
  if m.group(2) not in target:continue
  if m.group(1)=='begin':
   if active is None:active=m.start()
   depth+=1
  elif active is not None:
   depth-=1
   if depth==0:
    raw=text[active:m.end()]
    key='ZZDIFOPAQUE'+hashlib.sha256(' '.join(mask[active:m.end()].split()).encode()).hexdigest().upper()+'ZZ'
    blocks.setdefault(key,{})[side]=raw
    segments.append((active,m.end(),key))
    active=None
 assert active is None,'Unbalanced opaque block'
 for start,end,key in reversed(segments):text=text[:start]+'\n\n'+key+'\n\n'+text[end:]
 present[side]=len(segments)
 return text

for side in ['old','new']:
 text=(BASE/side/'flat.tex').read_text(encoding='utf-8')
 (BASE/side/'protected.tex').write_text(opaque(text,side),encoding='utf-8')
env=os.environ.copy();env['LC_ALL']='C';env['LANG']='C'
build=BASE/'new/03_Thesis'
pre=BASE/'diff-preamble.tex'
pretext=pre.read_text(encoding='utf-8')
if r'\RequirePackage{adjustbox}' not in pretext:
 pre.write_bytes((pretext+'\n'+r'\RequirePackage{adjustbox}'+'\n').encode('utf-8'))
cmd=['C:/texlive/2026/bin/windows/latexdiff.exe','--encoding=utf8','--preamble='+str(BASE/'diff-preamble.tex'),'--math-markup=whole','--graphics-markup=none','--exclude-safecmd=todo,highlight',str(BASE/'old/protected.tex'),str(BASE/'new/protected.tex')]
r=subprocess.run(cmd,cwd=build,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env)
(BASE/'latexdiff-blocks-log.txt').write_bytes(r.stderr)
assert r.returncode==0
text=r.stdout.decode('utf-8').replace('\r\n','\n')
def review_layout(raw,kind=None):
 if kind:
  # LaTeX resets color when entering a float. Apply the diff color inside it.
  color='DiffAdd' if kind=='added' else 'DiffDel'
  raw=re.sub(r'(\\begin\{(?:table\*?|figure\*?)\}(?:\[[^\]]*\])?)',lambda m:m.group(1)+r'\color{'+color+'}',raw)
 if r'\begin{tikzpicture}' in raw and r'\resizebox' not in raw:
  raw=raw.replace(r'\begin{tikzpicture}',r'\begin{adjustbox}{max width=\textwidth}'+r'\begin{tikzpicture}',1)
  raw=raw.replace(r'\end{tikzpicture}',r'\end{tikzpicture}\end{adjustbox}',1)
 if raw.startswith(r'\begin{lstlisting}'):
  m=re.fullmatch(r'\\begin\{lstlisting\}(\[.*?\])?\s*\n(.*?)\\end\{lstlisting\}\s*',raw,re.S)
  assert m is not None,'Cannot parse listing block'
  options=(m.group(1) or '[]')[1:-1]
  body=m.group(2)
  # UTF-8 literals in a listings option nested in diff markup can be split
  # into active bytes. Use an ASCII sentinel with the same rendered umlaut.
  mapping=r'literate={ä}{{\"a}}1'
  options=options.replace(', '+mapping,'').replace(','+mapping,'').replace(mapping,'').strip(', ')
  if 'ä' in body:
   assert '~' not in body
   body=body.replace('ä','~')
   options+=(',' if options else '')+r'literate={~}{{\"a}}1'
  folder=build/'diff-listings';folder.mkdir(exist_ok=True)
  key=hashlib.sha256(raw.encode('utf-8')).hexdigest()[:20]+'.txt'
  (folder/key).write_bytes(body.encode('utf-8'))
  if kind:
   color='DiffAdd' if kind=='added' else 'DiffDel'
   if re.search(r'basicstyle\s*=',options):
    options=re.sub(r'(basicstyle\s*=\s*[^,]+)',lambda m:m.group(1)+r'\color{'+color+'}',options)
   else:options+=(',' if options else '')+r'basicstyle=\ttfamily\scriptsize\color{'+color+'}'
  return r'\lstinputlisting['+options+']{diff-listings/'+key+'}'
 # The source puts two large tables in one float. Split that float only in
 # this review copy, preserving both tables and captions without clipping.
 if r'\label{tab:keywords}' in raw and r'\label{tab:eligibility}' in raw:
  raw=raw.replace(r'\vspace{3\baselineskip}',r'\end{singlespace}\end{table}'+'\n'+r'\begin{table}[p]\centering\begin{singlespace}')
 return raw
for key,b in blocks.items():
 if len(b)==2:replacement=review_layout(b['new'])
 elif 'old' in b:
  # Deleted table labels must not replace the current version's reference targets.
  new_labels=set(re.findall(r'\\label\{([^{}]+)\}',(BASE/'new/flat.tex').read_text(encoding='utf-8')))
  old=re.sub(r'\\label\{([^{}]*)\}',lambda m:'' if m.group(1) in new_labels else m.group(0),b['old'])
  replacement=r'{\color{DiffDel}'+review_layout(old,'deleted')+'\n}'
 else:replacement=r'{\color{DiffAdd}'+review_layout(b['new'],'added')+'\n}'
 text=text.replace(key,replacement)
assert 'ZZDIFOPAQUE' not in text
(build/'thesis-diff.tex').write_bytes(text.encode('utf-8'))
manifest=json.loads((BASE/'manifest.json').read_text(encoding='utf-8'))
manifest['block_handling']={'old_blocks':present['old'],'new_blocks':present['new'],'unchanged':sum(len(b)==2 for b in blocks.values()),'deleted':sum('new' not in b for b in blocks.values()),'added':sum('old' not in b for b in blocks.values()),'method':'Changed tables/figures shown as intact deleted and added blocks to preserve layouts; running text uses word-level red/green markup.'}
(BASE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(manifest['block_handling'])
