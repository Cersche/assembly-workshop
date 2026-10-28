"""Pack CM6A into one 3MF: faceplate (body + the baseline's colour parts: light pipes, logo, details) front face down,
rails L/R on their outer faces (baseline orientations without the 45 deg bed turn), side by side, 10 mm gaps.
Run from this folder after the STLs exist: python pack.py"""
import io, zipfile, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'Mechanical_Design_App'))
from print_layout import facets, move, bounds
import struct
def rd(p):   # ASCII (OpenSCAD) or binary (FreeCAD) STL
    b = open(p, 'rb').read()
    if b[:5] == b'solid' and b'facet' in b[:400]:
        return facets(b.decode('utf-8'))
    n = struct.unpack('<I', b[80:84])[0]
    return [[struct.unpack('<3f', b[84 + 50 * i + 12 + 12 * j:84 + 50 * i + 24 + 12 * j]) for j in range(3)] for i in range(n)]
colour = [(n, 'orig/fp_%d_normal_part.stl' % n) for n in range(2, 16)]
names = {2: 'Detail 1', 3: 'Detail 2', 4: 'Light pipe 1', 5: 'Light pipe 2', 6: 'Light pipe 3', 7: 'Light pipe 4',
         8: 'Light pipe 5', **{n: 'Logo %d' % (n - 8) for n in range(9, 16)}}
objs = [('CM6A-F faceplate', lambda v: (v[0], -v[2], v[1]),
         [('Faceplate body', rd('../CM6A_faceplate.stl'))] + [(names[n], rd(p)) for n, p in colour]),
        ('CM6A-L rail', lambda v: (v[1], v[2], v[0]), [('Rail L', rd('../CM6A_rail_l.stl'))]),
        ('CM6A-R rail', lambda v: (v[1], -v[2], -v[0]), [('Rail R', rd('../CM6A_rail_r.stl'))])]
placed, y = [], 0.0
for k, (name, rot, parts) in enumerate(objs):
    parts = [(pn, move(t, rot)) for pn, t in parts]
    lo, hi = bounds([t for _, p in parts for t in p])
    if k == 2:   # rail R beside rail L
        dx, dy = placed[1][3] + 10 - lo[0], placed[1][4] - lo[1]
    else:
        dx, dy = -lo[0], y - lo[1]
    parts = [(pn, move(t, lambda v: (v[0] + dx, v[1] + dy, v[2] - lo[2]))) for pn, t in parts]
    placed.append((name, parts, None, hi[0] + dx, lo[1] + dy))
    if k < 2: y = hi[1] + dy + 10
res, items, oid = [], [], 0
for name, parts, *_ in placed:
    comp = []
    for pn, tris in parts:
        oid += 1; idx, vs = {}, []
        def vid(v):
            if v not in idx:
                idx[v] = len(vs); vs.append(v)
            return idx[v]
        f = [tuple(vid(v) for v in t) for t in tris]
        res.append(f'<object id="{oid}" name="{pn}" type="model"><mesh><vertices>' + ''.join('<vertex x="%.5f" y="%.5f" z="%.5f"/>' % v for v in vs)
                   + '</vertices><triangles>' + ''.join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in f) + '</triangles></mesh></object>')
        comp.append(oid)
    oid += 1
    res.append(f'<object id="{oid}" name="{name}" type="model"><components>' + ''.join(f'<component objectid="{c}"/>' for c in comp) + '</components></object>')
    items.append(f'<item objectid="{oid}"/>')
model = ('<?xml version="1.0" encoding="UTF-8"?><model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
         '<metadata name="Title">CM1000 bracket M6 (CM6A)</metadata><metadata name="Designer">Remix of noyoustupid / Jsmaz3 (CC BY-NC-SA)</metadata>'
         '<resources>' + ''.join(res) + '</resources><build>' + ''.join(items) + '</build></model>')
with zipfile.ZipFile('../CM6A_CM1000_M6_bracket_set.3mf', 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    z.writestr('_rels/.rels', '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    z.writestr('3D/3dmodel.model', model)
for name, parts, *_ in placed:
    lo, hi = bounds([t for _, p in parts for t in p]); print(name, [round(a, 1) for a in lo], [round(a, 1) for a in hi])
