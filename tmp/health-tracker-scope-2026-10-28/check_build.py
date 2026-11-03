from pathlib import Path
import subprocess,json

root=Path(__file__).resolve().parent
cwd=root/'build-tree/03_Thesis'
commands=[('pdflatex-1',['C:/texlive/2026/bin/windows/pdflatex.exe','-interaction=nonstopmode','-halt-on-error','thesis.tex']),('biber',['C:/texlive/2026/bin/windows/biber.exe','thesis']),('pdflatex-2',['C:/texlive/2026/bin/windows/pdflatex.exe','-interaction=nonstopmode','-halt-on-error','thesis.tex']),('pdflatex-3',['C:/texlive/2026/bin/windows/pdflatex.exe','-interaction=nonstopmode','-halt-on-error','thesis.tex'])]
results=[]
for label,cmd in commands:
 print(label+' started',flush=True)
 with (root/(label+'.txt')).open('w',encoding='utf-8') as log:
  r=subprocess.run(cmd,cwd=cwd,stdout=log,stderr=subprocess.STDOUT)
 results.append(dict(stage=label,returncode=r.returncode))
 print(label+' exit '+str(r.returncode),flush=True)
 if r.returncode:break
(root/'build-check.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
if results[-1]['returncode']:
 print((root/(results[-1]['stage']+'.txt')).read_text(encoding='utf-8',errors='replace')[-4500:],flush=True)
