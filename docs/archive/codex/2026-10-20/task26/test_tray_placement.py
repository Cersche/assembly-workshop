"""Place on tray window, server side: {item, tray} requests use the saved library facts plus this slot's tray
choices, and the JS window's plain-language checks agree with clean() on what is blocked.
New disposable data only (temporary folder); nothing is rendered, built or exported."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock

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



class RackViewLookup(unittest.TestCase):
    """Rack view: an existing exact render of a slot's tray settings is found by looking only; nothing is rendered."""

    def setUp(self):
        self.folder = Path(tempfile.mkdtemp(prefix='rack-view-'))
        (self.folder / 'equipment-library.json').write_text(json.dumps([ITEM]), encoding='utf-8')

    def tearDown(self):
        shutil.rmtree(self.folder, ignore_errors=True)

    def fake_render(self, tray, quality='standard'):
        s = eq.allocation_request(self.folder, {'item': ITEM['id'], 'tray': tray, 'quality': quality})
        identity = hashlib.sha256(eq.source(s).encode('utf-8')).hexdigest()
        final = self.folder / 'equipment-revisions' / identity
        final.mkdir(parents=True)
        (final / 'revision.json').write_text(json.dumps({'id': identity, 'parts': ['tray', 'faceplate']}), encoding='utf-8')
        return identity

    def test_lookup_finds_existing_render_and_never_renders(self):
        tray = {'dev_off_x': -10, 'dev_rot': 90, 'keystones': [-100]}
        with mock.patch.object(eq, 'render', side_effect=AssertionError('no renders')), \
                mock.patch.object(eq.subprocess, 'run', side_effect=AssertionError('no OpenSCAD')):
            self.assertEqual(eq.cached_allocation_render(self.folder, {'item': ITEM['id'], 'tray': tray}), {'cached': False})
            self.assertFalse((self.folder / 'equipment-revisions').exists())
            identity = self.fake_render(tray)
            self.assertEqual(eq.cached_allocation_render(self.folder, {'item': ITEM['id'], 'tray': tray}),
                             {'cached': True, 'id': identity, 'parts': ['tray', 'faceplate'], 'quality': 'standard'})
            # Other tray settings do not match that render.
            self.assertFalse(eq.cached_allocation_render(self.folder, {'item': ITEM['id'], 'tray': {'dev_off_x': -11}})['cached'])
            fine = self.fake_render({'u': 2}, 'fine')
            self.assertEqual(eq.cached_allocation_render(self.folder, {'item': ITEM['id'], 'tray': {'u': 2}})['id'], fine)

    def test_invalid_settings_or_item_give_no_render(self):
        out = eq.cached_allocation_render(self.folder, {'item': ITEM['id'], 'tray': {'dev_off_x': 70}})
        self.assertFalse(out['cached'])
        self.assertIn('off the tray', out['error'])
        self.assertFalse(eq.cached_allocation_render(self.folder, {'item': 'eq-ffffffffffff', 'tray': {}})['cached'])

    def test_js_rack_sketch_matches_python_tray_size(self):
        exe = node()
        if not exe:
            self.skipTest('Node.js not found')
        trays = [c[0] for c in CASES if not c[1]] + [{'dev_off_x': -5, 'dev_off_y': 20, 'dev_rot': 270, 'u': 2, 'rear_support': True}]
        script = ('const T=require(process.argv[1]);const s=JSON.parse(process.argv[2]);'
                  'const b=f=>{const lo=[1e9,1e9,1e9],hi=[-1e9,-1e9,-1e9];for(let i=0;i<f.length;i+=3)for(let k=0;k<3;k++){lo[k]=Math.min(lo[k],f[i+k]);hi[k]=Math.max(hi[k],f[i+k]);}return [lo,hi];};'
                  'console.log(JSON.stringify(JSON.parse(process.argv[3]).map(t=>{const k=T.rackSketch(s,t);'
                  'return {tray:b(k.tray),plate:b(k.faceplate),ks:k.openings?k.openings.length/108:0,rear:!!k.rear_bracket};})));')
        r = subprocess.run([exe, '-e', script, str(HERE / 'tray-placement.js'), json.dumps(SPEC), json.dumps(trays)],
                           capture_output=True, text=True, timeout=60)
        self.assertEqual(r.returncode, 0, r.stderr)
        for tray, got in zip(trays, json.loads(r.stdout)):
            s = eq.clean(eq.allocation_spec(SPEC, tray))
            fp_w, fp_d = (s['dev_d'], s['dev_w']) if s['dev_rot'] in (90, 270) else (s['dev_w'], s['dev_d'])
            tray_w = 2 * (abs(s['dev_off_x']) + fp_w / 2 + 8)  # equipment_tray.scad tray_w / tray_d
            tray_d = 240 if s['rear_support'] else s['dev_off_y'] + fp_d + 12 + 8
            self.assertAlmostEqual(got['tray'][0][0], -tray_w / 2, msg=tray)
            self.assertAlmostEqual(got['tray'][1][1], tray_d, msg=tray)
            self.assertAlmostEqual(got['plate'][1][2], s['u'] * 44.45 - 0.025, msg=tray)
            self.assertEqual(got['ks'], len(s['keystones']) + len(s['ports']), tray)
            self.assertEqual(got['rear'], s['rear_support'], tray)


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



class FrontOpeningsFollowTheDevice(unittest.TestCase):
    """Brian, 2026-10-19: front-port openings move with the left/right offset and standoff in the slot build, the rack
    sketch and the cable markers; a turned device keeps them as entered and gets a plain warning. Nothing is rendered."""
    LIB = eq.clean({**SPEC, 'ports': [{'id': 'lan', 'label': 'LAN', 'type': 'rj45', 'x': 0, 'z': 20, 'w': 17, 'h': 14, 'r': 1},
                                      {'id': 'usb', 'label': 'USB', 'type': 'usb-a', 'x': -80, 'z': 15, 'w': 15, 'h': 8, 'r': 1}]})
    TRAYS = [{}, {'dev_off_x': 11}, {'dev_off_x': -7, 'standoff': 10}, {'device_mount': 'straps'}, {'dev_rot': 90, 'dev_off_x': 11},
             {'dev_rot': 180}, {'u': 2, 'standoff': 12}]

    def setUp(self):
        self.folder = Path(tempfile.mkdtemp(prefix='front-openings-'))
        (self.folder / 'equipment-library.json').write_text(json.dumps([{**ITEM, 'spec': self.LIB}]), encoding='utf-8')

    def tearDown(self):
        shutil.rmtree(self.folder, ignore_errors=True)

    def build(self, tray):
        return eq.allocation_request(self.folder, {'item': ITEM['id'], 'tray': tray})

    def test_slot_source_cuts_moved_openings(self):
        self.assertEqual(eq.source(self.build({})), eq.source(self.LIB))  # untouched slot: byte-identical source
        s = self.build({'dev_off_x': 11})
        self.assertEqual([(p['x'], p['z']) for p in s['ports']], [(11, 20), (-69, 15)])
        self.assertIn('ports=[[11.0, 20.0, 17.0, 14.0, 1.0], [-69.0, 15.0, 15.0, 8.0, 1.0]];', eq.source(s))
        self.assertEqual([p['z'] for p in self.build({'standoff': 10})['ports']], [24, 19])
        self.assertEqual([p['z'] for p in self.build({'device_mount': 'straps'})['ports']], [14, 9])
        # Turned: openings stay where they were entered (no guessing).
        self.assertEqual([(p['x'], p['z']) for p in self.build({'dev_rot': 90, 'dev_off_x': 11})['ports']], [(0, 20), (-80, 15)])
        self.assertEqual(self.LIB['ports'][0]['x'], 0)  # library spec not mutated

    def test_moved_openings_are_still_guarded(self):
        lib = eq.clean({**SPEC, 'ports': [{'label': 'Edge', 'x': 110, 'z': 30, 'w': 17, 'h': 14}]})
        (self.folder / 'equipment-library.json').write_text(json.dumps([{**ITEM, 'spec': lib}]), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Edge opening would run past the faceplate edge'):
            self.build({'dev_off_x': 20})
        with self.assertRaisesRegex(ValueError, 'run off the top or bottom'):
            self.build({'standoff': 12})
        lib = eq.clean({**SPEC, 'ports': [{'label': 'Near', 'x': -90, 'z': 20, 'w': 10, 'h': 8}]})
        (self.folder / 'equipment-library.json').write_text(json.dumps([{**ITEM, 'spec': lib}]), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Near opening would cut into keystone 1'):
            self.build({'keystones': [-100]})
        # Brian, 2026-10-19 (option 3): a tray screw joint moves clear of an opening in front of it (task 18: a 1U straps
        # faceplate whose opening edge sat on the screw hole did not render). 85 mm device: default joints ±38.5 mm.
        lib = eq.clean({**SPEC, 'ports': [{'label': 'LAN', 'x': -70, 'z': 25, 'w': 16, 'h': 14}]})
        self.assertNotIn('joint_x', lib)  # default joints already clear: unchanged source
        self.assertNotIn('joint_x=', eq.source(lib).split('// ---- wizard overrides')[1])
        (self.folder / 'equipment-library.json').write_text(json.dumps([{**ITEM, 'spec': lib}]), encoding='utf-8')
        s = self.build({'dev_off_x': 30})  # opening now at X = -40, right where the left joint was
        self.assertEqual(s['joint_x'], [-58.0, 40.0])  # nearest clear spot: 18 mm from the opening centre
        self.assertIn(chr(10) + 'joint_x=[-58.0, 40.0];', eq.source(s).split('// ---- wizard overrides')[1])
        self.assertNotIn('joint_x', self.build({'dev_off_x': 30, 'joint': 'single'}))
        # An opening the old default joint sat behind now gets a moved joint instead of being blocked.
        moved = eq.clean({**SPEC, 'ports': [{'label': 'LAN', 'x': -30, 'z': 21, 'w': 16, 'h': 14}]})
        self.assertEqual(moved['joint_x'], [-12.0, 38.5])  # 101 mm tray: only room inward
        # No clear spot anywhere on the tray: blocked in plain words.
        with self.assertRaisesRegex(ValueError, 'The left and right tray screw joints cannot be placed clear of the openings'):
            eq.clean({**SPEC, 'ports': [{'label': 'Wide', 'x': 0, 'z': 15, 'w': 200, 'h': 14}]})

    def test_js_sketch_markers_and_warnings_agree_with_the_build(self):
        exe = node()
        if not exe:
            self.skipTest('Node.js not found')
        script = ('const T=require(process.argv[1]),P=require(process.argv[2]);const s=JSON.parse(process.argv[3]);'
                  'console.log(JSON.stringify(JSON.parse(process.argv[4]).map(t=>({'
                  'marks:P.wizardPorts(s,t).filter(p=>p.opening).map(p=>[p.x,p.z]),'
                  'sketch:T.openings(s,T.values(s,t)).ports.map(p=>[p.x,p.z]),'
                  'warn:T.warnings(s,T.values(s,t)),problems:T.problems(s,T.values(s,t)),'
                  'joints:(T.joints(s,T.values(s,t))||{}).joints}))));')
        r = subprocess.run([exe, '-e', script, str(HERE / 'tray-placement.js'), str(HERE / 'cable-ports.js'),
                            json.dumps(self.LIB), json.dumps(self.TRAYS)], capture_output=True, text=True,
                           encoding='utf-8', timeout=60)
        self.assertEqual(r.returncode, 0, r.stderr)
        for tray, got in zip(self.TRAYS, json.loads(r.stdout)):
            want = [[p['x'], p['z']] for p in self.build(tray)['ports']]
            self.assertEqual(got['marks'], want, tray)
            self.assertEqual(got['sketch'], want, tray)
            self.assertEqual(got['problems'], [], tray)
            built = self.build(tray)
            jx = min(40, (abs(built['dev_off_x']) + (built['dev_d'] if built['dev_rot'] in (90, 270) else built['dev_w']) / 2 + 8) - 12)
            self.assertEqual(got['joints'], built.get('joint_x', [-jx, jx]), tray)
            turned = tray.get('dev_rot', 0)
            self.assertEqual(len(got['warn']), 1 if turned else 0, tray)
            if turned:
                self.assertIn('turned %d°' % turned, got['warn'][0])
                self.assertIn('The faceplate STL keeps the openings where they were entered', got['warn'][0])

if __name__ == '__main__':
    unittest.main()


class FlatFloorTests(unittest.TestCase):
    """In-memory geometry budgets and source compatibility; never renders."""
    def spec(self, **over):
        return dict(dict(name='Compatibility', dev_w=85, dev_d=56, dev_h=20,
                         device_mount='inserts', joint='screw', holes=[[3.5, 3.5]], u=1), **over)

    def test_new_source_uses_slot_bottom_standard(self):
        for mount in ('inserts', 'pegs', 'clips', 'straps', 'flat'):
            text = eq.source(eq.clean(self.spec(device_mount=mount)))
            self.assertIn('plate_h=u*rack_pitch-plate_gap', text)
            self.assertIn('floor_z=device_mount=="flat"?0.5:7+legacy_slot_offset', text)
            self.assertIn('i*rack_pitch+rack_pitch/2+dz', text)

    def test_height_boundaries_all_mounts(self):
        import equipment
        for mount, lift in [('inserts',17.225),('pegs',17.225),('clips',17.225),('straps',11.225),('flat',3.5)]:
            s = self.spec(device_mount=mount, dev_h=44.45-lift)
            self.assertAlmostEqual(equipment.device_lift(s), lift)
            equipment.clean(s)
            with self.assertRaisesRegex(ValueError, 'taller'):
                equipment.clean(dict(s, dev_h=44.451-lift))

    def test_optiplex_budget_and_no_holes(self):
        import equipment
        s = self.spec(dev_w=182.5,dev_d=194.5,dev_h=38.8,device_mount='flat',holes=[])
        self.assertEqual(equipment.clean(s)['u'], 1)
        self.assertAlmostEqual(equipment.needed_height(s),42.3)
        with self.assertRaisesRegex(ValueError, 'taller'):
            equipment.clean(dict(s,device_mount='inserts',holes=[[3.5,3.5]]))
        self.assertEqual(equipment.clean(dict(s,device_mount='inserts',holes=[[3.5,3.5]],u=2))['u'],2)
        text = equipment.source(equipment.clean(s))
        self.assertIn('floor_z=device_mount=="flat"?0.5:7+legacy_slot_offset', text)
        self.assertIn('device_mount=="straps"||device_mount=="flat"',text)

    def test_front_openings_follow_floor_both_directions(self):
        import equipment
        lib = self.spec(ports=[dict(x=0,z=22,w=8,h=6,r=1)])
        low = equipment.allocation_spec(lib,dict(device_mount='flat',standoff=30))
        self.assertEqual(low['ports'][0]['z'],8.275)
        restored = equipment.allocation_spec(low,dict(device_mount='inserts',standoff=6))
        self.assertEqual(restored['ports'],lib['ports'])
        turned = equipment.allocation_spec(lib,dict(device_mount='flat',dev_rot=90))
        self.assertEqual(turned['ports'],lib['ports'])
        self.assertEqual(lib['ports'][0]['z'],22)

    def test_flat_joint_clearance(self):
        import equipment
        s = self.spec(device_mount='flat',dev_off_y=-1)
        with self.assertRaisesRegex(ValueError,'front screw joint'):
            equipment.clean(s)
        equipment.clean(dict(s,dev_off_y=-0.5))
        with self.assertRaisesRegex(ValueError,'corner stops'):
            equipment.clean(dict(s,joint='single',dev_off_y=-6))
        equipment.clean(dict(s,joint='single',dev_off_y=-5.8))
        with self.assertRaisesRegex(ValueError,'rear screw joint'):
            equipment.clean(dict(s,dev_off_y=30,dev_d=190,rear_support=True))
