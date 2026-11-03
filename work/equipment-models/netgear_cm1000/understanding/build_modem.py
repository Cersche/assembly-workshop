"""CM1000 as understood 2026-11-02: Brian's measurements for the shell, rear details placed by eye from his photos. Picture only, not for fit."""
import os, numpy as np, trimesh
from trimesh.creation import box, cylinder
here = os.path.dirname(os.path.abspath(__file__))
w, d, H, strip, end, nose = 212.0, 131.0, 44.4, 3.0, 15.0, 25.0   # all Brian's: depth 131 = front slope 25 + top flat 106
m = H / 2
R = 8.5   # corner radius in plan, same on all corners (Brian); read from his top photo, 8.0 and 9.1 on the two front corners
def outline(ix, iy):
    # rounded rectangle, counterclockwise from above: slopes inset the ends by ix and the front by iy; the rear stays straight
    pts = []
    for cx, cy, a0 in ((w - ix - R, iy + R, -90), (w - ix - R, d - R, 0), (ix + R, d - R, 90), (ix + R, iy + R, 180)):
        for k in range(13):
            t = np.radians(a0 + k * 7.5)
            pts.append((cx + R * np.cos(t), cy + R * np.sin(t)))
    return pts
levels = [(0.0, outline(end, nose)), (m - strip / 2, outline(0, 0)), (m + strip / 2, outline(0, 0)), (H, outline(end, nose))]
N = len(levels[0][1])
V = [(x, y, z) for z, o in levels for x, y in o]
tris = []
for l in range(3):
    for i in range(N):
        k = (i + 1) % N
        a, b, c, e = l * N + i, l * N + k, (l + 1) * N + k, (l + 1) * N + i
        tris += [(a, b, c), (a, c, e)]
for z, base, flip in ((0.0, 0, True), (H, 3 * N, False)):
    o = levels[base // N][1]
    V.append((sum(p[0] for p in o) / N, sum(p[1] for p in o) / N, z))
    hub = len(V) - 1
    for i in range(N):
        k = (i + 1) % N
        tris.append((hub, base + k, base + i) if flip else (hub, base + i, base + k))
shell = trimesh.Trimesh(np.array(V, float), np.array(tris), process=True)
parts = {'modem_shell': shell}
def bx(n, x0, x1, y0, y1, z0, z1):
    b = box(extents=(x1 - x0, y1 - y0, z1 - z0)); b.apply_translation(((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)); parts[n] = b
def hole(n, x, y, z, axis, r=2.2):
    c = cylinder(radius=r, height=0.6, sections=24)
    c.apply_transform(trimesh.geometry.align_vectors((0, 0, 1), axis)); c.apply_translation((x, y, z)); parts[n] = c
bx('rear_panel', 20, 192, d, d + 0.2, 8, 36.4)
bx('ethernet', 160, 172, d + 0.2, d + 0.5, 15, 27)
hole('cable', 106, d + 0.5, m, (0, 1, 0), 4.5)
hole('reset', 184, d + 0.3, m, (0, 1, 0), 1.5)
bx('power_switch', 50, 58, d + 0.2, d + 0.5, 18, 26)
bx('power_jack', 34, 44, d + 0.2, d + 0.5, 17, 27)
for n, x in (('rear_hole_a', 12), ('rear_hole_b', 200)):
    hole(n, x, d + 0.1, m, (0, 1, 0))
hole('side_screw_hole', 0, 67.2, 22.25, (1, 0, 0), 1.2)   # 62.4 to 72 back (Brian), middle shown
for n, p in parts.items():
    p.export(os.path.join(here, n + '.stl'))
print(parts['modem_shell'].bounds.tolist(), round(parts['modem_shell'].volume / 1000, 1), parts['modem_shell'].is_watertight)
