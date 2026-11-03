"""Pictures of the S3 concept: Pi on the deck, ports through the plate, keystone on its side above them."""
import subprocess, re
from pathlib import Path
import numpy as np, trimesh, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path as MP
from matplotlib.patches import PathPatch, Rectangle
H = Path(__file__).parent; S = H / 'stl'; R = H.parent.parent; V = R / 'work/mesh-viewer'
src = (H / 'figures_no_keystone.py').read_text(encoding='utf-8')
exec(src[src.index('def loops'):src.index('OPT = {')])
C = dict(plate='#8a93a0', floor='#4f81bd', deck='#2f5f96', pi='#3aa655', hue='#e8a33d')
P = {k: S / f'S3_{k}.stl' for k in ('plate', 'floor', 'deck', 'pi', 'hue', 'mount', 'fan', 'ks')}
fig, axs = plt.subplots(1, 3, figsize=(19, 6.2), gridspec_kw=dict(width_ratios=[1.35, 1, 1]))
ax = axs[0]; sec(ax, P['plate'], 1, 2, C['plate'], a=.9)
def rect(x0, z0, x1, z1, col, label, ls='-'):
    ax.add_patch(Rectangle((x0, z0), x1 - x0, z1 - z0, fc=col, ec='k', lw=.8, alpha=.55, ls=ls, zorder=4)); ax.text((x0 + x1) / 2, (z0 + z1) / 2, label, ha='center', va='center', fontsize=9, zorder=6)
rect(-108.5, 64.5, -75, 85.5, '#f1c40f', 'keystone on its side\n33.5 wide x 21 tall')
for x in (-64.5, -50): rect(x - 7, 68, x + 7, 82, '#2f5f96', 'M6', '--')
for x, w, l in ((-93, 15, 'USB'), (-75, 15, 'USB'), (-56.3, 17.5, 'LAN')): rect(x - w / 2, 44.8, x + w / 2, 62.3, C['pi'], l)
for z, t in ((88.8, 'plate top 88.8'), (85.5, 'keystone top 85.5 (3.3 of plate left)'), (64.5, 'keystone bottom 64.5'), (62.3, 'port tops 62.3 (2.2 web)')):
    ax.plot([-128, -36], [z, z], color='#c0392b', lw=.7, zorder=7); ax.text(-35, z, t, color='#c0392b', fontsize=8, va='center', zorder=8, bbox=dict(fc='w', ec='none', pad=.5))
ax.set_xlim(-128, 40); ax.set_ylim(-3, 92); ax.set_aspect('equal'); ax.grid(alpha=.12); ax.set_title('Plate from the front (left half)', loc='left')
for ax, x, t in ((axs[1], -91.75, 'Side cut through the keystone'), (axs[2], -64.5, 'Side cut through the left M6 joint')):
    sec(ax, P['hue'], 0, -60, C['hue'], z=1); sec(ax, P['pi'], 0, x, C['pi'], z=3)
    for k in ('floor', 'deck', 'plate'): sec(ax, P[k], 0, x, C[k], z=2)
    ax.text(68, 22, 'Hue', ha='center', zorder=9); ax.set_xlim(-6, 120); ax.set_ylim(-3, 92); ax.set_aspect('equal'); ax.grid(alpha=.15); ax.set_title(t, loc='left'); ax.set_xlabel('mm back from the plate front')
axs[1].add_patch(Rectangle((4, 67), 34, 16, fc='#f1c40f', ec='k', ls='--', alpha=.4, zorder=5)); axs[1].text(21, 75, 'jack + cable\n(size not measured)', ha='center', va='center', fontsize=8, zorder=6)
fig.tight_layout(); fig.savefig(V / 'SCR5-swap_S3.png', dpi=100)
