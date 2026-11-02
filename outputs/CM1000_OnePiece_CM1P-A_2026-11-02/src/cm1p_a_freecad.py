# CM1P-A: full one-piece CM1000 bracket. Baseline faceplate (rack slots, ears, logo/icon recesses, pipe holes) + plain rails to the
# baseline's 137.62 depth, modem channel and nose pocket exactly as CM1P-T3, which went on by hand with 1.5 total side play.
# Frame: X across (254 plate), Y depth (plate front Y=0), Z height (0..44.45).
# Run from this folder: "C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('cm1p_a_freecad.py').read())"
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
    p3 = [V(a, u, w) if axis == 'x' else V(u, a, w) for u, w in pts]
    d = V(b - a, 0, 0) if axis == 'x' else V(0, b - a, 0)
    return Part.Face(Part.makePolygon(p3 + [p3[0]])).extrude(d)
def fit(lo, hi, nlo, nhi):
    k = (nhi - nlo) / (hi - lo); return k, nlo - k * lo
def stadium(x0, x1, y0, y1, z0, z1):
    # slot along Y, extruded along X, round ends
    r = (z1 - z0) / 2; zc = (z0 + z1) / 2
    s = Part.makeBox(x1 - x0, y1 - y0 - 2 * r, 2 * r, V(x0, y0 + r, z0))
    for y in (y0 + r, y1 - r):
        s = s.fuse(Part.makeCylinder(r, x1 - x0, V(x0, y, zc), V(1, 0, 0)))
    return s

plate_h, mid, rail_x, depth = 44.45, 44.45 / 2, 16.77, 137.62
modem_w = 211.69           # T2: 215 between floors less 3.31 total play, assumes nothing flexed
gap_x = 0.75               # T3: printed, on by hand, 1.5 total play
flat_w = 8.0
tip_x = 127 - modem_w / 2 - gap_x
slope = 14 / (22.2 - flat_w / 2)
over = 23.5
nose_k = (22.2 - 1.5) / 15
floor_y, floor_h, far_y = 1.6, 2.7, 20.0

sx = tip_x + slope * (over - flat_w / 2)
channel = prism([(tip_x, mid - flat_w / 2), (tip_x, mid + flat_w / 2), (sx, mid + over), (254 - sx, mid + over),
                 (254 - tip_x, mid + flat_w / 2), (254 - tip_x, mid - flat_w / 2), (254 - sx, mid - over), (sx, mid - over)], 'y', floor_y, depth + 1)
h = floor_h + nose_k * (far_y - floor_y)
nose = prism([(floor_y, mid - floor_h), (floor_y, mid + floor_h), (far_y, mid + h), (depth + 2, mid + h),
              (depth + 2, mid - h), (far_y, mid - h)], 'x', 0, 254)
pocket = channel.common(nose)

# ear fills as CM6A: inset 0.05 from coplanar plate faces
ky, oy = fit(0, 3, 0.05, 2.95); kz, oz = fit(0, 44.45, 0.05, 44.40)
kx, ox = fit(0, 16.9, 0.05, 17.3)
fl = solid(os.path.join(orig, 'fp_16_normal_part.stl'), App.Matrix(kx, 0, 0, ox, 0, ky, 0, oy, 0, 0, kz, oz, 0, 0, 0, 1))
kx, ox = fit(237.1, 254, 236.7, 253.95)
fr = solid(os.path.join(orig, 'fp_17_normal_part.stl'), App.Matrix(kx, 0, 0, ox, 0, ky, 0, oy, 0, 0, kz, oz, 0, 0, 0, 1))
body = solid(os.path.join(orig, 'fp_1_normal_part.stl')).fuse([fl, fr])
print('plate+ears', body.isValid(), len(body.Solids), round(body.Volume, 1))
# rail blocks start 0.3 back: behind the 0.2 logo recesses, and in front of the plate's rear face (0.4 at the old V apex), or a sealed void is left
for x0, x1 in ((rail_x, 40.0), (214.0, 254 - rail_x)):
    body = body.fuse(Part.makeBox(x1 - x0, depth - 0.3, plate_h - 0.1, V(x0, 0.3, 0.05)))   # 0.05 inset top and bottom: faces coplanar with the plate lose the plate in the boolean
print('blocks', body.isValid(), len(body.Solids), round(body.Volume, 1))
cuts = [pocket] + [solid(os.path.join(orig, 'fp_%d_negative_part.stl' % n)) for n in (18, 19, 20, 21)]
# side screw slots: baseline rail's length and position (Y 62.52..75.06, head recess 60.87..76.7 x 1.5 deep). Baseline centre is Z 22.99, the modem hole
# was reported at 22.25, so the slot is 0.74 taller downward to cover both
sl_z = (20.55, 24.69); rc_z = (18.97, 26.24)
for x0, x1, rx0, rx1 in ((15.0, 22.0, 15.0, 18.27), (232.0, 239.0, 235.73, 239.0)):
    cuts.append(stadium(x0, x1, 62.52, 75.06, *sl_z))
    cuts.append(stadium(rx0, rx1, 60.87, 76.7, *rc_z))
cuts.append(solid(os.path.join(here, 'id.stl')))
out = body.cut(cuts)
print('cuts', out.isValid(), len(out.Solids), round(out.Volume, 1))
out = out.removeSplitter()
print('valid', out.isValid(), 'solids', len(out.Solids), 'shells', len(out.Shells), 'volume', round(out.Volume, 1), 'tip_x', round(tip_x, 3), 'bbox', out.BoundBox)
m = MeshPart.meshFromShape(Shape=out, LinearDeflection=0.01, AngularDeflection=0.2618, Relative=False)
m.write(os.path.join(here, 'parts', 'body.stl'))
print('body facets', m.CountFacets)
# colour parts stay separate as in the baseline; the pipes' rear ends get the same pocket cut (T3 trimmed them the same way)
for n in (4, 5, 6, 7, 8):
    p = solid(os.path.join(orig, 'fp_%d_normal_part.stl' % n)).cut(pocket)
    print('pipe', n, p.isValid(), len(p.Solids), round(p.BoundBox.YMax, 2))
    MeshPart.meshFromShape(Shape=p, LinearDeflection=0.01, AngularDeflection=0.2618, Relative=False).write(os.path.join(here, 'parts', 'pipe_%d.stl' % n))
