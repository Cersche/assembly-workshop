"""Explicit SCR5-B build/check/pack; Python 3.10 standard library, OpenSCAD.exe."""
import argparse
import copy
from collections import Counter, defaultdict
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import struct
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile

HERE = Path(__file__).resolve().parent.parent
ROOT = HERE.parents[1]
CHECKS = HERE / 'checks'
SOURCE = HERE / 'src/SCR5-B.scad'
OPENSCAD = Path('C:/Program Files/OpenSCAD/openscad.exe')
CORE = 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
NAMES = ['SCR5-B plate', 'SCR5-B rear frame']


def dump(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def bounds(v):
    return [[min(p[k] for p in v), max(p[k] for p in v)] for k in range(3)]


def read_stl(path):
    data = path.read_bytes()
    count = struct.unpack_from('<I', data, 80)[0]
    assert len(data) == 84 + 50*count, 'Require binary STL, exact float32 coordinates'
    verts, tris, lookup = [], [], {}
    for i in range(count):
        c = struct.unpack_from('<9f', data, 96+50*i)
        tri = []
        for k in range(0, 9, 3):
            p = tuple(c[k:k+3])
            if p not in lookup:
                lookup[p] = len(verts)
                verts.append(p)
            tri.append(lookup[p])
        tris.append(tuple(tri))
    return verts, tris


def mesh_check(mesh):
    v, t = mesh
    assert all(math.isfinite(c) for p in v for c in p)
    edges, directed, adj = defaultdict(list), Counter(), defaultdict(set)
    degenerate = []
    volume = 0
    for i, tri in enumerate(t):
        assert len(set(tri)) == 3 and all(0 <= a < len(v) for a in tri)
        a, b, c = (v[k] for k in tri)
        area = cross(sub(b, a), sub(c, a))
        if dot(area, area) == 0:
            degenerate.append(i)
        volume += dot(a, cross(b, c))/6
        for a, b in zip(tri, tri[1:]+tri[:1]):
            edges[tuple(sorted((a, b)))].append(i)
            directed[(a, b)] += 1
    bad = [e for e, faces in edges.items() if len(faces) != 2]
    winding = [e for e in edges if directed[e] != 1 or directed[e[::-1]] != 1]
    for faces in edges.values():
        for a in faces:
            adj[a].update(faces)
    todo, shells = set(range(len(t))), 0
    while todo:
        shells += 1
        stack = [todo.pop()]
        while stack:
            for n in adj[stack.pop()]:
                if n in todo:
                    todo.remove(n)
                    stack.append(n)
    return {'vertices': len(v), 'triangles': len(t), 'edges': len(edges),
            'bounds': bounds(v), 'shells': shells, 'bad_edges': len(bad),
            'inconsistent_winding_edges': len(winding), 'degenerate_faces': degenerate,
            'signed_volume_mm3': volume,
            'pass': shells == 1 and not bad and not winding and not degenerate and volume > 0}


def render(part, target):
    command = [str(OPENSCAD),'--export-format','binstl','-o',str(target),'-D',f'part="{part}"',str(SOURCE)]
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', errors='replace')
    log = result.stdout + result.stderr
    (CHECKS/(part+'.log')).write_text(log,encoding='utf-8')
    if result.returncode or 'ERROR:' in log:
        raise RuntimeError(log)
    return log


def pack(meshes, gap):
    ET.register_namespace('',CORE)
    root=ET.Element('{'+CORE+'}model',{'unit':'millimeter','xml:lang':'en-US'})
    ET.SubElement(root,'metadata',{'name':'Title'}).text='SCR5-B PARAMETERIZED DIGITAL BUILD; PHYSICAL VALIDATION UNKNOWN'
    res=ET.SubElement(root,'resources'); build=ET.SubElement(root,'build')
    layouts=[]; next_x=0
    for i,(v,t) in enumerate(meshes,1):
        # Plate front on bed; frame rear on bed, so pads rise from its ring.
        rot=[(x,-z,y) if i==1 else (x,z,-y) for x,y,z in v]; b=bounds(rot)
        shift=(next_x-b[0][0],-b[1][0],-b[2][0])
        placed=[tuple(p[k]+shift[k] for k in range(3)) for p in rot]
        obj=ET.SubElement(res,'object',{'id':str(i),'type':'model','name':NAMES[i-1]})
        mesh=ET.SubElement(obj,'mesh'); vs=ET.SubElement(mesh,'vertices'); ts=ET.SubElement(mesh,'triangles')
        for x,y,z in placed:
            ET.SubElement(vs,'vertex',{'x':repr(x),'y':repr(y),'z':repr(z)})
        for a,b_,c in t:
            ET.SubElement(ts,'triangle',{'v1':str(a),'v2':str(b_),'v3':str(c)})
        ET.SubElement(build,'item',{'objectid':str(i)})
        layouts.append({'rotation':'(x,y,z) -> (x,-z,y)' if i==1 else '(x,y,z) -> (x,z,-y)','translation_after_rotation':shift,'bounds':bounds(placed)})
        next_x=bounds(placed)[0][1]+gap
    path=HERE/'SCR5-B_screen_plate_and_frame.3mf'
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml','<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
        z.writestr('_rels/.rels','<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
        z.writestr('3D/3dmodel.model',ET.tostring(root,encoding='utf-8',xml_declaration=True))
    dump(CHECKS/'placement.json',layouts)
    return path


def reopen(path, originals):
    # Independent fresh ZIP/XML traversal, independent of writing tree.
    with zipfile.ZipFile(path) as z:
        assert set(z.namelist()) == {'[Content_Types].xml','_rels/.rels','3D/3dmodel.model'}
        rel=ET.fromstring(z.read('_rels/.rels'))
        assert len(rel)==1 and rel[0].get('Target')=='/3D/3dmodel.model'
        assert rel[0].get('Type')=='http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel'
        ct=ET.fromstring(z.read('[Content_Types].xml'))
        assert {c.get('Extension'):c.get('ContentType') for c in ct} == {'rels':'application/vnd.openxmlformats-package.relationships+xml','model':'application/vnd.ms-package.3dmanufacturing-3dmodel+xml'}
        raw=z.read('3D/3dmodel.model')
    assert b'<vertex ' in raw and b'<triangle ' in raw and b'ns0:' not in raw
    q=lambda s:'{'+CORE+'}'+s
    root=ET.fromstring(raw); assert root.get('unit')=='millimeter'
    objects=root.findall('./'+q('resources')+'/'+q('object'))
    items=root.findall('./'+q('build')+'/'+q('item'))
    assert len(objects)==len(items)==2
    result=[]; boxes=[]
    for i,(obj,item,(ov,ot)) in enumerate(zip(objects,items,originals),1):
        assert obj.get('name')==NAMES[i-1] and obj.get('id')==item.get('objectid')==str(i)
        assert item.get('transform') is None and obj.find(q('components')) is None
        v=[tuple(float(e.get(k)) for k in ('x','y','z')) for e in obj.findall('./'+q('mesh')+'/'+q('vertices')+'/'+q('vertex'))]
        t=[tuple(int(e.get(k)) for k in ('v1','v2','v3')) for e in obj.findall('./'+q('mesh')+'/'+q('triangles')+'/'+q('triangle'))]
        assert len(v)==len(ov) and t==ot
        assert all(math.isfinite(c) for p in v for c in p)
        b=bounds(v); assert b[2][0]==0
        # Recover rigid shift from first vertex, verify every coordinate and
        # every triangle index exactly (no scaling / tolerance-based matching).
        transformed=[(x,-zz,y) if i==1 else (x,zz,-y) for x,y,zz in ov]
        shift=sub(v[0],transformed[0])
        assert all(a==tuple(c[k]+shift[k] for k in range(3)) for a,c in zip(v,transformed))
        checked=mesh_check((v,t)); assert checked['pass'],checked
        boxes.append(b); result.append({'name':obj.get('name'),**checked,'triangle_equivalence':'exact indexed triangles after rigid rotation and translation'})
    actual_gap=boxes[1][0][0]-boxes[0][0][1]; assert actual_gap>0
    return {'objects':result,'positive_gap_mm':actual_gap,'plain_tags':True,'relationships':'pass','slicer_load':'NOT TESTED'}


def preserved():
    base=json.loads((CHECKS/'baseline.json').read_text(encoding='utf-8'))
    changed=[]
    for name, old in base['sha256'].items():
        if name=='HANDOFF.md':
            continue
        if not (ROOT/name).is_file() or sha(ROOT/name)!=old:
            changed.append(name)
    assert not changed, changed
    return {'protected_files_compared':len(base['sha256'])-1,'changed':changed,'handoff':'excluded: authorized update','scope':base['roots']}


def parameter_checks(doc):
    p=doc['values']
    signed={'pcb_reg_x','pcb_reg_z','active_offset_x','active_offset_z','ribbon_x','buttons_x','id_x','seat_y'}
    for key,value in p.items():
        seq=value if isinstance(value,list) else [value]
        assert all(isinstance(v,(int,float)) and math.isfinite(v) for v in seq),key
        if key not in signed and not isinstance(value,list):
            assert all(v>0 for v in seq),key
    for key in ('touch_keepout','fpc_keepout'):
        assert len(p[key])==6 and all(v>0 for v in p[key][3:]),key
    assert p['seat_y']==0, 'Lip seating datum is Y=0'
    assert [p[k] for k in ('plate_w','plate_h','plate_t','plate_r')]==[252,88.8,4,2.5]
    assert p['slot_x']==118.2625 and p['slot_z']==[6.323,38.127,50.773,82.577]
    assert p['centre_z']==44.45 and p['rack_pitch']==44.45
    assert p['boss_end_y']==p['pocket_depth']==p['frame_front_y']
    assert p['insert_length']<=p['insert_seat_depth']<p['boss_end_y']
    assert p['insert_leadin']<p['insert_length']
    assert p['insert_pilot']>0 and p['insert_pilot']<p['insert_od']+2*p['boss_wall']
    assert p['screw_clearance']>2.5
    assert p['id_depth']<p['frame_t']
    assert p['screw_head_d']+p['head_clearance_d']<2*(p['frame_outer_w']/2-p['boss_x'])
    assert p['tool_d']<2*(p['frame_outer_w']/2-p['boss_x'])
    stack=p['frame_t']; engagement=p['screw_length']-stack
    limits=[stack+p['minimum_engagement'],stack+p['insert_length']-p['tip_clearance']]
    assert limits[0]<=p['screw_length']<=limits[1], 'Screw outside engagement/tip range'
    assert 0<p['preload']<p['total_depth']
    pad_front=p['seat_y']+p['total_depth']-p['preload']
    assert pad_front>0 and pad_front<p['frame_front_y']
    br=p['insert_od']/2+p['boss_wall']
    cx,ch=p['pocket_half_x'],p['pocket_half_z']
    # Full configured outlines including insertion clearances; rectangular rear path.
    gx=[-p['glass_w']/2-p['glass_clear_left'],p['glass_w']/2+p['glass_clear_right']]
    gz=[p['centre_z']-p['glass_h']/2-p['glass_clear_bottom'],p['centre_z']+p['glass_h']/2+p['glass_clear_top']]
    px=[p['pcb_reg_x']-p['pcb_w']/2-p['pcb_clear_x'],p['pcb_reg_x']+p['pcb_w']/2+p['pcb_clear_x']]
    pz=[p['centre_z']+p['pcb_reg_z']-p['pcb_h']/2-p['pcb_clear_z'],p['centre_z']+p['pcb_reg_z']+p['pcb_h']/2+p['pcb_clear_z']]
    assert min(gx+px)>-cx and max(gx+px)<cx
    assert min(gz+pz)>p['centre_z']-ch and max(gz+pz)<p['centre_z']+ch
    assert ch+p['pocket_wall']<p['plate_h']/2
    assert 0<p['pocket_relief_r']<p['pocket_wall']
    assert cx+p['pocket_wall']<104
    boss_gap=p['boss_x']-br-max(abs(v) for v in gx+px)
    assert boss_gap>=1, 'Boss must clear configured screen outlines by >=1 mm'
    assert p['boss_x']+br<=cx+p['pocket_wall'] and p['boss_x']+br>cx
    assert all(p['centre_z']-ch+br<z<p['centre_z']+ch-br for z in p['boss_z'])
    assert len(p['boss_z'])==2 and abs(p['boss_z'][1]-p['boss_z'][0])>2*br
    for outer,inner,rout,rin in [('frame_outer_w','frame_inner_w','frame_outer_r','frame_inner_r'),('frame_outer_h','frame_inner_h','frame_outer_r','frame_inner_r')]:
        assert p[outer]>p[inner] and 0<p[rout]<p[outer]/2 and 0<p[rin]<p[inner]/2
    assert 0<p['pad_r']<min(p['pad_w'],p['pad_h'])/2
    assert p['pad_x']-p['pad_w']/2>p['frame_inner_w']/2
    assert p['pad_x']+p['pad_w']/2 < p['frame_outer_w']/2
    assert p['pad_x']+p['pad_w']/2 < p['pcb_w']/2-abs(p['pcb_reg_x'])
    assert p['pad_z_offset']+p['pad_h']/2 < p['pcb_h']/2-abs(p['pcb_reg_z'])
    aw=p['glass_w']-p['lip_left']-p['lip_right']; ah=p['glass_h']-p['lip_top']-p['lip_bottom']
    ax=(p['lip_left']-p['lip_right'])/2; az=p['centre_z']+(p['lip_bottom']-p['lip_top'])/2
    r=p['aperture_r']; assert 0<r<min(aw,ah)/2
    active=[p['active_offset_x']-p['active_w']/2-p['active_keepout'],p['active_offset_x']+p['active_w']/2+p['active_keepout'],p['centre_z']+p['active_offset_z']-p['active_h']/2-p['active_keepout'],p['centre_z']+p['active_offset_z']+p['active_h']/2+p['active_keepout']]
    assert all(max(abs(x-ax)-aw/2+r,0)**2+max(abs(z-az)-ah/2+r,0)**2<r*r for x in active[:2] for z in active[2:]), 'Rounded aperture covers configured active keepout'
    assert p['boss_x']-br>abs(ax)+aw/2
    # Access cuts stay above the pads and clear all boss and tool projections.
    for prefix in ('ribbon','buttons'):
        x=p[prefix+'_x'];z=p[prefix+'_z'];mr=p[prefix+'_mouth_r']
        w=p[prefix+'_width']+2*mr;h=p[prefix+'_height']+2*mr
        y=p['ribbon_cut_y'] if prefix=='ribbon' else p['buttons_y']
        assert y>0 and y<p['total_depth'] and y+p[prefix+'_depth']>=p['frame_front_y']+p['frame_t']
        assert p[prefix+'_edge_r']<min(w,h)/2
        assert 2*mr<p['frame_t']
        assert z-h/2>p['centre_z']+p['pad_z_offset']+p['pad_h']/2
        for bx in (-p['boss_x'],p['boss_x']):
            for bz in p['boss_z']:
                assert math.hypot(max(abs(bx-x)-w/2,0),max(abs(bz-z)-h/2,0))>max(br,p['tool_d']/2)
    return {'status':'PASS — conditional digital geometry; no physical approval','architecture_blockers':[],
        'active_keepout_xz':active,'aperture_xz':[ax-aw/2,ax+aw/2,az-ah/2,az+ah/2],
        'active_registration':'UNKNOWN; configured offset 0 and 0.25 margin only',
        'boss_axes_xz':[[x,z] for x in (-p['boss_x'],p['boss_x']) for z in p['boss_z']],
        'boss_radius_mm':br,'boss_to_screen_with_clearance_mm':boss_gap,
        'screen_clearance_outlines':{'glass_x':gx,'glass_z':gz,'pcb_x':px,'pcb_z':pz},
        'pocket_reliefs':'outward circles at square cavity corners; square seating path is a subset',
        'pad_front_y':pad_front,'preload_mm':p['preload'],'pad_projection_mm':p['frame_front_y']-pad_front,
        'screw_stack_mm':stack,'screw_length_range_mm':limits,'selected_length_mm':p['screw_length'],
        'nominal_engagement_mm':engagement,'insert_tip_reserve_mm':p['insert_length']-engagement,
        'pilot_floor_mm':p['boss_end_y']-p['insert_seat_depth'],
        'engraving_remaining_wall_mm':p['frame_t']-p['id_depth'],
        'fixed_rear_y':p['pocket_depth'],'frame_rear_y':p['frame_front_y']+p['frame_t'],
        'screw_head_rear_y':p['frame_front_y']+p['frame_t']+p['screw_head_h'],
        'physical_unknowns':doc['unknown_measurements']}


def load_module(name):
    spec=importlib.util.spec_from_file_location(name,HERE/'src'/('SCR5-B_'+name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--final',action='store_true',help='Explicit conditional digital build, checks and packaging')
    group.add_argument('--check-only',action='store_true',help='Verify recorded inputs/meshes without rendering')
    args=parser.parse_args()
    doc=json.loads((HERE/'SCR5-B_parameters.json').read_text(encoding='utf-8'))
    conditions=parameter_checks(doc) # Fail BEFORE replacing any rendered file.
    dump(CHECKS/'acceptance.json',{'status':'CHECKS IN PROGRESS; package not yet validated'})
    dump(CHECKS/'conditional-clearance.json',conditions)
    p=doc['values']; inputs=[SOURCE,HERE/'SCR5-B_parameters.json',HERE/'src/SCR5-B_config.scad']
    if args.check_only:
        recorded=json.loads((CHECKS/'render-inputs.json').read_text(encoding='utf-8'))
        assert all(recorded[f.relative_to(HERE).as_posix()]==sha(f) for f in inputs),'Inputs changed: explicit --final rebuild required'
    else:
        assert OPENSCAD.name.lower()=='openscad.exe' and OPENSCAD.is_file()
        (HERE/'src/SCR5-B_config.scad').write_text('// Generated from parameters JSON; mm, numeric assumptions remain UNKNOWN physically.\n'+'\n'.join(k+'='+json.dumps(v)+';' for k,v in p.items())+'\n',encoding='utf-8')
        for part in ('plate','frame'):
            print('Rendering',part,flush=True);render(part,HERE/f'SCR5-B_{part}.stl')
        dump(CHECKS/'render-inputs.json',{f.relative_to(HERE).as_posix():sha(f) for f in inputs})
        version=subprocess.run([str(OPENSCAD),'--version'],capture_output=True,text=True,encoding='utf-8',errors='replace')
        dump(CHECKS/'build-context.json',{'python':sys.version,'openscad':version.stdout+version.stderr,'renderer':str(OPENSCAD),'invocation':'py -3.10 src/SCR5-B_build.py --final','format':'binary STL, no vertex repair/welding/rounding','automatic_build':False})
    meshes=[read_stl(HERE/f'SCR5-B_{part}.stl') for part in ('plate','frame')]
    topology={name:mesh_check(mesh) for name,mesh in zip(NAMES,meshes)}
    dump(CHECKS/'topology.json',topology)
    assert all(c['pass'] for c in topology.values()),topology
    expected=[[-126,126],[-4,20],[.05,88.85]]
    assert all(abs(x-y)<1e-5 for a,c in zip(topology[NAMES[0]]['bounds'],expected) for x,y in zip(a,c))
    geometry=load_module('geometry_checks').run(sys.modules[__name__],doc,meshes,not args.check_only)
    dump(CHECKS/'geometry.json',geometry)
    path=pack(meshes,p['print_gap']) if not args.check_only else HERE/'SCR5-B_screen_plate_and_frame.3mf'
    roundtrip=reopen(path,meshes);dump(CHECKS/'3mf-roundtrip.json',roundtrip)
    load_module('review').make(sys.modules[__name__],doc)
    dump(CHECKS/'preservation.json',preserved())
    hashfiles=list((HERE/'src').glob('*.py'))+list((HERE/'src').glob('*.scad'))+list(HERE.glob('*.stl'))+list(CHECKS.glob('*.stl'))+[HERE/'SCR5-B_parameters.json',path]
    dump(CHECKS/'hashes.json',{f.relative_to(HERE).as_posix():sha(f) for f in hashfiles})
    dump(CHECKS/'acceptance.json',{'status':'PASS — --final digital gate; physical validation UNKNOWN','topology':'pass','geometry':'pass','3mf':'independent exact rigid roundtrip pass; two named objects, plain tags','architecture':'plate bosses -> screws -> removable frame -> edge pads -> screen -> lip; no screen fasteners or interspace access','unknowns':list(doc['unknown_measurements']),'physical':'NOT PRINTED; vendor nominal; fit, preload, retention, access, ribbon reach and strength UNKNOWN','private_artifact':'private Artifact publishing pending in Claude'})
    (CHECKS/'final-gate.log').write_text('PASS: --final digital architecture, mesh, geometry, packaging and preservation checks. Physical UNKNOWNs are documented parameters, not approvals.\n',encoding='utf-8')
    print(json.dumps({'status':'PASS','topology':topology,'3mf_gap_mm':roundtrip['positive_gap_mm']},indent=2))


if __name__=='__main__':
    try: main()
    except Exception as exc:
        dump(CHECKS/'acceptance.json',{'status':'FAILED; no validated current export','error':str(exc)})
        raise
