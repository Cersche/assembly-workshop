"""CM6C digital checks: closed meshes, modem envelope clearance per Y plane, wall around the insert pilots.
Modem envelope = Brian's numbers (44.5 tall, 12 mm end wedge), tip at x20.38 from the 228 mm spread. Run from this folder."""
import math, os, struct
from collections import Counter

def load(p):
    d = open(p, 'rb').read()
    if d[:5] == b'solid' and b'facet' in d[:400]:
        vs = [tuple(float(x) for x in l.split()[1:4]) for l in d.decode('utf-8', 'ignore').splitlines() if l.strip().startswith('vertex')]
        return [vs[i:i + 3] for i in range(0, len(vs), 3)]
    n = struct.unpack('<I', d[80:84])[0]
    return [[struct.unpack('<3f', d[84 + 50 * i + 12 + 12 * j:84 + 50 * i + 24 + 12 * j]) for j in range(3)] for i in range(n)]

def closed(t):
    e = Counter()
    for a, b, c in t:
        for u, v in ((a, b), (b, c), (c, a)):
            u, v = tuple(round(x, 4) for x in u), tuple(round(x, 4) for x in v)
            if u != v: e[(min(u, v), max(u, v))] += 1
    return sum(1 for n in e.values() if n != 2)

def slice_y(t, y):
    out = []
    for tr in t:
        p = []
        for a, b in ((tr[0], tr[1]), (tr[1], tr[2]), (tr[2], tr[0])):
            if (a[1] - y) * (b[1] - y) < 0:
                s = (y - a[1]) / (b[1] - a[1]); p.append((a[0] + s * (b[0] - a[0]), a[2] + s * (b[2] - a[2])))
        if len(p) == 2: out.append(p)
    return out

def seg_dist(p, a, b):
    dx, dz = b[0] - a[0], b[1] - a[1]; L = dx * dx + dz * dz
    s = 0 if L == 0 else max(0, min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dz) / L))
    return math.hypot(p[0] - a[0] - s * dx, p[1] - a[1] - s * dz)

MID, TIP, SL, HALF = 44.45 / 2, 20.38, 12 / 22.25, 22.25
def modem_x(z):   # modem's left surface at height z
    return TIP + SL * abs(z - MID)
def nose_half(y):
    return 1.375 * y

P = {n: load('../CM6C_%s.stl' % n) for n in ('faceplate', 'rail_l', 'rail_r')}
for n, t in P.items():
    vs = [v for tr in t for v in tr]
    print(n, 'tris', len(t), 'bad edges', closed(t), 'bbox', [(round(min(v[i] for v in vs), 2), round(max(v[i] for v in vs), 2)) for i in range(3)])

print('\nLeft-end clearance, rail/stub surface to the modem wedge (positive = clear)')
for y, src in [(10, 'faceplate'), (12, 'faceplate'), (14, 'faceplate'), (15.5, 'faceplate'), (18, 'rail_l'), (40, 'rail_l'), (80, 'rail_l'), (130, 'rail_l')]:
    best = 99; at = None
    for a, b in slice_y(P[src], y):
        for k in range(11):
            s = k / 10; x, z = a[0] + s * (b[0] - a[0]), a[1] + s * (b[1] - a[1])
            lim = min(HALF, nose_half(y)) if src == 'faceplate' else HALF
            if abs(z - MID) > lim or x > 40: continue
            c = modem_x(z) - x
            if c < best: best, at = c, (round(x, 2), round(z, 2))
    print('Y', y, src, 'min clearance', round(best, 2), 'at x,z', at)

print('\nWall from each 7.6 pilot (faceplate, Y12 and Y15.5) to the nearest other surface')
for y in (9.5, 12, 15.5):
    segs = slice_y(P['faceplate'], y)
    for cx, cz in ((22.2, 5.6), (22.2, 38.85), (231.8, 5.6), (231.8, 38.85)):
        d = min(seg_dist((cx, cz), a, b) for a, b in segs if abs(math.hypot((a[0] + b[0]) / 2 - cx, (a[1] + b[1]) / 2 - cz) - 3.8) > 0.05)
        print('Y', y, 'pilot', cx, cz, 'wall', round(d - 3.8, 2))

print('\nFlange wall around the 6.6 hole, Y18')
segs = slice_y(P['rail_l'], 18)
for cz in (5.6, 38.85):
    d = min(seg_dist((22.2, cz), a, b) for a, b in segs if abs(math.hypot((a[0] + b[0]) / 2 - 22.2, (a[1] + b[1]) / 2 - cz) - 3.3) > 0.05)
    print('z', cz, 'wall', round(d - 3.3, 2))
print('\nRail web in the bay, Y40: z range and thickness')
segs = slice_y(P['rail_l'], 40)
zs = [p[1] for s in segs for p in s]; xs = [p[0] for s in segs for p in s]
print('z', round(min(zs), 2), round(max(zs), 2), 'x', round(min(xs), 2), round(max(xs), 2))
