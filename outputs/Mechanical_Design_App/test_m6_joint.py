"""M6 bracket hardware (Brian, 2026-10-28; reproduces HDT-M6-A): opt-in m6_joint source and validation tests; no renders."""
import json
import unittest
from pathlib import Path
import equipment as eq

HDT = json.loads((Path(__file__).resolve().parents[1] / 'Hard_Drive_Tray_2026-10-25' / 'revision.json').read_text(encoding='utf-8'))['spec']
FLAT = dict(name='Box', dev_w=150, dev_d=120, dev_h=30, device_mount='flat', joint='screw', standoff=0, u=1)


class M6JointTests(unittest.TestCase):
    def test_off_keeps_legacy_source(self):
        for spec in (HDT, FLAT, dict(FLAT, m6_joint=False)):
            src = eq.source(eq.clean(spec))
            self.assertNotIn('m6', src)
            self.assertIn('front_gap=12;', src)
            self.assertNotIn('m6_joint', eq.clean(spec))

    def test_on_hooks_every_legacy_line(self):
        for spec in (HDT, FLAT):
            s = eq.clean(dict(spec, m6_joint=True))
            self.assertIs(s['m6_joint'], True)
            src = eq.source(s)
            for old, new in eq.M6_HOOKS:
                self.assertNotIn(old, src)
                self.assertIn(new, src)
            self.assertIn('// @m6-begin', src)

    def test_joint_layout(self):
        self.assertEqual(eq.m6_joints(195.45 / 2), [-87.225, -40, 40, 87.225])
        self.assertEqual(eq.m6_joints(60), [-49.5, 49.5])  # narrow tray: edge pair only, never overlapping tabs

    def test_rejects_unsupported(self):
        for extra in (dict(device_mount='sleeve'), dict(rear_support=True), dict(dev_off_y=-3),
                      dict(device_mount='inserts', holes=[[10, 10]], standoff=6), dict(m6_joint='yes')):
            with self.assertRaises(ValueError, msg=extra):
                eq.clean(dict(dict(FLAT, m6_joint=True), **extra))
        eq.clean(dict(FLAT, m6_joint=True, device_mount='inserts', holes=[[10, 10]], standoff=6, u=2))

    def test_opening_in_front_of_joint(self):
        with self.assertRaises(ValueError):
            eq.clean(dict(FLAT, m6_joint=True, ports=[{'x': 40, 'z': 20, 'w': 10, 'h': 10, 'r': 1}]))
        eq.clean(dict(FLAT, m6_joint=True, ports=[{'x': 0, 'z': 20, 'w': 10, 'h': 10, 'r': 1}]))

    def test_placement_key(self):
        self.assertIn('m6_joint', eq.PLACEMENT_KEYS)
        self.assertEqual(eq.placement_settings({'m6_joint': True}), {'m6_joint': True})


if __name__ == '__main__':
    unittest.main()
