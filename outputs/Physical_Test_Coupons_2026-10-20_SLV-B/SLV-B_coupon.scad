// SLV-B (2026-10-20): full OptiPlex Micro 7010 sleeve tray on rear-post support + its rear bracket.
// The faceplate is NOT reprinted: SLV-A-PLATE is the same plate (the faceplate does not depend on rear_support).
// Geometry is NOT redrawn here: SLV-B_app_source.scad is exactly what the app writes (equipment.clean() +
// equipment.source() on SLV-B_spec.json; template body byte-identical to equipment_tray.scad). This wrapper only
// engraves each part's ID 0.6 mm deep where it touches no tested surface and lays the part flat for printing.
// PROPOSED, UNVALIDATED: full-length fit, retention and strength UNKNOWN until Brian prints it.
// Export: openscad.exe -o SLV-B-TRAY.stl -D part="\"tray\"" SLV-B_coupon.scad   (and part="rear" -> SLV-B-REAR.stl)
use <SLV-B_app_source.scad>
part="tray";                  // tray or rear
$fn=48;
depth=0.6;
font="Liberation Sans:style=Bold";

// Tray: same spot as SLV-A-TRAY (outside of the left wall, Y 6..32, mid-height between the joint pilots).
module tray_id(){multmatrix([[0,0,-1,-97.75],[-1,0,0,19],[0,1,0,21.5]])translate([0,0,-depth])linear_extrude(height=depth+0.1)
 resize([26,3.5])text("SLV-B-TRAY",size=4,font=font,halign="center",valign="center");}
// Rear bracket: plain plate on the rear posts at Y 240..244. ID on its outer (rear) face at the centre, reading
// from behind the rack; the joint tongues/bosses are on the inner face at X +/-40, well away.
module rear_id(){multmatrix([[-1,0,0,0],[0,0,1,244],[0,1,0,22.2]])translate([0,0,-depth])linear_extrude(height=depth+0.1)
 text("SLV-B-REAR",size=5,font=font,halign="center",valign="center");}

if(part=="tray") translate([0,0,-0.5]) difference(){tray();tray_id();}                          // floor bottom at Z=0
else if(part=="rear") translate([0,0,244]) rotate([-90,0,0]) difference(){rear_bracket();rear_id();}  // outer face on the bed, bosses up
