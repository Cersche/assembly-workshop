"""Tests for mesh_viewer.py --measure (measurement request pages). Python 3.10 stdlib."""
import json
import struct
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mesh_viewer as mv  # noqa: E402


def cube_stl(path, s=10.0):
    v = [(0, 0, 0), (s, 0, 0), (s, s, 0), (0, s, 0), (0, 0, s), (s, 0, s), (s, s, s), (0, s, s)]
    tris = [(0, 2, 1), (0, 3, 2), (4, 5, 6), (4, 6, 7), (0, 1, 5), (0, 5, 4), (1, 2, 6), (1, 6, 5), (2, 3, 7), (2, 7, 6), (3, 0, 4), (3, 4, 7)]
    data = bytearray(80) + struct.pack("<I", len(tris))
    for t in tris:
        data += struct.pack("<3f", 0, 0, 0) + b"".join(struct.pack("<3f", *v[i]) for i in t) + b"\0\0"
    Path(path).write_bytes(bytes(data))


class MeasureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="viewer-test-")
        self.dir = Path(self.temp.name)
        cube_stl(self.dir / "cube.stl")

    def tearDown(self):
        self.temp.cleanup()

    def spec(self, data):
        path = self.dir / "spec.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        return path

    def test_expected_defaults_to_modelled_length(self):
        m = mv.load_measure(self.spec({"measurements": [
            {"label": "Width", "from": [0, 0, 0], "to": [3, 4, 0]},
            {"label": "Height", "from": [0, 0, 0], "to": [0, 0, 10], "expected": 12.5, "how": "calipers"}]}))
        self.assertEqual([x["id"] for x in m["measurements"]], [1, 2])
        self.assertEqual(m["measurements"][0]["expected"], 5.0)
        self.assertEqual(m["measurements"][1]["expected"], 12.5)
        self.assertEqual(m["measurements"][1]["how"], "calipers")

    def test_bad_specs_refused(self):
        for bad in ({}, {"measurements": []}, {"measurements": [{"label": "", "from": [0, 0, 0], "to": [1, 0, 0]}]},
                    {"measurements": [{"label": "A", "from": [0, 0], "to": [1, 0, 0]}]},
                    {"measurements": [{"label": "A", "from": [0, 0, 0], "to": [1, 0, "x"]}]},
                    {"measurements": [{"label": "A", "from": [0, 0, 0], "to": [1, 0, 0], "expected": "ten"}]}):
            with self.assertRaises(ValueError):
                mv.load_measure(self.spec(bad))

    def test_page_embeds_request_safely(self):
        out = self.dir / "page.html"
        spec = self.spec({"intro": "</script><b>x", "measurements": [{"label": "Width", "from": [0, 0, 0], "to": [10, 0, 0]}]})
        mv.main([str(self.dir / "cube.stl"), "-o", str(out), "--measure", str(spec)])
        page = out.read_text(encoding="utf-8")
        self.assertNotIn("__MEASURE__", page)
        self.assertNotIn("</script><b>", page)
        block = page.split('<script id="measure" type="application/json">', 1)[1].split("</script>", 1)[0]
        self.assertEqual(json.loads(block)["measurements"][0]["label"], "Width")

    def test_page_without_request_has_null(self):
        out = self.dir / "page.html"
        mv.main([str(self.dir / "cube.stl"), "-o", str(out)])
        self.assertIn('<script id="measure" type="application/json">null</script>', out.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
