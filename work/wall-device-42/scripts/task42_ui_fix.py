from pathlib import Path
import json,hashlib
app=Path(r'D:\Projects\assembly-workshop\outputs\Mechanical_Design_App')
p=app/'tray-placement.js';t=p.read_text(encoding='utf-8').replace("return h('label',{},input,side[0]","return h('label',{class:'ew-chip'},input,' '+side[0]")
t=t.replace("?[h('p',{},'Open sides (cables):'),...WALL_SIDES.map", "?[h('p',{},'Open sides (cables):'),h('div',{class:'ew-row'},...WALL_SIDES.map")
t=t.replace("side.slice(1));}),h('p',{class:'ew-note'},'Device sits", "side.slice(1));})),h('p',{class:'ew-note'},'Device sits")
p.write_text(t,encoding='utf-8',newline='\n')
p=app/'asset-manifest.json';m=json.loads(p.read_text(encoding='utf-8'))
for r in m:
 f=app/r['file']
 if f.exists():r['sha256']=hashlib.sha256(f.read_text(encoding='utf-8').encode()).hexdigest()
p.write_text(json.dumps(m,indent=1)+'\n',encoding='utf-8')
print('compact checkbox row applied')
