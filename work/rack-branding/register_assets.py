from pathlib import Path
import hashlib
import json
ROOT = Path(__file__).resolve().parents[2] / 'outputs/Mechanical_Design_App/rack-references'
p = ROOT / 'asset-manifest.json'
entries = json.loads(p.read_text(encoding='utf-8'))
for entry in entries:
    if entry['file'] == 'rack-studio.js':
        entry['sha256'] = hashlib.sha256((ROOT / entry['file']).read_bytes()).hexdigest()
assert not any(e['file'] == 'rack-logo-faces.json' for e in entries)
entries.append({'url': '/rack-references/rack-logo-faces.json', 'file': 'rack-logo-faces.json',
                'mime': 'application/json', 'sha256': hashlib.sha256((ROOT / 'rack-logo-faces.json').read_bytes()).hexdigest()})
p.write_text(json.dumps(entries, indent=2) + '\n', encoding='utf-8')
