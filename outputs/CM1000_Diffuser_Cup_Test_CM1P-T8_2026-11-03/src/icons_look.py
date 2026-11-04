"""Picture and numbers for the cup icons against the plate holes. Usage: python icons_look.py out.png"""
import json, sys, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point
from shapely.ops import unary_union
def parts(g): return list(g.geoms) if g.geom_type == 'MultiPolygon' else [g]
d = json.load(open('icons.json', encoding='utf-8'))
fig, ax = plt.subplots(1, 5, figsize=(15, 3.4))
for a, (n, v) in zip(ax, d.items()):
    cx = v['cx']; C = Point(cx, 30.225)
    icon = unary_union([Polygon(p['o'], p['h']) for p in v['icon']])
    hole = unary_union([Polygon(p['o'], p['h']) for p in v['hole']])
    mask = C.buffer(4.6, 64).difference(hole)
    print(v['name'], 'max r icon', round(max(C.distance(Point(c)) for g in parts(icon) for c in g.exterior.coords), 2),
          'max r hole', round(max(C.distance(Point(c)) for g in parts(hole) for c in g.exterior.coords), 2),
          'hole parts', len(parts(hole)), 'mask parts', [round(m.area, 2) for m in parts(mask)])
    for g, c in ((hole, '#333333'), (icon, 'c')):
        for q in parts(g):
            a.fill(*q.exterior.xy, color=c)
            for i in q.interiors: a.fill(*i.xy, color='w')
    a.add_patch(plt.Circle((cx, 30.225), 3.995, fill=False))
    a.set_aspect('equal'); a.set_title(v['name']); a.set_xlim(cx - 4.6, cx + 4.6); a.set_ylim(25.6, 34.8)
plt.savefig(sys.argv[1], dpi=90, bbox_inches='tight')
