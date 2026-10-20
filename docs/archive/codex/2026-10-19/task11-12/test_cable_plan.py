"""Cable save validation on new temporary data only; no builds or exports."""
import copy
from pathlib import Path
import tempfile
import unittest

import cable_plan
import rack_workspace


def plan():
    return {'guides': [{'id': 'g1', 'kind': 'labrax-cable-guide', 'post': 'RR', 'slot': 2}],
            'ports': [{'allocation': 'p1', 'port': 'ethernet', 'face': 'rear'}],
            'exits': [{'id': 'e1', 'position': 'bottom-rear', 'slot': 6}],
            'endpoints': [{'id': 'out1', 'kind': 'wall-jack', 'name': 'Office'}],
            'cables': [{'id': 'c1', 'number': 'C1', 'type': 'rj45', 'color': '#3fb6ff',
                        'service_loop_m': 0.15, 'from': {'allocation': 'p1', 'port': 'ethernet'},
                        'to': {'endpoint': 'out1'}, 'face_assumed': 'rear', 'route_changed': False,
                        'route': {'mode': 'auto', 'guides': ['g1'], 'exit': 'e1'}, 'note': 'Planning only'}],
            'settings': {'guide_warn_above': 6, 'service_loop_m': 0.15}}


class CablePlanTests(unittest.TestCase):
    def check(self, value):
        return cable_plan.validate(value, 6, {'p1': 1}, {'g1'})

    def test_round_trip_and_legacy(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            value = {'version': 1, 'generation': None, 'racks': [
                {'id': 'r1', 'name': 'Test rack', 'slots': 6,
                 'placements': [{'id': 'p1', 'slot': 1, 'span': 1, 'equipment': 'pi4', 'fit': 'UNKNOWN'}],
                 'cabling': plan()}]}
            saved = rack_workspace.save(root, value)
            self.assertEqual(saved['racks'][0]['cabling'], plan())
            self.assertEqual(rack_workspace.read(root), saved)
            legacy = {key: plan()[key] for key in ('guides', 'ports')}
            saved['racks'][0]['cabling'] = legacy
            saved = rack_workspace.save(root, saved)
            self.assertEqual(saved['racks'][0]['cabling'], legacy)
            self.assertEqual(rack_workspace.read(root), saved)
            del saved['racks'][0]['cabling']
            saved = rack_workspace.save(root, saved)
            self.assertNotIn('cabling', saved['racks'][0])

    def test_valid_boundaries_and_defaults(self):
        self.assertEqual(self.check({}), {})
        self.assertEqual(self.check({'settings': {}})['settings'], plan()['settings'])
        value = plan()
        value['exits'] = []
        value['cables'][0]['route']['exit'] = None
        self.check(value)  # Outside endpoint with no exit is a UI warning only.
        value['cables'][0]['from'] = value['cables'][0]['to'] = None
        self.check(value)
        value['cables'][0]['to'] = {'endpoint': 'out1'}
        other = copy.deepcopy(value['cables'][0])
        other.update(id='c2', number='C2')
        value['cables'].append(other)
        self.check(value)  # Many cables may use the same outside endpoint.
        value['cables'][0]['from'] = {'allocation': 'p1', 'port': 'library-only'}
        self.check(value)  # Port existence belongs to the library/draft upkeep.
        for loop in (0, 2):
            value['cables'][0]['service_loop_m'] = loop
            self.check(value)
        value['endpoints'][0]['id'] = ' endpoint with spaces '
        for cable in value['cables']:
            cable['to']['endpoint'] = ' endpoint with spaces '
        self.assertEqual(self.check(value)['endpoints'][0]['id'], ' endpoint with spaces ')

    def test_unknown_guide_fields_rejected(self):
        value = plan()
        value['guides'][0]['unknown'] = True
        with self.assertRaisesRegex(ValueError, 'known fields'):
            rack_workspace._cabling(value, 6, {'p1': 1})

    def test_rejections(self):
        cases = []

        def case(path, replacement):
            value = plan()
            target = value
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = replacement
            cases.append((str(path) + '=' + repr(replacement)[:60], value))

        for key, limit in (('exits', 32), ('endpoints', 50), ('cables', 200)):
            case([key], {})
            case([key], [plan()[key][0]] * (limit + 1))
            case([key], [plan()[key][0]] * 2)
            case([key, 0, 'id'], '')
            case([key, 0, 'id'], 'x' * 81)
            case([key, 0, 'extra'], True)
            case([key, 0], 'invalid')
        case(['unknown'], [])
        for slot in (True, 0, 7, 1.5, float('nan'), float('inf')):
            case(['exits', 0, 'slot'], slot)
        case(['exits', 0, 'position'], 'front')
        case(['exits'], [plan()['exits'][0], {**plan()['exits'][0], 'id': 'e2'}])
        case(['endpoints', 0, 'kind'], 'unknown')
        for name in ('   ', 'x' * 61, None):
            case(['endpoints', 0, 'name'], name)
        for number in ('', 'x' * 13, None):
            case(['cables', 0, 'number'], number)
        duplicate = copy.deepcopy(plan()['cables'][0])
        duplicate.update(id='c2', number='C2')
        case(['cables'], [plan()['cables'][0], duplicate])  # Duplicate port across cables.
        duplicate.update(number='C1', **{'from': None})
        case(['cables'], [plan()['cables'][0], duplicate])  # Duplicate number.
        for field, val in (('type', 'scsi'), ('color', '#12345g'), ('color', None),
                           ('face_assumed', 'front'), ('route_changed', 1), ('note', 'x' * 201)):
            case(['cables', 0, field], val)
        for end in ({'allocation': 'gone', 'port': 'p'}, {'allocation': [], 'port': 'p'},
                    {'allocation': 'p1', 'port': 'Bad Port'}, {'endpoint': 'gone'},
                    {'endpoint': []}, {'allocation': 'p1'}, {'endpoint': 'out1', 'extra': 1}, [],
                    {'allocation': 'p1', 'port': 'p', 'endpoint': 'out1'}):
            case(['cables', 0, 'from'], end)
        case(['cables', 0, 'from'], {'endpoint': 'out1'})  # Same endpoint at both ends.
        case(['cables', 0, 'to'], {'allocation': 'p1', 'port': 'ethernet'})
        for field, val in (('mode', 'other'), ('guides', ['gone']), ('guides', ['g1', 'g1']),
                           ('guides', ['g1'] * 49), ('guides', {}), ('guides', [[]]),
                           ('exit', 'gone'), ('exit', []), ('extra', True)):
            case(['cables', 0, 'route', field], val)
        for val in (True, -0.1, 2.1, float('nan'), float('inf'), '0.15', 10**400):
            case(['cables', 0, 'service_loop_m'], val)
            case(['settings', 'service_loop_m'], val)
        for val in (True, 0, 51, 1.5):
            case(['settings', 'guide_warn_above'], val)
        case(['settings', 'extra'], 1)
        case(['settings'], [])
        for path in (['cables', 0, 'from'], ['cables', 0, 'to'], ['cables', 0, 'route', 'exit']):
            value = plan()
            target = value
            for key in path[:-1]:
                target = target[key]
            del target[path[-1]]
            cases.append(('missing ' + str(path), value))
        for label, value in cases:
            with self.subTest(case=label), self.assertRaises(ValueError):
                self.check(value)


if __name__ == '__main__':
    unittest.main()
