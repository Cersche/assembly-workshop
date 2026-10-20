import json
from pathlib import Path
import tempfile
import threading
import unittest
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from http.server import ThreadingHTTPServer
from faceplate_mounting import apply_default
from app import Store, evaluate, make_handler, validate_part, joint_geometry, ROOT, body_limit


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

    def test_model_uploads_get_a_larger_request_limit(self):
        self.assertGreaterEqual(body_limit('/api/step-to-stl'), 120_000_000)
        self.assertGreaterEqual(body_limit('/api/scad-to-stl'), 120_000_000)
        self.assertEqual(body_limit('/api/studio-save'), 2_000_000)

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


    def test_mesh_validation_and_bundle_path_rejection(self):
        import mesh_revision
        path = Path(self.tmp.name) / 'bad.stl'
        path.write_text('solid bad\nfacet normal 0 0 1\nouter loop\nvertex 0 0 0\nvertex 1 0 0\nvertex 0 1 0\nendloop\nendfacet\nendsolid')
        with self.assertRaisesRegex(ValueError, 'open or non-manifold'):
            mesh_revision.read_mesh(path, 'bad')
        with self.assertRaisesRegex(ValueError, 'Invalid revision'):
            mesh_revision.bundle('../other-file', self.tmp.name)


if __name__ == '__main__':
    unittest.main()
