"""Create an isolated latexdiff build; never write thesis sources/build files in place."""
from pathlib import Path
import subprocess, hashlib, io, tarfile, shutil, re, json, os, sys
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'tmp/thesis-diff-2026-10-28'
BASE.mkdir(parents=True,exist_ok=True)
HEAD=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
protected=[p for folder in ['03_Thesis','_shared'] for p in (ROOT/folder).rglob('*') if p.is_file() and p.suffix in ['.tex','.bib','.cls','.sty'] and 'proposal' not in p.parts]
before={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
(BASE/'source-hashes.json').write_text(json.dumps(before,indent=2),encoding='utf-8')
oldroot=BASE/'old';newroot=BASE/'new'
oldroot.mkdir(exist_ok=True)
archive=subprocess.check_output(['git','archive',HEAD,'03_Thesis','_shared','scripts'],cwd=ROOT)
with tarfile.open(fileobj=io.BytesIO(archive)) as t:
 for m in t.getmembers():
  target=(oldroot/m.name).resolve()
  assert target.is_relative_to(oldroot.resolve()),m.name
 t.extractall(oldroot,filter='data')
ignore=shutil.ignore_patterns('.venv','__pycache__','output','proposal','*.aux','*.bcf','*.bbl','*.blg','*.log','*.out','*.toc','*.lof','*.lot','*.lol','*.tdo','*.synctex.gz','*.run.xml','*.fdb_latexmk','*.fls','*.docx','thesis.pdf','thesis - Copy.pdf')
for folder in ['03_Thesis','_shared','scripts']:
 shutil.copytree(ROOT/folder,newroot/folder,ignore=ignore,dirs_exist_ok=True)

def flatten(path,master,seen=()):
 assert path not in seen,('recursive input',path)
 data=path.read_text(encoding='utf-8')
 result=[]
 for line in data.splitlines(keepends=True):
  parts=re.split(r'(?<!\\)%',line,maxsplit=1)
  code=parts[0]
  def replace(m):
   value=m.group(1)
   q=master/value
   if not q.suffix:q=q.with_suffix('.tex')
   if not q.exists():
    q=path.parent/value
    if not q.suffix:q=q.with_suffix('.tex')
   if not q.exists():raise FileNotFoundError(f'{path}: input {value}')
   return '\n'+flatten(q,master,seen+(path,))+'\n'
  code=re.sub(r'\\(?:input|include)\{([^{}]+)\}',replace,code)
  result.append(code+('%'+parts[1] if len(parts)>1 else ''))
 return ''.join(result)

for tree in [oldroot,newroot]:
 master=tree/'03_Thesis'
 flat=flatten(master/'thesis.tex',master)
 (tree/'flat.tex').write_text(flat,encoding='utf-8')

if '--prepare-only' in sys.argv:
 manifest=json.loads((BASE/'manifest.json').read_text(encoding='utf-8')) if (BASE/'manifest.json').exists() else {}
 captured={p:hashlib.sha256((newroot/p).read_bytes()).hexdigest() for p in before}
 manifest.update(baseline=HEAD,current_snapshot_utc=datetime.now(timezone.utc).isoformat(),production_hashes=captured,comparison='Saved working tree against last commit, complete thesis inputs',snapshot_files_match_working_tree=all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in captured.items()))
 (BASE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
 print('Prepared fresh snapshot',manifest['current_snapshot_utc'],'consistent:',manifest['snapshot_files_match_working_tree'],flush=True)
 raise SystemExit(0)

custom=r'''\RequirePackage{xcolor}
\definecolor{DiffAdd}{rgb}{0,0.42,0}
\definecolor{DiffDel}{rgb}{0.72,0,0}
\providecommand{\DIFadd}[1]{{\protect\color{DiffAdd}#1}}
\providecommand{\DIFdel}[1]{{\protect\color{DiffDel}#1}}
\providecommand{\DIFaddbegin}{}
\providecommand{\DIFaddend}{}
\providecommand{\DIFdelbegin}{}
\providecommand{\DIFdelend}{}
\providecommand{\DIFmodbegin}{}
\providecommand{\DIFmodend}{}
\providecommand{\DIFaddFL}[1]{\DIFadd{#1}}
\providecommand{\DIFdelFL}[1]{\DIFdel{#1}}
\providecommand{\DIFaddbeginFL}{}
\providecommand{\DIFaddendFL}{}
\providecommand{\DIFdelbeginFL}{}
\providecommand{\DIFdelendFL}{}
'''
(BASE/'diff-preamble.tex').write_text(custom,encoding='utf-8')
env=os.environ.copy();env['LC_ALL']='C';env['LANG']='C'
cmd=['C:/texlive/2026/bin/windows/latexdiff.exe','--encoding=utf8','--preamble='+str(BASE/'diff-preamble.tex'),'--math-markup=whole','--graphics-markup=none','--add-to-config','PICTUREENV=tikzpicture','--exclude-safecmd=todo,highlight',str(oldroot/'flat.tex'),str(newroot/'flat.tex')]
build=newroot/'03_Thesis'
with (build/'thesis-diff.tex').open('wb') as stdout,(BASE/'latexdiff-log.txt').open('wb') as stderr:
 result=subprocess.run(cmd,cwd=build,stdout=stdout,stderr=stderr,env=env)
if result.returncode:raise RuntimeError('latexdiff failed; see latexdiff-log.txt')

# Keep old bibliography entries referenced by deleted passages without changing production.
def entries(text):
 starts=list(re.finditer(r'(?m)^@\w+\s*\{\s*([^,\s]+)\s*,',text))
 return {m.group(1):text[m.start():starts[i+1].start() if i+1<len(starts) else len(text)] for i,m in enumerate(starts)}
oldbib=entries((oldroot/'_shared/references.bib').read_text(encoding='utf-8'))
newbibpath=newroot/'_shared/references.bib';newbib=newbibpath.read_text(encoding='utf-8');newkeys=entries(newbib)
extra=[oldbib[k] for k in oldbib.keys()-newkeys.keys()]
if extra:newbibpath.write_text(newbib+'\n\n'+'\n\n'.join(extra),encoding='utf-8')
diff=(build/'thesis-diff.tex').read_text(encoding='utf-8')
manifest=dict(baseline=HEAD,current_snapshot_utc=datetime.now(timezone.utc).isoformat(),comparison='Saved working tree against last commit, complete thesis inputs',diff_add_commands=len(re.findall(r'\\DIFadd(?:FL)?\{',diff)),diff_del_commands=len(re.findall(r'\\DIFdel(?:FL)?\{',diff)),retained_old_bib_entries=len(extra),production_hashes=before)
(BASE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
commands=[('pdflatex-1',['C:/texlive/2026/bin/windows/pdflatex.exe','-interaction=nonstopmode','-halt-on-error','thesis-diff.tex']),('biber',['C:/texlive/2026/bin/windows/biber.exe','thesis-diff']),('pdflatex-2',['C:/texlive/2026/bin/windows/pdflatex.exe','-interaction=nonstopmode','-halt-on-error','thesis-diff.tex']),('pdflatex-3',['C:/texlive/2026/bin/windows/pdflatex.exe','-interaction=nonstopmode','-halt-on-error','thesis-diff.tex'])]
results=[]
for label,cmd in commands:
 print(label+' started',flush=True)
 with (BASE/(label+'.txt')).open('wb') as f:r=subprocess.run(cmd,cwd=build,stdout=f,stderr=subprocess.STDOUT,env=env)
 results.append(dict(stage=label,returncode=r.returncode))
 print(label+' exit '+str(r.returncode),flush=True)
 if r.returncode:
  print((BASE/(label+'.txt')).read_text(encoding='utf-8',errors='replace')[-4500:],flush=True)
  break
(BASE/'build-check.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
if results[-1]['returncode']:raise SystemExit(1)
print('DIFF_COMPILED',build/'thesis-diff.pdf',flush=True)
