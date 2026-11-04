"""Mesh checks and picture sheets for the 3 diffuser concepts. Run from this folder after options_freecad.py."""
import os, sys, glob
from collections import Counter
import numpy as np, trimesh, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from trimesh import intersections
from shapely.geometry import LineString
from shapely.ops import polygonize, unary_union

OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
P = {os.path.basename(f)[:-4]: trimesh.load(f) for f in sorted(glob.glob('parts/*.stl'))}
for m in P.values():
    m.merge_vertices(digits_vertex=5)
BODY, CLEAR, MASK = (0.36, 0.38, 0.42), (0.62, 0.86, 0.96), (0.2, 0.2, 0.22)
def col(n): return BODY if 'body' in n else MASK if 'mask' in n else CLEAR

# --- checks: closed meshes, and nothing inside the modem envelope (front slope, front at Y 4.1)
MID, YF = 44.45 / 2, 4.1
def modem_half(y): return np.minimum(22.2, 1.5 + 20.7 / 25 * (y - YF))
for n, m in P.items():
    e = Counter(tuple(sorted(x)) for x in m.edges.tolist())
    bad = sum(1 for v in e.values() if v != 2)
    s, _ = trimesh.sample.sample_surface(m, 40000)
    hit = ((s[:, 1] > YF + .01) & (np.abs(s[:, 2] - MID) < modem_half(s[:, 1]))).sum()
    print(f'{n:16s} tris {len(m.faces):6d} bad edges {bad:3d} cm3 {abs(m.volume)/1000:6.2f} Y {m.bounds[0][1]:.2f}..{m.bounds[1][1]:.2f} in modem {hit}')


# --- simple shaded z-buffer renderer, orthographic
def render(parts, az, el, px_mm=9, pad=2):
    a, e = np.radians(az), np.radians(el)
    Rz = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
    Rx = np.array([[1, 0, 0], [0, np.cos(e), -np.sin(e)], [0, np.sin(e), np.cos(e)]])
    R = Rx @ Rz
    vs = [(m.vertices @ R.T) for m, _ in parts]   # screen x, depth, screen z (camera on -Y side)
    allv = np.vstack(vs)
    lo, hi = allv.min(0) - pad, allv.max(0) + pad
    W, H = int((hi[0] - lo[0]) * px_mm), int((hi[2] - lo[2]) * px_mm)
    img = np.ones((H, W, 3)); zb = np.full((H, W), np.inf)
    L = np.array([-0.35, -0.8, 0.5]); L /= np.linalg.norm(L)
    for (m, c), v in zip(parts, vs):
        t = v[m.faces]
        n = np.cross(t[:, 1] - t[:, 0], t[:, 2] - t[:, 0]); n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
        for tri, nn in zip(t, n):
            if nn[1] > 0:
                continue
            xs = (tri[:, 0] - lo[0]) * px_mm; zs = (hi[2] - tri[:, 2]) * px_mm
            x0, x1 = max(int(xs.min()), 0), min(int(xs.max()) + 1, W - 1)
            z0, z1 = max(int(zs.min()), 0), min(int(zs.max()) + 1, H - 1)
            if x1 < x0 or z1 < z0:
                continue
            gx, gz = np.meshgrid(np.arange(x0, x1 + 1) + .5, np.arange(z0, z1 + 1) + .5)
            d = (zs[1] - zs[2]) * (xs[0] - xs[2]) + (xs[2] - xs[1]) * (zs[0] - zs[2])
            if abs(d) < 1e-9:
                continue
            w0 = ((zs[1] - zs[2]) * (gx - xs[2]) + (xs[2] - xs[1]) * (gz - zs[2])) / d
            w1 = ((zs[2] - zs[0]) * (gx - xs[2]) + (xs[0] - xs[2]) * (gz - zs[2])) / d
            w2 = 1 - w0 - w1
            ok = (w0 >= -1e-6) & (w1 >= -1e-6) & (w2 >= -1e-6)
            dep = w0 * tri[0, 1] + w1 * tri[1, 1] + w2 * tri[2, 1]
            yy, xx = np.nonzero(ok & (dep < zb[z0:z1 + 1, x0:x1 + 1]))
            if len(yy):
                zb[z0 + yy, x0 + xx] = dep[yy, xx]
                img[z0 + yy, x0 + xx] = np.array(c) * (0.45 + 0.65 * max(0.0, float(-nn @ -L) * -1))
    return np.clip(img, 0, 1), (lo, hi, R)


def moved(m, dy=0, dz=0):
    c = m.copy(); c.apply_translation([0, dy, dz]); return c


def section(ax, m, x, color, edge='k'):
    l = intersections.mesh_plane(m, plane_normal=[1, 0, 0], plane_origin=[x, 0, 0])
    if not len(l):
        return
    segs = [LineString(np.round(s[:, [1, 2]], 3)) for s in l if np.abs(s[0] - s[1]).sum() > 1e-4]
    polys = sorted(polygonize(unary_union(segs)), key=lambda p: -p.area)
    # even-odd: a polygon inside an odd number of bigger ones is a hole
    for i, p in enumerate(polys):
        depth = sum(1 for q in polys[:i] if q.contains(p.representative_point()))
        if depth % 2 == 0:
            xy = np.array(p.exterior.coords)
            ax.fill(xy[:, 0], xy[:, 1], color=color, ec=edge, lw=.5, zorder=3)
        else:
            xy = np.array(p.exterior.coords)
            ax.fill(xy[:, 0], xy[:, 1], color='white', ec=edge, lw=.5, zorder=3)


def modem(ax):
    ys = [4.1, 4.1, 29.1, 33, 33, 29.1, 4.1]; zs = [MID - 1.5, MID + 1.5, MID + 22.2, MID + 22.2, MID - 22.2, MID - 22.2, MID - 1.5]
    ax.fill(ys, zs, color='#f4e3c8', ec='#b08040', lw=.8, zorder=1)
    ax.text(16, 24, 'modem front slope', ha='center', va='center', color='#a07030', fontsize=9, zorder=2)
    # LED readings: 22.3 and 26.7 down the slope from the crease
    for d, lab in ((22.3, '22.3'), (26.7, '26.7')):
        f = d / np.hypot(25, 20.7)
        ax.plot(29.1 - 25 * f, MID + 22.2 - 20.7 * f, 'o', color='#d0a000', ms=4, zorder=6)


def dim(ax, a, b, t, off=(0, 0), rot=0, fs=8):
    ax.annotate('', xy=a, xytext=b, arrowprops=dict(arrowstyle='<->', lw=.8, color='#c02020', shrinkA=0, shrinkB=0), zorder=8)
    ax.text((a[0] + b[0]) / 2 + off[0], (a[1] + b[1]) / 2 + off[1], t, color='#c02020', fontsize=fs, rotation=rot, ha='center', va='center', zorder=9,
            bbox=dict(fc='white', ec='none', pad=.6, alpha=.85))


def sheet(key, title, insert_dy, sec_xs, dims, fname):
    bodyn = [n for n in P if n.startswith(key) and 'body' in n][0]
    ins = [n for n in P if n.startswith(key) and 'body' not in n]
    fig = plt.figure(figsize=(14, 9.6))
    fig.suptitle(title, fontsize=13, x=.02, ha='left', fontweight='bold')
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.15], hspace=.1, wspace=.06, left=.03, right=.98, top=.93, bottom=.04)
    # assembled front, and exploded in the direction it goes in
    a1 = fig.add_subplot(gs[0, 0]); a2 = fig.add_subplot(gs[0, 1])
    img, _ = render([(P[bodyn], BODY)] + [(P[n], col(n)) for n in ins], 0, 0, 12)
    a1.imshow(img); a1.set_title('From the front, diffuser in', fontsize=10); a1.axis('off')
    az = -30 if insert_dy < 0 else 150
    img, _ = render([(P[bodyn], BODY)] + [(moved(P[n], insert_dy), col(n)) for n in ins], az, 22, 8)
    a2.imshow(img); a2.set_title('Pulled out the way it goes in (%s)' % ('from the front' if insert_dy < 0 else 'from behind'), fontsize=10); a2.axis('off')
    # sections
    for i, (x, sub) in enumerate(sec_xs):
        a = fig.add_subplot(gs[1, 0]) if i == 0 else fig.add_subplot(gs[1, 1])
        modem(a)
        section(a, P[bodyn], x, BODY)
        for n in ins:
            section(a, P[n], x, col(n))
        a.set_xlim(-1.5, 22); a.set_ylim(21, 40); a.set_aspect('equal'); a.set_title(sub, fontsize=10); a.grid(alpha=.2)
        a.set_xlabel('mm back from the plate front'); a.set_ylabel('height, mm')
        for d in dims.get(i, ()):
            dim(a, *d)
    fig.savefig(os.path.join(OUT, fname), dpi=105)
    plt.close(fig)


sheet('A', 'Option A: one bar, in from the FRONT, tilts in then snaps. Two filaments on the bar.', -24,
      [(127, 'Cut through the middle icon'), (109.75, 'Cut through a snap hook, between two icons')],
      {0: [((0, 25.2), (0, 35.25), '10', (-.8, 0)), ((0, 37), (1.5, 37), '1.5', (0.7, 1)), ((8, 26.2), (8, 34.25), 'tunnel 8', (1.5, 0))],
       1: [((1.5, 36.8), (7.4, 36.8), 'hook 6', (0, .8)), ((0, 37), (1.5, 37), '', (0, 0))]}, 'CM1P-diffuser_option_A.png')
sheet('B', 'Option B: one bar, in from BEHIND, tilts in then snaps. Front stays one piece.', 24,
      [(127, 'Cut through the middle icon'), (109.75, 'Cut through a snap hook, between two icons')],
      {0: [((1, 36.8), (2.2, 36.8), '1.2', (0, .8)), ((0, 38.2), (1, 38.2), '1 skin', (0, .8))],
       1: [((2.2, 37.5), (5, 37.5), 'hook 3', (0, .8))]}, 'CM1P-diffuser_option_B.png')
sheet('C', 'Option C: five round cups, in from BEHIND down the tunnels, each clicks into a groove. Front stays one piece.', 24,
      [(127, 'Cut through the middle icon'), (125, 'Cut 2 off centre, through a cup wall')],
      {0: [((3.9, 36), (5.6, 36), '', (0, 0)), ((0.42, 36.5), (1.92, 36.5), '1.5', (0, .8)), ((1.92, 38), (5.6, 38), 'skirt 3.7', (0, .8)), ((9, 26.2), (9, 34.25), 'tunnel 8.04', (2.1, 0))]},
      'CM1P-diffuser_option_C.png')
