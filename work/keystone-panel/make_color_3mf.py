"""Two-colour 3MF for KSP-B: one object, two parts (panel body + label inlay), face down, ready for
per-part filament in Bambu Studio / Orca / PrusaSlicer. Geometry is the released STLs, unchanged;
only rotated (front face to the bed) and moved onto the plate. Same 3MF component style as print_layout.py.

  python work/keystone-panel/make_color_3mf.py <panel.stl> <labels.stl> <out.3mf> [name]
"""
import sys
import zipfile

import numpy as np
import trimesh

panel_p, labels_p, out_p = sys.argv[1:4]
name = sys.argv[4] if len(sys.argv) > 4 else "KSP-B keystone panel"

meshes = [("panel (base colour)", trimesh.load(panel_p, force="mesh")),
          ("labels (second colour)", trimesh.load(labels_p, force="mesh"))]
# rotate +90 about X: Y -> Z, so the front face (Y = -4) is the lowest face
rot = trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0])
for _, m in meshes:
    m.apply_transform(rot)
lo = np.min([m.bounds[0] for _, m in meshes], axis=0)
hi = np.max([m.bounds[1] for _, m in meshes], axis=0)
shift = np.array([128.0, 128.0, 0.0]) - np.array([(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, lo[2]])
for _, m in meshes:
    m.apply_translation(shift)

res = []
for i, (label, m) in enumerate(meshes, start=1):
    v = "".join(f'<vertex x="{x:.5f}" y="{y:.5f}" z="{z:.5f}"/>' for x, y, z in m.vertices)
    t = "".join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in m.faces)
    res.append(f'<object id="{i}" name="{label}" type="model"><mesh><vertices>{v}</vertices>'
               f'<triangles>{t}</triangles></mesh></object>')
res.append(f'<object id="3" name="{name}" type="model"><components>'
           '<component objectid="1"/><component objectid="2"/></components></object>')
model = ('<?xml version="1.0" encoding="UTF-8"?><model unit="millimeter" xml:lang="en-US" '
         'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"><resources>'
         + "".join(res) + '</resources><build><item objectid="3"/></build></model>')
with zipfile.ZipFile(out_p, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.'
               'openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/'
               'vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/'
               'vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    z.writestr("_rels/.rels", '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.'
               'openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" '
               'Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    z.writestr("3D/3dmodel.model", model)
for label, m in meshes:
    print(f"{label}: {len(m.faces)} triangles, watertight {m.is_watertight}, z {m.bounds[0][2]:.2f}..{m.bounds[1][2]:.2f}")
print("wrote", out_p)
