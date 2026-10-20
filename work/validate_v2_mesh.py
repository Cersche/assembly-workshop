from pathlib import Path
import re,collections,json
out=Path('outputs/Lab_Rax_Pi4_Assembly_Beta_Clearance_v2')
results={}
for name in ['tray','faceplate']:
 vs=[tuple(map(float,m)) for m in re.findall(r'vertex\s+([-\d.e+]+)\s+([-\d.e+]+)\s+([-\d.e+]+)',(out/(name+'.stl')).read_text())]
 edges=collections.Counter(tuple(sorted((vs[i+j],vs[i+(j+1)%3]))) for i in range(0,len(vs),3) for j in range(3))
 assert set(edges.values())=={2}
 results[name]={'triangles':len(vs)//3,'closed_edges':True,'bounds':[[min(v[k] for v in vs) for k in range(3)],[max(v[k] for v in vs) for k in range(3)]]}
print(json.dumps(results,indent=2));Path('work/v2_mesh_checks.json').write_text(json.dumps(results,indent=2))
