"""Keystone faceplate mesh fix (2026-10-19). The wizard rejected faceplates with a golden keystone as non-manifold:
OpenSCAD 2021 snaps 2D polygon points to a 1/65536 mm grid, so the block's plate-flush faces (depth 0.08 / 4.08)
landed 0.0000134 mm off the plate, and its top/bottom faces landed a hair off the plate opening.

StaticKeystoneTests read the template text only (run_checks). KeystoneRenderTests really render a faceplate in a
temporary folder with OpenSCAD; they run only when AW_RENDER_TESTS=1 is set (run_checks starts no OpenSCAD)."""
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
import unittest

import equipment as eq
import mesh_revision

# Hash of the KS_GOLD table before the fix: the golden opening geometry must stay exactly as Brian approved it.
KS_GOLD_SHA256 = 'f8b03cd4c0337868d154835dac49e91d4eb4c80e22edb475281786356b2f1575'
GRID = 65536  # OpenSCAD 2021 ClipperUtils scale for 2D geometry


def on_grid(v):
    return abs(v * GRID - round(v * GRID)) < 1e-9


class StaticKeystoneTests(unittest.TestCase):
    def setUp(self):
        self.text = eq.TEMPLATE.read_text(encoding='utf-8')

    def test_golden_table_and_tightness_unchanged(self):
        block = re.search(r'KS_GOLD=\[.*?\n\];', self.text, re.S).group(0)
        self.assertEqual(hashlib.sha256(block.encode('utf-8')).hexdigest(), KS_GOLD_SHA256)
        self.assertIn('\nks_tight=0.2;', self.text)
        self.assertIn('\nks_style="golden";', self.text)

    def test_plate_flush_depths_land_on_the_2d_grid(self):
        # The cause: 0.08 and 4.08 are off the grid; shifted by -0.08 they are exactly 0 and 4.
        self.assertFalse(on_grid(0.08) or on_grid(4.08))
        self.assertTrue(on_grid(0.08 - 0.08) and on_grid(4.08 - 0.08))
        self.assertIn('polygon([for(q=pg)[q[0],q[1]-0.08]])', self.text)
        self.assertIn('[0,0,1,-4]', self.text)  # the 0.08 goes back in the 3D transform (was -4.08)
        self.assertNotIn('[0,0,1,-4.08]', self.text)

    def test_block_is_clipped_by_the_same_box_as_the_plate_opening(self):
        cut = re.search(r'module ks_box_cut\(\)\{for\(k=keystones\)let\([^\n]+?\)translate\(\[x-10\.5,[^,]+,kz-15\]\)cube\(\[21,[^,]+,33\.5\]\)', self.text)
        self.assertTrue(cut)
        golden = re.search(r'module ks_golden\(\)\{.*?\n\}\}', self.text, re.S).group(0)
        self.assertIn('translate([x-10.5,-plate_t-1,kz-15])cube([21,plate_t+16,33.5]);', golden)


@unittest.skipUnless(os.environ.get('AW_RENDER_TESTS') == '1', 'set AW_RENDER_TESTS=1 to render with OpenSCAD')
class KeystoneRenderTests(unittest.TestCase):
    def test_keystone_faceplates_pass_the_mesh_check_without_nudge(self):
        base = {'name': 'Keystone mesh', 'dev_w': 100, 'dev_d': 80, 'dev_h': 20, 'device_mount': 'inserts',
                'joint': 'screw', 'holes': [[10, 10]]}
        cases = [{'u': 1, 'keystones': [-75]}, {'u': 1, 'keystones': [-100, 100]}, {'u': 2, 'keystones': [75]}]
        with tempfile.TemporaryDirectory() as folder:
            for case in cases:
                with self.subTest(case=case):
                    final = eq.render(dict(base, **case), folder)
                    mesh = mesh_revision.read_mesh(final / 'faceplate.stl', 'faceplate')
                    self.assertGreater(mesh['signed_volume_mm3'], 0)
                    report = json.loads((final / 'revision.json').read_text(encoding='utf-8'))
                    self.assertEqual(report['nudge_mm']['faceplate'], 0)  # passes first time, no render-repair nudge


if __name__ == '__main__':
    unittest.main()
