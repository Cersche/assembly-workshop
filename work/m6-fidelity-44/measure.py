"""Task 44 read-only section audit. Python 3.10 standard library; millimetres.

Source meshes are measurement references only. Nothing here is imported by the generator.
"""
import collections
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'work/m6-rails-43'))
from measure_reference import mesh_info, crossing_intervals


def section(vs, ts, axis, station):
    axes = [a for a in range(3) if a != axis]
    segments = set()
    for tri in ts:
        points = [vs[i] for i in tri]
        hits = []
        for a, b in zip(points, points[1:] + points[:1]):
            if (a[axis] < station) != (b[axis] < station):
                t = (station-a[axis])/(b[axis]-a[axis])
                p = tuple(round(a[k]+t*(b[k]-a[k]), 5) for k in axes)
                if p not in hits:
                    hits.append(p)
        if len(hits) == 2 and hits[0] != hits[1]:
            segments.add(tuple(sorted(hits)))
    graph = collections.defaultdict(set)
    for a, b in segments:
        graph[a].add(b)
        graph[b].add(a)
    bad = {str(p): len(q) for p, q in graph.items() if len(q) != 2}
    loops = []
    remaining = set(segments)
    while remaining:
        a, b = remaining.pop()
        loop = [a, b]
        while b != loop[0]:
            nxt = [c for c in graph[b] if tuple(sorted((b, c))) in remaining]
            if not nxt:
                break
            c = nxt[0]
            remaining.remove(tuple(sorted((b, c))))
            loop.append(c)
            a, b = b, c
        # Preserve all section data, including any open chains, for audit.
        loops.append(dict(closed=loop[-1] == loop[0], points=loop[:-1] if loop[-1] == loop[0] else loop))
    return dict(station=station, axis=axis, bad_vertices=bad, loops=loops)


def volume(vs, ts):
    return abs(sum(vs[a][0]*(vs[b][1]*vs[c][2]-vs[b][2]*vs[c][1])
                   + vs[a][1]*(vs[b][2]*vs[c][0]-vs[b][0]*vs[c][2])
                   + vs[a][2]*(vs[b][0]*vs[c][1]-vs[b][1]*vs[c][0])
                   for a, b, c in ts)/6)


def main():
    result = {}
    folder = ROOT/'outputs/CM1000_M6_2026-10-28'
    for name in ['faceplate', 'rail_l', 'rail_r']:
        vs, ts, info = mesh_info(folder/f'CM6A_{name}.stl')
        info['volume'] = volume(vs, ts)
        stations = [0.1, 2, 3.9, 4.1, 5, 10, 12, 15.9] if name == 'faceplate' else [16.1, 20.1, 25, 30, 35, 40, 45, 50, 55, 60, 64.6, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 137.5]
        info['sections'] = [section(vs, ts, 1, y) for y in stations]
        result[name] = info
    for n in range(2, 16):
        vs, ts, info = mesh_info(folder/f'src/orig/fp_{n}_normal_part.stl')
        info['volume'] = volume(vs, ts)
        lo, hi = info['bounds']
        ys = [.0001, .1, .1999] if n >= 9 else [.0001, .1, .3999] if n < 4 else [.0001, .1, .3999, .5, 1, 2, 4, 6, 8, 8.7]
        info['sections'] = [section(vs, ts, 1, y) for y in ys if lo[1] < y < hi[1]]
        result[f'colour_{n}'] = info
    (HERE/'sections.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    for name, info in result.items():
        print(name, 'volume', round(info['volume'], 5), 'bounds', info['bounds'])
        print('  sections:', [(s['station'], [(len(p['points']), p['closed']) for p in s['loops']], len(s['bad_vertices'])) for s in info['sections']])


if __name__ == '__main__':
    main()
