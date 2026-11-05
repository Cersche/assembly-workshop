"""MRT-F digital checks: build parts, mesh closure, overhangs, then clash pairs on SOURCE modules with controls (importing the tray STL fails in CGAL and reads as a false clear)."""
import subprocess, pathlib, sys, tempfile, re
import numpy as np, trimesh
O = r'C:/Program Files/OpenSCAD/openscad.exe'
out = pathlib.Path('stl').resolve()
def bodies(m):  # no scipy here: union-find over shared vertices
    par = list(range(len(m.vertices)))
    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]; a = par[a]
        return a
    for x, y, z in m.faces.tolist():
        par[find(y)] = find(x); par[find(z)] = find(x)
    return len({find(int(i)) for i in np.unique(m.faces)})
for p, tag in [('tray', 'MRT-F'), ('cover_j', 'MRT-F'), ('cover_o', 'MRT-F'), ('cover_i', 'MRT-F'), ('jig', 'MRT-T3')]:
    f = out / f'{tag}_{p}.stl'
    r = subprocess.run([O, '-o', str(f), '--export-format', 'binstl', '-D', f'part="{p}"', 'MRT-F.scad'], capture_output=True, text=True)
    bad = [l for l in r.stderr.splitlines() if 'ERROR' in l or 'WARNING' in l or 'not closed' in l]
    m = trimesh.load(f)
    print(p, 'ok' if r.returncode == 0 else 'FAIL', bad[:4], 'watertight', m.is_watertight, 'bodies', bodies(m), 'cm3', round(m.volume / 1000, 1), np.round(m.bounds, 2).tolist(), flush=True)
    z0 = m.bounds[0][2]; n = m.face_normals; a = m.area_faces; c = m.triangles_center
    over = (n[:, 2] < -np.cos(np.radians(45)) - 0.01) & (c[:, 2] > z0 + 0.05)
    print('  overhang past 45 mm2', round(a[over].sum(), 1), flush=True)
src = pathlib.Path('MRT-F.scad').resolve().as_posix()
S = {'tray': 'tray();', 'plate': 'plate();', 'cables': 'cables();', 'dev': 'union(){screenbeam();splitter();}', 'cov': 'union(){cover_j();cover_o();cover_i();}', 'jig': 'translate([0,0,2])jig();', 'bl': 'shoe("MRT-C-L");'}
t = pathlib.Path(tempfile.mkdtemp())
def go(a, b):
    f = t / 'c.scad'; f.write_text(f'include <{src}>\npart="none";\nintersection(){{{a}{b}}}', encoding='utf-8')
    o = t / 'c.stl'; o.unlink(missing_ok=True)
    r = subprocess.run([O, '-o', str(o), str(f)], capture_output=True, text=True)
    if 'ERROR' in r.stderr: sys.exit('OPENSCAD ERROR ' + r.stderr[:300])
    if not o.exists(): return 'clear'
    v = re.findall(r'vertex\s+(\S+)\s+(\S+)\s+(\S+)', o.read_text(errors='replace'))
    if not v: return 'clear'
    c = list(zip(*[tuple(map(float, x)) for x in v]))
    return f'OVERLAP vol {abs(trimesh.load(o).volume):.3f} ' + ' '.join(f'{min(k):.2f}..{max(k):.2f}' for k in c)
T = lambda v, k: f'translate({v}){S[k]}'
for name, a, b in [
    ('CONTROL covers 0.5 low x tray (must overlap)', T('[0,0,-0.5]', 'cov'), S['tray']),
    ('CONTROL covers 10 low x cables (must overlap)', T('[0,0,-10]', 'cov'), S['cables']),
    ('covers x tray', S['cov'], S['tray']), ('covers x jig', S['cov'], S['jig']),
    ('covers x cables', S['cov'], S['cables']), ('covers x devices', S['cov'], S['dev']),
    ('covers x plate', S['cov'], S['plate']), ('covers x shoe L', S['cov'], S['bl']),
    ('cables x tray', S['cables'], S['tray']), ('devices x tray', S['dev'], S['tray']), ('cables x jig', S['cables'], S['jig']), ('tray x plate', S['tray'], S['plate'])]:
    print(name, '=>', go(a, b), flush=True)
