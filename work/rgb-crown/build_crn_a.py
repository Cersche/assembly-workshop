"""Build the CRN-A proposal (RGB-window crown beam) and its 3D viewer.

Proposal only: panel numbers are placeholders; fit and strength UNKNOWN.
The beam ends and the context parts are the Lab Rax creator's meshes
(BY-NC-SA, personal use): the outputs stay in this private repo, the
viewer page is not committed.

    python work/rgb-crown/build_crn_a.py [out_dir]
"""
import json
import struct
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "work" / "rack-finish"))
import build_rack_finish_3d as F  # noqa: E402

OPENSCAD = r"C:\Program Files\OpenSCAD\openscad.exe"
BEAM_T = [0, 27.425, 229.825 + (F.SLOTS - 5) * F.U]


def write_stl(path, verts, tris):
    with open(path, "wb") as f:
        f.write(b"\0" * 80 + struct.pack("<I", len(tris)))
        for t in tris:
            f.write(struct.pack("<12fH", 0, 0, 0, *verts[t[0]], *verts[t[1]], *verts[t[2]], 0))


def scad(out, part, beam_stl):
    subprocess.run([OPENSCAD, "-o", str(out), "-D", 'part="%s"' % part,
                    "-D", 'beam_stl="%s"' % beam_stl.as_posix(), str(HERE / "crn_a.scad")], check=True)


def placed(path, R, t, out):
    verts, tris = F.read_stl(path)
    verts = [[sum(R[3 * r + c] * v[c] for c in range(3)) + t[r] for r in range(3)] for v in verts]
    write_stl(out, verts, tris)


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "build"
    out.mkdir(parents=True, exist_ok=True)
    d = json.loads((F.APP / "rack-references" / "component_1_23.json").read_text(encoding="utf-8"))
    beam = out / "beam_orig.stl"
    write_stl(beam, d["vertices"], d["triangles"])
    for part in ("beam", "cover", "panel"):
        scad(out / ("CRN-A_%s_local.stl" % part), part, beam)
    # rack-placed copies for the seated viewer, plus context from the real frame
    view = out / "seated"
    view.mkdir(exist_ok=True)
    for part in ("beam", "cover", "panel"):
        placed(out / ("CRN-A_%s_local.stl" % part), F.I, BEAM_T, view / ("CRN-A_%s.stl" % part))
    keep = {"panel_top", "side_rail", "handle", "beam_top_rear"}
    n = 0
    for key, R, t in F.frame_parts():
        if key in keep or (key == "post4" and t[2] > 200 and t[1] < 100):
            comp = json.loads((F.APP / "rack-references" / (F.SOURCES[key] + ".json")).read_text(encoding="utf-8"))
            src = out / ("ctx_%s.stl" % key)
            write_stl(src, comp["vertices"], comp["triangles"])
            n += 1
            placed(src, R, t, view / ("ctx_%02d_%s.stl" % (n, key)))
            src.unlink()
    print("built", out)


if __name__ == "__main__":
    main()
