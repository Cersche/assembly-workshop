"""Build the Lab Rax Themes page: the real 9U Lab Rax frame and the final
brackets (same placement as work/rack-finish), with the top front beam split
into ends, middle and logo so the page can swap the middle for a themed crown.

Preview only. The frame meshes are the creator's (BY-NC-SA, personal use):
never commit or redistribute the generated page.

    python work/rack-moonshot/build_labrax_themes.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "work" / "rack-finish"))
import build_rack_finish_3d as F  # noqa: E402

END_X = 112  # beam triangles fully outside |x| >= this stay as the original ends


def main():
    meshes, instances = {}, []
    for key, comp in F.SOURCES.items():
        d = json.loads((F.APP / "rack-references" / (comp + ".json")).read_text(encoding="utf-8"))
        tris, verts = d["triangles"], d["vertices"]
        if key == "beam_top_front":
            logo = set(json.loads((F.APP / "rack-references" / "rack-logo-faces.json").read_text(encoding="utf-8"))["triangles"])
            rest = [t for i, t in enumerate(tris) if i not in logo]
            end = [t for t in rest if all(abs(verts[v][0]) >= END_X for v in t)]
            mid = [t for t in rest if not all(abs(verts[v][0]) >= END_X for v in t)]
            meshes["logo"] = F.pack(verts, [t for i, t in enumerate(tris) if i in logo])
            meshes["beam_end"] = F.pack(verts, end)
            meshes["beam_mid"] = F.pack(verts, mid)
            continue
        meshes[key] = F.pack(verts, tris)
    for key, R, t in F.frame_parts():
        if key == "beam_top_front":
            for m, g in (("beam_end", "frame"), ("beam_mid", "stockbeam"), ("logo", "logo")):
                instances.append({"mesh": m, "group": g, "R": R, "t": t})
            continue
        instances.append({"mesh": key, "group": F.GROUP[key], "R": R, "t": t})
    for k, (slot, span, rel, group, fn) in enumerate(F.BRACKETS):
        path = F.OUT / rel
        if not path.exists():  # revisions get moved into previous_* folders; take the moved copy
            hits = sorted((F.OUT / Path(rel).parts[0]).rglob(Path(rel).name))
            if not hits:
                print("skip missing", rel)
                continue
            path = hits[0]
        verts, tris = F.read_stl(path)
        lift = F.zb(slot, span)
        verts = [(lambda p: (p[0], p[1], p[2] + lift))(fn(*v)) for v in verts]
        meshes["b%d" % k] = F.pack(verts, tris)
        instances.append({"mesh": "b%d" % k, "group": group, "R": F.I, "t": [0, 0, 0], "slot": slot})
    v, t = F.blank_plate(8)
    meshes["blank8"] = F.pack(v, t)
    instances.append({"mesh": "blank8", "group": "faceplates", "R": F.I, "t": [0, 0, 0], "slot": 8})
    data = {"meshes": meshes, "instances": instances, "U": F.U, "slots": F.SLOTS}
    tpl = (HERE / "labrax_themes_template.html").read_text(encoding="utf-8")
    out = HERE / "LabRax_Themes.html"
    out.write_text(tpl.replace("/*__DATA__*/null", json.dumps(data, separators=(",", ":"))), encoding="utf-8")
    print(out, round(out.stat().st_size / 1e6, 2), "MB")


if __name__ == "__main__":
    main()
