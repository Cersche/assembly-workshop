"""Explicit task-43 regression renders in new scratch files only; never app data."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT / 'outputs/Mechanical_Design_App'))
sys.path.insert(0,str(ROOT / 'tools'))
import equipment as eq
from mesh_viewer import read_stl

def triangles(path):
    vs, ts = read_stl(path)
    return sorted(tuple(sorted(vs[i] for i in t)) for t in ts)

def main():
    folder = HERE / 'hdt-regression'
    folder.mkdir(exist_ok=True)
    cases = json.loads((HERE/'legacy-before.json').read_text(encoding='utf-8'))
    spec = next(r['spec'] for r in cases if r['label']=='HDT-M6-A')
    sources = {'generated':eq.source(eq.clean(spec))}
    original = ROOT/'outputs/Hard_Drive_Tray_M6_2026-10-28/HDT-M6-A.scad'
    sources['reference-without-id'] = ''.join(line for line in original.read_text(encoding='utf-8').splitlines(True)
                                            if 'text("HDT-M6-A"' not in line)
    exe = Path('C:/Program Files/OpenSCAD/openscad.exe')
    results = {'executable':str(exe),'reference_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),'renders':{}}
    for label,src in sources.items():
        scad = folder/(label+'.scad')
        scad.write_text(src,encoding='utf-8',newline='\n')
        for part in ['faceplate','tray']:
            target = folder/(label+'-'+part+'.stl')
            command = [str(exe),'--export-format','asciistl','-o',str(target),'-D',f'part="{part}"',str(scad)]
            p = subprocess.run(command,capture_output=True,text=True,timeout=300,
                               creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
            (folder/(label+'-'+part+'.log')).write_text(p.stdout+p.stderr,encoding='utf-8')
            results['renders'][label+'-'+part] = dict(returncode=p.returncode,exists=target.exists())
            print(label,part,p.returncode,flush=True)
    for part in ['faceplate','tray']:
        a,b = [folder/(label+'-'+part+'.stl') for label in sources]
        results[part] = {'triangle_for_triangle':triangles(a)==triangles(b),'generated_triangles':len(triangles(a))}
    (HERE/'hdt-regression.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(results,indent=2),flush=True)

if __name__=='__main__':
    main()
