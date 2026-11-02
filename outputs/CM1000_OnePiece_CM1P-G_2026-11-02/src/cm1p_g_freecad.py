# CM1P-G: CM1P-F with the V matched to the modem (CM1P-T4's channel) and the rails drawn leaning inward. Printed CM1P-E measured empty at its tips: outside 221.5 (design 220.46), V floors 214 (design 212.69), so its rails lean out.
# baseline's 137.62 depth, nose pocket as CM1P-T3 and CM1P-A.
# Frame: X across (254 plate), Y depth (plate front Y=0), Z height (0..44.45).
# Run from this folder: "C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('cm1p_g_freecad.py').read())"
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
gap_x = 0.25               # at the plate end, 0.5 total play, as CM1P-F and CM1P-T4
flat_w = 4.0               # modem end strip measured 3 (Brian), 4 so the corners don't bind
tip_x = 127 - modem_w / 2 - gap_x
slope = 14 / (22.2 - flat_w / 2)
over = 23.5
nose_k = (22.2 - 1.5) / 15
floor_y, floor_h, far_y = 1.6, 2.7, 20.0
lean = 0.52                # inward at the tips, per side: half of E's 1.04 outside growth. Assumes a straight lean that repeats
def dx(y): return lean * y / depth

sx = tip_x + slope * (over - flat_w / 2)
def section(y):
    d = dx(y)
    pts = [(tip_x + d, mid - flat_w / 2), (tip_x + d, mid + flat_w / 2), (sx + d, mid + over), (254 - sx - d, mid + over),
           (254 - tip_x - d, mid + flat_w / 2), (254 - tip_x - d, mid - flat_w / 2), (254 - sx - d, mid - over), (sx + d, mid - over)]
    p3 = [V(u, y, w) for u, w in pts]
    return Part.makePolygon(p3 + [p3[0]])
channel = Part.makeLoft([section(floor_y), section(depth + 1)], True, True)   # ruled: the channel narrows straight toward the tips
print('channel', channel.isValid(), round(channel.Volume, 1))
h = floor_h + nose_k * (far_y - floor_y)
nose = prism([(floor_y, mid - floor_h), (floor_y, mid + floor_h), (far_y, mid + h), (depth + 2, mid + h),
              (depth + 2, mid - h), (far_y, mid - h)], 'x', 0, 254)
pocket = channel.common(nose)

# ear fills as CM6A, inset 0.05 from coplanar plate faces, but 4 thick (Brian; baseline 3): added at the rear, front face unchanged
ky, oy = fit(0, 3, 0.05, 4.0); kz, oz = fit(0, 44.45, 0.05, 44.40)
kx, ox = fit(0, 16.9, 0.05, 17.3)
fl = solid(os.path.join(orig, 'fp_16_normal_part.stl'), App.Matrix(kx, 0, 0, ox, 0, ky, 0, oy, 0, 0, kz, oz, 0, 0, 0, 1))
kx, ox = fit(237.1, 254, 236.7, 253.95)
fr = solid(os.path.join(orig, 'fp_17_normal_part.stl'), App.Matrix(kx, 0, 0, ox, 0, ky, 0, oy, 0, 0, kz, oz, 0, 0, 0, 1))
body = solid(os.path.join(orig, 'fp_1_normal_part.stl')).fuse([fl, fr])
print('plate+ears', body.isValid(), len(body.Solids), round(body.Volume, 1))
# rail blocks start 0.3 back: behind the 0.2 logo recesses, and in front of the plate's rear face (0.4 at the old V apex), or a sealed void is left
for pts in (((rail_x + dx(0.3), 0.3), (40.0, 0.3), (40.0, depth), (rail_x + lean, depth)),
            ((214.0, 0.3), (254 - rail_x - dx(0.3), 0.3), (254 - rail_x - lean, depth), (214.0, depth))):
    p3 = [V(x, y, 0.05) for x, y in pts]   # 0.05 inset top and bottom: faces coplanar with the plate lose the plate in the boolean
    body = body.fuse(Part.Face(Part.makePolygon(p3 + [p3[0]])).extrude(V(0, 0, plate_h - 0.1)))
print('blocks', body.isValid(), len(body.Solids), round(body.Volume, 1))
# the ear fills square off the baseline's 0.5 front chamfer, so across the middle the plate looked about 0.45 short at top and bottom (Brian saw it from the front): square the middle to match
for z0 in (0.05, 43.5):
    body = body.fuse(Part.makeBox(220.0, 0.95, 0.9, V(17.0, 0.05, z0)))
print('front strips', body.isValid(), len(body.Solids), round(body.Volume, 1))

# rack slot cutters stretched from Y -1..4 to -1..5 so they clear the 4 ears
slot_m = App.Matrix(1, 0, 0, 0, 0, 1.2, 0, 0.2, 0, 0, 1, 0, 0, 0, 0, 1)
cuts = [pocket] + [solid(os.path.join(orig, 'fp_%d_negative_part.stl' % n), slot_m) for n in (18, 19, 20, 21)]
# side screw slot, left rail only as the baseline (Brian): baseline rail's position (Y 62.52..75.06, head recess 60.87..76.7 x 1.5 deep) + 1 longer at each end (Brian). Baseline centre is Z 22.99, the modem hole
# was reported at 22.25, so the slot is 0.74 taller downward to cover both
sl_z = (20.55, 24.69); rc_z = (18.97, 26.24)
cuts.append(stadium(15.0, 22.0, 61.52, 76.06, *sl_z))
cuts.append(stadium(15.0, 18.27 + dx(69), 59.87, 77.7, *rc_z))   # head recess stays 1.5 deep on the leaned rail
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
