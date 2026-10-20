"""Pass transient selection into the renderer, without changing saved appearance."""
from pathlib import Path
import hashlib
import json

root=Path(__file__).resolve().parents[2]
app=root/'outputs/Mechanical_Design_App'
p=app/'rack-references/rack-studio.js';s=p.read_text(encoding='utf-8')
changes=[
    ("kind:key,slot:allocation.slot,color:rgb(color)","kind:key,slot:allocation.slot,selected:key==='plate'&&selectedSlot>=allocation.slot&&selectedSlot<allocation.slot+allocation.span,color:rgb(color)"),
    ('draw(scene,meshes,view,width,height,rack){','draw(scene,meshes,view,width,height,rack,selectedSlot=null){'),
    ('objects=this.objects(scene,meshes,rack),','objects=this.objects(scene,meshes,rack,selectedSlot),'),
    ("g.uniform3fv(this.loc(p,'uColor'),o.color);","g.uniform1f(this.loc(p,'uSelected'),o.selected?1:0);g.uniform3fv(this.loc(p,'uColor'),o.color);"),
]
for old,new in changes:
    assert s.count(old)==1,old
    s=s.replace(old,new)
p.write_text(s,encoding='utf-8')
p=app/'workspace.js';s=p.read_text(encoding='utf-8')
old='sceneRenderer.draw(scene,sourceMeshes,view,Math.round(w*dpr),Math.round(h*dpr),rack)'
assert s.count(old)==1
s=s.replace(old,old[:-1]+',selectedSlot)')
p.write_text(s,encoding='utf-8')
data=root/'data/normal-use'
hashes={str(p.relative_to(data)):hashlib.sha256(p.read_bytes()).hexdigest() for p in data.rglob('*') if p.is_file()}
(Path(__file__).parent/'Data_Before.json').write_text(json.dumps(hashes,indent=2),encoding='utf-8')
