"""Place on tray window, server side: {item, tray} requests use the saved library facts plus this slot's tray
choices, and the JS window's plain-language checks agree with clean() on what is blocked.
New disposable data only (temporary folder); nothing is rendered, built or exported."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

import equipment as eq

HERE = Path(__file__).resolve().parent
SPEC = eq.clean({'name': 'Window test box', 'dev_w': 85, 'dev_d': 56, 'dev_h': 20, 'device_mount': 'inserts',
                 'joint': 'screw', 'holes': [[3.5, 3.5], [61.5, 49.5]], 'u': 1})
ITEM = {'id': 'eq-0123456789ab', 'name': 'Window test box', 'span': 1, 'spec': SPEC, 'build': '0' * 64,
        'parts': ['tray', 'faceplate'], 'status': 'PROPOSED — UNVALIDATED'}
# (tray settings, blocked?) — each blocked case matches one SCAD assert or clean() check.
CASES = [({}, False), ({'dev_off_x': 20, 'dev_off_y': 10, 'dev_rot': 90}, False),
         ({'dev_off_x': 70}, True),                       # device moved off the tray (tray > 230 mm)
         ({'dev_off_y': -13}, True),                      # device moved into the faceplate
         ({'dev_rot': 45}, True),                         # rotation not 0/90/180/270
         ({'rear_support': True, 'dev_off_y': 180}, True),  # past the rear posts
         ({'rear_support': True, 'joint': 'single'}, True),
         ({'standoff': 30}, True),                        # taller than 1U allows
         ({'standoff': 30, 'u': 2}, False),
         ({'device_mount': 'straps'}, False),
         ({'keystones': [-60]}, True),                    # keystone collar hits the tray
         ({'keystones': [-100, -90]}, True),              # keystones closer than 21 mm
         ({'keystones': [-100, 100]}, False)]


def node():
    found = shutil.which('node')
    if found:
        return found
    fallback = Path(os.environ.get('USERPROFILE', '')) / '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
    return str(fallback) if fallback.exists() else None


class PlaceOnTrayRequests(unittest.TestCase):
    def setUp(self):
        self.folder = Path(tempfile.mkdtemp(prefix='tray-window-'))
        (self.folder / 'equipment-library.json').write_text(json.dumps([ITEM]), encoding='utf-8')

    def tearDown(self):
        shutil.rmtree(self.folder, ignore_errors=True)

    def test_request_merges_library_facts_and_slot_tray(self):
        s = eq.allocation_request(self.folder, {'item': ITEM['id'], 'tray': {'dev_off_x': -10, 'dev_rot': 180, 'u': 2}})
        self.assertEqual((s['dev_off_x'], s['dev_rot'], s['u']), (-10, 180, 2))
        self.assertEqual((s['dev_w'], s['holes']), (85, [[3.5, 3.5], [61.5, 49.5]]))
        # The request cannot change equipment facts: unknown keys in tray are dropped.
        s = eq.allocation_request(self.folder, {'item': ITEM['id'], 'tray': {'dev_w': 200, 'holes': []}})
        self.assertEqual(eq.source(s), eq.source(SPEC))

    def test_unknown_item_and_bad_payload_are_rejected(self):
        for bad in ({'item': 'eq-ffffffffffff'}, {'item': 5}, [], {'item': ITEM['id'], 'tray': 'x'}):
            with self.assertRaises(ValueError):
                eq.allocation_request(self.folder, bad)

    def test_check_reports_plain_message_without_writing(self):
        before = sorted(p.name for p in self.folder.iterdir())
        out = eq.check_allocation(self.folder, {'item': ITEM['id'], 'tray': {'dev_off_x': 70}})
        self.assertFalse(out['ok'])
        self.assertIn('off the tray', out['error'])
        self.assertIn('into the faceplate', eq.check_allocation(self.folder, {'item': ITEM['id'], 'tray': {'dev_off_y': -13}})['error'])
        self.assertEqual(eq.check_allocation(self.folder, {'item': ITEM['id'], 'tray': {}}), {'ok': True, 'u': 1})
        self.assertEqual(sorted(p.name for p in self.folder.iterdir()), before)

    def test_python_checks_block_the_same_cases(self):
        for tray, blocked in CASES:
            out = eq.check_allocation(self.folder, {'item': ITEM['id'], 'tray': tray})
            self.assertEqual(not out['ok'], blocked, (tray, out))

    def test_js_window_checks_agree_with_python(self):
        exe = node()
        if not exe:
            self.skipTest('Node.js not found')
        script = ('const T=require(process.argv[1]);const s=JSON.parse(process.argv[2]);'
                  'console.log(JSON.stringify(JSON.parse(process.argv[3]).map(t=>T.problems(s,T.values(s,t)).length>0)));')
        r = subprocess.run([exe, '-e', script, str(HERE / 'tray-placement.js'), json.dumps(SPEC), json.dumps([c[0] for c in CASES])],
                           capture_output=True, text=True, timeout=60)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout), [c[1] for c in CASES])

    def test_app_routes_window_requests(self):
        src = (HERE / 'app.py').read_text(encoding='utf-8')
        self.assertIn("'/api/equipment-placement-check'", src)
        self.assertIn("'/tray-placement.js'", src)
        self.assertEqual(src.count("equipment.allocation_request(data_dir, payload) if isinstance(payload, dict) and 'item' in payload else payload"), 2)



class SlotTrayConsumers(unittest.TestCase):
    """Cable ports and clearance screening (JS) read the same merged spec as a slot build (allocation_spec + clean)."""

    def test_js_ports_and_screening_use_the_allocation_spec(self):
        exe = node()
        if not exe:
            self.skipTest('Node.js not found')
        lib = eq.clean({**SPEC, 'rear_ports': [{'id': 'pwr', 'label': 'Power', 'type': 'iec', 'x': -20, 'z': 15}],
                        'keystones': [-100]})
        trays = [c[0] for c in CASES if not c[1]] + [{'dev_off_x': -5, 'dev_off_y': 20, 'dev_rot': 270, 'keystones': [100], 'u': 2}]
        script = ('const P=require(process.argv[1]),C=require(process.argv[2]);const s=JSON.parse(process.argv[3]);'
                  'const rack={width_mm:208,depth_mm:240,pitch_mm:44.45};'
                  'console.log(JSON.stringify(JSON.parse(process.argv[4]).map(t=>{const ps=P.wizardPorts(s,t),r=ps.find(p=>p.id==="pwr");'
                  'const c=C.screen(rack,{equipment:"eq-1",span:(t.u||s.u),tray:t},{span:s.u,spec:s}).checks;'
                  'return {ks:ps.filter(p=>p.id.endsWith("-front")&&p.type==="keystone").map(p=>p.x),rear:[r.x,r.y,r.z],'
                  'need:c.map(x=>x.needed)};})));')
        r = subprocess.run([exe, '-e', script, str(HERE / 'cable-ports.js'), str(HERE / 'clearance.js'), json.dumps(lib), json.dumps(trays)],
                           capture_output=True, text=True, timeout=60)
        self.assertEqual(r.returncode, 0, r.stderr)
        for tray, got in zip(trays, json.loads(r.stdout)):
            s = eq.clean(eq.allocation_spec(lib, tray))
            turned = s['dev_rot'] in (90, 270)
            fp_w, fp_d = (s['dev_d'], s['dev_w']) if turned else (s['dev_w'], s['dev_d'])
            # Rear port: device frame (front-left origin) -> tray, as dp() in equipment_tray.scad.
            px, w, d = -20 + s['dev_w'] / 2, s['dev_w'], s['dev_d']
            q = {0: (px, d), 90: (0, px), 180: (w - px, 0), 270: (d, w - px)}[s['dev_rot']]
            lift = lambda spec: 0 if spec['device_mount'] == 'straps' else spec['standoff']
            rear = [-fp_w / 2 + s['dev_off_x'] + q[0], 12 + s['dev_off_y'] + q[1], 15 + lift(s) - lift(lib)]
            depth = 12 + s['dev_off_y'] + fp_d
            need = [10 + lift(s) + s['dev_h'], fp_w + 16 + 2 * abs(s['dev_off_x']), max(depth, 240) if s['rear_support'] else depth]
            self.assertEqual(got['ks'], s['keystones'], tray)
            for a, b in zip(got['rear'] + got['need'], rear + need):
                self.assertAlmostEqual(a, b, places=6, msg=str(tray))


if __name__ == '__main__':
    unittest.main()
