"""Package the print parts into outputs/Final_3MF as one 3MF, one object per part, side by side."""
import re, zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
STL = HERE.parent / 'stl'
OUT = HERE.parents[1] / 'Final_3MF' / 'PSB-A_power_strip_bracket_set.3mf'
PARTS = [('PSB-A_plate_with_spools', 1), ('PSB-A_brick_cradle', 1), ('PSB-A_brick_hoop', 2), ('PSB-A_hanger', 2)]
GAP = 10
VERT = re.compile(r'vertex\s+(\S+)\s+(\S+)\s+(\S+)')


def mesh(name, dx):
    pts = [tuple(map(float, m.groups())) for m in VERT.finditer((STL / f'{name}.stl').read_text(encoding='utf-8'))]
    lo = [min(p[k] for p in pts) for k in range(3)]
    hi = [max(p[k] for p in pts) for k in range(3)]
    verts, index, tris = [], {}, []
    for i in range(0, len(pts), 3):
        tri = []
        for p in pts[i:i + 3]:
            q = (round(p[0] - lo[0] + dx, 5), round(p[1] - lo[1], 5), round(p[2] - lo[2], 5))
            if q not in index:
                index[q] = len(verts)
                verts.append(q)
            tri.append(index[q])
        tris.append(tri)
    return verts, tris, hi[0] - lo[0]


objects, items, dx, oid = [], [], 0.0, 1
for name, qty in PARTS:
    for n in range(qty):
        verts, tris, width = mesh(name, dx)
        label = f'{name}_{n + 1}' if qty > 1 else name
        v = ''.join(f'<vertex x="{x}" y="{y}" z="{z}"/>' for x, y, z in verts)
        t = ''.join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in tris)
        objects.append(f'<object id="{oid}" type="model" name="{label}"><mesh><vertices>{v}</vertices><triangles>{t}</triangles></mesh></object>')
        items.append(f'<item objectid="{oid}"/>')
        dx += width + GAP
        oid += 1

model = ('<?xml version="1.0" encoding="UTF-8"?>\n<model unit="millimeter" xml:lang="en-US" '
         'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
         f'<resources>{"".join(objects)}</resources><build>{"".join(items)}</build></model>')
rels = ('<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
types = ('<?xml version="1.0" encoding="UTF-8"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
         '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
         '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', types)
    z.writestr('_rels/.rels', rels)
    z.writestr('3D/3dmodel.model', model)
print(OUT.name, oid - 1, 'objects,', model.count('<vertex '), 'vertices,', model.count('<triangle '), 'triangles')
