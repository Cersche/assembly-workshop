// Concept 15 porch (Brian, 2026-10-27): printable splitter porch under the MoCA box. PROPOSED - UNVALIDATED: fit,
// thread, strength and every splitter/adapter size are UNKNOWN (splitter sizes are photo estimates, +-1 mm).
// part="porch" | "nut" | "assembly". Coordinates are the box frame (box underside at Z=0, X 0..105, Y 0..72.5).
//
// - Rounded profile (r10 bottom edges, same as the box), closed tray, no front cover; front flush with the lid face.
// - Splitter IN goes through an open-top slot in the left wall; a threaded bezel nut on the ~1/4 in of IN post left
//   after the cable is on clamps the wall against the splitter body. No coax keystone.
// - Modem coax leaves through an open-top window in the right wall. The Ethernet keystone is on the box's right wall
//   (body15.scad), off the porch.
// - Two M3 x 40 screws from below go through the porch towers, the splitter ears and the box floor slots into
//   captive nut sliders inside the box (c15.scad nut_slider, keyed in 6 mm floor slots), so the same screws hold
//   the splitter and the porch and the nuts stay put during assembly. Shift the splitter with
//   sx (box slots allow +-8; keep sx in -8..0 so the porch stays on the flat part of the box bottom).
// Render the assembly from this folder; it needs body15.stl built from body15.scad.
include <../concepts12-14/parts.scad>
use <c15.scad>

pick=0;          // 0 assembly, 1 porch, 2 nut, 3 nut slider, 4 ScreenBeam cradle (for -D on the command line)
part=pick==1?"porch":pick==2?"nut":pick==3?"slider":pick==4?"cradle":"assembly";
sx=0;            // splitter + porch shift along X
t=2.5;           // porch wall
h=33;            // porch depth below the box
rb=10;           // bottom-edge radius (box corner_r)
in_face=41;      // splitter IN-side body face (X at sx=0)
px0=in_face-t;   // left wall outer face, wall clamped against the splitter body
px1=98;          // right edge (box bottom flat ends at X95; 0.5 mm gap under the box curve)
py0=-2.5; py1=72.5;
in_y=38; in_z=-11;       // IN port axis
post_slot=10;            // IN post 9.5 (3/8 in) + clearance
ears=[[59,62],[46,14]];  // splitter ear centres at sx=0
ear_z=-11;               // ear underside
tower_d=9; m3=3.4; cb_d=6.2; cb_h=3;
nut_d=21.5; nut_h=3;     // bezel nut, covers the open-top slot; with the 2.5 wall it uses 5.5 of the ~6.35 mm free post
win=[19,34,-19];         // right-wall coax window: Y from, Y to, bottom Z (modem coax at Y26.5 Z-11)

module profile(o)hull(){
 for(x=[px0+rb,px1-rb])translate([x,-h+rb])circle(r=rb-o,$fn=72);
 // outside only: the round meets the bed at 45 degrees (no curl-under overhang when printed floor-down)
 if(o==0)translate([px0+rb-0.4142*rb,-h])square([px1-px0-2*rb+2*0.4142*rb,0.01]);
 translate([px0+o,-h+rb])square([px1-px0-2*o,h-rb+(o>0?2:0)]);
}
module along_y(y0,y1)translate([0,y1,0])rotate([90,0,0])linear_extrude(y1-y0)children();

// Raised 0.6 labels on the outer walls (walls print vertical; Brian 2026-10-27 "some labels"). Left reads from the
// left (text runs towards the front), right reads from the right.
module porch_labels(){font="Liberation Sans:style=Bold";
 translate([px0+0.2,59,-14])multmatrix([[0,0,-1,0],[-1,0,0,0],[0,1,0,0]])linear_extrude(0.8)
  text("IN",size=6,font=font,halign="center",valign="center");
 translate([px1-0.2,50,-12])multmatrix([[0,0,1,0],[1,0,0,0],[0,1,0,0]])linear_extrude(0.8)
  text("MODEM",size=4,font=font,halign="center",valign="center");
}
module porch15(){
 color([0.55,0.75,0.6])difference(){
  union(){
   difference(){along_y(py0,py1)profile(0);along_y(py0+t,py1-t)profile(t);}
   for(e=ears)translate([e[0],e[1],-h+t-0.1])cylinder(d=tower_d,h=ear_z+h-t+0.1,$fn=40);
   porch_labels();
  }
  // IN post slot, open to the top
  translate([px0-1,in_y,0])rotate([0,90,0])linear_extrude(t+2)hull(){translate([-in_z,0])circle(d=post_slot,$fn=40);translate([-2,-post_slot/2])square([1,post_slot]);}
  // cable window in the right wall, open to the top, rounded bottom
  translate([px1-t-1,0,0])rotate([0,90,0])linear_extrude(t+2)hull(){
   r=6;for(y=[win[0]+r,win[1]-r])translate([-(win[2]+r),y])circle(r=r,$fn=40);
   translate([-2,win[0]])square([1,win[1]-win[0]]);}
  // screw holes and counterbores through the towers
  for(e=ears){translate([e[0],e[1],-h-1])cylinder(d=m3,h=h,$fn=24);translate([e[0],e[1],-h-1])cylinder(d=cb_d,h=cb_h+1,$fn=32);}
 }
}

// Bezel nut, 3/8-32 UNEF internal thread (F connector). Printed thread is UNKNOWN; a metal F panel nut can replace it
// and this part then becomes a plain cosmetic ring (set thread=false).
thread=true;
module bezel_nut(){
 p=25.4/32;
 color([0.92,0.91,0.87])difference(){
  hull(){cylinder(d=nut_d-1.2,h=0.01,$fn=72);translate([0,0,0.6])cylinder(d=nut_d,h=nut_h-1.2,$fn=72);translate([0,0,nut_h-0.01])cylinder(d=nut_d-1.2,h=0.01,$fn=72);}
  for(i=[0:23])rotate(i*15)translate([nut_d/2+0.3,0,-1])cylinder(d=1.6,h=nut_h+2,$fn=12);  // grip flutes
  if(thread)translate([0,0,-0.5])linear_extrude(nut_h+1,twist=-360*(nut_h+1)/p,slices=60)translate([0.35,0])circle(d=9.1,$fn=40);
  else translate([0,0,-1])cylinder(d=9.8,h=nut_h+2,$fn=40);
 }
}

if(part=="porch")porch15();
else if(part=="nut")bezel_nut();
else if(part=="slider")rotate([180,0,0])nut_slider();   // print pocket-down, key up (from c15.scad)
else if(part=="cradle")rotate([-90,0,0])translate([0,-62,0])cradle15();   // print back face down (from c15.scad)
else {
 translate([sx,0,0]){
  porch15();
  translate([px0,in_y,in_z])rotate([0,-90,0])bezel_nut();
  splitter_hang([52.5,38,-11],2);
  rod([76,49.5,-11],[88,49.5,-11]);rod([88,49.5,-11],[88,49.5,10]);   // right-angle F up through the floor slot
  for(e=ears)color("silver")translate([e[0],e[1],-h+cb_h])cylinder(d=3,h=40,$fn=16);   // M3 x 40
  color([0.95,0.95,0.95]){run([[29,in_y,in_z],[0,in_y,in_z],[-18,in_y,-18],[-25,in_y,-40]]);run([[76,26.5,-11],[100,26.5,-11],[130,26.5,-16]]);}
 }
 color([0.15,0.15,0.15])run([[-2,50,17],[-14,50,12],[-20,46,-8],[-25,46,-40]],4);   // power lead out the left wall, down beside the coax
 contents();
}
