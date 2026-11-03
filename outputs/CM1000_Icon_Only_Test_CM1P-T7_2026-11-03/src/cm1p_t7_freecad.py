# CM1P-T7: 70 wide slice of CM1P-O's plate and lips with the 5 icon-only pipes in their real places, open tunnels behind. Only tests light, no rails.
# Frame as CM1P-O: X across, Y depth (plate front Y=0), Z height (0..44.45). Modem front at Y 4.1, sits flat on the same table as the slice.
# Run from this folder: "C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('cm1p_t7_freecad.py').read())"
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
os.makedirs(os.path.join(here, 'parts'), exist_ok=True)

plate_h, mid = 44.45, 44.45 / 2
x0, x1 = 92.0, 162.0
# same pocket numbers as CM1P-O
over = 23.5
nose_k = (22.2 - 1.5) / 25
nose_gap = 0.5
floor_y, floor_h = 4.1, 1.5 + nose_gap
far_y = floor_y + (over - floor_h) / nose_k
lip_end = floor_y + (plate_h / 2 - 1.47 - floor_h) / nose_k
h = floor_h + nose_k * (far_y - floor_y)
pocket = prism([(floor_y, mid - floor_h), (floor_y, mid + floor_h), (far_y, mid + h), (60, mid + h), (60, mid - h), (far_y, mid - h)], 0, 254)
# middle relief as CM1P-O, narrower: the 6 at each end of the slice is what the modem's front stops on
relief = prism([(floor_y + 0.01, mid + floor_h), (floor_y - 1.24, 22.72), (floor_y - 1.24, 21.72), (floor_y + 0.01, mid - floor_h)], 98, 156)

pipe_c = {4: 104.0, 8: 115.5, 7: 127.0, 6: 138.5, 5: 150.0}   # baseline part: X
pipe_z = (26.23 + 34.22) / 2
for k, n in enumerate(pipe_c, 1):
    p = solid(os.path.join(orig, 'fp_%d_normal_part.stl' % n)).common(Part.makeBox(254, 2.0, plate_h, V(0, -0.5, 0)))   # icon + round section to Y 1.5, as CM1P-T6's hole 1
    print('icon', k, p.isValid(), len(p.Solids), round(p.BoundBox.YMax, 2), round(p.Volume, 1), flush=True)
    write(p, 'icon_%d.stl' % k)

body = solid(os.path.join(orig, 'fp_1_normal_part.stl')).common(Part.makeBox(x1 - x0, 12.0, plate_h, V(x0, -1.0, 0)))
fill = Part.makeBox(x1 - x0, lip_end - 0.3, plate_h - 0.1, V(x0, 0.3, 0.05)).cut([Part.makeCylinder(4.02, 30.0, V(cx, 0.0, pipe_z), V(0, 1, 0)) for cx in pipe_c.values()])
body = body.fuse(fill)
for z0 in (0.05, 43.5):
    body = body.fuse(Part.makeBox(x1 - x0, 0.95, 0.9, V(x0, 0.05, z0)))
out = body.cut([pocket, relief, solid(os.path.join(here, 'id.stl'))]).removeSplitter()
print('T7 valid', out.isValid(), 'solids', len(out.Solids), 'shells', len(out.Shells), 'cm3', round(out.Volume / 1000, 1), out.BoundBox, flush=True)
write(out, 'body.stl')
