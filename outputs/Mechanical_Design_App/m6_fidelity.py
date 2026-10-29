"""Optional numeric section/vector settings for primitive split-rail reconstruction.

No mesh files or hardware-specific defaults are read by this module.
"""
import math
import json

KEYS = ('m6_rail_len', 'm6_bay_h', 'm6_bay_d', 'm6_rail_profiles',
        'm6_side_windows', 'm6_stub_sections', 'm6_edge_radius',
        'm6_retention_slot', 'm6_light_pipes', 'm6_vectors', 'm6_nose_bridge')


def validate(spec, eq):
    out = {}
    for key, default, lo, hi in [('m6_rail_len', float(spec['dev_d'])+2, 38, 280),
                                ('m6_bay_h', 12, 6, 30), ('m6_bay_d', 34, 10, 100),
                                ('m6_edge_radius', 0, 0, 3)]:
        if key in spec:
            out[key] = eq.num(spec[key], key, lo, hi)
    h = out.get('m6_bay_h', 12)
    if 2*h+2*2.575+2.5 > float(spec.get('u',1))*44.45-.05:
        raise ValueError('Access bays need at least 2.5 mm of floor and top.')
    if out.get('m6_rail_len',float(spec['dev_d'])+2) > float(spec.get('m6_usable_depth',240)):
        raise ValueError('The rails are longer than the usable depth.')
    def numeric(value):
        if isinstance(value, list):
            if not value or len(value)>2048: raise ValueError('Section lists must have 1 to 2048 entries.')
            return [numeric(v) for v in value]
        if type(value) not in (int,float) or not math.isfinite(value) or abs(value)>1000:
            raise ValueError('Section settings need finite numeric coordinates within 1000 mm.')
        return value
    def polygon(p):
        if not isinstance(p,list) or not 3<=len(p)<=2048 or any(not isinstance(v,list) or len(v)!=2 for v in p):
            raise ValueError('Section outlines need at least three 2D points.')
        area=sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(p,p[1:]+p[:1]))
        if abs(area)<1e-7: raise ValueError('Section outline has zero area.')
    for key in KEYS[3:]:
        if key=='m6_edge_radius' or key not in spec: continue
        v=numeric(spec[key])
        if key in ('m6_rail_profiles','m6_side_windows'):
            if len(v)!=2: raise ValueError(key+' needs left and right outlines.')
            for p in v:
                if key=='m6_side_windows':
                    for loop in p:polygon(loop)
                else:polygon(p)
        elif key=='m6_stub_sections':
            if len(v)!=2: raise ValueError('Stub sections need two sides.')
            for side in v:
                if len(side)<2: raise ValueError('A loft needs at least two stations.')
                for i,(y,p) in enumerate(side):
                    polygon(p)
                    if len(p)!=len(side[0][1]) or (i and y<=side[i-1][0]):
                        raise ValueError('Loft stations must increase and have matching point counts.')
        elif key=='m6_retention_slot':
            if len(v)!=5 or v[2]<=0 or v[3]<=0 or v[4] not in (0,1):
                raise ValueError('Retention slot needs Y, Z, length, height, side (0/1).')
        elif key=='m6_light_pipes':
            if any(len(p)!=4 or p[2]<=0 or p[3]<=0 for p in v):
                raise ValueError('Light pipes need X, Z, diameter and depth.')
        elif key=='m6_vectors':
            for depth,loops in v:
                if not 0<depth<=1: raise ValueError('Vector inlays must be at most 1 mm deep.')
                for p in loops: polygon(p)
        elif key=='m6_nose_bridge':
            if len(v)!=2 or len(v[0])!=2 or v[0][0]>=v[0][1]:
                raise ValueError('Nose bridge needs increasing X limits and Y/Z outlines.')
            for p in v[1]:polygon(p)
        out[key]=v
    shape_keys=('m6_rail_profiles','m6_side_windows','m6_stub_sections')
    if any(k in out for k in shape_keys) and not all(k in out for k in shape_keys):
        raise ValueError('Measured rails need profiles, side outlines and stub sections together.')
    if any(k in out for k in ('m6_vectors','m6_light_pipes','m6_nose_bridge')) and 'm6_rail_profiles' not in out:
        raise ValueError('Colour parts need the measured rail profile adapter.')
    return out


def modules(s):
    """Create only extrusions, lofts, cylinders and vector inlays from saved numbers."""
    if not s.get('m6_rail_profiles'): return ''
    s=dict(s)
    for key,value in dict(m6_rail_len=float(s['dev_d'])+2,m6_bay_h=12,m6_bay_d=34,m6_edge_radius=0).items():
        s.setdefault(key,value)
    def lit(v): return json.dumps(v,separators=(',',':'))
    code='\n// Numeric section reconstruction; no imported meshes.\n'
    for k in KEYS:
        if k in s: code+=k+'='+lit(s[k])+';\n'
    code+=r'''
module mf_xz(p,y,d){translate([0,y+d,0])rotate([90,0,0])linear_extrude(d)polygon(p);}
module mf_side(p){rotate([90,0,90])linear_extrude(300,center=true)polygon(p);}
module mf_loft(sections){
 n=len(sections[0][1]); m=len(sections);
 polyhedron(points=[for(q=sections,p=q[1])[p[0],q[0],p[1]]],
 faces=concat([[for(j=[n-1:-1:0])j]],[[for(j=[0:n-1])(m-1)*n+j]],
 [for(i=[0:m-2],j=[0:n-1]) [i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n]],
 [for(i=[0:m-2],j=[0:n-1]) [i*n+j,(i+1)*n+(j+1)%n,(i+1)*n+j]]),convexity=20);
}
module mf_bridge(){q=m6_nose_bridge;
 difference(){translate([q[0][0],0,0])rotate([90,0,90])linear_extrude(q[0][1]-q[0][0])polygon(q[1][0]);
 if(len(q[1])>1)for(i=[1:len(q[1])-1])translate([q[0][0]-.01,0,0])rotate([90,0,90])linear_extrude(q[0][1]-q[0][0]+.02)polygon(q[1][i]);}}
module mf_stubs(){intersection(){union(){for(s=[0:1])mf_loft(m6_stub_sections[s]);if(!is_undef(m6_nose_bridge))mf_bridge();}
 translate([-126,-0.01,mr_start])cube([252,mr_stub+.01,mr_end-mr_start]);}}
module mf_slot(){q=m6_retention_slot; translate([0,q[0],q[1]])rotate([90,0,90])linear_extrude(300,center=true)
 hull(){for(y=[-(q[2]-q[3])/2,(q[2]-q[3])/2])translate([y,0])circle(d=q[3]);}}
module mf_access(p){
 ymin=min([for(q=p)q[0]]); ymax=max([for(q=p)q[0]]);
 zmin=min([for(q=p)q[1]]); zmax=max([for(q=p)q[1]]);
 bottom=zmin<22.225?2.6:44.45-2.6-m6_bay_h;
 translate([0,ymin,bottom])scale([1,m6_bay_d/(ymax-ymin),m6_bay_h/(zmax-zmin)])translate([0,-ymin,-zmin])mf_side(p);
}
module mf_rail(s){difference(){union(){intersection(){
 translate([0,12.05+m6_rail_len-.05,0])rotate([90,0,0])linear_extrude(m6_rail_len-.05)
 offset(r=m6_edge_radius)offset(delta=-m6_edge_radius)polygon(m6_rail_profiles[s]);
 difference(){mf_side(m6_side_windows[s][0]);for(i=[1:len(m6_side_windows[s])-1])
 if(i<=2)mf_access(m6_side_windows[s][i]);else mf_side(m6_side_windows[s][i]);}
 }
 // A full 2.5 mm horizontal skin under/over each access bay, including inner margins.
 xmin=min([for(p=m6_rail_profiles[s])p[0]]); xmax=max([for(p=m6_rail_profiles[s])p[0]]);
 for(z=[mr_start,mr_end-2.5])translate([xmin,16,z])cube([xmax-xmin,m6_bay_d,2.5]);
 }
 for(z=m6_joint_z)mr_yhole(m6_joint_x[s],z,6.6,11.9,4.3);
 if(!is_undef(m6_retention_slot)&&m6_retention_slot[4]==s)mf_slot();
 mr_id(s==0?"-L":"-R",m6_joint_x[s],72,90,3);
}}
module mf_vector(i,extra=0){q=m6_vectors[i];points=[for(l=q[1],p=l)p];
 lengths=[for(l=q[1])len(l)];
 function prefix(a,j)=j==0?0:a[j-1]+prefix(a,j-1);
 paths=[for(j=[0:len(lengths)-1])[for(k=[0:lengths[j]-1])prefix(lengths,j)+k]];
 translate([0,-4+q[0]+extra,0])rotate([90,0,0])linear_extrude(q[0]+extra)polygon(points,paths);
}
module mf_pipe(i){p=m6_light_pipes[i];mr_yhole(p[0],p[1],p[2],-4,p[3]);}
module mf_colours_cut(){
 if(!is_undef(m6_light_pipes))for(p=m6_light_pipes)mr_yhole(p[0],p[1],p[2],-4.01,p[3]+.02);
 if(!is_undef(m6_vectors))for(i=[0:len(m6_vectors)-1])mf_vector(i,.001);
}
'''
    return code
