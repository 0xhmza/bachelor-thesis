"""Render the methodology overview (HTML) to a one-page PDF with Microsoft Edge.

    python 04_Study/4.1_Study-Design/scripts/methodology-overview/v001/render_pdf.py [preview.png]

Reads  04_Study/4.1_Study-Design/methodology-overview.html
Writes 04_Study/4.1_Study-Design/methodology-overview.pdf (next to its source, like the
review copy of the thesis), one page as tall as the drawing.
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[5]
SRC = ROOT / "04_Study" / "4.1_Study-Design" / "methodology-overview.html"
OUT = SRC.with_suffix(".pdf")
PREVIEW = Path(sys.argv[1]) if len(sys.argv) > 1 else None  # optional PNG for checking the layout


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge")
        page = browser.new_page(viewport={"width": 1720, "height": 1200})
        page.goto(SRC.as_uri())
        page.wait_for_selector("body[data-drawn='1']", state="attached")
        width = page.evaluate("document.querySelector('.page').scrollWidth")
        height = page.evaluate("document.querySelector('.page').scrollHeight")
        page.pdf(path=str(OUT), width=f"{width}px", height=f"{height + 2}px", print_background=True,
                 margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
        if PREVIEW:
            page.screenshot(path=str(PREVIEW), full_page=True)
        browser.close()
    print(f"{OUT.relative_to(ROOT)}: {width} x {height} px")


if __name__ == "__main__":
    main()
