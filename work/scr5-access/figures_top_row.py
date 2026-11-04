"""Pictures for layout C: 4 keystones in one top row, Hue low and forward."""
import subprocess
from pathlib import Path
import numpy as np, trimesh
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from figures_cut import sec
H = Path(__file__).parent; S = H / 'stl'; R = H.parent.parent; V = R / 'work/mesh-viewer'; T = H / 'png'; T.mkdir(exist_ok=True)
EXE = r'C:\Program Files\OpenSCAD\openscad.exe'
def render(name, rot, hide=(), d=500, c=(0, 0, 44.4), w=1500, h=800):
    f = T / f'{name}.png'; hd = '[' + ','.join(f'"{x}"' for x in hide) + ']'
    subprocess.run([EXE, '-o', str(f), '--imgsize', f'{w},{h}', '--camera', f'{c[0]},{c[1]},{c[2]},{rot[0]},{rot[1]},{rot[2]},{d}', '--projection', 'o' if rot[0] == 90 else 'p', '--colorscheme', 'Tomorrow',
                    '-D', 'opt="C"', '-D', 'part="all"', '-D', f'hide={hd}', str(H / 'access_concept.scad')], capture_output=True, text=True)
    return plt.imread(f)
fig = plt.figure(figsize=(14, 13)); g = fig.add_gridspec(3, 2, height_ratios=[.62, 1, .8])
a = fig.add_subplot(g[0, :]); a.imshow(render('c_front', (90, 0, 0), ('frame', 'pi', 'ribbon', 'fan', 'hue', 'deck', 'post', 'ks', 'heads'), d=345, h=420)); a.set_title('Front: 4 keystones across the top, screen 5 right, bottom left blank', loc='left', fontweight='bold'); a.set_axis_off()
a = fig.add_subplot(g[1, 0]); a.imshow(render('c_rear', (62, 0, 215), ('post',), d=620, c=(-5, 60, 44), w=1000, h=800)); a.set_title('From behind, Hue on', loc='left', fontweight='bold'); a.set_axis_off()
a = fig.add_subplot(g[1, 1]); a.imshow(render('c_rear2', (62, 0, 215), ('post', 'hue'), d=620, c=(-5, 60, 44), w=1000, h=800)); a.set_title('Hue off: full cradle, walls, 3 M6 on the front wall', loc='left', fontweight='bold'); a.set_axis_off()
a = fig.add_subplot(g[2, :])
C = dict(plate='#8a93a0', deck='#4f81bd', hue='#e9e4d0', jacks='#e0c040', plugs='#7fb3d9', cables='#3b6ea5')
for k in C: sec(a, S / f'C_{k}.stl', 0, -79.35, C[k], z=3 if k in ('jacks', 'plugs', 'cables') else 2)
a.plot([-5, 165], [88.8, 88.8], color='#999', ls=':'); a.plot([-5, 165], [0, 0], color='#999', ls=':')
a.annotate('', xy=(68.5, 40), xytext=(4, 40), arrowprops=dict(arrowstyle='<->', color='#c0392b', lw=1.6)); a.text(36, 42, 'Hue centre 64.5 back', color='#c0392b', ha='center', fontsize=11)
a.text(68, 18, 'Hue', ha='center', fontsize=12, zorder=9);
a.set_xlim(-5, 165); a.set_ylim(-5, 92); a.set_aspect('equal'); a.set_xlabel('mm behind plate front'); a.set_ylabel('Z mm'); a.set_title('Cut through a keystone column', loc='left', fontweight='bold')
fig.tight_layout(); fig.savefig(V / 'SCR5-AP_C_top_row.png', dpi=75)
