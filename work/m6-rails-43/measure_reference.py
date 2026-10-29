"""Read-only STL evidence using triangle/axis-line intersections (Python standard library)."""
import collections
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from mesh_viewer import read_stl

def crossing_intervals(vertices, triangles, axis, point):
    """Material intervals on an infinite axis ray; avoid coincident boundary rays."""
    ij = [k for k in range(3) if k != axis]
    hits = []
    for tri in triangles:
        a, b, c = [vertices[i] for i in tri]
        i, j = ij
        det = (b[i]-a[i])*(c[j]-a[j])-(c[i]-a[i])*(b[j]-a[j])
        if abs(det) < 1e-12:
            continue
        u = ((point[i]-a[i])*(c[j]-a[j])-(c[i]-a[i])*(point[j]-a[j])) / det
        v = ((b[i]-a[i])*(point[j]-a[j])-(point[i]-a[i])*(b[j]-a[j])) / det
        if u >= -1e-9 and v >= -1e-9 and u+v <= 1+1e-9:
            hits.append(a[axis]+u*(b[axis]-a[axis])+v*(c[axis]-a[axis]))
    unique = []
    for v in sorted(hits):
        if not unique or abs(v-unique[-1]) > 1e-5:
            unique.append(v)
    return [[round(a,6),round(b,6)] for a,b in zip(unique[::2],unique[1::2])]

def mesh_info(path):
    vertices, triangles = read_stl(path)
    edges = collections.Counter(tuple(sorted((t[i],t[(i+1)%3]))) for t in triangles for i in range(3))
    neighbors = collections.defaultdict(set)
    for a,b in edges:
        neighbors[a].add(b)
        neighbors[b].add(a)
    remaining = set(neighbors)
    components = 0
    while remaining:
        components += 1
        todo = [remaining.pop()]
        while todo:
            fresh = neighbors[todo.pop()] & remaining
            remaining.difference_update(fresh)
            todo.extend(fresh)
    return vertices, triangles, dict(triangles=len(triangles), closed=set(edges.values())=={2},
        components=components, bounds=[[min(v[k] for v in vertices) for k in range(3)],
                                      [max(v[k] for v in vertices) for k in range(3)]])

def main():
    results = {}
    for name in ['faceplate','rail_l','rail_r']:
        path = ROOT / f'outputs/CM1000_M6_2026-10-28/CM6A_{name}.stl'
        vertices, triangles, info = mesh_info(path)
        probes = {}
        def probe(label,axis,p):
            probes[label] = dict(axis='XYZ'[axis],fixed=p,material_intervals=crossing_intervals(vertices,triangles,axis,p))
        x = 22.6 if name != 'rail_r' else 231.4
        for z in [8.6,35.85]:
            probe(f'hole-X-at-Z{z}',0,[0,12 if name=='faceplate' else 18,z])
            probe(f'hole-Z-at-Z{z}',2,[x,12 if name=='faceplate' else 18,0])
            probe(f'hole-Y-at-Z{z}',1,[x,0,z])
        if name!='faceplate':
            probe('bay-Z',2,[x,30,0])
            probe('bay-Y',1,[x,0,8.6])
            probe('wall-X-at-pocket-centre',0,[0,70,22.225])
        info['probes'] = probes
        results[name] = info
    target = Path(__file__).resolve().parent / 'cm6a-measurements.json'
    target.write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(results,indent=2))

if __name__=='__main__':
    main()
