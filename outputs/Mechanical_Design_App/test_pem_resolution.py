import json
import tempfile
import unittest
from pathlib import Path
from app import ROOT,Store,evaluate
from catalog_evidence import inspect
from test_app import screw

class PemResolution(unittest.TestCase):
 def test_resolved_intersection_boundaries_and_immutable_r1(self):
  old=[r for r in json.loads((ROOT/'catalog-packs/phase6-batch5.json').read_text()) if r['kind']=='heatset']
  new=json.loads((ROOT/'catalog-packs/phase6-batch7.json').read_text())
  with tempfile.TemporaryDirectory() as d:
   store=Store(Path(d)/'test.sqlite3');store.import_parts([screw()]+old)
   store.save({'selections':{'screw':{'id':'s','revision':1},'heatset':{'id':old[0]['id'],'revision':1}},'inputs':{}})
   before=store.project();store.import_parts(new);store.import_parts(new)
   self.assertEqual(Store(store.path).project(),before)
   self.assertEqual(len(store.parts()),9)
  for r in new:
   lo=r['hole_diameter'];hi=lo+.05
   for value,expected in [(lo,'pass'),(hi,'pass'),(lo-.001,'fail'),(hi+.001,'fail')]:
    checks={x['name']:x['status'] for x in evaluate(screw(diameter=r['diameter'],pitch=r['pitch']),r,{'pilot':value})['checks']}
    self.assertEqual(checks['Installation hole'],expected)
    self.assertEqual(checks['Usable thread engagement'],'unknown')
    self.assertEqual(checks['Boss wall'],'unknown')
   self.assertEqual(inspect(r)['installation_conflicts'],[])
   self.assertIn('retained_discrepancy',r['installation_evidence_resolution'])
   self.assertNotIn('min_wall',r)
