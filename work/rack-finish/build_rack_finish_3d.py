"""Build the Rack Finish 3D page: the saved 9U Lab Rax frame plus the current
final brackets, placed in rack coordinates, with colour pickers per part group.

Preview only. Reads meshes, writes one HTML file, changes no geometry or data.
The frame meshes are the creator's (BY-NC-SA, personal use): never commit or
share the generated page.

    python work/rack-finish/build_rack_finish_3d.py
"""
import base64
import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from mesh_viewer import read_stl  # noqa: E402

APP = ROOT / "outputs" / "Mechanical_Design_App"
OUT = ROOT / "outputs"
U = 44.45
SLOTS = 9
PX, DEPTH = 125.98, 240

# rack-scene.js poses (rows of R are applied to source vertices)
I = [1, 0, 0, 0, 1, 0, 0, 0, 1]
RX = [1, 0, 0, 0, -1, 0, 0, 0, -1]
RY = [-1, 0, 0, 0, 1, 0, 0, 0, -1]
RZ = [-1, 0, 0, 0, -1, 0, 0, 0, 1]
SOURCES = {"post4": "component_0_24", "beam_bottom": "component_1_20", "beam_top_front": "component_1_23",
           "beam_top_rear": "component_1_18", "side_rail": "component_1_28", "panel_bottom": "component_1_13",
           "panel_top": "component_1_11", "foot": "component_1_6", "handle": "component_1_25",
           "extension": "component_2_1"}
GROUP = {"post4": "posts", "extension": "extensions", "beam_bottom": "frame", "beam_top_front": "frame",
         "beam_top_rear": "frame", "side_rail": "frame", "panel_bottom": "panels", "panel_top": "panels",
         "foot": "feet", "handle": "handles"}


def frame_parts():
    """rack-scene.js frame() plus workspace.js rackFrame() for post_levels [4, 4] per side."""
    p = []
    add = lambda key, R, t: p.append((key, R, t))
    add("beam_bottom", I, [0, 27.425, -7.575]); add("beam_bottom", RZ, [0, DEPTH - 27.425, -7.575])
    add("side_rail", RX, [-PX, 120, -17.5]); add("side_rail", RY, [PX, 120, -17.5]); add("panel_bottom", I, [0, 120, -31.5])
    for x in (-124.73, 124.73):
        for y in (55, 185):
            add("foot", I, [x, y, -41])
    for side, x in (("left", -PX), ("right", PX)):
        z = 0
        for i, u in enumerate([4, 4]):
            mid = z + u * U / 2
            poses = [[I, -PX, 17.5], [RX, -PX, DEPTH - 17.5]] if side == "left" else [[RY, PX, 17.5], [RZ, PX, DEPTH - 17.5]]
            for R, px, py in poses:
                add("post4", R, [px, py, mid])
            z += u * U
            if i == 0:
                add("extension", I if side == "left" else RY, [x, 120, z + U / 2]); z += U
    dz = (SLOTS - 5) * U
    add("beam_top_front", I, [0, 27.425, 229.825 + dz]); add("beam_top_rear", RZ, [0, DEPTH - 27.425, 229.825 + dz])
    add("side_rail", I, [-PX, 120, 239.75 + dz]); add("side_rail", RZ, [PX, 120, 239.75 + dz]); add("panel_top", I, [0, 120, 253.75 + dz])
    add("handle", I, [-124.789, 120, 276 + dz]); add("handle", RZ, [124.789, 120, 276 + dz])
    return p


def zb(slot, span=1):
    """App slot 1 is the top; returns the slot range's bottom Z."""
    return (SLOTS - slot - span + 1) * U


# (slot, span, file, group, mapping(x, y, z) -> rack-local before the slot lift)
ident = lambda x, y, z: (x, y, z)
BRACKETS = [
    (1, 1, "CM1000_M6_2026-10-28/CM6A_faceplate.stl", "faceplates", lambda x, y, z: (x - 127, y - 4, z)),
    (1, 1, "CM1000_M6_2026-10-28/CM6A_rail_l.stl", "brackets", lambda x, y, z: (x - 127, y - 4, z)),
    (1, 1, "CM1000_M6_2026-10-28/CM6A_rail_r.stl", "brackets", lambda x, y, z: (x - 127, y - 4, z)),
    (2, 1, "TL-SG108E_M6_2026-10-28/SG8-M6-B_faceplate.stl", "faceplates", ident),
    (2, 1, "TL-SG108E_M6_2026-10-28/SG8-M6-B_tray.stl", "brackets", ident),
    (3, 1, "Faceplate_1U_10_Keystones_2026-10-22/Faceplate_1U_10_Keystones.stl", "faceplates", ident),
    # HDT faceplate is stored front face down: rotate it upright.
    (4, 1, "Hard_Drive_Tray_M6_2026-10-28/HDT-M6-A_faceplate_base_color.stl", "faceplates", lambda x, y, z: (x, z - 4, -y - 10)),
    (4, 1, "Hard_Drive_Tray_M6_2026-10-28/HDT-M6-A_faceplate_icon_inlay.stl", "icons", lambda x, y, z: (x, z - 4, -y - 10)),
    (4, 1, "Hard_Drive_Tray_M6_2026-10-28/HDT-M6-A_tray.stl", "brackets", lambda x, y, z: (x, y + 92, z + 1)),
    (5, 1, "Hue_Pi4_M6-B_2026-10-28/HP4-M6-B_faceplate.stl", "faceplates", ident),
    (5, 1, "Hue_Pi4_M6-B_2026-10-28/HP4-M6-B_tray.stl", "brackets", ident),
    (6, 2, "Screen_5in_SCR5-B_2026-10-29/SCR5-B_plate.stl", "faceplates", ident),
    (6, 2, "Screen_5in_SCR5-B_2026-10-29/SCR5-B_frame.stl", "brackets", ident),
    (6, 2, "Screen_5in_SCR5-B_2026-10-29/checks/SCR5-B_nominal-screen-envelope.stl", "glass", ident),
    (9, 1, "Physical_Test_Coupons_2026-10-21_SLV-F/SLV-F-PLATE.stl", "faceplates", lambda x, y, z: (x, z - 4, 44.4 - y)),
    (9, 1, "Physical_Test_Coupons_2026-10-21_SLV-F/SLV-F-TRAY.stl", "brackets", ident),
    (9, 1, "Physical_Test_Coupons_2026-10-21_SLV-F/SLV-F-REAR-O.stl", "brackets", lambda x, y, z: (x, 244 - z, y)),
]


def b64(fmt, values):
    return base64.b64encode(struct.pack("<%d%s" % (len(values), fmt), *values)).decode("ascii")


def pack(verts, tris):
    return {"v": b64("f", [c for v in verts for c in v]), "i": b64("I", [i for t in tris for i in t]), "n": len(tris)}


def blank_plate(slot):
    """Placeholder 1U blank plate for the reserved cooling slot (no part exists yet)."""
    x0, x1, y0, y1, z0, z1 = -126, 126, -4, 0, zb(slot) + 0.025, zb(slot) + 44.425
    v = [(x, y, z) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]
    t = [(0, 1, 3), (0, 3, 2), (4, 6, 7), (4, 7, 5), (0, 4, 5), (0, 5, 1), (2, 3, 7), (2, 7, 6), (0, 2, 6), (0, 6, 4), (1, 5, 7), (1, 7, 3)]
    return v, t


def main():
    meshes, instances = {}, []
    for key, comp in SOURCES.items():
        d = json.loads((APP / "rack-references" / (comp + ".json")).read_text(encoding="utf-8"))
        tris = d["triangles"]
        if key == "beam_top_front":  # painted Lab Rax logo faces get their own group
            logo = set(json.loads((APP / "rack-references" / "rack-logo-faces.json").read_text(encoding="utf-8"))["triangles"])
            meshes["logo"] = pack(d["vertices"], [t for i, t in enumerate(tris) if i in logo])
            tris = [t for i, t in enumerate(tris) if i not in logo]
        meshes[key] = pack(d["vertices"], tris)
    for key, R, t in frame_parts():
        instances.append({"mesh": key, "group": GROUP[key], "R": R, "t": t})
        if key == "beam_top_front":
            instances.append({"mesh": "logo", "group": "logo", "R": R, "t": t})
    for k, (slot, span, rel, group, fn) in enumerate(BRACKETS):
        verts, tris = read_stl(OUT / rel)
        lift = zb(slot, span)
        verts = [(lambda p: (p[0], p[1], p[2] + lift))(fn(*v)) for v in verts]
        name = "b%d" % k
        meshes[name] = pack(verts, tris)
        instances.append({"mesh": name, "group": group, "R": I, "t": [0, 0, 0], "slot": slot, "file": Path(rel).name})
    v, t = blank_plate(8)
    meshes["blank8"] = pack(v, t)
    instances.append({"mesh": "blank8", "group": "faceplates", "R": I, "t": [0, 0, 0], "slot": 8, "file": "placeholder"})
    data = {"meshes": meshes, "instances": instances, "U": U, "slots": SLOTS}
    tpl = (Path(__file__).parent / "rack_finish_3d_template.html").read_text(encoding="utf-8")
    out = Path(__file__).parent / "Rack_Finish_3D.html"
    out.write_text(tpl.replace("/*__DATA__*/null", json.dumps(data, separators=(",", ":"))), encoding="utf-8")
    print(out, round(out.stat().st_size / 1e6, 2), "MB", sum(m["n"] for m in meshes.values()), "unique triangles")


if __name__ == "__main__":
    main()
