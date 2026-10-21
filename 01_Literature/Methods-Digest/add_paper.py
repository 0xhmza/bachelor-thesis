"""Append an additional work to registry.json (numbers continue after the catalogue).

usage: python add_paper.py '<json object>'
Required keys: key, label, authors, year, title, venue, stages (list), pdf (repo-relative path).
Optional: doi, url, pages [first,last], priority, version, found_in (why it was added).
"""
import json
import sys
from pathlib import Path

reg_path = Path(__file__).with_name("registry.json")
reg = json.loads(reg_path.read_text(encoding="utf-8"))
new = json.loads(sys.argv[1])
if any(e["key"] == new["key"] for e in reg):
    sys.exit(f"key {new['key']} already registered")
entry = {
    "num": max(e["num"] for e in reg) + 1, "list_id": "add", "priority": new.pop("priority", ""),
    "category": "Additions", "doi": None, "url": None, "pages": None, "when": "", "use": "",
    "caution": "", "version": "",
}
entry.update(new)
entry["when"] = entry["when"] or "/".join(entry["stages"])
if not (Path(__file__).resolve().parents[2] / entry["pdf"]).exists():
    sys.exit(f"missing file {entry['pdf']}")
reg.append(entry)
reg_path.write_text(json.dumps(reg, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"[{entry['num']}] {entry['key']} added")
