// SLV-F (2026-10-21): full OptiPlex Micro sleeve v2 print package (Codex task 36 + Claude fixes). No coupon first, by Brian's choice.
// Geometry is NOT redrawn here: SLV-F_app_source_R.scad / _O.scad are exactly what the app writes (equipment.clean() +
// equipment.source() on SLV-F_spec_R.json / _O.json: the SLV-B spec plus sleeve_top=0.8, feet_style="grooves",
// rear_floor_opening=true, insert_bosses=true, and rear_style "reinforced" (R) or "open" (O)). The plate and tray are
// identical in both; only the rear bracket differs. This wrapper only engraves IDs 0.6 mm deep and lays parts flat.
// PROPOSED, UNVALIDATED: fit, click-in retention, insert strength and stiffness UNKNOWN until Brian prints it.
// Export: openscad.exe -o SLV-F-PLATE.stl -D part="\"plate\"" SLV-F_coupon.scad   (tray, rear_r likewise; SLV-F-REAR-O from SLV-F_coupon_O.scad)
use <SLV-F_app_source_R.scad>
part="plate";                 // plate, tray or rear_r (rear_o: SLV-F_coupon_O.scad)
$fn=48;
depth=0.6;
font="Liberation Sans:style=Bold";

// Plate: front face, right ear, bottom-to-top, between the M3 joint hole (X 95.75, d 3.4) and the rack slot (X 113.3).
module plate_id(){translate([104.5,-4,22.2])rotate([90,0,0])translate([0,0,-depth])linear_extrude(height=depth+0.1)
 rotate(90)text("SLV-F-PLATE",size=3.5,font=font,halign="center",valign="center");}
// Tray: outside of the left wall (X -97.75), Y 6..32, Z 19.75..23.25: between the insert bosses (Z 1.5..11.5 and
// 32.8..42.8, Y 0..12) and in front of the first strap slot (Y 38.6).
module tray_id(){multmatrix([[0,0,-1,-97.75],[-1,0,0,19],[0,1,0,21.5]])translate([0,0,-depth])linear_extrude(height=depth+0.1)
 resize([26,3.5])text("SLV-F-TRAY",size=4,font=font,halign="center",valign="center");}
// Rear bracket: outer face, left ear seen from behind (X 104..108), between the windows/lips (end X 100.25) and the rack slots.
module rear_id(t){multmatrix([[-1,0,0,106],[0,0,1,244],[0,1,0,22.2]])translate([0,0,-depth])linear_extrude(height=depth+0.1)
 rotate(90)text(t,size=3.5,font=font,halign="center",valign="center");}

if(part=="plate") rotate([-90,0,0]) difference(){faceplate();plate_id();}                                    // front face up
else if(part=="tray") difference(){tray();tray_id();}                                                        // flat underside on the bed (Z=0)
else if(part=="rear_r") translate([0,0,244]) rotate([-90,0,0]) difference(){rear_bracket();rear_id("SLV-F-REAR-R");}  // outer face on the bed
