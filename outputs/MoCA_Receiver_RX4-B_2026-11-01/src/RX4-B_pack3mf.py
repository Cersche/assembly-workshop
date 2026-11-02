"""RX4-B packer (adapted from SCR5-H_pack3mf.py): one 3MF, every printed part its own object, flat on the bed,
side by side. Parts are only moved/rotated. Python 3.10 stdlib."""
import struct, zipfile
from pathlib import Path
HERE = Path(__file__).resolve().parent.parent
def read(p):
    d = p.read_bytes(); n = struct.unpack_from('<I', d, 80)[0]; V = {}; T = []
    for i in range(n):
        c = struct.unpack_from('<9f', d, 96 + 50 * i)
        T.append([V.setdefault(c[k:k + 3], len(V)) for k in (0, 3, 6)])
    return list(V), T
ROT = {'upright': lambda x, y, z: (x, y, z),
       'flip': lambda x, y, z: (x, -y, -z)}   # lid: top face on the bed, lip and ribs up
PARTS = [("RX4-B body", "RX4-B_body.stl", "upright"), ("RX4-B base", "RX4-B_base.stl", "upright"),
         ("RX4-B lid", "RX4-B_lid.stl", "flip"), ("RX4-B shelf", "RX4-B_shelf.stl", "upright"),
         ("RX4-B cradle", "RX4-B_cradle.stl", "upright")] + \
        [(f"RX4-B washer {i}", "RX4-B_washer.stl", "upright") for i in (1, 2, 3, 4)]
objs = []; xcur = 0
for name, f, rot in PARTS:
    V, T = read(HERE / f)
    V = [ROT[rot](*v) for v in V]
    mn = [min(v[k] for v in V) for k in range(3)]; mx = max(v[0] for v in V)
    dx = xcur - mn[0]; V = [(v[0] + dx, v[1] - mn[1], v[2] - mn[2]) for v in V]; xcur += mx - mn[0] + 12
    objs.append((name, V, T))
out = ['<?xml version="1.0" encoding="UTF-8"?>', '<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">', '<resources>']
for i, (name, V, T) in enumerate(objs, 1):
    out.append(f'<object id="{i}" name="{name}" type="model"><mesh><vertices>')
    out += [f'<vertex x="{x:.6f}" y="{y:.6f}" z="{z:.6f}"/>' for x, y, z in V]
    out.append('</vertices><triangles>')
    out += [f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in T]
    out.append('</triangles></mesh></object>')
out.append('</resources><build>' + ''.join(f'<item objectid="{i}"/>' for i in range(1, len(objs) + 1)) + '</build></model>')
dst = HERE / 'RX4-B_moca_receiver_set.3mf'
with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    z.writestr('_rels/.rels', '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    z.writestr('3D/3dmodel.model', '\n'.join(out))
m = zipfile.ZipFile(dst).read('3D/3dmodel.model').decode()
print(dst.name, 'vertex tags', m.count('<vertex '), 'triangle tags', m.count('<triangle '), 'ns0' in m and 'HAS ns0' or 'no ns0',
      [(n, len(V), len(T)) for n, V, T in objs])
