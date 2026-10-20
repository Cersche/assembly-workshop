import json
from pathlib import Path
import tempfile
import threading
import unittest
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from http.server import ThreadingHTTPServer
from app import Store, evaluate, make_handler, validate_part, joint_geometry, ROOT


def screw(**changes):
    p = dict(id='s', revision=1, name='Test screw', kind='screw', diameter=3, pitch=.5,
             source='Test fixture', verification='custom', length=6, threaded_length=6,
             length_convention='under_head')
    return dict(p, **changes)


def insert(**changes):
    p = dict(id='i', revision=1, name='Test insert', kind='heatset', diameter=3, pitch=.5,
             source='Test fixture', verification='custom', length=5, usable_depth=5,
             outside_diameter=4.6, min_wall=2, hole_diameter=4.2, hole_profile='straight', end_type='closed')
    return dict(p, **changes)


class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.tmp.name) / 'db.sqlite3')

    def tearDown(self):
        self.tmp.cleanup()

    def test_atomic_immutable_import_and_pinning(self):
        self.store.import_parts([screw(), insert()])
        self.store.save({'selections': {'screw': {'id': 's', 'revision': 1}}, 'inputs': {}})
        self.store.import_parts([screw(revision=2, length=10)])
        reopened = Store(self.store.path)
        self.assertEqual(reopened.project()['selections']['screw']['length'], 6)
        with self.assertRaises(ValueError):
            self.store.import_parts([insert(id='new'), screw(length=9)])
        self.assertNotIn('new', [p['id'] for p in self.store.parts()])

    def test_invalid_dimensions(self):
        for value in [None, True, float('nan'), float('inf'), -1, 0, '3']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_part(screw(pitch=value))

    def test_thread_mismatch_and_missing_selection(self):
        self.assertEqual(evaluate(screw(), insert(pitch=.4), {})['checks'][0]['status'], 'fail')
        self.assertEqual(evaluate(None, None, {})['status'], 'incomplete')

    def test_starter_catalog_is_idempotent_and_keeps_selection(self):
        self.assertEqual(self.store.load_starter(), 6)
        parts = self.store.parts()
        selected = next(p for p in parts if p['kind'] == 'screw')
        self.store.save({'selections': {'screw': selected}, 'inputs': {}})
        before = self.store.project()
        self.assertEqual(self.store.load_starter(), 0)
        self.assertEqual(self.store.project(), before)
        self.assertEqual(len(self.store.parts()), 6)

    def test_maximum_hole_is_not_exact_recommendation(self):
        self.store.load_starter()
        p = next(p for p in self.store.parts() if p['kind'] == 'heatset')
        result = evaluate(screw(length=8), p, {})
        checks = {c['name']: c['status'] for c in result['checks']}
        self.assertEqual(checks['Maximum installation hole'], 'fail')
        self.assertEqual(checks['Installation hole'], 'unknown')
        result = evaluate(screw(length=8), p, {'pilot': 4})
        self.assertEqual(next(c['status'] for c in result['checks'] if c['name'] == 'Maximum installation hole'), 'pass')
        self.assertEqual(result['status'], 'incomplete')

    def test_reach_bottoming_and_unknowns(self):
        def check(s, i, name):
            return next(c for c in evaluate(s, i, {})['checks'] if c['name'] == name)['status']
        self.assertEqual(check(screw(length=5), insert(), 'Screw reach'), 'fail')
        self.assertEqual(check(screw(length=10), insert(), 'Bottom clearance'), 'fail')
        self.assertEqual(check(screw(length=7), insert(), 'Bottom clearance'), 'pass')
        self.assertEqual(check(screw(length=7), insert(end_type='open'), 'Bottom clearance'), 'unknown')
        self.assertEqual(check(screw(length_convention='overall'), insert(), 'Screw reach'), 'unknown')
        self.assertEqual(check(screw(), insert(hole_profile='tapered'), 'Installation hole'), 'unknown')

    def test_axial_geometry_and_open_insert_overrun(self):
        project = {'inputs': {}, 'selections': {'screw': screw(length=10), 'heatset': insert(length=4.3, end_type='open')}}
        g = joint_geometry(project)
        self.assertAlmostEqual(g['reach'], 6.7)
        self.assertAlmostEqual(g['tip_beyond_insert'], 2.4)
        self.assertAlmostEqual(g['tip_to_bore_end'], 1.3)
        checks = evaluate(screw(length=12, threaded_length=12), insert(end_type='open'), {})['checks']
        self.assertEqual(next(c['status'] for c in checks if c['name'] == 'Open insert bore envelope'), 'fail')
        self.assertIsNone(joint_geometry({'inputs': {}, 'selections': {}})['screw_tip'])

    def test_draft_preview_never_changes_saved_project(self):
        self.store.import_parts([screw(), insert()])
        before = self.store.project()
        draft = self.store.draft({'selections': {'screw': {'id': 's', 'revision': 1}}, 'inputs': {'stack': 1}})
        self.assertEqual(joint_geometry(draft)['reach'], 5)
        self.assertEqual(self.store.project(), before)

    def test_assembly_assets_preserve_design_coordinates(self):
        model = json.loads((ROOT / 'assembly.json').read_text())
        self.assertEqual(model['units'], 'mm')
        parts = {p['id']: p for p in model['parts']}
        self.assertEqual(len(parts['tray']['triangles']), 10340)
        self.assertEqual(len(parts['faceplate']['triangles']), 1220)
        self.assertEqual(parts['tray']['bounds'], [[-56, 0, 7], [56, 82, 29]])
        self.assertEqual(parts['faceplate']['bounds'], [[-126, -3, 0], [126, 8, 42]])
        for p in parts.values():
            self.assertEqual(len(p['source_sha256']), 64)
            self.assertTrue(all(0 <= i < len(p['vertices']) for tri in p['triangles'] for i in tri))

    def test_hardware_envelopes_follow_actual_joint_axes(self):
        project = {'inputs': {}, 'selections': {'screw': screw(length=10, head_diameter=5.5, head_height=3), 'heatset': insert(length=4.3, outside_diameter=None)}}
        g = joint_geometry(project)
        shafts = [p for p in g['hardware_envelopes'] if p['kind'] == 'screw']
        self.assertEqual([p['x'] for p in shafts], [-40, 40])
        for p in shafts:
            self.assertEqual(p['z'], 21)
            self.assertAlmostEqual(p['y0'], 1.3)
            self.assertEqual(p['y1'], 11.3)
        self.assertEqual(len(g['hardware_guides']), 2)
        self.assertFalse(any(p['kind'] == 'insert' for p in g['hardware_envelopes']))
        self.assertAlmostEqual(g['hardware_guides'][0]['y1'], 8)
        self.assertAlmostEqual(g['hardware_guides'][0]['y0'], 3.7)
        project['selections']['heatset']['outside_diameter'] = 4.6
        self.assertEqual(len(joint_geometry(project)['hardware_guides']), 0)
        self.assertEqual(len(joint_geometry(project)['hardware_envelopes']), 6)

    def test_http_handlers_without_network(self):
        import io
        from types import SimpleNamespace
        handler_type = make_handler(self.store, 'test-token')
        def request(path, data=None, token='test-token', host='127.0.0.1:8765'):
            h = handler_type.__new__(handler_type)
            raw = json.dumps(data).encode() if data is not None else b''
            h.headers = {'Host': host, 'X-App-Token': token, 'Content-Length': str(len(raw))}
            h.server = SimpleNamespace(server_port=8765)
            h.path = path
            h.rfile = io.BytesIO(raw)
            h.wfile = io.BytesIO()
            h.request_version = 'HTTP/1.1'
            h.log_request = lambda *args: None
            h.do_GET() if data is None else h.do_POST()
            head, body = h.wfile.getvalue().split(b'\r\n\r\n', 1)
            return int(head.split()[1]), body.decode()
        code, html = request('/')
        self.assertEqual(code, 200)
        self.assertIn("const token='test-token'", html)
        self.assertEqual(request('/api/import', [screw()], token='wrong')[0], 403)
        self.assertEqual(request('/api/state', host='example.com')[0], 403)
        code, body = request('/api/import', [screw(), insert()])
        self.assertEqual(code, 200)
        self.assertEqual(len(json.loads(body)['parts']), 2)
        code, body = request('/api/save', {'selections': {'screw': {'id': 's', 'revision': 1}, 'heatset': {'id': 'i', 'revision': 1}}, 'inputs': {}})
        self.assertEqual(code, 200)
        self.assertEqual(len(json.loads(body)['selections']), 2)
        self.assertEqual(json.loads(request('/api/check', {})[1])['status'], 'fail')
        self.assertIn('Test screw', request('/api/bom')[1])
        self.assertEqual(json.loads(request('/api/project')[1])['units'], 'mm')
        self.assertAlmostEqual(json.loads(request('/api/geometry')[1])['reach'], 2.7)
        before = self.store.project()
        code, body = request('/api/preview', {'selections': {'screw': {'id': 's', 'revision': 1}}, 'inputs': {'stack': 1}})
        self.assertEqual(code, 200)
        self.assertEqual(json.loads(body)['reach'], 5)
        self.assertEqual(self.store.project(), before)
        self.assertEqual(request('/api/import', [screw(length=-3)])[0], 400)
        self.assertEqual(json.loads(request('/api/assembly')[1])['revision'], 'Pi4 clearance v2')
        self.assertIn('initAssemblyViewer', request('/viewer.js')[1])


if __name__ == '__main__':
    unittest.main()
