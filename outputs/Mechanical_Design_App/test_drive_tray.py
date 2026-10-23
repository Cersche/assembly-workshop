"""Task 39: drive tray (3.5" HDD + 2.5" SSD) validation and source tests; no renders, no user data."""
import unittest
import equipment as eq

PRESET = dict(name='Drives', drives=[['3.5', -89.725, 0], ['2.5', 19.875, 0]])


class DriveTrayTests(unittest.TestCase):
    def test_preset_fits_width_and_depth(self):
        for mode in ('screws', 'sleeve'):
            s = eq.clean(dict(PRESET, drive_mount=mode))
            self.assertEqual(s['drive_mount'], mode)
            self.assertLessEqual(s['dev_w'] + 16, 204)
            src = eq.source(s)
            self.assertIn('drive_mount="%s";' % mode, src)
            self.assertIn('drive_add();else device_features_add();', src)

    def test_hardware_only_for_screws(self):
        self.assertEqual(len(eq.drive_hardware(eq.clean(dict(PRESET, drive_mount='screws')))), 2)
        self.assertEqual(eq.drive_hardware(eq.clean(dict(PRESET, drive_mount='sleeve'))), [])

    def test_rejects_bad_specs(self):
        bad = [dict(PRESET, drive_mount='glue'), dict(PRESET, ssd_h=8),
               dict(PRESET, drives=[['3.5', -89.725, 0]]),
               dict(PRESET, drives=[['3.5', -89.725, 0], ['2.5', 13, 0]]),   # side gap < 8 mm
               dict(PRESET, drives=[['3.5', -100, 0], ['2.5', 30, 0]]),      # wider than 204 mm
               dict(PRESET, keystones=[0]), dict(PRESET, u=2)]
        for spec in bad:
            with self.assertRaises(ValueError):
                eq.clean(spec)

    def test_no_drives_leaves_source_without_drive_code(self):
        src = eq.source(eq.clean(dict(name='Box', dev_w=80, dev_d=60, dev_h=20, device_mount='inserts', joint='screw', holes=[[5, 5], [75, 55]])))
        self.assertNotIn('drive', src)
        self.assertIn('   device_features_add();', src)


if __name__ == '__main__':
    unittest.main()
