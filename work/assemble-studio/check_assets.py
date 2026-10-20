"""Check delivery of studio inspection modules and preservation of prior assets."""
from pathlib import Path
import hashlib
import json
import sys
root=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(root/'outputs/Mechanical_Design_App'))
import rack_references
folder=rack_references.ROOT
before=json.loads((Path(__file__).parent/'before-app/asset-manifest.json').read_text(encoding='utf-8'))
current=json.loads((folder/'asset-manifest.json').read_text(encoding='utf-8'))
for item in before:
    if item['file']!='rack-studio.js':assert next(e for e in current if e['file']==item['file'])==item
assert {e['file'] for e in current}-{e['file'] for e in before}=={'assembly-studio.js'}
for name in ['rack-studio.js','assembly-studio.js']:
    assert rack_references.asset('/rack-references/'+name)[0]==(folder/name).read_bytes()
assert hashlib.sha256((folder/'rack-scene.js').read_bytes()).hexdigest()=='414214bcbf3f1f40ff7a6be0791741ec721cb3d9585cc4d148b1c68f7ff1c7d2'
print('PASS both authored modules served through integrity checks; all other reference entries and original rack hash unchanged.')
