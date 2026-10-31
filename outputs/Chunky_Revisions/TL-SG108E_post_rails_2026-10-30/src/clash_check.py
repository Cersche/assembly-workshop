"""SG8-M6-F clash checks: OpenSCAD intersection of every mating pair (digital only).
Usage: python clash_check.py <stl_dir> <post.stl> [post_z]  (creator's post mesh, local only; Brian's rack: 4U post, object_190,
post_z 0 puts one of its middle U's in the slot; 1U post object_168 uses post_z 22.225). Placement translate([s*126.12,17.5,post_z]) scale([-s,1,1]). Switch = 158 x 100 x 25 box."""
import pathlib, subprocess, sys, tempfile, re
OPENSCAD = r'C:/Program Files/OpenSCAD/openscad.exe'
d = pathlib.Path(sys.argv[1]).resolve(); post = pathlib.Path(sys.argv[2]).resolve().as_posix(); pz = sys.argv[3] if len(sys.argv) > 3 else '0'
P = {k: f'import("{(d / f"SG8-M6-F_{k}.stl").as_posix()}");' for k in ['faceplate', 'tray', 'post-rail_left', 'post-rail_right']}
P['post_left'] = f'translate([-126.12,17.5,{pz}])scale([1,1,1])import("{post}");'
P['post_right'] = f'translate([126.12,17.5,{pz}])scale([-1,1,1])import("{post}");'
P['switch'] = 'translate([-94,-2.7,6.9])cube([158,100,25]);'   # resting 0.1 low on the ledges (worst case)
pairs = [('tray', 'faceplate'), ('tray', 'post-rail_left'), ('tray', 'post-rail_right'), ('faceplate', 'post-rail_left'),
         ('faceplate', 'post-rail_right'), ('post-rail_left', 'post_left'), ('post-rail_right', 'post_right'), ('tray', 'post_left'),
         ('tray', 'post_right'), ('faceplate', 'post_left'), ('faceplate', 'post_right'), ('switch', 'faceplate'),
         ('switch', 'post-rail_left'), ('switch', 'post-rail_right')]
# Sliding the tray in from the front: tray moved forward by k mm must clear both cheeks and posts at every step.
for k in [5, 15, 30, 45, 60, 75, 90]:
    P[f'tray_fwd{k}'] = f'translate([0,-{k},0]){P["tray"]}'
    pairs += [(f'tray_fwd{k}', 'post-rail_left'), (f'tray_fwd{k}', 'post-rail_right'), (f'tray_fwd{k}', 'post_left'), (f'tray_fwd{k}', 'post_right')]
tmp = pathlib.Path(tempfile.mkdtemp())
bad = 0
for a, b in pairs:
    f = tmp / 'c.scad'; f.write_text(f'intersection(){{{P[a]}{P[b]}}}', encoding='utf-8')
    r = subprocess.run([OPENSCAD, '-o', str(tmp / 'c.stl'), str(f)], capture_output=True, text=True)
    empty = 'empty' in r.stderr.lower()
    vol = ''
    if not empty and (tmp / 'c.stl').exists():
        t = (tmp / 'c.stl').read_text(errors='replace')
        v = [tuple(map(float, m)) for m in re.findall(r'vertex\s+(\S+)\s+(\S+)\s+(\S+)', t)]
        if v: vol = ' bbox ' + ' '.join(f'{min(c):.2f}..{max(c):.2f}' for c in zip(*v))
    print(f'{a:>14} x {b:<12} {"CLEAR" if empty else "OVERLAP" + vol}')
    bad += not empty
    (tmp / 'c.stl').unlink(missing_ok=True)
print('FAIL' if bad else 'ALL CLEAR', bad)
