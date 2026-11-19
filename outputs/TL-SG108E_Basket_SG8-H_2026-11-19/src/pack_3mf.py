"""Pack SG8-H as one object with two parts: bracket + label inlay seated in its engraving (for a second colour).
Both turned front face (Y=-4) down onto the bed, same transform, so the inlay stays exactly in the recess.
Usage: python src/pack_3mf.py <release_dir> <out.3mf>"""
import sys, zipfile
from pathlib import Path
import numpy as np, trimesh
d, out = Path(sys.argv[1]), sys.argv[2]
br = trimesh.load(d / 'SG8-H_bracket.stl', process=False)
il = trimesh.load(d / 'SG8-H_inlay.stl', process=False)
def turn(v):  # (x, y, z) -> (x, -z, y): plate front Y=-4 becomes Z=-4, then lift so it sits at Z=0
    return np.c_[v[:, 0], -v[:, 2], v[:, 1]]
vb, vi = turn(br.vertices), turn(il.vertices)
lift = -vb[:, 2].min(); shift = np.array([128, 128 + 22.225, lift])   # centred on a 256 bed
vb += shift; vi += shift
def mesh(i, name, v, f):
    vv, inv = np.unique(np.round(v, 6), axis=0, return_inverse=True); ff = inv.reshape(-1)[f]
    return (f'<object id="{i}" name="{name}" type="model"><mesh><vertices>' + ''.join('<vertex x="%.6f" y="%.6f" z="%.6f"/>' % tuple(p) for p in vv)
            + '</vertices><triangles>' + ''.join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in ff) + '</triangles></mesh></object>')
objs = [mesh(1, 'SG8-H bracket', vb, br.faces), mesh(2, 'SG8-H UPLINK + WLAN label', vi, il.faces),
        '<object id="3" name="SG8-H bracket + labels" type="model"><components><component objectid="1"/><component objectid="2"/></components></object>']
model = ('<?xml version="1.0" encoding="UTF-8"?><model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"><resources>'
         + ''.join(objs) + '</resources><build><item objectid="3"/></build></model>')
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    z.writestr('_rels/.rels', '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    z.writestr('3D/3dmodel.model', model)
for n, v in (('bracket', vb), ('inlay', vi)):
    print(n, ' '.join(f'{a:.2f}..{b:.2f}' for a, b in zip(v.min(0), v.max(0))))
