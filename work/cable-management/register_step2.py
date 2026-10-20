"""Refresh the rack-studio.js SHA-256 after cable-management Step 2 (port markers, pickPort).

Run once from anywhere: python -I register_step2.py. Touches only rack-references/asset-manifest.json.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2] / 'outputs/Mechanical_Design_App/rack-references'
p = ROOT / 'asset-manifest.json'
entries = json.loads(p.read_text(encoding='utf-8'))
for entry in entries:
    if entry['file'] == 'rack-studio.js':
        entry['sha256'] = hashlib.sha256((ROOT / entry['file']).read_bytes()).hexdigest()
        print('rack-studio.js ->', entry['sha256'])
p.write_text(json.dumps(entries, indent=2) + '\n', encoding='utf-8')
