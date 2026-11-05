"""Place the real Lab Rax post meshes around a slot, for clearance checks.

  python tools/rack_posts.py --u 3 --side right -o posts.stl

Frame (the same as the faceplate parts): X centred on the rack, Y=0 front face of the front posts,
Y=240 rear face of the rear posts, Z=0 bottom of slot U (counted from the bottom, 44.45 per U).
Brian's 9U rack: 4U post (U1-U4), 1U extension (U5), 4U post (U6-U9) on each corner.

Source: the creator's post meshes in work/rack-geometry-recovery/sources/ (licensed, local use only;
never release or redistribute the STLs this writes). Orientation was found from the mesh's holes and walls;
the front-left post is the front-right mirrored, and each rear post is the front post on the other side
turned 180 degrees about the rack centre. Rear posts and the U5 extension's holes are not checked on the rack.
"""
import argparse
import re
import zipfile
from pathlib import Path

import numpy as np
import manifold3d as m3

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work" / "rack-geometry-recovery" / "sources" / "Lab+Rax+1-5U+Posts+&+Panels.3mf"
PITCH = 44.45
DEPTH = 240.0
POST_4U, POST_1U = "190", "168"       # objects in SOURCE; local frame centred, X 30 wide, Y 35 deep
SEGMENTS = [(1, 4, POST_4U), (5, 1, POST_1U), (6, 4, POST_4U)]  # first U, height in U, object
RACK_U = 9


def _load(obj):
    text = zipfile.ZipFile(SOURCE).read(f"3D/Objects/object_{obj}.model").decode("utf-8")
    v = np.array(re.findall(r'<vertex x="([^"]+)" y="([^"]+)" z="([^"]+)"', text), dtype=np.float32)
    f = np.array(re.findall(r'<triangle v1="(\d+)" v2="(\d+)" v3="(\d+)"', text), dtype=np.uint32)
    return m3.Manifold(m3.Mesh(v, f))


def segment(u):
    for first, height, obj in SEGMENTS:
        if first <= u < first + height:
            return first, height, obj
    raise ValueError(f"U{u} is outside the {RACK_U}U rack")


def front_right(u):
    """Front-right post holding slot U, in the slot frame."""
    first, height, obj = segment(u)
    z_mid = (first - u) * PITCH + height * PITCH / 2   # post centre height above the slot bottom
    # local X -> rack X = 126.12 - x (flange edge at X 111.12), local Y -> Y = 17.5 + y (flange at Y 0..6)
    return _load(obj).transform([[-1, 0, 0, 126.12], [0, 1, 0, 17.5], [0, 0, 1, z_mid]])


def posts(u, side="both"):
    """[(name, Manifold)] for the posts on the chosen side(s) of slot U."""
    fr = front_right(u)
    fl = fr.mirror([1, 0, 0])
    turn = lambda m: m.rotate([0, 0, 180]).translate([0, DEPTH, 0])
    found = {"front_right": fr, "rear_right": turn(fl), "front_left": fl, "rear_left": turn(fr)}
    keep = {"right": ("front_right", "rear_right"), "left": ("front_left", "rear_left"),
            "both": tuple(found)}[side]
    return [(f"post_{k}_U{u}", found[k]) for k in keep]


def write_stl(solid, path):
    mesh = solid.to_mesh()
    v, f = np.asarray(mesh.vert_properties)[:, :3], np.asarray(mesh.tri_verts)
    with open(path, "w", encoding="utf-8") as out:
        out.write("solid posts\n")
        for a, b, c in v[f]:
            n = np.cross(b - a, c - a)
            n = n / (np.linalg.norm(n) or 1)
            out.write(f"facet normal {n[0]:.6g} {n[1]:.6g} {n[2]:.6g}\n outer loop\n")
            for p in (a, b, c):
                out.write(f"  vertex {p[0]:.6f} {p[1]:.6f} {p[2]:.6f}\n")
            out.write(" endloop\nendfacet\n")
        out.write("endsolid posts\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--u", type=int, required=True, help="slot U, counted from the bottom")
    ap.add_argument("--side", choices=("right", "left", "both"), default="both")
    ap.add_argument("-o", "--out", type=Path, required=True)
    args = ap.parse_args(argv)
    solids = [s for _, s in posts(args.u, args.side)]
    total = solids[0]
    for s in solids[1:]:
        total = total + s
    write_stl(total, args.out)
    print(f"{len(solids)} posts around U{args.u} ({args.side}) written to {args.out}; local use only")


if __name__ == "__main__":
    main()
