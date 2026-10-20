from pathlib import Path
import re,json,hashlib
root=Path('outputs/Mechanical_Design_App');src=Path('outputs/Lab_Rax_Pi4_Assembly_Beta_Clearance_v2')
parts=[]
for name in ['tray','faceplate']:
 b=(src/(name+'.stl')).read_bytes();vs=[list(map(float,v)) for v in re.findall(r'vertex\s+([-\d.e+]+)\s+([-\d.e+]+)\s+([-\d.e+]+)',b.decode())]
 unique={};idx=[]
 for v in vs:
  k=tuple(v)
  if k not in unique:unique[k]=len(unique)
  idx.append(unique[k])
 parts.append(dict(id=name,vertices=list(unique),triangles=[idx[i:i+3] for i in range(0,len(idx),3)],source_sha256=hashlib.sha256(b).hexdigest(),bounds=[[min(v[k] for v in vs) for k in range(3)],[max(v[k] for v in vs) for k in range(3)]]))
(root/'assembly.json').write_text(json.dumps(dict(units='mm',revision='Pi4 clearance v2',parts=parts),separators=(',',':')))
print([(p['id'],len(p['triangles'])) for p in parts])
