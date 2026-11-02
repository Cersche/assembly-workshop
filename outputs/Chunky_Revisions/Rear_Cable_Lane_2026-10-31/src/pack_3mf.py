"""Pack CBL-A..E into one 3MF in print orientation (plates flat on the bed; D lies on its back with the comb up).
Usage: python pack_3mf.py <stl_dir> <out.3mf>"""
import sys, zipfile
from pathlib import Path
sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / 'AGENTS.md').exists()) / 'outputs' / 'Mechanical_Design_App'))
import print_layout as pl
d, out = Path(sys.argv[1]), sys.argv[2]
GAP = 10
names = [('CBL-A PWR right','CBL-A_R.stl'),('CBL-A DATA left','CBL-A_L.stl'),('CBL-B exit chute PWR right','CBL-B_R.stl'),('CBL-B exit chute DATA left','CBL-B_L.stl'),
         ('CBL-C strip ledge right','CBL-C_R.stl'),('CBL-C strip ledge left','CBL-C_L.stl'),('CBL-E window comb right','CBL-E_R.stl'),('CBL-E window comb left','CBL-E_L.stl'),('CBL-D patch comb panel','CBL-D.stl')]
meshes, x, y, rowh, BED = [], 0.0, 0.0, 0.0, 240.0
for n, f in names:
    t = pl.facets((d / f).read_text(encoding='utf-8'))
    if 'CBL-D' in f: t = pl.move(t, lambda v: (v[0], v[2], -v[1]))   # rotate -90 deg about X: Y=0 back face on the bed, comb up
    else: t = pl.move(t, lambda v: (v[0], -v[2], v[1]))              # rotate +90 deg about X: rack Y (rearward) becomes up
    lo, hi = pl.bounds(t)
    if x > 0 and x + hi[0] - lo[0] > BED: x, y, rowh = 0.0, y + rowh + GAP, 0.0
    t = pl.move(t, lambda v, x=x, y=y, lo=lo: (v[0] - lo[0] + x, v[1] - lo[1] + y, v[2] - lo[2]))
    x += hi[0] - lo[0] + GAP; rowh = max(rowh, hi[1] - lo[1])
    meshes.append((n, t))
def mesh(i, name, tris):
    idx, verts = {}, []
    def vid(v):
        if v not in idx: idx[v] = len(verts); verts.append(v)
        return idx[v]
    f = [tuple(vid(v) for v in t) for t in tris]
    return (f'<object id="{i}" name="{name}" type="model"><mesh><vertices>' + ''.join('<vertex x="%.6f" y="%.6f" z="%.6f"/>' % v for v in verts)
            + '</vertices><triangles>' + ''.join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in f) + '</triangles></mesh></object>')
objs = [mesh(i, n, t) for i, (n, t) in enumerate(meshes, 1)]
model = ('<?xml version="1.0" encoding="UTF-8"?><model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"><resources>'
         + ''.join(objs) + '</resources><build>' + ''.join(f'<item objectid="{i}"/>' for i in range(1, len(meshes) + 1)) + '</build></model>')
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    z.writestr('_rels/.rels', '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    z.writestr('3D/3dmodel.model', model)
for n, t in meshes:
    lo, hi = pl.bounds(t); print(n, len(t), 'tris', ' '.join(f'{a:.1f}..{b:.1f}' for a, b in zip(lo, hi)))
