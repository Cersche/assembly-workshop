import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import catalog_packs
from app import ROOT, Store, evaluate, joint_geometry


class PackEvidenceChecks(unittest.TestCase):
    def test_overall_length_catalog_record_does_not_gain_under_head_reach(self):
        from test_app import insert
        record=json.loads((ROOT/'catalog-packs/phase6-batch4.json').read_text())[0]
        with tempfile.TemporaryDirectory() as d:
            store=Store(Path(d)/'catalog.sqlite3');store.load_starter()
            before=store.project()
            for pack in catalog_packs.inventory()['packs']:
                self.assertTrue(pack['available'])
                store.import_parts(pack['records'])
            self.assertEqual(len(store.parts()),38)
            self.assertEqual(store.project(),before)
        self.assertEqual(record['length_convention'],'overall')
        checks={c['name']:c['status'] for c in evaluate(record,insert(diameter=1,pitch=.25),{})['checks']}
        self.assertEqual(checks['Thread compatibility'],'pass')
        self.assertEqual(checks['Screw reach'],'unknown')
        geometry=joint_geometry({'selections':{'screw':record},'inputs':{}})
        self.assertIsNone(geometry['reach'])

    def test_corrupt_and_missing_pack_are_unavailable(self):
        with tempfile.TemporaryDirectory() as d:
            folder=Path(d)
            identity='phase6-batch1'
            for suffix in ['.json','-manifest.json']:
                (folder/(identity+suffix)).write_bytes((catalog_packs.ROOT/(identity+suffix)).read_bytes())
            with patch.object(catalog_packs,'ROOT',folder):
                inventory=catalog_packs.inventory()
                self.assertTrue(inventory['packs'][0]['available'])
                self.assertFalse(inventory['packs'][1]['available'])
                self.assertIn('error',inventory['gaps'])
                (folder/(identity+'.json')).write_text('[]')
                inventory=catalog_packs.inventory()
                self.assertFalse(inventory['packs'][0]['available'])
                self.assertNotIn('records',inventory['packs'][0])
