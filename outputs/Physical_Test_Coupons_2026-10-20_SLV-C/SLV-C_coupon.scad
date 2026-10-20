// SLV-C (2026-10-20): OptiPlex sleeve rear bracket WITH CABLE OPENINGS. One-off test part, replaces SLV-B-REAR.
// Base geometry is the app's own rear_bracket() from SLV-C_app_source.scad (byte-identical to SLV-B's app source:
// equipment.clean() + equipment.source() on SLV-C_spec.json, rear_support true). THIS FILE ADDS what the app does
// not have yet (Codex task 29 will add it to the app): windows through the plate so the PC's rear cables (power,
// display, network, USB) can pass straight back. The openings keep 4 mm of plate around the two joint bosses
// (X +/-40, Z 10..19) and tongues (X 34..46, Z 4..7), a 3.5 mm band along the bottom, a 3.9 mm band along the top,
// and the rack ears (slots at X +/-113..123) untouched. Bracket stiffness with these openings is UNKNOWN.
// Export: openscad.exe -o SLV-C-REAR.stl SLV-C_coupon.scad
use <SLV-C_app_source.scad>
$fn=48;
depth=0.6;
font="Liberation Sans:style=Bold";
r=2;                          // opening corner radius

// Openings in rack X / Z (Z from the slot bottom). Top: one wide window above the bosses.
// Bottom: a centre window between the bosses and an outer window each side of them.
module openings2d(){
 for(q=[[-100,100,22,40.5],[-30,30,3.5,22.2],[50,100,3.5,22.2],[-100,-50,3.5,22.2]])
  translate([q[0]+r,q[2]+r])offset(r=r)square([q[1]-q[0]-2*r,q[3]-q[2]-2*r]);
}
// Through the plate (Y 240..244) only. The bosses and tongues sit in front of the plate (Y 232..240) and stay whole.
module openings(){translate([0,244.1,0])rotate([90,0,0])linear_extrude(height=4.2)openings2d();}
// ID on the outer face, on the left ear seen from behind the rack (rack X +100..112 is clear plate between the
// opening and the slots), reading bottom to top.
module rear_id(){multmatrix([[-1,0,0,106],[0,0,1,244],[0,1,0,22.2]])translate([0,0,-depth])linear_extrude(height=depth+0.1)
 rotate(90)text("SLV-C-REAR",size=3.5,font=font,halign="center",valign="center");}

translate([0,0,244]) rotate([-90,0,0]) difference(){rear_bracket();openings();rear_id();}   // outer face on the bed, bosses up
