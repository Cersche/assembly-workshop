from pathlib import Path
import json,hashlib
app=Path(r'D:\Projects\assembly-workshop\outputs\Mechanical_Design_App')
def change(f,a,b):
 p=app/f;t=p.read_text(encoding='utf-8');assert a in t,(f,a);p.write_text(t.replace(a,b),encoding='utf-8',newline='\n')
# The template's existing tapered rails reach Y=22, beyond the blocks/uprights at 11.3.
change('equipment.py',"y0<11.3 and y1>0 for x in joints)","((y0<11.3 and y1>0) or (y0<22 and y1>9 and any(x0<x+side*6+1 and x1>x+side*6-1 for side in (-1,1)))) for x in joints)")
change('equipment_tray.scad','q[1]<11.3&&q[3]>0)x]', '(q[1]<11.3&&q[3]>0||q[1]<22&&q[3]>9&&len([for(side=[-1,1])if(q[0]<x+side*6+1&&q[2]>x+side*6-1)side])>0))x]')
change('tray-placement.js',"q[1]<11.3&&q[3]>0))?WALL_MESSAGE", "(q[1]<11.3&&q[3]>0||q[1]<22&&q[3]>9&&[-1,1].some(side=>q[0]<x+side*6+1&&q[2]>x+side*6-1))))?WALL_MESSAGE")
change('tray-placement.js','problems(state.item.spec,state.v);','problems(state.item.spec,state.v,!!state.second);')
# The orange edge must show the device-local front when wall openings rotate with it.
change('tray-placement.js',"v:box(L.dev_x,L.dev_y-0.2,L.lift,L.dev_x+L.fp_w,L.dev_y+0.8,L.lift+ +spec.dev_h)","v:(()=>{const p=dp(spec,v.dev_rot,[0,-.2]),q=dp(spec,v.dev_rot,[+spec.dev_w,.8]);return box(L.dev_x+Math.min(p[0],q[0]),L.dev_y+Math.min(p[1],q[1]),L.lift,L.dev_x+Math.max(p[0],q[0]),L.dev_y+Math.max(p[1],q[1]),L.lift+ +spec.dev_h);})()")
change('test_wall_mount.py','dev_off_y=2','dev_off_y=13')
change('js-tests/wall-mount.js','dev_off_y:2','dev_off_y:13')
change('js-tests/wall-mount.js','v.dev_off_y=2','v.dev_off_y=13')
change('test_tray_placement.py','for mount in eq.MOUNTS:',"for mount in (m for m in eq.MOUNTS if m != 'wall'):  # archived templates predate wall")
change('test_allocation_tray.py',"'dev_rot', 'device_mount', 'standoff',","'dev_rot', 'device_mount', 'wall_open', 'standoff',")
p=app/'asset-manifest.json';m=json.loads(p.read_text(encoding='utf-8'))
for row in m:
 f=app/row['file']
 if f.exists():row['sha256']=hashlib.sha256(f.read_text(encoding='utf-8').encode()).hexdigest()
p.write_text(json.dumps(m,indent=1)+'\n',encoding='utf-8')
print('Joint rails screened; archived test mount sets limited to legacy mounts')
