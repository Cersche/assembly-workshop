"""Pack the SG8-PB-A brackets into one 3MF: separate named objects, assembly orientation (print standing), each dropped to Z=0."""
import sys, zipfile
names = {'SG8-PB-A_left.stl': 'SG8-PB-A left post bracket', 'SG8-PB-A_right.stl': 'SG8-PB-A right post bracket'}
*ins, out = sys.argv[1:]
objs, items = [], []
for i, p in enumerate(ins, 1):
    V = [tuple(map(float, l.split()[1:])) for l in open(p, encoding='utf-8') if l.strip().startswith('vertex')]
    z0 = min(v[2] for v in V); idx, verts, tris = {}, [], []
    for k in range(0, len(V), 3):
        t = []
        for v in V[k:k+3]:
            v = (v[0], v[1], v[2]-z0)
            if v not in idx: idx[v] = len(verts); verts.append(v)
            t.append(idx[v])
        tris.append(t)
    name = names.get(p.replace(chr(92), '/').split('/')[-1], p)
    objs.append(f'<object id="{i}" name="{name}" type="model"><mesh><vertices>' + ''.join('<vertex x="%.5f" y="%.5f" z="%.5f"/>' % v for v in verts)
                + '</vertices><triangles>' + ''.join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in tris) + '</triangles></mesh></object>')
    items.append(f'<item objectid="{i}"/>')
model = ('<?xml version="1.0" encoding="UTF-8"?><model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"><resources>'
         + ''.join(objs) + '</resources><build>' + ''.join(items) + '</build></model>')
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    z.writestr('_rels/.rels', '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    z.writestr('3D/3dmodel.model', model)
print(out, len(objs), 'objects')
