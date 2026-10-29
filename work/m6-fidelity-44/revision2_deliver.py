"""Replace only the explicitly authorized unprinted CM6B candidate delivery."""
import hashlib
import json
import shutil
import sys
import zipfile
import io
import xml.etree.ElementTree as ET
from measure import ROOT,HERE
REV=HERE/'revision2'
OUT=ROOT/'outputs/CM1000_M6_generated_2026-10-28'
sys.path.insert(0,str(ROOT/'outputs/Mechanical_Design_App'))
import equipment as eq
import print_layout

def main():
    audit=json.loads((REV/'audit.json').read_text(encoding='utf-8'))
    preservation=json.loads((REV/'preservation.json').read_text(encoding='utf-8'))
    assert preservation['all_14_identical'] and preservation['protected_identical']
    assert all(p['closed'] and p['components']==1 for p in audit['parts'].values())
    assert audit['structural_intersection']['empty'] and audit['colour_intersection']['empty']
    assert 'RESULT: all checks passed' in (REV/'checks-verified.log').read_text(encoding='utf-8')
    spec=json.loads((REV/'spec.json').read_text(encoding='utf-8'))
    source=eq.source(eq.clean(spec))
    assert source==(REV/'candidate.scad').read_text(encoding='utf-8')
    names={'faceplate':'CM6B_faceplate_with_stubs','rail_l':'CM6B_rail_left','rail_r':'CM6B_rail_right'}
    names.update({f'pipe_{i}':f'CM6B_light_pipe_{i}' for i in range(1,6)})
    names.update({f'vector_{i}':f'CM6B_logo_letter_{i}' for i in range(1,8)})
    names.update({f'vector_{i+7}':f'CM6B_detail_{i}' for i in range(1,3)})
    parts={n:(REV/(n+'.stl')).read_text(encoding='utf-8') for n in names}
    blob=print_layout.layout_3mf(parts)
    with zipfile.ZipFile(io.BytesIO(blob)) as z:entries={n:z.read(n) for n in z.namelist()}
    model=ET.fromstring(entries['3D/3dmodel.model'])
    ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
    objects=model.findall('m:resources/m:object',ns)
    assert len(objects)==len(model.findall('m:build/m:item',ns))==17
    # Prove packaged geometry is each source part under the packer's rigid shared placement.
    placement=dict(print_layout.place(parts));parity=[]
    for obj in objects:
        n=obj.attrib['name']
        vs=[tuple(float(v.attrib[k]) for k in ('x','y','z')) for v in obj.findall('m:mesh/m:vertices/m:vertex',ns)]
        tris=[tuple(sorted(vs[int(t.attrib[k])] for k in ('v1','v2','v3'))) for t in obj.findall('m:mesh/m:triangles/m:triangle',ns)]
        expected=[tuple(sorted(tuple(round(x,6) for x in v) for v in t)) for t in placement[n]]
        assert sorted(tris)==sorted(expected),n
        parity.append(dict(part=n,triangles=len(tris),identical_after_layout_and_6dp_encoding=True))
    raw=entries['3D/3dmodel.model'].decode('utf-8')
    for n,label in names.items():raw=raw.replace('name="'+n+'"','name="'+label+'"')
    entries['3D/3dmodel.model']=raw.encode('utf-8')
    with zipfile.ZipFile(OUT/'CM6B_CM1000_generated_split_rails.3mf','w',zipfile.ZIP_DEFLATED) as z:
        for n,b in entries.items():z.writestr(n,b)
    for n,label in names.items():shutil.copyfile(REV/(n+'.stl'),OUT/(label+'.stl'))
    (OUT/'CM6B_source.scad').write_text(source,encoding='utf-8',newline='\n')
    shutil.copyfile(REV/'spec.json',OUT/'CM6B_spec.json')
    proof=dict(objects=17,structural_objects=3,pipes=5,logo_letters=7,details=2,colour_materials=2,mesh_parity=parity)
    (REV/'3mf-proof.json').write_text(json.dumps(proof,indent=2),encoding='utf-8')
    evidence=OUT/'validation';evidence.mkdir(exist_ok=True)
    for n in ['audit.json','preservation.json','hdt-regression.json','3mf-proof.json','checks-verified.log']:
        shutil.copyfile(REV/n,evidence/n)
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.is_file() and p.name!='README.md'}
    (REV/'delivery-sha256.json').write_text(json.dumps(hashes,indent=2),encoding='utf-8')
    print('Delivered 17 closed parts and 17-object coloured 3MF; pocket fidelity remains FAIL.')

if __name__=='__main__':main()
