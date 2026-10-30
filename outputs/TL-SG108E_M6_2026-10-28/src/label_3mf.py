import sys, io, zipfile
from pathlib import Path
sys.path.insert(0, r'D:/Projects/assembly-workshop/outputs/Mechanical_Design_App')
import print_layout as pl
rev, inlay, out = sys.argv[1:4]
plate_only = sys.argv[4:] == ['plate']  # SG8-M6-E: faceplate + label only (tray already printed)
tray = Path(rev, 'tray.stl').read_text(encoding='utf-8')
fp = pl.facets(Path(rev, 'faceplate.stl').read_text(encoding='utf-8'))
il = pl.facets(Path(inlay).read_text(encoding='utf-8'))
# Same transform for plate + inlay: lay them out together, then split.
placed = dict(pl.place({'tray': tray, 'faceplate': pl.stl([('faceplate', fp + il)])}))
both = placed['faceplate']
meshes = [('tray', placed['tray']), ('faceplate', both[:len(fp)]), ('UPLINK label', both[len(fp):])]
def mesh(i, name, tris):
    idx, verts = {}, []
    def vid(v):
        if v not in idx: idx[v] = len(verts); verts.append(v)
        return idx[v]
    f = [tuple(vid(v) for v in t) for t in tris]
    return (f'<object id="{i}" name="{name}" type="model"><mesh><vertices>' + ''.join('<vertex x="%.6f" y="%.6f" z="%.6f"/>' % v for v in verts)
            + '</vertices><triangles>' + ''.join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in f) + '</triangles></mesh></object>')
objs = [mesh(i, n, t) for i, (n, t) in enumerate(meshes, 1) if not (plate_only and i == 1)]
objs.append('<object id="4" name="faceplate + UPLINK label" type="model"><components><component objectid="2"/><component objectid="3"/></components></object>')
model = ('<?xml version="1.0" encoding="UTF-8"?><model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"><resources>'
         + ''.join(objs) + '</resources><build>' + ('' if plate_only else '<item objectid="1"/>') + '<item objectid="4"/></build></model>')
src = pl.layout_3mf({'tray': tray})  # reuse the package boilerplate, swap the model
zin = zipfile.ZipFile(io.BytesIO(src)); buf = io.BytesIO()
with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
    for n in zin.namelist():
        z.writestr(n, model if n == '3D/3dmodel.model' else zin.read(n))
Path(out).write_bytes(buf.getvalue())
print('tray', len(meshes[0][1]), 'plate', len(fp), 'label', len(il), pl.bounds(meshes[2][1]))
