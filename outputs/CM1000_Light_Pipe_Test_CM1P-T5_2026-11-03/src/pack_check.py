"""CM1P-T5A/T5B: mesh and clearance checks, then one 3MF with both slices side by side, front faces on the bed. Run from this folder after FreeCAD."""
import re, zipfile
from collections import Counter
import numpy as np, trimesh
orig = '../../CM1000_M6_2026-10-28/src/orig/'
OUT = '../CM1P-T5_light_pipe_test_slices.3mf'
def load(p):
    m = trimesh.load(p, process=True, merge_tex=False, merge_norm=False)
    m.merge_vertices(digits_vertex=5)
    return m
def check(name, m):
    e = Counter()
    for f in m.faces.tolist():
        for u, v in ((f[0], f[1]), (f[1], f[2]), (f[2], f[0])):
            e[(min(u, v), max(u, v))] += 1
    bad = sum(1 for n in e.values() if n != 2)
    print(name, 'tris', len(m.faces), 'bad edges', bad, 'bbox', m.bounds.round(2).tolist(), 'cm3', round(abs(m.volume) / 1000, 2))
names = {1: 'Pipe 1 icon only', 2: 'Pipe 2 earlier faceplate', 3: 'Pipe 3 halfway', 4: 'Pipe 4 CM1P-O', 5: 'Pipe 5 short flat end'}
common = [('Icon detail 1', load(orig + 'fp_2_normal_part.stl')), ('Icon detail 2', load(orig + 'fp_3_normal_part.stl'))] + [(names[h], load('parts/pipe_hole_%d.stl' % h)) for h in names]
for n, m in common: check(n, m)
# modem, Brian's envelope: front at Y 4.1, front slope 25, strip 3
MID, YF = 44.45 / 2, 4.1
def modem_half(y): return min(22.2, 1.5 + 20.7 / 25 * (y - YF)) if YF + 0.01 < y < YF + 131 else -1
def hits(m):
    n = h = 0
    for a, b, c in m.vertices[m.faces].tolist():
        for s, u in ((.33, .33), (1, 0), (0, 1), (0, 0), (.5, .5), (.5, 0), (0, .5)):
            p = [a[i] + s * (b[i] - a[i]) + u * (c[i] - a[i]) for i in range(3)]
            n += 1; h += abs(p[2] - MID) < modem_half(p[1])
    return h, n
for n, m in common: print(n, 'points inside the modem', *hits(m))
# Y along each pipe's centre line, and the air to the modem's slope at that height
Z = (26.23 + 34.22) / 2
ysurf = YF + (Z - MID - 1.5) / (20.7 / 25)
for h, cx in zip(range(1, 6), (104.0, 115.5, 127.0, 138.5, 150.0)):
    m = dict(common)[names[h]]
    s = trimesh.intersections.mesh_plane(m, [1, 0, 0], [cx + 0.013, 0, 0])
    ye = max(q[0, 1] + (Z - q[0, 2]) / (q[1, 2] - q[0, 2]) * (q[1, 1] - q[0, 1]) for q in s if (q[0, 2] - Z) * (q[1, 2] - Z) < 0)
    print('hole', h, 'X', cx, 'plastic', round(ye, 2), 'air to the slope', round(ysurf - ye, 2), 'pipe rear', round(m.bounds[1, 1], 2))
res, comp, oid = [], [], 0
for tag, off in (('A', 0.0), ('B', 80.0)):
    body = load('parts/body_%s.stl' % tag)
    check('T5' + tag + ' body', body); print('T5' + tag, 'body points inside the modem', *hits(body))
    body.export('../CM1P-T5%s_body_only.stl' % tag)
    ids = []
    for name, m in [('Slice body', body)] + common:
        oid += 1; idx, vs = {}, []
        def vid(v):
            r = (float(v[0]) - 92 + off, 44.45 - float(v[2]), float(v[1]))
            if r not in idx:
                idx[r] = len(vs); vs.append(r)
            return idx[r]
        f = [tuple(vid(v) for v in t) for t in m.vertices[m.faces].tolist()]
        res.append('<object id="%d" name="%s" type="model"><mesh><vertices>' % (oid, name) + ''.join('<vertex x="%.5f" y="%.5f" z="%.5f"/>' % v for v in vs)
                   + '</vertices><triangles>' + ''.join('<triangle v1="%d" v2="%d" v3="%d"/>' % t for t in f) + '</triangles></mesh></object>')
        ids.append(oid)
    oid += 1
    res.append('<object id="%d" name="CM1P-T5%s light pipe test slice" type="model"><components>' % (oid, tag) + ''.join('<component objectid="%d"/>' % c for c in ids) + '</components></object>')
    comp.append(oid)
model = ('<?xml version="1.0" encoding="UTF-8"?><model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
         '<metadata name="Title">CM1000 light pipe test slices (CM1P-T5A, T5B)</metadata><metadata name="Designer">Remix of noyoustupid / Jsmaz3 (CC BY-NC-SA). In-house only</metadata><resources>'
         + ''.join(res) + '</resources><build>' + ''.join('<item objectid="%d"/>' % c for c in comp) + '</build></model>')
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    z.writestr('_rels/.rels', '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    z.writestr('3D/3dmodel.model', model)
t = zipfile.ZipFile(OUT).read('3D/3dmodel.model').decode()
print('3MF tags vertex', len(re.findall('<vertex ', t)), 'triangle', len(re.findall('<triangle ', t)), 'objects', len(re.findall('<object ', t)), 'build items', len(re.findall('<item ', t)))
