"""Build the CRN-B proposal (P2 panel tray on the stock beam slope) and its seated viewer set.

Proposal only: panel numbers are placeholders; fit and strength UNKNOWN. The stock beam and
context parts are the Lab Rax creator's meshes (BY-NC-SA, personal use): viewer page not committed.

    python work/rgb-crown/build_crn_b.py [out_dir]
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_crn_a as A  # noqa: E402

F = A.F


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "build_b"
    view = out / "seated"
    view.mkdir(parents=True, exist_ok=True)
    for part in ("tray", "bezel", "panel", "screws"):
        local = out / ("CRN-B_%s_local.stl" % part)
        subprocess.run([A.OPENSCAD, "-o", str(local), "-D", 'part="%s"' % part, str(HERE / "crn_b.scad")], check=True)
        A.placed(local, F.I, A.BEAM_T, view / ("CRN-B_%s.stl" % part))
    keep = {"beam_top_front", "panel_top", "side_rail", "handle"}
    n = 0
    for key, R, t in F.frame_parts():
        if key in keep and t[2] > 200 or (key == "post4" and t[2] > 200 and t[1] < 100):
            comp = json.loads((F.APP / "rack-references" / (F.SOURCES[key] + ".json")).read_text(encoding="utf-8"))
            src = out / "ctx.stl"
            A.write_stl(src, comp["vertices"], comp["triangles"])
            n += 1
            A.placed(src, R, t, view / ("ctx_%02d_%s.stl" % (n, key)))
            src.unlink()
    print("built", out)


if __name__ == "__main__":
    main()
