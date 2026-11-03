from pathlib import Path
import os,subprocess,json,sys
sys.stdout.reconfigure(encoding='utf-8')
BASE=Path(__file__).resolve().parents[1]/'tmp/thesis-diff-2026-10-28';build=BASE/'new/03_Thesis'
env=os.environ.copy();env['LC_ALL']='C';env['LANG']='C'
results=[]
for label,exe,args in [('pdflatex-1','pdflatex.exe',['-interaction=nonstopmode','-halt-on-error','thesis-diff.tex']),('biber','biber.exe',['thesis-diff']),('pdflatex-2','pdflatex.exe',['-interaction=nonstopmode','-halt-on-error','thesis-diff.tex']),('pdflatex-3','pdflatex.exe',['-interaction=nonstopmode','-halt-on-error','thesis-diff.tex'])]:
 print(label+' started',flush=True)
 with (BASE/(label+'.txt')).open('wb') as f:r=subprocess.run(['C:/texlive/2026/bin/windows/'+exe]+args,cwd=build,stdout=f,stderr=subprocess.STDOUT,env=env)
 results.append(dict(stage=label,returncode=r.returncode));print(label+' exit '+str(r.returncode),flush=True)
 if r.returncode:
  print((BASE/(label+'.txt')).read_text(encoding='utf-8',errors='replace')[-5000:],flush=True);break
(BASE/'build-check.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
raise SystemExit(results[-1]['returncode'])
