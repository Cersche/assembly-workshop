# CM1P-T3: third test slice for the one-piece CM1000 bracket. The real faceplate (baseline mesh + light pipes) cut to 30 deep,
# so it tests what T2's open middle could not: the nose pocket and pipe ends on the modem. Width from T2: modem 211.69 (215 - 3.31 play).
# Frame: X across (254 plate), Y depth (plate front Y=0), Z height (0..44.45).
# Run from this folder: "C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('cm1p_t3_freecad.py').read())"
import os, Mesh, MeshPart, Part, FreeCAD as App
V = App.Vector
here = os.getcwd()
orig = os.path.join(here, '..', '..', 'CM1000_M6_2026-10-28', 'src', 'orig')
def solid(path, mat=None):
    m = Mesh.Mesh(path)
    if mat: m.transform(mat)
    s = Part.Shape(); s.makeShapeFromMesh(m.Topology, 0.01)
    return Part.makeSolid(Part.makeShell(s.Faces))
def prism(pts, axis, a, b):
    # polygon in the plane across axis ('x': (y, z), 'y': (x, z)), extruded from a to b along the axis
    p3 = [V(a, u, w) if axis == 'x' else V(u, a, w) for u, w in pts]
    d = V(b - a, 0, 0) if axis == 'x' else V(0, b - a, 0)
    return Part.Face(Part.makePolygon(p3 + [p3[0]])).extrude(d)

plate_h, mid, rail_x, depth = 44.45, 44.45 / 2, 16.77, 30.0
modem_w = 211.69           # T2: 215 between floors less 3.31 total play, assumes nothing flexed
gap_x = 0.75               # clearance per side, about 1.5 total play
flat_w = 8.0               # channel floor, as T2
tip_x = 127 - modem_w / 2 - gap_x
slope = 14 / (22.2 - flat_w / 2)
over = 23.5
nose_k = (22.2 - 1.5) / 15
floor_y, floor_h, far_y = 1.6, 2.7, 20.0   # modem stops on the 1.6 walls, 1.2 clear on the nose, as T2
wall_x = 25.0              # stop walls end short of the icons at X 25.9

sx = tip_x + slope * (over - flat_w / 2)
channel = prism([(tip_x, mid - flat_w / 2), (tip_x, mid + flat_w / 2), (sx, mid + over), (254 - sx, mid + over),
                 (254 - tip_x, mid + flat_w / 2), (254 - tip_x, mid - flat_w / 2), (254 - sx, mid - over), (sx, mid - over)], 'y', floor_y, depth + 1)
h = floor_h + nose_k * (far_y - floor_y)
nose = prism([(floor_y, mid - floor_h), (floor_y, mid + floor_h), (far_y, mid + h), (depth + 2, mid + h),
              (depth + 2, mid - h), (far_y, mid - h)], 'x', 0, 254)
pocket = channel.common(nose)

w = 254 - 2 * rail_x
clip = Part.makeBox(w, depth - 0.5, plate_h, V(rail_x, 0.5, 0))   # front 0.5 goes: plain skin below, the logo/icon recesses cracked the mesh and don't affect fit
body = solid(os.path.join(orig, 'fp_1_normal_part.stl')).common(clip)
print('plate', round(body.Volume, 1), len(body.Solids))
# pipes grown 0.05 per side across and moved off the front face by 0.05: faces coplanar with the plate break the boolean (as CM6A's ear fills)
for n, x0 in ((4, 100.0), (5, 146.0), (6, 134.5), (7, 123.0), (8, 111.5)):
    kx, kz = 8.1 / 8, 8.09 / 7.99
    pm = App.Matrix(kx, 0, 0, x0 - 0.05 - kx * x0, 0, 1, 0, 0.05, 0, 0, kz, 26.18 - kz * 26.23, 0, 0, 0, 1)
    body = body.fuse(solid(os.path.join(orig, 'fp_%d_normal_part.stl' % n), pm))
    print('pipe', n, body.isValid(), len(body.Solids))
body = body.fuse(Part.makeBox(w, 0.6, plate_h, V(rail_x, 0, 0)))
print('pipes done', body.isValid(), len(body.Solids), round(body.Volume, 1))
for x0, x1 in ((rail_x, 40.0), (214.0, 254 - rail_x)):
    body = body.fuse(Part.makeBox(x1 - x0, depth - floor_y, plate_h, V(x0, floor_y, 0)))
for x0, x1 in ((rail_x, wall_x), (254 - wall_x, 254 - rail_x)):
    body = body.fuse(Part.makeBox(x1 - x0, floor_y, plate_h, V(x0, 0, 0)))
print('blocks done', body.isValid(), len(body.Solids), round(body.Volume, 1))
out = body.cut(pocket)
print('pocket done', out.isValid(), len(out.Solids), round(out.Volume, 1))
out = out.cut(solid(os.path.join(here, 'id.stl'))).removeSplitter()   # merged coplanar faces: unmerged ones left cracks in the export
print('valid', out.isValid(), 'solids', len(out.Solids), 'volume', round(out.Volume, 1), 'tip_x', round(tip_x, 3), 'bbox', out.BoundBox)
m = MeshPart.meshFromShape(Shape=out, LinearDeflection=0.01, AngularDeflection=0.2618, Relative=False)
m.write(os.path.join(here, '..', 'CM1P-T3_test_slice.stl'))
print('facets', m.CountFacets)
