"""Focused mesh measurements and intersection screening; standard library.

Topology always uses exact parsed coordinates in the builder. This supplementary
triangle intersection screen uses 1e-9 mm predicate tolerance, never moves vertices.
"""
import copy
import math
from pathlib import Path
import subprocess


def y_hits(mesh, x, z):
    """Intersections of line (x,Y,z) with triangles, in original coordinates."""
    v,t=mesh; result=[]
    for tri in t:
        a,b,c=(v[k] for k in tri)
        den=(b[2]-c[2])*(a[0]-c[0])+(c[0]-b[0])*(a[2]-c[2])
        if den==0:
            continue
        u=((b[2]-c[2])*(x-c[0])+(c[0]-b[0])*(z-c[2]))/den
        w=((c[2]-a[2])*(x-c[0])+(a[0]-c[0])*(z-c[2]))/den
        if u>=-1e-10 and w>=-1e-10 and u+w<=1+1e-10:
            result.append(u*a[1]+w*b[1]+(1-u-w)*c[1])
    return sorted(set(result))


def strict_triangle_screen(b, mesh):
    """Sweep AABBs; detect coplanar area overlap and transverse crossings.

    Incident edge pairs are excluded: they have their intended exact shared edge
    and are already checked for closure and winding. Vertex-only pairs are tested.
    This is a numerical digital screen, not an exact-arithmetic solid proof.
    """
    v,t=mesh; eps=1e-9
    tris=[tuple(v[k] for k in tri) for tri in t]
    boxes=[b.bounds(tri) for tri in tris]
    normals=[b.cross(b.sub(tri[1],tri[0]),b.sub(tri[2],tri[0])) for tri in tris]
    order=sorted(range(len(t)),key=lambda i:boxes[i][0][0])
    candidates=0; coplanar=0; bad=[]; active=[]

    def segment_triangle(p,q,tri):
        e1=b.sub(tri[1],tri[0]);e2=b.sub(tri[2],tri[0]);d=b.sub(q,p)
        h=b.cross(d,e2); det=b.dot(e1,h)
        if abs(det)<1e-14:
            return None
        s=b.sub(p,tri[0]);u=b.dot(s,h)/det
        qq=b.cross(s,e1);w=b.dot(d,qq)/det;tt=b.dot(e2,qq)/det
        if -eps<=u<=1+eps and -eps<=w and u+w<=1+eps and -eps<=tt<=1+eps:
            return tuple(p[k]+tt*d[k] for k in range(3))
        return None

    def area_overlap(a,c,n):
        drop=max(range(3),key=lambda k:abs(n[k]));axes=[k for k in range(3) if k!=drop]
        aa=[tuple(p[k] for k in axes) for p in a];cc=[tuple(p[k] for k in axes) for p in c]
        orient=lambda p,q,r:(q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
        sign=1 if orient(*cc)>0 else -1
        poly=aa
        for u,w in zip(cc,cc[1:]+cc[:1]):
            result=[]
            if not poly:
                break
            for p,q in zip(poly,poly[1:]+poly[:1]):
                dp=sign*orient(u,w,p);dq=sign*orient(u,w,q)
                pin=dp>=0; qin=dq>=0
                if pin:
                    result.append(p)
                if pin!=qin:
                    ratio=dp/(dp-dq)
                    result.append(tuple(p[k]+ratio*(q[k]-p[k]) for k in range(2)))
            poly=result
        # Translate before shoelace to avoid subtracting large nearly equal areas.
        if len(poly)<3:
            return False
        poly=[tuple(p[k]-poly[0][k] for k in range(2)) for p in poly]
        area=abs(sum(p[0]*q[1]-p[1]*q[0] for p,q in zip(poly,poly[1:]+poly[:1])))/2
        return area>1e-10

    for i in order:
        bb=boxes[i]; active=[j for j in active if boxes[j][0][1]>=bb[0][0]]
        for j in active:
            bc=boxes[j]
            if any(bb[k][1]<bc[k][0] or bc[k][1]<bb[k][0] for k in (1,2)):
                continue
            shared=set(t[i])&set(t[j])
            if len(shared)>=2:
                continue
            candidates+=1
            n=normals[i];norm=math.sqrt(b.dot(n,n))
            distances=[b.dot(n,b.sub(p,tris[i][0]))/norm for p in tris[j]]
            if min(distances)>eps or max(distances)<-eps:
                continue
            if all(abs(d)<eps for d in distances):
                coplanar+=1
                if area_overlap(tris[i],tris[j],n):
                    bad.append([j,i,'coplanar area overlap'])
            else:
                allowed=[v[k] for k in shared]
                for a,c in ((tris[i],tris[j]),(tris[j],tris[i])):
                    for p,q in zip(a,a[1:]+a[:1]):
                        hit=segment_triangle(p,q,c)
                        if hit is not None and not any(max(abs(x-y) for x,y in zip(hit,sv))<eps for sv in allowed):
                            bad.append([j,i,'nonincident crossing'])
                            break
                    if bad and bad[-1][:2]==[j,i]:
                        break
        active.append(i)
    return {'candidate_nonedge_pairs':candidates,'coplanar_pairs':coplanar,
            'intersections':bad,'pass':not bad,'predicate_tolerance_mm':eps,
            'scope':'AABB sweep, incident edges excluded; coplanar overlap and transverse segment/triangle screen; not exact-arithmetic certification'}


def run(b, doc, meshes, render_probes=True):
    p=doc['values'];plate,frame=meshes
    slots=[]
    for x in (-p['slot_x'],p['slot_x']):
        for z in p['slot_z']:
            free=[(x,z),(x-4.9,z),(x+4.9,z),(x,z-3.4),(x,z+3.4)]
            solid=[(x-5.1,z),(x+5.1,z),(x,z-3.6),(x,z+3.6)]
            assert all(not y_hits(plate,xx,zz) for xx,zz in free)
            assert all(y_hits(plate,xx,zz) for xx,zz in solid)
            verts=[v for v in plate[0] if abs(v[0]-x)<=5.0001 and abs(v[2]-z)<=3.5001]
            measured=b.bounds(verts)
            assert abs(measured[0][1]-measured[0][0]-10)<2e-5
            assert abs(measured[2][1]-measured[2][0]-7)<2e-5
            slots.append({'centre_xz':[x,z],'parsed_boundary_bounds':measured,'horizontal_10x7':True,'through_at_five_interior_rays':True})
    # Verify no front-facing opaque plate at centred assumed active corners.
    aperture_verts=[v for v in plate[0] if v[1]==-p['plate_t'] and abs(v[0])<60 and 8<v[2]<81]
    aperture_bounds=b.bounds(aperture_verts)
    assert abs(aperture_bounds[0][1]-aperture_bounds[0][0]-(p['glass_w']-p['lip_left']-p['lip_right']))<2e-5
    assert abs(aperture_bounds[2][1]-aperture_bounds[2][0]-(p['glass_h']-p['lip_top']-p['lip_bottom']))<2e-5
    assert abs(sum(aperture_bounds[0])/2-(p['lip_left']-p['lip_right'])/2)<2e-5
    assert abs(sum(aperture_bounds[2])/2-(p['centre_z']+(p['lip_bottom']-p['lip_top'])/2))<2e-5
    active=b.parameter_checks(doc)['active_keepout_xz']
    for x in active[:2]:
        for z in active[2:]:
            assert not [y for y in y_hits(plate,x,z) if -4.001<=y<=0.001]
    screw=[]
    for x in (-p['hole_dx']/2,p['hole_dx']/2):
        for z in (p['centre_z']-p['hole_dz']/2,p['centre_z']+p['hole_dz']/2):
            hits=y_hits(frame,x+p['pcb_reg_x'],z+p['pcb_reg_z'])
            assert len(hits)==2 and abs(hits[0]-p['frame_front_y'])<2e-5
            assert abs(hits[-1]-(p['frame_front_y']+p['frame_t']-p['insert_seat_depth']))<2e-5
            screw.append({'axis_xz':[x,z],'pilot_axis_material_hits_y':hits})
    noid=b.CHECKS/'SCR5-A_frame-unengraved-probe.stl'
    if render_probes:
        b.render('no_id',noid)
    noidmesh=b.read_stl(noid)
    removed=b.mesh_check(noidmesh)['signed_volume_mm3']-b.mesh_check(frame)['signed_volume_mm3']
    assert removed>1
    floor_y=p['frame_front_y']+p['frame_t']-p['id_depth']
    floor=[v for v in frame[0] if abs(v[1]-floor_y)<1e-6 and abs(v[0]-p['id_x'])<12 and abs(v[2]-p['id_z'])<3]
    assert len(floor)>20
    # CGAL intersection in common assembly datums; no translation/nudge.
    target=b.CHECKS/'SCR5-A_assembly-intersection.stl'
    if render_probes:
        args=[str(b.OPENSCAD),'--export-format','binstl','-o',str(target),'-D','part="intersection"',str(b.SOURCE)]
        proc=subprocess.run(args,capture_output=True,text=True,encoding='utf-8',errors='replace')
        log=proc.stdout+proc.stderr
        (b.CHECKS/'assembly-intersection.log').write_text(log,encoding='utf-8')
        assert proc.returncode in (0,1) and 'ERROR:' not in log, log
    else:
        log=(b.CHECKS/'assembly-intersection.log').read_text(encoding='utf-8')
    if target.exists():
        intermesh=b.read_stl(target); inter=b.mesh_check(intermesh)
        assert abs(inter['signed_volume_mm3'])<1e-9,inter
        assert all(all(intermesh[0][k][0]==intermesh[0][tri[0]][0] for k in tri)
                   and abs(intermesh[0][tri[0]][0])==p['clip_x']+p['clip_t']/2
                   for tri in intermesh[1]), 'Intersection must be only the intended two side-contact planes'
        assembly={'result':'boundary contact only','volume_mm3':inter['signed_volume_mm3'],'bounds':inter['bounds']}
    else:
        assert 'Current top level object is empty' in log,log
        assembly={'result':'empty CGAL intersection; no positive-volume collision','volume_mm3':0,
                  'contacts':'side stems nominally touch pocket inner wall X=+/-62.75; hooks have 0.5 rearward play before shoulders, not a collision'}
    selfcheck={name:strict_triangle_screen(b,m) for name,m in zip(b.NAMES,meshes)}
    b.dump(b.CHECKS/'self-intersection.json',selfcheck)
    assert all(c['pass'] for c in selfcheck.values()), 'Self-intersection screen failed; see JSON'
    # Invalid configurations must fail before any export, with no real data used.
    invalid={'long_screw':('screw_length',8),'short_screw':('screw_length',2),
             'deep_insert_seat':('insert_seat_depth',6),'zero_pilot':('insert_pilot',0),
             'negative_gap':('glass_pcb_gap',-1),'nan_clearance':('pcb_clear_x',float('nan')),
             'excess_aperture_radius':('aperture_r',40),'through_engraving':('id_depth',6),
             'clip_hits_pcb_when_retracted':('clip_x',62.25)}
    rejected=[]
    for case,(key,value) in invalid.items():
        test=copy.deepcopy(doc);test['values'][key]=value
        try:
            b.parameter_checks(test)
        except AssertionError:
            rejected.append(case)
        else:
            raise AssertionError('Invalid config was accepted: '+case)
    views=sorted(b.CHECKS.glob('*.stl'))
    subprocess.run([__import__('sys').executable,str(b.ROOT/'tools/mesh_viewer.py'),*[str(v) for v in views],'-o',str(b.ROOT/'work/mesh-viewer/SCR5-A-probes.html'),'-t','SCR5-A — retained probes, unengraved comparison and rejected first frame'],check=True)
    keepouts={}
    for key in ('touch_keepout','fpc_keepout'):
        k=p[key];box=[[k[i],k[i]+k[i+3]] for i in range(3)]
        candidates=0
        for tri in frame[1]:
            tb=b.bounds([frame[0][i] for i in tri])
            if all(tb[i][0]<box[i][1] and box[i][0]<tb[i][1] for i in range(3)):
                candidates+=1
        assert candidates==0, 'Provisional component box may touch frame: '+key
        keepouts[key]={'box':box,'overlapping_triangle_aabbs':candidates,'provenance':'assumed, not measured component geometry'}
    return {'slots':slots,'measured_aperture_bounds':aperture_bounds,'screw_pilots':screw,'assembly':assembly,'provisional_component_keepouts':keepouts,
            'engraving':{'source_text':'SCR5-A','removed_volume_mm3':removed,'floor_vertices':len(floor),'remaining_wall_mm':p['frame_t']-p['id_depth']},
            'invalid_configurations_rejected':rejected,'self_intersection_screen':'pass',
            'skipped_or_conditional':['Physical screen insertion/preassembly/clip deflection unverified',
             'Actual corner bearing regions/component/tool/access envelopes unverified',
             'Active registration unknown: centred corners are conditional only',
             'No exact-arithmetic self-intersection certification or slicer test']}
