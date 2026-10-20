"""Export quality (Brian, 2026-10-19): Draft / Standard / Fine curve resolution for equipment_tray.scad exports.
Standard must give byte-for-byte the same SCAD source as before. These tests compare generated SCAD text only:
nothing is rendered, built or exported (render() is replaced by a fake folder for the zip test)."""
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import zipfile

import equipment as eq

SPECS = [
    {'name': 'Quality box', 'dev_w': 85, 'dev_d': 56, 'dev_h': 20, 'device_mount': 'inserts', 'joint': 'screw',
     'holes': [[3.5, 3.5], [61.5, 49.5]], 'u': 1},
    {'name': 'Quality 2U', 'dev_w': 120, 'dev_d': 90, 'dev_h': 40, 'device_mount': 'straps', 'joint': 'single', 'u': 2,
     'keystones': [-100, 100], 'ports': [{'x': 0, 'z': 20, 'w': 15, 'h': 8, 'r': 1}]},
    {'name': 'Quality moved', 'dev_w': 100, 'dev_d': 150, 'dev_h': 30, 'device_mount': 'clips', 'joint': 'screw',
     'rear_support': True, 'u': 2, 'dev_off_x': 10, 'dev_rot': 90},
]


def legacy_source(s):
    """The pre-quality source(): template text plus the wizard override lines, nothing else."""
    over = {k: s[k] for k in ('dev_w', 'dev_d', 'dev_h', 'hole_d', 'standoff', 'insert_pilot', 'board_t', 'u',
                              'holes', 'keystones', 'device_mount', 'joint', 'rear_support', 'coupon')}
    for k in ('dev_off_x', 'dev_off_y', 'dev_rot'):
        if s.get(k):
            over[k] = s[k]
    over['ports'] = [[p['x'], p['z'], p['w'], p['h'], p['r']] for p in s['ports']]
    lines = ['', '// ---- wizard overrides: ' + s['name']] + [f'{k}={json.dumps(v)};' for k, v in over.items()]
    return eq.TEMPLATE.read_text(encoding='utf-8') + '\n'.join(lines) + '\n'


class ExportQualitySource(unittest.TestCase):
    def test_template_default_is_standard(self):
        text = eq.TEMPLATE.read_text(encoding='utf-8')
        self.assertIn('\n$fn=48;\n', text)
        self.assertEqual(eq.EXPORT_QUALITY[eq.DEFAULT_QUALITY], 48)

    def test_standard_is_byte_identical_to_before(self):
        for spec in SPECS:
            plain = eq.source(eq.clean(spec))
            self.assertEqual(plain, legacy_source(eq.clean(spec)), spec['name'])
            self.assertEqual(eq.source(eq.clean(dict(spec, quality='standard'))).encode('utf-8'), plain.encode('utf-8'))
            self.assertEqual(plain.count('$fn='), 1)

    def test_standard_spec_and_build_id_unchanged(self):
        for spec in SPECS:
            self.assertNotIn('quality', eq.clean(spec))
            self.assertEqual(eq.clean(dict(spec, quality='standard')), eq.clean(spec))

    def test_draft_and_fine_add_only_one_fn_line(self):
        for spec in SPECS:
            plain = eq.source(eq.clean(spec))
            for level, fn in (('draft', 24), ('fine', 96)):
                text = eq.source(eq.clean(dict(spec, quality=level)))
                extra = f'$fn={fn};\n'
                self.assertEqual(text.count(extra), 1)
                # The override comes after the template's $fn=48, so OpenSCAD uses it (last assignment wins).
                self.assertGreater(text.index(extra), text.index('$fn=48;'))
                self.assertEqual(text.replace(extra, '', 1), plain, level)
                self.assertNotEqual(eq.export_quality(eq.clean(dict(spec, quality=level)))['$fn'], 48)

    def test_unknown_quality_is_refused(self):
        for bad in ('ultra', 48, None, ''):
            with self.assertRaises(ValueError):
                eq.clean(dict(SPECS[0], quality=bad))

    def test_quality_is_not_a_tray_setting(self):
        self.assertNotIn('quality', eq.PLACEMENT_KEYS)
        self.assertEqual(eq.placement_settings({'quality': 'fine', 'u': 2}), {'u': 2})


class ExportQualityRequests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.data = Path(self.temp.name)
        item = {'id': 'eq-0123456789ab', 'name': 'Quality box', 'span': 1, 'spec': eq.clean(SPECS[0]),
                'build': '0' * 64, 'parts': ['tray', 'faceplate']}
        (self.data / 'equipment-library.json').write_text(json.dumps([item]), encoding='utf-8')

    def tearDown(self):
        self.temp.cleanup()

    def test_slot_export_request_carries_quality(self):
        plain = eq.allocation_request(self.data, {'item': 'eq-0123456789ab', 'tray': {'u': 2}})
        fine = eq.allocation_request(self.data, {'item': 'eq-0123456789ab', 'tray': {'u': 2}, 'quality': 'fine'})
        std = eq.allocation_request(self.data, {'item': 'eq-0123456789ab', 'tray': {'u': 2}, 'quality': 'standard'})
        self.assertNotIn('quality', plain)
        self.assertEqual(std, plain)
        self.assertEqual(fine['quality'], 'fine')
        self.assertEqual({k: v for k, v in fine.items() if k != 'quality'}, plain)
        with self.assertRaises(ValueError):
            eq.allocation_request(self.data, {'item': 'eq-0123456789ab', 'quality': 'best'})

    def test_zip_records_export_quality(self):
        for level, fn in (('standard', 48), ('fine', 96)):
            s = eq.clean(dict(SPECS[0], quality=level))
            folder = self.data / 'equipment-revisions' / ('a' * 63 + str(fn % 10))
            folder.mkdir(parents=True)
            (folder / 'equipment.scad').write_text(eq.source(s), encoding='utf-8')
            with mock.patch.object(eq, 'render', return_value=folder):
                blob = eq.build(dict(SPECS[0], quality=level), self.data)
            with zipfile.ZipFile(io.BytesIO(blob)) as z:
                trace = json.loads(z.read('export.json'))
                self.assertIn(f'$fn={fn};' if level != 'standard' else '$fn=48;', z.read('equipment.scad').decode('utf-8'))
            self.assertEqual(trace['export_quality'], {'level': level, '$fn': fn})
            self.assertEqual(trace['source_sha256'], folder.name)


if __name__ == '__main__':
    unittest.main()
