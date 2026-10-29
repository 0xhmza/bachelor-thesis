"""Append an immutable code/decision snapshot and publish a bundle hash manifest."""
import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

def main(run):
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    snapshot = run / ('derivation_' + stamp)
    snapshot.mkdir()
    for folder in ['scripts', 'config']:
        for src in sorted((BASE / folder).glob('*')):
            if src.is_file():
                dest = snapshot / folder / src.name
                dest.parent.mkdir(exist_ok=True)
                with dest.open('xb') as f:
                    f.write(src.read_bytes())
    records = []
    for folder in ['config', 'scripts', 'raw', 'processed']:
        for p in sorted((BASE / folder).rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts:
                records.append({'path': p.relative_to(BASE).as_posix(), 'bytes': p.stat().st_size,
                                'sha256': hashlib.sha256(p.read_bytes()).hexdigest()})
    for name in ['README.md', 'data_dictionary.md', 'report.md', 'report.pdf']:
        p = BASE / name
        records.append({'path': name, 'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()})
    manifest = {'created_utc': datetime.now(timezone.utc).isoformat(), 'run': run.name,
                'derivation_snapshot': snapshot.relative_to(BASE).as_posix(),
                'scope': 'Raw evidence, processing inputs, scripts, tables and delivered report; QA previews excluded',
                'files': records}
    text = json.dumps(manifest, ensure_ascii=False, indent=2)
    with (snapshot / 'bundle_manifest.json').open('x', encoding='utf-8') as f:
        f.write(text)
    (BASE / 'bundle_manifest.json').write_text(text, encoding='utf-8')
    print(json.dumps({'archived_files': len(records), 'snapshot': str(snapshot)}, indent=2))

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('run', type=Path)
    main(p.parse_args().run.resolve())
