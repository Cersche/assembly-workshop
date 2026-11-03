"""Exploration build for the Pi/Hue swap concepts. Writes work/scr5-swap/stl only."""
import concurrent.futures as cf, subprocess
from pathlib import Path
H = Path(__file__).parent; O = H / 'stl'; O.mkdir(exist_ok=True)
EXE = r'C:\Program Files\OpenSCAD\openscad.exe'
def b(a):
    o, p = a; d = O / f'{o}_{p}.stl'
    r = subprocess.run([EXE, '--export-format', 'binstl', '-D', f'opt="{o}"', '-D', f'part="{p}"', '-o', str(d), str(H / 'swap_concept.scad')],
                       capture_output=True, text=True, encoding='utf-8')
    return o, p, r.returncode, [l for l in r.stderr.splitlines() if 'ERROR' in l or 'Simple: no' in l], d.stat().st_size if d.exists() else 0
J = [(o, p) for o in ('S1', 'S2', 'N') for p in ('plate', 'floor', 'deck', 'pi', 'hue', 'fan', 'mount', 'ks', 'ribbon')]
with cf.ThreadPoolExecutor(4) as x:
    for r in x.map(b, J): print(r, flush=True)
