import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from app import ROOT, Store, evaluate, validate_part, design_revision

PACK = ROOT / 'catalog-packs' / 'phase6-batch1.json'

class Phase6CatalogChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.temp.name) / 'test.sqlite3')
        self.store.load_starter()
        self.records = json.loads(PACK.read_text(encoding='utf-8'))
    def tearDown(self):
        self.temp.cleanup()
    def test_pack_identity_and_provenance(self):
        manifest = json.loads(PACK.with_name('phase6-batch1-manifest.json').read_text())
        self.assertEqual(hashlib.sha256(PACK.read_bytes()).hexdigest(), manifest['sha256'])
        self.assertEqual(len({(r['id'],r['revision']) for r in self.records}),6)
        for record in self.records:
            validate_part(record)
            self.assertEqual(record['units'],'mm')
            self.assertTrue(record['field_sources'])
            self.assertTrue(record['unknown_fields'])
            self.assertIn('unknown',record['redistribution_status'])
    def test_explicit_import_preserves_pins_and_is_atomic(self):
        selected={r['kind']:r for r in self.store.parts() if r.get('part_number') in ['SSCF-M3-8-A2','94459A140']}
        self.store.save({'selections':selected,'inputs':{'pilot':4}})
        before=self.store.project()
        self.store.import_parts(self.records)
        self.store.import_parts(self.records)
        self.assertEqual(len(self.store.parts()),12)
        self.assertEqual(Store(self.store.path).project(),before)
        coverage={r['size']:r for r in self.store.state()['coverage']}
        for d in [2,4,8]:
            self.assertEqual((coverage[d]['screws'],coverage[d]['heatsets']),(1,1))
        for d in [1,1.2,1.4,1.6,2.5,3.5,4.5,5,6,7]:
            self.assertEqual((coverage[d]['screws'],coverage[d]['heatsets']),(0,0))
        bad=dict(self.records[-1],length=99)
        with self.assertRaisesRegex(ValueError,'immutable'):
            self.store.import_parts([dict(self.records[0],id='rollback-fixture'),bad])
        self.assertNotIn('rollback-fixture',{r['id'] for r in self.store.parts()})
        self.store.import_parts([dict(self.records[0],revision=2,length=9,threaded_length=9)])
        self.assertEqual(self.store.project(),before)
    def test_tapered_insert_never_becomes_straight_hole_pass(self):
        for insert in [r for r in self.records if r['kind']=='heatset']:
            self.assertNotIn('hole_diameter',insert)
            self.assertNotIn('usable_depth',insert)
            self.assertNotIn('min_wall',insert)
            screw=next(r for r in self.records if r['kind']=='screw' and r['diameter']==insert['diameter'])
            result=evaluate(screw,insert,{'pilot':insert['recommended_hole_entrance_diameter_mm']})
            checks={c['name']:c['status'] for c in result['checks']}
            self.assertEqual(checks['Thread compatibility'],'pass')
            self.assertEqual(checks['Installation hole'],'unknown')
            self.assertEqual(checks['Usable thread engagement'],'unknown')
            self.assertEqual(checks['Boss wall'],'unknown')
            self.assertEqual(checks['Nominal screw-head surface screening'],'unknown')
            with self.assertRaisesRegex(ValueError,'M3'):
                design_revision({'selections':{'screw':screw,'heatset':insert},'inputs':{}})


class Phase6Batch2Checks(unittest.TestCase):
    def setUp(self):
        self.records = json.loads((ROOT/'catalog-packs/phase6-batch2.json').read_text())

    def test_combined_pack_import_preserves_saved_project(self):
        manifest = json.loads((ROOT/'catalog-packs/phase6-batch2-manifest.json').read_text())
        self.assertEqual(hashlib.sha256((ROOT/'catalog-packs/phase6-batch2.json').read_bytes()).hexdigest(),manifest['sha256'])
        with tempfile.TemporaryDirectory() as d:
            store=Store(Path(d)/'catalog.sqlite3');store.load_starter()
            screw=next(p for p in store.parts() if p.get('part_number')=='SSCF-M3-8-A2')
            store.save({'selections':{'screw':screw},'inputs':{'pilot':4}})
            before=store.project()
            store.import_parts(json.loads(PACK.read_text()))
            store.import_parts(self.records);store.import_parts(self.records)
            self.assertEqual(len(store.parts()),19)
            self.assertEqual(Store(store.path).project(),before)
            coverage={r['size']:r for r in store.state()['coverage']}
            for size in [2.5,5,6]:
                self.assertEqual((coverage[size]['screws'],coverage[size]['heatsets']),(1,1))
            self.assertEqual(coverage[3]['heatsets'],4)
            self.assertEqual(coverage[3.5]['heatsets'],0)
            bad=dict(self.records[-1],length=99)
            with self.assertRaisesRegex(ValueError,'immutable'):
                store.import_parts([dict(self.records[0],id='batch2-rollback'),bad])
            self.assertNotIn('batch2-rollback',{p['id'] for p in store.parts()})
            for record in self.records:
                self.assertTrue(record['field_sources'])
                self.assertTrue(record['unknown_fields'])

    def test_sourced_hole_interval_and_legacy_exact_behavior(self):
        from test_app import screw as fixture_screw
        for insert in [r for r in self.records if r['kind']=='heatset']:
            screw=fixture_screw(diameter=insert['diameter'],pitch=insert['pitch'])
            def checks(pilot,part=insert):
                return {c['name']:c for c in evaluate(screw,part,{'pilot':pilot})['checks']}
            lo=insert['hole_diameter'];hi=lo+.08
            for pilot in [lo,(lo+hi)/2,hi]:
                self.assertEqual(checks(pilot)['Installation hole']['status'],'pass')
            for pilot in [lo-.000001,hi+.000001]:
                self.assertEqual(checks(pilot)['Installation hole']['status'],'fail')
            for name in ['Usable thread engagement','Boss wall','Bottom clearance','Physical and spatial checks']:
                self.assertEqual(checks(lo)[name]['status'],'unknown')
            legacy=dict(insert);legacy.pop('hole_diameter_tolerance_mm')
            self.assertEqual(checks(lo+.04,legacy)['Installation hole']['status'],'fail')
            tapered=dict(legacy,hole_profile='tapered')
            self.assertEqual(checks(lo,tapered)['Installation hole']['status'],'unknown')

    def test_invalid_hole_tolerances_rejected_atomically(self):
        insert=next(r for r in self.records if r['kind']=='heatset')
        invalid=[True,[],{'plus':.08},{'plus':.08,'minus':0,'extra':1}]
        invalid += [{'plus':v,'minus':0} for v in [True,-.1,float('nan'),float('inf'),'0.08']]
        invalid += [{'plus':.08,'minus':insert['hole_diameter']}]
        with tempfile.TemporaryDirectory() as d:
            store=Store(Path(d)/'catalog.sqlite3')
            for tolerance in invalid:
                with self.subTest(tolerance=tolerance),self.assertRaises(ValueError):
                    store.import_parts([self.records[0],dict(insert,hole_diameter_tolerance_mm=tolerance)])
                self.assertEqual(store.parts(),[])
            with self.assertRaises(ValueError):
                validate_part(dict(insert,hole_diameter=None))
            with self.assertRaises(ValueError):
                validate_part(dict(insert,hole_profile='tapered'))
            with self.assertRaises(ValueError):
                validate_part(dict(insert,hole_diameter=1e308,hole_diameter_tolerance_mm={'plus':1e308,'minus':0}))


class Phase6Batch3Checks(unittest.TestCase):
    def test_all_packs_reopen_and_new_family_rules(self):
        from test_app import screw as fixture_screw
        with tempfile.TemporaryDirectory() as d:
            store=Store(Path(d)/'catalog.sqlite3');store.load_starter()
            chosen=next(r for r in store.parts() if r.get('part_number')=='SSCF-M3-8-A2')
            before=store.save({'selections':{'screw':chosen},'inputs':{'pilot':4}})
            for n in [1,2,3]:
                path=ROOT/f'catalog-packs/phase6-batch{n}.json'
                manifest=json.loads(path.with_name(f'phase6-batch{n}-manifest.json').read_text())
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),manifest['sha256'])
                records=json.loads(path.read_text())
                store.import_parts(records);store.import_parts(records)
            reopened=Store(store.path)
            self.assertEqual(len(reopened.parts()),26)
            self.assertEqual(reopened.project(),before)
            counts={r['size']:r for r in reopened.state()['coverage']}
            self.assertEqual(sum(c['screws']>0 for c in counts.values()),10)
            self.assertEqual(sum(c['heatsets']>0 for c in counts.values()),8)
            screw=next(r for r in reopened.parts() if r['id']=='accu-sscf-m3.5-16-a2')
            self.assertEqual(screw['manufacturing_standard'],'Not Standardised')
            small=next(r for r in reopened.parts() if r['id']=='accu-sscf-m1.4-6-a4')
            self.assertEqual(small['material'],'A4 stainless steel')
            for insert in [r for r in records if r['kind']=='heatset']:
                compatible=fixture_screw(diameter=insert['diameter'],pitch=insert['pitch'])
                checks={c['name']:c['status'] for c in evaluate(compatible,insert,{'pilot':insert['hole_diameter']+.04})['checks']}
                self.assertEqual(checks['Thread compatibility'],'pass')
                self.assertEqual(checks['Installation hole'],'pass')
                self.assertEqual(checks['Boss wall'],'unknown')
                self.assertEqual(checks['Usable thread engagement'],'unknown')
                incompatible=dict(compatible,pitch=compatible['pitch']+.01)
                self.assertEqual(evaluate(incompatible,insert,{})['checks'][0]['status'],'fail')
