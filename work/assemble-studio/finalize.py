"""Register final authored rendering assets; preserve original rack lock."""
from pathlib import Path
import hashlib
import json
root=Path(__file__).resolve().parents[2]/'outputs/Mechanical_Design_App'
p=root/'viewer.js';s=p.read_text(encoding='utf-8').replace("onclick=()=>{frontMode=false;yaw=.55;pitch=.65;focus=", "onclick=()=>{frontMode=false;yaw=studioRenderer?-.55:.55;pitch=.65;focus=")
p.write_text(s,encoding='utf-8')
p=root/'index.html';s=p.read_text(encoding='utf-8').replace('Selected hardware · copper / gold','Selected hardware · preview envelopes');p.write_text(s,encoding='utf-8')
folder=root/'rack-references'
assert hashlib.sha256((folder/'rack-scene.js').read_bytes()).hexdigest()=='414214bcbf3f1f40ff7a6be0791741ec721cb3d9585cc4d148b1c68f7ff1c7d2'
p=folder/'asset-manifest.json';entries=json.loads(p.read_text(encoding='utf-8'))
for name in ['rack-studio.js','assembly-studio.js']:next(e for e in entries if e['file']==name)['sha256']=hashlib.sha256((folder/name).read_bytes()).hexdigest()
p.write_text(json.dumps(entries,indent=2)+'\n',encoding='utf-8')
print('PASS authored asset hashes registered; original rack script unchanged.')
