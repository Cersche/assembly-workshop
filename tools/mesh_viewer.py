"""Write a standalone HTML 3D viewer for STL / 3MF print parts.

Preview only: reads meshes, never changes them. The page has its own small
WebGL renderer (no CDN, works offline and in the Claude app side panel).

    python tools/mesh_viewer.py part.3mf other.stl -o work/mesh-viewer/view.html

Each 3MF object becomes its own part, placed by its build-item transform.
Several STL files are laid side by side on the bed unless --as-is is given.
Vertex positions are quantized to 16 bits per axis over each part's bounding
box (about 0.003 mm on a 200 mm part).
"""
import argparse
import base64
import html
import json
import re
import struct
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

NS = "{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}"
PNS = "{http://schemas.microsoft.com/3dmanufacturing/production/2015/06}"
GAP = 10.0  # mm between STL parts when laid out side by side


def read_stl(path):
    """Return (vertices, triangles) from an ASCII or binary STL."""
    data = Path(path).read_bytes()
    n = struct.unpack_from("<I", data, 80)[0] if len(data) >= 84 else -1
    if len(data) == 84 + 50 * n:
        coords = []
        for i in range(n):
            coords.append(struct.unpack_from("<9f", data, 84 + 50 * i + 12))
    else:
        nums = [float(v) for t in re.findall(rb"vertex\s+(\S+)\s+(\S+)\s+(\S+)", data) for v in t]
        coords = [nums[i:i + 9] for i in range(0, len(nums) - 8, 9)]
    verts, tris, index = [], [], {}
    for c in coords:
        tri = []
        for k in range(0, 9, 3):
            p = (c[k], c[k + 1], c[k + 2])
            if p not in index:
                index[p] = len(verts)
                verts.append(p)
            tri.append(index[p])
        tris.append(tri)
    return verts, tris


def parse_transform(text):
    if not text:
        return None
    m = [float(v) for v in text.split()]
    return m if len(m) == 12 else None


def apply(m, verts):
    if m is None:
        return list(verts)
    return [(x * m[0] + y * m[3] + z * m[6] + m[9],
             x * m[1] + y * m[4] + z * m[7] + m[10],
             x * m[2] + y * m[5] + z * m[8] + m[11]) for x, y, z in verts]


def compose(a, b):
    """Transform a then b (3MF row-vector 3x4 matrices)."""
    if a is None:
        return b
    if b is None:
        return a
    r = []
    for i in range(3):
        for j in range(3):
            r.append(sum(a[i * 3 + k] * b[k * 3 + j] for k in range(3)))
    for j in range(3):
        r.append(sum(a[9 + k] * b[k * 3 + j] for k in range(3)) + b[9 + j])
    return r


def read_3mf(path):
    """Return [(name, vertices, triangles)], one per build item."""
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        model = next((n for n in names if n.lower() == "3d/3dmodel.model"), None)
        if model is None:
            raise ValueError(f"{path}: no 3D/3dmodel.model")
        root = ET.fromstring(z.read(model))
        # Objects are keyed by (model part, id): Bambu/Prusa 3MFs keep meshes in
        # 3D/Objects/*.model and point at them with the production p:path attribute.
        main = "/" + model
        trees = {main: root}
        for n in names:
            if n.lower().startswith("3d/") and n.lower().endswith(".model") and n != model:
                trees["/" + n] = ET.fromstring(z.read(n))
    objects = {}
    for part, tree in trees.items():
        for obj in tree.iter(NS + "object"):
            mesh = obj.find(NS + "mesh")
            entry = {"name": obj.get("name") or f"object {obj.get('id')}", "verts": [], "tris": [], "comps": []}
            if mesh is not None:
                entry["verts"] = [(float(v.get("x")), float(v.get("y")), float(v.get("z")))
                                  for v in mesh.iter(NS + "vertex")]
                entry["tris"] = [(int(t.get("v1")), int(t.get("v2")), int(t.get("v3")))
                                 for t in mesh.iter(NS + "triangle")]
            for c in obj.iter(NS + "component"):
                ref = c.get(PNS + "path") or part
                entry["comps"].append(((ref, c.get("objectid")), parse_transform(c.get("transform"))))
            objects[(part, obj.get("id"))] = entry

    def flatten(oid, m, depth=0):
        o = objects[oid]
        verts, tris = apply(m, o["verts"]), [tuple(t) for t in o["tris"]]
        if depth < 16:
            for cid, cm in o["comps"]:
                v2, t2 = flatten(cid, compose(cm, m), depth + 1)
                base = len(verts)
                verts += v2
                tris += [(a + base, b + base, c + base) for a, b, c in t2]
        return verts, tris

    parts = []
    build = root.find(NS + "build")
    items = list(build.iter(NS + "item")) if build is not None else []
    if not items:
        items = [ET.Element("item", objectid=k[1]) for k in objects if k[0] == main]
    for it in items:
        oid = (main, it.get("objectid"))
        verts, tris = flatten(oid, parse_transform(it.get("transform")))
        if tris:
            parts.append((objects[oid]["name"], verts, tris))
    return parts


def bounds(verts):
    lo = [min(v[i] for v in verts) for i in range(3)]
    hi = [max(v[i] for v in verts) for i in range(3)]
    return lo, hi


def encode(name, verts, tris, source):
    lo, hi = bounds(verts)
    span = [max(hi[i] - lo[i], 1e-9) for i in range(3)]
    q = bytearray()
    for v in verts:
        q += struct.pack("<3H", *(round((v[i] - lo[i]) / span[i] * 65535) for i in range(3)))
    fmt = "H" if len(verts) < 65536 else "I"
    idx = struct.pack(f"<{3 * len(tris)}{fmt}", *(i for t in tris for i in t))
    return {
        "name": name, "source": source, "lo": lo, "span": span, "tris": len(tris),
        "idx32": fmt == "I",
        "pos": base64.b64encode(bytes(q)).decode("ascii"),
        "idx": base64.b64encode(idx).decode("ascii"),
    }


def load_parts(paths, as_is):
    parts = []
    stl_x = None
    for p in paths:
        p = Path(p)
        if p.suffix.lower() == ".3mf":
            for name, verts, tris in read_3mf(p):
                parts.append(encode(name, verts, tris, p.name))
        elif p.suffix.lower() == ".stl":
            verts, tris = read_stl(p)
            if not tris:
                raise ValueError(f"{p}: no triangles")
            if not as_is and len(paths) > 1:
                lo, hi = bounds(verts)
                stl_x = 0.0 if stl_x is None else stl_x
                d = (stl_x - lo[0], -lo[1], -lo[2])
                verts = [(x + d[0], y + d[1], z + d[2]) for x, y, z in verts]
                stl_x += hi[0] - lo[0] + GAP
            parts.append(encode(p.stem, verts, tris, p.name))
        else:
            raise ValueError(f"{p}: only .stl and .3mf are supported")
    return parts


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("files", nargs="+", help="STL or 3MF files")
    ap.add_argument("-o", "--out", required=True, help="output .html")
    ap.add_argument("-t", "--title", help="page title (default: first file name)")
    ap.add_argument("--as-is", action="store_true", help="keep STL coordinates, no side-by-side layout")
    a = ap.parse_args(argv)
    parts = load_parts(a.files, a.as_is)
    title = a.title or Path(a.files[0]).stem
    template = (Path(__file__).with_name("mesh_viewer_template.html")).read_text(encoding="utf-8")
    page = (template.replace("__TITLE__", html.escape(title))
            .replace("__DATA__", json.dumps(parts, separators=(",", ":")).replace("</", "<\\/")))
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    total = sum(p["tris"] for p in parts)
    print(f"{out}: {len(parts)} parts, {total} triangles, {out.stat().st_size / 1e6:.2f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
