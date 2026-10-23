import sys,json,hashlib,subprocess
from pathlib import Path
root=Path.cwd();sys.path.insert(0,str(root/'outputs/Mechanical_Design_App'))
import equipment as e,mesh_revision as m
out=root/'work/task39-checks-20261022';baseline=json.loads((out/'baseline.json').read_text(encoding='utf-8'));result={}
for name,b in baseline.items():
 src=e.source(e.clean(dict(b['spec'],drives=[])));assert hashlib.sha256(src.encode()).hexdigest()==b['source'],name+' source changed'
 folder=out/('after-'+name);folder.mkdir(exist_ok=True);(folder/'source.scad').write_text(src,encoding='utf-8',newline='\n');result[name]={}
 for part in ('tray','faceplate'):
  f=folder/(part+'.stl');r=subprocess.run([m.compiler(),'-o',str(f),'-D','part="'+part+'"',str(folder/'source.scad')],capture_output=True,text=True);assert r.returncode==0,r.stderr
  result[name][part]=hashlib.sha256(f.read_bytes()).hexdigest();same=sorted(f.read_bytes().splitlines())==sorted((out/('before-'+name)/(part+'.stl')).read_bytes().splitlines());assert same,name+' '+part+' STL changed'
 print(name,'source and meshes identical',flush=True)
(out/'regression.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
spec=dict(name='Drives',drives=[['3.5',-89.725,0],['2.5',19.875,0]])
results={}
for mode in ('screws','sleeve'):
 s=e.clean(dict(spec,drive_mount=mode));src=e.source(s);folder=out/mode;folder.mkdir(exist_ok=True);(folder/'source.scad').write_text(src,encoding='utf-8',newline='\n');results[mode]={}
 for part in ('assembly','tray','faceplate','combined'):
  f=folder/(part+'.stl');r=subprocess.run([m.compiler(),'-o',str(f),'-D','part="'+part+'"',str(folder/'source.scad')],capture_output=True,text=True);(folder/(part+'.log')).write_text(r.stderr,encoding='utf-8');assert r.returncode==0,r.stderr
  try:m.normalize_collinear_faces(f);check=m.read_mesh(f,part);results[mode][part]={'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'check':{k:v for k,v in check.items() if k!='vertices'}}
  except Exception as exc:results[mode][part]={'error':str(exc)}
  print(mode,part,results[mode][part].get('error','closed'),flush=True)
 (out/'renders.json').write_text(json.dumps(results,indent=2,default=str),encoding='utf-8')
