# CM1000 snap-in diffuser, 3 concepts on a 70 wide slice of CM1P-P's plate (same plate as CM1P-T7). Concept only, no test-print ID yet.
# Frame as CM1P-P: X across, Y depth (plate front Y=0), Z height (0..44.45). Modem front at Y 4.1.
# Run from this folder: "C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('options_freecad.py').read())"
import os, Mesh, MeshPart, Part, FreeCAD as App
V = App.Vector
here = os.getcwd()
orig = os.path.normpath(os.path.join(here, '..', '..', 'outputs', 'CM1000_M6_2026-10-28', 'src', 'orig'))
out_dir = os.path.join(here, 'parts')
os.makedirs(out_dir, exist_ok=True)
def solid(path):
    m = Mesh.Mesh(path)
    s = Part.Shape(); s.makeShapeFromMesh(m.Topology, 0.01)
    return Part.makeSolid(Part.makeShell(s.Faces))
def prism(pts, a, b):
    p3 = [V(a, u, w) for u, w in pts]
    return Part.Face(Part.makePolygon(p3 + [p3[0]])).extrude(V(b - a, 0, 0))
def box(x0, x1, y0, y1, z0, z1):
    return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))
def rbox(x0, x1, y0, y1, z0, z1, r):
    b = box(x0, x1, y0, y1, z0, z1)
    return b.makeFillet(r, [e for e in b.Edges if abs(e.Vertexes[0].Y - e.Vertexes[1].Y) > 1e-6])
def rev(profile, cx, cz):
    # profile: (radius, y) points, turned about the Y axis line through (cx, cz)
    p3 = [V(cx + r, y, cz) for r, y in profile]
    return Part.Face(Part.makePolygon(p3 + [p3[0]])).revolve(V(cx, 0, cz), V(0, 1, 0), 360)
def write(shape, name):
    print(name, 'valid', shape.isValid(), 'solids', len(shape.Solids), 'cm3', round(shape.Volume / 1000, 3), flush=True)
    MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.01, AngularDeflection=0.2618, Relative=False).write(os.path.join(out_dir, name))

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
pipe_c = {4: 104.0, 8: 115.5, 7: 127.0, 6: 138.5, 5: 150.0}
pz = (26.23 + 34.22) / 2

body = solid(os.path.join(orig, 'fp_1_normal_part.stl')).common(Part.makeBox(x1 - x0, 12.0, plate_h, V(x0, -1.0, 0)))
fill = Part.makeBox(x1 - x0, lip_end - 0.3, plate_h - 0.1, V(x0, 0.3, 0.05)).cut([Part.makeCylinder(4.02, 30.0, V(cx, 0.0, pz), V(0, 1, 0)) for cx in pipe_c.values()])
body = body.fuse(fill)
for z0 in (0.05, 43.5):
    body = body.fuse(Part.makeBox(x1 - x0, 0.95, 0.9, V(x0, 0.05, z0)))
body = body.cut([pocket, relief])
print('base', body.isValid(), len(body.Solids), flush=True)

# shared window: X 98..156, Z 25.2..35.25. The bar is 0.15 smaller per side (a guess until a coupon proves it)
wx0, wx1, wz0, wz1, gap = 98.0, 156.0, 25.2, 35.25, 0.15
hook_x = (109.75, 144.25)   # above the ribs between pipes

# --- Option A: one bar, in from the front, bottom tongue + 2 top snap hooks; ribs and tunnels stay behind it
cuts = [rbox(wx0, wx1, -1, 1.5, wz0, wz1, 1.5), box(99.8, 154.2, 0.7, 1.6, 24.0, wz0 + 0.5)]
for x in hook_x:
    cuts.append(box(x - 2.8, x + 2.8, 1.4, 8.0, 33.5, wz1 - 0.01))
    cuts.append(box(x - 2.8, x + 2.8, 6.0, 7.4, wz1 - 0.02, 35.75))
write(body.cut(cuts).removeSplitter(), 'A_body.stl')
bar = rbox(wx0 + gap, wx1 - gap, 0.39, 1.45, wz0 + gap, wz1 - gap, 1.35).fuse(box(100, 154, 0.8, 1.45, 24.2, wz0 + gap + 0.5))
for x in hook_x:
    leg = box(x - 2.5, x + 2.5, 1.4, 7.0, 34.1, 35.0)
    barb = prism([(5.9, 35.0), (6.3, 35.4), (7.0, 35.4), (7.0, 35.0)], x - 2.5, x + 2.5)
    bar = bar.fuse([leg, barb])
icons = []
for n, cx in pipe_c.items():
    icons.append(solid(os.path.join(orig, 'fp_%d_normal_part.stl' % n)).common(box(cx - 5, cx + 5, -0.5, 0.39, 24, 36)))
bar = bar.fuse(icons)
write(bar.removeSplitter(), 'A_clear_bar.stl')
mask = rbox(wx0 + gap, wx1 - gap, 0.02, 0.39, wz0 + gap, wz1 - gap, 1.35).cut(icons)
write(mask, 'A_bar_mask.stl')

# --- Option B: one bar, in from behind, bottom tongue + 2 top snap hooks; front stays one piece with the icon holes open
cuts = [box(wx0, wx1, 1.0, 30, wz0, wz1), box(99.8, 154.2, 1.0, 2.3, 24.0, wz0 + 0.5)]
for x in hook_x:
    cuts.append(box(x - 2.8, x + 2.8, 3.8, 5.2, wz1 - 0.5, 35.75))
write(body.cut(cuts).removeSplitter(), 'B_body.stl')
bar = box(wx0 + gap, wx1 - gap, 1.02, 2.2, wz0 + gap, wz1 - gap).fuse(box(100, 154, 1.02, 2.2, 24.2, wz0 + gap + 0.5))
bar = bar.fuse([Part.makeCylinder(3.9, 0.6, V(cx, 0.45, pz), V(0, 1, 0)) for cx in pipe_c.values()])
for x in hook_x:
    leg = box(x - 2.5, x + 2.5, 2.1, 5.1, 34.2, wz1 - gap)
    barb = prism([(3.7, wz1 - gap), (4.0, 35.5), (5.0, 35.5), (5.0, wz1 - gap)], x - 2.5, x + 2.5)
    bar = bar.fuse([leg, barb])
write(bar.removeSplitter(), 'B_clear_bar.stl')

# --- Option C: five separate cups, in from behind down the existing tunnels; barb clicks into a groove. Front as B, ribs stay
groove = [rev([(3.9, 4.2), (4.35, 4.2), (4.35, 5.0), (3.9, 5.0)], cx, pz) for cx in pipe_c.values()]
write(body.cut(groove).removeSplitter(), 'C_body.stl')
for k, cx in enumerate(pipe_c.values(), 1):
    cup = rev([(0.0, 0.42), (3.9, 0.42), (3.9, 3.9), (4.2, 4.3), (4.2, 4.85), (3.9, 5.1), (3.9, 5.6), (3.15, 5.6), (3.15, 1.92), (0.0, 1.92)], cx, pz)
    for s in (box(cx - 0.4, cx + 0.4, 2.6, 6, pz - 5, pz + 5), box(cx - 5, cx + 5, 2.6, 6, pz - 0.4, pz + 0.4)):
        cup = cup.cut(s)
    write(cup, 'C_clear_cup_%d.stl' % k)
