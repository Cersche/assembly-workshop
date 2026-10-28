# CM6A faceplate via FreeCAD/OCC: OpenSCAD 2021 CGAL fails on the baseline faceplate's sliver triangles
# (assertion at the x231 z35.45 pilot; its exports also came out open). Same cuts as cm1000_m6.scad faceplate().
# Run from this folder: "C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('faceplate_freecad.py').read())"
import os, Mesh, MeshPart, Part, FreeCAD as App
V = App.Vector
here = os.getcwd()
def solid(name, mat=None):
    m = Mesh.Mesh(os.path.join(here, 'orig', name))
    if mat: m.transform(mat)
    s = Part.Shape(); s.makeShapeFromMesh(m.Topology, 0.01)
    return Part.makeSolid(Part.makeShell(s.Faces))
joint_x, joint_z = [22.6, 231.4], [8.6, 35.85]
pilot_d, pilot_y = 7.6, (9.0, 16.5)
# ear fills: X 0..16.9 -> 0.05..17.3 (0.4 into the plate), Y 0..3 -> 0.05..2.95, Z 0..44.45 -> 0.05..44.40.
# Faces coplanar with the plate left cracks/non-manifold edges in the export; a 0.05 inset is below one layer.
def fit(lo, hi, nlo, nhi):
    k = (nhi - nlo) / (hi - lo); return k, nlo - k * lo
kx, ox = fit(0, 16.9, 0.05, 17.3); ky, oy = fit(0, 3, 0.05, 2.95); kz, oz = fit(0, 44.45, 0.05, 44.40)
fl = solid('fp_16_normal_part.stl', App.Matrix(kx, 0, 0, ox, 0, ky, 0, oy, 0, 0, kz, oz, 0, 0, 0, 1))
kx, ox = fit(237.1, 254, 236.7, 253.95)
fr = solid('fp_17_normal_part.stl', App.Matrix(kx, 0, 0, ox, 0, ky, 0, oy, 0, 0, kz, oz, 0, 0, 0, 1))
body = solid('fp_1_normal_part.stl').fuse([fl, fr])
cuts = [solid('fp_%d_negative_part.stl' % n) for n in (18, 19, 20, 21)]
for x in joint_x:
    for z in joint_z:
        cuts.append(Part.makeCylinder(pilot_d / 2, pilot_y[1] - pilot_y[0], V(x, pilot_y[0], z), V(0, 1, 0)))
# ID text: OpenSCAD makes orig/id_F.stl (cm1000_m6.scad part="id_F"), engraved 0.5 into the top face
cuts.append(solid('id_F.stl'))
print('fills', round(fl.Volume, 1), round(fr.Volume, 1), 'body', round(body.Volume, 1), len(body.Solids))
out = body.cut(cuts)
print('valid', out.isValid(), 'solids', len(out.Solids), 'volume', round(out.Volume, 1))
m = MeshPart.meshFromShape(Shape=out, LinearDeflection=0.01, AngularDeflection=0.2618, Relative=False)
m.write(os.path.join(here, '..', 'CM6A_faceplate.stl'))
print('facets', m.CountFacets)
