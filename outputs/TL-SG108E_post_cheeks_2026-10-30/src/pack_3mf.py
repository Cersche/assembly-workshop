"""Pack SG8-M6-F into one 3MF: tray, left cheek, right cheek, faceplate + UPLINK label (one object, two parts).
Tray and cheeks keep their installed orientation (flat bottoms on the bed); the faceplate lies on its front face.
Usage: python pack_3mf.py <stl_dir> <out.3mf>"""
import sys, zipfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'outputs' / 'Mechanical_Design_App'))
import print_layout as pl
d, out = Path(sys.argv[1]), sys.argv[2]
rd = lambda n: pl.facets((d / f'SG8-M6-F_{n}.stl').read_text(encoding='utf-8'))
GAP = 10
def drop(t, dx=0, dy=0):
    lo, _ = pl.bounds(t); return pl.move(t, lambda v: (v[0] + dx, v[1] + dy, v[2] - lo[2]))
tray = drop(rd('tray'))
tlo, thi = pl.bounds(tray)
fp, il = rd('faceplate'), rd('UPLINK-label-inlay')
both = pl.move(fp + il, lambda v: (v[0], -v[2], v[1]))           # front face (Y=-4) onto the bed
blo, bhi = pl.bounds(both)
both = drop(both, 0, tlo[1] - GAP - bhi[1])
cl, cr = rd('cheek_left'), rd('cheek_right')
cllo, clhi = pl.bounds(cl); crlo, crhi = pl.bounds(cr)
cl = drop(cl, -GAP / 2 - clhi[0], thi[1] + GAP - cllo[1])          # side by side behind the tray
cr = drop(cr, GAP / 2 - crlo[0], thi[1] + GAP - crlo[1])
meshes = [('SG8-M6-F tray', tray), ('SG8-M6-F cheek left', cl), ('SG8-M6-F cheek right', cr),
          ('SG8-M6-F faceplate', both[:len(fp)]), ('SG8-M6-F UPLINK label', both[len(fp):])]
def mesh(i, name, tris):
    idx, verts = {}, []
    def vid(v):
        if v not in idx: idx[v] = len(verts); verts.append(v)
        return idx[v]
    f = [tuple(vid(v) for v in t) for t in tris]
    return (f'<object id="{i}" name="{name}" type="model"><mesh><vertices>' + ''.join('<vertex x="%.6f" y="%.6f" z="%.6f"/>' % v for v in verts)
            + '</vertices><triangles>' + ''.join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in f) + '</triangles></mesh></object>')
objs = [mesh(i, n, t) for i, (n, t) in enumerate(meshes, 1)]
objs.append('<object id="6" name="SG8-M6-F faceplate + UPLINK label" type="model"><components><component objectid="4"/><component objectid="5"/></components></object>')
model = ('<?xml version="1.0" encoding="UTF-8"?><model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"><resources>'
         + ''.join(objs) + '</resources><build><item objectid="1"/><item objectid="2"/><item objectid="3"/><item objectid="6"/></build></model>')
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    z.writestr('_rels/.rels', '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    z.writestr('3D/3dmodel.model', model)
for n, t in meshes:
    lo, hi = pl.bounds(t); print(n, len(t), 'tris', ' '.join(f'{a:.1f}..{b:.1f}' for a, b in zip(lo, hi)))
