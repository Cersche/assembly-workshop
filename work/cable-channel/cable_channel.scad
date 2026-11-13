// Wall cable channel set: straight, flat 90 elbow, snap covers. DRAFT 2, unprinted (2026-11-12).
// Holds 1 Cat5 + a thin power lead, plus coax on the section between the wall outlet and the MoCA box.
// Fit, cable capacity, snap retention and strength UNKNOWN until printed.
// Frame: run along X, width Y, Z out from the wall (back on the wall/bed at Z=0).
// part = "channel" | "cover" | "elbow" | "elbow_cover" | "demo"  (pieces are in print orientation)

part="demo";
L=200;          // straight segment length
iw=22;          // inside width: coax 6.9 + Cat5 ~5.5 + lead ~6 side by side, with room (cable sizes UNKNOWN)
ih=11;          // inside height, floor top to cover underside
floor_t=4;      // back: deep enough for the tie recesses
wall=2.5;
fil=1.5;        // inside fillets: stress relief at the wall roots
W=iw+2*wall; H=floor_t+ih;

// snap cover: the cover legs flex, not the base walls. Leg 9 long x 1.6, 0.5 hook -> about 1.5% strain (estimate).
leg_t=1.6; leg_gap=0.2; leg_len=9; web_t=2.5; hook=0.5;
gz=H-leg_len;   // groove / hook bottom
// tie points: ties <= 4.8 wide (Brian 2026-11-12). Strap goes down one slot, under a bridge in the back, up the other.
tie_w=5.5; tie_slot=2.6; tie_recess=2.2; tie_x=[40,L/2,L-40];
// wall screws (into the wall, not the print): #6 / 3.5 mm countersunk. Screw type to confirm.
wall_hole=3.8; wall_head=7.5; mount_x=[15,L-15];
// elbow
R=20;           // inside radius of the turn (cable bend room)
S=15;           // square straight stubs at each end so pieces butt flush
$fn=64;

module base2d(){
 difference(){
  offset(r=-fil)offset(delta=fil)difference(){square([W,H]);translate([wall,floor_t])square([iw,ih+5]);}
  // detent groove on each outer face (trapezoid, 0.6 deep)
  for(m=[0,1])translate([m*W,0])mirror([m,0])polygon([[-0.01,gz-0.1],[0.6,gz+0.5],[0.6,gz+0.9],[-0.01,gz+1.7]]);
  // small chamfer on outer top edges so the cover seats
  for(m=[0,1])translate([m*W,0])mirror([m,0])polygon([[-0.01,H+0.01],[-0.01,H-0.5],[0.5,H+0.01]]);
 }
}
module cover2d(){
 ow=leg_gap+leg_t;
 difference(){
  hull(){
   translate([-ow,gz])square([W+2*ow,0.1]);
   for(y=[-ow+1.5,W+ow-1.5])translate([y,H+web_t-1.5])circle(r=1.5);
  }
  translate([-leg_gap,gz-1])square([W+2*leg_gap,H-gz+1]);
 }
 // hooks: lead-in below, 45 back face above so it can be pried off without snapping
 for(m=[0,1])translate([m*W,0])mirror([m,0])polygon([[-leg_gap-0.01,gz],[hook,gz+0.6],[hook,gz+0.9],[-leg_gap-0.01,gz+0.9+hook+leg_gap]]);
 // seat fillet matching the base chamfer
 for(m=[0,1])translate([m*W,0])mirror([m,0])polygon([[-leg_gap,H+0.01],[-leg_gap,H-0.4],[0.3,H+0.01]]);
}

module tie_cuts(x){
 for(y=[wall,W-wall-tie_slot])translate([x-tie_w/2,y,-1])cube([tie_w,tie_slot,floor_t+2]);
 translate([x-tie_w/2,wall,-1])cube([tie_w,iw,tie_recess+1]);
}
module mount_cut(){
 translate([0,0,-1])cylinder(d=wall_hole,h=floor_t+2);
 translate([0,0,floor_t-(wall_head-wall_hole)/2])cylinder(d1=wall_hole,d2=wall_head,h=(wall_head-wall_hole)/2+0.01);
 translate([0,0,floor_t])cylinder(d=wall_head,h=2);
}

module channel(){
 difference(){
  rotate([90,0,90])linear_extrude(height=L)base2d();
  for(x=tie_x)tie_cuts(x);
  for(x=mount_x)translate([x,W/2,0])mount_cut();
 }
}
module cover(){rotate([90,0,90])linear_extrude(height=L)cover2d();}

// elbow, native frame: enters along +Y at x=R..R+W (y=-S), turns about the origin, leaves along -X (x=-S)
module bend(prof){
 rotate_extrude(angle=90,$fn=160)translate([R,0])children(0);
 translate([R,0,0])rotate([90,0,0])linear_extrude(S)children(0);
 rotate([0,0,90])mirror([0,1,0])translate([R,0,0])rotate([90,0,0])linear_extrude(S)children(0);
}
module elbow(){
 c=R+W/2;
 difference(){
  bend()base2d();
  rotate([0,0,45])translate([c,0,0])mount_cut();
 }
}
module elbow_cover(){bend()cover2d();}

// demo: horizontal run, elbow turning up the wall, first vertical segment, covers on
module place_elbow(){translate([L+S,R+W,0])rotate([0,0,-90])children();}
module place_up(){translate([L+S+R+W,R+W+S,0])rotate([0,0,90])children();}

if(part=="channel")channel();
if(part=="cover")translate([0,W,H+web_t])rotate([180,0,0])cover();
if(part=="elbow")elbow();
if(part=="elbow_cover")translate([0,0,H+web_t])rotate([180,0,0])elbow_cover();
if(part=="demo"){
 channel(); place_elbow()elbow(); place_up()channel();
 color("lightblue"){cover(); place_elbow()elbow_cover(); place_up()cover();}
}
