"""Tests for release_part.py on disposable parts: python -m unittest tools/test_release_part.py"""
import contextlib
import io
import re
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import release_part as rp

SCAD = """
part="good";
module id(){translate([1,1,9.5])linear_extrude(1)text("TST-A",size=4);}
module block(){difference(){cube([40,40,10]);translate([20,30,-1])cylinder(d=BORE,h=DEPTH+1,$fn=48);}id();}
BORE=7.6; DEPTH=8;
if(part=="good")block();
if(part=="near"){difference(){cube([40,40,10]);translate([20,20,-1])cylinder(d=7.45,h=12,$fn=48);}}
if(part=="shallow"){difference(){cube([40,40,10]);translate([20,20,-1])cylinder(d=4.2,h=3,$fn=48);}}
if(part=="two"){cube(10);translate([30,0,0])cube(10);}
if(part=="broken"){cube(10);undefined_module_name_x();}
if(part=="empty"){}
"""


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.scad = self.dir / "TST-A.scad"
        self.scad.write_text(SCAD, encoding="utf-8")
        self.out = self.dir / "out"

    def tearDown(self):
        self.tmp.cleanup()

    def run_tool(self, *extra):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            code = rp.main([str(self.scad), "--id", "TST-A", "-o", str(self.out),
                            "--viewer-dir", str(self.dir / "viewer"), *extra])
        return code, buf.getvalue()


class ReleaseTests(Base):
    def test_good_part_releases_everything(self):
        code, text = self.run_tool("--part", "good")
        self.assertEqual(code, 0, text)
        self.assertIn("1 x dia 7.6", text)
        for name in ("TST-A_good.stl", "TST-A_1-parts-print-layout.3mf", "src/TST-A.scad", "release_report.md"):
            self.assertTrue((self.out / name).exists(), name)
        self.assertTrue((self.dir / "viewer" / "TST-A.html").exists())

    def test_existing_folder_is_never_overwritten(self):
        self.out.mkdir()
        keep = self.out / "keep.txt"
        keep.write_text("x", encoding="utf-8")
        with self.assertRaises(SystemExit):
            self.run_tool("--part", "good")
        self.assertEqual(keep.read_text(encoding="utf-8"), "x")

    def test_failures_write_nothing(self):
        for part, expect in (("two", "2 bodies"), ("broken", "unknown module"), ("empty", "nothing rendered")):
            with self.subTest(part=part):
                code, text = self.run_tool("--part", part)
                self.assertEqual(code, 1, text)
                self.assertIn(expect, text)
                self.assertFalse(self.out.exists())

    def test_expected_bodies_allows_two(self):
        code, text = self.run_tool("--part", "two:TST-A", "--bodies", "two=2")
        self.assertEqual(code, 0, text)

    def test_missing_id_fails(self):
        code, text = self.run_tool("--part", "good:NOPE-1")
        self.assertEqual(code, 1)
        self.assertIn('ID "NOPE-1" not found', text)

    def test_bore_warnings(self):
        code, text = self.run_tool("--part", "near")
        self.assertEqual(code, 0, text)
        self.assertIn("close to the M6 insert bore", text)
        self.out = self.dir / "out2"
        code, text = self.run_tool("--part", "shallow")
        self.assertEqual(code, 0, text)
        self.assertIn("shallower than 4.0", text)

    def _device(self, source):
        scad, stl = self.dir / "device.scad", self.dir / "device.stl"
        scad.write_text(source, encoding="utf-8")
        import subprocess
        subprocess.run([str(rp.SNAPSHOT), "--backend=manifold", "-o", str(stl), str(scad)], check=True, capture_output=True)
        return stl

    def test_clash_fails(self):
        stl = self._device("translate([5,5,5])cube(10);")
        code, text = self.run_tool("--part", "good", "--against", str(stl))
        self.assertEqual(code, 1)
        self.assertIn("overlaps device.stl", text)

    def test_gap_is_measured_and_enforced(self):
        stl = self._device("translate([0,0,12])cube(10);")
        code, text = self.run_tool("--part", "good", "--against", str(stl), "--min-gap", "1")
        self.assertEqual(code, 0, text)
        self.assertIn("nearest gap 1.", text)  # the raised text ends at Z 10.5
        self.out = self.dir / "out2"
        code, text = self.run_tool("--part", "good", "--against", str(stl), "--min-gap", "3")
        self.assertEqual(code, 1)

    def test_unreadable_device_fails_not_clears(self):
        bad = self.dir / "bad.stl"
        bad.write_text("not a mesh", encoding="utf-8")
        code, text = self.run_tool("--part", "good", "--against", str(bad))
        self.assertEqual(code, 1, text)


    def test_3mf_keeps_any_part_name_and_lies_flat(self):
        code, text = self.run_tool("--part", "good", "--part", "two:TST-A", "--bodies", "two=2", "--turn", "good=x90")
        self.assertEqual(code, 0, text)
        with zipfile.ZipFile(self.out / "TST-A_2-parts-print-layout.3mf") as z:
            xml = z.read("3D/3dmodel.model").decode("utf-8")
        self.assertIn('name="good"', xml)
        self.assertIn('name="two"', xml)
        lowest, boxes = [], []
        for body in xml.split("<object ")[1:]:
            v = [tuple(map(float, m)) for m in re.findall(r'x="([^"]+)" y="([^"]+)" z="([^"]+)"', body)]
            lowest.append(min(p[2] for p in v))
            boxes.append((min(p[1] for p in v), max(p[1] for p in v), max(p[2] for p in v)))
        self.assertAlmostEqual(lowest[0], 0, 3)
        self.assertAlmostEqual(lowest[1], 0, 3)
        self.assertAlmostEqual(boxes[0][2], 40, 2)  # x90 stands the 40 mm block side up
        self.assertAlmostEqual(boxes[1][0] - boxes[0][1], 10, 2)  # 10 mm apart


class LibraryFreezeTests(Base):
    def test_library_files_are_frozen(self):
        self.scad.write_text('include <workshop.scad>\nthe_id="TST-A";\nws_plate(1,keystones=[88]);\n', encoding="utf-8")
        code, text = self.run_tool("--part", "any")
        self.assertEqual(code, 0, text)
        self.assertTrue((self.out / "src" / "lib" / "workshop.scad").exists())
        self.assertIn("library file(s) frozen", text)


class Check3mfTests(Base):
    def make(self, xml):
        path = self.dir / "t.3mf"
        with zipfile.ZipFile(path, "w") as z:
            z.writestr("3D/3dmodel.model", xml)
        return path

    def test_good(self):
        rep = rp.Report()
        rp.check_3mf(self.make('<object><vertex x="0"/><triangle v1="0"/></object><item objectid="1"/>'), {"a": 1}, rep)
        self.assertEqual(rep.fails, [])

    def test_prefixed_tags_fail(self):
        rep = rp.Report()
        rp.check_3mf(self.make('<ns0:object><ns0:vertex x="0"/><ns0:triangle v1="0"/></ns0:object><ns0:item/>'), {"a": 1}, rep)
        self.assertTrue(rep.fails)

    def test_wrong_triangle_count_fails(self):
        rep = rp.Report()
        rp.check_3mf(self.make('<object><vertex x="0"/><triangle v1="0"/></object><item/>'), {"a": 5}, rep)
        self.assertTrue(rep.fails)


if __name__ == "__main__":
    unittest.main()
