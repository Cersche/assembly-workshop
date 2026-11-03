"""Clash check by ray parity on a 0.25 mm XZ grid: each mesh becomes Y intervals per column, overlap is measured directly.
OpenSCAD intersection() returned empty for the keystone plate mesh (a test cube inside the plate came back empty), so it is not trusted here.
Usage: check_ray.py A B"""
import json, sys
from pathlib import Path
import numpy as np, trimesh
H = Path(__file__).parent; S = H / 'stl'; G = 0.25
src = (H / 'build.py').read_text(encoding='utf-8')
exec(src[src.index('PAIRS ='):src.index('SRC =')])
def load(o, n):
    if n in ('post_l', 'post_r'):
        m = trimesh.load(H.parent / f'rack-post-hex/assembled/{"post_left" if n == "post_l" else "post_right"}.stl'); m.apply_translation([0, 4, 0]); return m
    return trimesh.load(S / f'{o}_{n}.stl')
def columns(m):
    """dict (ix,iz) -> sorted Y crossings."""
    out = {}
    for t in m.triangles:
        x, y, z = t.T
        i0, i1 = int(np.ceil(x.min() / G)), int(np.floor(x.max() / G))
        k0, k1 = int(np.ceil(z.min() / G)), int(np.floor(z.max() / G))
        d = (x[1] - x[0]) * (z[2] - z[0]) - (x[2] - x[0]) * (z[1] - z[0])
        if abs(d) < 1e-12: continue
        for i in range(i0, i1 + 1):
            for k in range(k0, k1 + 1):
                # small offset keeps grid points off shared triangle edges
                px, pz = i * G + 1.37e-4, k * G + 2.11e-4
                u = ((px - x[0]) * (z[2] - z[0]) - (x[2] - x[0]) * (pz - z[0])) / d
                v = ((x[1] - x[0]) * (pz - z[0]) - (px - x[0]) * (z[1] - z[0])) / d
                if u >= 0 and v >= 0 and u + v <= 1:
                    out.setdefault((i, k), []).append(y[0] + u * (y[1] - y[0]) + v * (y[2] - y[0]))
    return {c: sorted(q) for c, q in out.items() if len(q) % 2 == 0}
def overlap(a, b):
    v = 0.0; lo = None; hi = None
    for c in a.keys() & b.keys():
        A, B = a[c], b[c]
        for i in range(0, len(A), 2):
            for j in range(0, len(B), 2):
                s, e = max(A[i], B[j]), min(A[i + 1], B[j + 1])
                if e - s > 1e-3:
                    v += (e - s) * G * G; p = np.array([c[0] * G, s, c[1] * G]); q = np.array([c[0] * G, e, c[1] * G])
                    lo = p if lo is None else np.minimum(lo, p); hi = q if hi is None else np.maximum(hi, q)
    return v, lo, hi
for o in sys.argv[1:]:
    cache = {}
    def col(n):
        if n not in cache: cache[n] = columns(load(o, n))
        return cache[n]
    rows = []
    # sanity: plate boss must register as solid
    print(o, 'plate columns', len(col('plate')))
    for a, b in PAIRS:
        ma, mb = load(o, a), load(o, b)
        if (np.minimum(ma.bounds[1], mb.bounds[1]) <= np.maximum(ma.bounds[0], mb.bounds[0])).any():
            rows.append(dict(a=a, b=b, mm3=0.0)); continue
        v, lo, hi = overlap(col(a), col(b))
        r = dict(a=a, b=b, mm3=round(v, 1))
        if v > 0:
            r['from'] = lo.round(1).tolist(); r['to'] = hi.round(1).tolist()
            print(' ', a, b, r['mm3'], r['from'], r['to'])
        rows.append(r)
    json.dump(rows, open(H / f'checks_{o}.json', 'w', encoding='utf-8'), indent=0)
