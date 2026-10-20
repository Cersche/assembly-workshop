"""Rack document tests use only newly created temporary data."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

import rack_workspace
import equipment
from equipment_examples import EXAMPLE_ID, example_item


class RetiredEquipmentMigrationTests(unittest.TestCase):
    def test_saved_shape_migrates_as_unsaved_draft_with_exact_history(self):
        import uuid
        import assembly_records
        # Synthetic copy of the documented v2 shape; no actual user data is read.
        record = assembly_records.normalize({'id': 'asm-12345678', 'name': 'Saved board', 'revision': 7,
            'project': {'selections': {'screw': {'id': 'pinned', 'revision': 3}},
                        'inputs': {'pilot': 4}, 'reference': {'historical': True}},
            'appearance': {'tray': '#123456', 'artwork': {'sha256': 'a' * 64, 'name': 'Saved image'}}}, 'r', 'p')
        old = {'version': 2, 'generation': str(uuid.uuid4()), 'racks': [{'id': 'r', 'name': 'Saved rack',
            'slots': 5, 'placements': [{'id': 'p', 'equipment': 'pi4', 'slot': 2, 'span': 2,
                'geometry': 'pi4-clearance-v2-reference', 'assembly': record}],
            'cabling': {'ports': [{'allocation': 'p', 'port': 'ethernet', 'face': 'rear', 'x': 39}],
                        'guides': []}}]}
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            path = root / 'rack-workspace.json'
            raw = json.dumps(old, ensure_ascii=False, indent=1).encode('utf-8')
            path.write_bytes(raw)
            draft = rack_workspace.read(root)
            self.assertTrue(draft['migration_pending'])
            p = draft['racks'][0]['placements'][0]
            self.assertEqual(p['equipment'], EXAMPLE_ID)
            self.assertEqual(p['geometry'], 'equipment-library')
            self.assertEqual(p['assembly'], record)
            port = next(o for o in draft['racks'][0]['cabling']['ports'] if o['port'] == 'ethernet')
            self.assertEqual((port['face'], port['x'], port['z']), ('rear', 39, 24.4 + 44.45))
            self.assertEqual(path.read_bytes(), raw)
            history = root / 'rack-history' / (old['generation'] + '.json')
            self.assertEqual(history.read_bytes(), raw)
            self.assertEqual(rack_workspace.read(root), draft)  # idempotent without saving
            saved = rack_workspace.save(root, draft)
            self.assertNotIn('migration_pending', saved)
            self.assertNotEqual(saved['generation'], old['generation'])
            self.assertEqual(history.read_bytes(), raw)
            self.assertEqual(rack_workspace.read(root), saved)

    def test_example_is_generic_and_library_read_has_no_side_effect(self):
        with tempfile.TemporaryDirectory() as folder:
            items = equipment.library(folder)
            self.assertEqual(items, [example_item()])
            self.assertEqual(list(Path(folder).iterdir()), [])
            self.assertTrue(equipment.check_allocation(folder, {'item': EXAMPLE_ID})['ok'])
            self.assertEqual(len(equipment.clean(items[0]['spec'])['planning_ports']), 9)
            source = equipment.source(equipment.clean(items[0]['spec']))
            self.assertNotIn('planning_ports', source)
            self.assertNotIn('usb-c-power', source)

    def test_history_disagreement_blocks_migration_without_overwrite(self):
        import uuid
        generation = str(uuid.uuid4())
        value = {'version': 2, 'generation': generation, 'racks': [{'id': 'r', 'name': 'Rack',
            'slots': 1, 'placements': [{'id': 'p', 'equipment': 'pi4', 'slot': 1, 'span': 1}]}]}
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            raw = json.dumps(value).encode('utf-8')
            (root / 'rack-workspace.json').write_bytes(raw)
            (root / 'rack-history').mkdir()
            history = root / 'rack-history' / (generation + '.json')
            history.write_bytes(b'preserve this history')
            with self.assertRaisesRegex(ValueError, 'Recovery history differs'):
                rack_workspace.read(root)
            self.assertEqual(history.read_bytes(), b'preserve this history')
            self.assertEqual((root / 'rack-workspace.json').read_bytes(), raw)


class RackWorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.value = {'version': 1, 'generation': None, 'racks': [
            {'id': 'rack-1', 'name': 'Custom rack', 'slots': 5, 'width_mm': None,
             'depth_mm': None, 'pitch_mm': None, 'placements': []}]}

    def test_empty_read_has_no_side_effect(self):
        self.assertEqual(rack_workspace.read(self.root)['racks'], [])
        self.assertEqual(list(self.root.iterdir()), [])

    def test_round_trip_unknown_dimensions_and_historical_recovery(self):
        library = self.root / 'library.sqlite3'
        library.write_bytes(b'untouched hardware data')
        first = rack_workspace.save(self.root, self.value)
        changed = copy.deepcopy(first)
        changed['racks'][0]['width_mm'] = 260
        second = rack_workspace.save(self.root, changed)
        self.assertNotEqual(first['generation'], second['generation'])
        history = self.root / 'rack-history' / (first['generation'] + '.json')
        self.assertEqual(json.loads(history.read_text(encoding='utf-8')), first)
        self.assertEqual(rack_workspace.read(self.root), second)
        self.assertIsNone(second['racks'][0]['depth_mm'])
        self.assertEqual(library.read_bytes(), b'untouched hardware data')

    def test_stale_writer_rejected_without_changes(self):
        rack_workspace.save(self.root, self.value)
        before = (self.root / 'rack-workspace.json').read_bytes()
        with self.assertRaisesRegex(ValueError, 'another session'):
            rack_workspace.save(self.root, self.value)
        self.assertEqual((self.root / 'rack-workspace.json').read_bytes(), before)

    def test_overlap_and_out_of_range_rejected(self):
        placement = {'id': 'p1', 'slot': 2, 'span': 2, 'equipment': 'eq-000000000004'}
        self.value['racks'][0]['placements'] = [placement, dict(placement, id='p2', slot=3)]
        with self.assertRaisesRegex(ValueError, 'overlap'):
            rack_workspace.save(self.root, self.value)
        self.assertFalse((self.root / 'rack-workspace.json').exists())
        self.value['racks'][0]['placements'] = [dict(placement, slot=5)]
        with self.assertRaisesRegex(ValueError, 'outside'):
            rack_workspace.validate(self.value)

    def test_invalid_dimensions_and_equipment(self):
        for value in (-1, 0, float('nan'), float('inf'), True, '250'):
            self.value['racks'][0]['width_mm'] = value
            with self.assertRaises(ValueError):
                rack_workspace.validate(self.value)
        self.value['racks'][0]['width_mm'] = None
        self.value['racks'][0]['placements'] = [{'id': 'p1', 'slot': 1, 'span': 1, 'equipment': 'unsupported'}]
        with self.assertRaisesRegex(ValueError, 'Unknown equipment type'):
            rack_workspace.validate(self.value)
        # Wizard-built library equipment (eq- ids) is accepted as generic equipment.
        self.value['racks'][0]['placements'] = [{'id': 'p1', 'slot': 1, 'span': 1, 'equipment': 'eq-0123456789ab'}]
        rack_workspace.validate(self.value)

    def test_cable_guides_round_trip_and_reject_invalid(self):
        rack = self.value['racks'][0]
        rack['cabling'] = {'guides': [{'id': 'g1', 'post': 'RL', 'slot': 2}, {'id': 'g2', 'post': 'RR', 'slot': 2}]}
        saved = rack_workspace.save(self.root, self.value)
        self.assertEqual(saved['racks'][0]['cabling']['guides'][0], {'id': 'g1', 'kind': 'labrax-cable-guide', 'post': 'RL', 'slot': 2})
        self.assertEqual(rack_workspace.read(self.root)['racks'][0]['cabling'], saved['racks'][0]['cabling'])
        # Racks without cabling data stay unchanged.
        del rack['cabling']
        self.assertNotIn('cabling', rack_workspace.validate(self.value)['racks'][0])
        for guides, message in (([{'id': 'g', 'post': 'XX', 'slot': 1}], 'post FL'),
                                ([{'id': 'g', 'post': 'RL', 'slot': 6}], 'inside the rack'),
                                ([{'id': 'g', 'post': 'RL', 'slot': True}], 'inside the rack'),
                                ([{'id': 'a', 'post': 'RL', 'slot': 1}, {'id': 'b', 'post': 'RL', 'slot': 1}], 'already has'),
                                ([{'id': 'a', 'post': 'RL', 'slot': 1}, {'id': 'a', 'post': 'RR', 'slot': 1}], 'unique'),
                                ([{'id': 'g', 'post': 'RL', 'slot': 1, 'kind': 'zip-tie'}], 'type')):
            rack['cabling'] = {'guides': guides}
            with self.assertRaisesRegex(ValueError, message):
                rack_workspace.validate(self.value)
        rack['cabling'] = {'guides': [], 'unknown_field': []}
        with self.assertRaisesRegex(ValueError, 'Invalid cable'):
            rack_workspace.validate(self.value)

    def test_assignment_retains_unknown_fit(self):
        self.value['racks'][0]['placements'] = [{'id': 'p1', 'slot': 1, 'span': 1,
                                                'equipment': 'eq-000000000004', 'fit': 'PASS'}]
        saved = rack_workspace.save(self.root, self.value)
        self.assertEqual(saved['racks'][0]['placements'][0]['fit'], 'UNKNOWN')

    def test_history_lists_and_restores_draft_without_writing(self):
        self.value['racks'][0]['placements'] = [{'id': 'p1', 'slot': 1, 'span': 1, 'equipment': 'eq-000000000004'}]
        first = rack_workspace.save(self.root, self.value)
        moved = copy.deepcopy(first)
        moved['racks'][0]['placements'][0]['slot'] = 3
        moved['racks'][0]['name'] = 'Renamed'
        second = rack_workspace.save(self.root, moved)
        files = lambda: sorted((p.name, p.read_bytes()) for p in self.root.rglob('*') if p.is_file())
        before = files()
        entries = rack_workspace.list_history(self.root)
        self.assertEqual([e['generation'] for e in entries], [first['generation']])
        self.assertEqual(entries[0]['racks'][0]['allocations'][0]['slot'], 1)
        restored = rack_workspace.restore_rack(self.root, first['generation'], 'rack-1')
        self.assertEqual((restored['name'], restored['placements'][0]['slot']), ('Custom rack', 1))
        self.assertEqual(restored['placements'][0]['assembly'], second['racks'][0]['placements'][0]['assembly'])
        self.assertEqual(files(), before)
        draft = dict(second, racks=[restored])
        self.assertEqual(rack_workspace.save(self.root, draft)['racks'][0]['placements'][0]['slot'], 1)
        with self.assertRaisesRegex(ValueError, 'Unknown saved version'):
            rack_workspace.restore_rack(self.root, '../rack-workspace', 'rack-1')
        with self.assertRaisesRegex(ValueError, 'not in the selected'):
            rack_workspace.restore_rack(self.root, first['generation'], 'other')

    def test_malformed_history_generation_cannot_be_used_as_path(self):
        value = dict(self.value, generation='../elsewhere')
        (self.root / 'rack-workspace.json').write_text(json.dumps(value), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'generation'):
            rack_workspace.read(self.root)


if __name__ == '__main__':
    unittest.main()
