from pathlib import Path
import json,zipfile,xml.etree.ElementTree as E
base=Path.cwd();out=base/'outputs/Lab_Rax_Pi4_Assembly_Beta_Clearance_v2'
r=json.loads((base/'work/v2_verification.json').read_text());assert all(r[k]['empty'] and 'ERROR' not in r[k]['log'] for k in ['v2_usb_clearance_05','v2_joint','v2_pcb'])
p=(base/'work/align_pi.py').read_text().replace("p=p.replace('for oid", "p=p.replace('Lab_Rax_Pi4_Assembly_Beta_Gusset_Fix','Lab_Rax_Pi4_Assembly_Beta_Clearance_v2')\np=p.replace('for oid").replace("root/'work/pi_fit_review.3mf'","root/'outputs/Lab_Rax_Pi4_Assembly_Beta_Clearance_v2/Pi4_fit_REFERENCE_ONLY.3mf'")
exec(compile(p,str(base/'work/align_pi.py'),'exec'))
report='''# Pi4 tray clearance revision 2

All four gusset crests are 1 mm lower than the previous gusset-fix revision. No other design dimensions were changed. The faceplate, alignment pockets, screw bores, mounting-hole pattern, PCB height and tray envelope are unchanged.

Validation:
- OpenSCAD exported simple tray and faceplate solids. Every STL edge is shared by two triangles.
- The previously clashing USB connected solid clears the right inner gusset even after shifting that USB solid down 0.5 mm. This checks 0.5 mm vertical clearance at that feature, not a global minimum Euclidean distance.
- Direct triangle clipping of the complete Pi mesh against all four gussets finds no intersection after lowering the Pi 0.5 mm. The ear envelopes and the 48-sided standoff envelopes also have no triangle intersection, excluding intentional PCB contact by 0.001 mm. The floor and socket rails are separated from the Pi by their coordinate bounds.
- The whole-Pi CGAL solid check was inconclusive because the imported Pi has non-manifold edges; its empty output is not counted as a pass. The targeted USB solid check and direct triangle checks above provide the clearance evidence.
- The nominal PCB and the tray/faceplate solid-interference checks also pass, excluding their intentional contact surfaces by 0.001 mm.

Fit geometry retained: PCB hole pattern 58 x 49 mm; two tongue pockets with 0.15 mm nominal side/vertical clearance per side and 0.2 mm tip clearance; joint screw axes at X=+/-40, Z=21 along Y; 0.3 mm gap from plate bosses to tray ears. Tray floor and faceplate are perpendicular in model space.

Files:
- tray.stl: updated tray.
- faceplate.stl: unchanged matching faceplate.
- pi4_assembly.scad: editable source for this revision.
- assembly_review.3mf: tray and faceplate at assembled coordinates, geometry only.
- Pi4_fit_REFERENCE_ONLY.3mf: assembly with aligned detailed Pi mesh for inspection only. Do not print the Pi reference.
- verification.json: render and intersection logs.

Bambu Studio has not been updated during this file-only revision. Ask for desktop-session permission before loading these files there. Geometry-only 3MFs have no printer configuration, so Bambu may report that it is loading geometry only. The detailed Pi model may generate non-manifold warnings; it is a reference, not a printable part.

These checks establish clearance for the supplied tessellated Pi reference. Cables, heatsinks, actual fasteners/inserts, rack engagement, insertion path, printed tolerances and strength under load remain untested. Nothing was printed.
'''
(out/'README.md').write_text(report)
r=json.loads((base/'work/v2_verification.json').read_text())
r['triangle_gussets']=json.loads((base/'work/v2_gusset_triangle_checks.json').read_text())
r['triangle_ears_standoffs']=json.loads((base/'work/v2_other_triangle_checks.json').read_text())
(out/'verification.json').write_text(json.dumps(r,indent=2))
for f in out.glob('*.3mf'):
 with zipfile.ZipFile(f) as z:
  assert z.testzip() is None;E.fromstring(z.read('3D/3dmodel.model'))
with zipfile.ZipFile(base/'outputs/Lab_Rax_Pi4_Clearance_v2.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in out.iterdir():z.write(f,f.relative_to(out.parent))
print('Packaged revision 2')

