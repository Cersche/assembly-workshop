"""CM1P-N against CM1P-M: cut both bodies square to Y, fill each cut on a 0.1 mm grid by crossing counts, and report where they differ. Run from this folder."""
import numpy as np, trimesh
M = trimesh.load('../../CM1000_OnePiece_CM1P-M_2026-11-02/CM1P-M_body_only.stl')
N = trimesh.load('../CM1P-N_body_only.stl')
X = np.arange(0.033, 254, 0.1); Z = np.arange(0.037, 44.45, 0.1)
def fill(m, y):
    s = trimesh.intersections.mesh_plane(m, plane_normal=[0, 1, 0], plane_origin=[0, y, 0])
    x0, z0, x1, z1 = s[:, 0, 0], s[:, 0, 2], s[:, 1, 0], s[:, 1, 2]
    g = np.zeros((len(Z), len(X)), bool)
    for i, z in enumerate(Z):
        c = (z0 <= z) != (z1 <= z)
        xs = np.sort(x0[c] + (z - z0[c]) / (z1[c] - z0[c]) * (x1[c] - x0[c]))
        g[i] = np.searchsorted(xs, X) % 2 == 1
    return g
ys = np.arange(0.13, 137.6, 0.5)
n = 0
for y in ys:
    a, b = fill(M, y), fill(N, y)
    d = a ^ b
    if d.sum() > 0:
        n += 1
        r, c = np.nonzero(d)
        print('Y', round(float(y), 2), 'cells', int(d.sum()), 'area', round(d.sum() * .01, 2), 'X', round(X[c.min()], 1), round(X[c.max()], 1), 'Z', round(Z[r.min()], 1), round(Z[r.max()], 1), 'M only', int((a & ~b).sum()), 'N only', int((b & ~a).sum()))
print('slices', len(ys), 'with any difference', n)
for y in (137.5, 140.13, 143.5, 143.8, 147.5):
    print('N at Y', y, 'area', round(fill(N, y).sum() * .01, 1))
