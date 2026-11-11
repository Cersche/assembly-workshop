// OptiPlex rear cable bar: DRAFT concepts (2026-11-11). No ID yet; unprinted, fit and strength UNKNOWN.
// Spans left-right between the OPX-G rear channels, behind the PC, so cables crossing the rack have a path.
// Fits the OPX-G channels as they are: no change to them.
//  - Slides in from the rear between the channels.
//  - A long spring arm on each end rides the web's inner face and its bump clicks out into the OPX-G cable window,
//    catching the window's rear edge (Y 212). 45 deg catch: pull firmly to remove (retention UNKNOWN).
//  - A flag on each end lands on the ear plate's rear face (Y 244): forward stop.
//  - A column at each end sits between the floor ledge (Z 3.3) and roof ledge (Z 41): no lift.
// Frame as OPX-G: X centred, Z=0 slot bottom, rear post back Y=240, ear plate rear face Y=244.
// Prints upright (Z down on the bed), no supports intended.
part="A";   // A trough, B tie bar, C two-lane trough, keepout

$fn=40;
// OPX-G geometry (read from outputs/OptiPlex_Sleeve_Channels_OPX-G_2026-11-04/src/OPX-G.scad)
web_in=91.75; ledge_top=3.3; roof_low=41.0; ear_back=244; win_rear=212;
// bar
cl=0.3;
z_bot=ledge_top+cl;          // 3.6
y_f=214;  y_b=236;           // body: 42 behind the PC's rear (171.7) for plugs
body_x=86;                   // body ends; arm gap outside it
arm_x0=89.05; arm_x1=web_in-cl;   // 2.4 thick arm, 3.05 gap to flex into
arm_y0=199; arm_top=18.4;
bump=2.5; bz0=11.2; bz1=18.0;     // bump stays where the window's rear edge is straight
flag_x1=103; flag_t=3; flag_top=30;

module along_x(x0,x1){translate([x0,0,0])rotate([90,0,90])linear_extrude(x1-x0)children();}  // 2D (y,z) profile along X

// ---- one end, right side (left is mirrored)
module end(){
 // beam joining the body's rear to the flag
 translate([76,y_b-3,z_bot])cube([body_x-76,ear_back+cl-(y_b-3),13-z_bot]);
 // flag on the ear plate's rear face
 translate([76,ear_back+cl,z_bot])cube([flag_x1-76,flag_t,flag_top-z_bot]);
 // spring arm, rooted in the flag
 translate([arm_x0,arm_y0,z_bot])cube([arm_x1-arm_x0,ear_back+cl-arm_y0+0.01,arm_top-z_bot]);
 // column between floor and roof ledges, behind the cable path
 translate([arm_x0,238,z_bot])cube([arm_x1-arm_x0,ear_back+cl-238+0.01,roof_low-cl-z_bot]);
 // bump: ramp in front, 45 deg catch behind, 45 deg underside for printing
 intersection(){
  translate([0,0,bz0])linear_extrude(bz1-bz0)polygon([[arm_x1-0.01,arm_y0+2],[arm_x1+bump,arm_y0+7],[arm_x1+bump,win_rear-cl-bump],[arm_x1-0.01,win_rear-cl]]);
  translate([0,260,0])rotate([90,0,0])linear_extrude(80)polygon([[arm_x1-0.01,bz0],[arm_x1+bump+1,bz0+bump+1],[arm_x1+bump+1,bz1+1],[arm_x1-0.01,bz1+1]]);
 }
}
module ends(){end();mirror([1,0,0])end();}

// ---- body profiles (y,z)
module trough2d(){
 translate([y_f,z_bot])square([y_b-y_f,3]);            // floor
 translate([y_f,z_bot])square([3,30-z_bot]);            // front wall: keeps cables off the plugs
 translate([y_b-3,z_bot])square([3,13-z_bot]);          // low rear lip: push cables in from behind
}
module A(){along_x(-body_x,body_x)trough2d();ends();}

module C(){along_x(-body_x,body_x){trough2d();translate([224,z_bot])square([2,22-z_bot]);}ends();}  // divider: front lane / rear lane

// B: upright plate with strap slot pairs (velcro up to 12 wide or zip ties) plus a shelf at the bottom
slot_xs=[-60,-20,20,60];
module B(){
 difference(){
  along_x(-body_x,body_x){translate([222,z_bot])square([4,32-z_bot]);translate([y_f,z_bot])square([y_b-y_f,3]);}
  for(x=slot_xs,d=[-5,5])translate([x+d-1.5,221,11])cube([3,6,14]);
 }
 // beam from the plate to the end pieces
 for(s=[-1,1])scale([s,1,1])translate([70,y_f,z_bot])cube([body_x-70,y_b-y_f,13-z_bot]);
 ends();
}

module keepout(){}   // no screws on this part

if(part=="A")A();
else if(part=="B")B();
else if(part=="C")C();
else if(part=="keepout")keepout();
