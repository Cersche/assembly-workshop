# CM1P-T6: one 127 wide slice of CM1P-O's plate and lips with 10 light pipes, the same 5 types twice: A1-A5 to print as CM1P-O, B1-B5 to print at 100% infill. Only tests light, no rails.
# Frame as CM1P-O: X across, Y depth (plate front Y=0), Z height (0..44.45). Modem front at Y 4.1, sits flat on the same table as the slice.
# Run from this folder: "C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('cm1p_t6_freecad.py').read())"
import os, Mesh, MeshPart, Part, FreeCAD as App
V = App.Vector
here = os.getcwd()
orig = os.path.join(here, '..', '..', 'CM1000_M6_2026-10-28', 'src', 'orig')
def solid(path):
    m = Mesh.Mesh(path)
    s = Part.Shape(); s.makeShapeFromMesh(m.Topology, 0.01)
    return Part.makeSolid(Part.makeShell(s.Faces))
def prism(pts, a, b):
    p3 = [V(a, u, w) for u, w in pts]
    return Part.Face(Part.makePolygon(p3 + [p3[0]])).extrude(V(b - a, 0, 0))
def write(shape, name):
    MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.01, AngularDeflection=0.2618, Relative=False).write(os.path.join(here, 'parts', name))
def moved(shape, dx):
    s = shape.copy(); s.translate(V(dx, 0, 0)); return s
os.makedirs(os.path.join(here, 'parts'), exist_ok=True)

plate_h, mid = 44.45, 44.45 / 2
x0, x1 = 63.5, 190.5
shift = {'A': -28.75, 'B': 28.75}   # the baseline's 5 holes, X 98.25 to 155.75, copied side by side; the pitch stays 11.5 across the join at X 127
# same pocket numbers as CM1P-O
over = 23.5
nose_k = (22.2 - 1.5) / 25
nose_gap = 0.5
floor_y, floor_h = 4.1, 1.5 + nose_gap
far_y = floor_y + (over - floor_h) / nose_k
lip_end = floor_y + (plate_h / 2 - 1.47 - floor_h) / nose_k
h = floor_h + nose_k * (far_y - floor_y)
def nose_at(s):
    return prism([(floor_y - s, mid - floor_h), (floor_y - s, mid + floor_h), (far_y - s, mid + h), (60, mid + h), (60, mid - h), (far_y - s, mid - h)], 0, 254)
pocket = nose_at(0.0)
# middle relief as CM1P-O, narrower: the 6 at each end of the slice is what the modem's front stops on
relief = prism([(floor_y + 0.01, mid + floor_h), (floor_y - 1.24, 22.72), (floor_y - 1.24, 21.72), (floor_y + 0.01, mid - floor_h)], x0 + 6, x1 - 6)

pipe_c = {1: (4, 104.0), 2: (8, 115.5), 3: (7, 127.0), 4: (6, 138.5), 5: (5, 150.0)}   # type: (baseline part, baseline X)
pipe_z = (26.23 + 34.22) / 2
for hole, (n, cx) in pipe_c.items():
    src = solid(os.path.join(orig, 'fp_%d_normal_part.stl' % n))
    front = src.common(Part.makeBox(254, 2.0, plate_h, V(0, -0.5, 0)))
    cyl = lambda y1: Part.makeCylinder(3.97, y1 - 1.5, V(cx, 1.5, pipe_z), V(0, 1, 0))
    if hole == 1: p = front                                                  # icon only, 1.5 deep, open tunnel behind
    elif hole == 2: p = src                                                  # earlier faceplate's pipe, unchanged, open tunnel behind
    elif hole == 3: p = front.fuse(cyl(23.5)).cut(nose_at(2.85)).removeSplitter()   # halfway: 8.5 on the centre line, end parallel to the slope
    elif hole == 4: p = front.fuse(cyl(23.5)).cut(pocket).removeSplitter()   # CM1P-O's pipe
    else: p = front.fuse(cyl(6.5)).removeSplitter()                          # flat end at Y 6.5, clears the modem's slope at the pipe's lower edge
    for tag, dx in shift.items():
        q = moved(p, dx)
        print(tag, hole, q.isValid(), len(q.Solids), round(q.BoundBox.XMin, 2), round(q.BoundBox.YMax, 2), round(q.Volume, 1), flush=True)
        write(q, 'pipe_%s%d.stl' % (tag, hole))
for n in (2, 3):
    d = solid(os.path.join(orig, 'fp_%d_normal_part.stl' % n))
    for tag, dx in shift.items(): write(moved(d, dx), 'detail_%s%d.stl' % (tag, n))

plate = solid(os.path.join(orig, 'fp_1_normal_part.stl')).common(Part.makeBox(57.5, 12.0, plate_h, V(98.25, -1.0, 0)))
print('plate', plate.isValid(), len(plate.Solids), round(plate.Volume, 1), flush=True)
holes = [Part.makeCylinder(4.02, 30.0, V(c[1] + dx, 0.0, pipe_z), V(0, 1, 0)) for c in pipe_c.values() for dx in shift.values()]
fill = Part.makeBox(x1 - x0, lip_end - 0.3, plate_h - 0.1, V(x0, 0.3, 0.05)).cut(holes)
ends = [Part.makeBox(6.0, 0.95, plate_h - 0.1, V(x, 0.05, 0.05)) for x in (x0, x1 - 6)]
body = moved(plate, shift['A']).fuse([moved(plate, shift['B']), fill] + ends)
for z0 in (0.05, 43.5):
    body = body.fuse(Part.makeBox(x1 - x0, 0.95, 0.9, V(x0, 0.05, z0)))
print('filled', body.isValid(), len(body.Solids), round(body.Volume, 1), flush=True)
body = body.cut([pocket, relief])
print('cut', body.isValid(), len(body.Solids), round(body.Volume, 1), flush=True)
out = body.cut(solid(os.path.join(here, 'id.stl'))).removeSplitter()
print('T6 valid', out.isValid(), 'solids', len(out.Solids), 'shells', len(out.Shells), 'cm3', round(out.Volume / 1000, 1), out.BoundBox, flush=True)
write(out, 'body.stl')
