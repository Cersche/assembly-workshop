"""ER6-E: pack the print 3MF (front face on the bed, centred on a 256 bed) and run the digital checks.
Usage: python src/pack_check.py <folder> [reference_faceplate.stl] [source.stl]"""
import re, subprocess, sys, tempfile, zipfile
from pathlib import Path
import numpy as np, trimesh
from trimesh.intersections import mesh_plane
d = Path(sys.argv[1]); stl = d / 'ER6-E_ER605_bracket.stl'; out = d / 'ER6-E_ER605_bracket.3mf'
OPENSCAD = r'C:/Program Files/OpenSCAD/openscad.exe'
m = trimesh.load(str(stl), process=True)
print('watertight', m.is_watertight, 'volume cm3 %.1f' % (m.volume / 1000), 'bounds', np.round(m.bounds, 3).tolist())
def down_area(mesh, up, base):
    n = mesh.face_normals[:, up]; c = mesh.triangles_center[:, up]
    return float(mesh.area_faces[(n < -np.cos(np.radians(45)) - 1e-3) & (c > base + 0.01)].sum())
print('ER6-E faces steeper than 45 deg overhang, off the bed: %.2f mm2' % down_area(m, 1, m.bounds[0, 1]))
if len(sys.argv) > 2:
    r = trimesh.load(sys.argv[2], process=True)
    pa = mesh_plane(m, [0, 1, 0], [0, -2, 0]).reshape(-1, 3); pb = mesh_plane(r, [0, 1, 0], [0, -2, 0]).reshape(-1, 3)
    ka = pa[np.abs(pa[:, 0]) > 110]; kb = pb[np.abs(pb[:, 0]) > 110]
    # every point of the reference outline/slots must lie on ours and the other way round
    def near(x, y):
        return max(np.min(np.hypot(y[:, 0] - v[0], y[:, 2] - v[2])) for v in x)
    print('plate ears against SG8-M6-F faceplate, worst gap mm: %.3f / %.3f' % (near(ka, kb), near(kb, ka)))
    print('reference plate bounds', np.round(r.bounds[:, [0, 2]], 3).tolist())
if len(sys.argv) > 3:
    s = trimesh.load(sys.argv[3], process=True)
    print('Source: volume cm3 %.1f, faces steeper than 45 off the bed %.1f mm2' % (s.volume / 1000, down_area(s, 2, s.bounds[0, 2])))
# Router box against the bracket: nominal 158 x 101 x 25 and the pocket-sized envelope, front flush with the plate front
tmp = Path(tempfile.mkdtemp()); f = tmp / 'c.scad'
Rt = 'difference(){translate([-79,-3.3,9.235])cube([158,101,25.98]);for(s=[-1,1])translate([s*61.75,47.7,0])cylinder(d=8,h=11.3,$fn=64);}'
for name, b in [('router 158x101x25.98 seated, keyholes over bumps', Rt), ('router path above the bumps, from the front', 'translate([-79,-120,11.3])cube([158,218,23.9]);'), ('router path, Y<40, full height', 'translate([-79,-120,9.235])cube([158,160,25.98]);')]:
    f.write_text('intersection(){import("%s");%s}' % (stl.resolve().as_posix(), b), encoding='utf-8')
    rr = subprocess.run([OPENSCAD, '-o', str(tmp / 'c.stl'), str(f)], capture_output=True, text=True)
    print(name, 'CLEAR' if 'empty' in rr.stderr.lower() else 'OVERLAP')
# Print 3MF: rotate about X so the front face (Y=-4) is on the bed
v = m.vertices.copy(); pv = np.c_[v[:, 0] + 128, -v[:, 2] + 128 + 22.225, v[:, 1] + 4]
verts = ''.join('<vertex x="%.6f" y="%.6f" z="%.6f"/>' % tuple(p) for p in pv)
tris = ''.join('<triangle v1="%d" v2="%d" v3="%d"/>' % tuple(t) for t in m.faces)
model = ('<?xml version="1.0" encoding="UTF-8"?><model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"><resources>'
         '<object id="1" name="ER6-E ER605 bracket" type="model"><mesh><vertices>' + verts + '</vertices><triangles>' + tris + '</triangles></mesh></object></resources><build><item objectid="1"/></build></model>')
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    z.writestr('_rels/.rels', '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    z.writestr('3D/3dmodel.model', model)
t = zipfile.ZipFile(out).read('3D/3dmodel.model').decode()
print('3MF tags: vertex %d triangle %d' % (len(re.findall('<vertex ', t)), len(re.findall('<triangle ', t))), 'expected', len(pv), len(m.faces))
print('print bounds', np.round(pv.min(0), 2).tolist(), np.round(pv.max(0), 2).tolist())
