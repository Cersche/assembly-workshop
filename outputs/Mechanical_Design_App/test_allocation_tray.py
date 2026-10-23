"""Option 1 data model: equipment facts on the library item, tray choices on each slot allocation.
Uses new disposable data only; nothing is rendered or exported."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

import equipment as eq
import rack_workspace

OLD_SPEC = {'name': 'Older item', 'dev_w': 85, 'dev_d': 56, 'dev_h': 20, 'device_mount': 'inserts', 'joint': 'screw',
            'holes': [[3.5, 3.5], [61.5, 49.5]], 'standoff': 5, 'insert_pilot': 3.4, 'board_t': 1.6,
            'keystones': [-100], 'rear_support': False, 'u': 2,
            'ports': [{'label': 'USB', 'x': 0, 'z': 20, 'w': 14, 'h': 8, 'r': 1}]}


def rack(placements):
    return {'version': 1, 'generation': None, 'racks': [
        {'id': 'rack-1', 'name': 'Test rack', 'slots': 5, 'width_mm': None, 'depth_mm': None, 'pitch_mm': None,
         'placements': placements}]}


class AllocationTray(unittest.TestCase):
    def test_keys_split_between_library_and_allocation(self):
        facts = eq.device_facts(OLD_SPEC)
        for key in ('name', 'dev_w', 'dev_d', 'dev_h', 'holes', 'ports'):
            self.assertIn(key, facts)
        for key in eq.PLACEMENT_KEYS:
            self.assertNotIn(key, facts)
        self.assertEqual(set(eq.PLACEMENT_KEYS), {'dev_off_x', 'dev_off_y', 'dev_rot', 'device_mount', 'standoff',
                                                  'insert_pilot', 'board_t', 'joint', 'keystones', 'rear_support', 'rear_openings', 'rear_style', 'u', 'front_position', 'front_setback', 'bezel', 'bezel_size', 'sleeve_top', 'feet_style', 'rear_floor_opening', 'insert_bosses'})

    def test_no_tray_settings_gives_identical_source(self):
        expected = eq.source(eq.clean(OLD_SPEC))
        for tray in (None, {}):
            self.assertEqual(eq.source(eq.clean(eq.allocation_spec(OLD_SPEC, tray))), expected)
        # Settings equal to the library values also give the same build identity.
        same = {k: OLD_SPEC[k] for k in eq.PLACEMENT_KEYS if k in OLD_SPEC}
        self.assertEqual(eq.source(eq.clean(eq.allocation_spec(OLD_SPEC, same))), expected)

    def test_allocation_values_override_library_defaults(self):
        spec = eq.allocation_spec(OLD_SPEC, {'standoff': 8, 'dev_rot': 90, 'dev_off_x': -5, 'keystones': [100]})
        s = eq.clean(spec)
        self.assertEqual((s['standoff'], s['dev_rot'], s['dev_off_x'], s['keystones']), (8, 90, -5, [100]))
        self.assertEqual((s['insert_pilot'], s['u'], s['holes']), (3.4, 2, [[3.5, 3.5], [61.5, 49.5]]))
        self.assertEqual(OLD_SPEC['standoff'], 5)  # library spec is not changed
        self.assertNotEqual(eq.source(s), eq.source(eq.clean(OLD_SPEC)))

    def test_unknown_keys_dropped_and_bad_values_rejected(self):
        self.assertEqual(eq.placement_settings({'dev_w': 999, 'name': 'x', 'u': 1}), {'u': 1})
        for bad in ([], {'u': 'two'}, {'rear_support': 1}, {'keystones': 5}, {'keystones': [True]},
                    {'joint': 3}, {'standoff': float('nan')}):
            with self.assertRaises(ValueError):
                eq.placement_settings(bad)
        # Range/combination checks still come from clean().
        with self.assertRaisesRegex(ValueError, 'retired'):
            eq.clean(eq.allocation_spec(OLD_SPEC, {'joint': 'snap'}))

    def test_rack_document_keeps_tray_per_allocation(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            value = rack([{'id': 'a', 'slot': 1, 'span': 2, 'equipment': 'eq-0123456789ab',
                           'tray': {'dev_off_x': 4, 'standoff': 7, 'extra': 1}},
                          {'id': 'b', 'slot': 3, 'span': 2, 'equipment': 'eq-0123456789ab'}])
            saved = rack_workspace.save(root, copy.deepcopy(value))
            first, second = saved['racks'][0]['placements']
            self.assertEqual(first['tray'], {'dev_off_x': 4, 'standoff': 7})
            self.assertNotIn('tray', second)  # older-style allocation: library spec values apply
            reread = rack_workspace.read(root)['racks'][0]['placements']
            self.assertEqual(reread[0]['tray'], {'dev_off_x': 4, 'standoff': 7})
            self.assertNotIn('tray', reread[1])
        bad = rack([{'id': 'a', 'slot': 1, 'span': 1, 'equipment': 'eq-0123456789ab', 'tray': {'u': 'x'}}])
        with self.assertRaises(ValueError):
            rack_workspace.validate(bad)

    def test_library_allocation_keeps_tray(self):
        out = rack_workspace.validate(rack([{'id': 'a', 'slot': 1, 'span': 1, 'equipment': 'eq-000000000004', 'tray': {'u': 3}}]))
        self.assertEqual(out['racks'][0]['placements'][0]['tray'], {'u': 3})

    def test_older_documents_validate_unchanged(self):
        value = rack([{'id': 'a', 'slot': 1, 'span': 1, 'equipment': 'eq-0123456789ab'}])
        out = rack_workspace.validate(copy.deepcopy(value))
        self.assertEqual(set(out['racks'][0]['placements'][0]), {'assembly', 'id', 'equipment', 'slot', 'span', 'geometry', 'fit'})


if __name__ == '__main__':
    unittest.main()

# Registered here because run_checks loads this module; no renders.
from test_faceplate_slot import FaceplateSlotTests
