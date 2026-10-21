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
        self.assertIn('rack opening allows 204 mm', out['error'])
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
        self.assertIn('rack opening allows 204 mm', out['error'])
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
            self.assertIn('floor_z=(device_mount=="flat"||sleeve)?0.5:7+legacy_slot_offset', text)
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
        self.assertIn('floor_z=(device_mount=="flat"||sleeve)?0.5:7+legacy_slot_offset', text)
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


class RackWidthTests(unittest.TestCase):
    def test_width_and_rotation_boundaries(self):
        base = dict(name='Width fixture',dev_w=194.5,dev_d=182.5,dev_h=38.8,
                    device_mount='flat',joint='screw',u=1,holes=[])
        with self.assertRaisesRegex(ValueError, '210.5.*204.*Rotate 90'):
            eq.clean(base)
        self.assertEqual(eq.clean(dict(base,dev_rot=90))['dev_rot'],90)
        eq.clean(dict(base,dev_w=188))
        with self.assertRaisesRegex(ValueError,'204.1.*204'):
            eq.clean(dict(base,dev_w=188.1))
        with self.assertRaisesRegex(ValueError,'204.2.*204'):
            eq.clean(dict(base,dev_w=188,dev_off_x=0.1))
        eq.clean(dict(base,dev_w=85,dev_d=56,dev_h=20,device_mount='inserts',holes=[[3.5,3.5]]))


class SleeveTests(unittest.TestCase):
    def spec(self, **over):
        return dict(dict(name='Sleeve fixture',dev_w=182.5,dev_d=194.5,dev_h=38.8,
                         device_mount='sleeve',joint='screw',u=1,holes=[]), **over)

    def test_optiplex_budgets_and_rear_support(self):
        import port_openings as P
        for over in ({}, {'rear_support':True}, {'joint':'single'}, {'dev_w':194.5,'dev_d':182.5,'dev_rot':90}):
            s=eq.clean(self.spec(**over)); w=P.sleeve(s)
            self.assertAlmostEqual(eq.device_lift(s),3.5)
            self.assertAlmostEqual(w['outside'],195.5)
            self.assertAlmostEqual(w['width'],183.5)
            self.assertAlmostEqual(w['height'],39.1)
            self.assertAlmostEqual(w['lip'],1.5)
            self.assertAlmostEqual(w['bottom']-0.025,3.475)
            self.assertAlmostEqual(44.425-w['top'],1.825)
            self.assertAlmostEqual(240-w['stop_end'],45.5)
            self.assertEqual(w['joints'],[-94.75,94.75])
            for x in w['joints']:
                self.assertGreater(abs(x)-2,w['half'])
        with self.assertRaisesRegex(ValueError,'Rear-post support needs'):
            eq.clean(self.spec(joint='single',rear_support=True))
        with self.assertRaisesRegex(ValueError,'Too tall for a flush window in 1U; choose 2U'):
            eq.clean(self.spec(dev_h=39.2))
        eq.clean(self.spec(dev_h=39.2,u=2))

    def test_window_drops_only_contained_openings_without_mutating_input(self):
        import copy, port_openings as P
        ports=[dict(x=0,z=20,w=17,h=14,r=1),dict(x=106,z=22,w=3,h=5,r=0)]
        raw=self.spec(ports=ports);before=copy.deepcopy(raw)
        s=eq.clean(raw)
        self.assertEqual(len(s['ports']),1)
        self.assertEqual(s['ports'][0]['x'],106)
        self.assertEqual(raw,before)
        self.assertEqual(len(P.sleeve_ports(ports,raw)[1]),1)
        with self.assertRaisesRegex(ValueError,'crosses the sleeve window'):
            eq.clean(self.spec(ports=[dict(x=91,z=20,w=5,h=6,r=0)]))
        with self.assertRaisesRegex(ValueError,'sleeve wall joint'):
            eq.clean(self.spec(ports=[dict(x=95,z=20,w=3,h=6,r=0)]))
        with self.assertRaisesRegex(ValueError,'collar would hit'):
            eq.clean(self.spec(keystones=[0]))

    def test_python_js_sleeve_agree(self):
        import port_openings as P
        exe=node()
        if not exe:self.skipTest('Node unavailable')
        fixtures=[self.spec(**o) for o in ({},{'rear_support':True},{'joint':'single'},{'dev_h':39.2},{'dev_off_x':3},{'dev_w':194.5,'dev_d':182.5,'dev_rot':90},{'ports':[dict(x=0,z=20,w=10,h=8,r=0)]})]
        script="const T=require(process.argv[1]),P=require(process.argv[2]);console.log(JSON.stringify(JSON.parse(process.argv[3]).map(s=>({errors:T.problems(s,T.values(s)),window:P.sleeve(s)}))));"
        run=subprocess.run([exe,'-e',script,str(HERE/'tray-placement.js'),str(HERE/'port-openings.js'),json.dumps(fixtures)],capture_output=True,text=True,encoding='utf-8',timeout=60)
        self.assertEqual(run.returncode,0,run.stderr)
        for s,js in zip(fixtures,json.loads(run.stdout)):
            try:eq.clean(s);valid=True
            except ValueError:valid=False
            self.assertEqual(not js['errors'],valid,(s,js))
            for k,v in P.sleeve(s).items():
                if isinstance(v,list):self.assertEqual(js['window'][k],v)
                else:self.assertAlmostEqual(js['window'][k],v)

    def test_source_keeps_rear_joint_and_has_sleeve_window(self):
        text=eq.source(eq.clean(self.spec(rear_support=True)))
        for fragment in ('if(sleeve)translate([dev_off_x,(sl_bottom+sl_window_top)/2])square',
                         'if(joint=="screw"&&(!sleeve||rear))', 'to_rear()tray_joint_add(true)',
                         'plate_joint_add(true)', 'cylinder(d=joint_pilot,h=8.1)',
                         'cylinder(d=m3_clear,h=plate_t+0.2)', 'sl_rear+sl_stop_t<=rack_depth-11.5'):
            self.assertIn(fragment,text)


class SleeveGuardTests(unittest.TestCase):
    def test_short_depth_and_narrow_screw_height_are_guarded(self):
        base=dict(name='Guard',dev_w=85,dev_d=72,dev_h=20,device_mount='sleeve',joint='screw',u=1)
        eq.clean(base)
        with self.assertRaisesRegex(ValueError,'at least 72 mm'):
            eq.clean(dict(base,dev_d=71.9))
        with self.assertRaisesRegex(ValueError,'window at least 10 mm'):
            eq.clean(dict(base,dev_h=5))
        eq.clean(dict(base,dev_h=5,joint='single'))

    def test_sleeve_parameters_match_scad(self):
        import port_openings as P
        text=eq.template_source(eq.clean(dict(name='Legacy',dev_w=85,dev_d=100,dev_h=20,device_mount='sleeve',joint='screw')))
        for key,value in [('sl_side',P.SLEEVE_SIDE),('sl_top',P.SLEEVE_TOP),('sl_wall',P.SLEEVE_WALL),
                          ('sl_lip_w',P.SLEEVE_LIP_W),('sl_lip_t',P.SLEEVE_LIP_T),('sl_band',P.SLEEVE_BAND),
                          ('sl_stop_t',P.SLEEVE_STOP_T),('sl_stop_h',P.SLEEVE_STOP_H)]:
            self.assertIn(f'{key}={value:g};',text)


class RearOpeningsTests(unittest.TestCase):
    def test_old_sources_byte_identical_and_new_opt_in(self):
        archive = HERE.parents[1] / 'docs/archive/codex/2026-10-20/task29/equipment_tray.scad'
        old = archive.read_text(encoding='utf-8')
        for mount in eq.MOUNTS:
            for u in range(1, 6):
                s = eq.clean(dict(name='Rear test', holes=[[20,20]], dev_w=85, dev_d=100, dev_h=20,
                                  device_mount=mount, joint="screw", rear_support=True, u=u))
                with mock.patch.object(eq, 'template_source', return_value=old):
                    expected = eq.source(s)
                self.assertEqual(eq.source(s), expected)
                enabled = eq.clean(dict(s, rear_openings=True))
                self.assertIn('rear_openings=true;', eq.source(enabled))
                self.assertIn('if(plain && rear_support && rear_openings)rear_windows2d();', eq.source(enabled))
                self.assertEqual(eq.source(eq.clean(dict(s, rear_openings=False))), expected)

    def test_boolean_and_placement_roundtrip(self):
        s = dict(name='Rear', holes=[[20,20]], dev_w=85, dev_d=56, dev_h=20, device_mount='inserts', joint='screw')
        self.assertNotIn('rear_openings', eq.clean(dict(s, rear_openings=True)))
        self.assertTrue(eq.clean(dict(s, rear_support=True, rear_openings=True))['rear_openings'])
        self.assertEqual(eq.placement_settings({'rear_openings':False}), {'rear_openings':False})
        with self.assertRaises(ValueError):
            eq.clean(dict(s, rear_support=True, rear_openings='true'))

    def test_geometry_clearance_contract(self):
        # Analytical bounds, not a render or physical test. Tie the calculations to source expressions.
        text = eq.TEMPLATE.read_text(encoding='utf-8')
        for formula in ('rear_limit=hole_x-10/2-rear_ear_keep;',
                        'rear_joint_half=max(boss_d/2,tongue_w/2)+rear_margin;',
                        'rear_joint_top=max(tray_z+14+boss_d/2,tongue_z+tongue_h)+rear_margin;',
                        'split=min(i*rack_pitch+rack_pitch/2,top-rear_radius*2)',
                        'q[1]-q[0]>=rear_min_window && q[3]-q[2]>=rear_min_window'):
            self.assertIn(formula,text)
        for floor in (0.5,8.225):
            for u in range(1,6):
                for i in range(u):
                    lo=max(.025,i*44.45)+3.5
                    hi=min(u*44.45-.025,(i+1)*44.45)-3.5
                    top=i*44.45+max(floor+14+4.5,floor+3.5+3)+4
                    split=min(i*44.45+22.225,top-4)
                    self.assertGreaterEqual(top-(i*44.45+floor+14+4.5),4-1e-10)
                    self.assertGreaterEqual(top-(i*44.45+floor+6.5),4)
                    self.assertGreaterEqual(lo-max(.025,i*44.45),3.5-1e-10)
                    self.assertGreaterEqual(min(u*44.45-.025,(i+1)*44.45)-hi,3.5-1e-10)
                    self.assertGreaterEqual(top-split,4-1e-10)
        self.assertAlmostEqual(118.2625-5-13,100.2625)
        self.assertEqual(max(4.5,12/2)+4,10)
        # SLV-B sleeve: 4mm boss margin and a 4mm horizontal web, unlike SLV-C.
        self.assertEqual(max(.5+14+4.5,.5+3.5+3)+4,23)

    def test_slv_b_reference(self):
        folder = HERE.parent / 'Physical_Test_Coupons_2026-10-20_SLV-B'
        spec = json.loads((folder / 'SLV-B_spec.json').read_text(encoding='utf-8'))
        old = eq.source(eq.clean(spec))
        self.assertNotIn('rear_windows', old)
        source = eq.source(eq.clean(dict(spec, rear_openings=True)))
        self.assertIn('rear_openings=true;', source)
        self.assertIn('rear_joint_top=max(tray_z+14+boss_d/2,tongue_z+tongue_h)+rear_margin;', source)
        self.assertIn('device_mount="sleeve";', source)
        self.assertIn('rear_band=3.5;', source)


class RearStyleTests(unittest.TestCase):
    def specimens(self):
        return [dict(name='OptiPlex',dev_w=182.5,dev_d=194.5,dev_h=38.8,device_mount='sleeve',joint='screw',rear_support=True,u=1),
                dict(name='2U inserts',dev_w=85,dev_d=100,dev_h=20,holes=[[20,20]],device_mount='inserts',joint='screw',rear_support=True,u=2)]

    def test_legacy_open_exact_source_and_style_precedence(self):
        old = (HERE.parents[1]/'docs/archive/codex/2026-10-20/task30/equipment_tray.scad').read_text(encoding='utf-8')
        for spec in self.specimens():
            s=eq.clean(dict(spec,rear_openings=True))
            with mock.patch.object(eq,'template_source',return_value=old): expected=eq.source(s)
            self.assertEqual(eq.source(s),expected)
            self.assertEqual(eq.source(eq.clean(dict(s,rear_style='open'))),expected)
            self.assertEqual(eq.source(eq.clean(dict(s,rear_style='solid'))),eq.source(eq.clean(spec)))

    def test_validation_and_disabled_support(self):
        for spec in self.specimens():
            for style in eq.REAR_STYLES:
                self.assertEqual(eq.clean(dict(spec,rear_style=style))['rear_style'],style)
                self.assertNotIn('rear_style',eq.clean(dict(spec,rear_style=style,rear_support=False)))
                self.assertEqual(eq.placement_settings({'rear_style':style}),{'rear_style':style})
                self.assertEqual(eq.placement_settings({'rear_support':False,'rear_style':style}),{'rear_support':False})
            for bad in ('bad','',None,7,[],{}):
                with self.assertRaises(ValueError):eq.clean(dict(spec,rear_style=bad))
                with self.assertRaises(ValueError):eq.placement_settings({'rear_style':bad})

    def test_geometry_all_styles_all_units(self):
        for spec in self.specimens():
            for u in range(1,6):
                for style in eq.REAR_STYLES:
                    s=eq.clean(dict(spec,u=u,rear_style=style))
                    g=eq.rear_geometry(s)
                    margin,band,strip,limit=(4,3.5,4,100.2625) if style=='open' else (6,5,6,96)
                    floor=.5 if s['device_mount']=='sleeve' else 8.225
                    width=s['dev_w']+16
                    jx=min(40,width/2-12)
                    r=eq.REAR_VENT_D/2
                    cuts=list(g['windows'])+[[x-r,x+r,z-r,z+r] for x,z in g['holes']]
                    for a,b,c,d in cuts:
                        self.assertGreaterEqual(a,-limit-1e-9);self.assertLessEqual(b,limit+1e-9)
                        i=int(c/44.45)
                        self.assertGreaterEqual(c,max(.025,i*44.45)+band-1e-9)
                        self.assertLessEqual(d,min(u*44.45-.025,(i+1)*44.45)-band+1e-9)
                        for x in (-jx,jx):
                            # Conservative boss + tongue rectangle, inflated by the style margin.
                            self.assertTrue(b<=x-6-margin+1e-9 or a>=x+6+margin-1e-9 or c>=i*44.45+floor+18.5+margin-1e-9)
                        # Rack slot nearest X=113.2625: all cuts remain inboard.
                        self.assertLess(b,113.2625);self.assertGreater(a,-113.2625)
                    for a,b,c,d in g['windows']:
                        self.assertGreaterEqual(b-a,10);self.assertGreaterEqual(d-c,10)
                    for lo in g['windows']:
                        for hi in g['windows']:
                            if lo[3]<hi[2] and int(lo[2]/44.45)==int(hi[2]/44.45):
                                self.assertGreaterEqual(hi[2]-lo[3],strip-1e-9)
                    for x,y,z,w,d,h in g['flanges']:
                        self.assertGreaterEqual(x,-100);self.assertLessEqual(x+w,100)
                        self.assertEqual(y,0);self.assertEqual(d,8)
                        self.assertGreaterEqual(z,.525);self.assertLessEqual(z+h,u*44.45-.525+1e-9)
                        # Mirror maps lips to the inner face, Y [232,240].
                        self.assertEqual(240-(y+d),232);self.assertEqual(240-y,240)
                        self.assertTrue(w==2.5 or h==2.5)
                    if style in ('reinforced','vents'):
                        self.assertEqual(len(g['flanges']),3)
                    if style=='vents':
                        self.assertGreater(len(g['holes']),0)
                        for x,z in g['holes']:
                            for a,b,c,d in g['windows']:
                                self.assertTrue(x+r<=a or x-r>=b or z+r<=c or z-r>=d)
                    src=eq.source(s)
                    if style in ('reinforced','slots','vents'):
                        self.assertIn('if(plain && rear_support)rear_style_cuts();',src)
                        self.assertIn('plate_joint_add(true);rear_style_flanges();',src)
                        self.assertIn('rear_style_windows='+json.dumps(g['windows'])+';',src)
                        self.assertIn('rear_style_holes='+json.dumps(g['holes'])+';',src)
                        self.assertIn('rear_style_lips='+json.dumps(g['flanges'])+';',src)


    def test_task31_unchanged_sources_and_specs(self):
        import importlib.util
        import copy
        path=HERE.parents[1]/'docs/archive/codex/2026-10-20/task31/equipment.py'
        loader=importlib.util.spec_from_file_location('task31_before',path)
        old=importlib.util.module_from_spec(loader);loader.loader.exec_module(old)
        old.TEMPLATE=eq.ROOT.parents[1]/'docs/archive/codex/2026-10-21/task36/equipment_tray.scad'
        for raw in self.specimens():
            for style in (None,'solid','open','slots'):
                spec=dict(raw)
                if style:spec['rear_style']=style
                original=copy.deepcopy(spec)
                self.assertEqual(old.clean(spec),eq.clean(spec))
                self.assertEqual(old.source(old.clean(spec)),eq.source(eq.clean(spec)))
                self.assertEqual(spec,original)

    def test_task31_lip_clearances(self):
        fixtures=self.specimens()+[
            dict(self.specimens()[1],u=1),
            dict(name='204 flat',dev_w=188,dev_d=200,dev_h=20,device_mount='flat',rear_support=True,joint='screw',u=1,dev_off_y=16.5)]
        for raw in fixtures:
            for style in ('reinforced','vents'):
                s=eq.clean(dict(raw,rear_style=style))
                # Include end-position joints to exercise the shortening path.
                for joints in ([-40,40],[-94,94]):
                    s['joint_x']=joints
                    g=eq.rear_geometry(s)
                    floor=.5 if s['device_mount'] in ('flat','sleeve') else 8.225
                    rear=(-4 if s['device_mount']=='sleeve' else 12+s['dev_off_y'])+s['dev_d']
                    for x,y,z,w,d,h in g['flanges']:
                        self.assertEqual(y,0);self.assertLessEqual(d,8)
                        self.assertLessEqual(240-y,244)
                        self.assertGreaterEqual(z-(floor+3),.5-1e-9)
                        self.assertGreaterEqual(240-d-rear-eq.REAR_RETENTION_REACH.get(s['device_mount'],0),.5-1e-9)
                        self.assertGreaterEqual(108-max(abs(x),abs(x+w)),8)
                        # Inflated envelope encloses uprights, tongues, slots and bosses.
                        for j in joints:
                            self.assertTrue(x+w<=j-9-.5 or x>=j+9+.5 or z>=floor+22+.5)
                    if joints==[-94,94]:
                        self.assertIn('End lip shortened',eq.source(s))

    def test_task31_dense_vents(self):
        import math
        r=eq.REAR_VENT_D/2
        for raw in self.specimens():
            s=eq.clean(dict(raw,rear_style='vents'))
            g=eq.rear_geometry(s)
            reinforced=eq.rear_geometry(dict(s,rear_style='reinforced'))
            rectangles=[q for q in reinforced['windows'] if q not in g['windows']]
            # The 2U inserts upper free region is below the window minimum;
            # vent holes there remain within the same conservative bands.
            for a,b,c,d in rectangles:
                holes=[(x,z) for x,z in g['holes'] if a<=x<=b and c<=z<=d]
                self.assertTrue(holes)
                for x,z in holes:
                    self.assertGreaterEqual(x-r,a-1e-9);self.assertLessEqual(x+r,b+1e-9)
                    self.assertGreaterEqual(z-r,c-1e-9);self.assertLessEqual(z+r,d+1e-9)
                polygon_area=24/2*r**2*math.sin(2*math.pi/24)
                self.assertGreaterEqual(len(holes)*polygon_area/((b-a)*(d-c)),.4)
            for i,(x,z) in enumerate(g['holes']):
                for xx,zz in g['holes'][i+1:]:
                    self.assertGreaterEqual(math.hypot(xx-x,zz-z)-2*r,2-1e-9)
            for q in g['windows']:
                self.assertIn(q,eq.rear_geometry(dict(s,rear_style='slots'))['windows'])


import math


class SleeveV2Tests(unittest.TestCase):
    ROOT = Path(__file__).resolve().parents[2]
    CHOICES = dict(sleeve_top=.8, feet_style='grooves', rear_floor_opening=True, insert_bosses=True)

    def raw(self, **choices):
        spec = json.loads((self.ROOT/'outputs/Physical_Test_Coupons_2026-10-20_SLV-B/SLV-B_spec.json').read_text(encoding='utf-8'))
        spec.update(self.CHOICES)
        spec.update(choices)
        return spec

    def test_optiplex_tracks_floor_and_45_degree_dips(self):
        s=eq.clean(self.raw()); tracks=eq.foot_grooves(s)
        self.assertEqual(len(tracks),2)
        self.assertEqual([(t['x0'],t['x1']) for t in tracks],[(-76.75,-70.75),(71.25,76.25)])
        for t in tracks:
            self.assertAlmostEqual(t['depth'],2.3)
            self.assertAlmostEqual(t['bottom'],1.2)
            self.assertEqual(t['floor_bottom'],0)
            self.assertGreaterEqual(t['bottom']-t['floor_bottom'],.8)
            self.assertEqual(t['y0'],-4)
            self.assertAlmostEqual(t['y1'],165.8)
            self.assertEqual([(p['y0'],p['y1']) for p in t['dips']],[(13.5,29.5),(148.5,164.5)])
            for p in t['dips']:
                self.assertAlmostEqual(p['ramp'],p['cut_depth']-t['depth'])
                self.assertAlmostEqual(p['ramp'],1.3)
        source=eq.source(s)
        self.assertIn('if(sleeve&&feet_style=="grooves")sleeve_v2_cut();',source)
        self.assertIn('rotate([90,0,90])linear_extrude',source)
        self.assertIn('foot_tracks=[[-76.75, -70.75, -4.0, 165.8, 2.3, 0]',source)
        self.assertEqual(eq.clean(s),s)

    def test_optiplex_window_bosses_width_and_cable_clearances(self):
        s=eq.clean(self.raw()); w=eq.sleeve_geometry(s); q=eq.rear_floor_geometry(s)
        self.assertAlmostEqual(w['height'],37.3); self.assertAlmostEqual(w['top'],40.8)
        self.assertAlmostEqual(44.45-.025-w['top'],3.625);self.assertEqual(w['lip'],3)
        self.assertEqual(w['joints'],[-95.75,95.75]);self.assertEqual(w['joint_z'],[6.5,37.8])
        self.assertAlmostEqual(eq.tray_width(s),201.521456708);self.assertLessEqual(eq.tray_width(s),204)
        self.assertEqual(abs(w['joints'][0])-eq.PILOT_RADIUS-w['half'],2)
        self.assertAlmostEqual(eq.INSERT_BOSS_R*math.cos(math.pi/eq.BOSS_FACETS)-eq.PILOT_RADIUS,3)
        self.assertEqual(q,dict(x0=-28,x1=28,y0=198.5,y1=225.7,r=2))
        self.assertGreaterEqual(q['y0']-w['stop_end'],4)
        self.assertGreaterEqual(240-eq.REAR_FLOOR_JOINT_REACH-q['y1'],3-1e-9)
        self.assertGreaterEqual(40-eq.REAR_JOINT_HALF-q['x1'],3)
        self.assertGreaterEqual(w['half']-q['x1'],5)
        self.assertTrue(all(not eq._rect_overlap(q,t) for t in eq.foot_grooves(s)))
        self.assertIn('floor_cable_box=[-28, 28, 198.5, 225.7];',eq.source(s))
        with self.assertRaisesRegex(ValueError,'204'):eq.clean(self.raw(dev_off_x=2))

    def test_validation_and_settings_round_trip(self):
        self.assertEqual(eq.placement_settings(self.CHOICES),self.CHOICES)
        s=eq.clean(eq.allocation_spec(self.raw(**eq.V2_DEFAULTS),self.CHOICES))
        self.assertEqual(eq.clean(s),s)
        for k,v in [('sleeve_top',.29),('sleeve_top',2.1),('sleeve_top',True),('sleeve_top',float('nan')),('feet_style','slots'),('rear_floor_opening',1),('insert_bosses','yes')]:
            with self.subTest(key=k,value=v):
                with self.assertRaises(ValueError):eq.clean(self.raw(**{k:v}))
                with self.assertRaises(ValueError):eq.placement_settings({k:v})
        for spec,message in [(self.raw(feet=[]),'need'),(self.raw(joint='single',rear_support=False,rear_floor_opening=False),'bosses'),(self.raw(rear_support=False),'rear support'),(self.raw(dev_w=220,dev_d=182.5,dev_rot=90),'Not enough floor')]:
            with self.assertRaisesRegex(ValueError,message):eq.clean(spec)
        raw=self.raw();raw['feet']=[dict(f,h=3.3) for f in raw['feet']]
        with self.assertRaisesRegex(ValueError,'too tall for grooves'):eq.clean(raw)
        raw=self.raw();raw['feet'][0]['h']=.5
        with self.assertRaises(ValueError):eq.clean(raw)

    def test_flat_and_rotated_tracks_and_interference(self):
        spec=dict(name='Flat',dev_w=100,dev_d=110,dev_h=20,device_mount='flat',joint='single',feet_style='grooves',feet=[dict(x=20,y=20,w=5,d=8,h=2)])
        for rotation in (0,90,180,270):
            s=eq.clean(dict(spec,dev_rot=rotation));t=eq.foot_grooves(s)[0]
            self.assertAlmostEqual(t['depth'],1.5)
            self.assertEqual(t['floor_bottom'],.5)
            self.assertEqual(t['y0'],12)
        with self.assertRaisesRegex(ValueError,'rear screw joint'):
            eq.clean(dict(spec,joint='screw',rear_support=True,dev_d=200,dev_off_y=16,feet=[dict(x=10,y=195,w=5,d=5,h=2)]))
        with self.assertRaisesRegex(ValueError,'rear stop'):
            eq.clean(self.raw(feet=[dict(x=20,y=190,w=5,d=4.5,h=2.8)]))

    def test_legacy_specs_and_sources_byte_identical(self):
        import importlib.util
        folder=self.ROOT/'docs/archive/codex/2026-10-21/task36'
        loader=importlib.util.spec_from_file_location('before36',folder/'equipment.py')
        old=importlib.util.module_from_spec(loader);loader.loader.exec_module(old)
        old.TEMPLATE=folder/'equipment_tray.scad'
        fixtures=[]
        for name,day in [('SLV-B','2026-10-20'),('SLV-D','2026-10-20'),('SLV-E','2026-10-21')]:
            fixtures.append(json.loads((self.ROOT/f'outputs/Physical_Test_Coupons_{day}_{name}/{name}_spec.json').read_text(encoding='utf-8')))
        for mount in eq.MOUNTS:
            for joint in eq.JOINTS:
                for units in (1,2,5):
                    for style in ('solid','open','reinforced','slots','vents'):
                        fixtures.append(dict(name='Legacy',dev_w=85,dev_d=100,dev_h=20,holes=[[20,20]],device_mount=mount,joint=joint,u=units,rear_support=joint=='screw',rear_style=style))
        for raw in fixtures:
            with self.subTest(mount=raw['device_mount'],name=raw['name']):
                before=old.clean(raw);after=eq.clean(raw)
                self.assertEqual(json.dumps(before),json.dumps(after))
                expected=old.source(before).encode('utf-8')
                self.assertEqual(eq.source(after).encode('utf-8'),expected)
                self.assertEqual(eq.source(eq.clean(dict(raw,**eq.V2_DEFAULTS))).encode('utf-8'),expected)
