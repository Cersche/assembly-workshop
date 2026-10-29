"""Build the required local comparison viewer without touching reference files."""
import json
import subprocess
import sys
from measure import ROOT,HERE,mesh_info
sys.path.insert(0,str(ROOT/'outputs/Mechanical_Design_App'))
import print_layout
REV=HERE/'revision2'
def main():
    folder=REV/'viewer-parts';folder.mkdir(exist_ok=True)
    files=[];placement=[]
    refs=ROOT/'outputs/CM1000_M6_2026-10-28'
    out=ROOT/'outputs/CM1000_M6_generated_2026-10-28'
    reference=[(f'CM6A_{n}',refs/f'CM6A_{n}.stl') for n in ['faceplate','rail_l','rail_r']]
    reference += [(f'CM6A_pipe_{n-3}' if n<9 else f'CM6A_logo_{n-8}' if n>=9 else f'CM6A_detail_{n-1}',refs/f'src/orig/fp_{n}_normal_part.stl') for n in range(4,16)]
    reference += [(f'CM6A_detail_{n-1}',refs/f'src/orig/fp_{n}_normal_part.stl') for n in [2,3]]
    candidates=[(p.stem,p) for p in out.glob('*.stl')]
    for name,path in reference+candidates:
        is_a=name.startswith('CM6A')
        shift=(-272,-4,0) if is_a else (145,0,0)
        vs,ts,_=mesh_info(path)
        moved=[tuple(v[i]+shift[i] for i in range(3)) for v in vs]
        target=folder/(name+'.stl')
        target.write_text(print_layout.stl([(name,[[moved[i] for i in t] for t in ts])]),encoding='utf-8')
        files.append(str(target));placement.append(dict(name=name,original=str(path.relative_to(ROOT)),translation=list(shift)))
    (REV/'viewer-placement.json').write_text(json.dumps(placement,indent=2),encoding='utf-8')
    subprocess.run([sys.executable,str(ROOT/'tools/mesh_viewer.py'),*files,'--as-is','-o',str(ROOT/'work/mesh-viewer/CM6A_vs_CM6B.html'),'-t','CM6A (left) vs CM6B Revision 2 (right) — POCKET FAIL; items 2–7 sampled PASS'],check=True)
    hdt=REV/'hdt-regression'
    subprocess.run([sys.executable,str(ROOT/'tools/mesh_viewer.py'),*[str(hdt/(n+'.stl')) for n in ['generated-faceplate','generated-tray','reference-without-id-faceplate','reference-without-id-tray']],'-o',str(ROOT/'work/mesh-viewer/task44-revision2-hdt.html'),'-t','Task 44 Revision 2 — HDT-M6-A fresh scratch preservation proof'],check=True)

if __name__=='__main__':main()
