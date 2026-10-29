"""Disposable primitive reconstruction experiment; not a deliverable generator."""
import json
from pathlib import Path
import subprocess
from measure import HERE, ROOT, section, mesh_info, volume


def dist(p, a, b):
    dx, dy = b[0]-a[0], b[1]-a[1]
    t = max(0, min(1, ((p[0]-a[0])*dx+(p[1]-a[1])*dy)/(dx*dx+dy*dy))) if dx or dy else 0
    return ((p[0]-a[0]-t*dx)**2+(p[1]-a[1]-t*dy)**2)**.5


def simplify(points, tolerance=.015):
    # Iterative local removal avoids recursion depth on dense faceted contours.
    points = points[:]
    changed = True
    while changed:
        changed = False
        out = []
        for i, p in enumerate(points):
            if len(points)-len(out)>3 and i%2 == 0 and dist(p, points[i-1], points[(i+1)%len(points)]) < tolerance:
                changed = True
            else:
                out.append(p)
        points = out
    return points


def polygon(data):
    points, paths = [], []
    for l in data['loops']:
        if not l['closed']:
            raise ValueError('Cannot use an open measured contour')
        p = simplify(l['points'])
        paths.append(list(range(len(points),len(points)+len(p))))
        points.extend(p)
    return 'polygon(points='+json.dumps(points)+',paths='+json.dumps(paths)+');'


def main():
    results = {}
    for side, x in [('l',18), ('r',236)]:
        vs, ts, info = mesh_info(ROOT/f'outputs/CM1000_M6_2026-10-28/CM6A_rail_{side}.stl')
        base = section(vs, ts, 1, 125.123)
        mask = section(vs, ts, 0, x)
        code = 'intersection(){translate([0,137.62,0])rotate([90,0,0])linear_extrude(121.62)'+polygon(base)+'\ntranslate([0,0,0])rotate([90,0,90])linear_extrude(254)'+polygon(mask)+'}\n'
        # Original bores are primitives, along Y; the side sample is outside these bores.
        code = 'difference(){'+code+'for(z=[8.6,35.85])translate(['+str(22.6 if side=='l' else 231.4)+',15,z])rotate([-90,0,0])cylinder(d=6.6,h=5.5,$fn=48);}\n'
        source = HERE/f'trial-{side}.scad'
        source.write_text(code, encoding='utf-8')
        target = HERE/f'trial-{side}.stl'
        p = subprocess.run(['C:/Program Files/OpenSCAD/openscad.exe','--export-format','asciistl','-o',str(target),str(source)],capture_output=True,text=True,timeout=300,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        (HERE/f'trial-{side}.log').write_text(p.stdout+p.stderr,encoding='utf-8')
        if p.returncode:
            raise ValueError(p.stderr)
        v, t, trial = mesh_info(target)
        trial['volume'] = volume(v,t)
        trial['reference_volume'] = volume(vs,ts)
        trial['volume_error_percent'] = 100*(trial['volume']/trial['reference_volume']-1)
        results[side] = trial
        print(side, trial)
    (HERE/'rail-trial.json').write_text(json.dumps(results,indent=2),encoding='utf-8')


if __name__ == '__main__':
    main()
