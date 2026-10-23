"""Opt-in tray_follow and engraved labels (Brian, 2026-10-22). Source-level checks only; no rendering."""
import unittest

import equipment

SWITCH = {'name': 'Switch', 'dev_w': 158, 'dev_d': 101, 'dev_h': 25, 'u': 1, 'device_mount': 'sleeve', 'joint': 'screw',
          'rear_support': False, 'dev_off_x': -10, 'holes': [], 'ports': [], 'rear_ports': [], 'keystones': [102]}


class TrayFollowTests(unittest.TestCase):
    def test_centred_tray_blocks_keystone(self):
        with self.assertRaises(ValueError):
            equipment.clean(SWITCH)

    def test_following_tray_frees_keystone(self):
        src = equipment.source(equipment.clean(dict(SWITCH, tray_follow=True)))
        self.assertIn('tray_w=174.0;', src)
        self.assertIn('tray_x=-97.0;', src)

    def test_follow_still_checks_collar_on_tray_side(self):
        with self.assertRaises(ValueError):
            equipment.clean(dict(SWITCH, tray_follow=True, keystones=[-102]))

    def test_follow_needs_sleeve(self):
        with self.assertRaises(ValueError):
            equipment.clean(dict(SWITCH, tray_follow=True, device_mount='flat', keystones=[]))

    def test_labels_engrave_only_when_given(self):
        spec = dict(SWITCH, tray_follow=True)
        self.assertNotIn('label_cut', equipment.source(equipment.clean(spec)))
        src = equipment.source(equipment.clean(dict(spec, labels=[{'text': 'UPLINK', 'x': 101, 'z': 3.8}])))
        self.assertIn('label_cut();', src)
        self.assertIn('labels=[["UPLINK", 101.0, 3.8, 4.5]];', src)
        with self.assertRaises(ValueError):
            equipment.clean(dict(spec, labels=[{'text': 'bad"text', 'x': 0, 'z': 3}]))


if __name__ == '__main__':
    unittest.main()
