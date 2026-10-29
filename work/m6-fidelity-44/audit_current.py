"""Explicit OpenSCAD.exe renders of the unchanged task-43 source in fresh data.

This is an audit of rejected CM6B, not acceptance or a replacement delivery.
"""
import hashlib
import json
from pathlib import Path
import random
import subprocess
import sys
from measure import HERE, ROOT, mesh_info, crossing_intervals, volume
from rail_trial import dist

sys.path.insert(0,str(ROOT/'outputs/Mechanical_Design_App'))
import equipment as eq

EXE = 'C:/Program Files/OpenSCAD/openscad.exe'
OUT = ROOT/'outputs/CM1000_M6_generated_2026-10-28'


def run(source, target, extra=()):
    p = subprocess.run([EXE,'--export-format','asciistl','-o',str(target),*extra,str(source)],capture_output=True,text=True,timeout=300,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    target.with_suffix('.log').write_text(p.stdout+p.stderr,encoding='utf-8')
    return p


def main():
    folder = HERE/'current-render'
    folder.mkdir(exist_ok=True)
    spec = json.loads((OUT/'CM6B_spec.json').read_text(encoding='utf-8'))
    code = eq.source(eq.clean(spec))
    source = folder/'current.scad'
    source.write_text(code,encoding='utf-8',newline='\n')
    result = dict(executable=EXE,source_identical_to_task43_delivery=source.read_bytes()==(OUT/'CM6B_source.scad').read_bytes(), parts={})
    meshes = {}
    for name in ['faceplate','rail_l','rail_r']:
        target = folder/(name+'.stl')
        p = run(source,target,['-D',f'part="{name}"'])
        if p.returncode:
            raise ValueError(p.stderr)
        vs,ts,info = mesh_info(target)
        info['volume'] = volume(vs,ts)
        meshes[name] = (vs,ts)
        result['parts'][name] = info
        print(name,info,flush=True)
    intersection = folder/'intersection.scad'
    intersection.write_text('intersection(){import("'+(folder/'faceplate.stl').as_posix()+'");union(){import("'+(folder/'rail_l.stl').as_posix()+'");import("'+(folder/'rail_r.stl').as_posix()+'");}}',encoding='utf-8')
    p = run(intersection,folder/'intersection.stl')
    result['intersection_empty'] = 'top level object is empty' in p.stderr.lower()
    result['intersection_exit_code'] = p.returncode
    # A fixed-seed audit, not the task's complete station / every-shape-change acceptance.
    rng = random.Random(44)
    random_ys = sorted(rng.uniform(1.6,137.6) for _ in range(20))
    stations = sorted(set([2,3.9,4.1,5,10,12,15.9]+list(range(20,138,5))+random_ys))
    a_meshes = {n:mesh_info(ROOT/f'outputs/CM1000_M6_2026-10-28/CM6A_{n}.stl')[:2] for n in meshes}
    rows = []
    poly = [[x+127,z] for x,z in spec['m6_pocket_profile']]
    segments = list(zip(poly,poly[1:]+poly[:1]))
    for y in stations:
        n = 'faceplate' if y < 16 else 'rail_l'
        av,at = a_meshes[n]
        bv,bt = meshes[n]
        for x in [21.5,22.6,24,26,30,34]:
            a = crossing_intervals(av,at,2,[x,y,0])
            b = crossing_intervals(bv,bt,2,[x-127,y-4,0])
            lower = [end for start,end in a if end<22.225]
            upper = [start for start,end in a if start>22.225]
            if lower and upper and not any(start<22.225<end for start,end in a):
                lo,hi = max(lower),min(upper)
                rows.append(dict(y_A=y,x_A=x,reference_pocket_z=[lo,hi],current_material_intervals=b,
                                 distances_to_task43_profile=[min(dist([x,z],u,v) for u,v in segments) for z in [lo,hi]]))
    result['pocket_audit'] = dict(seed=44, random_y_stations=random_ys, stations=stations, samples=rows,
                                complete_shape_change_acceptance=False)
    probes = {}
    for side in ['l','r']:
        x = 18 if side=='l' else 236
        av,at = a_meshes['rail_'+side]
        bv,bt = meshes['rail_'+side]
        probes[side] = dict(reference_bay_z=crossing_intervals(av,at,2,[x,30,0]),
                            current_bay_z=crossing_intervals(bv,bt,2,[x-127,26,0]),
                            reference_bay_y=crossing_intervals(av,at,1,[x,0,8.6]),
                            current_bay_y=crossing_intervals(bv,bt,1,[x-127,0,8.6]),
                            reference_end_channel=crossing_intervals(av,at,2,[22.6 if side=='l' else 231.4,125,0]))
    result['probes'] = probes
    (HERE/'current-audit.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print('source identical',result['source_identical_to_task43_delivery'],'intersection empty',result['intersection_empty'],flush=True)


if __name__ == '__main__':
    main()
