"""Explicit Revision 2 candidate renders; no application data or automatic builds."""
import json
import sys
import subprocess
from pathlib import Path
from measure import ROOT,HERE,mesh_info,volume

sys.path.insert(0,str(ROOT/'outputs/Mechanical_Design_App'))
import equipment as eq
REV=HERE/'revision2'
EXE='C:/Program Files/OpenSCAD/openscad.exe'

def render(source,name,part,index=None):
    target=REV/(name+'.stl')
    cmd=[EXE,'--export-format','asciistl','-o',str(target),'-D',f'part="{part}"']
    if index is not None:cmd+=['-D',f'colour_index={index}']
    p=subprocess.run(cmd+[str(source)],capture_output=True,text=True,timeout=600,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    (REV/(name+'.log')).write_text(p.stdout+p.stderr,encoding='utf-8')
    if p.returncode:raise ValueError((name,p.stderr))
    v,t,info=mesh_info(target);info['volume']=volume(v,t)
    print(name,info,flush=True)
    return info

def main():
    spec=json.loads((REV/'spec.json').read_text(encoding='utf-8'))
    cleaned=eq.clean(spec)
    assert eq.clean(cleaned)==cleaned
    source=REV/'candidate.scad'
    source.write_text(eq.source(cleaned),encoding='utf-8',newline='\n')
    result={}
    todo=[(p,p,None) for p in ['faceplate','rail_l','rail_r']]+[(f'pipe_{i+1}','pipe',i) for i in range(5)]+[(f'vector_{i+1}','vector',i) for i in range(9)]
    if sys.argv[1:]:todo=[p for p in todo if p[0] in sys.argv[1:]]
    for name,part,index in todo:result[name]=render(source,name,part,index)
    (REV/'render-results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')

if __name__=='__main__':main()
