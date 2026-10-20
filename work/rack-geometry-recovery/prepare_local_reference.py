"""Extract local reference data only. No meshing, resizing, CAD render, or export."""
import hashlib
import json
from pathlib import Path

from inspect_references import OUT, ROOT, inspect_3mf, write_json


def main():
    target = ROOT/'outputs/Mechanical_Design_App/rack-references'
    target.mkdir(exist_ok=True)
    inspection = json.loads((OUT/'Reference_Inspection.json').read_text(encoding='utf-8'))
    manifest = []
    catalog = {'version': 1, 'scope': 'Local source reference only; rack layout remains schematic.',
               'manufacturing_geometry_supported': False,
               'm6_note': 'Brian supplied: M6 heat inserts can be placed in the rack post mounting holes. Insert selection, bore dimensions, installation, fit and strength remain UNKNOWN.',
               'references': []}
    def asset(name, data, mime):
        (target/name).write_bytes(data)
        manifest.append({'url': '/rack-references/'+name, 'file': name, 'mime': mime,
                         'sha256': hashlib.sha256(data).hexdigest()})
    for i, reference in enumerate(inspection['references']):
        source = OUT/'sources'/reference['file']
        full = inspect_3mf(source,i)
        meta = reference['metadata']
        item = {'id': str(i), 'title':meta.get('Title'), 'designer':meta.get('Designer'),
                'license_metadata':meta.get('License'), 'source_file':source.name,
                'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                'geometry_status':'Full source coordinates for individual components; assembled placement and fit UNKNOWN.',
                'pictures':[], 'components':[]}
        # Three source images already visually inspected. No image generation/editing.
        pic = reference['pictures'][1 if i == 0 else 0]
        path = ROOT/pic['local']
        name = 'reference_%s%s' % (i,path.suffix)
        asset(name,path.read_bytes(),'image/webp')
        item['pictures'].append({'url':'/rack-references/'+name,'source_member':pic['member']})
        for m in full['meshes']:
            name = 'component_%s_%s.json' % (i,m['object_id'])
            geometry = {'vertices': m['_vertices'], 'triangles':m['_triangles']}
            asset(name,(json.dumps(geometry,separators=(',',':'))+'\n').encode('utf-8'),'application/json')
            item['components'].append({'id':m['object_id'],'name':next(iter(m['names']),m['object_id']),
                'source_member':m['member'],'unit':m['unit'],'extent_mm':m['extent_mm'],
                'vertices':m['vertices'],'triangles':m['triangles'], 'url':'/rack-references/'+name})
        catalog['references'].append(item)
    asset('catalog.json',(json.dumps(catalog,indent=2,ensure_ascii=False)+'\n').encode('utf-8'),'application/json')
    write_json(target/'asset-manifest.json',manifest)
    (target/'LOCAL_ONLY.md').write_text(
        '# Local reference assets\n\nExtracted from Brian\'s supplied 3MFs for local inspection. '
        'License strings are archive metadata, not permission clearance. No redistribution, release packaging or publishing is authorized. '
        'Full source coordinates are preserved; these are not a rack manufacturing adapter. '
        'Photos are unchanged embedded creator reference images. Asset hashes are integrity checks, not rights or physical approval.\n',encoding='utf-8')
    print('Prepared %s local reference assets; no manufacturing geometry generated.' % len(manifest))


if __name__ == '__main__':
    main()
