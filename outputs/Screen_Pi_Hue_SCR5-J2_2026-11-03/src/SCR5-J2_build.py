"""SCR5-J2: render parts and references, mesh checks, clash pairs by ray parity on a 0.25 mm grid. Needs OpenSCAD, trimesh, numpy and the local Hue cradle."""
import concurrent.futures as cf, json, subprocess
from pathlib import Path
import numpy as np, trimesh
HERE = Path(__file__).resolve().parent.parent; C = HERE / 'checks'; C.mkdir(exist_ok=True)
import importlib.util
sp = importlib.util.spec_from_file_location('g', HERE / 'src/build_check.py'); g = importlib.util.module_from_spec(sp); sp.loader.exec_module(g)
REPO = HERE.parent.parent; EXE = r'C:\Program Files\OpenSCAD\openscad.exe'; SCAD = HERE / 'src/SCR5-J2.scad'; G = 0.25
PARTS = ['plate', 'frame', 'deck', 'fanmount']
REFS = 'screen pi pi_screws pi_drivers ribbon fan hue jacks plugs cables m6_heads m6_tools sd_path usbc pi_plugs pins hue_pose0 hue_pose1 hue_pose2 hue_pose3 hue_pose4'.split()
def build(a):
    n, dst, extra = a
    r = subprocess.run([EXE, '--export-format', 'binstl', '-D', f'part="{n}"', *extra, '-o', str(dst), str(SCAD)], capture_output=True, text=True, encoding='utf-8')
    if r.returncode or 'ERROR:' in r.stderr: raise RuntimeError(n + r.stderr[-600:])
    if n in PARTS and dst.parent == HERE: g.repair_collinear(dst)
    return n
jobs = [(p, HERE / f'SCR5-J2_{p}.stl', []) for p in PARTS] + [(p, C / f'ref_{p}.stl', []) for p in REFS] + [('deck', C / 'ref_deck_no_cradle.stl', ['-D', 'cradle_on=false'])]
with cf.ThreadPoolExecutor(6) as x: list(x.map(build, jobs))
def path(n):
    return HERE / f'SCR5-J2_{n}.stl' if n in PARTS else C / f'ref_{n}.stl'
def load(n):
    if n in ('post_l', 'post_r'):
        m = trimesh.load(REPO / f'work/rack-post-hex/assembled/{"post_left" if n == "post_l" else "post_right"}.stl'); m.apply_translation([0, 4, 0]); return m
    return trimesh.load(path(n))
def shells(m):
    par = list(range(len(m.vertices)))
    def find(i):
        while par[i] != i:
            par[i] = par[par[i]]; i = par[i]
        return i
    for a, b in m.edges_unique: par[find(a)] = find(b)
    return len({find(i) for f in m.faces for i in f})
meshes = {}
for p in PARTS:
    m = trimesh.load(path(p))
    e = m.edges_sorted; _, cnt = np.unique(e, axis=0, return_counts=True)
    meshes[p] = dict(shells=shells(m), watertight=bool(m.is_watertight), bad_edges=int((cnt != 2).sum()), degenerate=int((m.area_faces < 1e-10).sum()), grams_solid=round(abs(m.volume) * 1.24e-3, 1), bounds=m.bounds.round(2).tolist())
    print(p, meshes[p])
json.dump(meshes, open(C / 'meshes.json', 'w', encoding='utf-8'), indent=1)
def columns(m):
    out = {}
    for t in m.triangles:
        x, y, z = t.T
        i0, i1 = int(np.ceil(x.min() / G)), int(np.floor(x.max() / G)); k0, k1 = int(np.ceil(z.min() / G)), int(np.floor(z.max() / G))
        d = (x[1] - x[0]) * (z[2] - z[0]) - (x[2] - x[0]) * (z[1] - z[0])
        if abs(d) < 1e-12: continue
        for i in range(i0, i1 + 1):
            for k in range(k0, k1 + 1):
                px, pz = i * G + 1.37e-4, k * G + 2.11e-4
                u = ((px - x[0]) * (z[2] - z[0]) - (x[2] - x[0]) * (pz - z[0])) / d
                v = ((x[1] - x[0]) * (pz - z[0]) - (px - x[0]) * (z[1] - z[0])) / d
                if u >= 0 and v >= 0 and u + v <= 1: out.setdefault((i, k), []).append(y[0] + u * (y[1] - y[0]) + v * (y[2] - y[0]))
    return {c: sorted(q) for c, q in out.items() if len(q) % 2 == 0}
cache = {}
def col(n):
    if n not in cache: cache[n] = columns(load(n))
    return cache[n]
def overlap(a, b):
    v = 0.0; lo = hi = None
    for c in col(a).keys() & col(b).keys():
        A, B = col(a)[c], col(b)[c]
        for i in range(0, len(A), 2):
            for j in range(0, len(B), 2):
                s, e = max(A[i], B[j]), min(A[i + 1], B[j + 1])
                if e - s > 1e-3:
                    v += (e - s) * G * G; p = np.array([c[0] * G, s, c[1] * G]); q = np.array([c[0] * G, e, c[1] * G])
                    lo = p if lo is None else np.minimum(lo, p); hi = q if hi is None else np.maximum(hi, q)
    return v, lo, hi
BUILT = ['plate', 'frame', 'deck', 'fanmount']
OTHER = ['screen', 'pi', 'pi_screws', 'ribbon', 'fan', 'hue', 'jacks', 'plugs', 'cables', 'm6_heads', 'usbc', 'pi_plugs', 'pins', 'post_l', 'post_r']
PAIRS = [(a, b) for i, a in enumerate(BUILT) for b in BUILT[i + 1:]] + [(a, b) for a in BUILT for b in OTHER]
PAIRS += [('pi', x) for x in ('ribbon', 'hue', 'fan', 'jacks', 'pins')] + [('hue', x) for x in ('jacks', 'plugs', 'cables', 'ribbon', 'fan', 'usbc')] + [('pi_plugs', 'post_r'), ('pi_plugs', 'fan'), ('screen', 'pi'), ('screen', 'post_r')]
# Tool paths: the Hue is expected to block only the listed ones.
PAIRS += [('m6_tools', x) for x in ('deck', 'hue', 'jacks', 'plugs', 'cables', 'fan', 'fanmount')] + [('pi_drivers', x) for x in ('fan', 'fanmount', 'frame', 'hue', 'deck')] + [('sd_path', x) for x in ('deck', 'hue', 'ribbon', 'fanmount', 'fan')]
# Hue removal, 5 still positions (POSE in the SCAD). Pose 0 still sits between the cradle posts.
PAIRS += [(f'hue_pose{i}', x) for i in range(5) for x in ('deck', 'plate', 'jacks', 'plugs', 'cables', 'ribbon', 'frame')]
rows = []
for a, b in PAIRS:
    ma, mb = load(a), load(b)
    if (np.minimum(ma.bounds[1], mb.bounds[1]) <= np.maximum(ma.bounds[0], mb.bounds[0])).any():
        rows.append(dict(a=a, b=b, mm3=0.0)); continue
    v, lo, hi = overlap(a, b); r = dict(a=a, b=b, mm3=round(v, 1))
    if v > 0:
        r['from'] = lo.round(1).tolist(); r['to'] = hi.round(1).tolist(); print(' ', a, b, r['mm3'], r['from'], r['to'])
    rows.append(r)
json.dump(rows, open(C / 'pairwise.json', 'w', encoding='utf-8'), indent=0)
print(len(rows), 'pairs')
