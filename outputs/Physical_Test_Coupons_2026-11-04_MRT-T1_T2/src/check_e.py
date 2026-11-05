"""MRT-E digital checks: build parts, mesh closure, overhangs. Then clash pairs on SOURCE modules with controls (importing the tray STL fails in CGAL and reads as a false clear).
Usage: python check_e.py <post4u.stl>. The creator's post stays local."""
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
for p, tag in [('plate', 'MRT-E'), ('tray', 'MRT-E'), ('jig', 'MRT-T1'), ('slice', 'MRT-T2')]:
    f = out / f'{tag}_{p}.stl'
    r = subprocess.run([O, '-o', str(f), '--export-format', 'binstl', '-D', f'part="{p}"', 'MRT-E.scad'], capture_output=True, text=True)
    bad = [l for l in r.stderr.splitlines() if 'ERROR' in l or 'WARNING' in l or 'not closed' in l]
    m = trimesh.load(f)
    print(p, 'ok' if r.returncode == 0 else 'FAIL', bad[:4], 'watertight', m.is_watertight, 'bodies', bodies(m), 'cm3', round(m.volume / 1000, 1), np.round(m.bounds, 2).tolist(), flush=True)
    if p == 'plate': continue
    z0 = m.bounds[0][2]; n = m.face_normals; a = m.area_faces; c = m.triangles_center
    over = (n[:, 2] < -np.cos(np.radians(45)) - 0.01) & (c[:, 2] > z0 + 0.05)
    print('  overhang past 45 mm2', round(a[over].sum(), 1), np.round(c[over][np.argsort(-a[over])[:6]], 1).tolist(), flush=True)
src = pathlib.Path('MRT-E.scad').resolve().as_posix(); post = pathlib.Path(sys.argv[1]).resolve().as_posix()
S = {'tray': 'tray();', 'plate': 'plate();', 'cables': 'cables();', 'dev': 'union(){screenbeam();splitter();}', 'bl': 'shoe("MRT-C-L");'}
for n, s in (('L', -1), ('R', 1)):
    S['fp' + n] = f'translate([110,0,0])translate([{s}*126.12,17.5,0])scale([{-s},1,1])import("{post}");'
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
    ('CONTROL tray 1 forward x plate (must overlap)', T('[0,-1,0]', 'tray'), S['plate']),
    ('CONTROL tray 0.5 low x plate (must overlap: ledge)', T('[0,-0.3,-0.5]', 'tray'), S['plate']),
    ('tray x plate', S['tray'], S['plate']),
    ('tray 0.3 forward (screws tight) x plate', T('[0,-0.3,0]', 'tray'), S['plate']),
    ('tray x front post L', S['tray'], S['fpL']), ('tray x front post R', S['tray'], S['fpR']),
    ('plate x front post L', S['plate'], S['fpL']),
    ('tray x shoe L', S['tray'], S['bl']),
    ('cables x tray', S['cables'], S['tray']), ('cables x plate', S['cables'], S['plate']),
    ('devices x tray', S['dev'], S['tray']), ('devices x plate', S['dev'], S['plate']),
    ('devices x jig (raised 2)', S['dev'], 'translate([0,0,2])jig();'), ('cables x jig (raised 2)', S['cables'], 'translate([0,0,2])jig();')]:
    print(name, '=>', go(a, b), flush=True)
