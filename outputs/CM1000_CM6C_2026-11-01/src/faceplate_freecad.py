# CM6C faceplate via FreeCAD/OCC: OpenSCAD 2021 CGAL fails on the baseline faceplate's sliver triangles.
# CM6A's build + the end channels recut to the modem's wedge (numbers as in cm1000_cm6c.scad).
# Run from this folder: "C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('faceplate_freecad.py').read())"
import os, Mesh, MeshPart, Part, FreeCAD as App
V = App.Vector
here = os.getcwd()
orig = os.path.join(here, '..', '..', 'CM1000_M6_2026-10-28', 'src', 'orig')
def solid(path, mat=None):
    m = Mesh.Mesh(path)
    if mat: m.transform(mat)
    s = Part.Shape(); s.makeShapeFromMesh(m.Topology, 0.01)
    return Part.makeSolid(Part.makeShell(s.Faces))
joint_x, joint_z = [22.2, 231.8], [5.6, 38.85]
pilot_d, pilot_y = 7.6, (9.0, 16.5)
tip_x, slope, mid, over = 20.0, 12 / 22.25, 44.45 / 2, 23.5
nose_k, nose_add = 1.375, 0.1   # pocket's own nose taper (height 2.75 x Y); +0.1 keeps the cut off its surface
def prism(pts, d):
    return Part.Face(Part.makePolygon(pts + [pts[0]])).extrude(d)
def channel(x_in):   # left-end cut: channel profile (X, Z) along Y, inside the nose taper (Y, Z) along X
    prof = prism([V(tip_x, 0.6, mid), V(tip_x + slope * over, 0.6, mid + over), V(x_in, 0.6, mid + over),
                  V(x_in, 0.6, mid - over), V(tip_x + slope * over, 0.6, mid - over)], V(0, 16, 0))
    y1 = 17.0; h = nose_k * y1 + nose_add
    nose = prism([V(15, 0, mid - nose_add), V(15, y1, mid - h), V(15, y1, mid + h), V(15, 0, mid + nose_add)], V(x_in - 15, 0, 0))
    return prof.common(nose)
# ear fills: as CM6A (0.05 inset: coplanar faces left cracks in the export)
def fit(lo, hi, nlo, nhi):
    k = (nhi - nlo) / (hi - lo); return k, nlo - k * lo
kx, ox = fit(0, 16.9, 0.05, 17.3); ky, oy = fit(0, 3, 0.05, 2.95); kz, oz = fit(0, 44.45, 0.05, 44.40)
fl = solid(os.path.join(orig, 'fp_16_normal_part.stl'), App.Matrix(kx, 0, 0, ox, 0, ky, 0, oy, 0, 0, kz, oz, 0, 0, 0, 1))
kx, ox = fit(237.1, 254, 236.7, 253.95)
fr = solid(os.path.join(orig, 'fp_17_normal_part.stl'), App.Matrix(kx, 0, 0, ox, 0, ky, 0, oy, 0, 0, kz, oz, 0, 0, 0, 1))
body = solid(os.path.join(orig, 'fp_1_normal_part.stl')).fuse([fl, fr])
cuts = [solid(os.path.join(orig, 'fp_%d_negative_part.stl' % n)) for n in (18, 19, 20, 21)]
for x in joint_x:
    for z in joint_z:
        cuts.append(Part.makeCylinder(pilot_d / 2, pilot_y[1] - pilot_y[0], V(x, pilot_y[0], z), V(0, 1, 0)))
left = channel(38.0)
right = left.copy(); right = right.mirror(V(127, 0, 0), V(1, 0, 0))
cuts += [left, right]
cuts.append(solid(os.path.join(here, 'id_F.stl')))
print('body', round(body.Volume, 1), len(body.Solids), 'channel cut', round(left.Volume, 1), round(right.Volume, 1))
out = body.cut(cuts)
print('valid', out.isValid(), 'solids', len(out.Solids), 'volume', round(out.Volume, 1))
m = MeshPart.meshFromShape(Shape=out, LinearDeflection=0.01, AngularDeflection=0.2618, Relative=False)
m.write(os.path.join(here, '..', 'CM6C_faceplate.stl'))
print('facets', m.CountFacets)
