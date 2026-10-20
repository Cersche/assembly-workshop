from pathlib import Path
import hashlib
import json
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[2]
APP=ROOT/'outputs/Mechanical_Design_App'
sys.path.insert(0,str(APP))
import assembly_records
import rack_workspace
import rack_references

class BrandingTests(unittest.TestCase):
    def test_appearance_validation_and_roundtrip(self):
        with tempfile.TemporaryDirectory(prefix='schema-',dir=Path(__file__).parent) as folder:
            for labels in (True,False):
                appearance={'logo_color':'#ABCD12','post_labels':labels,'color':'#112233','components':{'post5':'#334455'}}
                document={'version':2,'generation':None,'racks':[{'id':'brand','name':'Branding fixture','slots':48,'placements':[],'width_mm':None,'depth_mm':None,'pitch_mm':None,'appearance':appearance}]}
                document['generation']=rack_workspace.read(Path(folder)).get('generation')
                rack_workspace.save(Path(folder),document)
                actual=rack_workspace.read(Path(folder))['racks'][0]['appearance']
                self.assertEqual(actual,{**appearance,'logo_color':'#abcd12'})
        for bad in ('yes',0,1,None):
            with self.assertRaises(ValueError):assembly_records.appearance({'post_labels':bad},rack=True)
        with self.assertRaises(ValueError):assembly_records.appearance({'logo_color':'red'},rack=True)
        self.assertEqual(assembly_records.appearance({},rack=True),{})

    def test_asset_integrity_and_old_rack_lock(self):
        assets=APP/'rack-references'
        old=json.loads((Path(__file__).parent/'before-app/asset-manifest.json').read_text(encoding='utf-8'))
        new=json.loads((assets/'asset-manifest.json').read_text(encoding='utf-8'))
        for entry in old:
            if entry['file']!='rack-studio.js':self.assertIn(entry,new)
        for name in ('rack-studio.js','rack-logo-faces.json'):
            data,mime=rack_references.asset('/rack-references/'+name)
            self.assertTrue(data)
        self.assertEqual(hashlib.sha256((assets/'rack-scene.js').read_bytes()).hexdigest(),'414214bcbf3f1f40ff7a6be0791741ec721cb3d9585cc4d148b1c68f7ff1c7d2')

if __name__=='__main__':unittest.main(verbosity=2)
