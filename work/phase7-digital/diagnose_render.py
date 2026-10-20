from pathlib import Path
import sys,json,subprocess,concurrent.futures,re,math
root=Path.cwd();sys.path.insert(0,'outputs/Mechanical_Design_App')
from app import design_revision
records=json.loads(Path('outputs/Mechanical_Design_App/starter-hardware.json').read_text(encoding='utf-8'))
selection={p['kind']:p for p in records if p.get('part_number') in ['SSCF-M3-8-A2','94459A140']}
source,meta=design_revision({'selections':selection,'inputs':{'pilot':4}})
folder=Path('work/phase7-digital/render-diagnostics');folder.mkdir(parents=True,exist_ok=True)
(folder/'source.scad').write_text(source,encoding='utf-8',newline='\n')
exe='C:/Program Files/OpenSCAD/openscad.exe'
def run(fmt):
    target=(folder/('tray-'+fmt+'.stl')).resolve()
    r=subprocess.run([exe,'--export-format',fmt,'-o',str(target),'-D','part="tray"',str((folder/'source.scad').resolve())],capture_output=True,text=True,timeout=180,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    (folder/(fmt+'.log')).write_text(r.stdout+r.stderr,encoding='utf-8')
    return dict(format=fmt,exit_code=r.returncode,bytes=target.stat().st_size if target.exists() else 0)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: results=list(pool.map(run,['asciistl','binstl']))
raw=(folder/'tray-asciistl.stl').read_bytes()
vertices=[tuple(map(float,l.split())) for l in re.findall(rb'^\s*vertex\s+([^\r\n]+)',raw,re.M)]
deg=[]
for i in range(0,len(vertices),3):
 a,b,c=vertices[i:i+3];u=[b[k]-a[k] for k in range(3)];v=[c[k]-a[k] for k in range(3)];cross=(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
 if sum(x*x for x in cross)==0:deg.append(dict(triangle=i//3,vertices=[a,b,c]))
result=dict(renders=results,ascii_degenerate_triangles=len(deg),examples=deg[:5])
(folder/'diagnostics.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2))
