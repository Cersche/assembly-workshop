"""Task 38: disposable panel tests; no app/user data and no automatic renders."""
import hashlib
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch
import equipment as eq
import faceplate_color
import rack_workspace


class FaceplateSlotTests(unittest.TestCase):
    def test_reference_spacing_and_warning(self):
        s=eq.clean_faceplate(dict(layout='keystones',count=10,rows=1))
        self.assertEqual([p[0] for p in s['keystones']],[-96.75,-75.25,-53.75,-32.25,-10.75,10.75,32.25,53.75,75.25,96.75])
        self.assertEqual(eq.faceplate_check(s),['thin wall, fit/strength UNKNOWN'])
        self.assertEqual(eq.faceplate_spacing(1,1,1),[[0,22.225]])
        with self.assertRaisesRegex(ValueError,'Maximum 10'):eq.faceplate_spacing(11,1,1)
        with self.assertRaises(ValueError):eq.faceplate_spacing(1,2,1)

    def test_multirow_and_color_keepout(self):
        s=eq.clean_faceplate(dict(layout='keystones',count=5,rows=2,u=2))
        self.assertEqual(sorted(set(z for x,z in s['keystones'])),[22.225,66.675])
        self.assertEqual(eq.faceplate_check(s),[])
        holes=faceplate_color.openings(s)
        self.assertEqual([h['z'] for h in holes],[23.975]*5+[68.425]*5)
        self.assertEqual([h['x'] for h in holes],[-96,-48,0,48,96]*2)

    def test_failures_block_render_before_compiler(self):
        for raw in [dict(u=0),dict(u=1.5),dict(layout='keystones',count=11),
                    dict(layout='keystones',count=2,rows=1,keystones=[[0,22.225],[20,22.225]]),
                    dict(layout='keystones',count=1,rows=1,keystones=[[115,22.225]]),
                    dict(layout='keystones',count=1,rows=1,keystones=[[0,15]]),
                    dict(layout='custom',ports=[dict(x=118,z=6.323,w=10,h=7)]),
                    dict(layout='custom',ports=[dict(x=0,z=22,w=20,h=10),dict(x=1,z=22,w=20,h=10)])]:
            with self.subTest(raw=raw),tempfile.TemporaryDirectory() as folder,patch.object(eq.mesh_revision,'compiler') as compiler:
                with self.assertRaises(ValueError):eq.render(dict(raw,faceplate_only=True),folder)
                compiler.assert_not_called()

    def test_disposable_roundtrip_per_slot_and_color(self):
        from test_allocation_tray import rack
        with tempfile.TemporaryDirectory() as folder:
            value=rack([dict(id='blank',equipment=eq.FACEPLATE_ID,slot=1,span=2,tray={'faceplate':{'u':2,'layout':'blank'}}),
                        dict(id='panel',equipment=eq.FACEPLATE_ID,slot=3,span=1,tray={'faceplate':{'u':1,'layout':'keystones','count':10,'rows':1}})])
            clean=rack_workspace.validate(value)
            saved=rack_workspace.save(folder,clean,None)
            loaded=rack_workspace.read(folder)
            self.assertEqual(saved,loaded)
            a,b=loaded['racks'][0]['placements']
            self.assertNotEqual(a['assembly']['id'],b['assembly']['id'])
            self.assertEqual(faceplate_color.slot_spec(folder,a)['keystones'],[])
            self.assertEqual(len(faceplate_color.slot_spec(folder,b)['keystones']),10)
            self.assertFalse((Path(folder)/'equipment-library.json').exists())

    def test_legacy_source_hash_and_blank_only_parts(self):
        from test_allocation_tray import OLD_SPEC
        self.assertEqual(hashlib.sha256(eq.source(eq.clean(OLD_SPEC)).encode()).hexdigest(),'1b843b157db172454bc2b62617d9332b71cb56fce64d327fba568e93223573f8')
        for u in (1,3):
            s=eq.clean_faceplate({'u':u})
            self.assertEqual((s['joint'],s['ports'],s['keystones']),('none',[],[]))
            text=eq.source(s)
            self.assertIn('joint="none";',text)
            self.assertIn('part="faceplate";',text)
            self.assertIn('keystones=[];',text)
            self.assertEqual(eq.clean(s),s)

    def test_custom_openings_and_unknowns(self):
        raw={'u':2,'layout':'custom','ports':[{'x':0,'z':40,'w':50,'h':25,'r':2}]}
        s=eq.clean_faceplate(raw)
        self.assertEqual(faceplate_color.openings(s),[{'x':0,'z':40,'w':50,'h':25}])
        self.assertIn('UNKNOWN',eq.LIMITS[0])
