"""Print-layout 3MF with the UPLINK inlay as a second part of the faceplate object (pick its filament in the slicer).
The engraving (x=88, z=3.8, 4.5 mm, 0.6 deep) is the same as ../2026-10-22_TL-SG108E, so its inlay STL is reused.
Run after build.py: python label_3mf.py
"""
import io, pathlib, sys, zipfile
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'Mechanical_Design_App'))
import print_layout as pl

N = 'TL-SG108E_1U_hidden-screws_'
read = lambda p: pl.facets(pathlib.Path(p).read_text(encoding='utf-8'))
tray = read(HERE / f'{N}tray.stl')
face = read(HERE / f'{N}faceplate.stl')
label = read(HERE.parent / '2026-10-22_TL-SG108E' / 'TL-SG108E_1U_sleeve_shifted-left_UPLINK-keystone_UPLINK-label-inlay.stl')

rot = lambda v: (v[0], -v[2], v[1])  # same turn as print_layout: front face onto the bed
face_r, label_r = pl.move(face, rot), pl.move(label, rot)
flo, fhi = pl.bounds(face_r)
tlo, thi = pl.bounds(tray)
dy = tlo[1] - pl.GAP - fhi[1]
shift = lambda v: (v[0], v[1] + dy, v[2] - flo[2])
tray = pl.move(tray, lambda v: (v[0], v[1], v[2] - tlo[2]))
face_r, label_r = pl.move(face_r, shift), pl.move(label_r, shift)

def mesh(i, name, tris):
    idx, verts = {}, []
    def vid(v):
        if v not in idx:
            idx[v] = len(verts); verts.append(v)
        return idx[v]
    faces = [tuple(vid(v) for v in t) for t in tris]
    return (f'<object id="{i}" name="{name}" type="model"><mesh><vertices>'
            + ''.join('<vertex x="%.6f" y="%.6f" z="%.6f"/>' % v for v in verts) + '</vertices><triangles>'
            + ''.join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in faces) + '</triangles></mesh></object>')

objs = [mesh(1, 'tray', tray), mesh(2, 'faceplate', face_r), mesh(3, 'UPLINK label', label_r),
        '<object id="4" name="faceplate + UPLINK label" type="model"><components>'
        '<component objectid="2"/><component objectid="3"/></components></object>']
model = ('<?xml version="1.0" encoding="UTF-8"?><model unit="millimeter" xml:lang="en-US" '
         'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"><resources>' + ''.join(objs)
         + '</resources><build><item objectid="1"/><item objectid="4"/></build></model>')
# reuse print_layout's package files, swapping in this model
src = zipfile.ZipFile(io.BytesIO(pl.layout_3mf({'tray': (HERE / f'{N}tray.stl').read_text(encoding='utf-8')})))
out = HERE / f'{N}2-parts-print-layout.3mf'
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for n in src.namelist():
        z.writestr(n, model if n == '3D/3dmodel.model' else src.read(n))
print(out.name, 'label bounds', [[round(c, 2) for c in b] for b in pl.bounds(label_r)])
