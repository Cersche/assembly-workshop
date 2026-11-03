"""Outlines of the old pipes' icons, read at Y 0.2 from the baseline meshes, scaled for CM1P-I. Writes icon_loops.json for cm1p_i_freecad.py."""
import json
import numpy as np, trimesh
orig = '../../CM1000_M6_2026-10-28/src/orig/'
S, ZT = 0.62, 40.5
def section_y(m, val):
    segs = []
    d = m.triangles[:, :, 1] - val
    for t, dd in zip(m.triangles, d):
        if (dd > 0).all() or (dd < 0).all(): continue
        P = []
        for i in range(3):
            j = (i + 1) % 3
            if dd[i] * dd[j] < 0:
                s = dd[i] / (dd[i] - dd[j]); P.append((t[i] + s * (t[j] - t[i]))[[0, 2]])
        if len(P) == 2: segs.append(P)
    key = lambda p: (round(float(p[0]), 3), round(float(p[1]), 3))
    nb = {}
    for a, b in segs:
        ka, kb = key(a), key(b)
        if ka != kb:
            nb.setdefault(ka, []).append(kb); nb.setdefault(kb, []).append(ka)
    seen, loops = set(), []
    for s in nb:
        if s in seen: continue
        L, c = [s], s; seen.add(s)
        while True:
            n = [x for x in nb[c] if x not in seen]
            if not n: break
            c = n[0]; seen.add(c); L.append(c)
        loops.append(L)
    return loops
def thin(L, tol):
    out = [L[0]]
    for p in L[1:]:
        if np.hypot(p[0] - out[-1][0], p[1] - out[-1][1]) >= tol: out.append(p)
    if np.hypot(out[0][0] - out[-1][0], out[0][1] - out[-1][1]) < tol: out.pop()
    return out
def inside(p, L):
    c = False
    for i in range(len(L)):
        a, b = L[i], L[i - 1]
        if (a[1] > p[1]) != (b[1] > p[1]) and p[0] < a[0] + (p[1] - a[1]) * (b[0] - a[0]) / (b[1] - a[1]): c = not c
    return c
res = {}
for n, xc in ((4, 104.0), (8, 115.5), (7, 127.0), (6, 138.5), (5, 150.0)):
    m = trimesh.load(orig + 'fp_%d_normal_part.stl' % n)
    loops = [[(xc + S * (x - xc), ZT + S * (z - 30.225)) for x, z in thin(L, 0.06)] for L in section_y(m, 0.2)]
    loops = [L for L in loops if len(L) >= 3]
    faces = []
    for i, L in enumerate(loops):
        depth = sum(inside(L[0], o) for j, o in enumerate(loops) if j != i)
        if depth % 2 == 0:
            faces.append({'outer': L, 'holes': [h for j, h in enumerate(loops) if j != i and inside(h[0], L)
                                                and sum(inside(h[0], o) for k, o in enumerate(loops) if k != j) == depth + 1]})
    res[str(n)] = faces
    print(n, 'loops', len(loops), 'faces', len(faces), 'points', sum(len(L) for L in loops))
json.dump(res, open('icon_loops.json', 'w', encoding='utf-8'))
