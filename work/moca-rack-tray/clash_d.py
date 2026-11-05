"""MRT-C clash checks on the SOURCE modules (importing the tray STL fails in CGAL and reads as a false clear). Stops on any OpenSCAD error.
Usage: python clash_b.py <post4u.stl>. The post stays local."""
import subprocess, pathlib, sys, tempfile, re
O = r'C:/Program Files/OpenSCAD/openscad.exe'; src = pathlib.Path('MRT-D.scad').resolve().as_posix(); post = pathlib.Path(sys.argv[1]).resolve().as_posix()
S = {'tray': 'tray();', 'bl': 'shoe("MRT-C-L");', 'br': 'mir(1)shoe("MRT-C-R");', 'cables': 'cables();', 'dev': 'union(){screenbeam();splitter();}'}
for n, s in (('L', -1), ('R', 1)):
    fp = f'translate([{s}*126.12,17.5,0])scale([{-s},1,1])import("{post}");'
    S['rp' + n] = f'translate([110,240,0])mirror([0,1,0]){fp}'; S['fp' + n] = f'translate([110,0,0]){fp}'
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
    import trimesh
    return f'OVERLAP vol {abs(trimesh.load(o).volume):.3f} ' + ' '.join(f'{min(k):.2f}..{max(k):.2f}' for k in c)
T = lambda v, k: f'translate({v}){S[k]}'
for name, a, b in [
    ('CONTROL cables 2 left x tray (must overlap)', T('[-2,0,0]', 'cables'), S['tray']),
    ('tray x shoe L', S['tray'], S['bl']), ('tray x shoe R', S['tray'], S['br']), ('tray 16 forward x shoe L', T('[0,-16,0]', 'tray'), S['bl']),
    ('tray x rear post L', S['tray'], S['rpL']), ('cables x tray', S['cables'], S['tray']), ('cables x shoe L', S['cables'], S['bl']), ('cables x shoe R', S['cables'], S['br']),
    ('devices x tray', S['dev'], S['tray'])]:
    print(name, '=>', go(a, b), flush=True)
