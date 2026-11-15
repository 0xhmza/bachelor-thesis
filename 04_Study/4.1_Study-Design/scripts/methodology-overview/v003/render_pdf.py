"""Render every methodology overview (HTML) in 04_Study/4.1_Study-Design to a one-page PDF.

    python 04_Study/4.1_Study-Design/scripts/methodology-overview/v003/render_pdf.py [preview-folder]

v003: a page marked data-paper="A4" is printed on one A4 page, scaled down only if it would
not fit; any other page gets one page as large as the drawing (as in v002). Each PDF is
written next to its source. With a folder argument, a PNG preview of each is written there.
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[5]
FOLDER = ROOT / "04_Study" / "4.1_Study-Design"
PREVIEW = Path(sys.argv[1]) if len(sys.argv) > 1 else None
A4_PX = (794, 1123)  # 210 x 297 mm at 96 px per inch


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge")
        for src in sorted(FOLDER.glob("*.html")):
            page = browser.new_page(viewport={"width": 1720, "height": 1200})
            page.goto(src.as_uri())
            page.wait_for_selector("body[data-drawn='1']", state="attached")
            width = page.evaluate("document.querySelector('.page').scrollWidth")
            height = page.evaluate("document.querySelector('.page').scrollHeight")
            paper = page.evaluate("document.querySelector('.page').dataset.paper || ''")
            out = src.with_suffix(".pdf")
            margin = {"top": "0", "right": "0", "bottom": "0", "left": "0"}
            if paper == "A4":
                scale = min(1.0, A4_PX[0] / width, (A4_PX[1] - 2) / height)
                page.pdf(path=str(out), format="A4", scale=scale, print_background=True,
                         margin=margin, page_ranges="1")
                size = f"A4, scale {scale:.2f}"
            else:
                page.pdf(path=str(out), width=f"{width}px", height=f"{height + 2}px",
                         print_background=True, margin=margin)
                size = f"{width} x {height} px"
            if PREVIEW:
                page.set_viewport_size({"width": width, "height": 1200})
                page.screenshot(path=str(PREVIEW / f"{src.stem}.png"), full_page=True)
            page.close()
            print(f"{out.relative_to(ROOT)}: {size} (drawing {width} x {height} px)")
        browser.close()


if __name__ == "__main__":
    main()
