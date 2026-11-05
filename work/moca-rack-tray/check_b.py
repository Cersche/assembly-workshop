"""MRT-B digital checks: build parts, mesh closure, overhangs, clash pairs. Usage: python check_b.py <post4u.stl>
Creator's 4U post (object_190) stays local, never copied here. OpenSCAD reports "empty" for a failed import too, so controls must overlap."""
import subprocess, tempfile, pathlib, sys
import numpy as np, trimesh
O = r'C:/Program Files/OpenSCAD/openscad.exe'
out = pathlib.Path('stl').resolve(); out.mkdir(exist_ok=True)
post = pathlib.Path(sys.argv[1]).resolve().as_posix()
parts = ['tray', 'brace_left', 'brace_right', 'screenbeam', 'splitter', 'cables']
for p in parts:
    r = subprocess.run([O, '-o', str(out / f'MRT-B_{p}.stl'), '--export-format', 'binstl', '-D', f'part="{p}"', 'MRT-B.scad'], capture_output=True, text=True)
    bad = [l for l in r.stderr.splitlines() if 'ERROR' in l or 'WARNING' in l or 'not closed' in l]
    m = trimesh.load(out / f'MRT-B_{p}.stl')
    print(p, 'ok' if r.returncode == 0 else 'FAIL', bad[:4], 'watertight', m.is_watertight, 'cm3', round(m.volume / 1000, 1), np.round(m.bounds, 2).tolist())
    if p in ('tray', 'brace_left', 'brace_right'):
        z0 = m.bounds[0][2]; n = m.face_normals; a = m.area_faces; c = m.triangles_center
        over = (n[:, 2] < -np.cos(np.radians(45)) - 0.01) & (c[:, 2] > z0 + 0.05)
        print('  overhang past 45 mm2', round(a[over].sum(), 1), np.round(c[over][np.argsort(-a[over])[:8]], 1).tolist())

