"""CM1P-T4: mesh and clearance checks, then the print 3MF (front face on the bed). Run from this folder after FreeCAD."""
import re, zipfile
from collections import Counter
import trimesh

mesh = trimesh.load('../CM1P-T4_test_slice.stl', process=True, merge_tex=False, merge_norm=False)
mesh.merge_vertices(digits_vertex=5)
tris = mesh.vertices[mesh.faces].tolist()
edges = Counter()
for f in mesh.faces.tolist():
    for u, v in ((f[0], f[1]), (f[1], f[2]), (f[2], f[0])):
        edges[(min(u, v), max(u, v))] += 1
print('tris', len(tris), 'bad edges', sum(1 for n in edges.values() if n != 2), 'bbox', mesh.bounds.round(2).tolist(), 'volume cm3', round(abs(mesh.volume) / 1000, 1))

# modem envelope: 211.69 from T2, Brian's 14 end wedge, 3 tall at the front, 44.4 at 15 back; flat strip 3 measured (Brian); front on the 1.6 walls
MID, TIP, FL, SL, YF = 44.45 / 2, 127 - 211.69 / 2, 1.5, 14 / 20.7, 1.6
def modem_half(y): return min(22.2, 1.5 + 20.7 / 15 * (y - YF)) if y > YF + 0.01 else -1
def inside(x, y, z):
    h = abs(z - MID)
    for xx in (x, 254 - x):
        if xx < 127 and xx < TIP + SL * max(0, h - FL): return False
    return h < modem_half(y)
hits, n = 0, 0
for a, b, c in tris:
    for s, t in ((0.33, 0.33), (1, 0), (0, 1), (0, 0), (.5, .5), (.5, 0), (0, .5)):
        p = [a[i] + s * (b[i] - a[i]) + t * (c[i] - a[i]) for i in range(3)]
        n += 1
        hits += inside(*p)
print('points checked', n, 'inside the modem envelope', hits)

idx, out = {}, []
def vid(v):
    r = (v[0], -v[2] + 44.45, v[1])
    if r not in idx:
        idx[r] = len(out); out.append(r)
    return idx[r]
f = [tuple(vid(v) for v in t) for t in tris]
model = ('<?xml version="1.0" encoding="UTF-8"?><model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
         '<metadata name="Title">CM1000 one-piece test slice (CM1P-T4)</metadata><resources><object id="1" name="CM1P-T4 test slice" type="model"><mesh><vertices>'
         + ''.join('<vertex x="%.5f" y="%.5f" z="%.5f"/>' % v for v in out) + '</vertices><triangles>'
         + ''.join('<triangle v1="%d" v2="%d" v3="%d"/>' % t for t in f)
         + '</triangles></mesh></object></resources><build><item objectid="1"/></build></model>')
with zipfile.ZipFile('../CM1P-T4_test_slice.3mf', 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    z.writestr('_rels/.rels', '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    z.writestr('3D/3dmodel.model', model)
m = zipfile.ZipFile('../CM1P-T4_test_slice.3mf').read('3D/3dmodel.model').decode()
print('3MF tags vertex', len(re.findall('<vertex ', m)), 'triangle', len(re.findall('<triangle ', m)))
