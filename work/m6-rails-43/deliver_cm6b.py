"""Explicit CM6B acceptance build and local delivery. Never user data."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'outputs/Mechanical_Design_App'))
sys.path.insert(0,str(HERE))
import equipment as eq
from measure_reference import mesh_info,crossing_intervals

spec=json.loads((HERE/'cm6b-spec.json').read_text(encoding='utf-8'))
folder=eq.render(spec,HERE/'render-data')
# A failed exact check blocks creation of a proposed delivery on future runs.
for part in ('faceplate','rail_l','rail_r'):
    _,_,preflight=mesh_info(folder/(part+'.stl'))
    if not preflight['closed'] or preflight['components']!=1:
        raise ValueError('Delivery blocked: each part must be one closed solid.')
preflight_source=HERE/'preflight-intersection.scad'
preflight_source.write_text('intersection(){import("'+(folder/'faceplate.stl').as_posix()+'");union(){import("'+(folder/'rail_l.stl').as_posix()+'");import("'+(folder/'rail_r.stl').as_posix()+'");}}\n',encoding='utf-8')
preflight_run=subprocess.run(['C:/Program Files/OpenSCAD/openscad.exe','--export-format','asciistl','-o',str(HERE/'preflight-intersection.stl'),str(preflight_source)],capture_output=True,text=True,timeout=300,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
if 'top level object is empty' not in preflight_run.stderr.lower():
    raise ValueError('Delivery blocked: faceplate and rails do not render an empty intersection.')
out=ROOT/'outputs/CM1000_M6_generated_2026-10-28'
out.mkdir(exist_ok=True)
names={'faceplate':'CM6B_faceplate_with_stubs','rail_l':'CM6B_rail_left','rail_r':'CM6B_rail_right'}
for part,name in names.items():
    shutil.copyfile(folder/(part+'.stl'),out/(name+'.stl'))
shutil.copyfile(folder/'equipment.scad',out/'CM6B_source.scad')
(out/'CM6B_spec.json').write_text(json.dumps(spec,indent=2),encoding='utf-8')
target=out/'CM6B_CM1000_generated_split_rails.3mf'
cmd=[sys.executable,str(ROOT/'tools/plate_layout_stl.py')]+[str(folder/(p+'.stl')) for p in names]+[str(target)]
subprocess.run(cmd,check=True,cwd=ROOT)
# Descriptive object labels; vertices and triangles remain the packer's unchanged output.
with zipfile.ZipFile(target) as z:entries={n:z.read(n) for n in z.namelist()}
model=entries['3D/3dmodel.model'].decode('utf-8')
for part,name in names.items():model=model.replace('name="'+part+'"','name="'+name+'"')
entries['3D/3dmodel.model']=model.encode('utf-8')
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
    for n,b in entries.items():z.writestr(n,b)
results={'source_sha256':hashlib.sha256((folder/'equipment.scad').read_bytes()).hexdigest(),'parts':{},'build_report':json.loads((folder/'revision.json').read_text(encoding='utf-8'))}
for part in names:
    vs,ts,info=mesh_info(folder/(part+'.stl'))
    probes={}
    def probe(label,axis,p):probes[label]=dict(axis='XYZ'[axis],fixed=p,material_intervals=crossing_intervals(vs,ts,axis,p))
    x=-104.4 if part!='rail_r' else 104.4
    for z in [8.6,35.85]:
        probe(f'hole-X-Z{z}',0,[0,8 if part=='faceplate' else 14,z])
        probe(f'hole-Z-Z{z}',2,[x,8 if part=='faceplate' else 14,0])
        probe(f'hole-Y-Z{z}',1,[x,0,z])
    if part!='faceplate':
        probe('bay-Z',2,[x,30,0])
        probe('bay-Y-off-bore',1,[x-4 if part=='rail_l' else x+4,0,8.6])
        probe('non-bay-floor-top',2,[x,80,0])
        probe('engraved-ID',2,[x,101.7,0])
    else:
        for x0 in [-118.2625,118.2625]:
            for z0 in [6.323,38.127]:probe(f'rack-slot-{x0}-{z0}',0,[0,-2,z0])
    info['probes']=probes
    results['parts'][part]=info
intersection=HERE/'intersection.scad'
intersection.write_text('intersection(){import("'+(folder/'faceplate.stl').as_posix()+'");union(){import("'+(folder/'rail_l.stl').as_posix()+'");import("'+(folder/'rail_r.stl').as_posix()+'");}}\n',encoding='utf-8')
p=subprocess.run(['C:/Program Files/OpenSCAD/openscad.exe','--export-format','asciistl','-o',str(HERE/'intersection.stl'),str(intersection)],capture_output=True,text=True,timeout=300,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
(HERE/'intersection.log').write_text(p.stdout+p.stderr,encoding='utf-8')
results['intersection']=dict(returncode=p.returncode,empty='top level object is empty' in p.stderr.lower(),log=p.stderr)
with zipfile.ZipFile(target) as z:root=ET.fromstring(z.read('3D/3dmodel.model'))
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
results['3mf_objects']=[o.attrib for o in root.findall('m:resources/m:object',ns)]
(HERE/'cm6b-measurements.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in results.items() if k not in ('parts','build_report')},indent=2))
for part,info in results['parts'].items():print(part,info['closed'],info['components'],info['bounds'])
