"""Pack the MRT test prints into one 3MF: separate named objects, side by side, flat on the bed. Run from the folder above src/."""
import zipfile, numpy as np, trimesh
parts = [('MRT-T1_channel_forming_jig.stl', 'MRT-T1 channel forming jig'), ('MRT-T2_notch_slice.stl', 'MRT-T2 notch slice')]
objs, items, x = [], [], 0.0
for i, (f, name) in enumerate(parts, 1):
    m = trimesh.load(f)
    m.merge_vertices()
    lo, hi = m.bounds
    v = m.vertices - [lo[0], lo[1], lo[2]] + [x, 0, 0]
    vs = ''.join(f'<vertex x="{a:.5f}" y="{b:.5f}" z="{c:.5f}"/>' for a, b, c in v)
    ts = ''.join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in m.faces)
    objs.append(f'<object id="{i}" type="model" name="{name}"><mesh><vertices>{vs}</vertices><triangles>{ts}</triangles></mesh></object>')
    items.append(f'<item objectid="{i}"/>')
    x += float(hi[0] - lo[0]) + 10
model = ('<?xml version="1.0" encoding="UTF-8"?><model unit="millimeter" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
         f'<resources>{"".join(objs)}</resources><build>{"".join(items)}</build></model>')
with zipfile.ZipFile('MRT-T1_T2_channel_test_prints.3mf', 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    z.writestr('_rels/.rels', '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    z.writestr('3D/3dmodel.model', model)
t = model
print('objects', t.count('<object '), 'vertex', t.count('<vertex '), 'triangle', t.count('<triangle '), 'width', round(x - 10, 1))
