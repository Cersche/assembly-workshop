"""Write RW_wall_mount_set.3mf (plain tags, parts side by side, print orientation) from the RW print STLs.
python make_3mf.py <out_dir>"""
import re, sys, zipfile
from pathlib import Path

out = Path(sys.argv[1])
parts = [('RW-WP-A wall rail', 'RW-WP-A_wall_rail.stl'), ('RW-RC-A rack cleat bar', 'RW-RC-A_rack_cleat_bar.stl'),
         ('RW-SO-A standoff right', 'RW-SO-A_bottom_standoff_x2.stl'), ('RW-SO-A standoff left', 'RW-SO-A_bottom_standoff_x2.stl')]
objs, yoff = [], 0.0
for name, f in parts:
    v = [tuple(map(float, m)) for m in re.findall(r'vertex\s+(\S+)\s+(\S+)\s+(\S+)', (out / f).read_text(encoding='utf-8'))]
    mn = [min(p[i] for p in v) for i in range(3)]; mx = [max(p[i] for p in v) for i in range(3)]
    idx, V, T = {}, [], []
    for k in range(0, len(v), 3):
        tri = []
        for p in v[k:k + 3]:
            q = (round(p[0] - mn[0], 5), round(p[1] - mn[1] + yoff, 5), round(p[2] - mn[2], 5))
            if q not in idx: idx[q] = len(V); V.append(q)
            tri.append(idx[q])
        if len(set(tri)) == 3: T.append(tri)
    e = len(T) * 3 // 2
    print(name, 'size', [round(mx[i] - mn[i], 1) for i in range(3)], 'V', len(V), 'T', len(T), 'genus', (2 - (len(V) - e + len(T))) / 2)
    yoff += mx[1] - mn[1] + 10
    objs.append((name, V, T))
x = ['<?xml version="1.0" encoding="UTF-8"?>\n<model unit="millimeter" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">\n<resources>']
for i, (n, V, T) in enumerate(objs, 1):
    x.append(f'<object id="{i}" name="{n}" type="model"><mesh><vertices>')
    x += [f'<vertex x="{a}" y="{b}" z="{c}" />' for a, b, c in V]
    x.append('</vertices><triangles>'); x += [f'<triangle v1="{a}" v2="{b}" v3="{c}" />' for a, b, c in T]; x.append('</triangles></mesh></object>')
x.append('</resources>\n<build>' + ''.join(f'<item objectid="{i}" />' for i in range(1, len(objs) + 1)) + '</build>\n</model>\n')
with zipfile.ZipFile(out / 'RW_wall_mount_set.3mf', 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', '<?xml version="1.0" encoding="UTF-8"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    z.writestr('_rels/.rels', '<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    z.writestr('3D/3dmodel.model', '\n'.join(x))
t = zipfile.ZipFile(out / 'RW_wall_mount_set.3mf').read('3D/3dmodel.model').decode()
print('plain tags: vertex', len(re.findall(r'<vertex ', t)), 'triangle', len(re.findall(r'<triangle ', t)), 'objects', len(re.findall(r'<object ', t)))
