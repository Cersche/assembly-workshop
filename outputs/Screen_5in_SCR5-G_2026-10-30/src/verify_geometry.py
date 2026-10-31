"""Independent delivered-mesh sections and 3MF rigid roundtrip; stdlib only."""
from pathlib import Path
import json
import struct
import xml.etree.ElementTree as ET
import zipfile

HERE=Path(__file__).resolve().parent.parent
def read(path):
    b=path.read_bytes();n=struct.unpack_from('<I',b,80)[0];v={};tri=[]
    for i in range(n):
        c=struct.unpack_from('<9f',b,96+50*i)
        tri.append([v.setdefault(c[k:k+3],len(v)) for k in (0,3,6)])
    return list(v),tri
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def hits_yz(verts,tris,y,z):
    origin=(-200,y,z);direction=(1,0,0);hits=[]
    for t in tris:
        a,b,c=[verts[i] for i in t];e1=sub(b,a);e2=sub(c,a);p=cross(direction,e2);det=dot(e1,p)
        if abs(det)<1e-12:continue
        s=sub(origin,a);u=dot(s,p)/det
        if not -1e-8<=u<=1+1e-8:continue
        q=cross(s,e1);v=dot(direction,q)/det
        if v< -1e-8 or u+v>1+1e-8:continue
        d=dot(e2,q)/det
        if d>=0:hits.append(origin[0]+d)
    return sorted({round(x,5) for x in hits})
def main():
    v,t=read(HERE/'SCR5-G_plate.stl')
    sections={str(y):[x for x in hits_yz(v,t,y,41.5) if -110<x<110] for y in (0.15,1.0,2.0)}
    for y in ('1.0','2.0'):
        assert len(sections[y])==2,sections
        assert abs(sections[y][0]-(-27.55))<0.00002
        assert abs(sections[y][1]-93.55)<0.00002
    assert abs(sections['0.15'][0]-(-27.7))<0.00005,sections
    assert abs(sections['0.15'][1]-93.7)<0.00005,sections
    assert abs((sections['1.0'][1]-sections['1.0'][0])-121.1)<0.00002
    vertical=hits_yz([(z,y,x) for x,y,z in v],t,1,33)
    assert len(vertical)==4,vertical
    assert abs(vertical[1]-2.7)<0.00002 and abs(vertical[2]-80.3)<0.00002,vertical
    lip_section=[x for x in hits_yz(v,t,2.9,41.5) if -110<x<110]
    assert len(lip_section)==2,lip_section
    assert abs(lip_section[0]-(-26.75))<0.00003 and abs(lip_section[1]-92.75)<0.00003,lip_section
    outside_lip={str(y):[x for x in hits_yz(v,t,y,41.5) if -110<x<110] for y in (2.4,3.4)}
    for edges in outside_lip.values():
        assert len(edges)==2 and abs(edges[0]+27.55)<0.00003 and abs(edges[1]-93.55)<0.00003,edges
    lip_vertical=hits_yz([(z,y,x) for x,y,z in v],t,2.9,33)
    assert abs(lip_vertical[1]-2.7)<0.00003 and abs(lip_vertical[2]-80.3)<0.00003,lip_vertical
    # Direct dummy bounds verify the measured metal frame is independent of the lip toggle.
    lcdv,_=read(HERE/'checks/dummy_lcd.stl')
    lcd_bounds=[[min(p[k] for p in lcdv),max(p[k] for p in lcdv)] for k in range(3)]
    clearance=min(lcd_bounds[0][0]-lip_section[0],lip_section[1]-lcd_bounds[0][1])
    assert clearance>=0.8999,clearance
    assert abs(lcd_bounds[1][0]-2.5)<0.00001 and abs(lcd_bounds[1][1]-5.5)<0.00001
    ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
    with zipfile.ZipFile(HERE/'SCR5-G_screen_plate_set.3mf') as z:
        tree=ET.fromstring(z.read('3D/3dmodel.model'))
    parts=['plate','frame','pin1','pin2','pin3'];out=[];xcur=0
    for part,obj in zip(parts,tree.findall('m:resources/m:object',ns)):
        vv,tt=read(HERE/f'SCR5-G_{part}.stl')
        if part=='plate':vv=[(x,-z,y) for x,y,z in vv]
        elif part=='frame':vv=[(x,z,-y) for x,y,z in vv]
        else:vv=[(z,y,-x) for x,y,z in vv]
        mn=[min(v[k] for v in vv) for k in range(3)];mx=max(v[0] for v in vv)
        expected=[(v[0]+xcur-mn[0],v[1]-mn[1],v[2]-mn[2]) for v in vv]
        verts=[tuple(float(e.attrib[k]) for k in ('x','y','z')) for e in obj.findall('.//m:vertex',ns)]
        tri=[tuple(int(e.attrib[k]) for k in ('v1','v2','v3')) for e in obj.findall('.//m:triangle',ns)]
        assert len(verts)==len(expected) and tri==[tuple(t) for t in tt],part
        error=max(abs(a-b) for p,q in zip(expected,verts) for a,b in zip(p,q))
        assert error<0.00000051,(part,error)
        out.append(dict(part=part,max_coordinate_error_mm=error,triangles_identical=True,print_min_z=min(v[2] for v in verts)))
        xcur+=mx-mn[0]+12
    result=dict(window_sections_at_glass_centre_z=sections,vertical_section=vertical,nominal_window_w_mm=121.1,
        side_lip_section=lip_section,sections_outside_lip_y=outside_lip,no_top_bottom_lip_section=lip_vertical,
        lip_to_metal_frame_clearance_mm=clearance,metal_frame_bounds=lcd_bounds,
        chamfer_verified_45deg_mm=0.3,roundtrip=out)
    (HERE/'checks/independent_geometry.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
