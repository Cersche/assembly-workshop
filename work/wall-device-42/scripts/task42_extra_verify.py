from pathlib import Path
import json,sys,subprocess,hashlib
root=Path(r'D:\Projects\assembly-workshop');app=root/'outputs/Mechanical_Design_App';out=root/'work/wall-device-42'
sys.path.insert(0,str(app));import equipment as eq,mesh_revision as mr
# Compare every side, each rotation and dimension thresholds across Python and JavaScript.
raws=[]
for w,d,h in [(90.7,90.4,25.4),(29,39,8),(30,40,3)]:
 for rot in (0,90,180,270):
  for side in eq.WALL_SIDES:
   raws.append(dict(name='Mirror',dev_w=w,dev_d=d,dev_h=h,device_mount='wall',wall_open=[side],dev_rot=rot,dev_off_y=13,joint='single'))
node=Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
script="const T=require(process.argv[1]);const fs=require('fs'),ss=JSON.parse(fs.readFileSync(0,'utf8'));console.log(JSON.stringify(ss.map(s=>T.wallBoxes(s,T.values(s)))));"
r=subprocess.run([str(node),'-e',script,str(app/'tray-placement.js')],input=json.dumps(raws),capture_output=True,text=True,encoding='utf-8',check=True)
js=json.loads(r.stdout)
for raw,boxes in zip(raws,js):
 py=eq.wall_rectangles(eq.clean(raw))
 assert len(py)==len(boxes)
 assert all(abs(a-b)<1e-8 for p,q in zip(py,boxes) for a,b in zip(p,q)),raw
(out/'mirror-results.json').write_text(json.dumps({'cases':len(raws),'result':'all coordinates agree within 1e-8 mm','dimensions':[[90.7,90.4,25.4],[29,39,8],[30,40,3]],'rotations':[0,90,180,270],'open_sides':eq.WALL_SIDES},indent=2),encoding='utf-8')
print('48 Python/JS wall geometry cases agree')
# Check SCAD guards through CSG evaluation, no proposed export from failed checks.
s=eq.clean(raws[0]);src=eq.source(s)
checks=[]
for name,override,message in [('none','wall_open=[];','Open sides'),('all','wall_open=["front","rear","left","right"];','Open sides'),('unknown','wall_open=["back"];','Open sides'),('clash','wall_open=["rear"];joint="screw";dev_off_y=1;','wall would hit')]:
 p=out/(name+'-guard.scad');p.write_text(src+'\n'+override,encoding='utf-8')
 rr=subprocess.run([mr.compiler(),'-o',str(out/(name+'-guard.csg')),str(p)],capture_output=True,text=True,encoding='utf-8')
 assert message in rr.stderr,(name,rr.stderr)
 checks.append(dict(name=name,assertion=message,passed=True))
(out/'scad-guards.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
# Measure notch and thickness planes independently from the exact single STL.
rr=json.loads((out/'renders.json').read_text(encoding='utf-8'))
single=next(x for x in rr if x['label']=='single');s=single['spec'];m=mr.read_mesh(root/single['folder']/'tray.stl','tray');fx,_,fy,_=eq.footprint(s);floor=eq.floor_z(s)+3
verts=[[p[0]-fx,p[1]-fy,p[2]-floor] for p in m['vertices']]
notch=[p for p in verts if abs(p[2]-4)<.001 and abs(p[0]+.5)<.001 and abs(p[1]-s['dev_d']/2)<=10.001]
assert len(notch)>=2
measure=dict(notch_width_mm=round(max(p[1] for p in notch)-min(p[1] for p in notch),4),notch_bottom_above_floor_mm=4,
 wall_thickness_mm=round(single['measurements']['x_section'][1]-single['measurements']['x_section'][0],4),
 corner_return_along_inner_edge_mm=round(single['measurements']['rear_section'][1]-single['measurements']['x_section'][1],4))
(out/'extra-measurements.json').write_text(json.dumps(measure,indent=2),encoding='utf-8');print(measure)
# Verify browser Save persisted independent arrays and did not change its library defaults.
doc=json.loads((out/'browser-data/rack-workspace.json').read_text(encoding='utf-8'));p=doc['racks'][0]['placements'][0]
assert p['tray']['wall_open']==['front','rear'];assert p['second']['tray']['wall_open']==['rear','right']
assert all(i['spec']['device_mount']=='straps' for i in json.loads((out/'browser-data/equipment-library.json').read_text(encoding='utf-8')))
print('Browser saved both wall settings; synthetic library defaults remain straps')
# Complete before/after legacy source record, re-evaluated after final SCAD changes.
rows=json.loads((out/'legacy-before.json').read_text(encoding='utf-8'))
for row in rows:
 row['after']=hashlib.sha256(eq.source(eq.clean(row['spec'])).encode('utf-8')).hexdigest();assert row['after']==row['before'],row['label']
(out/'legacy-results.json').write_text(json.dumps(rows,indent=2),encoding='utf-8');print('20/20 legacy SHA-256 unchanged')
