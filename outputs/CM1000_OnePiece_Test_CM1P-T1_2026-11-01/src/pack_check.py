"""CM1P-T1: mesh and clearance checks, then the print 3MF (front face on the bed). Run from this folder after OpenSCAD."""
import re, zipfile
from collections import Counter

vs = [tuple(float(x) for x in l.split()[1:4]) for l in open('../CM1P-T1_test_slice.stl', encoding='utf-8') if l.strip().startswith('vertex')]
tris = [vs[i:i + 3] for i in range(0, len(vs), 3)]
edges = Counter()
for a, b, c in tris:
    for u, v in ((a, b), (b, c), (c, a)):
        edges[(min(u, v), max(u, v))] += 1
print('tris', len(tris), 'bad edges', sum(1 for n in edges.values() if n != 2))
print('bbox', [(min(v[i] for v in vs), max(v[i] for v in vs)) for i in range(3)])
vol = sum((a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])) / 6 for a, b, c in tris)
print('volume cm3', round(abs(vol) / 1000, 1))

# modem envelope from Brian's numbers: front face at Y=2 (seated)
MID, TIP, SL, YF = 44.45 / 2, 21.0, 14 / 22.2, 2.0
def modem_half(y): return min(22.2, 1.5 + 20.7 / 15 * (y - YF)) if y >= YF else -1
def inside(x, y, z):
    h = abs(z - MID)
    for xx in (x, 254 - x):
        if xx < 127 and xx < TIP + SL * h: return False
    return h < modem_half(y)
worst, n = 99, 0
for a, b, c in tris:
    for s, t in ((0.33, 0.33), (1, 0), (0, 1), (0, 0), (.5, .5), (.5, 0), (0, .5)):
        p = tuple(a[i] + s * (b[i] - a[i]) + t * (c[i] - a[i]) for i in range(3))
        n += 1
        if inside(*p): worst = 0
print('points checked', n, 'inside the modem envelope' if worst == 0 else 'none inside the modem envelope')

idx, out = {}, []
def vid(v):
    r = (v[0], -v[2] + 44.45, v[1])
    if r not in idx:
        idx[r] = len(out); out.append(r)
    return idx[r]
f = [tuple(vid(v) for v in t) for t in tris]
model = ('<?xml version="1.0" encoding="UTF-8"?><model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
         '<metadata name="Title">CM1000 one-piece test slice (CM1P-T1)</metadata><resources><object id="1" name="CM1P-T1 test slice" type="model"><mesh><vertices>'
         + ''.join('<vertex x="%.5f" y="%.5f" z="%.5f"/>' % v for v in out) + '</vertices><triangles>'
         + ''.join('<triangle v1="%d" v2="%d" v3="%d"/>' % t for t in f)
         + '</triangles></mesh></object></resources><build><item objectid="1"/></build></model>')
with zipfile.ZipFile('../CM1P-T1_test_slice.3mf', 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    z.writestr('_rels/.rels', '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    z.writestr('3D/3dmodel.model', model)
m = zipfile.ZipFile('../CM1P-T1_test_slice.3mf').read('3D/3dmodel.model').decode()
print('3MF tags vertex', len(re.findall('<vertex ', m)), 'triangle', len(re.findall('<triangle ', m)))
