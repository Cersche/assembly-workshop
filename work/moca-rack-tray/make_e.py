"""Generates MRT-E.scad from MRT-D.scad: separate faceplate + tray, hidden M6 joint, channel jig and notch slice."""
import pathlib
s = pathlib.Path('MRT-D.scad').read_text(encoding='utf-8')
def rep(a, b):
    global s
    assert s.count(a) == 1, a
    s = s.replace(a, b)
rep(s.split('\n')[0], '// MRT-E (2026-11-04): MRT-D split into a separate faceplate and tray, joined by four hidden M6 screws, the tray seated on a 45 deg ledge. Channel layout unchanged. Shoes unchanged, still MRT-C-L / MRT-C-R.')
rep('// One piece: 1U faceplate + floor + side walls. Carries', '// Two pieces plus shoes: 1U faceplate, tray (floor + side walls). Carries')
rep('// z = 0 at the slot bottom. Prints floor down, no supports.', '// z = 0 at the slot bottom. Tray prints floor down, plate prints front face down, no supports.')
rep('// part: tray, shoe_left', '// part: plate, tray, jig, slice, shoe_left')
rep('id="MRT-D";', 'id="MRT-E";')
# channels become a module shared with the jig
a = s.index('    // jumper channel\n'); c = s.index('  }\n  // ScreenBeam foot pockets')
chan = s[a:c]
s = s[:a] + '    channels();\n' + s[c:]
rep('module tray(){difference(){', 'module channels(){\n' + chan + '}\n' + r'''// ---- Hidden M6 joint, dimensions from SG8-M6-B / coupon SG8-C1 (head recess and fit good, Brian 2026-10-28): 7.6 bore 7 deep in an 8 long boss,
// upright 6 thick with a 0.3 gap to the boss, 6.6 clearance, 11.5 x 3.5 head counterbore, 2.5 under the head: M6 x 8 reaches about 5.2 into the insert.
// Bosses 14 OD here (room allows, SG8 had 12). Near the plate ends, so the load goes side wall > upright > boss > corner rack screw. Insert and strength UNKNOWN.
tray_front=0.5; hs_d=14; hs_l=8; hs_bore=7.6; hs_bore_d=7; hs_gap=0.3; hs_t=6; hs_w=16; hs_web=2.5; hs_head=11.5; up_top=42; knee_y=34; fin_t=2; fin_y=34;
j_z=[11.5,33]; j_x=[tx0+side_t+8,tx1-side_t-8];
// Ledge on the plate back, the tray's underside chamfer sits on it. Stops short of the Velcro slots.
ledge_h=3; ledge_c=2.525; ledge_segs=[[5,89],[111,149],[171,215]];
module plate(){difference(){union(){
    translate([110,0,0])along(-plate_t,0)plate2d();
    for(x=j_x,z=j_z)translate([x,-0.01,z])rotate([-90,0,0])cylinder(d=hs_d,h=hs_l+0.01);
    for(g=ledge_segs)translate([g[0],0,0])rotate([90,0,90])linear_extrude(g[1]-g[0])polygon([[-0.01,0.025],[ledge_h,0.025],[-0.01,ledge_h+0.025]]);
  }
  for(x=j_x,z=j_z)translate([x,hs_l-hs_bore_d,z])rotate([-90,0,0])cylinder(d=hs_bore,h=hs_bore_d+1);
  translate([110,-0.6,33])rotate([90,0,180])mirror([1,0,0])linear_extrude(1)text("MRT-E-P",size=5,font="Liberation Sans:style=Bold",halign="center",valign="center");
}}
module upright(s){ // s=0 left, s=1 right; built on the left and mirrored
  mir(s){
    x0=tx0+side_t-0.01; yu=hs_l+hs_gap;
    difference(){
      translate([x0,yu,fl_z])cube([hs_w+0.01,hs_t,up_top-fl_z]);
      for(z=j_z){translate([j_x[0],yu-1,z])rotate([-90,0,0])cylinder(d=m6_clear,h=hs_t+2);
        translate([j_x[0],yu+hs_web,z])rotate([-90,0,0])cylinder(d=hs_head,h=hs_t);}
    }
    // side wall raised up to the upright
    translate([tx0,0,0])rotate([90,0,90])linear_extrude(side_t)polygon([[tray_front,wall_top-0.01],[knee_y,wall_top-0.01],[yu+hs_t,up_top],[tray_front,up_top]]);
    // fin behind the upright's inner edge, closes the box with the side wall; driver room stays between them
    translate([x0+hs_w-fin_t,0,0])rotate([90,0,90])linear_extrude(fin_t)polygon([[yu+hs_t-0.01,fl_z],[fin_y,fl_z],[yu+hs_t-0.01,up_top]]);
  }
}
module tray(){difference(){''')
rep("""    // plate, with the rack holes; tray parts run behind it
    translate([110,0,0])along(-plate_t,0)plate2d();
""", '')
rep('    for(m=[0,1])mir(m)rear_wall();\n', '    for(m=[0,1]){mir(m)rear_wall();upright(m);}\n')
rep('  // ScreenBeam foot pockets\n', """  // front edge stands off the plate, underside chamfered onto the plate's ledge
  translate([tx0-1,-5,-1])cube([tx1-tx0+2,5+tray_front,up_top+2]);
  translate([tx0-1,0,0])rotate([90,0,90])linear_extrude(tx1-tx0+2)polygon([[-1,-1],[ledge_c+2,-1],[-1,ledge_c+2]]);
  // room for the bosses
  for(x=j_x,z=j_z)translate([x,-1,z])rotate([-90,0,0])cylinder(d=hs_d+1,h=hs_l+hs_gap+1);
  // ScreenBeam foot pockets
""")
rep('for(x=[sbx0+30,sbx0+90]){strap_slot(x,0.8);strap_slot(x,sby0+SB[1]+sb_clr/2+2.3);}', 'for(x=[sbx0+30,sbx0+90]){translate([x-9,-1,fl_z-1])cube([18,4.3,11]);strap_slot(x,sby0+SB[1]+sb_clr/2+2.3);}')
rep("for(x=[sbx0+30,sbx0+90])translate([x-9,0.8,fl_z-1])cube([18,sby0+SB[1]+sb_clr/2+2.3+2.5-0.8,1+groove_strap]);", "for(x=[sbx0+30,sbx0+90])translate([x-9,-1,fl_z-1])cube([18,sby0+SB[1]+sb_clr/2+2.3+2.5+1,1+groove_strap]);")
rep('// ---- Context models\n', r'''// ---- MRT-T1 channel forming jig: the tray's channels, rib, ScreenBeam foot pockets and splitter riser in their exact places, on a thin open floor.
// Same heights above the floor as the tray. Set the real gear on it, form the coax and cut the jumpers. Floor is 2 thick, lowered 2 so it sits on the bed.
jf=2;
module sector2d(c,a0,da,r0,r1){n=24;translate(c)polygon(concat([for(i=[0:n])let(a=a0+da*i/n)[r1*cos(a),r1*sin(a)]],[for(i=[n:-1:0])let(a=a0+da*i/n)[r0*cos(a),r0*sin(a)]]));}
module jig_floor2d(){ w=chan/2+wall_t;
  sector2d(c_jump,0,90,R-w,R+w); sector2d(c_out2,-90,90,R-w,R+w); sector2d(c_in,180,90,R-w,R+w);
  translate([c_jump[0]-34,c_jump[1]+R-w])square([34.01,2*w]);       // jumper straight
  translate([c_out2[0]+R-w,c_out2[1]-0.01])square([2*w,bar_y1-c_out2[1]]);  // OUT straight
  translate([c_in[0]-R-w,c_in[1]-0.01])square([2*w,bar_y1-c_in[1]]);        // IN straight
  translate([tx0,70])square([split_wall-tx0,bar_y1-70]);            // cords
  translate([tx0,bar_y0])square([tx1-tx0,bar_y1-bar_y0]);           // under the rib
  translate([xc-24,y0-11])square([48,sp_l+22]);                      // splitter
  // ScreenBeam frame
  for(y=[3,sby0+SB[1]-1.5])translate([sbx0+10,y])square([SB[0]-20,5.5]);
  for(x=[sbx0+16-4,sbx0+104-4])translate([x,3])square([8,70]);
  for(f=sb_feet)translate(f)circle(d=22);
  // ties between the groups
  translate([tx0,70])square([sbx0+24-tx0,8]);                       // frame to cords
  translate([sbx0+100,73])square([8,c_jump[1]+R-73]);               // frame to jumper
  translate([xc+20,c_jump[1]+R-4])square([c_jump[0]-34-xc-20+0.01,8]); // splitter to jumper
  translate([c_in[0]-2,in_y-5])square([xc-24-c_in[0]+2.01,10]);     // splitter to IN
  translate([xc+20,out2_y-5])square([c_out2[0]-xc-20+2,10]);        // splitter to OUT
  translate([xc-8,y0+sp_l+10])square([16,c_in[1]+36-y0-sp_l-10]);     // splitter to the ID patch
  translate([c_in[0]-R,c_in[1]+30])square([c_out2[0]+2*R-c_in[0],10]); // cross tie, carries the ID
  translate([xc-8,c_in[1]+30])square([16,bar_y0-c_in[1]-29.99]);    // to the rib
}
module jig(){translate([0,0,-(fl_top-jf)])difference(){
  union(){
    translate([0,0,fl_top-jf])linear_extrude(jf)jig_floor2d();
    channels(); rear_rib();
    translate([tx0,70,fl_top-0.01])cube([side_t,bar_y1-70,wall_top-fl_top+0.01]);
    for(f=sb_feet)translate([f[0],f[1],fl_top-0.01])cylinder(d=22,h=pad+0.01);
    for(y=[sby0-sb_clr/2-2,sby0+SB[1]+sb_clr/2])translate([sbx0+15,y,fl_top-0.01])cube([SB[0]-30,2,pad+6]);
    translate([xc-sp_w/2+2,y0+2,fl_top-0.01])cube([sp_w-4,sp_l-4,riser+0.01]);
    for(e=ears)translate([e[0],e[1],fl_top-0.01])cylinder(d=boss_d,h=riser+0.01);
  }
  for(f=sb_feet)translate([f[0],f[1],case_z-foot_dp])cylinder(d=foot_d,h=foot_dp+pad);
  for(e=ears)translate([e[0],e[1],sp_z-ins_dp])cylinder(d=ins_d,h=ins_dp+1);
  translate([xc,c_in[1]+35,fl_top-0.6])linear_extrude(1)text("MRT-T1",size=6,font="Liberation Sans:style=Bold",halign="center",valign="center");
}}
// ---- MRT-T2 notch slice: three short channels ending in a rib notch, lip gaps 6.4 / 6.8 (the tray's) / 7.4. Same channel, wall, lip and rib sizes as the tray.
sl_l=34; sl_gaps=[6.4,6.8,7.4]; sl_pitch=chan+wall_t;
module slice(){translate([0,0,-(fl_top-jf)])difference(){
  union(){
    translate([0,0,fl_top-jf])cube([3*sl_pitch+wall_t,sl_l,jf]);
    for(i=[0:3])translate([i*sl_pitch,0,fl_top-0.01])cube([wall_t,sl_l,wall_top-fl_top+0.01]);
    for(i=[0:2]){f=i*sl_pitch+wall_t; p=chan-sl_gaps[i];
      lip_y(f,1,p,4,14);   // wall lip, as in the tray
      // rib lip at the rear, same height as the tray's rib
      translate([0,sl_l,0])rotate([90,0,0])linear_extrude(4)polygon([[f-0.4,lip_u],[f,lip_u],[f+p,lip_u+p],[f+p,rib_top],[f-0.4,rib_top]]);
    }
  }
  for(i=[0:2])translate([i*sl_pitch+wall_t+chan/2,22,fl_top-0.6])linear_extrude(1)text(str(sl_gaps[i]),size=4,font="Liberation Sans:style=Bold",halign="center",valign="center");
  translate([(3*sl_pitch+wall_t)/2,0.6,5.5+fl_top])rotate([90,0,0])linear_extrude(1)text("MRT-T2",size=4,font="Liberation Sans:style=Bold",halign="center",valign="center");
}}
// ---- Context models
''')
rep('if(part=="tray")tray();', 'if(part=="plate")plate();\nif(part=="tray")tray();\nif(part=="jig")jig();\nif(part=="slice")slice();')
rep("// right-angle F on the ScreenBeam (Brian's reach and tip numbers)", '// right-angle F on the ScreenBeam. Span from port face to outer face 24.6 confirmed by Brian 2026-11-04; barrel tip 38.2 from porch16, not confirmed here')
pathlib.Path('MRT-E.scad').write_text(s, encoding='utf-8')
