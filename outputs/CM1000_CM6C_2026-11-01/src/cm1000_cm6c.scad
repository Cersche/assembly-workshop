// CM1000 bracket CM6C (2026-11-01). CM6A + the end channels recut to the modem's measured end wedge.
// Brian measured: modem 44.5 tall, 12 mm end wedge; forced into CM6A the rail rear ends spread to 228 (design 220.46),
// 3.8 per side: the channel slope was wrong, not the rail spacing.
// Built on the printed baseline meshes in ../../CM1000_M6_2026-10-28/src/orig (read only).
// Remix of noyoustupid / Jsmaz3 (CC BY-NC-SA): personal use, never redistribute.
// Frame = the baseline 3MF parts: X across (254), Y depth (faceplate front Y=0, rails Y16..137.6), Z height (0..44.45).
// part = "id_F" | "rail_l" | "rail_r"; the faceplate is built by faceplate_freecad.py (same numbers)
part = "rail_l";
id = "CM6C";

joint_x = [22.2, 231.8];   // CM6A x22.6/231.4
joint_z = [5.6, 38.85];    // CM6A z8.6/35.85: toward the top and bottom faces, away from the recut channel
clear_d = 6.6;             // M6 clearance through the 4 mm rail flange (Y16..20)
bay_top = 6;               // bay reach from the joint centre; head 10.5 dia
bay_y   = [20, 54];        // head seat Y20; 34 mm fits a standard 4 mm L-key's short arm

// channel surface: x = tip_x + slope * |z - mid|. Modem wedge 12 long x 22.25 half-height = 0.539, tip about x20.38, so 0.38 clear.
tip_x = 20.0;
slope = 12 / 22.25;
mid   = 44.45 / 2;
over  = 23.5;              // past the rail top and bottom

o = "../../CM1000_M6_2026-10-28/src/orig/";
module engrave(t, p, rot = 0)
    translate(p) rotate([0, 0, rot]) translate([0, 0, -0.5]) linear_extrude(1)
        text(t, size = 4, font = "Liberation Sans:style=Bold", halign = "center", valign = "center");
module ycyl(x, z, d, y0, y1) translate([x, y0, z]) rotate([-90, 0, 0]) cylinder(d = d, h = y1 - y0, $fn = 48);

module channel(y0, y1)     // left end; polygon (x, z) extruded along Y
    translate([0, y1, 0]) rotate([90, 0, 0]) linear_extrude(y1 - y0)
        polygon([[tip_x, mid], [tip_x + slope * over, mid + over], [45, mid + over], [45, mid - over], [tip_x + slope * over, mid - over]]);
module end_mirror(left) if (left) children(); else translate([254, 0, 0]) mirror([1, 0, 0]) children();

module rail(body, x0) difference() {
    import(str(o, "rl_", body, "_normal_part.stl"));
    end_mirror(x0 < 127) channel(15, 140);
    for (z = joint_z) {
        ycyl(x0, z, clear_d, 15, 20.5);
        // open through the top or bottom face: the head reaches within 0.35 of it, too thin to keep
        zlo = z < mid ? -1 : z - bay_top;
        zhi = z < mid ? z + bay_top : 45.5;
        translate([x0 - 9, bay_y[0], zlo]) cube([26, bay_y[1] - bay_y[0], zhi - zlo]);
    }
    engrave(str(id, x0 < 127 ? "-L" : "-R"), [x0 + 1, 95, 44.45], 90);
}
if (part == "id_F") engrave(str(id, "-F"), [127, 7.5, 44.45]);
if (part == "rail_l") rail(1, joint_x[0]);
if (part == "rail_r") rail(6, joint_x[1]);
