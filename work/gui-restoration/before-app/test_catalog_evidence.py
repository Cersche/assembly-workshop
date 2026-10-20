import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import catalog_evidence
import catalog_packs
from app import Store,validate_part,evaluate
from test_app import insert,screw

class EvidenceTests(unittest.TestCase):
    def profile(self):
        return insert(hole_profile='segmented',installation_hole_segments=[
          dict(z0=0,z1=1,diameter0=4.5,diameter1=4.2,source='Fictional tapered entrance'),
          dict(z0=1,z1=5,diameter0=4.2,diameter1=4.2,source='Fictional straight bore')])

    def test_segmented_custom_record_roundtrip_stays_unsupported(self):
        part=self.profile();validate_part(part)
        with tempfile.TemporaryDirectory() as d:
            store=Store(Path(d)/'test.sqlite3');store.load_starter();before=store.project()
            store.import_parts([part])
            self.assertEqual(next(x for x in Store(store.path).parts() if x['id']==part['id']),part)
            self.assertEqual(store.project(),before)
        check=next(c for c in evaluate(screw(),part,{})['checks'] if c['name']=='Installation hole')
        self.assertEqual(check['status'],'unknown')

    def test_invalid_segments_reject_atomic_import(self):
        mutations=[lambda p:p.update(installation_hole_segments=[]),
                   lambda p:p['installation_hole_segments'][0].update(z0=.1),
                   lambda p:p['installation_hole_segments'][1].update(z0=2),
                   lambda p:p['installation_hole_segments'][0].update(diameter0=-1),
                   lambda p:p['installation_hole_segments'][0].update(z1=True),
                   lambda p:p['installation_hole_segments'][0].update(source=''),
                   lambda p:p.update(hole_profile='straight')]
        with tempfile.TemporaryDirectory() as d:
            store=Store(Path(d)/'test.sqlite3')
            for mutate in mutations:
                p=copy.deepcopy(self.profile());mutate(p)
                with self.assertRaises(ValueError):store.import_parts([screw(),p])
                self.assertEqual(store.parts(),[])

    def test_all_pack_evidence_inspects_without_network_or_mutation(self):
        with patch('socket.socket',side_effect=AssertionError('Offline acceptance forbids network')):
            packs=catalog_packs.inventory()['packs'];records=[r for p in packs for r in p['records']]
            before=copy.deepcopy(records);reports=[catalog_evidence.inspect(r) for r in records]
        self.assertEqual(records,before)
        self.assertEqual(len(reports),32)
        self.assertEqual(sum(bool(r['installation_conflicts']) for r in reports),4)
        self.assertTrue(all(not r['physical_approval'] for r in reports))
        pem=next(r for r in reports if r['id']=='msia-m1-250')
        self.assertIn('usable_depth',pem['missing_fields'])
