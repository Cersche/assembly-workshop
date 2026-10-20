"""Independent slot hardware and appearance acceptance; disposable data, no renderer."""
import base64
import copy
import hashlib
import io
import json
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch
import zipfile
import zlib

import app
import assembly_records as records
import rack_workspace as racks


def png():
    def chunk(kind,body):
        return struct.pack('>I',len(body))+kind+body+struct.pack('>I',zlib.crc32(kind+body)&0xffffffff)
    return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',1,1,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(b'\0\xff\0\0\xff'))+chunk(b'IEND',b'')


class AssemblyRecordTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.store=app.Store(self.root/'library.sqlite3');self.store.load_starter()
        initial=self.store.project()
        self.store.save({'inputs':initial['inputs'],'selections':{kind:next(p for p in self.store.parts() if p['kind']==kind) for kind in ('screw','heatset')}})
        self.legacy=self.store.project()
        self.document=racks.save(self.root,{'version':1,'generation':None,'racks':[{'id':'rack','name':'Test','slots':5,'placements':[
            {'id':'a','slot':1,'span':1,'equipment':'pi4'},{'id':'b','slot':2,'span':1,'equipment':'pi4'}]}]},seed_project=self.legacy,
            canonical_project=lambda p:self.store.draft(p,project=p))
        self.a,self.b=[p['assembly']['id'] for p in self.document['racks'][0]['placements']]

    def instance(self,identity,document=None):
        return records.InstanceStore(self.store,identity,(document or racks.read(self.root))['generation'])

    def payload(self,project):
        return {'instance_revision':project['instance_revision'],'selections':copy.deepcopy(project['selections']),'inputs':copy.deepcopy(project['inputs'])}

    def request(self,path,body=None,headers=None):
        handler=app.make_handler(self.store,'token').__new__(app.make_handler(self.store,'token'))
        handler.path=path;handler.valid_host=lambda:True;handler.headers=headers or {}
        handler.command='GET' if body is None else 'POST'
        results=[];handler.send=lambda value,status=200,mime='application/json':results.append((value,status,mime))
        if body is None: handler.do_GET()
        else:
            data=json.dumps(body).encode('utf-8');handler.rfile=io.BytesIO(data)
            handler.headers={**handler.headers,'X-App-Token':'token','Content-Length':str(len(data))};handler.do_POST()
        return results[0]

    def test_two_instances_are_isolated_and_legacy_db_is_unchanged(self):
        before=(self.root/'library.sqlite3').read_bytes();b=self.instance(self.b).project()
        a=self.instance(self.a);payload=self.payload(a.project());payload['inputs']['pilot']=3.9
        saved=a.save(payload)
        self.assertEqual(saved['instance_revision'],2)
        self.assertEqual(saved['inputs']['pilot'],3.9)
        self.assertEqual(self.instance(self.b).project()['inputs'],b['inputs'])
        self.assertEqual(self.instance(self.b).project()['selections'],b['selections'])
        self.assertEqual(self.store.project(),self.legacy)
        self.assertEqual((self.root/'library.sqlite3').read_bytes(),before)
        self.assertEqual(len(list((self.root/'rack-history').glob('*.json'))),1)

    def test_stale_save_rejected_and_noop_does_not_bump_revision(self):
        instance=self.instance(self.a);project=instance.project();payload=self.payload(project)
        self.assertEqual(instance.save(payload)['instance_revision'],1)
        payload['inputs']['pilot']=3.8;instance.save(payload)
        with self.assertRaisesRegex(ValueError,'workspace changed'): instance.save(payload)
        latest=self.instance(self.a)
        with self.assertRaisesRegex(ValueError,'another session'): latest.save(payload)

    def test_layout_cannot_overwrite_hardware_and_old_client_is_rejected(self):
        doc=racks.read(self.root);doc['racks'][0]['placements'][0]['assembly']['project']['inputs']['pilot']=3.7
        with self.assertRaisesRegex(ValueError,'hardware changed'): racks.save(self.root,doc)
        doc=racks.read(self.root);doc['version']=1
        with self.assertRaisesRegex(ValueError,'old clients'): racks.save(self.root,doc)

    def test_v1_read_migrates_only_in_memory(self):
        path=self.root/'rack-workspace.json';value=json.loads(path.read_text(encoding='utf-8'));value['version']=1
        for p in value['racks'][0]['placements']: p.pop('assembly')
        path.write_text(json.dumps(value),encoding='utf-8');before=path.read_bytes()
        read=racks.read(self.root,seed_project=self.legacy)
        self.assertEqual(read['version'],2);self.assertEqual(path.read_bytes(),before)
        self.assertNotEqual(read['racks'][0]['placements'][0]['assembly']['id'],read['racks'][0]['placements'][1]['assembly']['id'])
        self.assertEqual(read['racks'][0]['placements'][0]['assembly']['project']['selections'],self.legacy['selections'])

    def test_appearance_does_not_change_hardware_identity(self):
        instance=self.instance(self.a);fingerprint=records.fingerprint(instance.project());document=racks.read(self.root)
        document['racks'][0]['appearance']={'color':'#123456','components':{'post5':'#ABCDEF'}}
        document['racks'][0]['placements'][0]['assembly']['appearance']={'tray':'#ff0088'}
        racks.save(self.root,document)
        self.assertEqual(records.fingerprint(instance.project()),fingerprint)
        self.assertEqual(instance.project()['instance_revision'],1)
        self.assertEqual(racks.read(self.root)['racks'][0]['appearance']['components']['post5'],'#abcdef')
        with self.assertRaises(ValueError): records.appearance({'tray':'url(evil)'})
        with self.assertRaises(ValueError): records.appearance({'components':{'unknown':'#123456'}},rack=True)

    def test_saved_release_undo_retains_latest_hardware_revision(self):
        instance=self.instance(self.a);payload=self.payload(instance.project());payload['inputs']['pilot']=3.9;instance.save(payload)
        document=racks.read(self.root);placement=document['racks'][0]['placements'].pop(0);saved=racks.save(self.root,document)
        saved['racks'][0]['placements'].append(placement)
        racks.save(self.root,saved)
        self.assertEqual(self.instance(self.a).project()['instance_revision'],2)
        self.assertEqual(self.instance(self.a).project()['inputs']['pilot'],3.9)

    def test_old_shared_editor_cannot_mutate_independent_workspace(self):
        before=self.store.project()
        _,status,_=self.request('/api/save',{'inputs':before['inputs'],'selections':{}})
        self.assertEqual(status,400);self.assertEqual(self.store.project(),before)

    def test_artwork_is_local_verified_png_and_tamper_is_blocked(self):
        data=png();asset=records.save_artwork(self.root,{'data_url':'data:image/png;base64,'+base64.b64encode(data).decode('ascii')})
        self.assertEqual(records.artwork(self.root,asset['sha256']),data)
        self.assertEqual(records.save_artwork(self.root,{'data_url':'data:image/png;base64,'+base64.b64encode(data).decode('ascii')}),asset)
        with self.assertRaises(ValueError): records.artwork(self.root,'../library')
        with self.assertRaises(ValueError): records.validate_png(data[:-1])
        with self.assertRaises(ValueError): records.validate_png(data+b'extra')
        (self.root/'artwork'/(asset['sha256']+'.png')).write_bytes(data+b'changed')
        with self.assertRaisesRegex(ValueError,'integrity'): records.artwork(self.root,asset['sha256'])

    def test_routes_scope_state_save_bom_and_check_to_instance(self):
        headers={'X-Assembly-Id':self.a,'X-Workspace-Generation':self.document['generation']}
        state,status,_=self.request('/api/state',headers=headers);self.assertEqual(status,200);self.assertEqual(state['project']['id'],self.a)
        payload=self.payload(state['project']);payload['inputs']['pilot']=3.9
        project,status,_=self.request('/api/save',payload,headers);self.assertEqual(status,200);self.assertEqual(project['instance_revision'],2)
        bom,status,_=self.request('/api/bom?assembly='+self.a);self.assertEqual(status,200);self.assertIn(self.a,bom);self.assertNotIn(self.b,bom)
        project,status,_=self.request('/api/project?assembly='+self.b);self.assertEqual(status,200);self.assertNotEqual(project['inputs']['pilot'],3.9)
        _,status,_=self.request('/api/check',{},headers);self.assertEqual(status,200)
        _,status,_=self.request('/api/project?assembly='+self.b,headers=headers);self.assertEqual(status,400)
        self.assertEqual(self.store.project(),self.legacy)

    def test_wrong_or_stale_instance_bundle_is_rejected_without_render(self):
        def bundle(binding):
            stream=io.BytesIO()
            with zipfile.ZipFile(stream,'w') as archive: archive.writestr('revision.json',json.dumps({'assembly_instance':binding}))
            return stream.getvalue()
        project=self.instance(self.a).project();binding={'id':self.a,'revision':1,'project_sha256':records.fingerprint(project)}
        for identity,status in [(self.a,200),(self.b,400)]:
            with patch.object(app.mesh_revision,'bundle',return_value=bundle(binding)):
                _,actual,_=self.request('/api/build-bundle',{'id':'fake'},headers={'X-Assembly-Id':identity});self.assertEqual(actual,status)
        changed=dict(binding,revision=2)
        with patch.object(app.mesh_revision,'bundle',return_value=bundle(changed)):
            _,status,_=self.request('/api/build-bundle',{'id':'fake'},headers={'X-Assembly-Id':self.a});self.assertEqual(status,400)


if __name__=='__main__': unittest.main()
