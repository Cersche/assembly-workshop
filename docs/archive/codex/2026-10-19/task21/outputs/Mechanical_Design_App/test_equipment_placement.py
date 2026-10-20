import re
import subprocess
import unittest
from pathlib import Path

import equipment as eq

HERE = Path(__file__).resolve().parent
BASE = {'name': 'Placement test', 'dev_w': 85, 'dev_d': 56, 'dev_h': 20, 'device_mount': 'inserts',
        'joint': 'screw', 'holes': [[3.5, 3.5], [61.5, 49.5]]}


class PlacementSettings(unittest.TestCase):
    def test_template_declares_settings_with_neutral_defaults(self):
        t = eq.TEMPLATE.read_text(encoding='utf-8')
        for line in ('dev_off_x=0;', 'dev_off_y=0;', 'dev_rot=0;'):
            self.assertIn(line, t)
        # Default expressions reduce exactly to the previous centred layout.
        self.assertIn('tray_w=2*(abs(dev_off_x)+fp_w/2+margin)', t)
        self.assertIn('dev_x=-fp_w/2+dev_off_x; dev_y=front_gap+dev_off_y;', t)
        self.assertIn('dev_rot==0||dev_rot==90||dev_rot==180||dev_rot==270', t)

    def test_older_items_without_keys_keep_identical_override_block(self):
        s = eq.clean(dict(BASE))
        self.assertEqual((s['dev_off_x'], s['dev_off_y'], s['dev_rot']), (0, 0, 0))
        tail = eq.source(s)[len(eq.TEMPLATE.read_text(encoding='utf-8')):]
        self.assertNotRegex(tail, r'dev_off_|dev_rot')
        explicit = eq.source(eq.clean(dict(BASE, dev_off_x=0, dev_off_y=0, dev_rot=0)))
        self.assertEqual(explicit, eq.source(s))

    def test_moved_rotated_item_writes_settings(self):
        src = eq.source(eq.clean(dict(BASE, dev_off_x=-10, dev_off_y=5, dev_rot='90')))
        self.assertIn('dev_off_x=-10.0;', src)
        self.assertIn('dev_off_y=5.0;', src)
        self.assertIn('dev_rot=90;', src)

    def test_invalid_placements_are_rejected(self):
        for bad in ({'dev_rot': 45}, {'dev_rot': 'x'}, {'dev_off_y': -13}, {'dev_off_x': 70},
                    {'dev_off_x': 50, 'dev_w': 120}):
            with self.assertRaises(ValueError):
                eq.clean(dict(BASE, **bad))
        # Rotation swaps width/depth: a 200 mm wide device fits only unrotated, a 60 mm deep one rotated.
        eq.clean(dict(BASE, dev_w=200, dev_d=60, holes=[], device_mount='straps'))
        eq.clean(dict(BASE, dev_w=200, dev_d=60, holes=[], device_mount='straps', dev_rot=90))
        with self.assertRaises(ValueError):
            eq.clean(dict(BASE, dev_w=60, dev_d=220, holes=[], device_mount='straps', dev_rot=90, u=1))


if __name__ == '__main__':
    unittest.main()
