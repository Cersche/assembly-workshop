"""Option A (faceplates proud) vs option B (frame flush with faceplates), with example generic gear.
X width, Y depth front->rear, Z up, mm. Concept preview only."""
import math, os, sys

out = sys.argv[1]
os.makedirs(out, exist_ok=True)

def zprism(poly, z0, z1):
    a = [(x, y, z0) for x, y in poly]
    b = [(x, y, z1) for x, y in poly]
    n = len(poly)
    tris = [(a[0], a[i + 1], a[i]) for i in range(1, n - 1)] + [(b[0], b[i], b[i + 1]) for i in range(1, n - 1)]
    for i in range(n):
        j = (i + 1) % n
        tris += [(a[i], a[j], b[j]), (a[i], b[j], b[i])]
    return tris

def xprism(poly, x0, x1):   # poly in (y, z)
    return [tuple((p[2], p[0], p[1]) for p in t) for t in zprism(poly, x0, x1)]

def yprism(poly, y0, y1):   # poly in (x, z)
    return [tuple((p[0], p[2], p[1]) for p in t) for t in zprism(poly, y0, y1)]

def rrect(x0, x1, y0, y1, r=0.0, round_=()):
    centers = {(0, 0): (x0 + r, y0 + r, 180), (1, 0): (x1 - r, y0 + r, 270),
               (1, 1): (x1 - r, y1 - r, 0), (0, 1): (x0 + r, y1 - r, 90)}
    pts = []
    for c in ((0, 0), (1, 0), (1, 1), (0, 1)):
        if c in round_:
            cx, cy, a0 = centers[c]
            pts += [(cx + r * math.cos(math.radians(a0 + 15 * k)), cy + r * math.sin(math.radians(a0 + 15 * k))) for k in range(7)]
        else:
            pts.append((x1 if c[0] else x0, y1 if c[1] else y0))
    return pts

def box(x0, x1, y0, y1, z0, z1):
    return zprism(rrect(x0, x1, y0, y1), z0, z1)

def bar(y0, z0, y1, z1, w, x0, x1):
    dy, dz = y1 - y0, z1 - z0
    l = math.hypot(dy, dz)
    py, pz = -dz / l * w / 2, dy / l * w / 2
    return xprism([(y0 + py, z0 + pz), (y0 - py, z0 - pz), (y1 - py, z1 - pz), (y1 + py, z1 + pz)], x0, x1)

ALL = [(0, 0), (1, 0), (1, 1), (0, 1)]
OUTER = [(1, 0), (1, 1)]
U, C, S, T, R = 44.45, 28.0, 24.0, 8.0, 6.0
Z0, Z1 = C, C + 9 * U
MY = 290.0
mx = lambda ts: [tuple((-x, y, z) for x, y, z in reversed(t)) for t in ts]
my = lambda ts: [tuple((x, MY - y, z) for x, y, z in reversed(t)) for t in ts]
full = lambda q: q + mx(q) + my(q) + mx(my(q))
shift = lambda ts, dx: [tuple((x + dx, y, z) for x, y, z in t) for t in ts]

def frame(opt):
    q = {k: [] for k in ("posts", "rails", "widths", "nodes", "trim", "strips")}
    q["posts"] = box(104, 124, 33, 53, Z0, Z1)
    if opt == "A":     # node faces flush with the post sleeve; strips and faceplates stand proud
        col = lambda z0, z1: zprism(rrect(104, 128, 29, 57, R, OUTER), z0, z1)
        xs, ys = ((29, 57), 76, 122), ((100, 128), 35, 81)
        brace_x, out_x = (122, 128), 128
    else:              # rounded bezel columns frame the faceplates; front of frame flush with faceplates (Y 21)
        col = lambda z0, z1: zprism(rrect(126, 138, 21, 57, R, OUTER), z0, z1) + box(124, 126, 25, 57, z0, z1) \
            + box(104, 124, 53, 57, z0, z1)
        xs, ys = ((21, 57), 76, 132), ((100, 138), 27, 81)
        brace_x, out_x = (132, 138), 138
    for zc0, c0, c1 in ((0.0, 0.0, C + S), (Z1, Z1 - S, Z1 + C)):
        zh = zc0 + 4
        q["nodes"] += col(c0, c1)
        q["nodes"] += xprism(rrect(*xs[0], zc0, zc0 + C, R, ALL), xs[1], xs[2]) \
            + yprism(rrect(*ys[0], zc0, zc0 + C, R, ALL), ys[1], ys[2])
        q["widths"] += box(0, 100, 33, 53, zh, zh + 20)
        if opt == "B":   # printed cover over the width member, flush with the node fronts
            q["trim"] += xprism(rrect(21, 33, zc0, zc0 + C, R, [(0, 0), (0, 1)]), 0, xs[1])
        q["rails"] += box(104, 124, 45, MY / 2, zh, zh + 20)   # 200 stock: runs under the post into the node core
    L = (Z1 - Z0 - 2 * S) / 3
    for k in range(3):
        q["strips"] += box(104, 124, 25, 33, Z0 + k * 3 * U + 0.2, Z0 + (k + 1) * 3 * U - 0.2)
        q["trim"] += col(Z0 + S + k * L + 0.2, Z0 + S + (k + 1) * L - 0.2)
    q["extrusion_rails_2020"] = q.pop("rails") + q.pop("widths")
    parts = {k: full(v) for k, v in q.items()}
    za, zb = Z0 + 3 * U + 0.2, Z0 + 6 * U - 0.2
    ya, yb = 57, MY - 57
    br = box(*brace_x, ya, yb, za, za + 10) + box(*brace_x, ya, yb, zb - 10, zb) \
        + bar(ya + 6, za + 5, yb - 6, zb - 5, 10, *brace_x) + bar(ya + 6, zb - 5, yb - 6, za + 5, 10, *brace_x)
    parts["side_braces"] = br + mx(br)
    return parts, out_x

# example generic gear: (first U, U count, device w x d x h, rear plate)
GEAR = [(1, 2, (180, 230, 80), True), (3, 1, (200, 120, 30), False), (6, 2, (190, 180, 78), False), (9, 1, (170, 140, 32), False)]
def gear():
    plates, trays, devices = [], [], []
    for s, n, (w, d, h), rear in GEAR:
        zb = Z0 + (s - 1) * U
        plates += box(-126, 126, 21, 25, zb + 0.025, zb + n * U - 0.025)
        if rear:
            plates += box(-126, 126, 265, 269, zb + 0.025, zb + n * U - 0.025)
        trays += box(-w / 2 - 4, w / 2 + 4, 25, 26 + d, zb + 1, zb + 3)
        devices += box(-w / 2, w / 2, 27, 26 + d, zb + 3, zb + 3 + h)
    return {"faceplates": plates, "example_gear": trays + devices}

names = []
for opt, dx in (("A", 0.0), ("B", 340.0)):
    parts, out_x = frame(opt)
    parts.update(gear())
    for k, tris in parts.items():
        name = f"{opt}_{k}"
        with open(os.path.join(out, name + ".stl"), "w", encoding="utf-8") as f:
            f.write(f"solid {name}\n")
            for tri in shift(tris, dx):
                f.write(" facet normal 0 0 0\n  outer loop\n")
                for p in tri:
                    f.write("   vertex %.3f %.3f %.3f\n" % p)
                f.write("  endloop\n endfacet\n")
            f.write(f"endsolid {name}\n")
        names.append(os.path.join(out, name + ".stl"))
    print(opt, "outer width", 2 * out_x)
print("\n".join(names))
