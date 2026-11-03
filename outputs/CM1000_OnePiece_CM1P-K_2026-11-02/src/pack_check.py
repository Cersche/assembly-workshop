"""CM1P-K: mesh and clearance checks, then the print 3MF (front face on the bed, body + baseline colour parts as parts of one object).
Run from this folder after FreeCAD."""
import re, zipfile, os
from collections import Counter
import trimesh
orig = '../../CM1000_M6_2026-10-28/src/orig/'
def load(p):
    m = trimesh.load(p, process=True, merge_tex=False, merge_norm=False)
    m.merge_vertices(digits_vertex=5)
    return m
def check(name, m):
    e = Counter()
    for f in m.faces.tolist():
        for u, v in ((f[0], f[1]), (f[1], f[2]), (f[2], f[0])):
            e[(min(u, v), max(u, v))] += 1
    bad = [k for k, n in e.items() if n != 2]
    print(name, 'tris', len(m.faces), 'bad edges', len(bad), 'bbox', m.bounds.round(2).tolist(), 'cm3', round(abs(m.volume) / 1000, 1))
    return bad
body = load('parts/body.stl')
bad = check('body', body)
if bad:
    print('first bad at', body.vertices[bad[0][0]].round(2).tolist(), body.vertices[bad[-1][0]].round(2).tolist())
parts = [('Bracket body', body)]
for n, nm in ((4, 'Icon 1'), (8, 'Icon 2'), (7, 'Icon 3'), (6, 'Icon 4'), (5, 'Icon 5')):
    m = load('parts/icon_%d.stl' % n); check(nm, m); parts.append((nm, m))
for n in range(9, 16):
    m = load(orig + 'fp_%d_normal_part.stl' % n); check('Logo %d' % (n - 8), m); parts.append(('Logo %d' % (n - 8), m))

# modem envelope, Brian's: 212 x 131 x 44.4, strip 3, wedge 15, front slope 25; front at Y 4.1. Corners left square, which is the cautious side
MID, TIP, FL, SL, YF = 44.45 / 2, 127 - 106.0, 1.5, 15 / 20.7, 4.1
LEAN = 0.52
def modem_half(y): return min(22.2, 1.5 + 20.7 / 25 * (y - YF)) if YF + 0.01 < y < YF + 131 else -1
def inside(x, y, z, relaxed):
    # relaxed: rails as they should print (drawn lean gone); otherwise as drawn, where the tips overlap the modem on purpose
    h = abs(z - MID)
    d = LEAN * y / 137.62 if relaxed else 0
    for xx in (x, 254 - x):
        if xx < 127 and xx - d < TIP + SL * max(0, h - FL): return False
    return h < modem_half(y)
hits, drawn, first, n = 0, 0, 999, 0
for name, m in parts:
    for t in m.vertices[m.faces].tolist():
        a, b, c = t
        for s, u in ((.33, .33), (1, 0), (0, 1), (0, 0), (.5, .5), (.5, 0), (0, .5)):
            p = [a[i] + s * (b[i] - a[i]) + u * (c[i] - a[i]) for i in range(3)]
            n += 1
            hits += inside(*p, True)
            if inside(*p, False):
                drawn += 1; first = min(first, p[1])
print('points checked', n, 'inside the modem envelope, rails relaxed', hits, '; as drawn', drawn, 'starting at Y', round(first, 1))

res, comp, oid = [], [], 0
for name, m in parts:
    oid += 1; idx, vs = {}, []
    def vid(v):
        r = (float(v[0]), 44.45 - float(v[2]), float(v[1]))
        if r not in idx:
            idx[r] = len(vs); vs.append(r)
        return idx[r]
    f = [tuple(vid(v) for v in t) for t in m.vertices[m.faces].tolist()]
    res.append('<object id="%d" name="%s" type="model"><mesh><vertices>' % (oid, name) + ''.join('<vertex x="%.5f" y="%.5f" z="%.5f"/>' % v for v in vs)
               + '</vertices><triangles>' + ''.join('<triangle v1="%d" v2="%d" v3="%d"/>' % t for t in f) + '</triangles></mesh></object>')
    comp.append(oid)
oid += 1
res.append('<object id="%d" name="CM1P-K CM1000 one-piece bracket" type="model"><components>' % oid + ''.join('<component objectid="%d"/>' % c for c in comp) + '</components></object>')
model = ('<?xml version="1.0" encoding="UTF-8"?><model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
         '<metadata name="Title">CM1000 one-piece bracket (CM1P-K)</metadata><metadata name="Designer">Remix of noyoustupid / Jsmaz3 (CC BY-NC-SA), V from CM1000_1U_Mount (source not recorded). In-house only</metadata><resources>'
         + ''.join(res) + '</resources><build><item objectid="%d"/></build></model>' % oid)
with zipfile.ZipFile('../CM1P-K_CM1000_one_piece_bracket.3mf', 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    z.writestr('_rels/.rels', '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    z.writestr('3D/3dmodel.model', model)
t = zipfile.ZipFile('../CM1P-K_CM1000_one_piece_bracket.3mf').read('3D/3dmodel.model').decode()
print('3MF tags vertex', len(re.findall('<vertex ', t)), 'triangle', len(re.findall('<triangle ', t)), 'objects', len(re.findall('<object ', t)))
body.export('../CM1P-K_body_only.stl')
