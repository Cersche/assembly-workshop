"""SCR5-J1: bending numbers, 3MF in print orientation, pictures. Run after SCR5-J1_build.py."""
import json, struct, subprocess, zipfile
from pathlib import Path
import numpy as np, trimesh
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE = Path(__file__).resolve().parent.parent; C = HERE / 'checks'; REPO = HERE.parent.parent; V = REPO / 'work/mesh-viewer'
H11 = REPO / 'outputs/Screen_Pi_Hue_SCR5-H11_2026-11-03'; EXE = r'C:\Program Files\OpenSCAD\openscad.exe'; SCAD = HERE / 'src/SCR5-J.scad'
# ---- bending at the plate: same assumptions as work/scr5-swap (Hue 150 g not weighed, printed 1.24 g/cm3 solid) ----
PLA = 1.24e-3; M = 150 * (82.2 - 4); tot = 150
for f in ('deck', 'underframe'):
    m = trimesh.load(HERE / f'SCR5-J1_{f}.stl'); g = abs(m.volume) * PLA; M += g * (m.center_mass[1] - 4); tot += g
H11M = 27463
num = dict(tray_moment_gmm=round(M), pct_of_H11=round(M / H11M * 100), tray_total_g=round(tot), hue_lever=78.2, pull_g_per_row_58mm=round(M / 58))
print(num); json.dump(num, open(C / 'bending.json', 'w', encoding='utf-8'), indent=1)
# ---- 3MF ----
def read(p):
    d = p.read_bytes(); n = struct.unpack_from('<I', d, 80)[0]; W = {}; T = []
    for i in range(n):
        c = struct.unpack_from('<9f', d, 96 + 50 * i); T.append([W.setdefault(c[k:k + 3], len(W)) for k in (0, 3, 6)])
    return list(W), T
ROT = {'down_front': lambda x, y, z: (x, -z, y), 'down_rear': lambda x, y, z: (x, z, -y), 'upright': lambda x, y, z: (x, y, z), 'flip': lambda x, y, z: (-x, y, -z), 'side': lambda x, y, z: (z, y, -x)}
PARTS = [('SCR5-J1 plate', HERE / 'SCR5-J1_plate.stl', 'down_front'), ('SCR5-J1 frame (3 pieces)', HERE / 'SCR5-J1_frame.stl', 'down_rear'), ('SCR5-J1 deck', HERE / 'SCR5-J1_deck.stl', 'upright'),
         ('SCR5-J1 underframe', HERE / 'SCR5-J1_underframe.stl', 'flip'), ('SCR5-J1 fan mount', HERE / 'SCR5-J1_fanmount.stl', 'down_rear')] + [(f'SCR5-H8 pin{i} (unchanged)', H11 / f'SCR5-H8_pin{i}.stl', 'side') for i in (1, 2, 3)]
objs = []; xcur = 0
for name, f, rot in PARTS:
    W, T = read(f); W = [ROT[rot](*v) for v in W]
    mn = [min(v[k] for v in W) for k in range(3)]; mx = max(v[0] for v in W); dx = xcur - mn[0]
    W = [(v[0] + dx, v[1] - mn[1], v[2] - mn[2]) for v in W]; xcur += mx - mn[0] + 12; objs.append((name, W, T))
out = ['<?xml version="1.0" encoding="UTF-8"?>', '<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">', '<resources>']
for i, (name, W, T) in enumerate(objs, 1):
    out.append(f'<object id="{i}" name="{name}" type="model"><mesh><vertices>')
    out += [f'<vertex x="{x:.6f}" y="{y:.6f}" z="{z:.6f}"/>' for x, y, z in W]
    out.append('</vertices><triangles>')
    out += [f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in T]
    out.append('</triangles></mesh></object>')
out.append('</resources><build>' + ''.join(f'<item objectid="{i}"/>' for i in range(1, len(objs) + 1)) + '</build></model>')
dst = HERE / 'SCR5-J1_screen_pi_hue_4port_set.3mf'
with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    z.writestr('_rels/.rels', '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    z.writestr('3D/3dmodel.model', '\n'.join(out))
m = zipfile.ZipFile(dst).read('3D/3dmodel.model').decode()
print(dst.name, 'vertex', m.count('<vertex '), 'triangle', m.count('<triangle '), 'objects', m.count('<object '), 'HAS ns0' if 'ns0' in m else 'no ns0')
# ---- pictures ----
W, HH = 1500, 800
def render(name, rot, hide=(), d=500, c=(0, 0, 44.4), w=W, h=HH):
    f = C / f'{name}.png'; hd = '[' + ','.join(f'"{x}"' for x in hide) + ']'
    subprocess.run([EXE, '-o', str(f), '--imgsize', f'{w},{h}', '--camera', f'{c[0]},{c[1]},{c[2]},{rot[0]},{rot[1]},{rot[2]},{d}', '--projection', 'o' if rot[0] == 90 else 'p', '--colorscheme', 'Tomorrow', '-D', 'part="all"', '-D', f'hide={hd}', str(SCAD)], capture_output=True, text=True)
    return plt.imread(f)
def note(ax, t, xy, tx):
    ax.annotate(t, xy=xy, xytext=tx, fontsize=10, color='#c0392b', ha='center', va='center', bbox=dict(fc='white', ec='#c0392b', lw=.8, pad=2.5), arrowprops=dict(arrowstyle='-', color='#c0392b', lw=1.1))
ALL = ('frame', 'pi', 'ribbon', 'fan', 'hue', 'deck', 'post', 'ks', 'heads')
fig, axs = plt.subplots(3, 1, figsize=(13, 16))
axs[0].imshow(render('j_front', (90, 0, 0), ('frame', 'pi', 'ribbon', 'fan', 'hue', 'deck', 'post', 'ks', 'heads'), d=345, h=420)); axs[0].set_title('SCR5-J1 front: 4 keystones, screen where it was. No screw shows in the free strip', loc='left', fontweight='bold')
axs[1].imshow(render('j_rear34', (62, 0, 215), d=620, c=(-5, 60, 44), w=1200, h=800)); axs[1].set_title('From behind: Hue between the rows, cables over and under', loc='left', fontweight='bold')
px = HH / (380 * 2 * np.tan(np.radians(22.5 / 2)))
axs[2].imshow(render('j_joints', (90, 0, 180), ('hue', 'fan', 'ks', 'post'), d=380, c=(-55, 0, 44.4)))
for x, z in ((-60, 15), (-47, 15), (-60, 73), (-47, 73)): axs[2].plot([W / 2 - (x + 55) * px], [HH / 2 - (z - 44.4) * px], 'o', mfc='none', mec='#c0392b', ms=18, mew=2)
axs[2].set_title('From behind, Hue off: 4 M6, 58 apart in height. A driver reaches all 4 straight in, even with the Hue on', loc='left', fontweight='bold')
for ax in axs: ax.set_axis_off()
fig.tight_layout(); fig.savefig(V / 'SCR5-J1_views.png', dpi=75)
