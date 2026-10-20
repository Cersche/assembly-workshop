import json
import tempfile
import unittest
from pathlib import Path
import catalog_packs
from app import ROOT, Store, evaluate
from test_app import insert

class Batch6Tests(unittest.TestCase):
    def test_all_screw_families_preserve_unknown_geometry_and_pins(self):
        with tempfile.TemporaryDirectory() as d:
            store=Store(Path(d)/'test.sqlite3');store.load_starter();before=store.project()
            for pack in catalog_packs.inventory()['packs']:
                self.assertTrue(pack['available']);store.import_parts(pack['records'])
            self.assertEqual(len(store.parts()),38)
            self.assertEqual(len({p['diameter'] for p in store.parts() if p['kind']=='screw'}),14)
            self.assertEqual(Store(store.path).project(),before)
            records=json.loads((ROOT/'catalog-packs/phase6-batch6.json').read_text())
            store.import_parts(records);self.assertEqual(len(store.parts()),38)
        flat,cap=records
        checks={c['name']:c['status'] for c in evaluate(flat,insert(diameter=4.5,pitch=.75),{})['checks']}
        self.assertEqual(checks['Thread compatibility'],'pass')
        self.assertEqual(checks['Screw reach'],'unknown')
        self.assertNotIn('countersunk_angle_degrees',flat)
        self.assertEqual(cap['head_height'],6)
        self.assertEqual(cap['threaded_length'],25)
        gaps=json.loads((ROOT/'catalog-packs/source-gaps.json').read_text())['gaps']
        self.assertEqual({(g['kind'],g['size']) for g in gaps},{('heatset',4.5),('heatset',7)})
