"""Render, check and package a new part in one command.

  python tools/release_part.py work/x/ABC-A.scad --id ABC-A --part tray --part plate:ABC-A-P \
      -o outputs/ABC_2026-11-05 [--against device.stl] [--min-gap 0.5] [--bodies tray=2]
      [--posts 3:right] [--cuts cuts=6] [--keepout keepout]

Renders each part on the pinned OpenSCAD snapshot, checks it, then writes one new folder:
  <ID>_<part>.stl, <ID>_<N>-parts-print-layout.3mf, src/ (frozen source), release_report.md
plus the viewer page work/mesh-viewer/<ID>.html.

A FAIL writes nothing into outputs/ and exits 1. An existing output folder is never overwritten.
WARNs are printed and kept in the report. Digital checks only: printed fit and strength stay UNKNOWN.
"""
import argparse
import datetime
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

import numpy as np
import manifold3d as m3
import trimesh

import rack_posts

# abspath, not resolve(): resolve turns the mapped R:\ share into a UNC path, which OpenSCAD cannot open.
ROOT = Path(os.path.abspath(__file__)).parents[1]
LIB = ROOT / "lib"
# AW_OPENSCAD_SNAPSHOT overrides the path on machines where tools/setup_3d_tools.ps1 used another folder.
# Default: R:\Tools (rack share, 2026-11-12), else the older D:\Tools.
_SNAP_REL = r"Tools\OpenSCAD-snapshot\OpenSCAD-2026.11.01-x86-64\openscad.exe"
SNAPSHOT = Path(os.environ.get("AW_OPENSCAD_SNAPSHOT")
                or next((d + _SNAP_REL for d in ("R:\\", "D:\\") if os.path.exists(d + _SNAP_REL)), "R:\\" + _SNAP_REL))
# name, design bore, minimum depth (Brian's fastener standard, 2026-10-31)
INSERTS = [("M6 insert", 7.6, 6.0), ("M3 insert", 4.2, 4.0), ("M2.5 insert", 3.2, 5.0)]
NEAR = 0.15       # a hole this close to a standard bore, but not on it, gets a warning
ON_SIZE = 0.03    # polygon and float tolerance for "on" a standard bore
STEP = 0.25       # hole scan spacing, mm
LAYOUT_GAP = 10.0
QUOTE = {'"': "&quot;"}
OVERLAP_LIMIT = 0.01  # mm3; smaller overlaps are numerical noise from touching faces


class Report:
    def __init__(self):
        self.lines, self.fails, self.warns = [], [], []

    def info(self, text):
        self.lines.append(f"- {text}")

    def warn(self, text):
        self.warns.append(text)
        self.lines.append(f"- WARN: {text}")

    def fail(self, text):
        self.fails.append(text)
        self.lines.append(f"- FAIL: {text}")

    def heading(self, text):
        self.lines.append(f"\n## {text}")


def load_manifold(path):
    mesh = trimesh.load(str(path), force="mesh")
    mesh.merge_vertices()
    solid = m3.Manifold(m3.Mesh(np.asarray(mesh.vertices, dtype=np.float32),
                                np.asarray(mesh.faces, dtype=np.uint32)))
    return mesh, solid


def render(openscad, scad, part, out, deps, rep):
    run = subprocess.run([str(openscad), "--backend=manifold", "-o", str(out), "-d", str(deps),
                          "-D", f'part="{part}"', str(scad)],
                         capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(scad.parent),
                         env={**os.environ, "OPENSCADPATH": str(LIB)})
    log = run.stdout + run.stderr
    # These are only warnings in OpenSCAD, but the part can silently lose geometry.
    fatal = ("Ignoring unknown module", "Ignoring unknown variable", "Ignoring unknown function",
             "Can't open", "Can't read", "import() failed")
    errors = sorted({l.strip() for l in log.splitlines()
                     if l.startswith("ERROR") or (l.startswith("WARNING") and any(f in l for f in fatal))})
    warnings = sorted({l.strip() for l in log.splitlines()
                       if l.startswith("WARNING") and "was assigned on line" not in l and not any(f in l for f in fatal)})
    for line in errors:
        rep.fail(f"{part}: OpenSCAD: {line[:200]}")
    for line in warnings[:10]:
        rep.warn(f"{part}: OpenSCAD: {line[:200]}")
    if len(warnings) > 10:
        rep.warn(f"{part}: {len(warnings) - 10} more OpenSCAD warnings not shown")
    if run.returncode or not out.exists() or out.stat().st_size == 0:
        rep.fail(f"{part}: nothing rendered (exit {run.returncode}); is the part name right?")
        return False
    return True


def check_id_on_mesh(openscad, scad, part, part_id, solid, stage, rep):
    """Render the part again with its ID text blanked; the ID is on the mesh only if the geometry changes."""
    token = f'"{part_id}"'
    text = scad.read_text(encoding="utf-8", errors="replace")
    if token not in text:
        rep.warn(f"{part}: ID {part_id} is set in an included file, so its mesh check did not run; check it in the viewer")
        return
    blank = scad.parent / f".idcheck_{part}_{os.getpid()}.scad"
    out = stage / f"idcheck_{part}.stl"
    try:
        blank.write_text(text.replace(token, '""'), encoding="utf-8")
        ok = render(openscad, blank, part, out, stage / f"idcheck_{part}.deps", Report())
    finally:
        blank.unlink(missing_ok=True)
    if not ok:
        rep.warn(f"{part}: the part did not render with its ID blanked, so the ID mesh check did not run")
        return
    _, without = load_manifold(out)
    changed = (solid - without) + (without - solid)
    volume = changed.volume()
    if volume <= OVERLAP_LIMIT:
        rep.fail(f"{part}: ID {part_id} is in the source but not on this part's mesh")
        return
    box = changed.bounding_box()
    lo, hi = box[:3], box[3:]
    rep.info(f"{part}: ID {part_id} is on the mesh, {volume:.1f} mm3 of text at X {lo[0]:.1f}..{hi[0]:.1f}, "
             f"Y {lo[1]:.1f}..{hi[1]:.1f}, Z {lo[2]:.1f}..{hi[2]:.1f}; legibility not checked")


def check_cuts(openscad, scad, part, wanted, stage, rep):
    """A check-only part holding each opening as a solid: openings that run together merge into one body."""
    out = stage / f"cuts_{part}.stl"
    if not render(openscad, scad, part, out, stage / f"cuts_{part}.deps", rep):
        return
    _, cuts = load_manifold(out)
    if cuts.status().name != "NoError" or cuts.volume() <= 0:
        rep.fail(f"cuts {part} is not a closed solid; cuts not checked")
        return
    bodies = cuts.decompose()
    if len(bodies) == wanted:
        rep.info(f"cuts {part}: {wanted} separate openings, none run together")
        return
    rep.fail(f"cuts {part}: {len(bodies)} separate openings, expected {wanted}"
             + ("; some run into each other" if len(bodies) < wanted else ""))
    for body in sorted(bodies, key=lambda b: -b.volume())[:3]:
        lo, hi = body.bounding_box()[:3], body.bounding_box()[3:]
        rep.info(f"cuts {part}: largest opening X {lo[0]:.1f}..{hi[0]:.1f}, Y {lo[1]:.1f}..{hi[1]:.1f}, "
                 f"Z {lo[2]:.1f}..{hi[2]:.1f}")


def read_deps(depfile, scad):
    """Parse OpenSCAD's make-style dependency file into source file paths."""
    text = depfile.read_text(encoding="utf-8", errors="replace").replace("\\\n", " ").replace("\\\r\n", " ")
    _, _, body = text.partition(": ")
    tokens = re.findall(r"(?:\\ |\S)+", body)
    found = {Path(os.path.abspath(t.replace("\\ ", " "))) for t in tokens}
    found.add(Path(os.path.abspath(scad)))
    return sorted(found)


def find_holes(solid):
    """Find round holes along X, Y and Z by slicing. Only sees holes fully surrounded in the slice plane."""
    rotations = {"Z": ((0, 0, 0), 2), "X": ((0, -90, 0), 0), "Y": ((90, 0, 0), 1)}
    holes = []
    for axis, (rot, index) in rotations.items():
        turned = solid.rotate(list(rot))
        box = turned.bounding_box()
        rings = []
        for h in np.arange(box[2] + STEP / 2, box[5], STEP):
            for contour in turned.slice(float(h) + 0.00137).to_polygons():
                p = np.asarray(contour)
                if len(p) < 6:
                    continue
                x, y = p[:, 0], p[:, 1]
                if 0.5 * np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y) >= 0:
                    continue  # outer contour, not a hole
                c = p.mean(axis=0)
                r = np.hypot(*(p - c).T)
                # Vertices can lie on facet flats, so compare against the largest radius.
                if r.max() < 0.75 or r.max() > 15 or r.min() / r.max() < 0.93:
                    continue
                rings.append((float(h), c, 2 * float(r.max())))
        clusters = []
        for h, c, d in rings:
            for g in clusters:
                if abs(g["d"] - d) < 0.06 and np.hypot(*(g["c"] - c)) < 0.15 and h - g["top"] < 2 * STEP:
                    g["top"] = h
                    break
            else:
                clusters.append({"d": d, "c": c, "bottom": h, "top": h})
        for g in clusters:
            holes.append({"axis": axis, "d": round(g["d"], 2), "depth": round(g["top"] - g["bottom"] + STEP, 2)})
    holes.sort(key=lambda g: (-g["d"], g["axis"]))
    return holes


def check_holes(part, holes, rep):
    if not holes:
        rep.info(f"{part}: no round holes found by the scan")
        return
    grouped = {}
    for g in holes:
        grouped.setdefault(g["d"], []).append(g)
    for d, group in grouped.items():
        depths = sorted({g["depth"] for g in group})
        rep.info(f"{part}: {len(group)} x dia {d} ({'/'.join(sorted({g['axis'] for g in group}))}), "
                 f"depth about {depths[0]}" + (f" to {depths[-1]}" if len(depths) > 1 else ""))
        for name, bore, minimum in INSERTS:
            if abs(d - bore) <= ON_SIZE:
                short = [g for g in group if g["depth"] < minimum - STEP]
                if short:
                    rep.warn(f"{part}: {len(short)} {name} bore(s) dia {d} look shallower than {minimum} mm "
                             f"(about {short[0]['depth']}); confirm this is not a bore")
            elif abs(d - bore) <= NEAR:
                rep.warn(f"{part}: dia {d} is close to the {name} bore {bore} but not on it")


def check_clearance(part, solid, devices, min_gap, rep):
    for path, device in devices:
        overlap = (solid ^ device).volume()
        name = path.name
        if overlap > OVERLAP_LIMIT:
            rep.fail(f"{part}: overlaps {name} by {overlap:.3f} mm3")
            continue
        search = max(min_gap + 1, 10.0)
        gap = solid.min_gap(device, search)
        shown = f"{gap:.2f} mm" if gap < search else f"over {search:.0f} mm"
        if gap < min_gap:
            rep.fail(f"{part}: only {shown} from {name}; needs {min_gap} mm")
        else:
            rep.info(f"{part}: no overlap with {name}; nearest gap {shown}")


def check_3mf(path, expected, rep):
    """The slicer reads the 3MF itself, so count its plain tags. Viewers read the STLs and miss a broken file."""
    try:
        with zipfile.ZipFile(path) as z:
            xml = z.read("3D/3dmodel.model").decode("utf-8")
    except (OSError, KeyError, zipfile.BadZipFile) as e:
        rep.fail(f"3MF unreadable: {e}")
        return
    tri, obj, item, vert = (len(re.findall(rf"<{t}[\s/>]", xml)) for t in ("triangle", "object", "item", "vertex"))
    if re.search(r"<\w+:(vertex|triangle|item|object)\b", xml):
        rep.fail("3MF uses prefixed tags such as ns0:vertex; slicers read these as no geometry")
    if vert == 0 or tri != sum(expected.values()) or obj != len(expected) or item != len(expected):
        rep.fail(f"3MF contents wrong: {obj} objects, {item} items, {vert} vertices, {tri} triangles; "
                 f"expected {len(expected)} objects and {sum(expected.values())} triangles")
    else:
        rep.info(f"3MF: {obj} objects, {item} items, {vert} vertices, {tri} triangles, matching the STLs")


def write_3mf(path, parts):
    """One object per part, flat on Z=0, 10 mm apart along Y. parts: (name, stl path, turn such as x90 or None).
    Any part name works, unlike the app's print_layout, which drops names it doesn't know."""
    objects, items, next_y = [], [], None
    for i, (name, stl, turn) in enumerate(parts, 1):
        mesh = trimesh.load(str(stl), force="mesh")
        mesh.merge_vertices()
        if turn:
            axis = {"x": [1, 0, 0], "y": [0, 1, 0], "z": [0, 0, 1]}[turn[0]]
            mesh.apply_transform(trimesh.transformations.rotation_matrix(np.radians(float(turn[1:])), axis))
        lo, hi = mesh.bounds
        dy = 0.0 if next_y is None else next_y - lo[1]
        mesh.apply_translation([0.0, dy, -lo[2]])
        next_y = hi[1] + dy + LAYOUT_GAP
        vertices = "".join(f'<vertex x="{x:.5f}" y="{y:.5f}" z="{z:.5f}"/>' for x, y, z in mesh.vertices)
        faces = "".join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in mesh.faces)
        objects.append(f'<object id="{i}" name="{escape(name, QUOTE)}" type="model"><mesh><vertices>{vertices}</vertices>'
                       f"<triangles>{faces}</triangles></mesh></object>")
        items.append(f'<item objectid="{i}"/>')
    model = ('<?xml version="1.0" encoding="UTF-8"?><model unit="millimeter" '
             'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
             f'<resources>{"".join(objects)}</resources><build>{"".join(items)}</build></model>')
    types = ('<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
             '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
             '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Target="/3D/3dmodel.model" Id="rel0" '
            'Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", types)
        z.writestr("_rels/.rels", rels)
        z.writestr("3D/3dmodel.model", model)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("scad", type=Path)
    ap.add_argument("--id", required=True, help="revision ID, used in file names")
    ap.add_argument("--part", action="append", required=True, metavar="NAME[:ID]",
                    help='value of the SCAD "part" variable, repeatable; :ID is the text modeled on it (default --id)')
    ap.add_argument("-o", "--out", required=True, type=Path, help="new output folder; must not exist")
    ap.add_argument("--against", action="append", default=[], type=Path, metavar="STL",
                    help="device mesh in the same coordinates as the rendered parts")
    ap.add_argument("--min-gap", type=float, default=0.0, help="smallest allowed gap to --against meshes, mm")
    ap.add_argument("--bodies", action="append", default=[], metavar="PART=N", help="expected body count (default 1)")
    ap.add_argument("--turn", action="append", default=[], metavar="PART=AXISDEG",
                    help="print orientation in the 3MF, such as tray=x180 (a part named faceplate defaults to x90)")
    ap.add_argument("--keepout", metavar="PART", help='SCAD part holding solids no released part may overlap, such as screw head room')
    ap.add_argument("--posts", action="append", default=[], metavar="U:SIDE",
                    help="check against the real rack posts around slot U (from the bottom), side right, left or both")
    ap.add_argument("--cuts", action="append", default=[], metavar="PART=N",
                    help="check-only SCAD part holding each opening as a solid; fails unless it has N separate bodies")
    ap.add_argument("--openscad", type=Path, default=SNAPSHOT)
    ap.add_argument("--viewer-dir", type=Path, default=ROOT / "work" / "mesh-viewer")
    args = ap.parse_args(argv)

    scad = Path(os.path.abspath(args.scad))
    out = Path(os.path.abspath(args.out))
    if out.exists():
        sys.exit(f"Refusing to overwrite {out}: revisions are immutable, use a new folder.")
    if not scad.is_file():
        sys.exit(f"No such file: {scad}")
    if not args.openscad.is_file():
        sys.exit(f"OpenSCAD not found: {args.openscad}")

    parts = [(p.partition(":")[0], p.partition(":")[2] or args.id) for p in args.part]
    expected_bodies = {k: int(v) for k, v in (b.split("=", 1) for b in args.bodies)}
    turns = {k: v for k, v in (t.split("=", 1) for t in args.turn)}
    for part, turn in turns.items():
        if not re.fullmatch(r"[xyz]-?\d+(\.\d+)?", turn):
            sys.exit(f"Bad --turn for {part}: {turn}; use a form like x90")
    rep = Report()
    rep.lines.append(f"# {args.id} release report\n")
    rep.info(f"Date {datetime.date.today().isoformat()}; source `{scad.name}`; renderer `{args.openscad.parent.name}` with Manifold")

    devices = []
    for path in args.against:
        try:
            _, device = load_manifold(path)
        except Exception as e:  # a clash check that didn't run must never read as clear
            rep.fail(f"device mesh {path.name} could not be read: {e}")
            continue
        if device.status().name != "NoError" or device.volume() <= 0:
            rep.fail(f"device mesh {path.name} is not a closed solid ({device.status().name}); clearance not checked")
        else:
            devices.append((path, device))

    for spec in args.posts:
        u, _, side = spec.partition(":")
        try:
            placed = rack_posts.posts(int(u), side or "both")
        except Exception as e:  # a clash check that didn't run must never read as clear
            rep.fail(f"posts {spec} could not be placed: {e}")
            continue
        for name, post in placed:
            devices.append((Path(name), post))
        rep.info(f"posts {spec}: {len(placed)} real post meshes placed for slot U{u}")

    stage = Path(tempfile.mkdtemp(prefix=f"release-{args.id}-"))
    triangles, stls, sources = {}, [], set()
    keepout = None
    if args.keepout:
        rep.heading("Keep-out")
        keep_stl = stage / "keepout.stl"
        keep_deps = stage / "keepout.deps"
        if render(args.openscad, scad, args.keepout, keep_stl, keep_deps, rep):
            sources.update(read_deps(keep_deps, scad))
            _, keepout = load_manifold(keep_stl)
            if keepout.status().name != "NoError" or keepout.volume() <= 0:
                rep.fail(f"keep-out {args.keepout} is not a closed solid; keep-out not checked")
                keepout = None
            else:
                rep.info(f"keep-out {args.keepout}: {keepout.volume():.0f} mm3, {len(keepout.decompose())} bodies")
    for spec in args.cuts:
        name, _, n = spec.partition("=")
        rep.heading(f"Cuts {name}")
        check_cuts(args.openscad, scad, name, int(n or 0), stage, rep)
    for part, part_id in parts:
        rep.heading(part)
        stl = stage / f"{args.id}_{part}.stl"
        deps = stage / f"{part}.deps"
        if not render(args.openscad, scad, part, stl, deps, rep):
            continue
        sources.update(read_deps(deps, scad))
        mesh, solid = load_manifold(stl)
        status = solid.status().name
        if status != "NoError" or solid.volume() <= 0:
            rep.fail(f"{part}: mesh is not a closed solid ({status})")
            continue
        bodies = len(solid.decompose())
        wanted = expected_bodies.get(part, 1)
        if bodies != wanted:
            rep.fail(f"{part}: {bodies} bodies, expected {wanted}")
        size = mesh.bounds[1] - mesh.bounds[0]
        rep.info(f"{part}: closed solid, {bodies} body, {len(mesh.faces)} triangles, volume {solid.volume():.0f} mm3, "
                 f"size {size[0]:.2f} x {size[1]:.2f} x {size[2]:.2f} mm")
        source_text = "\n".join(f.read_text(encoding="utf-8", errors="replace") for f in sources
                                if f.suffix == ".scad" and LIB not in f.parents)
        if f'"{part_id}"' in source_text:
            check_id_on_mesh(args.openscad, scad, part, part_id, solid, stage, rep)
        else:
            rep.fail(f'{part}: ID "{part_id}" not found in the source')
        check_holes(part, find_holes(solid), rep)
        check_clearance(part, solid, devices, args.min_gap, rep)
        if keepout is not None:
            intrusion = (solid ^ keepout).volume()
            if intrusion > OVERLAP_LIMIT:
                rep.fail(f"{part}: intrudes into the keep-out by {intrusion:.2f} mm3")
            else:
                rep.info(f"{part}: keep-out clear")
        triangles[part] = len(mesh.faces)
        stls.append(stl)

    layout = stage / f"{args.id}_{len(parts)}-parts-print-layout.3mf"
    if len(stls) == len(parts):
        rep.heading("3MF")
        write_3mf(layout, [(p, stage / f"{args.id}_{p}.stl", turns.get(p, "x90" if p == "faceplate" else None))
                           for p, _ in parts])
        check_3mf(layout, triangles, rep)
        for p, _ in parts:
            turn = turns.get(p, "x90" if p == "faceplate" else None)
            if turn:
                rep.info(f"{p}: turned {turn} for printing in the 3MF; its STL keeps the design position")

    rep.heading("Source")
    source_dir = scad.parent
    inside = [f for f in sources if source_dir in f.parents or f == scad]
    from_lib = [f for f in sources if LIB in f.parents and f not in inside]
    outside = [f for f in sources if f not in inside and f not in from_lib]
    rep.info(f"{len(inside)} source file(s) frozen in src/")
    if from_lib:
        rep.info(f"{len(from_lib)} library file(s) frozen in src/lib/; to re-render, set OPENSCADPATH to src/lib")
    for f in outside:
        rep.warn(f"dependency outside the source folder was not frozen: {f}")

    rep.heading("Result")
    rep.info(f"{len(rep.fails)} failed, {len(rep.warns)} warnings")
    rep.info("Digital checks only. The hole scan sees only fully surrounded round holes. Printed fit and strength: UNKNOWN.")
    report = "\n".join(rep.lines) + "\n"
    print(report)
    if rep.fails:
        print(f"NOT RELEASED: nothing written to {out}. Rendered files left in {stage}", file=sys.stderr)
        return 1

    out.mkdir(parents=True)
    for stl in stls:
        shutil.copy2(stl, out / stl.name)
    shutil.copy2(layout, out / layout.name)
    for f in inside:
        target = out / "src" / f.relative_to(source_dir)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, target)
    for f in from_lib:
        target = out / "src" / "lib" / f.relative_to(LIB)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, target)
    (out / "release_report.md").write_text(report, encoding="utf-8")
    shutil.rmtree(stage, ignore_errors=True)

    args.viewer_dir.mkdir(parents=True, exist_ok=True)
    viewer = args.viewer_dir / f"{args.id}.html"
    run = subprocess.run([sys.executable, str(ROOT / "tools" / "mesh_viewer.py"), *(str(out / s.name) for s in stls),
                          "-o", str(viewer), "-t", args.id], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if run.returncode:
        print(f"Released, but the viewer failed: {run.stderr[-300:]}", file=sys.stderr)
        return 1
    print(f"RELEASED {out}\nVIEWER {viewer}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
