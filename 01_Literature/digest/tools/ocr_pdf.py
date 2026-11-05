"""Add an invisible OCR text layer to a scanned PDF. usage: ocr_pdf.py in.pdf out.pdf"""
import sys
import fitz
import numpy as np
from rapidocr_onnxruntime import RapidOCR

src, dst = sys.argv[1], sys.argv[2]
ocr = RapidOCR()
doc = fitz.open(src)
DPI = 200
k = 72 / DPI
for pno, page in enumerate(doc):
    if len(page.get_text().strip()) > 200:
        continue
    pix = page.get_pixmap(dpi=DPI)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)[:, :, :3]
    res, _ = ocr(img)
    res = res or []
    # reading order: top to bottom, left to right within a line
    items = []
    for box, text, conf in res:
        xs = [p[0] for p in box]
        ys = [p[1] for p in box]
        items.append((min(ys), min(xs), max(ys), text))
    items.sort(key=lambda t: (round(t[0] / 12), t[1]))
    for top, left, bottom, text in items:
        h = max(4.0, (bottom - top) * k)
        page.insert_text((left * k, bottom * k - h * 0.2), text, fontsize=h * 0.9, render_mode=3)
    print(pno + 1, len(items), flush=True)
doc.save(dst, garbage=3, deflate=True)
