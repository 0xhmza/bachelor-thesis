"""Render translucent line highlights over latexdiff's exact red/green text."""
from pathlib import Path
from collections import defaultdict,Counter
import json,io,hashlib,sys
from pypdf import PdfReader,PdfWriter
import pdfplumber
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'tmp/thesis-diff-2026-10-28'
SOURCE=BASE/'new/03_Thesis/thesis-diff.pdf'
OUT=ROOT/'output/pdf';OUT.mkdir(parents=True,exist_ok=True)
manifest=json.loads((BASE/'manifest.json').read_text(encoding='utf-8'))

# Normalize rotated landscape pages before measuring rendered coordinates.
reader=PdfReader(SOURCE);normal=PdfWriter();normal.clone_document_from_reader(reader)
for p in normal.pages:
 if p.rotation:p.transfer_rotation_to_content()
normpath=BASE/'normalized-diff.pdf'
with normpath.open('wb') as f:normal.write(f)
writer=PdfWriter();writer.clone_document_from_reader(PdfReader(normpath))
targets={'added':(0,.42,0),'deleted':(.72,0,0)}
bg={'added':(.58,.96,.58),'deleted':(1,.57,.57)}
counts=Counter();page_stats=[]
with pdfplumber.open(normpath) as pdf:
 for n,page in enumerate(pdf.pages):
  selected=defaultdict(list)
  for ch in page.chars:
   color=ch.get('non_stroking_color')
   if not isinstance(color,(tuple,list)) or len(color)!=3:continue
   if not ch['text'].strip():continue
   for kind,rgb in targets.items():
    if max(abs(float(a)-b) for a,b in zip(color,rgb))<.003:
     selected[kind].append(ch);counts[kind+'_chars']+=1;break
  if not selected:continue
  stream=io.BytesIO();c=canvas.Canvas(stream,pagesize=(page.width,page.height));c.setFillAlpha(.25)
  rects=[]
  for kind,chars in selected.items():
   lines=[]
   for ch in sorted(chars,key=lambda ch:(round(ch['top']/2),ch['x0'])):
    line=next((line for line in reversed(lines[-4:]) if abs(line[0]['top']-ch['top'])<2.5),None)
    if line is None:line=[];lines.append(line)
    line.append(ch)
   c.setFillColor(colors.Color(*bg[kind]));c.setFillAlpha(.25)
   for line in lines:
    runs=[]
    for ch in sorted(line,key=lambda x:x['x0']):
     if runs and ch['x0']-runs[-1][-1]['x1']<=max(5,ch['size']*.65):runs[-1].append(ch)
     else:runs.append([ch])
    for run in runs:
     x0=min(x['x0'] for x in run)-.6;x1=max(x['x1'] for x in run)+.6
     top=min(x['top'] for x in run)-.6;bottom=max(x['bottom'] for x in run)+.6
     c.rect(x0,page.height-bottom,x1-x0,bottom-top,fill=1,stroke=0)
     counts[kind+'_highlight_spans']+=1
     rects.append(dict(kind=kind,box=[x0,top,x1,bottom],text=''.join(x['text'] for x in run)))
  c.save();stream.seek(0)
  writer.pages[n].merge_page(PdfReader(stream).pages[0],over=True)
  page_stats.append(dict(thesis_pdf_page=n+1,output_page=n+2,spans=rects))
assert counts['added_chars']>0 and counts['deleted_chars']>0

# A concise legend makes comparison provenance explicit.
pdfmetrics.registerFont(TTFont('Legend','C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('LegendBold','C:/Windows/Fonts/arialbd.ttf'))
legend=io.BytesIO();c=canvas.Canvas(legend,pagesize=(595.28,841.89))
c.setFillColor(colors.HexColor('#183b56'));c.setFont('LegendBold',24);c.drawString(52,747,'Thesis - review of changes')
c.setFillColor(colors.HexColor('#47576b'));c.setFont('Legend',11)
c.drawString(52,718,'28 October 2026 | Full thesis comparison')
c.setFont('LegendBold',12);c.setFillColor(colors.HexColor('#203047'));c.drawString(52,667,'How to read this copy')
for y,kind,label in [(625,'deleted','Deleted text - red'),(580,'added','Added text - green')]:
 c.setFillColor(colors.Color(*bg[kind]));c.rect(52,y-8,270,28,fill=1,stroke=0)
 c.setFillColor(colors.Color(*targets[kind]));c.setFont('LegendBold',12);c.drawString(61,y+1,label)
c.setFillColor(colors.HexColor('#203047'));c.setFont('Legend',10.5)
lines=[
 'Comparison: last committed thesis versus the saved working-tree snapshot.',
 'Baseline commit: '+manifest['baseline'][:12],
 'Snapshot: '+manifest['current_snapshot_utc'],
 '',
 'All saved changes are included, including the literature rewrite and the',
 'health-tracker scope clarification. Unchanged text retains its normal style.',
 '',
 'Running text is compared at word level. Changed tables and figures appear',
 'as intact old and new blocks so their layouts remain readable.',
 '',
 'This is a review copy containing both old and new text. The thesis sources',
 'and the open source document were not edited to create it.'
]
for i,line in enumerate(lines):c.drawString(52,532-i*17,line)
c.setStrokeColor(colors.HexColor('#c6d4df'));c.line(52,72,543,72)
c.setFont('Legend',9);c.setFillColor(colors.HexColor('#566578'));c.drawString(52,54,'Change legend | Original thesis begins on the next page')
c.save();legend.seek(0)
writer.insert_page(PdfReader(legend).pages[0],index=0)
writer.add_metadata({'/Title':'Thesis diff - red deletions, green additions - 28 October 2026','/Subject':'Last committed thesis versus saved working tree; baseline '+manifest['baseline'],'/Author':'Hamza Sghaier'})
dest=OUT/'Thesis_Diff_2026-10-28.pdf'
with dest.open('wb') as f:writer.write(f)

manifest['highlight_counts']=dict(counts);manifest['output_pages']=len(writer.pages)
manifest['changed_pages']=[x['output_page'] for x in page_stats]
manifest['output_sha256']=hashlib.sha256(dest.read_bytes()).hexdigest()
manifest['source_hash_changes_during_build']=[p for p,h in manifest['production_hashes'].items() if not (ROOT/p).exists() or hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
(BASE/'highlight-map.json').write_text(json.dumps(page_stats,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(BASE/'final-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
(OUT/'Thesis_Diff_2026-10-28.txt').write_text('Thesis diff, 28 October 2026\nBaseline: '+manifest['baseline']+'\nSnapshot UTC: '+manifest['current_snapshot_utc']+'\nDeleted text: red. Added text: green. Changed tables/figures are shown as intact old/new blocks.\nNo source files were edited by this PDF generation.\n',encoding='utf-8')
print(json.dumps({k:manifest[k] for k in ['highlight_counts','output_pages','changed_pages','source_hash_changes_during_build']},indent=2))
print(dest)
