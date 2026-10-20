"""Independent assembly snapshots and local preview assets; no geometry generation."""
import base64
import binascii
import copy
import hashlib
import json
from pathlib import Path
import re
import struct
import zlib

COLORS = {'equipment', 'tray', 'faceplate'}
RACK_COMPONENTS = {'post1','post2','post3','post4','post5','beam_bottom','beam_top_front',
                   'beam_top_rear','side_rail','panel_bottom','panel_top','panel1','panel2',
                   'panel3','panel4','panel5','foot','handle'}


def color(value):
    if not isinstance(value,str) or re.fullmatch(r'#[0-9a-fA-F]{6}',value) is None:
        raise ValueError('Use a six-digit hex color.')
    return value.lower()


def appearance(value, rack=False):
    if value is None:
        return {}
    if not isinstance(value,dict):
        raise ValueError('Appearance must be an object.')
    result={}
    if rack:
        if 'color' in value: result['color']=color(value['color'])
        components=value.get('components',{})
        if not isinstance(components,dict) or set(components)-RACK_COMPONENTS:
            raise ValueError('Unsupported rack component color.')
        if components: result['components']={k:color(v) for k,v in components.items()}
    else:
        result={k:color(v) for k,v in value.items() if k in COLORS}
        art=value.get('artwork')
        if art is not None:
            if not isinstance(art,dict) or re.fullmatch(r'[a-f0-9]{64}',str(art.get('sha256',''))) is None:
                raise ValueError('Artwork must reference a local preview image.')
            name=art.get('name','Artwork')
            if not isinstance(name,str) or len(name)>120:
                raise ValueError('Artwork name is too long.')
            result['artwork']={'sha256':art['sha256'],'name':name,'mode':'preview-only'}
            for key,default in [('x',.5),('y',.5),('scale',.65)]:
                v=art.get(key,default)
                if type(v) not in (int,float) or not 0<=v<=1:
                    raise ValueError('Artwork position/scale must be between zero and one.')
                result['artwork'][key]=v
    return result


def project_snapshot(project, identity, name='Raspberry Pi 4'):
    if not isinstance(project,dict) or not isinstance(project.get('selections',{}),dict) or not isinstance(project.get('inputs',{}),dict):
        raise ValueError('Assembly project needs hardware selections and inputs.')
    result={k:copy.deepcopy(project[k]) for k in ('selections','inputs','notes','reference') if k in project}
    result.update(id=identity,name=name,units='mm')
    result.setdefault('selections',{});result.setdefault('inputs',{})
    if len(json.dumps(result,ensure_ascii=False))>100_000:
        raise ValueError('Assembly project metadata is too large.')
    return result


def normalize(value, rack_id, placement_id, seed=None):
    value=value or {}
    if not isinstance(value,dict): raise ValueError('Invalid assembly record.')
    identity=value.get('id') or 'asm-'+hashlib.sha256((rack_id+'\n'+placement_id).encode('utf-8')).hexdigest()[:32]
    if not isinstance(identity,str) or re.fullmatch(r'asm-[a-zA-Z0-9-]{8,64}',identity) is None:
        raise ValueError('Invalid assembly identity.')
    revision=value.get('revision',1)
    if type(revision) is not int or revision<1: raise ValueError('Invalid assembly revision.')
    name=value.get('name','Raspberry Pi 4')
    if not isinstance(name,str) or not name.strip() or len(name)>100: raise ValueError('Give the assembly a name, up to 100 characters.')
    project=project_snapshot(value.get('project',seed or {}),identity,name.strip())
    return {'id':identity,'name':name.strip(),'revision':revision,'project':project,
            'appearance':appearance(value.get('appearance')),'fit':'UNKNOWN'}


def find(document, identity):
    for rack in document['racks']:
        for placement in rack['placements']:
            if placement['assembly']['id']==identity:
                return rack,placement
    raise ValueError('Save the slot allocation before opening its independent assembly.')


def fingerprint(project):
    clean={k:project[k] for k in ('id','selections','inputs')}
    return hashlib.sha256(json.dumps(clean,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()


def save_workspace(base, payload):
    """One explicit commit for layout, appearance and the open hardware draft."""
    import rack_workspace
    value=payload.get('workspace')
    if not isinstance(value,dict) or value.get('version')!=2:
        raise ValueError('Use the updated studio document for a combined Save.')
    seed=base.project()
    candidate=rack_workspace.validate(value,seed)
    candidate['generation']=value.get('generation')
    previous=rack_workspace.read(Path(base.path).parent,seed)
    old={p['assembly']['id']:p['assembly'] for r in previous['racks'] for p in r['placements']}
    for rack in candidate['racks']:
        for p in rack['placements']:
            record=p['assembly'];saved=old.get(record['id'])
            if saved and (saved['project']!=record['project'] or saved['revision']!=record['revision']):
                raise ValueError('Assembly hardware changed. Preserve your draft and reload before saving.')
    update=payload.get('assembly')
    if update is not None:
        if not isinstance(update,dict): raise ValueError('Invalid assembly draft.')
        _,p=find(candidate,update.get('id'));record=p['assembly']
        if update.get('instance_revision')!=record['revision']:
            raise ValueError('Assembly revision changed. Preserve your draft and reload.')
        project=base.draft(update,project=record['project'])
        if fingerprint(project)!=fingerprint(record['project']):
            record['project']=project_snapshot(project,record['id'],record['name'])
            if record['id'] in old: record['revision']+=1
    return rack_workspace.save(Path(base.path).parent,candidate,seed_project=seed,
        allow_project_changes=True,canonical_project=lambda p:base.draft(p,project=p))


class InstanceStore:
    def __init__(self, base, identity, expected_generation=None):
        self.base,self.identity,self.expected_generation=base,identity,expected_generation
        self.path=base.path

    def document(self):
        import rack_workspace
        return rack_workspace.read(Path(self.path).parent,seed_project=self.base.project())

    def project(self):
        document=self.document();_,placement=find(document,self.identity);record=placement['assembly']
        return dict(copy.deepcopy(record['project']),instance_id=record['id'],
                    instance_revision=record['revision'],workspace_generation=document['generation'])

    def parts(self): return self.base.parts()

    def state(self):
        value=self.base.state();value['project']=self.project();return value

    def draft(self,payload):
        return self.base.draft(payload,project=self.project())

    def save(self,payload):
        import rack_workspace
        document=self.document();_,placement=find(document,self.identity);record=placement['assembly']
        if self.expected_generation!=document['generation']:
            raise ValueError('Rack workspace changed. Preserve your draft and reload before saving this assembly.')
        if payload.get('instance_revision')!=record['revision']:
            raise ValueError('Assembly changed in another session. Preserve your draft and reload.')
        project=self.draft(payload)
        if fingerprint(project)==fingerprint(record['project']): return self.project()
        record['project']=project_snapshot(project,record['id'],record['name']);record['revision']+=1
        saved=rack_workspace.save(Path(self.path).parent,document,seed_project=self.base.project(),
                                  allow_project_changes=True)
        return dict(copy.deepcopy(record['project']),instance_id=record['id'],
                    instance_revision=record['revision'],workspace_generation=saved['generation'])


def validate_png(data):
    if len(data)>524288 or data[:8]!=b'\x89PNG\r\n\x1a\n':
        raise ValueError('Artwork must be a PNG preview, at most 512 KB.')
    offset=8;dimensions=None;ended=False
    while offset<len(data):
        if offset+12>len(data): raise ValueError('Truncated PNG preview.')
        size=struct.unpack('>I',data[offset:offset+4])[0]
        if offset+size+12>len(data): raise ValueError('Truncated PNG chunk.')
        kind=data[offset+4:offset+8];body=data[offset+8:offset+8+size]
        expected=struct.unpack('>I',data[offset+8+size:offset+12+size])[0]
        if zlib.crc32(kind+body)&0xffffffff!=expected: raise ValueError('PNG checksum failed.')
        if offset==8:
            if kind!=b'IHDR' or size!=13: raise ValueError('PNG header is missing.')
            dimensions=struct.unpack('>II',body[:8])
            if any(not 0<v<=512 for v in dimensions): raise ValueError('Artwork preview must be at most 512 × 512 pixels.')
        offset+=size+12
        if kind==b'IEND': ended=True;break
    if not ended or offset!=len(data): raise ValueError('Invalid PNG ending.')
    return dimensions


def save_artwork(data_dir,payload):
    encoded=payload.get('data_url','')
    if not isinstance(encoded,str) or not encoded.startswith('data:image/png;base64,'):
        raise ValueError('Use the local image chooser to prepare a PNG preview.')
    try: data=base64.b64decode(encoded.split(',',1)[1],validate=True)
    except (ValueError,binascii.Error) as exc: raise ValueError('Invalid artwork encoding.') from exc
    width,height=validate_png(data);identity=hashlib.sha256(data).hexdigest()
    folder=Path(data_dir)/'artwork';folder.mkdir(exist_ok=True)
    path=folder/(identity+'.png')
    if path.exists():
        if path.read_bytes()!=data: raise ValueError('Artwork integrity conflict.')
    else:
        with path.open('xb') as stream: stream.write(data)
    return {'sha256':identity,'width':width,'height':height,'mode':'preview-only'}


def artwork(data_dir,identity):
    if re.fullmatch(r'[a-f0-9]{64}',identity) is None: raise ValueError('Invalid artwork identity.')
    data=(Path(data_dir)/'artwork'/(identity+'.png')).read_bytes()
    if hashlib.sha256(data).hexdigest()!=identity: raise ValueError('Artwork integrity check failed.')
    validate_png(data);return data
