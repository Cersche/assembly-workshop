"""Pack OPX-A into one 3MF, print layout: front sleeve plate-down, both channels ear-down behind it. One object per part.
Usage: python pack_3mf.py <out.3mf>"""
import pathlib, subprocess, sys, tempfile, zipfile
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(next(p for p in HERE.parents if (p / 'AGENTS.md').exists()) / 'outputs' / 'Mechanical_Design_App'))
import print_layout as pl
OPENSCAD = r'C:/Program Files/OpenSCAD/openscad.exe'
GAP = 10
tmp = pathlib.Path(tempfile.mkdtemp())

def part(p):
    o = tmp / f'{p}.stl'
    r = subprocess.run([OPENSCAD, '-o', str(o), '-D', f'part="{p}"', str(HERE / 'OPX-A.scad')], capture_output=True, text=True)
    assert r.returncode == 0 and 'ERROR' not in r.stderr, r.stderr
    return pl.facets(o.read_text(encoding='utf-8'))

def place(t, x, y):
    """Corner of the part's footprint at (x, y), underside on the bed."""
    lo, _ = pl.bounds(t)
    return pl.move(t, lambda v: (v[0] - lo[0] + x, v[1] - lo[1] + y, v[2] - lo[2]))

front = place(part('print_front'), 0, 0)
fhi = pl.bounds(front)[1]
left = place(part('print_rear_left'), 40, fhi[1] + GAP)
lhi = pl.bounds(left)[1]
right = place(part('print_rear_right'), lhi[0] + GAP, fhi[1] + GAP)
meshes = [('OPX-A-FRONT sleeve', front), ('OPX-A-L rear channel left', left), ('OPX-A-R rear channel right', right)]

def mesh(i, name, tris):
    idx, verts = {}, []
    def vid(v):
        if v not in idx: idx[v] = len(verts); verts.append(v)
        return idx[v]
    f = [tuple(vid(v) for v in t) for t in tris]
    return (f'<object id="{i}" name="{name}" type="model"><mesh><vertices>' + ''.join('<vertex x="%.6f" y="%.6f" z="%.6f"/>' % v for v in verts)
            + '</vertices><triangles>' + ''.join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in f) + '</triangles></mesh></object>')

model = ('<?xml version="1.0" encoding="UTF-8"?><model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"><resources>'
         + ''.join(mesh(i, n, t) for i, (n, t) in enumerate(meshes, 1)) + '</resources><build>'
         + ''.join(f'<item objectid="{i}"/>' for i in range(1, len(meshes) + 1)) + '</build></model>')
with zipfile.ZipFile(sys.argv[1], 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    z.writestr('_rels/.rels', '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    z.writestr('3D/3dmodel.model', model)
for n, t in meshes:
    lo, hi = pl.bounds(t); print(n, len(t), 'tris', ' '.join(f'{a:.1f}..{b:.1f}' for a, b in zip(lo, hi)))
