from pathlib import Path
import subprocess,json,shutil
base=Path.cwd();old=base/'outputs/Lab_Rax_Pi4_Assembly_Beta_Gusset_Fix';out=base/'outputs/Lab_Rax_Pi4_Assembly_Beta_Clearance_v2';out.mkdir(exist_ok=True)
s=(old/'pi4_assembly.scad').read_text().replace('tray_z+9])cube','tray_z+8])cube').replace('// Lowered crest clears the nominal PCB underside (Z=16), including at Y=13.','// Crest lowered another 1 mm after detailed Pi STEP USB mounting-feature check.')
(out/'pi4_assembly.scad').write_text(s)
exe='C:/Program Files/OpenSCAD/openscad.exe'
results={}
for part in ['tray','faceplate']:
 r=subprocess.run([exe,'-o',str(out/(part+'.stl')),'-D',f'part="{part}"',str(out/'pi4_assembly.scad')],capture_output=True,text=True);results[part]={'code':r.returncode,'log':r.stderr};print(part,r.stderr,flush=True);assert r.returncode==0
body=s.split('if(part=="faceplate")')[0]
expressions={
'v2_usb_clearance_05':'intersection(){translate([0,0,-0.5])import("usb_candidate.stl");translate([33,0,0])hull(){translate([0,9,9.7])cube([2,2,0.5]);translate([0,9,15])cube([2,2,0.5]);translate([0,20,9.7])cube([2,2,0.5]);}}',
'v2_joint':'intersection(){tray();translate([0,-0.001,0])faceplate();}',
'v2_pcb':'intersection(){tray();translate([-44,13,16.001])cube([85,56,1.6]);}',
'v2_full_pi':'intersection(){tray();translate([0,0,0.001])import("pi_aligned.stl");}'
}
for name,expr in expressions.items():
 p=base/'work'/f'{name}.scad';p.write_text(body+expr)
 r=subprocess.run([exe,'-o',str(base/'work'/f'{name}.stl'),str(p)],capture_output=True,text=True);results[name]={'code':r.returncode,'empty':'Current top level object is empty' in r.stderr,'log':r.stderr};print(name,r.stderr,flush=True)
(base/'work/v2_verification.json').write_text(json.dumps(results,indent=2))
assert all(results[k]['empty'] for k in expressions)
p=(base/'work/package_revision.py').read_text().replace('Lab_Rax_Pi4_Assembly_Beta_Gusset_Fix','Lab_Rax_Pi4_Assembly_Beta_Clearance_v2');exec(compile(p,str(base/'work/package_revision.py'),'exec'))
