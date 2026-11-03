"""Front and side section pictures of H11 and the swap concepts, cut from the real meshes."""
import subprocess
from pathlib import Path
import numpy as np, trimesh
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path as MP
from matplotlib.patches import PathPatch, Rectangle, FancyArrowPatch
H = Path(__file__).parent; S = H / 'stl'; R = H.parent.parent
OUT = R / 'outputs/Screen_Pi_Hue_SCR5-H11_2026-11-03'
V = R / 'work/mesh-viewer'
C = dict(plate='#8a93a0', floor='#4f81bd', deck='#2f5f96', frame='#b9b9b9', pi='#3aa655', hue='#e8a33d', fan='#9b6fc4', mount='#b49ad6', screen='#30343a', post='#d9d9d9')
def loops(m, axis, val, ix):
    """Slice triangles with a plane, chain the segments into closed loops."""
    t = m.vertices[m.faces]; d = t[:, :, axis] - val + 1e-7
    segs = []
    for tri, dd in zip(t[(d.min(1) < 0) & (d.max(1) > 0)], d[(d.min(1) < 0) & (d.max(1) > 0)]):
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
def sec(ax, f, axis, val, col, a=1.0, ec='k', z=2):
    m = trimesh.load(f); ix = (0, 2) if axis == 1 else (1, 2)
    verts, codes = [], []
    for q in loops(m, axis, val, ix):
        verts += q.tolist(); codes += [MP.MOVETO] + [MP.LINETO] * (len(q) - 2) + [MP.CLOSEPOLY]
    if verts: ax.add_patch(PathPatch(MP(verts, codes), fc=col, ec=ec, lw=.4, alpha=a, zorder=z))
OPT = {
 'H11': dict(plate=OUT / 'SCR5-H11_plate.stl', floor=OUT / 'SCR5-H11_floor.stl', deck=OUT / 'SCR5-H11_deck.stl', pi=S / 'N_pi.stl', hue=OUT / 'checks/ref_hue.stl', mount=OUT / 'SCR5-H11_fanmount.stl', fan=OUT / 'checks/ref_fan.stl'),
}
for o in ('S1', 'S2', 'N'):
    OPT[o] = {p: S / f'{o}_{p}.stl' for p in ('plate', 'floor', 'deck', 'pi', 'hue', 'mount', 'fan')}
OPT['N']['plate'] = OUT / 'SCR5-H11_plate.stl'
FRAME = OUT / 'SCR5-H8_frame.stl'; SCREEN = OUT / 'checks/ref_screen.stl'
TITLE = {'H11': 'H11 today', 'S1': 'Swap A: ports stay in front, keystone moves down', 'S2': 'Swap B: keystone stays, Pi turned round', 'N': 'No swap: Hue forward and right'}
HUE = {'H11': (93, 59), 'S1': (64.5, 24), 'S2': (64.5, 24), 'N': (77.5, 59)}
HZ = {'H11': 59, 'S1': 23, 'S2': 23, 'N': 59}
HY = {'H11': 97, 'S1': 68.5, 'S2': 68.5, 'N': 81.5}
# ---------- side cut at X -74, through the Pi ----------
fig, axs = plt.subplots(2, 2, figsize=(14, 8.4))
for ax, o in zip(axs.flat, ('H11', 'S1', 'S2', 'N')):
    P = OPT[o]
    sec(ax, P['hue'], 0, -60, C['hue'], z=1); sec(ax, P['pi'], 0, -74.0, C['pi'], z=3)
    for k in ('floor', 'deck', 'plate'): sec(ax, P[k], 0, -74.0, C[k], z=2)
    ax.annotate('', xy=(HY[o], 3), xytext=(4, 3), arrowprops=dict(arrowstyle='<->', color='#c0392b', lw=1.6), zorder=9)
    ax.text((HY[o] + 4) / 2, -4.5, f'Hue lever {HY[o]-4:.0f} mm', color='#c0392b', ha='center', fontsize=10)
    ax.plot([HY[o]], [HZ[o]], marker='v', color='#c0392b', ms=9, zorder=9)
    ax.text(HY[o], HZ[o] - 8 if o in ('H11', 'N') else HZ[o] + 2, 'Hue', ha='center', fontsize=10, zorder=9)
    ax.set_title(TITLE[o], fontsize=11, loc='left'); ax.set_xlim(-6, 150); ax.set_ylim(-8, 92); ax.set_aspect('equal')
    ax.set_xlabel('mm back from the front of the plate'); ax.set_ylabel('mm up from slot bottom'); ax.grid(alpha=.15)
    ax.axhline(88.8, color='#999', lw=.6, ls=':')
fig.suptitle('Side cut through the Pi (X -74). Blue = printed tray, grey = plate, green = Pi, orange = Hue', fontsize=12)
fig.tight_layout(); fig.savefig(V / 'SCR5-swap_side_cuts.png', dpi=110); plt.close(fig)
# ---------- plate from the front ----------
fig, axs = plt.subplots(2, 2, figsize=(14, 7.2))
def rect(ax, x0, z0, x1, z1, col, label=None, a=.55, ls='-'):
    ax.add_patch(Rectangle((x0, z0), x1 - x0, z1 - z0, fc=col, ec='k', lw=.7, alpha=a, ls=ls, zorder=4))
    if label: ax.text((x0 + x1) / 2, (z0 + z1) / 2, label, ha='center', va='center', fontsize=8, zorder=6)
for ax, key in zip(axs.flat, ('H11', 'naive', 'S1', 'S2')):
    o = 'H11' if key == 'naive' else key
    sec(ax, OPT[o]['plate'], 1, 2, C['plate'], a=.9)
    if key == 'H11':
        rect(ax, -103, 51, -82, 84.5, '#f1c40f', 'keystone')
        for x in (-71, -50): rect(ax, x - 7, 57.5, x + 7, 71.5, '#2f5f96', 'M6', ls='--')
        for x, w in ((-93, 15), (-75, 15), (-56.3, 17.5)): rect(ax, x - w / 2, 18, x + w / 2, 35.5, C['pi'], 'Pi')
    if key == 'naive':
        rect(ax, -103, 51, -82, 84.5, '#f1c40f', None)
        for x in (-71, -50): rect(ax, x - 7, 57.5, x + 7, 71.5, '#2f5f96', None, ls='--')
        for x, w in ((-93, 15), (-75, 15), (-56.3, 17.5)): rect(ax, x - w / 2, 50, x + w / 2, 68, '#e74c3c', 'Pi', a=.65)
        ax.text(-76, 90.5, 'all three openings hit something', color='#c0392b', ha='center', fontsize=9, fontweight='bold')
    if key == 'S1':
        rect(ax, -102, 8, -81, 41.5, '#f1c40f', 'keystone\nmoved down')
        for x in (-71, -50): rect(ax, x - 7, 70.5, x + 7, 84.5, '#2f5f96', 'M6 up', ls='--')
        for x, w in ((-93, 15), (-75, 15), (-56.3, 17.5)): rect(ax, x - w / 2, 48.3, x + w / 2, 65.8, C['pi'], 'Pi')
    if key == 'S2':
        rect(ax, -103, 51, -82, 84.5, '#f1c40f', 'keystone\nsame')
        for x in (-71, -50): rect(ax, x - 7, 57.5, x + 7, 71.5, '#2f5f96', 'M6\nsame', ls='--')
        ax.text(-76, 28, 'no Pi openings:\nUSB and Ethernet\nnow at the rear', ha='center', va='center', fontsize=9, zorder=6)
    ax.set_title({'H11': 'H11 today', 'naive': 'Just lifting the Pi straight up', 'S1': 'Swap A', 'S2': 'Swap B'}[key], loc='left', fontsize=11)
    ax.set_xlim(-128, 128); ax.set_ylim(-3, 94); ax.set_aspect('equal'); ax.set_xlabel('X mm, seen from the front'); ax.grid(alpha=.12)
fig.tight_layout(); fig.savefig(V / 'SCR5-swap_plate_fronts.png', dpi=110); plt.close(fig)
# ---------- 3D colour shots, rear left ----------
EXE = r'C:\Program Files\OpenSCAD\openscad.exe'
for o, P in OPT.items():
    body = ''.join(f'color("{C[k]}")import("{Path(f).as_posix()}");' for k, f in P.items()) + f'color("{C["frame"]}")import("{FRAME.as_posix()}");color("{C["screen"]}")import("{SCREEN.as_posix()}");'
    s = H / f'shot_{o}.scad'; s.write_text(body, encoding='utf-8')
    subprocess.run([EXE, '-o', str(V / f'SCR5-swap_3d_{o}.png'), '--imgsize=1100,800', '--viewall', '--autocenter', '--camera=0,0,0,62,0,215,500', '--colorscheme=Tomorrow', '--projection=p', str(s)], capture_output=True, text=True, encoding='utf-8')
# ---------- H11 HDMI question ----------
s = H / 'hdmi.scad'; s.write_text(f'intersection(){{import("{(OUT / "SCR5-H11_floor.stl").as_posix()}");import("{(S / "N_pi.stl").as_posix()}");}}', encoding='utf-8')
d = H / 'hdmi.stl'; subprocess.run([EXE, '--export-format', 'binstl', '-o', str(d), str(s)], capture_output=True, text=True)
if d.exists() and d.stat().st_size > 84:
    m = trimesh.load(d); print('H11 floor vs Pi with connectors', round(abs(m.volume), 1), m.bounds.round(2).tolist())
else:
    print('H11 floor vs Pi: none')
