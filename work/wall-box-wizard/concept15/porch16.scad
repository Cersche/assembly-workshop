// Concept 15 porch rev 2 (Brian, 2026-10-27, after printing porch15). PROPOSED - UNVALIDATED: fit, thread, strength,
// cord grip and plug sizes are UNKNOWN. Same box frame as porch15 (box underside Z=0, X 0..105, Y 0..72.5, back at
// Y72.5). Render the assembly from this folder; it needs body15.stl built from body15.scad (part="body").
//
// Changes from porch15 (Brian's notes):
// - Splitter sizes are Brian's caliper readings (below), not photo estimates. Porch is 19.6 deep instead of 33.
// - Form-fitting: the front part stops at the splitter's OUT face, so the modem OUT post and its plug sit fully outside
//   (only the 2.5 wall the port passes through; 9.5 of the 13 post is outside). The back part still covers the right-angle F.
// - Splitter ears screw to the box on their own (short M3 into the nut sliders); the porch has its own two M3 x 20
//   screws into heat-set inserts in new floor bosses (body15.scad porch_screws), so it comes off on its own.
// - Power comes in from below: the flat cord (3.55 x 1.75) slips sideways into a slit in the left lobe, weaves around
//   two posts for strain relief and goes up through the 12 mm floor hole (X20 Y54.5) to the ScreenBeam.
// - Bezel nut 14 x 2 (was 21.5 x 3: too tall, too thick, too tight); thread bore opened 0.4 mm.
include <../concepts12-14/parts.scad>
use <c15.scad>

show_box=true;   // assembly: false shows the porch, splitter and cables only
pick=0;          // 0 assembly, 1 porch, 2 nut (for -D on the command line)
part=pick==1?"porch":pick==2?"nut":"assembly";

// Bridgelink splitter, calipers (Brian, 2026-10-27). Back face (ears flush) against the box underside at Z=0, IN to
// -X, OUTs to +X.
sp_l=38.75; sp_w=23; sp_base=7.5; sp_h=15.9; sp_axis=7.5; sp_out=22; sp_in_end=18.5; sp_port=13; sp_port_d=9.5;
sp_ear_l=48.5; sp_ear_s=14; sp_ear_hole=5; sp_ear_d=10; sp_ear_t=9; sp_gnd=8;
ra_reach=18.6; ra_tip=38.2;   // right-angle F: body OUT face to leg centre; port axis to barrel tip
ra_x=88; ra_y=41.5;   // 8 mm forward (Brian 2026-10-28) so the IN coax clears the power plug           // the leg stands in the existing round floor hole, which sets the splitter position
in_face=ra_x-ra_reach-sp_w; out_x=in_face+sp_w; xc=in_face+sp_w/2;
yc=ra_y-sp_out/2; y0=yc-sp_l/2;
in_y=y0+sp_in_end;            // measured from the front end; if it is the other end IN moves 1.75 (slot takes it)
mod_y=yc-sp_out/2;            // modem OUT
ears=[[xc+sp_ear_s/2,yc+sp_ear_l/2],[xc-sp_ear_s/2,yc-sp_ear_l/2]];   // back ear OUT side, front ear IN side

t=2.5; fl=2.5; gap=1.2;   // gap keeps the splitter clear of the inside floor fillet
h=sp_h+gap+fl;               // porch depth below the box
rb=6; rc=3;                  // bottom-edge round (45 deg to the bed), convex plan-corner round
x_in=in_face-t;              // IN wall outer face, clamped against the splitter body
x_out=out_x+1+t;             // front part's right wall (1 mm off the ground block); the modem OUT passes through it
y_step=32.5;                 // front part (Y<y_step) stops at x_out, back part runs to x_back
// Step wall between the two OUT posts (Brian, 2026-10-28: more clearance): 0.5 toward the modem post and thinned to
// step_t above the bottom round, so its inner face is 1 mm off the right-angle F nut (7/16 hex assumed, size UNKNOWN).
step_t=1.6;
x_back=98;                   // box bottom flat ends at X95; 0.5 gap under the box curve (as porch15)
x_lobe=11; y_lobe=37;        // power lobe behind the incoming coax; reaches forward over the plug (0.4 off the bezel nut)
x_lug=83.5; y_lug=11;        // front-right lug for the front porch screw (the ground block fills the front part)
py0=-2.5; py1=72.5;
port_slot=10;
in_slot=11;                  // IN post slot (Brian, 2026-10-28: more clearance at the IN post / bezel nut), 0.75 a side on the 9.5 post
porch_screws=[[18,42],[78,5],[86,62]]; tower_d=9; m3=3.4; cb_d=6.2; cb_h=3;   // same points as body15.scad
pwr_hole=[38.5,43];   // plug under the ScreenBeam jack, 10 mm floor hole (2026-10-28)
cord=[3.55,1.75]; slit_w=2.3; slit_y=66; slit_x1=36;
pwr_posts=[[31,61.5],[25,64.5]]; post_d=5;
nut_d=14; nut_h=2;           // top edge 0.5 below the box underside

module fp()offset(r=rc)offset(delta=-rc)   // inside corners stay sharp: rounding them eats the splitter clearance

 polygon([[x_in,py0],[x_lug,py0],[x_lug,y_lug],[x_out,y_lug],[x_out,y_step],[x_back,y_step],[x_back,py1],[x_lobe,py1],[x_lobe,y_lobe],[x_in,y_lobe]]);
// inset of the outer skin at height z above the porch bottom: r8 round, finishing in a 45 deg flat at the bed
function ins(z)=let(z0=rb*(1-sqrt(0.5)),d0=rb-sqrt(rb*rb-(rb-z0)*(rb-z0)))
 z>=rb?0:z>=z0?rb-sqrt(rb*rb-(rb-z)*(rb-z)):d0+(z0-z);
// cavity: same centre, radius rb-t, so the wall stays t thick round the bottom edge
function ins_c(z)=let(ri=rb-t)z>=rb?0:ri-sqrt(max(ri*ri-(rb-z)*(rb-z),0));
step=0.4;
module skin(extra,z_from){
 for(i=[0:ceil((rb-z_from)/step)-1])let(z=z_from+i*step,zm=z+step/2)translate([0,0,-h+z])linear_extrude(step+0.01)
  offset(delta=-(extra+(extra>0?ins_c(zm):ins(zm))))fp();
 translate([0,0,-h+max(rb,z_from)])linear_extrude(h-max(rb,z_from)+(extra>0?1:0))offset(delta=-extra)fp();
}
module side_slot(x0,x1,y,w=port_slot)translate([x0,y,0])rotate([0,90,0])linear_extrude(x1-x0)
 hull(){translate([sp_axis,0])circle(d=w,$fn=40);translate([-2,-w/2])square([1,w]);}

module porch_labels(){font="Liberation Sans:style=Bold";zl=-(h-rb)/2;
 translate([x_in+0.2,in_y-17,zl])multmatrix([[0,0,-1,0],[-1,0,0,0],[0,1,0,0]])linear_extrude(0.8)
  text("IN",size=5,font=font,halign="center",valign="center");
 translate([x_lobe+0.2,56,zl])multmatrix([[0,0,-1,0],[-1,0,0,0],[0,1,0,0]])linear_extrude(0.8)
  text("PWR",size=5,font=font,halign="center",valign="center");
 translate([63,py0+0.2,zl])rotate([90,0,0])linear_extrude(0.8)   // front face (the lug took the old spot)
  text("MODEM",size=4,font=font,halign="center",valign="center");
}
module porch16(){
 color([0.55,0.75,0.6])difference(){
  union(){
   difference(){skin(0,0);skin(t,fl);}
   for(p=porch_screws)translate([p[0],p[1],-h+fl-0.1])cylinder(d=tower_d,h=h-fl+0.1,$fn=40);
   for(p=pwr_posts)translate([p[0],p[1],-h+fl-0.1])cylinder(d=post_d,h=9,$fn=32);
   porch_labels();
  }
  translate([x_out-t-0.01,y_step+step_t,-h+rb-0.3])cube([x_back-x_out+0.02,t-step_t+0.01,h]);   // thin step wall
  side_slot(x_in-1,in_face+0.5,in_y,in_slot);          // IN post, open to the top
  side_slot(out_x-0.5,x_out+1,mod_y);          // modem OUT post, open to the top
  for(e=ears)translate([e[0],e[1],-sp_ear_t-1])cylinder(d=sp_ear_d+1,h=sp_ear_t+2,$fn=40);   // ear relief
  for(p=porch_screws){translate([p[0],p[1],-h-1])cylinder(d=m3,h=h+2,$fn=24);translate([p[0],p[1],-h-1])cylinder(d=cb_d,h=cb_h+1,$fn=32);}
  // power cord slit: through the lobe's left wall and floor, so the cord slips in sideways with the plug already up
  translate([x_lobe-1,slit_y-slit_w/2,-h-1])cube([slit_x1-x_lobe+1,slit_w,h+2]);
 }
}

// Bezel nut, 3/8-32 UNEF internal thread (F connector), looser than porch15 (bore 9.5 instead of 9.1). Printed thread
// UNKNOWN; thread=false gives a plain 9.8 bore.
thread=true;
module bezel_nut(){
 p=25.4/32;c=0.4;
 color([0.92,0.91,0.87])difference(){
  hull(){cylinder(d=nut_d-2*c,h=0.01,$fn=72);translate([0,0,c])cylinder(d=nut_d,h=nut_h-2*c,$fn=72);translate([0,0,nut_h-0.01])cylinder(d=nut_d-2*c,h=0.01,$fn=72);}
  for(i=[0:19])rotate(i*18)translate([nut_d/2+0.3,0,-1])cylinder(d=1.4,h=nut_h+2,$fn=12);   // grip flutes
  if(thread)translate([0,0,-0.5])linear_extrude(nut_h+1,twist=-360*(nut_h+1)/p,slices=40)translate([0.35,0])circle(d=9.5,$fn=40);
  else translate([0,0,-1])cylinder(d=9.8,h=nut_h+2,$fn=40);
 }
}

// Measured splitter (preview only)
module splitter16(){
 color([0.8,0.8,0.82]){
  translate([in_face,y0,-sp_base])cube([sp_w,sp_l,sp_base]);
  translate([in_face+1,y0+1,-sp_h])cube([sp_w-2,sp_l-2,sp_h-sp_base]);
  translate([xc,y0-sp_gnd,-sp_h+0.5])cube([out_x-xc,sp_gnd,sp_h-0.5]);   // ground block, end of the body, OUT half
  for(e=ears)translate([e[0],e[1],-sp_ear_t])difference(){cylinder(d=sp_ear_d,h=sp_ear_t,$fn=32);translate([0,0,-1])cylinder(d=sp_ear_hole,h=sp_ear_t+2,$fn=24);}
 }
 color([0.75,0.72,0.6]){
  translate([in_face,in_y,-sp_axis])rotate([0,-90,0])cylinder(d=sp_port_d,h=sp_port,$fn=32);
  for(y=[mod_y,ra_y])translate([out_x,y,-sp_axis])rotate([0,90,0])cylinder(d=sp_port_d,h=sp_port,$fn=32);
 }
}

if(part=="porch")porch16();
else if(part=="nut")bezel_nut();
else {
 porch16();
 translate([x_in,in_y,-sp_axis])rotate([0,-90,0])bezel_nut();
 splitter16();
 rod([out_x+sp_port-4,ra_y,-sp_axis],[ra_x,ra_y,-sp_axis]);rod([ra_x,ra_y,-sp_axis],[ra_x,ra_y,ra_tip-sp_axis]);
 slot_y=[54,6];   // body15 ear_slots; the screw sits on the slot line, inside the 5 mm ear hole (0.75 off centre)
 for(i=[0,1]){color("silver")translate([ears[i][0],slot_y[i],-sp_ear_t-2])cylinder(d=3,h=16,$fn=16);   // M3 x 16
  translate([ears[i][0],slot_y[i],2.5])nut_slider();}
 for(p=porch_screws)color("silver")translate([p[0],p[1],-h+cb_h])cylinder(d=3,h=20,$fn=16);  // M3 x 20, porch to insert
 if(show_box){color([0.92,0.91,0.87])import("body15.stl");
  color([0.2,0.4,0.9])translate([102.5-14,18.5-8.5,121.5-8])cube([14,17,16]);   // Ethernet keystone rear
  sb_device();cradle15();}
 color([0.95,0.95,0.95]){
  run([[in_face-sp_port-12,in_y,-sp_axis],[0,in_y,-sp_axis],[-15,in_y,-18],[-20,in_y,-45]]);     // incoming coax
  run([[out_x+sp_port-2,mod_y,-sp_axis],[out_x+sp_port+20,mod_y,-sp_axis],[130,mod_y,-14]]);     // modem coax, outside
 }
 // power: up the wall, sideways into the slit, around the two posts, up through the floor hole to the ScreenBeam
 color([0.15,0.15,0.15])run([[slit_x1-1,slit_y,-60],[slit_x1-1,slit_y,-h+fl+1],[31,58.5,-h+fl+1.5],[25,67.5,-h+fl+1.5],
  [pwr_hole[0],pwr_hole[1],-h+fl+2],[pwr_hole[0],pwr_hole[1],2]],3);
 color([0.1,0.1,0.1])translate([pwr_hole[0],pwr_hole[1],2])cylinder(d=7.75,h=35,$fn=32);   // barrel plug, 35 below the jack
 if(show_box)color([0.45,0.45,0.45])run([[ra_x,ra_y,ra_tip-sp_axis],[ra_x,ra_y,135],sh([82,49.5,186]),sh([64,43,196]),sh([49.5,43,194])],7);
}
