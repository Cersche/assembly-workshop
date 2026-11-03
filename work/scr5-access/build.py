"""Export concept parts to stl/ and run clash pairs. Usage: build.py A B"""
import concurrent.futures as cf, json, subprocess, sys, tempfile
from pathlib import Path
import trimesh
H = Path(__file__).parent; S = H / 'stl'; EXE = r'C:\Program Files\OpenSCAD\openscad.exe'
S.mkdir(exist_ok=True)
PARTS = 'plate frame screen pi pi_screws ribbon fan fan_mount hue deck jacks plugs cables m6_tools m6_heads sd_path usbc pi_plugs pins pi_drivers rail'.split()
PAIRS = [('plate', 'frame'), ('plate', 'pi'), ('plate', 'hue'), ('plate', 'deck'), ('plate', 'pins'), ('frame', 'pi'), ('frame', 'deck'), ('frame', 'hue'), ('frame', 'pi_screws'), ('frame', 'fan_mount'),
         ('screen', 'pi'), ('screen', 'frame'), ('screen', 'deck'), ('pi', 'hue'), ('pi', 'deck'), ('pi', 'fan'), ('pi', 'fan_mount'), ('pi', 'ribbon'), ('pi', 'pins'), ('ribbon', 'hue'), ('ribbon', 'deck'), ('ribbon', 'fan_mount'), ('ribbon', 'frame'),
         ('hue', 'deck'), ('hue', 'fan'), ('hue', 'fan_mount'), ('hue', 'jacks'), ('hue', 'plugs'), ('hue', 'cables'), ('hue', 'usbc'), ('deck', 'jacks'), ('deck', 'plugs'), ('deck', 'cables'), ('deck', 'm6_heads'), ('jacks', 'frame'), ('jacks', 'ribbon'), ('plugs', 'ribbon'),
         ('deck', 'fan_mount'), ('deck', 'usbc'), ('fan_mount', 'pi_plugs'), ('fan', 'pi_plugs'), ('frame', 'usbc'), ('frame', 'pi_plugs'), ('pi_plugs', 'post_r'), ('plate', 'post_l'), ('plate', 'post_r'), ('deck', 'post_l'), ('jacks', 'post_l'), ('plugs', 'post_l'), ('frame', 'post_r'), ('screen', 'post_r'),
         ('m6_tools', 'jacks'), ('m6_tools', 'plugs'), ('m6_tools', 'deck'), ('m6_tools', 'fan_mount'), ('m6_tools', 'hue'), ('pi_drivers', 'fan'), ('pi_drivers', 'fan_mount'), ('pi_drivers', 'frame'), ('pi_drivers', 'hue'), ('sd_path', 'hue'), ('sd_path', 'deck'), ('sd_path', 'ribbon'), ('usbc', 'fan_mount'), ('rail', 'plate'), ('rail', 'post_l'), ('rail', 'jacks'), ('rail', 'plugs'), ('rail', 'deck')]
SRC = (H / 'access_concept.scad').as_posix()
def exp(a):
    o, p = a; f = S / f'{o}_{p}.stl'
    subprocess.run([EXE, '--export-format', 'binstl', '-D', f'opt="{o}"', '-D', f'part="{p}"', '-D', 'rail=true', '-o', str(f), SRC], capture_output=True, text=True)
    return f
def imp(o, n):
    if n == 'post_l': return f'translate([0,4,0])import("{(H.parent / "rack-post-hex/assembled/post_left.stl").as_posix()}");'
    if n == 'post_r': return f'translate([0,4,0])import("{(H.parent / "rack-post-hex/assembled/post_right.stl").as_posix()}");'
    return f'import("{(S / f"{o}_{n}.stl").as_posix()}");'
def run(a):
    o, x, y = a
    with tempfile.TemporaryDirectory() as t:
        s = Path(t) / 'x.scad'; d = Path(t) / 'x.stl'
        s.write_text(f'intersection(){{{imp(o, x)}{imp(o, y)}}}', encoding='utf-8')
        subprocess.run([EXE, '--export-format', 'binstl', '-o', str(d), str(s)], capture_output=True, text=True)
        v = 0.0
        if d.exists() and d.stat().st_size > 84: v = abs(trimesh.load(d).volume)
    return dict(opt=o, a=x, b=y, mm3=round(v, 2))
for o in sys.argv[1:]:
    with cf.ThreadPoolExecutor(6) as x: list(x.map(exp, [(o, p) for p in PARTS]))
    with cf.ThreadPoolExecutor(6) as x: rows = list(x.map(run, [(o, a, b) for a, b in PAIRS]))
    json.dump(rows, open(H / f'checks_{o}.json', 'w', encoding='utf-8'), indent=0)
    print(o, len(rows), 'pairs')
    for r in rows:
        if r['mm3'] > 0: print(' ', r['a'], r['b'], r['mm3'])
