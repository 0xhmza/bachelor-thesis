"""Block-wise text of registry papers, for reading and for choosing \\pc snippets.

usage (from anywhere):  python tools/blocks.py key [key ...]
Writes text-cache/<num3>_<key>.txt with '=== PAGE n ===' markers where n is the page
number *relative to the appended copy* (the number to use in \\pc{key}{n}{...}).
The text layer is what build_digest.py matches against, so pick snippets from this file.
"""
import json
import pathlib
import re
import sys

import fitz  # PyMuPDF

here = pathlib.Path(__file__).resolve().parent.parent          # .../Methods-Digest
root = here.parent.parent                                      # repository root
reg = {e["key"]: e for e in json.loads((here / "registry.json").read_text(encoding="utf-8"))}
out_dir = here / "text-cache"
out_dir.mkdir(exist_ok=True)

for key in sys.argv[1:]:
    e = reg[key]
    p = pathlib.Path(e["pdf"])
    if not p.is_absolute():
        p = root / p
    doc = fitz.open(p)
    lo, hi = e["pages"] or [1, doc.page_count]
    out = out_dir / f"{str(e['num']).zfill(3)}_{key}.txt"
    with open(out, "w", encoding="utf-8") as fh:
        for rel, i in enumerate(range(lo - 1, hi), start=1):
            fh.write(f"=== PAGE {rel} ===\n")
            for b in doc[i].get_text("blocks", sort=False):
                if b[6] != 0:
                    continue
                t = re.sub(r"\s+", " ", b[4]).strip()
                if t:
                    fh.write(t + "\n")
    print(key, out.name, out.stat().st_size, hi - lo + 1, "pages")
