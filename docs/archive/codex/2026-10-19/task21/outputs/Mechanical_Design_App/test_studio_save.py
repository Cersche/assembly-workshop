"""Atomic explicit Save acceptance; fresh temporary data, no CAD generation."""
import copy
import unittest
import assembly_records as records
import rack_workspace as racks
from test_assembly_records import AssemblyRecordTests


class StudioSaveTests(unittest.TestCase):
    setUp=AssemblyRecordTests.setUp
    instance=AssemblyRecordTests.instance
    payload=AssemblyRecordTests.payload
    request=AssemblyRecordTests.request

    def test_combined_save_is_one_workspace_commit(self):
        value=racks.read(self.root);p=value['racks'][0]['placements'][0]
        p['slot']=3;p['assembly']['appearance']={'faceplate':'#335577'}
        hardware=self.payload(self.instance(self.a).project());hardware['id']=self.a;hardware['inputs']['pilot']=3.9
        library=(self.root/'library.sqlite3').read_bytes()
        saved=records.save_workspace(self.store,{'workspace':value,'assembly':hardware})
        a=saved['racks'][0]['placements'][0]['assembly']
        self.assertEqual(a['revision'],2);self.assertEqual(a['project']['inputs']['pilot'],3.9)
        self.assertEqual(a['appearance']['faceplate'],'#335577');self.assertEqual(saved['racks'][0]['placements'][0]['slot'],3)
        self.assertEqual(len(list((self.root/'rack-history').glob('*.json'))),1)
        self.assertEqual((self.root/'library.sqlite3').read_bytes(),library)
        self.assertEqual(self.instance(self.b).project()['instance_revision'],1)

    def test_invalid_hardware_leaves_layout_and_appearance_unsaved(self):
        before=(self.root/'rack-workspace.json').read_bytes();value=racks.read(self.root);value['racks'][0]['appearance']={'color':'#123456'}
        hardware=self.payload(self.instance(self.a).project());hardware.update(id=self.a,inputs={'pilot':'invalid'})
        with self.assertRaises(ValueError): records.save_workspace(self.store,{'workspace':value,'assembly':hardware})
        self.assertEqual((self.root/'rack-workspace.json').read_bytes(),before)
        self.assertFalse((self.root/'rack-history').exists())

    def test_stale_generation_is_rejected_without_partial_save(self):
        stale=racks.read(self.root);racks.save(self.root,copy.deepcopy(stale));before=(self.root/'rack-workspace.json').read_bytes()
        with self.assertRaisesRegex(ValueError,'another session'): records.save_workspace(self.store,{'workspace':stale})
        self.assertEqual((self.root/'rack-workspace.json').read_bytes(),before)

    def test_unscoped_hardware_tampering_is_rejected(self):
        value=racks.read(self.root);value['racks'][0]['placements'][1]['assembly']['project']['inputs']['pilot']=3.7
        with self.assertRaisesRegex(ValueError,'hardware changed'): records.save_workspace(self.store,{'workspace':value})

    def test_appearance_only_preserves_hardware_revision(self):
        value=racks.read(self.root);value['racks'][0]['appearance']={'color':'#123456'}
        saved=records.save_workspace(self.store,{'workspace':value})
        self.assertEqual(saved['racks'][0]['placements'][0]['assembly']['revision'],1)
        self.assertEqual(self.instance(self.a).project()['selections'],self.document['racks'][0]['placements'][0]['assembly']['project']['selections'])

    def test_atomic_save_route_and_capability(self):
        caps,status,_=self.request('/api/workspace-capabilities');self.assertEqual(status,200);self.assertEqual(caps['studio_save_version'],1)
        value=racks.read(self.root);value['racks'][0]['name']='Combined save'
        saved,status,_=self.request('/api/studio-save',{'workspace':value});self.assertEqual(status,200);self.assertEqual(saved['racks'][0]['name'],'Combined save')


if __name__=='__main__': unittest.main()
