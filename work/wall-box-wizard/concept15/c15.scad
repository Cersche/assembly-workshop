// Concept 15 "Detachable boot" v2 (scratch, 2026-10-27): concept 12 layout, porch is a separate part held by two
// M3 screws up into the box underside. New: the right-angle F on the back OUT passes UP through a slot in the box
// floor and a short jumper inside goes to the ScreenBeam; the splitter slides left/right on slotted floor mounts and
// the floor slot moves with it. Splitter/adapter sizes are estimates / UNKNOWN.
// Render from this folder; needs body15.stl built from body15.scad (STL not committed). The Ethernet keystone is on
// the right wall (2026-10-27), off the porch.
include <../concepts12-14/parts.scad>
exploded=0;     // porch drop for the exploded view
sx=0;           // splitter shift along X (adjustment range +-adj)
adj=8;          // slot half-travel
floor_t=2.5;    // box bottom wall
ra_top=10;      // height of the right-angle F's top above the box underside

module porch(){
 color([0.55,0.75,0.6]){
  translate([5,69,-33])cube([95,3.5,33]);   // back plate
  translate([5,2,-33])cube([95,70.5,3]);    // floor
  translate([5,68,-3])cube([95,4.5,3]);     // top lip against the box underside
 }
 color([0.92,0.91,0.87,0.35])translate([5,2,-30])cube([95,3,30]); // clip-on front cover
 for(x=[20,85]){
  color("silver")translate([x,70.25,-12])cylinder(d=3,h=16,$fn=20);
  color([0.2,0.2,0.2])translate([x,70.25,-12])cylinder(d=5.5,h=3,$fn=20);
 }
}
// floor cutouts: one slot per splitter ear (M3 into a nut/insert inside) and a slot for the right-angle F
module floor_cuts(){
 // 6 mm wide so the nut slider's key rides in it; long enough for the key (10) plus +-adj of travel
 for(e=[[59,62],[46,14]])translate([e[0],e[1],-1])linear_extrude(floor_t+2)
  hull(){translate([-(adj+5)+3,0])circle(d=6,$fn=24);translate([adj+5-3,0])circle(d=6,$fn=24);}
 translate([88,49.5,-1])linear_extrude(floor_t+2)hull(){translate([-adj,0])circle(d=13,$fn=32);translate([adj,0])circle(d=13,$fn=32);}
}
// Captive nut slider (one per ear screw), sits on the box floor inside. Its key rides in the 6 mm floor slot so it
// slides along X but cannot turn; an M3 nut drops into the hex pocket on top. Z=0 is the floor's top face.
module nut_slider(){
 color([0.55,0.75,0.6])difference(){
  union(){translate([-7,-6,0])cube([14,12,4]);translate([-5,-2.8,-2])cube([10,5.6,2.01]);}
  translate([0,0,-3])cylinder(d=3.4,h=10,$fn=24);
  translate([0,0,4-2.6])cylinder(d=5.8/cos(30),h=3,$fn=6);   // M3 nut 5.5 AF x 2.4, pocket 5.8 AF x 2.6
 }
}
// box contents as in parts.scad, with the cut floor and the jumper starting above the floor
module contents(){
 color([0.92,0.91,0.87])difference(){import("body15.stl");floor_cuts();}
 for(e=[[59,62],[46,14]])translate([e[0]+sx,e[1],floor_t])nut_slider();
 color([0.2,0.4,0.9])translate([102.5-14,30-8.5,35-8])cube([14,17,16]);   // Ethernet keystone rear, right wall
 screenbeam([17.5,34,62]);
 rod([37.5,49,182],[37.5,49,194]);rod([37.5,49,194],[49.5,49,194]);
 plug45([44.5,49,62],[0,0,-1]);
 color([0.15,0.15,0.15])run([[44.5,49,17],[40,52,11],[15,52,9],[15,49,-6]],4);
 color([0.55,0.75,0.6])difference(){translate([8,42,4])cube([14,14,9]);translate([15,49,0])cylinder(d=4.5,h=20,$fn=16);}
 rj45ra([60.5,49,55]);
 color([0.15,0.15,0.15])run([[67.5,49,55],[78,42,42],[88.5,30,35]],6);
 // Brian's braided jumper (photo 2026-10-27, ~220 mm): F female end on an F male-male barrel screwed onto the
 // right-angle's jack above the floor, up the ScreenBeam's right side (strapped), right-angle F male onto Coax In on
 // top. Barrel and connector lengths are photo estimates / UNKNOWN.
 color([0.85,0.7,0.3])translate([88+sx,49.5,ra_top])cylinder(d=11,h=12,$fn=6);   // male-male barrel
 color("silver")translate([88+sx,49.5,ra_top+12])cylinder(d=10,h=9,$fn=24);      // jumper F female body
 color([0.1,0.1,0.1])translate([88+sx,49.5,ra_top+21])cylinder(d=9,h=11,$fn=24);  // strain relief
 color([0.45,0.45,0.45])run([[88+sx,49.5,ra_top+32],[88,49.5,160],[82,49.5,186],[64,49,196],[49.5,49,194]],7);
}

translate([0,0,-exploded])porch();
translate([sx,0,0]){
 splitter_hang([52.5,38,-11],2);
 rod([76,49.5,-11],[88,49.5,-11]);rod([88,49.5,-11],[88,49.5,ra_top]);   // right-angle F up through the floor slot
 for(e=[[59,62],[46,14]])color("silver")translate([e[0],e[1],-4])cylinder(d=3,h=8,$fn=16); // ear screws
}
color([0.95,0.95,0.95]){run([[29+sx,38,-11],[5,38,-11],[-25,38,-16]]);run([[76+sx,26.5,-11],[100,26.5,-11],[130,26.5,-16]]);}
color([0.15,0.15,0.15]){run([[15,49,-6],[13,58,-20],[0,62,-24],[-25,62,-26]],4);
 run([[105,30,35],[125,30,30],[140,30,20]],6);}   // Ethernet patch out of the right-wall keystone
contents();
