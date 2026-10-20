"""Measure a reference mesh (a bracket that already works) so our design can learn from it.

Born from the OptiPlex bracket study (work/optiplex-bracket-study/Report.md, 2026-10-20): the bracket's
floor had two 2 mm grooves for the PC's feet, invisible in a plain scan because the STL is three
overlapping bodies. Lessons built in here:

* Split the mesh into its separate bodies first and ray-cast each one on its own, then merge the solid
  intervals. Even/odd counting over overlapping bodies gives nonsense.
* A part may be modelled upside down or in print orientation: report both faces (floor and roof) and let
  the reader decide which one is "up" in the rack.
* Find recesses and bumps as clusters of rays whose surface differs from the face's main level.

Read-only: never writes the measured file. Third-party meshes stay where they are (local, never copied or
redistributed). Python 3.10 stdlib. Results are digital measurements only; fit and strength stay UNKNOWN.

Command line (run with `python -I` when the file came from outside the project):
  python -I mesh_study.py info FILE
  python -I mesh_study.py section FILE AXIS AT [STEP]      # ASCII cross-section, AXIS 0/1/2 = X/Y/Z
  python -I mesh_study.py recesses FILE UP [STEP] [MIN_DEPTH]  # floor/roof levels, grooves and bumps
"""
import math
import re
import struct
import sys
import zipfile
from collections import Counter, defaultdict


def load_mesh(path):
    """Triangles [((x,y,z),(x,y,z),(x,y,z)), ...] from binary/ASCII STL or 3MF (all objects, transforms ignored)."""
    path = str(path)
    if path.lower().endswith('.3mf'):
        tris = []
        with zipfile.ZipFile(path) as z:
            for name in z.namelist():
                if not name.endswith('.model'):
                    continue
                text = z.read(name).decode('utf-8', 'replace')
                verts = [tuple(float(v) for v in m) for m in
                         re.findall(r'<vertex\s+x="([^"]+)"\s+y="([^"]+)"\s+z="([^"]+)"', text)]
                for a, b, c in re.findall(r'<triangle\s+v1="(\d+)"\s+v2="(\d+)"\s+v3="(\d+)"', text):
                    tris.append((verts[int(a)], verts[int(b)], verts[int(c)]))
        return tris
    with open(path, 'rb') as f:
        data = f.read()
    if len(data) >= 84:
        n = struct.unpack_from('<I', data, 80)[0]
        if 84 + 50 * n == len(data):
            out = []
            for i in range(n):
                v = struct.unpack_from('<12f', data, 84 + 50 * i)
                out.append((v[3:6], v[6:9], v[9:12]))
            return out
    text = data.decode('utf-8', 'replace')
    vs = [tuple(float(x) for x in m) for m in re.findall(r'vertex\s+(\S+)\s+(\S+)\s+(\S+)', text)]
    return [tuple(vs[i:i + 3]) for i in range(0, len(vs) - 2, 3)]


def bbox(tris):
    return [(min(v[i] for t in tris for v in t), max(v[i] for t in tris for v in t)) for i in range(3)]


def volume(tris):
    s = 0.0
    for a, b, c in tris:
        s += (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0])
              + a[2] * (b[0] * c[1] - b[1] * c[0]))
    return s / 6


def bodies(tris):
    """Separate shells (triangles connected through shared vertices), largest first."""
    parent = {}

    def find(x):
        while parent.setdefault(x, x) != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    key = lambda v: (round(v[0], 4), round(v[1], 4), round(v[2], 4))
    for a, b, c in tris:
        ka = find(key(a))
        parent[find(key(b))] = ka
        parent[find(key(c))] = ka
    groups = defaultdict(list)
    for t in tris:
        groups[find(key(t[0]))].append(t)
    return sorted(groups.values(), key=len, reverse=True)


def open_edges(tris):
    """Number of edges not shared by exactly two triangles (0 = closed mesh)."""
    key = lambda v: (round(v[0], 4), round(v[1], 4), round(v[2], 4))
    edges = Counter()
    for a, b, c in tris:
        for u, v in ((a, b), (b, c), (c, a)):
            edges[tuple(sorted((key(u), key(v))))] += 1
    return sum(1 for n in edges.values() if n != 2)


def _merge(intervals):
    out = []
    for a, b in sorted(intervals):
        if out and a <= out[-1][1] + 1e-3:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out


def _body_columns(tris, axis, step):
    """Even/odd solid intervals along `axis` for ONE body, on a grid of the other two axes."""
    ua, va = [i for i in range(3) if i != axis]
    grid = defaultdict(list)
    for t in tris:
        us = [v[ua] for v in t]
        vv = [v[va] for v in t]
        for i in range(math.floor(min(us) / step), math.floor(max(us) / step) + 1):
            for j in range(math.floor(min(vv) / step), math.floor(max(vv) / step) + 1):
                grid[(i, j)].append(t)
    out = {}
    for (i, j), cell in grid.items():
        pu, pv = (i + 0.5) * step + 1e-4, (j + 0.5) * step + 2e-4   # nudged off vertices and edges
        hits = []
        for a, b, c in cell:
            x1, y1, x2, y2, x3, y3 = a[ua], a[va], b[ua], b[va], c[ua], c[va]
            den = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
            if abs(den) < 1e-12:
                continue
            l1 = ((y2 - y3) * (pu - x3) + (x3 - x2) * (pv - y3)) / den
            l2 = ((y3 - y1) * (pu - x3) + (x1 - x3) * (pv - y3)) / den
            if min(l1, l2, 1 - l1 - l2) < 0:
                continue
            hits.append(l1 * a[axis] + l2 * b[axis] + (1 - l1 - l2) * c[axis])
        hits.sort()
        uniq = []
        for h in hits:
            if not uniq or abs(h - uniq[-1]) > 1e-5:
                uniq.append(h)
        if len(uniq) >= 2:
            out[((i + 0.5) * step, (j + 0.5) * step)] = [(uniq[k], uniq[k + 1]) for k in range(0, len(uniq) - 1, 2)]
    return out


def columns(tris, axis, step=1.0):
    """Solid intervals along `axis` per grid point, merged over all bodies (safe for overlapping bodies)."""
    merged = defaultdict(list)
    for body in bodies(tris):
        for k, iv in _body_columns(body, axis, step).items():
            merged[k].extend(iv)
    return {k: _merge(v) for k, v in merged.items()}


def section(tris, axis, at, step=1.0):
    """ASCII cross-section perpendicular to `axis` at `at`: '#' = material. Rows = higher axis on top."""
    ua, va = [i for i in range(3) if i != axis]
    # Rays run along ua on a grid of (axis, va); keep the grid row nearest `at`.
    cols = columns(tris, ua, step)
    at_c = (math.floor(at / step) + 0.5) * step
    pick = (lambda k: k[0]) if axis < va else (lambda k: k[1])
    other = (lambda k: k[1]) if axis < va else (lambda k: k[0])
    rows_iv = {other(k): iv for k, iv in cols.items() if abs(pick(k) - at_c) < step / 4}
    b = bbox(tris)
    us = [b[ua][0] + (i + 0.5) * step for i in range(int((b[ua][1] - b[ua][0]) / step) + 1)]
    vs = [b[va][0] + (j + 0.5) * step for j in range(int((b[va][1] - b[va][0]) / step) + 1)]
    rows = []
    for v in reversed(vs):
        iv = rows_iv.get((math.floor(v / step) + 0.5) * step, [])
        rows.append('%7.1f %s' % (v, ''.join('#' if any(a <= u <= c for a, c in iv) else '.' for u in us)))
    return rows


def _cluster(points, step):
    cells = {(math.floor(x / step), math.floor(y / step)): (x, y, lv) for x, y, lv in points}
    seen, out = set(), []
    for start in cells:
        if start in seen:
            continue
        stack, group = [start], []
        seen.add(start)
        while stack:
            c = stack.pop()
            group.append(cells[c])
            for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (c[0] + d[0], c[1] + d[1])
                if n in cells and n not in seen:
                    seen.add(n)
                    stack.append(n)
        out.append(group)
    return out


def recesses(tris, up, step=0.5, min_depth=0.3, min_cells=4):
    """Floor and roof faces seen along axis `up`, their main level, and any grooves/bumps in them.

    Floor = top of the material that starts at the part's lowest level; roof = bottom of the material that
    ends at its highest level. Returns {'floor': {...}, 'roof': {...}} with 'level' (most common value) and
    'features': [{'kind': 'recess'|'bump', 'depth', 'span': [(min,max) of the two grid axes], 'cells'}].
    Which face is really "up" in the rack is for the reader to decide; both are reported.
    """
    lo, hi = bbox(tris)[up]
    cols = columns(tris, up, step)
    faces = {'floor': {}, 'roof': {}}
    for k, iv in cols.items():
        if iv[0][0] <= lo + 0.05 and iv[0][1] < hi - 0.05:
            faces['floor'][k] = iv[0][1]
        if iv[-1][1] >= hi - 0.05 and iv[-1][0] > lo + 0.05:
            faces['roof'][k] = iv[-1][0]
    result = {}
    for name, surf in faces.items():
        if not surf:
            result[name] = {'level': None, 'features': []}
            continue
        level = Counter(round(v, 2) for v in surf.values()).most_common(1)[0][0]
        feats = []
        for sign, kind in ((1, 'recess'), (-1, 'bump')):
            # A floor recess sits lower than the floor; a roof recess sits higher than the roof.
            d = (lambda v: level - v) if name == 'floor' else (lambda v: v - level)
            pts = [(k[0], k[1], v) for k, v in surf.items() if sign * d(v) >= min_depth]
            for g in _cluster(pts, step):
                if len(g) < min_cells:
                    continue
                depth = Counter(round(sign * d(v), 2) for _, _, v in g).most_common(1)[0][0]
                feats.append({'kind': kind, 'depth': depth, 'cells': len(g),
                              'span': [(min(p[0] for p in g) - step / 2, max(p[0] for p in g) + step / 2),
                                       (min(p[1] for p in g) - step / 2, max(p[1] for p in g) + step / 2)]})
        result[name] = {'level': level, 'features': sorted(feats, key=lambda f: -f['cells'])}
    return result


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd, path = argv[0], argv[1]
    tris = load_mesh(path)
    if cmd == 'info':
        b = bbox(tris)
        print('%s: %d triangles, %d bodies, %d open edges' % (path, len(tris), len(bodies(tris)), open_edges(tris)))
        print('size X %.2f  Y %.2f  Z %.2f   (bounds %s)' % (*(hi - lo for lo, hi in b), [tuple(round(x, 2) for x in r) for r in b]))
        for i, body in enumerate(bodies(tris)):
            print('  body %d: %d triangles, bounds %s, volume %.0f mm3' % (i, len(body), [tuple(round(x, 2) for x in r) for r in bbox(body)], volume(body)))
    elif cmd == 'section':
        axis, at = int(argv[2]), float(argv[3])
        print('\n'.join(section(tris, axis, at, float(argv[4]) if len(argv) > 4 else 1.0)))
    elif cmd == 'recesses':
        up = int(argv[2])
        step = float(argv[3]) if len(argv) > 3 else 0.5
        md = float(argv[4]) if len(argv) > 4 else 0.3
        axes = 'XYZ'
        ua, va = [axes[i] for i in range(3) if i != up]
        for name, face in recesses(tris, up, step, md).items():
            print('%s level %s' % (name, face['level']))
            for f in face['features']:
                print('  %s %.2f mm deep: %s %.1f-%.1f, %s %.1f-%.1f (%d samples)' % (
                    f['kind'], f['depth'], ua, *f['span'][0], va, *f['span'][1], f['cells']))
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
