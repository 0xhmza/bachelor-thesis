"""Render every methodology overview (HTML) in 04_Study/4.1_Study-Design to a one-page PDF.

    python scripts/methodology-overview/v002/render_pdf.py [preview-folder]

v002 renders all HTML files of the folder (the detailed and the simple version); v001
rendered the detailed one only. Each PDF is written next to its source, one page as tall
as the drawing. With a folder argument, a PNG preview of each is written there too.
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[3]
FOLDER = ROOT / "04_Study" / "4.1_Study-Design"
PREVIEW = Path(sys.argv[1]) if len(sys.argv) > 1 else None


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge")
        for src in sorted(FOLDER.glob("*.html")):
            page = browser.new_page(viewport={"width": 1720, "height": 1200})
            page.goto(src.as_uri())
            page.wait_for_selector("body[data-drawn='1']", state="attached")
            width = page.evaluate("document.querySelector('.page').scrollWidth")
            height = page.evaluate("document.querySelector('.page').scrollHeight")
            out = src.with_suffix(".pdf")
            page.pdf(path=str(out), width=f"{width}px", height=f"{height + 2}px", print_background=True,
                     margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
            if PREVIEW:
                page.set_viewport_size({"width": width, "height": 1200})
                page.screenshot(path=str(PREVIEW / f"{src.stem}.png"), full_page=True)
            page.close()
            print(f"{out.relative_to(ROOT)}: {width} x {height} px")
        browser.close()


if __name__ == "__main__":
    main()
