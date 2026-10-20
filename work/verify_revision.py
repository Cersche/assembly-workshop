from pathlib import Path
import subprocess, re, json

root = Path(__file__).resolve().parents[1]
out = root / 'outputs/Lab_Rax_Pi4_Assembly_Beta_Gusset_Fix'
work = root / 'work'
exe = 'C:/Program Files/OpenSCAD/openscad.exe'
src = (out / 'pi4_assembly.scad').read_text()
body = src.split('if(part=="faceplate")')[0]
results = {}
for name, expression in {
    # Exclude intentional zero-thickness contact: PCB rests on bosses at Z=16;
    # tray front meets faceplate at Y=0. Detect penetration exceeding 0.001 mm.
    'pcb_collision': 'intersection(){tray(); translate([tray_x+12,tray_y+13,16.001])cube([85,56,1.6]);}',
    'joint_collision': 'intersection(){tray();translate([0,-0.001,0])faceplate();}',
}.items():
    scad = work / (name + '.scad')
    scad.write_text(body + expression)
    r = subprocess.run([exe, '-o', str(work / (name+'.stl')), str(scad)], capture_output=True, text=True)
    results[name] = {'returncode':r.returncode, 'log':r.stderr, 'empty': 'Current top level object is empty' in r.stderr}
r = subprocess.run([exe, '-o', str(out/'faceplate.stl'), '-D', 'part="faceplate"', str(out/'pi4_assembly.scad')],capture_output=True,text=True)
results['faceplate_export'] = {'returncode':r.returncode, 'log':r.stderr}
text = (out/'tray.stl').read_text()
vertices = [tuple(map(float,m)) for m in re.findall(r'vertex\s+([-\d.e+]+)\s+([-\d.e+]+)\s+([-\d.e+]+)',text)]
results['tray'] = {'triangles':len(vertices)//3,'bounds':[[min(v[k] for v in vertices) for k in range(3)],[max(v[k] for v in vertices) for k in range(3)]], 'gusset_vertices':{str(x):sum(abs(v[0]-x)<=1.001 and v[1]>11.31 and v[2]>10.01 for v in vertices) for x in [-46,-34,34,46]}}
(work/'verification.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
assert all(results[k]['empty'] for k in ['pcb_collision','joint_collision']), 'Unexpected solid interference'
assert all(results['tray']['gusset_vertices'].values()), 'Missing gusset'
assert r.returncode==0
