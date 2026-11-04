# CM1P-T8: option C. 70 wide slice of CM1P-P's plate with a barb groove in each tunnel and 5 clear cups that go in from behind, each with its raised icon in the plate's icon hole.
# Frame as CM1P-P: X across, Y depth (plate front Y=0), Z height (0..44.45). Modem front at Y 4.1, sits flat on the same table as the slice.
# Run from this folder after icons_profile.py: "C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('cm1p_t8_freecad.py').read())"
import os, json, Mesh, MeshPart, Part, FreeCAD as App
V = App.Vector
here = os.getcwd()
orig = os.path.join(here, '..', '..', 'CM1000_M6_2026-10-28', 'src', 'orig')
os.makedirs(os.path.join(here, 'parts'), exist_ok=True)
def solid(path):
    m = Mesh.Mesh(path)
    s = Part.Shape(); s.makeShapeFromMesh(m.Topology, 0.01)
    return Part.makeSolid(Part.makeShell(s.Faces))
def prism(pts, a, b):
    p3 = [V(a, u, w) for u, w in pts]
    return Part.Face(Part.makePolygon(p3 + [p3[0]])).extrude(V(b - a, 0, 0))
def box(x0, x1, y0, y1, z0, z1):
    return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))
def rev(profile, cx, cz):
    p3 = [V(cx + r, y, cz) for r, y in profile]
    return Part.Face(Part.makePolygon(p3 + [p3[0]])).revolve(V(cx, 0, cz), V(0, 1, 0), 360)
def outline(pts, y):
    pp = []
    for x, z in pts:
        q = V(round(x, 3), y, round(z, 3))
        if not pp or (q - pp[-1]).Length > 1e-3:
            pp.append(q)
    if (pp[0] - pp[-1]).Length > 1e-3:
        pp.append(pp[0])
    else:
        pp[-1] = pp[0]
    return Part.makePolygon(pp)
def extrude_poly(p, y0, y1):
    wires = [outline(p['o'], y0)] + [outline(h, y0) for h in p['h']]
    f = Part.Face(wires[0])
    for w in wires[1:]:
        f = f.cut(Part.Face(w))
    return f.extrude(V(0, y1 - y0, 0))
def write(shape, name):
    print('RESULT', name, 'valid', shape.isValid(), 'solids', len(shape.Solids), 'shells', len(shape.Shells), 'cm3', round(shape.Volume / 1000, 3), flush=True)
    MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.01, AngularDeflection=0.2618, Relative=False).write(os.path.join(here, 'parts', name))

icons = json.load(open(os.path.join(here, 'icons.json'), encoding='utf-8'))
plate_h, mid = 44.45, 44.45 / 2
x0, x1 = 92.0, 162.0
over = 23.5
nose_k = (22.2 - 1.5) / 25
floor_y, floor_h = 4.1, 2.0
far_y = floor_y + (over - floor_h) / nose_k
lip_end = floor_y + (plate_h / 2 - 1.47 - floor_h) / nose_k
h = floor_h + nose_k * (far_y - floor_y)
pocket = prism([(floor_y, mid - floor_h), (floor_y, mid + floor_h), (far_y, mid + h), (60, mid + h), (60, mid - h), (far_y, mid - h)], 0, 254)
relief = prism([(floor_y + 0.01, mid + floor_h), (floor_y - 1.24, 22.72), (floor_y - 1.24, 21.72), (floor_y + 0.01, mid - floor_h)], 98, 156)
pz = (26.23 + 34.22) / 2

body = solid(os.path.join(orig, 'fp_1_normal_part.stl')).common(Part.makeBox(x1 - x0, 12.0, plate_h, V(x0, -1.0, 0)))
fill = Part.makeBox(x1 - x0, lip_end - 0.3, plate_h - 0.1, V(x0, 0.3, 0.05)).cut([Part.makeCylinder(4.02, 30.0, V(v['cx'], 0.0, pz), V(0, 1, 0)) for v in icons.values()])
body = body.fuse(fill)
for z0 in (0.05, 43.5):
    body = body.fuse(Part.makeBox(x1 - x0, 0.95, 0.9, V(x0, 0.05, z0)))
cuts = [pocket, relief, solid(os.path.join(here, 'id.stl'))]
for v in icons.values():
    cuts.append(rev([(3.9, 4.2), (4.35, 4.2), (4.35, 5.0), (3.9, 5.0)], v['cx'], pz))   # barb groove
    cuts += [extrude_poly(p, -1.0, 0.45) for p in v['hole']]                              # icon hole, 0.1 play around the cup's icon
write(body.cut(cuts).removeSplitter(), 'body.stl')

for k, v in enumerate(icons.values(), 1):
    cx = v['cx']
    cup = rev([(0.0, 0.4), (3.9, 0.4), (3.9, 3.9), (4.2, 4.3), (4.2, 4.85), (3.9, 5.1), (3.9, 5.6), (3.15, 5.6), (3.15, 1.5), (0.0, 1.5)], cx, pz)
    for s in (box(cx - 0.4, cx + 0.4, 1.9, 6, pz - 5, pz + 5), box(cx - 5, cx + 5, 1.9, 6, pz - 0.4, pz + 0.4)):
        cup = cup.cut(s)
    cup = cup.fuse([extrude_poly(p, 0.0, 0.45) for p in v['icon']]).removeSplitter()
    write(cup, 'cup_%d_%s.stl' % (k, v['name']))
