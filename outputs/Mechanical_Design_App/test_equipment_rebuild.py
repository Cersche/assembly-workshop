"""Disposable library fixtures only; renderer mocked, no OpenSCAD/server/export."""
import copy
import hashlib
import io
import json
from pathlib import Path
import tempfile
import threading
import types
import unittest
from unittest.mock import patch

import app
import equipment as eq


class EquipmentRebuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.spec = eq.clean({'name': 'Router', 'dev_w': 85, 'dev_d': 56, 'dev_h': 20,
                              'device_mount': 'clips', 'joint': 'screw',
                              'ports': [{'x': -90, 'z': 20, 'w': 10, 'h': 8, 'type': 'usb-c', 'id': 'front-a'}],
                              'rear_ports': [{'x': 0, 'z': 20, 'type': 'rj45', 'id': 'rear-a', 'label': 'Uplink'}]})
        self.index = self.root / 'equipment-library.json'
        self.original = self.fixture_item(eq.source(self.spec).replace('plate_t=4;', 'plate_t=3;') + '// legacy fixture\n')
        # Deliberately compact: append must preserve original serialized records, not reformat them.
        self.index.write_text(json.dumps([self.original], separators=(',', ':')), encoding='utf-8')
        (self.root / 'rack-workspace.json').write_text(json.dumps({'placements': [{'equipment': self.original['id']}]}), encoding='utf-8')
        (self.root / 'rack-history').mkdir()
        (self.root / 'rack-history' / 'saved.json').write_bytes(b'fixture saved rack; pins unchanged')
        (self.root / 'library.sqlite3').write_bytes(b'fixture hardware sentinel, not a database')

    def write_build(self, spec, src):
        identity = hashlib.sha256(src.encode('utf-8')).hexdigest()
        folder = self.root / 'equipment-revisions' / identity
        if folder.exists():
            return folder
        folder.mkdir(parents=True)
        (folder / 'equipment.scad').write_bytes(src.encode('utf-8'))
        parts = ['tray', 'faceplate']
        hashes = {}
        for part in parts:
            raw = ('synthetic integrity fixture ' + part).encode('utf-8')
            (folder / (part + '.stl')).write_bytes(raw)
            hashes[part + '.stl'] = hashlib.sha256(raw).hexdigest()
        (folder / 'revision.json').write_text(json.dumps({'id': identity, 'spec': spec, 'parts': parts,
                                                       'sha256': hashes, 'template': 'legacy descriptive label'}), encoding='utf-8')
        return folder

    def fixture_item(self, src):
        folder = self.write_build(self.spec, src)
        return {'id': 'eq-0123456789ab', 'name': self.spec['name'], 'span': 1, 'spec': copy.deepcopy(self.spec),
                'build': folder.name, 'parts': ['tray', 'faceplate'], 'status': 'PROPOSED — UNVALIDATED'}

    def fake_render(self, spec, data_dir):
        self.assertEqual(Path(data_dir), self.root)
        return self.write_build(eq.clean(spec), eq.source(eq.clean(spec)))

    def snapshot(self):
        return {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}

    def rebuild(self):
        return eq.rebuild_copy(self.root, self.original['id'], self.original['build'])

    def test_status_is_read_only_legacy_array_older_source(self):
        before = self.snapshot()
        with patch.object(eq, 'render', side_effect=AssertionError('must not render')):
            self.assertEqual(eq.library(self.root), [self.original])
            result = eq.template_status(self.root, self.original)
        self.assertEqual(result['status'], 'older_source')
        self.assertIn('Change details unavailable', result['reason'])
        self.assertEqual(before, self.snapshot())

    def test_old_keystone_and_arbitrary_source_flag_without_inventing_reason(self):
        for source in [eq.source(self.spec).replace('ks_w=14.8;', 'ks_w=14.5;'), '// unknown legacy source\n']:
            item = self.fixture_item(source)
            self.assertEqual(eq.template_status(self.root, item)['status'], 'older_source')
            self.assertIn('Change details unavailable', eq.template_status(self.root, item)['reason'])

    def test_current_source_reports_unknown_pipeline_and_still_rebuilds_copy(self):
        self.original = self.fixture_item(eq.source(self.spec))
        self.index.write_text(json.dumps([self.original]), encoding='utf-8')
        self.assertEqual(eq.template_status(self.root, self.original)['status'], 'matches_source_unknown_pipeline')
        with patch.object(eq, 'render', side_effect=self.fake_render) as render:
            out = self.rebuild()
        self.assertTrue(out['reused_build'])
        self.assertNotEqual(out['item']['id'], self.original['id'])
        self.assertEqual(out['item']['build'], self.original['build'])
        render.assert_called_once()

    def test_missing_malformed_and_tampered_evidence_are_separate_states(self):
        folder = self.root / 'equipment-revisions' / self.original['build']
        manifest = folder / 'revision.json'; saved = manifest.read_bytes()
        for raw in [b'not JSON', b'{}']:
            manifest.write_bytes(raw)
            self.assertEqual(eq.template_status(self.root, self.original)['status'], 'unknown_evidence')
        manifest.write_bytes(saved)
        missing = {**self.original, 'build': '0' * 64}
        self.assertEqual(eq.template_status(self.root, missing)['status'], 'unknown_evidence')
        (folder / 'tray.stl').write_bytes(b'tampered')
        self.assertEqual(eq.template_status(self.root, self.original)['status'], 'integrity_problem')
        before = self.index.read_bytes()
        with self.assertRaisesRegex(ValueError, 'integrity'):
            self.rebuild()
        self.assertEqual(before, self.index.read_bytes())

    def test_wrong_source_hash_and_manifest_id_are_integrity_problems(self):
        folder = self.root / 'equipment-revisions' / self.original['build']
        source = folder / 'equipment.scad'; saved = source.read_bytes()
        source.write_bytes(saved + b'changed')
        self.assertEqual(eq.template_status(self.root, self.original)['status'], 'integrity_problem')
        source.write_bytes(saved)
        manifest = folder / 'revision.json'; report = json.loads(manifest.read_text(encoding='utf-8'))
        report['id'] = '0' * 64; manifest.write_text(json.dumps(report), encoding='utf-8')
        self.assertEqual(eq.template_status(self.root, self.original)['status'], 'integrity_problem')

    def test_invalid_snap_and_keystone_specs_need_review_without_substitution(self):
        for changes, reason in [({'joint': 'snap'}, 'retired'), ({'keystones': [60]}, 'collar')]:
            item = copy.deepcopy(self.original); item['spec'].update(changes)
            self.index.write_text(json.dumps([item]), encoding='utf-8'); before = self.snapshot()
            result = eq.template_status(self.root, item)
            self.assertEqual(result['status'], 'needs_review'); self.assertIn(reason, result['reason'])
            with patch.object(eq, 'render', side_effect=AssertionError('must not render')):
                with self.assertRaisesRegex(ValueError, reason): self.rebuild()
            self.assertEqual(before, self.snapshot())

    def test_copy_preserves_original_build_records_placements_and_planning_ports(self):
        before = self.snapshot(); original_record = json.dumps(self.original, separators=(',', ':')).encode('utf-8')
        with patch.object(eq, 'render', side_effect=self.fake_render): out = self.rebuild()
        item = out['item']; items = eq.library(self.root)
        self.assertEqual(items[0], self.original); self.assertIn(original_record, self.index.read_bytes())
        self.assertEqual(len(items), 2); self.assertNotEqual(item['build'], self.original['build'])
        self.assertEqual(item['rebuilt_from_item'], self.original['id']); self.assertEqual(item['rebuilt_from_build'], self.original['build'])
        self.assertEqual(item['display_name'], 'Router (current template copy)')
        self.assertEqual(item['spec'], self.spec); self.assertEqual(item['spec']['name'], 'Router')
        for name, raw in before.items():
            if name != 'equipment-library.json': self.assertEqual((self.root / name).read_bytes(), raw)
        self.assertEqual(eq.template_status(self.root, item)['status'], 'matches_source_unknown_pipeline')
        placed = json.loads((self.root / 'rack-workspace.json').read_text(encoding='utf-8'))['placements'][0]['equipment']
        self.assertEqual(next(i['build'] for i in items if i['id'] == placed), self.original['build'])

    def test_planning_only_metadata_does_not_change_source_name_only_change_does(self):
        s = copy.deepcopy(self.spec); s['rear_ports'][0]['label'] = 'Renamed'; s['ports'][0]['type'] = 'rj45'
        self.assertEqual(eq.source(eq.clean(s)), eq.source(self.spec))
        s['name'] = 'Different name'; self.assertNotEqual(eq.source(eq.clean(s)), eq.source(self.spec))

    def test_copy_normal_edit_persists_display_rename_without_source_name_suffix(self):
        with patch.object(eq, 'render', side_effect=self.fake_render):
            item = self.rebuild()['item']
        draft = {**item['spec'], 'id': item['id'], 'display_name': 'Renamed copy'}
        # Mock the existing build/report boundary, producing no ZIP or geometry.
        with patch.object(eq, 'build', return_value=b'fixture only') as build, patch.object(eq.zipfile, 'ZipFile') as archive:
            archive.return_value.__enter__.return_value.read.return_value = json.dumps({'id': item['build'], 'parts': item['parts']}).encode('utf-8')
            saved = eq.save_item(draft, self.root)
        self.assertEqual(saved['display_name'], 'Renamed copy'); self.assertEqual(saved['name'], 'Renamed copy')
        self.assertEqual(saved['spec']['name'], 'Router'); self.assertEqual(saved['rebuilt_from_item'], self.original['id'])
        self.assertEqual(build.call_args.args[0]['name'], 'Router')
        self.assertEqual(eq.library(self.root)[0], self.original)

    def test_render_failure_or_index_failure_preserves_original_index(self):
        before = self.index.read_bytes()
        for reason in ['Fixture renderer timeout', 'Fixture mesh rejection']:
            with patch.object(eq, 'render', side_effect=ValueError(reason)):
                with self.assertRaisesRegex(ValueError, reason): self.rebuild()
            self.assertEqual(self.index.read_bytes(), before)
        with patch.object(eq, 'render', side_effect=self.fake_render), patch.object(Path, 'replace', side_effect=OSError('Fixture index failure')):
            with self.assertRaisesRegex(OSError, 'index failure'): self.rebuild()
        self.assertEqual(self.index.read_bytes(), before)
        self.assertTrue((self.root / 'equipment-revisions' / hashlib.sha256(eq.source(self.spec).encode('utf-8')).hexdigest()).exists())

    def test_duplicate_and_double_click_requests_append_one_copy(self):
        results = []; errors = []
        def worker():
            try: results.append(self.rebuild())
            except Exception as exc: errors.append(exc)
        with patch.object(eq, 'render', side_effect=self.fake_render) as render:
            threads = [threading.Thread(target=worker) for _ in range(2)]
            for t in threads: t.start()
            for t in threads: t.join(timeout=5)
            self.assertFalse(any(t.is_alive() for t in threads)); self.assertEqual(errors, [])
            again = self.rebuild()
        self.assertEqual(len(results), 2); self.assertEqual(results[0]['item']['id'], results[1]['item']['id'])
        self.assertEqual(again['item']['id'], results[0]['item']['id'])
        self.assertEqual(len(eq.library(self.root)), 2); render.assert_called_once()

    def test_stale_missing_or_invalid_identity_rejected_before_render(self):
        before = self.index.read_bytes()
        with patch.object(eq, 'render', side_effect=AssertionError('must not render')):
            for ident, build in [('eq-ffffffffffff', self.original['build']), (self.original['id'], '0' * 64), ('../escape', self.original['build'])]:
                with self.assertRaises(ValueError): eq.rebuild_copy(self.root, ident, build)
        self.assertEqual(before, self.index.read_bytes())

    def test_changed_original_during_render_is_not_published(self):
        def render(spec, data):
            result = self.fake_render(spec, data)
            latest = eq.library(self.root); latest[0]['name'] = 'Concurrent edit'
            self.index.write_text(json.dumps(latest), encoding='utf-8')
            return result
        with patch.object(eq, 'render', side_effect=render):
            with self.assertRaisesRegex(ValueError, 'changed while rebuilding'): self.rebuild()
        self.assertEqual(len(eq.library(self.root)), 1); self.assertEqual(eq.library(self.root)[0]['name'], 'Concurrent edit')

    def test_corrupt_current_target_blocks_reuse_without_overwrite(self):
        folder = self.write_build(self.spec, eq.source(self.spec)); (folder / 'tray.stl').write_bytes(b'bad target')
        before = self.snapshot()
        with patch.object(eq, 'render', side_effect=AssertionError('must not render')):
            with self.assertRaisesRegex(ValueError, 'target cache'): self.rebuild()
        self.assertEqual(before, self.snapshot())

    def request(self, route, body=None, token='token', host=True):
        cls = app.make_handler(types.SimpleNamespace(path=self.root / 'library.sqlite3'), 'token')
        h = cls.__new__(cls); h.path = route; h.valid_host = lambda: host; h.headers = {}
        results = []; h.send = lambda value, status=200, mime='application/json': results.append((value, status))
        if body is None: h.do_GET()
        else:
            raw = json.dumps(body).encode('utf-8'); h.rfile = io.BytesIO(raw)
            h.headers = {'X-App-Token': token, 'Content-Length': str(len(raw))}; h.do_POST()
        return results[0]

    def test_status_and_rebuild_routes_preserve_array_contract_and_token_guard(self):
        before = self.snapshot()
        values, status = self.request('/api/equipment-library'); self.assertEqual(status, 200); self.assertIsInstance(values, list)
        statuses, status = self.request('/api/equipment-template-status'); self.assertEqual(status, 200)
        self.assertEqual(statuses[self.original['id']]['status'], 'older_source'); self.assertEqual(before, self.snapshot())
        payload = {'id': self.original['id'], 'expected_build': self.original['build']}
        with patch.object(eq, 'render', side_effect=self.fake_render) as render:
            _, status = self.request('/api/equipment-rebuild-copy', payload, token='wrong'); self.assertEqual(status, 403); render.assert_not_called()
            _, status = self.request('/api/equipment-rebuild-copy', payload, host=False); self.assertEqual(status, 403); render.assert_not_called()
            out, status = self.request('/api/equipment-rebuild-copy', payload); self.assertEqual(status, 200)
        self.assertNotEqual(out['item']['id'], self.original['id'])


if __name__ == '__main__':
    unittest.main()
