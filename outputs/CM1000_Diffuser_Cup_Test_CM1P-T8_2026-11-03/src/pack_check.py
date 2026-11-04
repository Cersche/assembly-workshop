"""CM1P-T8: mesh checks, seated-cup clash slices, modem envelope, then the print 3MF (body and 5 cups as separate objects, front faces on the bed). Run from this folder after FreeCAD."""
import glob, os, re, zipfile
from collections import Counter
import numpy as np, trimesh
from trimesh import intersections
from shapely.geometry import LineString, Polygon
from shapely.ops import polygonize, unary_union
OUT = '../CM1P-T8_diffuser_cup_test.3mf'
def load(p):
    m = trimesh.load(p, process=True); m.merge_vertices(digits_vertex=5); return m
body = load('parts/body.stl')
cups = [(os.path.basename(f)[:-4], load(f)) for f in sorted(glob.glob('parts/cup_*.stl'))]
parts = [('body', body)] + cups
MID, YF = 44.45 / 2, 4.1
def modem_half(y): return np.minimum(22.2, 1.5 + 20.7 / 25 * (y - YF))
for n, m in parts:
    e = Counter(tuple(sorted(x)) for x in m.edges.tolist())
    s, _ = trimesh.sample.sample_surface(m, 60000)
    hit = ((s[:, 1] > YF + .01) & (np.abs(s[:, 2] - MID) < modem_half(s[:, 1]))).sum()
    print(f'{n:22s} tris {len(m.faces):6d} bad edges {sum(1 for v in e.values() if v != 2)} cm3 {abs(m.volume)/1000:6.2f} bbox {m.bounds.round(2).tolist()} in modem {hit}')
def slice_y(m, y):
    l = intersections.mesh_plane(m, plane_normal=[0, 1, 0], plane_origin=[0, y, 0])
    segs = [LineString(np.round(s[:, [0, 2]], 3)) for s in l if np.abs(s[0] - s[1]).sum() > 1e-4]
    polys = sorted(polygonize(unary_union(segs)), key=lambda p: -p.area)
    out = None
    for i, p in enumerate(polys):
        q = Polygon(p.exterior)
        out = q if out is None else out.symmetric_difference(q)
    return out
print('seated cups against the body, overlap area in mm2 per slice:')
for y in (0.2, 0.6, 1.0, 2.5, 3.5, 4.4, 4.6, 4.8, 5.3):
    b = slice_y(body, y)
    print(' Y', y, 'overlap', round(sum(b.intersection(slice_y(m, y)).area for _, m in cups), 4))
res, ids, oid = [], [], 0
for k, (name, m) in enumerate(parts):
    oid += 1; idx, vs = {}, []
    # front face on the bed: (x, y, z) to (x, -z, y). Body behind, cups in a row in front of it
    dx, dy = (-92.0, 44.45 + 14.0) if k == 0 else (-m.bounds[0][0] + 2 + (k - 1) * 13.5, m.bounds[1][2] + 2)
    def vid(v):
        r = (float(v[0]) + dx, dy - float(v[2]), float(v[1]))
        if r not in idx:
            idx[r] = len(vs); vs.append(r)
        return idx[r]
    f = [tuple(vid(v) for v in t) for t in m.vertices[m.faces].tolist()]
    nice = 'CM1P-T8 body' if k == 0 else 'CM1P-T8 cup ' + name.split('_', 2)[2]
    res.append('<object id="%d" name="%s" type="model"><mesh><vertices>' % (oid, nice) + ''.join('<vertex x="%.5f" y="%.5f" z="%.5f"/>' % v for v in vs)
               + '</vertices><triangles>' + ''.join('<triangle v1="%d" v2="%d" v3="%d"/>' % t for t in f) + '</triangles></mesh></object>')
    ids.append(oid)
model = ('<?xml version="1.0" encoding="UTF-8"?><model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
         '<metadata name="Title">CM1000 diffuser cup test (CM1P-T8)</metadata><metadata name="Designer">Remix of noyoustupid / Jsmaz3 (CC BY-NC-SA). In-house only</metadata><resources>'
         + ''.join(res) + '</resources><build>' + ''.join('<item objectid="%d"/>' % c for c in ids) + '</build></model>')
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    z.writestr('_rels/.rels', '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    z.writestr('3D/3dmodel.model', model)
t = zipfile.ZipFile(OUT).read('3D/3dmodel.model').decode()
print('3MF tags vertex', len(re.findall('<vertex ', t)), 'triangle', len(re.findall('<triangle ', t)), 'objects', len(re.findall('<object ', t)), 'build items', len(re.findall('<item ', t)))
