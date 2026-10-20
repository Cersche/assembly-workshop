"""One-off: convert the supplied Lab Rax Cable Guide 3MF object to the rack-references {vertices, triangles} JSON.

Usage: python -I convert_guide.py <extracted object_1.model> <output cable_guide.json>
Vertices and triangle indices are copied exactly; nothing is rescaled or repaired.
"""
import json
import re
import sys

src = open(sys.argv[1], encoding='utf-8').read()
vertices = [[float(x), float(y), float(z)] for x, y, z in re.findall(r'<vertex x="([^"]+)" y="([^"]+)" z="([^"]+)"', src)]
triangles = [[int(a), int(b), int(c)] for a, b, c in re.findall(r'<triangle v1="(\d+)" v2="(\d+)" v3="(\d+)"', src)]
assert len(vertices) == 352 and len(triangles) == 708, (len(vertices), len(triangles))
assert all(0 <= i < len(vertices) for t in triangles for i in t)
with open(sys.argv[2], 'x', encoding='utf-8') as out:
    json.dump({'vertices': vertices, 'triangles': triangles}, out, separators=(',', ':'))
print('wrote', len(vertices), 'vertices', len(triangles), 'triangles')
