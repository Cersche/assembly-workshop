"""Cut a mesh with a plane and draw the section."""
import numpy as np, trimesh
from matplotlib.path import Path as MP
from matplotlib.patches import PathPatch
def loops(m, axis, val, ix):
    t = m.vertices[m.faces]; d = t[:, :, axis] - val + 1e-7
    segs = []
    keep = (d.min(1) < 0) & (d.max(1) > 0)
    for tri, dd in zip(t[keep], d[keep]):
        pts = [tri[i] + (tri[(i + 1) % 3] - tri[i]) * dd[i] / (dd[i] - dd[(i + 1) % 3]) for i in range(3) if dd[i] * dd[(i + 1) % 3] < 0]
        segs.append((tuple(np.round(pts[0][list(ix)], 3)), tuple(np.round(pts[1][list(ix)], 3))))
    nb = {}
    for a, b in segs:
        nb.setdefault(a, []).append(b); nb.setdefault(b, []).append(a)
    seen = set(); out = []
    for st in nb:
        if st in seen: continue
        lp = [st]; seen.add(st); cur = st
        while True:
            nx = [q for q in nb[cur] if q not in seen]
            if not nx: break
            cur = nx[0]; seen.add(cur); lp.append(cur)
        if len(lp) > 2: out.append(np.array(lp + [lp[0]]))
    return out
def sec(ax, f, axis, val, col, z=2):
    m = trimesh.load(f); verts, codes = [], []
    for q in loops(m, axis, val, (1, 2)):
        verts += q.tolist(); codes += [MP.MOVETO] + [MP.LINETO] * (len(q) - 2) + [MP.CLOSEPOLY]
    if verts: ax.add_patch(PathPatch(MP(verts, codes), fc=col, ec='k', lw=.4, zorder=z))
