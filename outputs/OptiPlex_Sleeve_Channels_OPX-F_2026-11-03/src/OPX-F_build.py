"""OPX-F: render the two new rails and run the digital checks (OpenSCAD intersections; digital only, fit and strength UNKNOWN).
Checks intersect the source modules, not re-imported STLs. A CGAL error or a control that fails to overlap stops the run,
because OpenSCAD reports "top level object is empty" for both a clear pair and a failed one.
Usage: python OPX-D_build.py <post.stl>   (creator's 4U post, object_190, local only; never copied into this folder)"""
import pathlib, re, subprocess, sys, tempfile
OPENSCAD = r'C:/Program Files/OpenSCAD/openscad.exe'
HERE = pathlib.Path(__file__).resolve().parent; OUT = HERE.parent; SCAD = HERE / 'OPX-F.scad'
PARTS = {'rail_left': 'OPX-F-RL', 'rail_right': 'OPX-F-RR'}

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
    S = {'front': 'front();', 'rear_left': 'rear(-1,"OPX-D-L");', 'rear_right': 'rear(1,"OPX-D-R");', 'pc': 'pc();', 'rail_left': 'rail(-1,"OPX-F-RL");', 'rail_right': 'rail(1,"OPX-F-RR");'}
    for s, n in ((-1, 'L'), (1, 'R')):
        S[f'fpost{n}'] = f'translate([{s}*126.12,17.5,0])scale([{-s},1,1])import("{post}");'
        S[f'rpost{n}'] = f'translate([0,240,0])mirror([0,1,0]){S[f"fpost{n}"]}'
    tmp = pathlib.Path(tempfile.mkdtemp())
    # Controls: these must overlap.
    for a, b in (('translate([0,0,-3])pc();', S['front']), (f'translate([100,0,0]){S["fpostL"]}', S['front'])):
        assert overlap(tmp, a, b), ('control did not overlap', a)
    print('controls overlap as expected')
    # The rear stops must catch the PC: 1.5 mm rearward hits both channels.
    for a, b in (('translate([0,1.5,0])pc();', S['rear_left']), ('translate([0,1.5,0])pc();', S['rear_right'])):
        assert overlap(tmp, a, b), ('rear stop misses the PC', b)
    print('rear stops catch the PC')
    pairs = [('front', 'pc'), ('rear_left', 'pc'), ('rear_right', 'pc'), ('front', 'rear_left'), ('front', 'rear_right')]
    pairs += [('front', f'fpost{n}') for n in 'LR'] + [('rear_left', 'rpostL'), ('rear_right', 'rpostR')]
    # Play once seated: 0.45 forward (foot stop), 0.7 rearward (rear stop): must touch nothing.
    for k in (-0.45, 0.7):
        n = f'pc_play{k}'; S[n] = f'translate([0,{k},0])pc();'
        pairs += [(n, 'front'), (n, 'rear_left'), (n, 'rear_right')]
    # PC riding on its feet (0.5 up), k mm behind seated, sliding forward into the bare sleeve.
    for k in (3, 20, 40):
        S[f'pc{k}'] = f'translate([0,{k},0.5])pc();'
        pairs += [(f'pc{k}', 'front')]
    # Sleeve + PC together, k mm in front of seated, going into the channels.
    for k in (5, 20, 40):
        S[f'pcin{k}'] = f'translate([0,-{k},0])pc();'
        pairs += [(f'pcin{k}', 'rear_left'), (f'pcin{k}', 'rear_right')]
    # Sleeve in from the front, channels in from the rear.
    for k in (20, 60):
        S[f'front_f{k}'] = f'translate([0,-{k},0])front();'; S[f'rl_b{k}'] = f'translate([0,{k},0]){S["rear_left"]}'
        pairs += [(f'front_f{k}', 'fpostL'), (f'front_f{k}', 'fpostR'), (f'rl_b{k}', 'rpostL')]
    # Rails: seated and while the sleeve slides in from the front; rail against its post, plate and the PC.
    pairs += [('front', 'rail_left'), ('front', 'rail_right'), ('rail_left', 'fpostL'), ('rail_right', 'fpostR'), ('rail_left', 'pc'), ('rail_right', 'pc')]
    for k in (5, 20, 40, 60):
        pairs += [(f'front_m{k}', 'rail_left'), (f'front_m{k}', 'rail_right')]; S[f'front_m{k}'] = f'translate([0,-{k},0])front();'
    # The runner must still sit in the rail, with the new play: expected 1.1 down, 1.35 up, 1.1 out on each side.
    for x, z in ((0, -1.0), (0, 1.3), (1.0, 0), (-1.0, 0)):
        for r in ('rail_left', 'rail_right'):
            assert not overlap(tmp, f'translate([{x},0,{z}])front();', S[r]), ('play smaller than designed', x, z, r)
    for x, z, r in ((0, -1.2, 'rail_right'), (0, 1.45, 'rail_right'), (1.2, 0, 'rail_right'), (-1.2, 0, 'rail_left')):
        assert overlap(tmp, f'translate([{x},0,{z}])front();', S[r]), ('runner not captured', x, z, r)
    print('runner captured by the rail, play as designed')
    bad = 0
    for a, b in pairs:
        box = overlap(tmp, S[a], S[b])
        print(f'{a:>10} x {b:<10} {box or "CLEAR"}'); bad += bool(box) and box.startswith('OVERLAP')
    print('FAIL' if bad else 'ALL CLEAR', bad)

if __name__ == '__main__':
    main(sys.argv[1])
