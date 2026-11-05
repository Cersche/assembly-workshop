"""Checks lib/workshop.scad against the built SG8-M6-F parts: python -m unittest tools/test_workshop_lib.py"""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import manifold3d as m3
import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "outputs" / "Chunky_Revisions" / "TL-SG108E_post_rails_2026-10-30"
OPENSCAD = r"D:\Tools\OpenSCAD-snapshot\OpenSCAD-2026.11.01-x86-64\openscad.exe"
BOSS_X, BOSS_Z = -88, 38.425  # SG8-M6-F hs_x[0] and hs_z


def solid(path):
    mesh = trimesh.load(str(path), force="mesh")
    mesh.merge_vertices()
    return m3.Manifold(m3.Mesh(np.asarray(mesh.vertices, dtype=np.float32), np.asarray(mesh.faces, dtype=np.uint32)))


def box(x0, x1, y0, y1, z0, z1):
    return m3.Manifold.cube([x1 - x0, y1 - y0, z1 - z0]).translate([x0, y0, z0])


class LibraryMatchesBuiltParts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def render(self, body):
        scad = Path(self.tmp.name) / "t.scad"
        stl = Path(self.tmp.name) / "t.stl"
        scad.write_text("include <workshop.scad>\n" + body, encoding="utf-8")
        run = subprocess.run([OPENSCAD, "--backend=manifold", "-o", str(stl), str(scad)], capture_output=True, text=True,
                             encoding="utf-8", errors="replace", env={**os.environ, "OPENSCADPATH": str(ROOT / "lib")})
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertNotIn("Ignoring unknown", run.stderr)
        return solid(stl)

    def same_in(self, a, b, region, limit=0.05):
        """Compare inside one region only; the rest of the reference has that bracket's own window and label."""
        x, y = a ^ region, b ^ region
        self.assertGreater(y.volume(), 1, "region is empty in the reference, so this check would prove nothing")
        difference = (x - y).volume() + (y - x).volume()
        self.assertLess(difference, limit, f"{difference:.3f} mm3 differs; region volume {y.volume():.0f} mm3")

    def test_plate_slots_and_keystone(self):
        ref = solid(REF / "SG8-M6-F_faceplate.stl")
        lib = self.render("ws_plate(1,keystones=[88]);")
        for name, region in (("left slots", box(-127, -105, -5, 0, -1, 46)), ("right slots", box(105, 127, -5, 0, -1, 46))):
            with self.subTest(name):
                self.same_in(lib, ref, region)
        with self.subTest("keystone"):
            self.same_in(lib, ref, box(77, 99, -5, 12, 7.2, 42), limit=1.0)

    def test_hidden_m6_boss(self):
        ref = solid(REF / "SG8-M6-F_faceplate.stl")
        lib = self.render(f"ws_m6_plate_boss({BOSS_X},{BOSS_Z});")
        self.same_in(lib, ref, box(BOSS_X - 7, BOSS_X + 7, 0, 8, BOSS_Z - 7, 45))

    def test_m6_screw_cut_in_tray_upright(self):
        ref = solid(REF / "SG8-M6-F_tray.stl")
        lib = self.render(f"difference(){{translate([{BOSS_X}-8,8.3,32.35])cube([16,6,11.5]);"
                          f"ws_m6_screw_cut({BOSS_X},8.3,{BOSS_Z});}}")
        # Starts above Z 33.91: below that, SG8-M6-F's own sleeve lip fills the recess.
        self.same_in(lib, ref, box(BOSS_X - 8, BOSS_X + 8, 8.3, 14.3, 34, 43.85))

    def test_bosl2_available(self):
        self.assertGreater(self.render("include <BOSL2/std.scad>\ncuboid([10,10,10],rounding=1);").volume(), 900)


if __name__ == "__main__":
    unittest.main()
