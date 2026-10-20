// SLV-A coupon (2026-10-20): front 38 mm of the OptiPlex Micro 7010 sleeve tray + its full faceplate.
// Geometry is NOT redrawn here: SLV-A_app_source.scad is exactly what the app writes (equipment.clean() +
// equipment.source() on SLV-A_spec.json, template body byte-identical to equipment_tray.scad), and its own
// coupon=[-130,130,38] parameter keeps every part's slice from Y<=38 at full width. This wrapper only:
//   1. engraves the part ID 0.6 mm deep where it touches no tested surface, and
//   2. lays each part flat for printing (plate front face up; tray floor on the bed).
// The cut rear end is a flat, closed face (OpenSCAD intersection), so no extra capping is needed.
// PROPOSED, UNVALIDATED: fit, retention and strength UNKNOWN until Brian prints it.
// Export: openscad.exe -o SLV-A-PLATE.stl -D part="\"plate\"" SLV-A_coupon.scad   (and part="tray" -> SLV-A-TRAY.stl)
use <SLV-A_app_source.scad>
part="plate";                 // plate or tray
$fn=48;
depth=0.6;                    // engraving depth
font="Liberation Sans:style=Bold";

// Plate: front face (Y=-4), right ear, read bottom-to-top. Band X 98..111 sits between the M3 joint hole
// (X 94.75, d 3.4) and the rack slot (starts X 113.3); Z 8..37 stays clear of all holes and edges.
module plate_id(){translate([104.5,-4,22.2])rotate([90,0,0])translate([0,0,-depth])linear_extrude(height=depth+0.1)
 rotate(90)text("SLV-A-PLATE",size=3.5,font=font,halign="center",valign="center");}
// Tray: outside face of the left wall (X=-97.75), text forced to 26 x 3.5 mm at Y 6..32, Z 19.75..23.25:
// 6 mm clear of the cut end (Y 38), at mid-height between the joint pilots (Z 6.5 / 36.8, 8 mm deep).
// Reads correctly when you look at the left side of the tray from outside.
module tray_id(){multmatrix([[0,0,-1,-97.75],[-1,0,0,19],[0,1,0,21.5]])translate([0,0,-depth])linear_extrude(height=depth+0.1)
 resize([26,3.5])text("SLV-A-TRAY",size=4,font=font,halign="center",valign="center");}

if(part=="plate") translate([0,0,0])rotate([-90,0,0]) difference(){clip_coupon()faceplate();plate_id();}   // front face up at Z=4
else if(part=="tray") translate([0,0,-0.5]) difference(){clip_coupon()tray();tray_id();}                  // floor bottom at Z=0
