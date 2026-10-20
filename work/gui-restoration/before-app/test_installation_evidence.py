import json
import tempfile
import unittest
from pathlib import Path
from app import ROOT, Store, evaluate, validate_part
from test_app import screw

class InstallationEvidenceTests(unittest.TestCase):
    def test_conditional_evidence_never_becomes_generic_fit_pass(self):
        records=json.loads((ROOT/'catalog-packs/phase6-batch5.json').read_text())
        self.assertEqual(len(records),5)
        for record in records:
            validate_part(record)
            if record['kind']!='heatset':continue
            evidence=record['manufacturer_installation_evidence']
            self.assertGreater(evidence['minimum_hole_depth_mm'],evidence['A_mm'])
            self.assertIn('No governing interval selected',evidence['hole_tolerance_conflict'])
            for key in ['usable_depth','min_wall','hole_diameter','outside_diameter','length']:
                self.assertNotIn(key,record)
            report=evaluate(screw(diameter=record['diameter'],pitch=record['pitch']),record,{})
            for check in report['checks']:
                if any(word in check['name'].lower() for word in ['installation','wall','pocket']):
                    self.assertNotEqual(check['status'],'pass')
        with tempfile.TemporaryDirectory() as d:
            store=Store(Path(d)/'test.sqlite3');store.load_starter();before=store.project()
            store.import_parts(records);store.import_parts(records)
            self.assertEqual(len(store.parts()),11)
            self.assertEqual(Store(store.path).project(),before)
