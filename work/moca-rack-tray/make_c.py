import pathlib
s=pathlib.Path('MRT-B.scad').read_text(encoding='utf-8')
def rep(a,b,n=1):
    global s
    assert s.count(a)>=1 and (n==0 or s.count(a)==n),a
    s=s.replace(a,b)
rep(s[:s.index('\n')],'// MRT-C (2026-11-04): MRT-B with the rear braces replaced (Brian picked option A): the tray side walls reach back to small shoes on the rear posts.')
rep('// part: tray, brace_left, brace_right, screenbeam, splitter, cables','// part: tray, shoe_left, shoe_right, screenbeam, splitter, cables')
rep('id="MRT-B";','id="MRT-C";')
rep('rp=9.7; lp=21.3;','rp=11; lp=24;')
rep('depth+25','245',0)
i=s.index('// ---- Rear braces.');j=s.index('module tray(){difference(){')
s=s[:i]+'''// ---- Rear support. The side walls run on to Y 220 and tie across with a low bar the cables pass over. Each wall tip has a 45 deg underside and
// seats on the ramp of a shoe bolted to the back of the rear post (2 M6 x 8, existing corner inserts, as the OptiPlex rear channels).
// No screw at the tip, so the plate alone sets the tray front to back. Vertical ear slots give +-1: tray home, raise the shoe until the tip just sits, tighten.
rack_depth=240; x_mid=110; ext_y0=166; wy=208; tip=220; bar_y0=198; bar_y1=206; flange_w=5.5;
seat_gap=0.15; side_gap=0.4; cap_gap=0.4; top_rise=2.5;
b_z0=1.1; b_z1=43.35; ear_t=4; ear_out=126; ear_slot=1; m6_clear=6.6;
s_x0=-0.9; s_x1=3.9; s_chk=tx0-side_gap; s_y0=wy-1; s_block=tip+1; cap_y0=212; chk_top=31;
function ramp_z(y)=y-wy+fl_z-seat_gap;
function cap_z(x)=wall_top+(x-tx0)+cap_gap;
module mir(m){if(m==1)translate([2*x_mid,0,0])mirror([1,0,0])children();else children();}
module rear_wall(){
  // wall carried on, underside rising at 45 deg over the last 12
  translate([tx0,0,0])rotate([90,0,90])linear_extrude(side_t)polygon([[ext_y0,fl_z],[wy,fl_z],[tip,tip-wy+fl_z],[tip,wall_top],[ext_y0,wall_top]]);
  // sloped top at the tip, the hold-down bears on it
  translate([0,tip,0])rotate([90,0,0])linear_extrude(tip-bar_y1)polygon([[tx0,wall_top-0.01],[tx0+side_t,wall_top-0.01],[tx0+side_t,wall_top+top_rise],[tx0,wall_top]]);
  // floor flange along the wall
  translate([tx0+side_t-0.01,ext_y0,fl_z])cube([flange_w,bar_y1-ext_y0,fl_top-fl_z]);
}
module shoe(tag){difference(){union(){
  translate([s_x0,s_block,b_z0])cube([s_x1-s_x0,rack_depth+ear_t-s_block,b_z1-b_z0]);
  translate([x_mid,rack_depth+ear_t,0])rotate([90,0,0])linear_extrude(ear_t)hull(){
    for(z=[b_z0+plate_r,b_z1-plate_r])translate([-ear_out+plate_r,z])circle(r=plate_r);
    translate([s_x0-x_mid,b_z0])square([0.01,b_z1-b_z0]);}
  // cheek outside the wall, lead-in at its front
  translate([0,0,b_z0])linear_extrude(chk_top-b_z0)polygon([[s_x0,s_y0],[s_chk-0.8,s_y0],[s_chk,s_y0+2],[s_chk,s_block+0.01],[s_x0,s_block+0.01]]);
  // ramp under the tip
  translate([s_chk-0.01,0,0])rotate([90,0,90])linear_extrude(s_x1-s_chk+0.01)polygon([[wy+b_z0-fl_z+seat_gap,b_z0],[s_block+0.01,ramp_z(s_block+0.01)],[s_block+0.01,b_z0]]);
  // hold-down over the tip, 45 deg underside
  translate([0,s_block+0.01,0])rotate([90,0,0])linear_extrude(s_block+0.01-cap_y0)polygon([[s_chk-0.01,cap_z(s_chk)],[s_x1,cap_z(s_x1)],[s_x1,chk_top],[s_chk-0.01,chk_top]]);
 }
 for(dz=[-hole_dz,hole_dz])translate([x_mid-hole_x,rack_depth-1,rack_pitch/2+dz])rotate([-90,0,0])hull()for(k=[-1,1])translate([0,k*ear_slot,0])cylinder(d=m6_clear,h=ear_t+2);
 translate([x_mid-hole_x,rack_depth+ear_t-0.6,rack_pitch/2])rotate([90,0,180])rotate([0,0,90])linear_extrude(1)text(tag,size=3,font="Liberation Sans:style=Bold",halign="center",valign="center");
}}
'''+s[j:]
rep('    for(m=[0,1])mir(m)tail();\n','    for(m=[0,1])mir(m)rear_wall();\n    translate([tx0,bar_y0,fl_z])cube([tx1-tx0,bar_y1-bar_y0,fl_top-fl_z]);\n')
rep('  // floor windows\n','''  // tie slots in the rear bar for the cords and both coax runs
  for(x=[11,c_in[0]-R,c_out2[0]+R]){tie([x,(bar_y0+bar_y1)/2],90,5.5);tie_groove([x,(bar_y0+bar_y1)/2],90,5.5);}
  // floor windows\n''')
rep('if(part=="brace_left")brace("MRT-B-L");\nif(part=="brace_right")mir(1)brace("MRT-B-R");','if(part=="shoe_left")shoe("MRT-C-L");\nif(part=="shoe_right")mir(1)shoe("MRT-C-R");')
pathlib.Path('MRT-C.scad').write_text(s,encoding='utf-8')
for a,b in (('check_b.py','check_c.py'),('clash_b.py','clash_c.py')):
    t=pathlib.Path(a).read_text(encoding='utf-8').replace('MRT-B','MRT-C').replace('brace_left','shoe_left').replace('brace_right','shoe_right').replace('brace(','shoe(').replace('brace L','shoe L').replace('brace R','shoe R')
    if a=='clash_b.py':
        t=t.replace("    ('tray x shoe L', S['tray'], S['bl']),","    ('CONTROL tray 1 high x shoe L (must overlap)', T('[0,0,1]', 'tray'), S['bl']),\n    ('CONTROL tray 1 outward x shoe L (must overlap)', T('[-1,0,0]', 'tray'), S['bl']),\n    ('tray x shoe L', S['tray'], S['bl']),")
        t=t.replace("('tray 0.1 high x shoe L', T('[0,0,0.1]', 'tray'), S['bl']),","('tray 0.3 high x shoe L', T('[0,0,0.3]', 'tray'), S['bl']),")
    pathlib.Path(b).write_text(t,encoding='utf-8')
