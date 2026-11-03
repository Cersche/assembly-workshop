"""Pictures for the access panel options, rendered from the concept model with OpenSCAD and labelled with matplotlib."""
import subprocess
from pathlib import Path
import numpy as np, trimesh
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path as MP
from matplotlib.patches import PathPatch
H = Path(__file__).parent; S = H / 'stl'; R = H.parent.parent; V = R / 'work/mesh-viewer'; T = H / 'png'; T.mkdir(exist_ok=True)
OUT = R / 'outputs/Screen_Pi_Hue_SCR5-H11_2026-11-03'
EXE = r'C:\Program Files\OpenSCAD\openscad.exe'
W, HH, D = 1500, 800, 500
def scale(d): return HH / (d * 2 * np.tan(np.radians(22.5 / 2)))
def render(name, opt, rot, hide=(), rail=False, part='all', d=D, c=(0, 0, 44.4), w=W, h=HH):
    f = T / f'{name}.png'
    hd = '[' + ','.join(f'"{x}"' for x in hide) + ']'
    cam = f'{c[0]},{c[1]},{c[2]},{rot[0]},{rot[1]},{rot[2]},{d}'
    subprocess.run([EXE, '-o', str(f), '--imgsize', f'{w},{h}', '--camera', cam, '--projection', 'o' if rot[2] % 90 == 0 and rot[0] == 90 else 'p', '--colorscheme', 'Tomorrow',
                    '-D', f'opt="{opt}"', '-D', f'part="{part}"', '-D', f'hide={hd}', '-D', f'rail={"true" if rail else "false"}', str(H / 'access_concept.scad')], capture_output=True, text=True)
    return plt.imread(f)
def show(ax, img, title=None):
    ax.imshow(img); ax.set_axis_off()
    if title: ax.set_title(title, loc='left', fontsize=13, fontweight='bold')
def note(ax, txt, xy, tx, col='#c0392b', fs=10):
    ax.annotate(txt, xy=xy, xytext=tx, fontsize=fs, color=col, ha='center', va='center', bbox=dict(fc='white', ec=col, lw=.8, pad=2.5), arrowprops=dict(arrowstyle='-', color=col, lw=1.1))
ALL = ('frame', 'pi', 'ribbon', 'fan', 'hue', 'deck', 'post', 'ks', 'heads')
# ---------- 1: the fronts ----------
fig, axs = plt.subplots(2, 2, figsize=(16, 6.2))
T1 = {'A': '1. SIX upright, screen stays', 'B': '2. EIGHT upright, screen 5 right', 'S': '3. EIGHT sideways, screen stays', 'T': '4. TEN (2 upright + 8 sideways), screen 5.6 right'}
for ax, o in zip(axs.flat, 'ABST'):
    show(ax, render(f'front_{o}', o, (90, 0, 0), h=420, hide=ALL, d=345), T1[o])
fig.tight_layout(); fig.savefig(V / 'SCR5-AP_1_fronts.png', dpi=75); plt.close(fig)
# ---------- 2: rear three-quarter ----------
fig, axs = plt.subplots(1, 2, figsize=(16, 7.6))
for ax, o, t in ((axs[0], 'A', '1. Six: from behind'), (axs[1], 'B', '2. Eight: same view')):
    show(ax, render(f'rear34_{o}', o, (62, 0, 215), d=620, c=(-5, 55, 44), w=1200, h=1000), t)
fig.tight_layout(); fig.savefig(V / 'SCR5-AP_2_overview.png', dpi=80); plt.close(fig)
# ---------- 3: Pi on the screen, rear view ----------
fig, ax = plt.subplots(figsize=(15, 8))
img = render('pi_rear', 'A', (90, 0, 180), hide=('hue', 'deck', 'post', 'ks', 'fan', 'heads'), d=340, c=(33, 0, 44.4))
show(ax, img, "Pi on the screen's own 4 standoffs, seen from behind (Layout 1, fan off to show it)")
px = scale(340)
X = lambda x: W / 2 - (x - 33) * px; Z = lambda z: HH / 2 - (z - 44.4) * px
pi0 = -8.15
for t, x, z, tx, tz in (('USB-C on top: right-angle plug needed\n(13.7 to the plate top)', pi0 + 11.2, 75, 1120, 30),
                        ('micro-HDMI x2 and audio: top edge, not useful here', pi0 + 39.5, 75, 560, 30),
                        ('USB x2 + Ethernet point this way (right, from the front).\n48 to the post, so short or right-angle plugs', pi0 + 87, 55, 210, 640),
                        ('GPIO along the bottom, fan plugs in from behind', pi0 + 30, 19, 800, 770),
                        ('50 mm DSI ribbon, screen to Pi: about 29 + slack', -14, 45, 1330, 300),
                        ('SD card here, under the ribbon:\nHue out, then fingers', pi0 - 2, 40, 1320, 560)):
    note(ax, t, (X(x), Z(z)), (tx, tz))
for x in (-4.65, 53.35):
    for z in (70.1, 21.1): ax.plot([X(x)], [Z(z)], 'o', mfc='none', mec='#c0392b', ms=13, mew=1.6)
note(ax, "M2.5 socket head x 4 into the\nscreen's own brass standoffs", (X(53.35), Z(21.1)), (480, 700))
fig.tight_layout(); fig.savefig(V / 'SCR5-AP_3_pi_on_screen.png', dpi=80); plt.close(fig)
# ---------- 4: side cut through a keystone column vs H11 ----------
C = dict(plate='#8a93a0', deck='#4f81bd', floor='#7da7d9', hue='#e9e4d0', jacks='#e0c040', plugs='#7fb3d9', cables='#3b6ea5', pi='#2e9e4f')
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
fig, axs = plt.subplots(2, 1, figsize=(13, 8.6))
ax = axs[0]
for k, f in (('floor', OUT / 'SCR5-H11_floor.stl'), ('deck', OUT / 'SCR5-H11_deck.stl'), ('plate', OUT / 'SCR5-H11_plate.stl'), ('hue', OUT / 'checks/ref_hue.stl'), ('pi', OUT / 'checks/ref_pi.stl')):
    sec(ax, f, 0, -75.0, C[k], z=3 if k == 'hue' else 2)
ax.annotate('', xy=(97, 3), xytext=(4, 3), arrowprops=dict(arrowstyle='<->', color='#c0392b', lw=1.6)); ax.text(50, -5, 'H11 today: Hue centre 93 behind the plate, tray to Y 142', color='#c0392b', ha='center', fontsize=11)
ax.set_title('H11 today, cut through the Pi', loc='left', fontweight='bold')
ax = axs[1]
for k in ('hue', 'deck', 'plate', 'jacks', 'plugs', 'cables'):
    sec(ax, S / f'A_{k}.stl', 0, -79.35, C[k], z=3 if k in ('jacks', 'plugs', 'cables') else 2)
ax.annotate('', xy=(71, 3), xytext=(4, 3), arrowprops=dict(arrowstyle='<->', color='#c0392b', lw=1.6)); ax.text(40, -5, 'Hue centre 67 behind the plate, tray ends Y 119', color='#c0392b', ha='center', fontsize=11)
ax.text(108, 79, 'Top row: plug and cable pass over the Hue', fontsize=11); ax.text(122, 8, 'Bottom row: under the deck', fontsize=11); ax.text(70, 44, 'Hue', fontsize=12, ha='center', zorder=9)
ax.set_title('Layouts 1 and 2: Hue between the rows. Cut through a keystone column', loc='left', fontweight='bold')
for ax in axs:
    ax.plot([-5, 165], [88.8, 88.8], color='#999', ls=':'); ax.plot([-5, 165], [0, 0], color='#999', ls=':')
    ax.set_xlim(-5, 165); ax.set_ylim(-10, 92); ax.set_aspect('equal'); ax.set_xlabel('mm behind plate front'); ax.set_ylabel('Z mm')
fig.tight_layout(); fig.savefig(V / 'SCR5-AP_4_side_cut.png', dpi=80); plt.close(fig)
# ---------- 5: joints and screw paths, Hue out, rear view ----------
fig, axs = plt.subplots(2, 1, figsize=(13, 10))
J = {'A': [(-40, 21.5), (-40, 59), (-69, 44.4)], 'B': [(-90, 44.4), (-60, 44.4)]}
px = scale(380)
for ax, o, t in ((axs[0], 'A', 'Layout 1: 3 M6, 37.5 apart in height. Hue out for the upper two; the low one stays reachable'), (axs[1], 'B', 'Layout 2: 2 M6, both at mid height, so the Hue pulls harder on them')):
    show(ax, render(f'joints_{o}', o, (90, 0, 180), hide=('hue', 'fan', 'ks', 'post'), d=380, c=(-55, 0, 44.4)), t)
    for x, z in J[o]:
        ax.plot([W / 2 - (x + 55) * px], [HH / 2 - (z - 44.4) * px], 'o', mfc='none', mec='#c0392b', ms=20, mew=2)
fig.tight_layout(); fig.savefig(V / 'SCR5-AP_5_joints.png', dpi=70); plt.close(fig)
