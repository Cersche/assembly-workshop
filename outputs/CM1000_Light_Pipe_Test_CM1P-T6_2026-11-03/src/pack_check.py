"""CM1P-T6: mesh and clearance checks, then the print 3MF, front face on the bed, body and pipes as parts of one object. Run from this folder after FreeCAD."""
import re, zipfile
from collections import Counter
import trimesh
OUT = '../CM1P-T6_light_pipe_test_slice.3mf'
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
types = {1: 'icon only', 2: 'earlier faceplate', 3: 'halfway', 4: 'CM1P-O', 5: 'short flat end'}
parts = [('Slice body', load('parts/body.stl'))]
for tag in 'AB':
    parts += [('%s%d %s' % (tag, h, types[h]), load('parts/pipe_%s%d.stl' % (tag, h))) for h in types]
    parts += [('%s icon detail %d' % (tag, k - 1), load('parts/detail_%s%d.stl' % (tag, k))) for k in (2, 3)]
for n, m in parts: check(n, m)
# modem, Brian's envelope: front at Y 4.1, front slope 25, strip 3
MID, YF = 44.45 / 2, 4.1
def modem_half(y): return min(22.2, 1.5 + 20.7 / 25 * (y - YF)) if YF + 0.01 < y < YF + 131 else -1
n = hit = 0
for name, m in parts:
    for a, b, c in m.vertices[m.faces].tolist():
        for s, u in ((.33, .33), (1, 0), (0, 1), (0, 0), (.5, .5), (.5, 0), (0, .5)):
            p = [a[i] + s * (b[i] - a[i]) + u * (c[i] - a[i]) for i in range(3)]
            n += 1; hit += abs(p[2] - MID) < modem_half(p[1])
print('points checked', n, 'inside the modem', hit)
# Y along each pipe's centre line, the air to the modem's slope, and any body wall behind the pipe end
Z = (26.23 + 34.22) / 2
ysurf = YF + (Z - MID - 1.5) / (20.7 / 25)
body = parts[0][1]
for tag, x0 in (('A', 75.25), ('B', 132.75)):
    for h in types:
        cx = x0 + (h - 1) * 11.5; m = dict(parts)['%s%d %s' % (tag, h, types[h])]
        s = trimesh.intersections.mesh_plane(m, [1, 0, 0], [cx + 0.013, 0, 0])
        ye = max(q[0, 1] + (Z - q[0, 2]) / (q[1, 2] - q[0, 2]) * (q[1, 1] - q[0, 1]) for q in s if (q[0, 2] - Z) * (q[1, 2] - Z) < 0)
        w = sum(1 for q in trimesh.intersections.mesh_plane(body, [1, 0, 0], [cx + 0.013, 0, 0]) if (q[0, 2] - Z) * (q[1, 2] - Z) < 0 and q[:, 1].max() > 1.0)
        print(tag, h, 'X', cx, 'plastic', round(ye, 2), 'air', round(ysurf - ye, 2), 'body walls in the tunnel', w)
res, ids, oid = [], [], 0
for name, m in parts:
    oid += 1; idx, vs = {}, []
    def vid(v):
        r = (float(v[0]) - 63.5, 44.45 - float(v[2]), float(v[1]))
        if r not in idx:
            idx[r] = len(vs); vs.append(r)
        return idx[r]
    f = [tuple(vid(v) for v in t) for t in m.vertices[m.faces].tolist()]
    res.append('<object id="%d" name="%s" type="model"><mesh><vertices>' % (oid, name) + ''.join('<vertex x="%.5f" y="%.5f" z="%.5f"/>' % v for v in vs)
               + '</vertices><triangles>' + ''.join('<triangle v1="%d" v2="%d" v3="%d"/>' % t for t in f) + '</triangles></mesh></object>')
    ids.append(oid)
oid += 1
res.append('<object id="%d" name="CM1P-T6 light pipe test slice" type="model"><components>' % oid + ''.join('<component objectid="%d"/>' % c for c in ids) + '</components></object>')
model = ('<?xml version="1.0" encoding="UTF-8"?><model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
         '<metadata name="Title">CM1000 light pipe test slice (CM1P-T6)</metadata><metadata name="Designer">Remix of noyoustupid / Jsmaz3 (CC BY-NC-SA). In-house only</metadata><resources>'
         + ''.join(res) + '</resources><build><item objectid="%d"/></build></model>' % oid)
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    z.writestr('_rels/.rels', '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    z.writestr('3D/3dmodel.model', model)
t = zipfile.ZipFile(OUT).read('3D/3dmodel.model').decode()
print('3MF tags vertex', len(re.findall('<vertex ', t)), 'triangle', len(re.findall('<triangle ', t)), 'objects', len(re.findall('<object ', t)), 'build items', len(re.findall('<item ', t)))
body.export('../CM1P-T6_body_only.stl')
