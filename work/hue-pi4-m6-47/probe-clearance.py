from pathlib import Path
import subprocess,re,json,concurrent.futures
R=Path('D:/Projects/assembly-workshop');O=R/'outputs/Hue_Pi4_M6-B_2026-10-28';W=R/'work/hue-pi4-m6-47';C=O/'checks';C.mkdir()
s=(O/'src/HP4-M6-B.scad').read_text(encoding='utf-8').replace('clip_coupon(){\n if(part=="faceplate")','if(false)clip_coupon(){\n if(part=="faceplate")')
probes={'cradle':'cradle();','keystone':'ks_golden();','plate-id':'hp4_plate_id();','tray-id':'hp4_tray_id();'}
def run(item):
 name,call=item;p=C/(name+'.scad');p.write_text(s+'\n'+call+'\n',encoding='utf-8')
 a=subprocess.run(['C:/Program Files/OpenSCAD/openscad.exe','--export-format','asciistl','-o',str(C/(name+'.stl')),str(p)],capture_output=True,text=True,encoding='utf-8');(C/(name+'.log')).write_text(a.stdout+a.stderr,encoding='utf-8');assert a.returncode==0,a.stderr
 return name
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex: print(list(ex.map(run,probes.items())))
def components(path):
 v=[tuple(map(float,m)) for m in re.findall(r'\bvertex\s+([\d.eE+-]+)\s+([\d.eE+-]+)\s+([\d.eE+-]+)',path.read_text(encoding='utf-8'))];ts=[v[i:i+3] for i in range(0,len(v),3)];parent=list(range(len(ts)));seen={}
 def find(i):
  while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
  return i
 for i,t in enumerate(ts):
  for q in t:
   if q in seen:parent[find(i)]=find(seen[q])
   else:seen[q]=i
 groups={}
 for i,t in enumerate(ts):groups.setdefault(find(i),[]).extend(t)
 def bb(v):return [[min(q[k] for q in v) for k in range(3)],[max(q[k] for q in v) for k in range(3)]]
 return {'triangles':len(ts),'bounds':bb(v),'components':[bb(g) for g in groups.values()],'behind_plate_x':[min(q[0] for q in v if q[1]>0),max(q[0] for q in v if q[1]>0)] if any(q[1]>0 for q in v) else None}
a={name:components(C/(name+'.stl')) for name in probes};(W/'probe-bounds.json').write_text(json.dumps(a,indent=2),encoding='utf-8');print(json.dumps(a,indent=2))
