import re,pathlib
s=pathlib.Path('MRT-A.scad').read_text(encoding='utf-8')
def rep(a,b):
    global s
    assert s.count(a)==1,a
    s=s.replace(a,b)
rep('// MRT-A (2026-11-04): MoCA rack tray mock-up, layout A with walled cable channels and built-in cable retention.',
    '// MRT-B (2026-11-04): MRT-A plus two rear braces on the back of the rear posts (Brian). Floor moved down to the plate bottom so it prints flat on the bed.')
rep('// part: tray, screenbeam, splitter, cables, clash_devices, clash_cables','// part: tray, brace_left, brace_right, screenbeam, splitter, cables')
rep('id="MRT-A";','id="MRT-B";')
rep('fl_z=2; fl_top=5;','fl_z=0.025; fl_top=4;')
# LAN and power move inward of the tail and ramp
rep('rp=11; lp=24;','rp=9.7; lp=21.3;')
# under-floor grooves and tail
rep('  // ID on the floor top','''  // Grooves under the floor: ties and straps pass under without reaching the slot below
  tie_groove(on_arc(c_jump,28),28+90,3.5); tie_groove(on_arc(c_out2,-38),-38+90,3.5); tie_groove(on_arc(c_in,206),206+90,3.5);
  tie_groove([(tx0+side_t+split_wall-wall_t)/2,100],90,5.5); tie_groove([(tx0+side_t+split_wall-wall_t)/2,138],90,5.5);
  for(x=[sbx0+30,sbx0+90])translate([x-9,0.8,fl_z-1])cube([18,sby0+SB[1]+sb_clr/2+2.3+2.5-0.8,1+groove_strap]);
  // ID on the floor top''')
rep('module strap_slot(x,y)','''groove_tie=1.6; groove_strap=2;
module tie_groove(p,ang,half){translate([p[0],p[1],fl_z-1])rotate(ang)linear_extrude(1+groove_tie)offset(r=0.9)square([3.4,2*half],center=true);}
module strap_slot(x,y)''')
rep('    // ScreenBeam: foot pads and long-side fences','    for(m=[0,1])mir(m)tail();\n    // ScreenBeam: foot pads and long-side fences')
# tail + brace modules
rep('module tray(){difference(){','''// ---- Rear braces. Each bolts to the back of a rear post with 2 M6 x 8 (existing corner inserts), as the OptiPlex rear channels.
// The tray's rear corners carry a tail with a 45 deg underside; pushing the tray home seats it on the brace ramp. No screw at this
// joint, so the tray is fixed front to back only by the plate and can't be over-constrained by print length.
// Vertical ear slots give +-1 height adjustment: tray home, raise brace until the tail just sits on the ramp, tighten.
rack_depth=240; x_mid=110; flange_u=111.12;
tail_x0=4; tail_x1=7; tail_y0=160; tail_end=188; tail_top=24; tail_rise=3;
seat_gap=0.15; side_gap=0.4; web_x0=-0.9; web_x1=tail_x0-side_gap;   // web passes the 222.24 post opening with 0.22 a side
b_z0=1.1; b_z1=43.35; ear_t=4; ear_out=126; ear_slot=1; m6_clear=6.6; ramp_x1=tail_x1+0.4;
br_y0=tray_end_y+0.5;
cap_y0=tray_end_y+4; cap_y1=tail_end+4; cap_gap=0.4;
module mir(m){if(m==1)translate([2*x_mid,0,0])mirror([1,0,0])children();else children();}
module tail(){difference(){
  translate([0,tail_end,0])rotate([90,0,0])linear_extrude(tail_end-tail_y0)
    polygon([[tx0+side_t-0.01,fl_z],[tail_x1,fl_z],[tail_x1,tail_top+tail_rise],[tail_x0,tail_top],[tx0+side_t-0.01,tail_top]]);
  // 45 deg underside rising to the rear
  translate([tail_x0-5,0,0])rotate([90,0,90])linear_extrude(tail_x1-tail_x0+10)
    polygon([[tray_end_y,fl_z-0.01],[tail_end+1,fl_z-0.01],[tail_end+1,tail_end+1-tray_end_y+fl_z]]);
}}
module brace(tag){difference(){union(){
  // web, passes the post opening
  translate([web_x0,br_y0,b_z0])cube([web_x1-web_x0,rack_depth+ear_t-br_y0,b_z1-b_z0]);
  // ramp under the tail, one block up from the bed
  translate([web_x1-0.01,0,0])rotate([90,0,90])linear_extrude(ramp_x1-web_x1+0.01)
    polygon([[br_y0+b_z0-fl_z-seat_gap+0.5,b_z0],[tail_end+2,tail_end+2-tray_end_y+fl_z-seat_gap],[tail_end+6,tail_end+2-tray_end_y+fl_z-seat_gap],[tail_end+6+(tail_end+2-tray_end_y+fl_z-seat_gap-b_z0),b_z0]]);
  // hold-down cap over the tail, 45 deg underside matches the tail's sloped top
  translate([0,cap_y1,0])rotate([90,0,0])linear_extrude(cap_y1-cap_y0)
    polygon([[web_x1-0.01,tail_top-(tail_x0-web_x1)*tail_rise/(tail_x1-tail_x0)+cap_gap],[ramp_x1,tail_top+tail_rise+(ramp_x1-tail_x1)+cap_gap],[ramp_x1,b_z1],[web_x1-0.01,b_z1]]);
  // ear on the back of the post
  translate([x_mid,rack_depth+ear_t,0])rotate([90,0,0])linear_extrude(ear_t)intersection(){
    translate([-ear_out,b_z0])square([ear_out+web_x1-x_mid,b_z1-b_z0]);
    hull()for(z=[b_z0+plate_r,b_z1-plate_r])translate([-ear_out+plate_r,z])circle(r=plate_r);
    // keeps the inner end square
  }
  translate([x_mid-ear_out+plate_r,rack_depth,b_z0])cube([web_x1-x_mid+ear_out-plate_r,ear_t,b_z1-b_z0]);
 }
 // M6 clearance slots, vertical
 for(dz=[-hole_dz,hole_dz])translate([x_mid-hole_x,rack_depth-1,rack_pitch/2+dz])rotate([-90,0,0])hull()for(k=[-1,1])translate([0,k*ear_slot,0])cylinder(d=m6_clear,h=ear_t+2);
 // lightening diamond in the web
 translate([web_x0-1,0,0])rotate([90,0,90])linear_extrude(web_x1-web_x0+2)polygon([[212,rack_pitch/2-15],[227,rack_pitch/2],[212,rack_pitch/2+15],[197,rack_pitch/2]]);
 // ID on the ear's rear face, between the slots
 translate([x_mid-hole_x,rack_depth+ear_t+0.01,rack_pitch/2])rotate([90,0,180])translate([0,0,0])rotate([0,0,90])linear_extrude(0.61)text(tag,size=3,font="Liberation Sans:style=Bold",halign="center",valign="center");
}}
module tray(){difference(){''')
rep('tx0=1; tx1=219; depth=172;','tx0=1; tx1=219; depth=172; tray_end_y=172;')
rep('if(part=="tray")tray();','if(part=="tray")tray();\nif(part=="brace_left")brace("MRT-B-L");\nif(part=="brace_right")mir(1)brace("MRT-B-R");')
pathlib.Path('MRT-B.scad').write_text(s,encoding='utf-8')
