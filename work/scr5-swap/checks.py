"""Clash pairs (OpenSCAD intersection) and mass/lever table for the swap concepts. Writes checks.json next to this file."""
import concurrent.futures as cf, json, subprocess, struct, tempfile
from pathlib import Path
import trimesh
H = Path(__file__).parent; S = H / 'stl'; R = H.parent.parent
OUT = R / 'outputs/Screen_Pi_Hue_SCR5-H11_2026-11-03'
EXE = r'C:\Program Files\OpenSCAD\openscad.exe'
EXTRA = {'frame': OUT / 'SCR5-H8_frame.stl', 'screen': OUT / 'checks/ref_screen.stl'}
POST = R / 'work/rack-post-hex/assembled/post_left.stl'
def path(o, n):
    return EXTRA[n] if n in EXTRA else S / f'{o}_{n}.stl'
PAIRS = [('plate', 'floor'), ('plate', 'deck'), ('floor', 'deck'), ('plate', 'pi'), ('floor', 'pi'), ('deck', 'pi'), ('floor', 'hue'), ('deck', 'hue'), ('plate', 'hue'),
         ('pi', 'hue'), ('plate', 'ks'), ('floor', 'ks'), ('deck', 'ks'), ('pi', 'ks'), ('hue', 'ks'), ('floor', 'ribbon'), ('deck', 'ribbon'), ('plate', 'ribbon'), ('hue', 'ribbon'),
         ('frame', 'floor'), ('frame', 'deck'), ('frame', 'hue'), ('frame', 'pi'), ('screen', 'floor'), ('screen', 'deck'), ('screen', 'hue'), ('screen', 'pi'),
         ('mount', 'floor'), ('mount', 'deck'), ('mount', 'pi'), ('mount', 'plate'), ('fan', 'mount'), ('post', 'floor'), ('post', 'deck'), ('post', 'fan'), ('post', 'mount')]
def imp(o, n):
    if n == 'post': return f'translate([0,4,0])import("{POST.as_posix()}");'
    return f'import("{path(o, n).as_posix()}");'
def run(a):
    o, x, y = a
    with tempfile.TemporaryDirectory() as t:
        s = Path(t) / 'x.scad'; d = Path(t) / 'x.stl'
        s.write_text(f'intersection(){{{imp(o, x)}{imp(o, y)}}}', encoding='utf-8')
        r = subprocess.run([EXE, '--export-format', 'binstl', '-o', str(d), str(s)], capture_output=True, text=True, encoding='utf-8')
        v = 0.0
        if d.exists() and d.stat().st_size > 84:
            v = abs(trimesh.load(d).volume)
    return dict(opt=o, a=x, b=y, mm3=round(v, 2))
J = [(o, a, b) for o in ('S1', 'S2', 'N') for a, b in PAIRS]
with cf.ThreadPoolExecutor(4) as x:
    rows = list(x.map(run, J))
PLA = 1.24e-3
def com(p):
    m = trimesh.load(p); return abs(m.volume) * PLA, m.center_mass[1], m.center_mass[0]
HUE_G, PI_G, FAN_G = 150.0, 46.0, 15.0
table = {}
def add(name, parts, hue_xy, pi_y):
    tot = 0.0; mom = 0.0; mx = 0.0; det = {}
    for n, p in parts.items():
        g, y, xc = com(p); det[n] = round(g); tot += g; mom += g * (y - 4); mx += g * (xc + 60)
    for g, y, xc in ((HUE_G, hue_xy[1], hue_xy[0]), (PI_G, pi_y, -74.0), (FAN_G, 46, -115)):
        tot += g; mom += g * (y - 4); mx += g * (xc + 60)
    table[name] = dict(grams_printed=det, total_g=round(tot), moment_gmm=round(mom), lever_mm=round(mom / tot, 1), twist_gmm=round(mx), hue_lever=round(hue_xy[1] - 4, 1))
add('H11', {'floor': OUT / 'SCR5-H11_floor.stl', 'deck': OUT / 'SCR5-H11_deck.stl'}, (-54.4, 97), 46.5)
add('S1', {'floor': S / 'S1_floor.stl', 'deck': S / 'S1_deck.stl'}, (-34, 68.5), 46.5)
add('S2', {'floor': S / 'S2_floor.stl', 'deck': S / 'S2_deck.stl'}, (-34, 68.5), 63.5)
add('N', {'floor': S / 'N_floor.stl', 'deck': S / 'N_deck.stl'}, (-34, 81.5), 46.5)
json.dump(dict(pairs=rows, table=table), open(H / 'checks.json', 'w', encoding='utf-8'), indent=1)
for r in rows:
    if r['mm3'] > 0: print(r)
for k, v in table.items(): print(k, v)
