from pathlib import Path
import sys,json,subprocess
r=Path.cwd();w=r/'work/cm6b-46';sys.path[:0]=[str(r/'outputs/Mechanical_Design_App')]
import equipment as eq
s=json.loads((w/'spec.json').read_text(encoding='utf-8'));src=eq.source(eq.clean(s));(w/'candidate.scad').write_text(src,encoding='utf-8',newline='\n')
todo=[(p,p,None) for p in ['faceplate','rail_l','rail_r']]+[(f'pipe_{i+1}','pipe',i) for i in range(5)]+[(f'vector_{i+1}','vector',i) for i in range(9)]
for name,part,index in todo:
 cmd=['C:/Program Files/OpenSCAD/openscad.exe','--export-format','asciistl','-o',str(w/(name+'.stl')),'-D',f'part="{part}"']
 if index is not None:cmd+=['-D',f'colour_index={index}']
 p=subprocess.run(cmd+[str(w/'candidate.scad')],capture_output=True,text=True,encoding='utf-8',timeout=600,creationflags=subprocess.CREATE_NO_WINDOW)
 (w/(name+'.log')).write_text(p.stdout+p.stderr,encoding='utf-8');assert p.returncode==0,(name,p.stderr)
 print(name,'rendered',flush=True)
