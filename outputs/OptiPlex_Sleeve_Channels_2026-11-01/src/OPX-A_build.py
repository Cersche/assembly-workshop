"""OPX-A: render the parts and run the digital checks (OpenSCAD intersections; digital only, fit and strength UNKNOWN).
Checks intersect the source modules, not re-imported STLs. A CGAL error or a control that fails to overlap stops the run,
because OpenSCAD reports "top level object is empty" for both a clear pair and a failed one.
Usage: python OPX-A_build.py <post.stl>   (creator's 4U post, object_190, local only; never copied into this folder)"""
import pathlib, re, subprocess, sys, tempfile
OPENSCAD = r'C:/Program Files/OpenSCAD/openscad.exe'
HERE = pathlib.Path(__file__).resolve().parent; OUT = HERE.parent; SCAD = HERE / 'OPX-A.scad'
PARTS = {'front': 'OPX-A-FRONT', 'rear_left': 'OPX-A-L', 'rear_right': 'OPX-A-R', 'pc': 'PC_dummy'}

def render(part, out):
    r = subprocess.run([OPENSCAD, '-o', str(out), '-D', f'part="{part}"', str(SCAD)], capture_output=True, text=True)
    print(part, r.returncode, [l for l in r.stderr.splitlines() if 'WARNING' in l or 'ERROR' in l][:4])

def overlap(tmp, a, b):
    """Returns the overlap's bounding box, or None if the pair is clear. Raises on any OpenSCAD error."""
    f = tmp / 'c.scad'; o = tmp / 'c.stl'; o.unlink(missing_ok=True)
    f.write_text(f'use <{SCAD.as_posix()}>\n$fn=48;\nintersection(){{{a}{b}}}', encoding='utf-8')
    r = subprocess.run([OPENSCAD, '-o', str(o), str(f)], capture_output=True, text=True)
    if 'ERROR' in r.stderr: raise RuntimeError(r.stderr)
    if 'top level object is empty' in r.stderr: return None
    v = [tuple(map(float, m)) for m in re.findall(r'vertex\s+(\S+)\s+(\S+)\s+(\S+)', o.read_text(errors='replace'))]
    box = ' '.join(f'{min(c):.2f}..{max(c):.2f}' for c in zip(*v))
    return ('TOUCH ' if any(max(c) - min(c) < 0.001 for c in zip(*v)) else 'OVERLAP ') + box

def main(post):
    assert pathlib.Path(post).is_file(), post
    for part, name in PARTS.items(): render(part, OUT / f'{name}.stl')
    post = pathlib.Path(post).resolve().as_posix()
    S = {'front': 'front();', 'rear_left': 'rear(-1,"OPX-A-L");', 'rear_right': 'rear(1,"OPX-A-R");', 'pc': 'pc();'}
    for s, n in ((-1, 'L'), (1, 'R')):
        S[f'fpost{n}'] = f'translate([{s}*126.12,17.5,0])scale([{-s},1,1])import("{post}");'
        S[f'rpost{n}'] = f'translate([0,240,0])mirror([0,1,0]){S[f"fpost{n}"]}'
    tmp = pathlib.Path(tempfile.mkdtemp())
    # Controls: these must overlap.
    for a, b in (('translate([0,0,-3])pc();', S['front']), (f'translate([100,0,0]){S["fpostL"]}', S['front'])):
        assert overlap(tmp, a, b), ('control did not overlap', a)
    print('controls overlap as expected')
    pairs = [('front', 'pc'), ('rear_left', 'pc'), ('rear_right', 'pc'), ('front', 'rear_left'), ('front', 'rear_right')]
    pairs += [('front', f'fpost{n}') for n in 'LR'] + [('rear_left', 'rpostL'), ('rear_right', 'rpostR')]
    # PC riding on its feet (0.5 up), k mm behind seated, sliding forward into the sleeve and the channels.
    for k in (3, 20, 60, 100, 170):
        S[f'pc{k}'] = f'translate([0,{k},0.5])pc();'
        pairs += [(f'pc{k}', 'front'), (f'pc{k}', 'rear_left'), (f'pc{k}', 'rear_right')]
    # Sleeve in from the front, channels in from the rear.
    for k in (20, 60):
        S[f'front_f{k}'] = f'translate([0,-{k},0])front();'; S[f'rl_b{k}'] = f'translate([0,{k},0]){S["rear_left"]}'
        pairs += [(f'front_f{k}', 'fpostL'), (f'front_f{k}', 'fpostR'), (f'rl_b{k}', 'rpostL')]
    bad = 0
    for a, b in pairs:
        box = overlap(tmp, S[a], S[b])
        print(f'{a:>10} x {b:<10} {box or "CLEAR"}'); bad += bool(box) and box.startswith('OVERLAP')
    print('FAIL' if bad else 'ALL CLEAR', bad)

if __name__ == '__main__':
    main(sys.argv[1])
