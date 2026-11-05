"""SCR5-J5 (tray only): bending numbers, 3MF in print orientation, pictures. Run after SCR5-J4_build.py."""
import json, struct, subprocess, zipfile
from pathlib import Path
import numpy as np, trimesh
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE = Path(__file__).resolve().parent.parent; C = HERE / 'checks'; REPO = HERE.parent.parent; V = REPO / 'work/mesh-viewer'
H11 = REPO / 'outputs/Screen_Pi_Hue_SCR5-H11_2026-11-03'; EXE = r'C:\Program Files\OpenSCAD\openscad.exe'; SCAD = HERE / 'src/SCR5-J5.scad'
# ---- bending at the plate: same assumptions as work/scr5-swap (Hue 150 g not weighed, printed 1.24 g/cm3 solid) ----
PLA = 1.24e-3; M = 150 * (68.5 - 4); tot = 150
for f in ('deck',):
    m = trimesh.load(HERE / f'SCR5-J5_{f}.stl'); g = abs(m.volume) * PLA; M += g * (m.center_mass[1] - 4); tot += g
H11M = 27463
num = dict(tray_moment_gmm=round(M), pct_of_H11=round(M / H11M * 100), tray_total_g=round(tot), hue_lever=64.5, pull_g_M6_row_36p5mm_above_pads=round(M / 36.5))
print(num); json.dump(num, open(C / 'bending.json', 'w', encoding='utf-8'), indent=1)
# ---- 3MF ----
def read(p):
    d = p.read_bytes(); n = struct.unpack_from('<I', d, 80)[0]; W = {}; T = []
    for i in range(n):
        c = struct.unpack_from('<9f', d, 96 + 50 * i); T.append([W.setdefault(c[k:k + 3], len(W)) for k in (0, 3, 6)])
    return list(W), T
ROT = {'down_front': lambda x, y, z: (x, -z, y), 'down_rear': lambda x, y, z: (x, z, -y), 'upright': lambda x, y, z: (x, y, z), 'flip': lambda x, y, z: (-x, y, -z), 'side': lambda x, y, z: (z, y, -x)}
PARTS = [('SCR5-J5 tray (Hue cradle loosened)', HERE / 'SCR5-J5_deck.stl', 'upright')]
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
dst = HERE / 'SCR5-J5_tray.3mf'
with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    z.writestr('_rels/.rels', '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    z.writestr('3D/3dmodel.model', '\n'.join(out))
m = zipfile.ZipFile(dst).read('3D/3dmodel.model').decode()
print(dst.name, 'vertex', m.count('<vertex '), 'triangle', m.count('<triangle '), 'objects', m.count('<object '), 'HAS ns0' if 'ns0' in m else 'no ns0')
