"""Print layout: every part is its own body, flat on Z=0, faceplate front face down, no overlap."""
import unittest
import print_layout as pl


def box(x0, y0, z0, x1, y1, z1):
    c = [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
    f = [[0,2,1],[0,3,2],[4,5,6],[4,6,7],[0,1,5],[0,5,4],[1,2,6],[1,6,5],[2,3,7],[2,7,6],[3,0,4],[3,4,7]]
    return pl.stl([('p', [[c[i] for i in t] for t in f])])


class PrintLayoutTests(unittest.TestCase):
    def test_parts_flat_separate_and_plate_face_down(self):
        out = pl.layout({'tray': box(-50, 0, 7, 50, 100, 20), 'faceplate': box(-126, -4, 0, 126, 8, 44.4),
                         'rear_bracket': box(-60, 230, 5, 60, 240, 30)})
        self.assertEqual([l for l in out.splitlines() if l.startswith('solid')], ['solid tray', 'solid faceplate', 'solid rear_bracket'])
        bodies = out.split('endsolid')[:3]
        spans = []
        for b in bodies:
            lo, hi = pl.bounds(pl.facets(b))
            self.assertAlmostEqual(lo[2], 0)
            spans.append((lo[1], hi[1], hi[2]))
        self.assertAlmostEqual(spans[1][2], 12)       # faceplate lies on its face: height = its depth
        self.assertAlmostEqual(spans[0][0] - spans[1][1], pl.GAP)
        self.assertAlmostEqual(spans[2][0] - spans[0][1], pl.GAP)

    def test_3mf_has_one_object_per_part(self):
        import io, zipfile
        data = pl.layout_3mf({'tray': box(-50, 0, 7, 50, 100, 20), 'faceplate': box(-126, -4, 0, 126, 8, 44.4)})
        model = zipfile.ZipFile(io.BytesIO(data)).read('3D/3dmodel.model').decode()
        self.assertEqual(model.count('<object '), 2)
        self.assertEqual(model.count('<item '), 2)
        self.assertEqual(model.count('<triangle '), 24)

    def test_single_part(self):
        self.assertIn('solid combined', pl.layout({'combined': box(0, 0, 0, 1, 1, 1)}))
        with self.assertRaises(ValueError):
            pl.layout({})


if __name__ == '__main__':
    unittest.main()
