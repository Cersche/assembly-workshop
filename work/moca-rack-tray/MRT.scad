// MoCA rack tray, working draft (one file from 2026-11-05; replaces the MRT-B..F make_*.py chain).
// Geometry is MRT-F (2026-11-04), now built on lib/workshop.scad: plate outline and slots, the hidden M6 joint and the insert bores
// come from the shared library. Part IDs are unchanged (tray MRT-F, plate MRT-E-P, covers MRT-F-C1..C3, shoes MRT-C-L/R) because the
// geometry is unchanged; a release gets the next free ID. PROPOSED, MOCK-UP, UNPRINTED. Fit, heat, retention and strength are UNKNOWN.
// Frame: rack frame, as lib/workshop.scad and tools/rack_posts.py: X centred, Y = 0 plate back (front face of the front posts), + to the rear,
// Z = 0 slot bottom. Modules are written in the old x = 0..220 frame and shifted by -x_mid at the end. Tray prints floor down, plate front face down.
// part: plate, tray, cover_j, cover_o, cover_i, jig, slice, shoe_left, shoe_right, screenbeam, splitter, cables, keepout (check only), cuts (check only)
part="tray";
id="MRT-G";
$fn=64;
include <workshop.scad>

// ---- Faceplate: project standard (44.4/U, 252 wide, 4 thick, R2.5, four-corner slots)
u=1; rack_pitch=ws_pitch; plate_t=ws_plate_t; plate_r=ws_plate_r; hole_x=ws_hole_x; hole_dz=ws_hole_dz;

// ---- Tray. Post flange inner faces are at rack X +-111.12 (4U post mesh), so 218 wide leaves 2.12 a side.
tx0=1; tx1=219; depth=172; tray_end_y=172; fl_z=0.025; fl_top=4; side_t=2.5; wall_top=24; wall_t=2; chan=10;
// ---- Retention lips: 45 deg underside, so they print without supports. The cable presses past from above.
lip_p=3.2; lip_pl=4.5;
// Coax lips get a 60 deg lead-in on top (Brian, MRT-T1 2026-11-06: the flat top took enough force to nearly damage the coax).
// Gap 6.8 and the 45 deg underside are kept as printed. The cord lips (lip_pl) are unchanged.
lip_lead=5.5;

// ---- ScreenBeam (Brian): 120 x 65 x 30 incl. feet; feet 2.25 proud, pockets as the receiver cradle. Coax end at the right.
SB=[120,65,30]; foot_h=2.25; foot_d=16; foot_dp=2.6; pad=2; sb_clr=0.5;
sbx0=70; sby0=6; case_z=fl_top+pad;
sb_feet=[for(x=[16,104],y=[8.5,56.5])[sbx0+x,sby0+y]];
coax_p=[sbx0+SB[0],sby0+SB[1]-22,case_z+15.25];
port_z=case_z+(SB[2]-foot_h)/2; lan_y=sby0+24; pwr_y=sby0+43;
lan_end=32; pwr_end=25;     // ASSUMED plug ends: LAN 38 long, power 45 long

// ---- Splitter (Brian's calipers, porch16.scad). Back face up on a 5.5 riser, IN to -x, OUTs to +x.
sp_l=38.75; sp_w=23; sp_base=7.5; sp_h=15.9; sp_axis=7.5; sp_out=22; sp_in_end=18.5; sp_port=13; sp_port_d=9.5;
sp_ear_l=48.5; sp_ear_s=14; sp_ear_hole=5; sp_ear_d=10; sp_ear_t=9;
// Straight coax past each port (Brian, MRT-T1 with the real cable, 2026-11-06): crimp sleeve ends 33 from the body face (sp_a),
// and the cable only starts to curve 48 from it (sp_b). The splitter moved +19.5 (xc 95 -> 114.5) so the IN bend stays put.
sp_a=33; sp_b=48;
// Right-angle F on the ScreenBeam (Brian, 2026-11-06): crimp sleeve ends 44 behind the port centre line (ra_tip), the jumper starts to
// curve 58 behind it (ra_bend). OUT1 sits on the jumper's straight (bend R30), so the splitter moved back 19 with it (out1_y 118 -> 137).
ra_bend=58; out1_y=sby0+SB[1]-22+ra_bend+30;
riser=5.5; sp_z=fl_top+riser; xc=114.5; yc=out1_y+sp_out/2; y0=yc-sp_l/2; in_y=y0+sp_in_end; out2_y=out1_y+sp_out;
axis_z=sp_z+sp_axis; x_in=xc-sp_w/2; x_out=xc+sp_w/2;
ears=[[xc+sp_ear_s/2,yc+sp_ear_l/2],[xc-sp_ear_s/2,yc-sp_ear_l/2]];
ins_d=ws_insert_m3[0]; ins_dp=ws_insert_m3[1]; boss_d=9.5;   // M3 x 3 x 5 insert standard

// ---- Channel centrelines, all bends R30
R=30; ra_reach=18.6; ra_tip=44;
ra_x=coax_p[0]+ra_reach; ra_tip_y=coax_p[1]+ra_tip;
c_jump=[ra_x-R,coax_p[1]+ra_bend];            // jumper bend, angle 0..90; ends on y = out1_y
c_out2=[x_out+sp_b,out2_y+R];                 // modem OUT bend, angle -90..0, starts sp_b from the body
c_in=[x_in-sp_b,in_y+R];                      // coax IN bend, angle 180..270, starts sp_b from the body
jw0=x_out+sp_b;                               // jumper channel walls start here (were 38 from the body, lips over the crimp)
split_wall=c_in[0]-R-chan/2;                  // left channel inner face

module along(y0,y1){translate([0,y1,0])rotate([90,0,0])linear_extrude(height=y1-y0)children();}
module rr(x0,x1,y0,y1,r){translate([x0+r,y0+r])offset(r=r)square([x1-x0-2*r,y1-y0-2*r]);}

// ---- Curved walls: inner and outer wall of one channel bend
module arc_wall(c,a0,da){translate([c[0],c[1],fl_top-0.01])rotate(a0)rotate_extrude(angle=da){
  translate([R-chan/2-wall_t,0])square([wall_t,wall_top-fl_top+0.01]);
  translate([R+chan/2,0])square([wall_t,wall_top-fl_top+0.01]);
}}
module wall_x(y,x0,x1){translate([x0,y,fl_top-0.01])cube([x1-x0,wall_t,wall_top-fl_top+0.01]);}
module wall_y(x,y0,y1){translate([x,y0,fl_top-0.01])cube([wall_t,y1-y0,wall_top-fl_top+0.01]);}

// ---- Lips. d = +1 points toward +r (or +x/+y), d = -1 the other way; face = the wall face it grows from.
module lip_prof(face,d,p,lead=0){u=wall_top-p-0.5-lead;polygon([[face-d*0.4,u],[face,u],[face+d*p,u+p],[face+d*p,u+p+0.5],[face,wall_top],[face-d*0.4,wall_top]]);}
module arc_lip(c,a0,da,inner){translate([c[0],c[1],0])rotate(a0)rotate_extrude(angle=da)
  if(inner)lip_prof(R-chan/2,1,lip_p,lip_lead);else lip_prof(R+chan/2,-1,lip_p,lip_lead);}
module lip_y(face,d,p,y0,y1){translate([0,y1,0])rotate([90,0,0])linear_extrude(height=y1-y0)lip_prof(face,d,p);}
module lip_x(face,d,p,x0,x1){translate([x0,0,0])rotate([90,0,90])linear_extrude(height=x1-x0)lip_prof(face,d,p);}

// ---- Cable-tie slots: a pair across the channel; the tie goes down one, under the floor, up the other and around the cable.
module tie(p,ang,half){translate([p[0],p[1],fl_z-1])rotate(ang)for(s=[-1,1])translate([0,s*half,0])linear_extrude(fl_top-fl_z+1.5)
  offset(r=0.9)square([3.4,0.2],center=true);}
function on_arc(c,a)=[c[0]+R*cos(a),c[1]+R*sin(a)];

groove_tie=1.6; groove_strap=2;
module tie_groove(p,ang,half){translate([p[0],p[1],fl_z-1])rotate(ang)linear_extrude(1+groove_tie)offset(r=0.9)square([3.4,2*half],center=true);}
module strap_slot(x,y){translate([x-9,y,fl_z-1])cube([18,2.5,8.5]);}   // 16 mm Velcro, same as the rear cable lane

// ---- Rear support. The side walls run on to Y 220 and tie across with a low bar the cables pass over. Each wall tip has a 45 deg underside and
// seats on the ramp of a shoe bolted to the back of the rear post (2 M6 x 8, existing corner inserts, as the OptiPlex rear channels).
// No screw at the tip, so the plate alone sets the tray front to back. Vertical ear slots give +-1: tray home, raise the shoe until the tip just sits, tighten.
rack_depth=240; x_mid=110; ext_y0=166; wy=208; tip=220; bar_y0=198; bar_y1=206; flange_w=5.5;
seat_gap=0.15; side_gap=0.4; cap_gap=0.4; top_rise=2.5;
b_z0=1.1; b_z1=43.35; ear_t=4; ear_out=126; ear_slot=1; m6_clear=ws_m6_clear;
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
// ---- Rear rib: a stiff wall across the back. Each run sits in a notch and presses past a 45 deg lip, so the rib takes the cable's push, not a tie.
rib_y0=bar_y1-4; rib_top=22; lip_u=12.5;   // rib 18 -> 22 tall to fit the coax lead-in
module rib_lip(f,p,lead=0){translate([0,bar_y1,0])rotate([90,0,0])linear_extrude(bar_y1-rib_y0)polygon(lead>0?
  [[f-0.4,lip_u],[f,lip_u],[f+p,lip_u+p],[f+p,lip_u+p+0.5],[f,lip_u+p+0.5+lead],[f-0.4,lip_u+p+0.5+lead]]:
  [[f-0.4,lip_u],[f,lip_u],[f+p,lip_u+p],[f+p,rib_top],[f-0.4,rib_top]]);}
module rear_rib(){
  difference(){
    translate([tx0,rib_y0,fl_top-0.01])cube([tx1-tx0,bar_y1-rib_y0,rib_top-fl_top+0.01]);
    for(n=[[tx0+side_t,split_wall-wall_t],[c_in[0]-R-chan/2,c_in[0]-R+chan/2],[c_out2[0]+R-chan/2,c_out2[0]+R+chan/2]])
      translate([n[0],rib_y0-1,fl_top])cube([n[1]-n[0],bar_y1-rib_y0+2,rib_top]);
  }
  rib_lip(tx0+side_t,lip_pl); rib_lip(c_in[0]-R-chan/2,lip_p,lip_lead); rib_lip(c_out2[0]+R-chan/2,lip_p,lip_lead);
}
module channels(){
    // jumper channel
    arc_wall(c_jump,0,90);
    wall_x(c_jump[1]+R+chan/2,jw0,c_jump[0]+0.01);
    wall_x(c_jump[1]+R-chan/2-wall_t,jw0,c_jump[0]+0.01);
    // no lips on the jumper (Brian, 2026-11-06): it hangs between two ports above the floor; the connectors and cover C1 hold it
    // modem OUT channel
    arc_wall(c_out2,-90,90);
    wall_y(c_out2[0]+R-chan/2-wall_t,c_out2[1]-0.01,bar_y1);
    wall_y(c_out2[0]+R+chan/2,c_out2[1]-0.01,bar_y1);
    arc_lip(c_out2,-82,18,true); arc_lip(c_out2,-60,18,false); arc_lip(c_out2,-26,18,true);
    // coax IN channel
    arc_wall(c_in,180,90);
    wall_y(c_in[0]-R-chan/2-wall_t,c_in[1]-0.01,bar_y1);
    wall_y(c_in[0]-R+chan/2,c_in[1]-0.01,bar_y1);
    arc_lip(c_in,244,18,true); arc_lip(c_in,222,18,false); arc_lip(c_in,188,18,true);
    // power + LAN channel: long inner wall, tray side wall on the other side
    wall_y(split_wall-wall_t,70,c_in[1]);
    lip_y(tx0+side_t,1,lip_pl,82,92); lip_y(split_wall-wall_t,-1,lip_pl,102,112);
    lip_y(tx0+side_t,1,lip_pl,122,132); lip_y(split_wall-wall_t,-1,lip_pl,142,152);
}
// ---- Hidden M6 joint, dimensions from SG8-M6-B / coupon SG8-C1 (head recess and fit good, Brian 2026-10-28): 7.6 bore 7 deep in an 8 long boss,
// upright 6 thick with a 0.3 gap to the boss, 6.6 clearance, 11.5 x 3.5 head counterbore, 2.5 under the head: M6 x 8 reaches about 5.2 into the insert.
// Bosses 14 OD here (room allows, SG8 had 12). Near the plate ends, so the load goes side wall > upright > boss > corner rack screw. Insert and strength UNKNOWN.
tray_front=0.5; hs_d=14; hs_l=8; hs_bore=ws_insert_m6[0]; hs_bore_d=7; hs_gap=0.3; hs_t=6; hs_w=16; hs_web=ws_m6_web; hs_head=ws_m6_head_d; up_top=42; knee_y=34; fin_t=2; fin_y=34;
j_z=[11.5,33]; j_x=[tx0+side_t+8,tx1-side_t-8];
// Ledge on the plate back, the tray's underside chamfer sits on it. Stops short of the Velcro slots.
ledge_h=3; ledge_c=2.525; ledge_segs=[[5,89],[111,149],[171,215]];
module plate(){difference(){union(){
    translate([x_mid,0,0])rotate([90,0,0])linear_extrude(plate_t)ws_plate2d(u);
    for(x=j_x,z=j_z)translate([x_mid,0,0])ws_m6_plate_boss(x-x_mid,z,u,d=hs_d,h=hs_l);
    for(g=ledge_segs)translate([g[0],0,0])rotate([90,0,90])linear_extrude(g[1]-g[0])polygon([[-0.01,0.025],[ledge_h,0.025],[-0.01,ledge_h+0.025]]);
  }
  translate([110,-0.6,33])rotate([90,0,180])mirror([1,0,0])linear_extrude(1)text("MRT-E-P",size=5,font="Liberation Sans:style=Bold",halign="center",valign="center");
}}
module upright(s){ // s=0 left, s=1 right; built on the left and mirrored
  mir(s){
    x0=tx0+side_t-0.01; yu=hs_l+hs_gap;
    difference(){
      translate([x0,yu,fl_z])cube([hs_w+0.01,hs_t,up_top-fl_z]);
      for(z=j_z)ws_m6_screw_cut(j_x[0],yu,z,hs_t);
    }
    // side wall raised up to the upright
    translate([tx0,0,0])rotate([90,0,90])linear_extrude(side_t)polygon([[tray_front,wall_top-0.01],[knee_y,wall_top-0.01],[yu+hs_t,up_top],[tray_front,up_top]]);
    // fin behind the upright's inner edge, closes the box with the side wall; driver room stays between them
    translate([x0+hs_w-fin_t,0,0])rotate([90,0,90])linear_extrude(fin_t)polygon([[yu+hs_t-0.01,fl_z],[fin_y,fl_z],[yu+hs_t-0.01,up_top]]);
  }
}
// ---- Channel covers. M3 countersunk screw down through the cover into an M3 x 3 x 5 insert (4.2 bore, 4 deep) in a 9.5 pillar on the channel's outer wall face.
// Below the insert, a 3.4 clearance hole so a longer screw won't bottom out. Screw length on hand UNKNOWN. Fit, retention and strength UNKNOWN.
cov_t=3; cov_off=2.75; pil_d=9.5; cov_ear=11; csk_d=6.6; csk_h=1.8; screw_clear=3.4; relief=12;
ri=R-chan/2-wall_t-cov_off; ro=R+chan/2+wall_t+cov_off; cov_w=chan/2+wall_t;
function pol(c,a,r)=[c[0]+r*cos(a),c[1]+r*sin(a)];
cov_j=[pol(c_jump,12,ri),pol(c_jump,55,ro),[jw0,c_jump[1]+R-cov_w-cov_off]];
cov_o=[pol(c_out2,-80,ri),pol(c_out2,-40,ro),[c_out2[0]+R+cov_w+cov_off,196]];
cov_i=[[split_wall+cov_off,90],pol(c_in,240,ro),pol(c_in,255,ri),[c_in[0]-R+cov_w+cov_off,196]];
cov_all=concat(cov_j,cov_o,cov_i);
module sector2d(c,a0,da,r0,r1){n=48;translate(c)polygon(concat([for(i=[0:n])let(a=a0+da*i/n)[r1*cos(a),r1*sin(a)]],[for(i=[n:-1:0])let(a=a0+da*i/n)[r0*cos(a),r0*sin(a)]]));}
module cov2d(pts){offset(r=-2)offset(r=2)union(){children();for(p=pts)translate(p)circle(d=cov_ear);}}
module cov_solid(pts,tag,tp,ta){difference(){
  translate([0,0,wall_top])linear_extrude(cov_t)cov2d(pts)children();
  for(p=pts)translate([p[0],p[1],wall_top-1]){cylinder(d=screw_clear,h=cov_t+2);translate([0,0,1+cov_t-csk_h])cylinder(d1=screw_clear,d2=csk_d,h=csk_h+0.01);}
  translate([tp[0],tp[1],wall_top+cov_t-0.6])rotate(ta)linear_extrude(1)text(tag,size=4,font="Liberation Sans:style=Bold",halign="center",valign="center");
}}
module cover_j(){cov_solid(cov_j,"MRT-G-C1",pol(c_jump,45,R),-45){sector2d(c_jump,0,90,R-cov_w,R+cov_w);translate([jw0,c_jump[1]+R-cov_w])square([c_jump[0]-jw0+0.01,2*cov_w]);}}
module cover_o(){cov_solid(cov_o,"MRT-G-C2",[c_out2[0]+R,188],90){sector2d(c_out2,-90,90,R-cov_w,R+cov_w);translate([c_out2[0]+R-cov_w,c_out2[1]-0.01])square([2*cov_w,bar_y1-c_out2[1]]);}}
module cover_i(){cov_solid(cov_i,"MRT-G-C3",[11,130],90){sector2d(c_in,180,90,R-cov_w,R+cov_w);translate([c_in[0]-R-cov_w,c_in[1]-0.01])square([2*cov_w,bar_y1-c_in[1]]);translate([tx0,70])square([split_wall-tx0,bar_y1-70]);}}
module cov_pillars(z0){for(p=cov_all)translate([p[0],p[1],z0])cylinder(d=pil_d,h=wall_top-z0);}
module cov_bores(){for(p=cov_all)translate([p[0],p[1],0]){translate([0,0,wall_top-ins_dp])ws_insert_bore(ws_insert_m3,ins_dp+1);translate([0,0,wall_top-ins_dp-relief])cylinder(d=screw_clear,h=relief+0.01);}}
module tray(){difference(){
  union(){
    // floor
    translate([0,0,fl_z])linear_extrude(fl_top-fl_z)union(){rr(tx0,tx1,0,depth,4);translate([tx0,0])square([tx1-tx0,10]);}
    // side walls, tied into the plate by a chamfer
    for(x=[tx0,tx1-side_t])translate([x,0,fl_z])cube([side_t,depth-4,wall_top-fl_z]);
    for(s=[0,1])translate([s==0?tx0+side_t-0.01:tx1-side_t-6.01,0,fl_top-0.01])
      linear_extrude(wall_top-fl_top+0.01)polygon(s==0?[[0,0],[6,0],[0,6]]:[[0,0],[6,0],[6,6]]);
    // floor-to-plate chamfer across the width
    translate([tx0,0,0])rotate([90,0,90])linear_extrude(tx1-tx0)polygon([[-0.01,fl_top-0.01],[5,fl_top-0.01],[-0.01,fl_top+5]]);
    for(m=[0,1]){mir(m)rear_wall();upright(m);}
    translate([tx0,bar_y0,fl_z])cube([tx1-tx0,bar_y1-bar_y0,fl_top-fl_z]);
    // floor carried back under the cords, coax IN and coax OUT
    translate([tx0,depth-6,fl_z])cube([c_in[0]-R+chan/2+wall_t-tx0,bar_y0-depth+6.01,fl_top-fl_z]);
    translate([c_out2[0],depth-6,fl_z])cube([tx1-side_t-c_out2[0]+0.01,bar_y0-depth+6.01,fl_top-fl_z]);   // under the OUT2 bend too
    rear_rib();
    // ScreenBeam: foot pads and long-side fences
    for(f=sb_feet)translate([f[0],f[1],fl_top-0.01])cylinder(d=22,h=pad+0.01);
    for(y=[sby0-sb_clr/2-2,sby0+SB[1]+sb_clr/2])translate([sbx0+15,y,fl_top-0.01])cube([SB[0]-30,2,pad+6]);
    // splitter riser and ear bosses
    translate([xc-sp_w/2+2,y0+2,fl_top-0.01])cube([sp_w-4,sp_l-4,riser+0.01]);
    for(e=ears)translate([e[0],e[1],fl_top-0.01])cylinder(d=boss_d,h=riser+0.01);
    channels();
    cov_pillars(fl_z);
  }
  // front edge stands off the plate, underside chamfered onto the plate's ledge
  translate([tx0-1,-5,-1])cube([tx1-tx0+2,5+tray_front,up_top+2]);
  translate([tx0-1,0,0])rotate([90,0,90])linear_extrude(tx1-tx0+2)polygon([[-1,-1],[ledge_c+2,-1],[-1,ledge_c+2]]);
  // room for the bosses
  for(x=j_x,z=j_z)translate([x,-1,z])rotate([-90,0,0])cylinder(d=hs_d+1,h=hs_l+hs_gap+1);
  cov_bores();
  // ScreenBeam foot pockets
  for(f=sb_feet)translate([f[0],f[1],case_z-foot_dp])cylinder(d=foot_d,h=foot_dp+pad);
  // Velcro strap slots around the ScreenBeam
  for(x=[sbx0+30,sbx0+90]){translate([x-9,-1,fl_z-1])cube([18,4.3,11]);strap_slot(x,sby0+SB[1]+sb_clr/2+2.3);}
  // insert bores in the splitter bosses
  for(e=ears)translate([e[0],e[1],sp_z-ins_dp])ws_insert_bore(ws_insert_m3,ins_dp+1);
  // cable-tie slots
  tie(on_arc(c_jump,28),28+90,3.5); tie(on_arc(c_out2,-38),-38+90,3.5); tie(on_arc(c_in,206),206+90,3.5);
  tie([(tx0+side_t+split_wall-wall_t)/2,100],90,5.5); tie([(tx0+side_t+split_wall-wall_t)/2,138],90,5.5);
  // tie slots in the floor behind the tray, inside each channel
  for(t=[[(tx0+side_t+split_wall-wall_t)/2,5.5],[c_in[0]-R,3.5],[c_out2[0]+R,3.5]]){tie([t[0],186],90,t[1]);tie_groove([t[0],186],90,t[1]);}
  // floor windows
  translate([0,0,fl_z-1])linear_extrude(fl_top-fl_z+1.01){
    rr(sbx0+30,sbx0+90,sby0+13,sby0+52,6);
    rr(32,sbx0+60,78,99,6);
    rr(134,166,104,128,6);
  }
  // Grooves under the floor: ties and straps pass under without reaching the slot below
  tie_groove(on_arc(c_jump,28),28+90,3.5); tie_groove(on_arc(c_out2,-38),-38+90,3.5); tie_groove(on_arc(c_in,206),206+90,3.5);
  tie_groove([(tx0+side_t+split_wall-wall_t)/2,100],90,5.5); tie_groove([(tx0+side_t+split_wall-wall_t)/2,138],90,5.5);
  for(x=[sbx0+30,sbx0+90])translate([x-9,-1,fl_z-1])cube([18,sby0+SB[1]+sb_clr/2+2.3+2.5+1,1+groove_strap]);
  // ID on the floor top, open area left of the splitter
  translate([66,136,fl_top-0.6])linear_extrude(1)text(id,size=5,font="Liberation Sans:style=Bold",halign="center",valign="center");
}}

// ---- MRT-T3 channel forming jig (MRT-T1 plus the cover pillars): the tray's channels, rib, ScreenBeam foot pockets and splitter riser in their exact places, on a thin open floor.
// Same heights above the floor as the tray. Set the real gear on it, form the coax and cut the jumpers. Floor is 2 thick, lowered 2 so it sits on the bed.
jf=2;
module sector2d_old(c,a0,da,r0,r1){n=24;translate(c)polygon(concat([for(i=[0:n])let(a=a0+da*i/n)[r1*cos(a),r1*sin(a)]],[for(i=[n:-1:0])let(a=a0+da*i/n)[r0*cos(a),r0*sin(a)]]));}
module jig_floor2d(){ w=chan/2+wall_t;
  sector2d(c_jump,0,90,R-w,R+w); sector2d(c_out2,-90,90,R-w,R+w); sector2d(c_in,180,90,R-w,R+w);
  translate([jw0,c_jump[1]+R-w])square([c_jump[0]-jw0+0.01,2*w]);   // jumper straight
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
  translate([xc+20,c_jump[1]+R-4])square([jw0-xc-20+0.01,8]); // splitter to jumper
  translate([c_in[0]-2,in_y-5])square([xc-24-c_in[0]+2.01,10]);     // splitter to IN
  translate([xc+20,out2_y-5])square([c_out2[0]-xc-20+2,10]);        // splitter to OUT
  translate([xc-8,y0+sp_l+10])square([16,c_in[1]+36-y0-sp_l-10]);     // splitter to the ID patch
  translate([c_in[0]-R,c_in[1]+30])square([c_out2[0]+2*R-c_in[0],10]); // cross tie, carries the ID
  translate([xc-8,c_in[1]+30])square([16,bar_y0-c_in[1]-29.99]);    // to the rib
}
module jig(){translate([0,0,-(fl_top-jf)])difference(){
  union(){
    translate([0,0,fl_top-jf])linear_extrude(jf)jig_floor2d();
    channels(); rear_rib(); cov_pillars(fl_top-jf);
    translate([tx0,70,fl_top-0.01])cube([side_t,bar_y1-70,wall_top-fl_top+0.01]);
    for(f=sb_feet)translate([f[0],f[1],fl_top-0.01])cylinder(d=22,h=pad+0.01);
    for(y=[sby0-sb_clr/2-2,sby0+SB[1]+sb_clr/2])translate([sbx0+15,y,fl_top-0.01])cube([SB[0]-30,2,pad+6]);
    translate([xc-sp_w/2+2,y0+2,fl_top-0.01])cube([sp_w-4,sp_l-4,riser+0.01]);
    for(e=ears)translate([e[0],e[1],fl_top-0.01])cylinder(d=boss_d,h=riser+0.01);
  }
  for(f=sb_feet)translate([f[0],f[1],case_z-foot_dp])cylinder(d=foot_d,h=foot_dp+pad);
  for(e=ears)translate([e[0],e[1],sp_z-ins_dp])ws_insert_bore(ws_insert_m3,ins_dp+1);
  cov_bores();
  translate([xc,c_in[1]+35,fl_top-0.6])linear_extrude(1)text("MRT-T3",size=6,font="Liberation Sans:style=Bold",halign="center",valign="center");
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
      translate([0,sl_l,0])rotate([90,0,0])linear_extrude(4)polygon([[f-0.4,lip_u],[f,lip_u],[f+p,lip_u+p],[f+p,18],[f-0.4,18]]);
    }
  }
  for(i=[0:2])translate([i*sl_pitch+wall_t+chan/2,22,fl_top-0.6])linear_extrude(1)text(str(sl_gaps[i]),size=4,font="Liberation Sans:style=Bold",halign="center",valign="center");
  translate([(3*sl_pitch+wall_t)/2,0.6,5.5+fl_top])rotate([90,0,0])linear_extrude(1)text("MRT-T2",size=4,font="Liberation Sans:style=Bold",halign="center",valign="center");
}}
// ---- Context models
module screenbeam(){
  translate([sbx0,sby0,case_z])cube([SB[0],SB[1],SB[2]-foot_h]);
  for(f=sb_feet)translate([f[0],f[1],case_z-foot_h])cylinder(d=13,h=foot_h+0.01);
  translate([coax_p[0]-0.01,coax_p[1],coax_p[2]])rotate([0,90,0])cylinder(d=9.5,h=11);
}
module splitter(){
  translate([x_in,y0,sp_z])cube([sp_w,sp_l,sp_h]);
  for(y=[out1_y,out2_y])translate([x_out-0.01,y,axis_z])rotate([0,90,0])cylinder(d=sp_port_d,h=sp_port);
  translate([x_in+0.01,in_y,axis_z])rotate([0,-90,0])cylinder(d=sp_port_d,h=sp_port);
  for(e=ears)translate([e[0],e[1],sp_z])difference(){
    union(){cylinder(d=sp_ear_d,h=sp_ear_t);hull(){cylinder(d=sp_ear_d,h=sp_ear_t);translate([xc-e[0],yc-e[1],0])cylinder(d=sp_ear_d,h=sp_ear_t);}}
    translate([0,0,-1])cylinder(d=sp_ear_hole,h=sp_ear_t+2);
  }
}
module rod(a,b,d){hull(){translate(a)sphere(d=d,$fn=24);translate(b)sphere(d=d,$fn=24);}}
module run(pts,d){for(i=[0:len(pts)-2])rod(pts[i],pts[i+1],d);}
function arc_pts(c,a0,a1,z0,z1,n=8)=[for(i=[0:n])let(t=i/n,a=a0+(a1-a0)*t)[c[0]+R*cos(a),c[1]+R*sin(a),z0+(z1-z0)*t]];
coax_d=7; rest=fl_top+coax_d/2+1;
module cables(){
  // right-angle F on the ScreenBeam. Span from port face to outer face 24.6 confirmed by Brian 2026-11-04; barrel tip 38.2 from porch16, not confirmed here
  rod(coax_p,[ra_x,coax_p[1],coax_p[2]],12); rod([ra_x,coax_p[1],coax_p[2]],[ra_x,ra_tip_y,coax_p[2]],12);
  // jumper: right-angle F, bend, straight into OUT1
  run(concat([[ra_x,ra_tip_y,coax_p[2]]],arc_pts(c_jump,0,90,coax_p[2]-3,rest+3),[[x_out+sp_port,out1_y,axis_z]]),coax_d);
  // modem coax out of OUT2, IN coax into IN, each with an F connector at the port
  run(concat([[x_out+sp_port,out2_y,axis_z]],arc_pts(c_out2,-90,0,rest+4,rest),[[c_out2[0]+R,245,rest]]),coax_d);
  run(concat([[x_in-sp_port,in_y,axis_z]],arc_pts(c_in,270,180,rest+4,rest),[[c_in[0]-R,245,rest]]),coax_d);
  for(p=[[x_out+sp_port-1,out1_y],[x_out+sp_port-1,out2_y]])translate([p[0],p[1],axis_z])rotate([0,90,0])cylinder(d=11.5,h=sp_a-sp_port+1);
  translate([x_in-sp_port+1,in_y,axis_z])rotate([0,-90,0])cylinder(d=11.5,h=sp_a-sp_port+1);
  // power plug and cord (ASSUMED 45 long, 5 cord), LAN plug and cord (ASSUMED 38 long, 6 cord)
  translate([pwr_end,pwr_y-6,port_z-6])cube([sbx0-pwr_end,12,12]);
  translate([lan_end,lan_y-8,port_z-7])cube([sbx0-lan_end,16,14]);
  rp=11; lp=24; cx=(tx0+side_t+split_wall-wall_t)/2;
  run(concat([for(i=[0:6])let(a=90-i*15)[pwr_end-rp*sin(90-a),pwr_y+rp-rp*cos(90-a),port_z-i*1.8]],[[pwr_end-rp,pwr_y+rp+20,fl_top+4],[pwr_end-rp,245,fl_top+4]]),5);
  run(concat([for(i=[0:6])let(a=90-i*15)[lan_end-lp*sin(90-a),lan_y+lp-lp*cos(90-a),port_z-i*1.6]],[[lan_end-lp,lan_y+lp+20,fl_top+4],[lan_end-lp,245,fl_top+4]]),6);
}
// ---- Check-only parts for tools/release_part.py (never released)
// keepout: each M6 head recess stays open, plus an 8 mm driver path 40 mm straight back from it; the shoe screw heads behind the rear posts.
drive_d=6; drive_l=40;
module keepout(){
  for(s=[0,1])mir(s)for(z=j_z){yu=hs_l+hs_gap;
    ws_m6_head_keepout(j_x[0],yu,z,hs_t);
    ws_head_keepout(j_x[0],yu+hs_t,z,drive_d,drive_l);}
  for(s=[0,1])mir(s)for(dz=[-hole_dz,hole_dz])ws_head_keepout(x_mid-hole_x,rack_depth+ear_t,rack_pitch/2+dz,ws_m6_head_d,6);
}
// cuts: the tray's three floor windows and four Velcro strap slots as solids; they must stay separate openings.
module cuts(){
  translate([0,0,fl_z-1])linear_extrude(fl_top-fl_z+1.01){rr(sbx0+30,sbx0+90,sby0+13,sby0+52,6);rr(32,sbx0+60,78,99,6);rr(134,166,104,128,6);}
  for(x=[sbx0+30,sbx0+90]){translate([x-9,-1,fl_z-1])cube([18,4.3,11]);strap_slot(x,sby0+SB[1]+sb_clr/2+2.3);}
}
translate([-x_mid,0,0]){
  if(part=="plate")plate();
  if(part=="tray")tray();
  if(part=="cover_j")cover_j();
  if(part=="cover_o")cover_o();
  if(part=="cover_i")cover_i();
  if(part=="jig")jig();
  if(part=="slice")slice();
  if(part=="shoe_left")shoe("MRT-C-L");
  if(part=="shoe_right")mir(1)shoe("MRT-C-R");
  if(part=="screenbeam")screenbeam();
  if(part=="splitter")splitter();
  if(part=="cables")cables();
  if(part=="clash_devices")intersection(){tray();union(){screenbeam();splitter();}}
  if(part=="clash_cables")intersection(){tray();cables();}
  if(part=="keepout")keepout();
  if(part=="cuts")cuts();
}
