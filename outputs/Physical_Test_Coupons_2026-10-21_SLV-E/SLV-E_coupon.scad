// SLV-E (2026-10-21): OptiPlex sleeve rear bracket in the APP's default "Reinforced" rear_style (Codex tasks 29-31),
// for comparison with SLV-D (the older "Open" cable openings). Nothing is redrawn or cut here: SLV-E_app_source.scad is
// exactly what the app writes (equipment.clean() + equipment.source() on SLV-E_spec.json = the SLV-D spec with
// rear_openings removed and rear_style="reinforced"). This wrapper only engraves the ID and lays the part flat for printing.
// PROPOSED, UNVALIDATED: bracket stiffness, fit and strength UNKNOWN.
// Export: openscad.exe -o SLV-E-REAR.stl SLV-E_coupon.scad
use <SLV-E_app_source.scad>
$fn=48;
depth=0.6;
font="Liberation Sans:style=Bold";

// ID on the outer face, on the left ear seen from behind the rack: X 104..108 sits between the windows and side lip
// (end at X 100) and the rack slots (start at X 113.26). Reads bottom to top.
module rear_id(){multmatrix([[-1,0,0,106],[0,0,1,244],[0,1,0,22.2]])translate([0,0,-depth])linear_extrude(height=depth+0.1)
 rotate(90)text("SLV-E-REAR",size=3.5,font=font,halign="center",valign="center");}

translate([0,0,244]) rotate([-90,0,0]) difference(){rear_bracket();rear_id();}   // outer face on the bed, bosses up
