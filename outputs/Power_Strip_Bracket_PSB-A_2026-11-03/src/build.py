"""Build PSB-A: python build.py. Renders each part, checks closed meshes, reports sizes."""
import re, subprocess, sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
OPENSCAD = r'C:\Program Files\OpenSCAD\openscad.exe'
PARTS = {'plate': 'PSB-A_plate_with_spools', 'hanger': 'PSB-A_hanger', 'cradle': 'PSB-A_brick_cradle',
         'hoop': 'PSB-A_brick_hoop', 'strip_dummy': 'dummy_strip', 'asm_hangers': 'view_hangers',
         'asm_cradle': 'view_cradle', 'asm_brick': 'dummy_brick', 'asm_hoops': 'view_hoops'}


def check(path):
    vert = re.compile(r'vertex\s+(\S+)\s+(\S+)\s+(\S+)')
    pts = [tuple(m.groups()) for m in vert.finditer(path.read_text(encoding='utf-8'))]
    edges = Counter()
    for i in range(0, len(pts), 3):
        a, b, c = pts[i:i + 3]
        for e in ((a, b), (b, c), (c, a)):
            edges[e] += 1
    bad = sum(1 for (a, b), n in edges.items() if edges[(b, a)] != n)
    xyz = [[float(p[k]) for p in pts] for k in range(3)]
    size = [round(max(v) - min(v), 2) for v in xyz]
    return len(pts) // 3, bad, size


fail = 0
for part, name in PARTS.items():
    stl = OUT / 'stl' / f'{name}.stl'
    stl.parent.mkdir(exist_ok=True)
    r = subprocess.run([OPENSCAD, '-o', str(stl), '--export-format', 'asciistl', '-D', f'part="{part}"', str(HERE / 'psb_a.scad')],
                       capture_output=True, text=True, encoding='utf-8')
    if r.returncode or 'ERROR' in r.stderr or 'WARNING' in r.stderr:
        print(part, r.stderr[-1500:])
        fail = 1
        continue
    tris, bad, size = check(stl)
    print(f'{name}: {tris} triangles, {bad} bad edges, size {size}')
    fail |= bad > 0
sys.exit(fail)
