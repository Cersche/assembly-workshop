"""Explicitly register this authored renderer; retain the original rack hash lock."""
from pathlib import Path
import json
import hashlib

root=Path(__file__).resolve().parents[2]/'outputs/Mechanical_Design_App/rack-references'
original='414214bcbf3f1f40ff7a6be0791741ec721cb3d9585cc4d148b1c68f7ff1c7d2'
assert hashlib.sha256((root/'rack-scene.js').read_bytes()).hexdigest()==original
manifest=root/'asset-manifest.json'
entries=json.loads(manifest.read_text(encoding='utf-8'))
entry=next(e for e in entries if e['file']=='rack-studio.js')
entry['sha256']=hashlib.sha256((root/'rack-studio.js').read_bytes()).hexdigest()
manifest.write_text(json.dumps(entries,indent=2)+'\n',encoding='utf-8')
print('Renderer registered:',entry['sha256'],'; original rack hash unchanged.')
