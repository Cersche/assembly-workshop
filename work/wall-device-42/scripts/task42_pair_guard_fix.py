from pathlib import Path
import json,hashlib
app=Path(r'D:\Projects\assembly-workshop\outputs\Mechanical_Design_App')
p=app/'tray-pair.js';t=p.read_text(encoding='utf-8');a="if(v1.joint==='screw'){const j=PO().jointPositions([...p1,...p2],ks,H);if(j.problem)out.push(j.problem);for(const [sp,v] of [[spec1,v1],[spec2,m]]){const wp=T().wallProblem(sp,v,j.joints);if(wp&&!out.includes(wp))out.push(wp);}}"
b="const j=v1.joint==='screw'?PO().jointPositions([...p1,...p2],ks,H):null;if(j?.problem)out.push(j.problem);\n    for(const [sp,v] of [[spec1,v1],[spec2,m]]){const wp=T().wallProblem(sp,v,j?.joints||[]);if(wp&&!out.includes(wp))out.push(wp);}"
assert a in t;t=t.replace(a,b);p.write_text(t,encoding='utf-8',newline='\n')
p=app/'js-tests/wall-mount.js';t=p.read_text(encoding='utf-8');t+='''
test('Single-piece pair still checks the wall against the faceplate',()=>{
 const a={...spec,dev_w:60,dev_d:70,dev_off_x:-40,joint:'single',dev_off_y:-12},b={...a,dev_off_x:40,dev_off_y:13};
 assert(Pair.problems(a,T.values(a),b,Pair.values(b)).includes(T.WALL_MESSAGE));
});
''';p.write_text(t,encoding='utf-8',newline='\n')
p=app/'asset-manifest.json';m=json.loads(p.read_text(encoding='utf-8'))
for r in m:
 f=app/r['file']
 if f.exists():r['sha256']=hashlib.sha256(f.read_text(encoding='utf-8').encode()).hexdigest()
p.write_text(json.dumps(m,indent=1)+'\n',encoding='utf-8')
print('Single-piece pair faceplate guard added')
