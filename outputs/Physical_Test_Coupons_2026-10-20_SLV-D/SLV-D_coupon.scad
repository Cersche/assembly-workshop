// SLV-D (2026-10-20): OptiPlex sleeve rear bracket with the APP's own cable openings (Codex task 29).
// Replaces SLV-C-REAR (hand-cut openings, unprinted). Nothing is redrawn or cut here: SLV-D_app_source.scad is
// exactly what the app writes (equipment.clean() + equipment.source() on SLV-D_spec.json = the SLV-B spec plus
// rear_openings=true). This wrapper only engraves the ID and lays the part flat for printing.
// PROPOSED, UNVALIDATED: bracket stiffness, fit and strength UNKNOWN.
// Export: openscad.exe -o SLV-D-REAR.stl SLV-D_coupon.scad
use <SLV-D_app_source.scad>
$fn=48;
depth=0.6;
font="Liberation Sans:style=Bold";

// ID on the outer face, on the left ear seen from behind the rack: X 104..108 sits between the openings
// (end at X 100.26) and the rack slots (start at X 113.26). Reads bottom to top.
module rear_id(){multmatrix([[-1,0,0,106],[0,0,1,244],[0,1,0,22.2]])translate([0,0,-depth])linear_extrude(height=depth+0.1)
 rotate(90)text("SLV-D-REAR",size=3.5,font=font,halign="center",valign="center");}

translate([0,0,244]) rotate([-90,0,0]) difference(){rear_bracket();rear_id();}   // outer face on the bed, bosses up
