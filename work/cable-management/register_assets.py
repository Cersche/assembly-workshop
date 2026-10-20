"""Refresh SHA-256 entries for the files cable-management Step 1 changed, and add the local cable guide mesh.

Run once from anywhere: python -I register_assets.py. Touches only rack-references/asset-manifest.json.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2] / 'outputs/Mechanical_Design_App/rack-references'
p = ROOT / 'asset-manifest.json'
entries = json.loads(p.read_text(encoding='utf-8'))
digest = lambda name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
for entry in entries:
    if entry['file'] in ('rack-studio.js', 'rack-scene.js'):
        entry['sha256'] = digest(entry['file'])
if not any(e['file'] == 'cable_guide.json' for e in entries):
    # Lab Rax Cable Guide, MakerWorld Exclusive License: local preview only, never redistributed.
    entries.append({'url': '/rack-references/cable_guide.json', 'file': 'cable_guide.json',
                    'mime': 'application/json', 'sha256': digest('cable_guide.json')})
p.write_text(json.dumps(entries, indent=2) + '\n', encoding='utf-8')
print('manifest entries:', len(entries))
