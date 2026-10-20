"""Cable management Step 2 port data tests. Temporary data only; no builds, no exports."""
import copy
from pathlib import Path
import tempfile
import unittest

import equipment
import rack_workspace


class CablePortTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.value = {'version': 1, 'generation': None, 'racks': [
            {'id': 'rack-1', 'name': 'Ports rack', 'slots': 5, 'width_mm': None, 'depth_mm': None, 'pitch_mm': None,
             'placements': [{'id': 'p1', 'slot': 1, 'span': 1, 'equipment': 'pi4', 'fit': 'UNKNOWN'},
                            {'id': 'p2', 'slot': 3, 'span': 2, 'equipment': 'pi4', 'fit': 'UNKNOWN'}]}]}

    def test_port_edits_round_trip(self):
        ports = [{'allocation': 'p1', 'port': 'ethernet', 'face': 'rear', 'x': 44.2, 'y': 58.75, 'z': 24.4},
                 {'allocation': 'p1', 'port': 'usb-c-power', 'label': '  Power  ', 'type': 'usb-c'},
                 {'allocation': 'p2', 'port': 'custom-ab12cd', 'custom': True, 'label': 'Fan', 'type': 'dc-barrel',
                  'face': 'rear', 'x': 0, 'y': 70, 'z': 80.123456}]
        self.value['racks'][0]['cabling'] = {'ports': ports}
        saved = rack_workspace.save(self.root, self.value)
        out = saved['racks'][0]['cabling']['ports']
        self.assertEqual(out[0], ports[0])
        self.assertEqual(out[1]['label'], 'Power')
        self.assertEqual(out[2]['z'], 80.123)
        self.assertIs(out[2]['custom'], True)
        self.assertNotIn('custom', out[0])
        self.assertEqual(rack_workspace.read(self.root)['racks'][0]['cabling'], saved['racks'][0]['cabling'])

    def test_port_edits_rejected(self):
        good = {'allocation': 'p1', 'port': 'hdmi0', 'face': 'front'}
        cases = (('nope', 'must be a list'),
                 ([{**good, 'colour': 'red'}], 'known fields'),
                 ([{**good, 'allocation': 'gone'}], 'not in this rack'),
                 ([{**good, 'port': 'Bad Id'}], 'lowercase'),
                 ([good, dict(good)], 'twice'),
                 ([{**good, 'type': 'scsi'}], 'connector type'),
                 ([{**good, 'face': 'top'}], 'front or rear'),
                 ([{**good, 'x': 151}], 'X must'),
                 ([{**good, 'z': 60}], 'Z must'),  # 1U allocation: Z up to 54.45
                 ([{**good, 'y': float('nan')}], 'Y must'),
                 ([{**good, 'x': True}], 'X must'),
                 ([{**good, 'label': 'x' * 41}], 'labels'),
                 ([{'allocation': 'p1', 'port': 'hdmi0'}], 'change something'),
                 ([{**good, 'custom': 'yes'}], 'true or false'),
                 ([{**good, 'custom': True}], 'custom port needs'),
                 ([{'allocation': 'p1', 'port': f'c-{i}', 'face': 'rear'} for i in range(65)], 'at most 64'))
        rack = self.value['racks'][0]
        for ports, message in cases:
            rack['cabling'] = {'ports': ports}
            with self.subTest(message=message), self.assertRaisesRegex(ValueError, message):
                rack_workspace.validate(self.value)
        # A 2U allocation accepts the taller Z.
        rack['cabling'] = {'ports': [{**good, 'allocation': 'p2', 'z': 60}]}
        self.assertEqual(rack_workspace.validate(self.value)['racks'][0]['cabling']['ports'][0]['z'], 60)


def wizard_spec(**extra):
    spec = {'name': 'Switch', 'dev_w': 100, 'dev_d': 80, 'dev_h': 20, 'u': 1, 'device_mount': 'inserts', 'joint': 'screw',
            'holes': [[5, 5]], 'keystones': [], 'ports': [{'label': 'LAN', 'x': 0, 'z': 20, 'w': 15, 'h': 8, 'r': 1}]}
    spec.update(extra)
    return spec


class WizardPortTests(unittest.TestCase):
    def test_type_ids_and_rear_ports(self):
        s = equipment.clean(wizard_spec(rear_ports=[{'label': 'Power', 'type': 'iec', 'x': -40, 'z': 20},
                                                    {'id': 'p-abc123', 'label': 'Fan', 'x': 10, 'z': 5}]))
        self.assertEqual(s['ports'][0]['type'], 'other')
        self.assertEqual(s['ports'][0]['id'], 'front-1')
        self.assertEqual(s['rear_ports'], [{'id': 'rear-1', 'label': 'Power', 'type': 'iec', 'x': -40, 'z': 20},
                                           {'id': 'p-abc123', 'label': 'Fan', 'type': 'other', 'x': 10, 'z': 5}])
        self.assertEqual(equipment.clean(wizard_spec())['rear_ports'], [])
        # Keystone ids are reserved for the pass-through pairs; such an id falls back to the position id.
        kept = equipment.clean(wizard_spec(ports=[{'id': 'ks-1-front', 'x': 0, 'z': 20, 'w': 15, 'h': 8}]))
        self.assertEqual(kept['ports'][0]['id'], 'front-1')

    def test_rejections(self):
        for extra, message in (({'ports': [{'x': 0, 'z': 20, 'w': 15, 'h': 8, 'type': 'scsi'}]}, 'connector type'),
                               ({'rear_ports': ['usb']}, 'must be an object'),
                               ({'rear_ports': [{'x': 200, 'z': 5}]}, 'Rear port X'),
                               ({'rear_ports': [{'x': 0, 'z': 50}]}, 'Rear port Z'),
                               ({'rear_ports': [{'id': 'front-1', 'x': 0, 'z': 5}]}, 'own id')):
            with self.subTest(message=message), self.assertRaisesRegex(ValueError, message):
                equipment.clean(wizard_spec(**extra))

    def test_source_ignores_planning_fields(self):
        base = equipment.source(equipment.clean(wizard_spec()))
        spec = wizard_spec()
        spec['ports'][0].update(type='rj45', id='p-xyz789')
        spec['rear_ports'] = [{'label': 'Power', 'type': 'iec', 'x': 0, 'z': 20}]
        self.assertEqual(equipment.source(equipment.clean(copy.deepcopy(spec))), base)


if __name__ == '__main__':
    unittest.main()
