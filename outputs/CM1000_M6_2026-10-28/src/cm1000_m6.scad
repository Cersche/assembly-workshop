// CM1000 bracket, M6 revision (CM6A). Brian 2026-10-28: rack M6 heat-set inserts + M6 x 8 button heads,
// and tie into the unused middle rack-post hole. Built on the printed baseline meshes
// (outputs/STL_Deliveries/2026-10-16_CM1000_bracket, faceplate + rails v2), extracted to orig/ by extract.py.
// Remix of noyoustupid / Jsmaz3 (CC BY-NC-SA): personal use, never redistribute.
// Frame = the baseline 3MF parts: X across (254), Y depth (faceplate front Y=0, rails Y16..137.6), Z height (0..44.45).
// part = "faceplate" | "rail_l" | "rail_r"
part = "faceplate";
id = "CM6A";

joint_x = [22.6, 231.4];   // faceplate-to-rail screws, were x23/x231
joint_z = [8.6, 35.85];    // were 8.8 / 35.7; moved toward the outer face and floor: the 7.6 pilot keeps ~2 mm walls to the pocket corner
pilot_d = 7.6;             // rack-post insert hole (Brian: "fits the heatsets perfectly")
pilot_y = [9.0, 16.5];     // 7 mm deep into the faceplate's rear stub (post holes are 6 deep)
clear_d = 6.6;             // M6 clearance through the 4 mm rail flange (Y16..20)
bay_h   = 12;              // M6 button head 10.5 dia + 0.75 each side
bay_y   = [20, 54];        // head seat Y20; 34 mm fits a standard 4 mm L-key's ~29 mm short arm
mid_dz  = 22.225 - 6.35;   // middle post hole = U centre; copy of the lower rack slot

o = "orig/";
module engrave(t, p, rot = 0)
    translate(p) rotate([0, 0, rot]) translate([0, 0, -0.5]) linear_extrude(1)
        text(t, size = 4, font = "Liberation Sans:style=Bold", halign = "center", valign = "center");
module ycyl(x, z, d, y0, y1) translate([x, y0, z]) rotate([-90, 0, 0]) cylinder(d = d, h = y1 - y0, $fn = 48);

module faceplate() difference() {
    union() { import(str(o, "fp_1_normal_part.stl")); import(str(o, "fp_16_normal_part.stl")); import(str(o, "fp_17_normal_part.stl")); }
    for (n = [18:21]) import(str(o, "fp_", n, "_negative_part.stl"));          // four corner rack slots
    for (n = [18, 20]) translate([0, 0, mid_dz]) import(str(o, "fp_", n, "_negative_part.stl")); // middle slots
    for (x = joint_x, z = joint_z) ycyl(x, z, pilot_d, pilot_y[0], pilot_y[1]);
    engrave(str(id, "-F"), [127, 7.5, 44.45]);
}
module rail(body, x0) difference() {
    import(str(o, "rl_", body, "_normal_part.stl"));
    for (z = joint_z) {
        ycyl(x0, z, clear_d, 15, 20.5);
        translate([x0 - 9, bay_y[0], z - bay_h / 2]) cube([26, bay_y[1] - bay_y[0], bay_h]);
    }
    engrave(str(id, x0 < 127 ? "-L" : "-R"), [x0 + 3, 95, 44.45], 90);
}
if (part == "faceplate") faceplate();   // CGAL fails on this mesh: build with faceplate_freecad.py
if (part == "id_F") engrave(str(id, "-F"), [127, 7.5, 44.45]);
if (part == "rail_l") rail(1, joint_x[0]);
if (part == "rail_r") rail(6, joint_x[1]);
