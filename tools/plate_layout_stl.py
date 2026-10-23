"""Lay a tray and its faceplate side by side for printing, as two bodies in one ASCII STL.

The tray keeps its orientation; the faceplate is turned front face down. Both sit on Z=0,
the faceplate 10 mm in front of the tray. Geometry is only moved/rotated, never changed.
Usage: python tools/plate_layout_stl.py tray.stl faceplate.stl out.stl
"""
import sys
from pathlib import Path

GAP = 10.0


def facets(path):
    tris, cur = [], []
    for line in Path(path).read_text(encoding='utf-8').splitlines():
        p = line.split()
        if p[:1] == ['vertex']:
            cur.append(tuple(map(float, p[1:4])))
            if len(cur) == 3:
                tris.append(cur); cur = []
    return tris


def move(tris, f):
    return [[f(v) for v in t] for t in tris]


def bounds(tris):
    vs = [v for t in tris for v in t]
    return [min(v[i] for v in vs) for i in range(3)], [max(v[i] for v in vs) for i in range(3)]


def write(path, bodies):
    out = []
    for name, tris in bodies:
        out.append(f'solid {name}')
        for a, b, c in tris:
            u = [b[i] - a[i] for i in range(3)]; w = [c[i] - a[i] for i in range(3)]
            n = [u[1]*w[2]-u[2]*w[1], u[2]*w[0]-u[0]*w[2], u[0]*w[1]-u[1]*w[0]]
            m = sum(x*x for x in n) ** 0.5 or 1
            out.append('facet normal %g %g %g\nouter loop' % tuple(x/m for x in n))
            out += ['vertex %.6f %.6f %.6f' % v for v in (a, b, c)]
            out.append('endloop\nendfacet')
        out.append(f'endsolid {name}')
    Path(path).write_text('\n'.join(out) + '\n', encoding='utf-8')


def main(tray_path, plate_path, out_path):
    tray = facets(tray_path)
    lo, _ = bounds(tray)
    tray = move(tray, lambda v: (v[0], v[1], v[2] - lo[2]))
    # Rotate +90 deg about X: front face (Y=-4) goes down onto the bed.
    plate = move(facets(plate_path), lambda v: (v[0], -v[2], v[1]))
    plo, phi = bounds(plate)
    tlo, _ = bounds(tray)
    plate = move(plate, lambda v: (v[0], v[1] - phi[1] + tlo[1] - GAP, v[2] - plo[2]))
    write(out_path, [('tray', tray), ('faceplate', plate)])
    lo, hi = bounds(tray + plate)
    print('bed footprint %.1f x %.1f mm, height %.1f mm' % (hi[0]-lo[0], hi[1]-lo[1], hi[2]-lo[2]))


if __name__ == '__main__':
    main(*sys.argv[1:4])
