# CM1P-O: CM1P-N's rails, V, lips and screw slot on the baseline faceplate front: logo, 5 light pipes with their icons, no window. Pipes run back to the lip surface, as the modem now sits further back on a longer slope.
# Frame: X across (254 plate), Y depth (plate front Y=0), Z height (0..44.45).
# Run from this folder: "C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('cm1p_o_freecad.py').read())"
import os, Mesh, MeshPart, Part, FreeCAD as App
V = App.Vector
here = os.getcwd()
orig = os.path.join(here, '..', '..', 'CM1000_M6_2026-10-28', 'src', 'orig')
def solid(path, mat=None):
    m = Mesh.Mesh(path)
    if mat: m.transform(mat)
    s = Part.Shape(); s.makeShapeFromMesh(m.Topology, 0.01)
    return Part.makeSolid(Part.makeShell(s.Faces))
def prism(pts, a, b):
    p3 = [V(a, u, w) for u, w in pts]
    return Part.Face(Part.makePolygon(p3 + [p3[0]])).extrude(V(b - a, 0, 0))
def fit(lo, hi, nlo, nhi):
    k = (nhi - nlo) / (hi - lo); return k, nlo - k * lo
def stadium(x0, x1, y0, y1, z0, z1):
    r = (z1 - z0) / 2; zc = (z0 + z1) / 2
    s = Part.makeBox(x1 - x0, y1 - y0 - 2 * r, 2 * r, V(x0, y0 + r, z0))
    for y in (y0 + r, y1 - r):
        s = s.fuse(Part.makeCylinder(r, x1 - x0, V(x0, y, zc), V(1, 0, 0)))
    return s
def write(shape, name):
    MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.01, AngularDeflection=0.2618, Relative=False).write(os.path.join(here, 'parts', name))

plate_h, mid, rail_x, depth = 44.45, 44.45 / 2, 16.77, 137.62
rail_end = depth + 10.0    # Brian: rails a tad short at the rear
k = 20.88 / 22.33          # the mount's slope, 43 degrees off vertical. Steeper than the modem's 35.9, so the modem rides on the arm tips, not on its end strip
modem_w, gap = 212.0, 0.25 # Brian's caliper; play per side at the arm tips
arm_end = 1.5              # the arm tip stays this thick, not a knife edge; it lies this far inside the modem's top and bottom faces
tip_dz = 22.2 - arm_end
arm_x = 127 - modem_w / 2 + 15 / 20.7 * (tip_dz - 1.5) - gap   # where the tip meets the modem's slope, less the play (wedge 15, Brian)
ax = rail_x + 2.58         # V floor: same 215.3 across as first drawn, rail stays 220.46 outside
floor_dz = tip_dz - (arm_x - ax) / k
over = 23.5
sx = arm_x + k * (over - tip_dz)
nose_k = (22.2 - 1.5) / 25   # Brian's 25 front slope, top and underside both measured
nose_gap = 0.5              # up and down, between lip and modem slope
back = 2.5                 # modem further back than CM1P-H
floor_y, floor_h = 1.6 + back, 1.5 + nose_gap
far_y = floor_y + (over - floor_h) / nose_k
lip_end = floor_y + (plate_h / 2 - 1.47 - floor_h) / nose_k   # lip stops blunt, about as thick as CM1P-J's lip end
lean = 0.52                # as CM1P-H, from CM1P-E's measured growth; assumes a straight lean that repeats on this V
def dx(y): return lean * y / depth
def section(y):
    d = dx(y)
    pts = [(ax + d, mid - floor_dz), (ax + d, mid + floor_dz), (sx + d, mid + over), (254 - sx - d, mid + over), (254 - ax - d, mid + floor_dz), (254 - ax - d, mid - floor_dz), (254 - sx - d, mid - over), (sx + d, mid - over)]
    p3 = [V(u, y, w) for u, w in pts]
    return Part.makePolygon(p3 + [p3[0]])
channel = Part.makeLoft([section(floor_y), section(rail_end + 1)], True, True)
h = floor_h + nose_k * (far_y - floor_y)
nose = prism([(floor_y, mid - floor_h), (floor_y, mid + floor_h), (far_y, mid + h), (rail_end + 2, mid + h), (rail_end + 2, mid - h), (far_y, mid - h)], 0, 254)
pocket = channel.common(nose)
# the baseline's relief behind the modem's nose, moved back with it: the modem stops on the end walls, 1.24 of room across the middle
relief = prism([(floor_y + 0.01, mid + floor_h), (floor_y - 1.24, 22.72), (floor_y - 1.24, 21.72), (floor_y + 0.01, mid - floor_h)], 40, 214)

ky, oy = fit(0, 3, 0.05, 4.0); kz, oz = fit(0, 44.45, 0.05, 44.40)
kx, ox = fit(0, 16.9, 0.05, 17.3)
fl = solid(os.path.join(orig, 'fp_16_normal_part.stl'), App.Matrix(kx, 0, 0, ox, 0, ky, 0, oy, 0, 0, kz, oz, 0, 0, 0, 1))
kx, ox = fit(237.1, 254, 236.7, 253.95)
fr = solid(os.path.join(orig, 'fp_17_normal_part.stl'), App.Matrix(kx, 0, 0, ox, 0, ky, 0, oy, 0, 0, kz, oz, 0, 0, 0, 1))
body = solid(os.path.join(orig, 'fp_1_normal_part.stl')).fuse([fl, fr])
print('V floor half', round(floor_dz, 2), 'arm_x', round(arm_x, 2), 'lip_end', round(lip_end, 2))
print('plate+ears', body.isValid(), len(body.Solids), round(body.Volume, 1))
for pts in (((rail_x + dx(0.3), 0.3), (arm_x + dx(0.3), 0.3), (arm_x + dx(rail_end), rail_end), (rail_x + dx(rail_end), rail_end)),
            ((254 - arm_x - dx(0.3), 0.3), (254 - rail_x - dx(0.3), 0.3), (254 - rail_x - dx(rail_end), rail_end), (254 - arm_x - dx(rail_end), rail_end))):
    p3 = [V(x, y, 0.05) for x, y in pts]
    body = body.fuse(Part.Face(Part.makePolygon(p3 + [p3[0]])).extrude(V(0, 0, plate_h - 0.1)))
# light pipes: baseline front (icon face + round section) as it is to Y 1.5, then a plain round section straight back to the lip surface, 0.5 off the modem's slope.
# Rear section 7.94 across (baseline 7.99) and tunnel 8.04: neither may lie on the baseline's faceted hole, near-coincident faces hang the boolean
pipe_c = {4: 104.0, 8: 115.5, 7: 127.0, 6: 138.5, 5: 150.0}
pipe_z = (26.23 + 34.22) / 2
pipes = []
for n, cx in pipe_c.items():
    src = solid(os.path.join(orig, 'fp_%d_normal_part.stl' % n))
    front = src.common(Part.makeBox(254, 2.0, plate_h, V(0, -0.5, 0)))
    p = front.fuse(Part.makeCylinder(3.97, 22.0, V(cx, 1.5, pipe_z), V(0, 1, 0))).cut(pocket).removeSplitter()
    print('pipe', n, p.isValid(), len(p.Solids), round(p.BoundBox.YMax, 2), round(p.Volume, 1), flush=True)
    pipes.append((n, p))
# fills the baseline's old nose pocket behind the logo recesses (0.2 deep), so the pocket can be recut further back; the pipe tunnels stay open
fill = Part.makeBox(220.0, lip_end - 0.3, plate_h - 0.1, V(17.0, 0.3, 0.05)).cut([Part.makeCylinder(4.02, 30.0, V(cx, 0.0, pipe_z), V(0, 1, 0)) for cx in pipe_c.values()])
body = body.fuse(fill)
print('blocks+fill', body.isValid(), len(body.Solids), round(body.Volume, 1))
for z0 in (0.05, 43.5):
    body = body.fuse(Part.makeBox(220.0, 0.95, 0.9, V(17.0, 0.05, z0)))

slot_m = App.Matrix(1, 0, 0, 0, 0, 1.2, 0, 0.2, 0, 0, 1, 0, 0, 0, 0, 1)
cuts = [pocket, relief] + [solid(os.path.join(orig, 'fp_%d_negative_part.stl' % n), slot_m) for n in (18, 19, 20, 21)]
# side screw slot, left rail only: CM1P-H's slot moved back with the modem, then screw_back further from Brian's fit of CM1P-K
screw_back = 8.71
sl_z = (20.55, 24.69); rc_z = (18.97, 26.24)
cuts.append(stadium(15.0, 24.0, 61.52 + back + screw_back, 76.06 + back + screw_back, *sl_z))
cuts.append(stadium(15.0, 18.27 + dx(69 + back + screw_back), 59.87 + back + screw_back, 77.7 + back + screw_back, *rc_z))
cuts.append(solid(os.path.join(here, 'id.stl')))
# rear bar provision, CM1P-I + these only: M3 x 3 x 5 insert bores, 4.2 x 4 deep, in the rail end faces, top and bottom on each rail. No bar yet, empty bores do no harm
for x in (22.5, 254 - 22.5):
    for z in (5.5, plate_h - 5.5):
        cuts.append(Part.makeCylinder(2.1, 5.0, V(x, rail_end - 4.0, z), V(0, 1, 0)))
out = body.cut(cuts)
print('cuts', out.isValid(), len(out.Solids), round(out.Volume, 1))
out = out.removeSplitter()
print('valid', out.isValid(), 'solids', len(out.Solids), 'shells', len(out.Shells), 'volume', round(out.Volume, 1), 'bbox', out.BoundBox)
write(out, 'body.stl')
for n, p in pipes: write(p, 'pipe_%d.stl' % n)
