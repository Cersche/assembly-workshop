// FP44 plate-height coupons (2026-10-20): right-ear slice of the faceplate at a test height.
// Checks whether a taller plate (44.4 target) clears in the Lab Rax rack, alone and stacked in adjacent U.
// Same outline rules as equipment_tray.scad: 4 mm plate, corner radius 2.5, capsule slots 10 x 7 at
// X = +/-118.2625 and plate centre +/-15.902 (faceplate_mounting.json). The plate stays centred on its
// slots, so a taller plate grows equally top and bottom and the slots keep their rack positions.
// Laid flat for printing: front face up (Z = 4), ID engraved into the front face, inner edge is a cut, not a test edge.
// Does not change the app default (plate_h = u*44.45-2.45 = 42). PROPOSED, UNVALIDATED: fit UNKNOWN.
// Export one coupon: openscad.exe -o FP44-A_h44.4.stl -D id="\"FP44-A\"" -D h=44.4 -D label="\"44.4\"" FP44_plate_height_coupon.scad
$fn=64;
id="FP44-A";               // coupon ID, engraved on the part
h=44.4;                    // plate height under test (mm)
plate_w=252; plate_t=4; plate_r=2.5;
hole_x=118.2625; hole_dz=15.902;
x0=86;                     // inner cut edge; coupon spans X 86..126 (40 mm, one ear)
text_depth=0.6;

module capsule2d(len=10,diam=7){hull(){translate([-(len-diam)/2,0])circle(d=diam);translate([(len-diam)/2,0])circle(d=diam);}}
// Full plate outline (2D X = rack X, 2D Y = plate height), then keep only the right ear.
module ear2d(){
 intersection(){
  difference(){
   hull()for(sx=[-1,1],sz=[-1,1])translate([sx*(plate_w/2-plate_r),h/2+sz*(h/2-plate_r)])circle(r=plate_r);
   for(dz=[-hole_dz,hole_dz],x=[-hole_x,hole_x])translate([x,h/2+dz])capsule2d();
  }
  translate([x0,-1])square([plate_w/2-x0+1,h+2]);
 }
}
label="44.4";               // height text engraved under the ID (pass with -D so 44.0 keeps its decimal)
difference(){
 translate([-x0,0,0])linear_extrude(height=plate_t)ear2d();
 // ID and height, centred in the 27 mm between the cut edge and the slots, well clear of top/bottom edges.
 for(line=[[id,h/2+2.5],[label,h/2-6.5]])
  translate([(hole_x-5-x0)/2-1,line[1],plate_t-text_depth])linear_extrude(height=text_depth+0.1)
   text(line[0],size=4,font="Liberation Sans:style=Bold",halign="center",valign="bottom");
}
