import sys,json,hashlib,subprocess
from pathlib import Path
root=Path.cwd(); app=root/'outputs/Mechanical_Design_App'; sys.path.insert(0,str(app))
import equipment as e, mesh_revision as m
from test_tray_pair import A,B
from test_tray_placement import SPEC
out=root/'work/task39-checks-20261022'; records={}
fixtures={'Router':A,'Switch':B,'Window':SPEC,'Sleeve':dict(name='OptiPlex regression',dev_w=182,dev_d=178,dev_h=36,device_mount='sleeve',joint='screw',rear_support=True,holes=[],feet=[dict(x=x,y=y,w=10,d=10,h=2.75) for x in (15,163) for y in (18,153)])}
for name,s in fixtures.items():
 s=e.clean(s); folder=out/('before-'+name);folder.mkdir();src=e.source(s);(folder/'source.scad').write_text(src,encoding='utf-8',newline='\n');records[name]={'spec':s,'source':hashlib.sha256(src.encode()).hexdigest(),'stl':{}}
 for part in ('tray','faceplate'):
  f=folder/(part+'.stl');r=subprocess.run([m.compiler(),'-o',str(f),'-D','part="'+part+'"',str(folder/'source.scad')],capture_output=True,text=True);assert r.returncode==0,r.stderr
  records[name]['stl'][part]=hashlib.sha256(f.read_bytes()).hexdigest()
 (out/'baseline.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
 print(name,records[name]['stl'],flush=True)
