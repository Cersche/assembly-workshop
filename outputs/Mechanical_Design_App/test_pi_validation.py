import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import pi_validation as pv
from app import Store

class PiChecks(unittest.TestCase):
    def test_reference_and_positive_interference_regression(self):
        part,manifest=pv.reference()
        self.assertEqual(len(part['triangles']),122174)
        self.assertEqual(manifest['units'],'mm')
        self.assertFalse(any(pv.gusset_hits(part).values()))
        self.assertGreater(pv.gusset_hits(part,1)['34'],0)
        self.assertFalse(any(pv.other_hits(part).values()))
    def test_conversion_error_is_never_clearance_pass(self):
        self.assertEqual(pv.solid_result('ERROR: mesh not closed',True),'unknown')
        self.assertEqual(pv.solid_result('Current top level object is empty.',True),'pass')
        self.assertEqual(pv.solid_result('',False,0),'fail')
    def test_missing_or_corrupt_asset_is_unknown(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/'pi_reference_manifest.json').write_bytes((pv.ROOT/'pi_reference_manifest.json').read_bytes())
            with patch.object(pv,'ROOT',root):
                self.assertEqual(pv.validate()['checks'][0]['status'],'unknown')
                (root/'pi_reference.json').write_text('{}')
                self.assertEqual(pv.validate()['checks'][0]['status'],'unknown')
    def test_project_reference_round_trip_and_report_limits(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'test.sqlite3'; store=Store(path)
            saved=store.save({'inputs':{},'selections':{}})
            self.assertEqual(Store(path).project()['reference'],saved['reference'])
        report=pv.validate()
        self.assertEqual(report['status'],'incomplete')
        checks={c['name']:c for c in report['checks']}
        self.assertEqual(checks['PCB mounting placement']['status'],'pass')
        self.assertEqual(checks['PCB hole XY alignment']['status'],'pass')
        self.assertEqual(checks['Whole-Pi solid interference']['status'],'unknown')
        self.assertFalse(report['manufacturing_reference_included'])

    def test_pcb_underside_is_separate_from_ring_surfaces(self):
        part,_=pv.reference()
        pcb=pv.pcb_measurements(part)
        self.assertTrue(pcb['identified'])
        self.assertTrue(pcb['xy_match'])
        self.assertAlmostEqual(pcb['bounds'][0][2],16,places=6)
        self.assertEqual(pcb['underside_gap_to_standoff_mm'],0)
        self.assertTrue(all(r['surface_z_levels']==[16.01001,17.59001] for r in pcb['rings']))
        shifted=dict(part,vertices=[[v[0]+.1,v[1],v[2]+.02] for v in part['vertices']])
        measured=pv.pcb_measurements(shifted)
        self.assertFalse(measured['xy_match'])
        self.assertAlmostEqual(measured['underside_gap_to_standoff_mm'],.02,places=6)

    def test_joint_axes_and_nonmatching_solid_evidence(self):
        assembly=json.loads((pv.ROOT/'assembly.json').read_text(encoding='utf-8'))
        self.assertTrue(pv.joint_measurements(assembly)['axes_match'])
        tray=next(p for p in assembly['parts'] if p['id']=='tray')
        tray['vertices']=[[v[0]+.1,v[1],v[2]] for v in tray['vertices']]
        self.assertFalse(pv.joint_measurements(assembly)['axes_match'])
        self.assertEqual(pv.joint_evidence('wrong-source')['status'],'unknown')
        self.assertEqual(pv.solid_result('',True),'unknown')
        self.assertEqual(pv.solid_result('Current top level object is empty.',True,2),'unknown')
        self.assertEqual(pv.solid_result('WARNING: conversion failed. Current top level object is empty.',True),'unknown')

    def test_bound_separation_reports_only_named_objects(self):
        part,_=pv.reference()
        result=pv.separation_measurements(part)
        self.assertAlmostEqual(result['faceplate_y_gap_mm'],2.599998474121094)
        self.assertAlmostEqual(result['tray_floor_z_gap_mm'],3.9000091552734375)
        self.assertEqual(set(result),{'pi_min_y','pi_min_z','faceplate_y_gap_mm','socket_rail_y_gap_mm','tray_floor_z_gap_mm'})

    def test_pinned_solid_evidence_and_failed_export_gate(self):
        import hashlib
        from app import design_revision, ROOT
        source_hash=hashlib.sha256((pv.ROOT/'pi4_baseline.scad').read_bytes()).hexdigest()
        report=pv.joint_evidence(source_hash)
        self.assertEqual(report['status'],'pass')
        self.assertEqual(report['checks'][-1]['actual_intersection_status'],'fail')
        records=json.loads((ROOT/'starter-hardware.json').read_text(encoding='utf-8'))
        project={'inputs':{'pilot':4},'selections':{p['kind']:p for p in records if p.get('part_number') in ['SSCF-M3-8-A2','94459A140']}}
        with patch('app.pi_validation.validate',return_value={'status':'fail','checks':[]}):
            with self.assertRaisesRegex(ValueError,'assembly checks'):
                design_revision(project)
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)
            evidence=json.loads((pv.ROOT/'joint_validation.json').read_text(encoding='utf-8'))
            evidence['results']['positive_joint_clash'].update(log='Current top level object is empty.',empty=True,returncode=1)
            (path/'joint_validation.json').write_text(json.dumps(evidence),encoding='utf-8')
            with patch.object(pv,'ROOT',path):
                self.assertEqual(pv.joint_evidence(source_hash)['status'],'fail')

    def test_nominal_head_surface_screen_and_missing_dimensions(self):
        records=json.loads((pv.ROOT/'starter-hardware.json').read_text(encoding='utf-8'))
        screw=next(p for p in records if p.get('part_number')=='SSCF-M3-8-A2')
        result=pv.head_screen(screw)
        self.assertEqual(result['status'],'pass')
        self.assertEqual(len(result['measurements']),6)
        self.assertTrue(all(r['outer']==0 for r in result['measurements']))
        self.assertEqual(pv.head_screen(dict(screw,head_diameter=None))['status'],'unknown')
        self.assertEqual(pv.head_screen(dict(screw,head_height=float('nan')))['status'],'unknown')
        self.assertEqual(pv.head_screen(dict(screw,diameter=4))['status'],'unknown')

    def test_head_cylinder_collision_and_polygon_ambiguity(self):
        import math
        triangle={'vertices':[[-40,12,21],[-39.9,12,21],[-40,12.1,21.1]],'triangles':[[0,1,2]]}
        self.assertEqual(pv.head_surface_hits(triangle,-40,2,3)['status'],'fail')
        self.assertEqual(pv.head_surface_hits(triangle,40,2,3)['status'],'pass')
        a=math.pi/48
        center=[-40+.999*math.cos(a),12,21+.999*math.sin(a)]
        near={'vertices':[[center[0],12,center[2]],[center[0],12.1,center[2]],
                          [center[0]-.0001*math.sin(a),12,center[2]+.0001*math.cos(a)]],
              'triangles':[[0,1,2]]}
        self.assertEqual(pv.head_surface_hits(near,-40,2,3)['status'],'unknown')

    def test_access_unknowns_require_actual_envelopes(self):
        records=json.loads((pv.ROOT/'starter-hardware.json').read_text(encoding='utf-8'))
        screw=next(p for p in records if p.get('part_number')=='SSCF-M3-8-A2')
        insert=next(p for p in records if p.get('part_number')=='94459A140')
        assessments=pv.access_assessment(screw,insert)
        self.assertEqual(len(assessments),5)
        self.assertTrue(all(a['status']=='unknown' and a['required'] and a['limit'] for a in assessments))
        self.assertEqual(assessments[0]['known']['drive'],'2.5 mm hex')
        self.assertEqual(assessments[1]['known']['length_mm'],5.7)
        self.assertNotIn('shaft_diameter',assessments[0]['known'])
        self.assertIsNone(pv.access_assessment()[0]['known']['drive'])
