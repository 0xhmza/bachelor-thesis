"""Render every report page and check content/bounds; requires PyMuPDF and Pillow."""
import json
from pathlib import Path
import fitz
from PIL import Image, ImageDraw

BASE = Path(__file__).resolve().parents[1]
qa = BASE / 'qa'
qa.mkdir(exist_ok=True)
doc = fitz.open(BASE / 'report.pdf')
issues, thumbs, all_text = [], [], ''
for i, page in enumerate(doc, 1):
    text = page.get_text()
    all_text += text
    if len(text.strip()) < 80:
        issues.append(f'Page {i}: suspiciously little text')
    for word in page.get_text('words'):
        x0, y0, x1, y1 = word[:4]
        if x0 < 25 or x1 > page.rect.width - 25 or y0 < 15 or y1 > page.rect.height - 12:
            issues.append(f'Page {i}: text outside safe page bounds: {word[4]}')
    pix = page.get_pixmap(matrix=fitz.Matrix(1.25, 1.25), alpha=False)
    pix.save(qa / f'page-{i:02}.png')
    img = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
    img.thumbnail((280, 396))
    card = Image.new('RGB', (300, 427), '#dce4e8')
    card.paste(img, ((300 - img.width) // 2, 10))
    ImageDraw.Draw(card).text((12, 408), f'Page {i}', fill='#12344b')
    thumbs.append(card)
for start in range(0, len(thumbs), 6):
    group = thumbs[start:start + 6]
    sheet = Image.new('RGB', (900, 427 * ((len(group) + 2) // 3)), 'white')
    for j, thumb in enumerate(group):
        sheet.paste(thumb, ((j % 3) * 300, (j // 3) * 427))
    sheet.save(qa / f'contact-{start // 6 + 1}.png')
for term in ['202', '30 fitness', '20 fertility', 'Clue', 'Alpha Progression', 'BfArM', 'not frozen']:
    if term not in all_text:
        issues.append('Missing expected content: ' + term)
(qa / 'report-extracted.txt').write_text(all_text, encoding='utf-8')
(qa / 'report-checks.json').write_text(json.dumps({'pages': len(doc), 'issues': issues, 'all_pages_rendered': True}, indent=2), encoding='utf-8')
print(json.dumps({'pages': len(doc), 'issues': issues}, indent=2))
if issues:
    raise SystemExit(1)
