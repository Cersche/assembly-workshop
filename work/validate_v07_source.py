from pathlib import Path
import sys,subprocess
sys.path.insert(0,str(Path('outputs/Mechanical_Design_App').resolve()))
from app import design_revision
import json
ps=json.loads(Path('outputs/Mechanical_Design_App/starter-hardware.json').read_text())
selected={p['kind']:p for p in ps if p.get('part_number') in ['SSCF-M3-8-A2','94459A140']}
s,metadata=design_revision({'inputs':{'pilot':4},'selections':selected})
Path('work/v07_proposed.scad').write_text(s)
r=subprocess.run(['C:/Program Files/OpenSCAD/openscad.exe','-o','work/v07_faceplate.stl','-D','part="faceplate"','work/v07_proposed.scad'],capture_output=True,text=True)
print(r.stderr);assert r.returncode==0 and 'Simple:        yes' in r.stderr
