"""mesh_study: overlapping bodies and a hidden floor groove (the OptiPlex bracket lesson, 2026-10-20)."""
import struct
import tempfile
import unittest
from pathlib import Path

import mesh_study


def box(x0, y0, z0, x1, y1, z1):
    p = [(x, y, z) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]
    q = lambda i, j, k: p[i * 4 + j * 2 + k]
    faces = [  # outward winding
        (q(0, 0, 0), q(0, 1, 0), q(0, 1, 1), q(0, 0, 1)), (q(1, 0, 0), q(1, 0, 1), q(1, 1, 1), q(1, 1, 0)),
        (q(0, 0, 0), q(0, 0, 1), q(1, 0, 1), q(1, 0, 0)), (q(0, 1, 0), q(1, 1, 0), q(1, 1, 1), q(0, 1, 1)),
        (q(0, 0, 0), q(1, 0, 0), q(1, 1, 0), q(0, 1, 0)), (q(0, 0, 1), q(0, 1, 1), q(1, 1, 1), q(1, 0, 1))]
    return [t for a, b, c, d in faces for t in ((a, b, c), (a, c, d))]


def write_stl(path, tris):
    with open(path, 'wb') as f:
        f.write(b'\0' * 80 + struct.pack('<I', len(tris)))
        for t in tris:
            f.write(struct.pack('<12fH', 0, 0, 0, *t[0], *t[1], *t[2], 0))


# A 100 x 60 floor seen with Y up: base slab Y 0-2, plus two OVERLAPPING upper slabs (Y 1.5-4) that leave a
# 5 mm groove at X 40-45, 2 mm deep. Three separate bodies, like the third-party bracket's STL.
FLOOR = box(0, 0, 0, 100, 2, 60) + box(0, 1.5, 0, 40, 4, 60) + box(45, 1.5, 0, 100, 4, 60) + box(0, 10, 0, 100, 12, 60)


class MeshStudyTests(unittest.TestCase):
    def setUp(self):
        self.path = Path(tempfile.mkdtemp()) / 'floor.stl'
        write_stl(self.path, FLOOR)
        self.tris = mesh_study.load_mesh(self.path)

    def test_bodies_and_closure(self):
        self.assertEqual(len(mesh_study.bodies(self.tris)), 4)
        self.assertEqual(mesh_study.open_edges(self.tris), 0)
        self.assertEqual([tuple(round(v, 3) for v in r) for r in mesh_study.bbox(self.tris)], [(0, 100), (0, 12), (0, 60)])

    def test_overlapping_bodies_merge_into_one_solid(self):
        cols = mesh_study.columns(self.tris, 1, 1.0)
        self.assertEqual([tuple(round(v, 3) for v in iv) for iv in cols[(20.5, 30.5)]], [(0, 4), (10, 12)])
        self.assertEqual([tuple(round(v, 3) for v in iv) for iv in cols[(42.5, 30.5)]], [(0, 2), (10, 12)])

    def test_finds_the_groove(self):
        r = mesh_study.recesses(self.tris, 1, step=0.5)
        self.assertEqual(r['floor']['level'], 4.0)
        groove = r['floor']['features'][0]
        self.assertEqual((groove['kind'], groove['depth']), ('recess', 2.0))
        self.assertEqual([tuple(round(v, 2) for v in s) for s in groove['span']], [(40, 45), (0, 60)])
        self.assertEqual(r['roof']['level'], 10.0)
        self.assertEqual(r['roof']['features'], [])

    def test_section_shows_the_groove(self):
        rows = mesh_study.section(self.tris, 2, 30, 1.0)
        floor_row = [r for r in rows if r.strip().startswith('3.5')][0]
        self.assertIn('#.....#', floor_row.replace(' ', '')[-70:])


if __name__ == '__main__':
    unittest.main()
