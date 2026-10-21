"""Two devices on one tray (Brian, 2026-10-20): placement.second, clean_pair() checks, the second-device SCAD block,
and agreement between the JS window (tray-pair.js) and Python on what is blocked.
New disposable data only (temporary folder); nothing is rendered, built or exported."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

import equipment as eq
import rack_workspace
from test_tray_placement import node

HERE = Path(__file__).resolve().parent
A = eq.clean({'name': 'Router', 'dev_w': 80, 'dev_d': 60, 'dev_h': 20, 'device_mount': 'inserts', 'joint': 'screw',
              'holes': [[5, 5], [75, 55]], 'ports': [{'label': 'LAN', 'x': 0, 'z': 20, 'w': 16, 'h': 14}],
              'rear_ports': [{'label': 'Power', 'x': 0, 'z': 15}]})
B = eq.clean({'name': 'Switch', 'dev_w': 70, 'dev_d': 50, 'dev_h': 25, 'device_mount': 'straps', 'joint': 'screw',
              'ports': [{'label': 'USB', 'x': 0, 'z': 20, 'w': 14, 'h': 8}]})
ITEMS = [{'id': 'eq-0000000000a1', 'name': 'Router', 'span': 1, 'spec': A, 'build': '1' * 64, 'parts': ['tray', 'faceplate']},
         {'id': 'eq-0000000000b2', 'name': 'Switch', 'span': 1, 'spec': B, 'build': '2' * 64, 'parts': ['tray', 'faceplate']}]
# (first tray, second tray, blocked?)
CASES = [({'dev_off_x': -45}, {'dev_off_x': 50}, False),
         ({}, {}, True),                                                    # overlapping
         ({'dev_off_x': -40}, {'dev_off_x': 39}, True),                     # 4 mm apart, straps need 5.5
         ({'dev_off_x': -40}, {'dev_off_x': 41}, False),                    # 6 mm apart
         ({'dev_off_x': -55}, {'dev_off_x': 60}, True),                     # together wider than 204 mm
         ({'dev_off_x': -45}, {'dev_off_x': 50, 'device_mount': 'flat'}, True),    # one floor for both
         ({'dev_off_x': -45}, {'dev_off_x': 50, 'device_mount': 'sleeve'}, True),  # a sleeve cannot share
         ({'dev_off_x': -45, 'front_position': 'flush'}, {'dev_off_x': 50}, True),
         ({}, {'dev_off_y': 70}, True),                                     # behind, but both openings at X = 0 clash
         ({}, {'dev_off_y': 70, 'dev_off_x': 30}, False),                 # one behind the other
         ({'dev_off_x': -45, 'keystones': [-100]}, {'dev_off_x': 50}, True),  # keystone collar hits the wider tray
         ({'dev_off_x': -45}, {'dev_off_x': 50, 'dev_rot': 90}, False)]   # turned: its opening stays as entered


class TwoDevicesOnOneTray(unittest.TestCase):
    def setUp(self):
        self.folder = Path(tempfile.mkdtemp(prefix='tray-pair-'))
        (self.folder / 'equipment-library.json').write_text(json.dumps(ITEMS), encoding='utf-8')

    def tearDown(self):
        shutil.rmtree(self.folder, ignore_errors=True)

    def request(self, tray, tray2):
        return {'item': ITEMS[0]['id'], 'tray': tray, 'second': {'item': ITEMS[1]['id'], 'tray': tray2}}

    def test_one_device_source_is_unchanged(self):
        one = eq.allocation_request(self.folder, {'item': ITEMS[0]['id'], 'tray': {'dev_off_x': -45}})
        self.assertNotIn('second', one)
        self.assertNotIn('dev2_', eq.source(one))
        self.assertEqual(eq.source(eq.clean(dict(A, second=None))), eq.source(A))

    def test_pair_source_has_both_devices_and_a_wider_tray(self):
        s = eq.allocation_request(self.folder, self.request({'dev_off_x': -45}, {'dev_off_x': 50}))
        self.assertEqual(s['second']['device_mount'], 'straps')
        self.assertEqual([p['id'] for p in s['ports']], ['front-1', 'd2-front-1'])
        self.assertEqual(s['ports'][1]['x'], 50)  # the second device's opening follows it
        self.assertEqual([p['id'] for p in s['rear_ports']], ['rear-1'])
        src = eq.source(s)
        for text in ('device2_features_add();', 'device2_features_cut();', 'device2_ghost();', 'module device2_features_add()',
                     'dev2_mount="straps";', 'dev2_off_x=50', 'tray_w=186.0;'):
            self.assertIn(text, src)
        # dev2_* are declared before the derived values use them (OpenSCAD keeps a variable at its first assignment).
        self.assertLess(src.index('dev2_rot=0;'), src.index('fp2_w='))
        self.assertNotIn('dev_rot', src[src.index('module device2_features_add'):src.index('// ---- wizard overrides')].replace('dev2_rot', ''))

    def test_blocked_cases_have_plain_messages(self):
        for tray, tray2, blocked in CASES:
            with self.subTest(tray=tray, tray2=tray2):
                if blocked:
                    with self.assertRaises(ValueError):
                        eq.allocation_request(self.folder, self.request(tray, tray2))
                else:
                    eq.allocation_request(self.folder, self.request(tray, tray2))
        with self.assertRaisesRegex(ValueError, 'need at least 5.5 mm'):
            eq.allocation_request(self.folder, self.request({}, {}))
        with self.assertRaisesRegex(ValueError, 'second device is no longer in the library'):
            eq.allocation_request(self.folder, {'item': ITEMS[0]['id'], 'second': {'item': 'eq-000000000fff'}})

    def test_second_tray_keeps_only_its_own_keys(self):
        s = eq.allocation_request(self.folder, self.request({'dev_off_x': -45, 'u': 2}, {'dev_off_x': 50, 'u': 4, 'keystones': [90]}))
        self.assertEqual((s['u'], s['keystones']), (2, []))
        self.assertEqual(eq.second_settings({'dev_off_x': 3, 'u': 4, 'joint': 'single'}), {'dev_off_x': 3})

    def test_rack_document_keeps_the_second_device(self):
        place = {'id': 'a', 'slot': 1, 'span': 1, 'equipment': ITEMS[0]['id'], 'tray': {'dev_off_x': -45},
                 'second': {'equipment': ITEMS[1]['id'], 'tray': {'dev_off_x': 50, 'u': 3}, 'extra': 1}}
        doc = {'version': 1, 'generation': None, 'racks': [{'id': 'rack-1', 'name': 'Test', 'slots': 5, 'width_mm': None,
               'depth_mm': None, 'pitch_mm': None, 'placements': [place]}]}
        out = rack_workspace.validate(doc)['racks'][0]['placements'][0]
        self.assertEqual(out['second'], {'equipment': ITEMS[1]['id'], 'tray': {'dev_off_x': 50}})
        place['second'] = {'equipment': 'not-an-item'}
        with self.assertRaisesRegex(ValueError, 'second device'):
            rack_workspace.validate(doc)
        del place['second']
        self.assertNotIn('second', rack_workspace.validate(doc)['racks'][0]['placements'][0])

    def test_js_window_checks_agree_with_python(self):
        exe = node()
        if not exe:
            self.skipTest('Node.js not found')
        script = ('const T=require(process.argv[1]),P=require(process.argv[2]);const a=JSON.parse(process.argv[3]),b=JSON.parse(process.argv[4]);'
                  'console.log(JSON.stringify(JSON.parse(process.argv[5]).map(([t,t2])=>{const v=T.values(a,t),v2=P.values(b,t2);'
                  'return [...T.problems(a,v).filter(x=>!/screw joints? cannot be placed/.test(x)),...P.problems(a,v,b,v2)].length>0;})));')
        r = subprocess.run([exe, '-e', script, str(HERE / 'tray-placement.js'), str(HERE / 'tray-pair.js'), json.dumps(A), json.dumps(B),
                            json.dumps([[c[0], c[1]] for c in CASES])], capture_output=True, text=True, timeout=60, cwd=HERE)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout), [c[2] for c in CASES])

    def test_library_delete_counts_the_second_device_as_in_use(self):
        app = (HERE / 'app.py').read_text(encoding='utf-8')
        self.assertIn("p.get('second', {}).get('equipment')", app)
        self.assertIn('/tray-pair.js', app)
        self.assertIn('<script src="/tray-pair.js"></script>', (HERE / 'index.html').read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
