"""Icon outlines from the baseline pipes: cup keeps the icon, trimmed to R 3.88 so it passes the 7.99 bore; plate hole opens 0.1 per side around that, and never less than the baseline's own hole. Writes icons.json for FreeCAD; prints the thinnest strokes and plate gaps."""
import json, trimesh, numpy as np
from trimesh import intersections
from shapely.geometry import LineString, Polygon, MultiPolygon
from shapely.ops import polygonize, unary_union
orig = '../../CM1000_M6_2026-10-28/src/orig/'
CX = {4: 104.0, 8: 115.5, 7: 127.0, 6: 138.5, 5: 150.0}
NAMES = {4: 'network', 8: 'internet', 7: 'upstream', 6: 'downstream', 5: 'power'}
PLAY = 0.10
def as_list(g): return list(g.geoms) if isinstance(g, MultiPolygon) else [g]
def min_width(g, step=0.02):
    # smallest r whose opening (shrink r/2, grow r/2) removes more than 1% of the area
    a = g.area; r = step
    while r < 3:
        if g.buffer(-r / 2).buffer(r / 2).area < a * 0.97: return r
        r += step
    return r
out = {}
for n, cx in CX.items():
    m = trimesh.load(orig + 'fp_%d_normal_part.stl' % n)
    l = intersections.mesh_plane(m, plane_normal=[0, 1, 0], plane_origin=[0, 0.2, 0])
    segs = [LineString(np.round(s[:, [0, 2]], 3)) for s in l if np.abs(s[0] - s[1]).sum() > 1e-4]
    polys = sorted(polygonize(unary_union(segs)), key=lambda p: -p.area)
    tops = [p for i, p in enumerate(polys) if not any(q.contains(p.representative_point()) for q in polys[:i])]
    print(NAMES[n], 'pieces', len(tops), 'all polys', len(polys), 'areas', [round(p.area, 2) for p in tops])
    disc = Polygon([(cx + 3.995 * np.cos(t), 30.225 + 3.995 * np.sin(t)) for t in np.linspace(0, 2 * np.pi, 90)])
    full = unary_union([Polygon(p.exterior) for p in tops])
    trim = Polygon([(cx + 3.88 * np.cos(t), 30.225 + 3.88 * np.sin(t)) for t in np.linspace(0, 2 * np.pi, 120)])
    icon = full.intersection(trim).simplify(0.01)
    hole = icon.buffer(PLAY, join_style=1, resolution=4).simplify(0.01)
    print('   stroke min', round(min_width(icon), 2), 'skin strip min (between hole parts)', round(min_width(disc.difference(hole)), 2), 'hole inside disc', disc.buffer(0.01).contains(hole))
    out[n] = {'name': NAMES[n], 'cx': cx,
              'icon': [{'o': list(p.exterior.coords), 'h': [list(i.coords) for i in p.interiors]} for p in as_list(icon)],
              'hole': [{'o': list(p.exterior.coords), 'h': [list(i.coords) for i in p.interiors]} for p in as_list(hole)]}
json.dump(out, open('icons.json', 'w', encoding='utf-8'))
