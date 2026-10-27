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
// ScreenBeam standing, coax end up, vents towards the lid; 6 mm further forward than parts.scad so the cradle bosses
// on the back wall are deep enough for inserts. cz = vertical adjustment of cradle + ScreenBeam (slots allow +-cz_adj).
cz=0; cz_adj=6;
SB=[17.5,28,62];   // ScreenBeam corner (65 x 30 x 120)
module sb_device(){translate([0,0,cz]){
 color([0.12,0.12,0.13])translate(SB)cube([65,30,120]);
 color([0.3,0.3,0.32])translate([SB[0]+12,SB[1]-0.5,SB[2]+30])cube([41,1,60]);
}}
// Cradle (printable, part pick=4 in porch15.scad). Back plate on four back-wall bosses (M3 heat-set inserts) through
// vertical slots, so the cradle and ScreenBeam slide up/down +-cz_adj, then lock. Two shelf pads carry the ScreenBeam
// with a gap between them for the power and Ethernet plugs; front lips on the pads and side lips keep it in; a Velcro
// strap (~20 mm, like Brian's) goes through two plate slots and across the front, also holding the jumper.
cr_y=SB[1]+30;          // plate front face (ScreenBeam back)
cr_t=4;                 // plate thickness; bosses fill cr_y+cr_t .. back wall
cr_slots=[[8,70],[97,70],[8,136],[97,136]];   // slot centres (X, Z at cz=0)
module cradle15(){translate([0,0,cz])color([0.55,0.75,0.6])difference(){
 union(){
  translate([4,cr_y,56])cube([97,cr_t,94]);                                   // back plate
  translate([14.5,cr_y-8,56])cube([3,8,94]);translate([82.5,cr_y-8,56])cube([2,8,94]);   // side lips (right one thin: jumper beside it)
  for(x=[[14.5,36],[70,85.5]])translate([x[0],SB[1]-3,SB[2]-4])cube([x[1]-x[0],cr_y-SB[1]+3,4]);   // shelf pads
  for(x=[[14.5,36],[70,85.5]])translate([x[0],SB[1]-3,SB[2]-0.01])cube([x[1]-x[0],3,6]);           // front lips
 }
 for(s=cr_slots)translate([s[0],cr_y-1,s[1]])rotate([-90,0,0])linear_extrude(cr_t+2)
  hull(){translate([0,-cz_adj])circle(d=3.4,$fn=20);translate([0,cz_adj])circle(d=3.4,$fn=20);}
 for(x=[9.5,87.5])translate([x,cr_y-1,100])cube([3,cr_t+2,24]);              // strap slots
}}
// box contents as in parts.scad, with the cut floor and the jumper starting above the floor
module contents(){
 color([0.92,0.91,0.87])difference(){import("body15.stl");floor_cuts();}
 for(e=[[59,62],[46,14]])translate([e[0]+sx,e[1],floor_t])nut_slider();
 color([0.2,0.4,0.9])translate([102.5-14,30-8.5,35-8])cube([14,17,16]);   // Ethernet keystone rear, right wall
 sb_device();
 cradle15();
 rod([37.5,43,182],[37.5,43,194]);rod([37.5,43,194],[49.5,43,194]);
 plug45([44.5,43,62],[0,0,-1]);
 // power lead: plug straight down, gentle bend left along the floor, out the left-wall hole (Y50 Z17)
 color([0.15,0.15,0.15])run([[44.5,43,17],[40,47,10],[25,50,11],[14,50,17],[-2,50,17]],4);
 color([0.55,0.75,0.6])difference(){translate([2.5,43,10])cube([11.5,14,14]);translate([0,50,17])rotate([0,90,0])cylinder(d=4.5,h=20,$fn=16);}   // strain-relief clamp
 rj45ra([60.5,43,55]);
 color([0.15,0.15,0.15])run([[67.5,43,55],[78,38,42],[88.5,30,35]],6);
 // Brian's braided jumper (photo 2026-10-27, ~220 mm): F female end on an F male-male barrel screwed onto the
 // right-angle's jack above the floor, up the ScreenBeam's right side (strapped), right-angle F male onto Coax In on
 // top. Barrel and connector lengths are photo estimates / UNKNOWN.
 color([0.85,0.7,0.3])translate([88+sx,49.5,ra_top])cylinder(d=11,h=12,$fn=6);   // male-male barrel
 color("silver")translate([88+sx,49.5,ra_top+12])cylinder(d=10,h=9,$fn=24);      // jumper F female body
 color([0.1,0.1,0.1])translate([88+sx,49.5,ra_top+21])cylinder(d=9,h=11,$fn=24);  // strain relief
 color([0.45,0.45,0.45])run([[88+sx,49.5,ra_top+32],[88,49.5,160],[82,49.5,186],[64,43,196],[49.5,43,194]],7);
}

translate([0,0,-exploded])porch();
translate([sx,0,0]){
 splitter_hang([52.5,38,-11],2);
 rod([76,49.5,-11],[88,49.5,-11]);rod([88,49.5,-11],[88,49.5,ra_top]);   // right-angle F up through the floor slot
 for(e=[[59,62],[46,14]])color("silver")translate([e[0],e[1],-4])cylinder(d=3,h=8,$fn=16); // ear screws
}
color([0.95,0.95,0.95]){run([[29+sx,38,-11],[5,38,-11],[-25,38,-16]]);run([[76+sx,26.5,-11],[100,26.5,-11],[130,26.5,-16]]);}
color([0.15,0.15,0.15]){run([[-2,50,17],[-14,50,12],[-20,46,-8],[-25,46,-40]],4);   // power lead down beside the coax
 run([[105,30,35],[125,30,30],[140,30,20]],6);}   // Ethernet patch out of the right-wall keystone
contents();
