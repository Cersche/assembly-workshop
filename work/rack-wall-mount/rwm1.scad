// Lab Rax 9U rack wall mount, first build (Brian picked "top French cleat + bottom standoffs", 2026-10-30).
// Our own geometry only; no Lab Rax creator mesh is used or exported.
//
// Frame (assembly): X across the rack, 0 = rack centre. Z up, 0 = bottom of slot U1 (post stack bottom),
// 44.45 per U. Y = 0 is the rack's rear face (rear post faces); +Y points to the wall; the wall is Y = wall_y.
// Rear post insert holes: X +/-118.26 (same as front, see the 1U support extension), Z = U centre +/-15.9 and 0.
//
// part: "bar" rack cleat RW-RC-A, "rail" wall rail RW-WP-A, "standoff" RW-SO-A (right side; left = same part
// turned upside down), "assembly" all seated, "none".
// print=true puts the chosen part in print orientation (min Z = 0).
part  = "assembly";
print = false;
lift  = 0;     // assembly: rack parts raised by this (clash sweeps)
pull  = 0;     // assembly: rack parts moved away from the wall by this
$fn = 48;

pitch   = 44.45;
hole_x  = 118.26;
half_w  = 141;           // rack outer half width (post outer faces)
wall_y  = 30;            // rack rear face to wall = cable gap
plate_t = 5;             // wall rail plate thickness
cleat_d = 8;             // cleat depth (Y)
cl_y0   = wall_y - plate_t - cleat_d;   // 17: cleat front face
cl_y1   = wall_y - plate_t;             // 25: cleat back / plate front face
slope_z = 380;           // cleat top at its front face; 45 deg down towards the wall
tip_gap = 0.5;           // hook tip clear of the plate face
hook_y1 = cl_y1 - tip_gap;
bar_y1  = cl_y0 - 0.5;    // bar body face, 0.5 clear of the cleat front
flange  = 3.5;           // material under the M6 x 8 button heads
m6_d = 6.8; m6_cb = 12;
lock_x = 60; lock_y = 21;

function ucz(u) = (u - 0.5) * pitch;
bar_z0 = 350; bar_zm = 368; bar_z1 = 408; bar_end = 104;
so_x0 = 104; so_z0 = ucz(1) - 32; so_z1 = ucz(1) + 32;
rail_z0 = 336; rail_z1 = 412; cl_z0 = 356;
row_z = [344, 400]; row_x = [for (i = [-5:5]) i * 25];

module m6_hole(x, z, y_end) {      // clearance through the flange, counterbore from the wall side
    translate([x, -1, z]) rotate([-90, 0, 0]) cylinder(d = m6_d, h = flange + 1.01);
    translate([x, flange, z]) rotate([-90, 0, 0]) cylinder(d = m6_cb, h = y_end - flange + 1);
}

// region above the 45 deg slope z = slope_z - (y - cl_y0), y in [ya, yb]
module above_slope(ya, yb, ztop, xw) {
    translate([-xw, 0, 0]) rotate([90, 0, 90]) linear_extrude(2 * xw)
        polygon([[ya, slope_z - (ya - cl_y0)], [yb, slope_z - (yb - cl_y0)], [yb, ztop], [ya, ztop]]);
}
module below_slope(ya, yb, zbot, xw) {
    translate([-xw, 0, 0]) rotate([90, 0, 90]) linear_extrude(2 * xw)
        polygon([[ya, zbot], [yb, zbot], [yb, slope_z - (yb - cl_y0)], [ya, slope_z - (ya - cl_y0)]]);
}

module bar() {
    difference() {
        union() {
            for (s = [-1, 1]) translate([s > 0 ? bar_end : -half_w, 0, bar_z0]) cube([half_w - bar_end, bar_y1, bar_z1 - bar_z0]);
            translate([-half_w, 0, bar_zm]) cube([2 * half_w, bar_y1, bar_z1 - bar_zm]);
            above_slope(bar_y1 - 0.01, hook_y1, bar_z1, half_w);
        }
        for (s = [-1, 1], z = [ucz(9) - 15.9, ucz(9) + 15.9]) m6_hole(s * hole_x, z, hook_y1 + 1);
        for (s = [-1, 1]) translate([s * lock_x, lock_y, 360]) cylinder(d = 3.4, h = 60);
        // centre V notch on the top face, ID on the top face
        translate([0, -1, bar_z1]) rotate([-90, 0, 0]) linear_extrude(cl_y0 + 2) polygon([[-3, 0.01], [3, 0.01], [0, 3]]);
        translate([-35, 8.5, bar_z1 - 0.6]) linear_extrude(1) text("RW-RC-A", size = 6, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");
        translate([35, 8.5, bar_z1 - 0.6]) linear_extrude(1) text("TOP", size = 6, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");
    }
}

module countersink(x, z) {     // #8 / 4 mm wood screw, head 1 mm below the room-side face
    translate([x, cl_y1 - 1, z]) rotate([-90, 0, 0]) cylinder(d = 4.5, h = plate_t + 2);
    translate([x, cl_y1 - 1, z]) rotate([-90, 0, 0]) cylinder(d = 9.2, h = 2.01);
    translate([x, cl_y1 + 1, z]) rotate([-90, 0, 0]) cylinder(d1 = 9.2, d2 = 4.5, h = 2.35);
}

module rail() {
    difference() {
        union() {
            translate([-half_w, cl_y1, rail_z0]) cube([2 * half_w, plate_t, rail_z1 - rail_z0]);
            below_slope(cl_y0, cl_y1 + 0.01, cl_z0, half_w);
        }
        for (z = row_z, x = row_x) countersink(x, z);
        for (s = [-1, 1]) translate([s * lock_x, lock_y, slope_z - (lock_y - cl_y0) - 10]) cylinder(d = 2.5, h = 20);
        // V notches: centre on the top edge, level line (top screw row) on both ends
        translate([0, cl_y1 - 1, rail_z1]) rotate([-90, 0, 0]) linear_extrude(plate_t + 2) polygon([[-3, -0.01], [3, -0.01], [0, 4]]);
        for (s = [-1, 1]) translate([s * half_w, cl_y1 - 1, row_z[1]]) rotate([-90, 0, 0])
            linear_extrude(plate_t + 2) polygon([[0, -3], [0, 3], [-s * 4, 0]]);
        // ID on the cleat's front face (faces the room, hidden behind the rack bar when hung)
        translate([0, cl_y0 + 0.6, (cl_z0 + slope_z) / 2 - 2]) rotate([90, 0, 0])
            linear_extrude(1) text("TOP  RW-WP-A", size = 7, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");
    }
}

module standoff() {   // right side; the left one is the same part turned upside down
    difference() {
        translate([so_x0, 0, so_z0]) cube([half_w - so_x0, wall_y, so_z1 - so_z0]);
        for (z = [ucz(1) - 15.9, ucz(1) + 15.9]) m6_hole(hole_x, z, wall_y + 1);
        translate([half_w - 0.6, wall_y / 2, ucz(1)]) rotate([90, 0, 90])
            linear_extrude(1) text("RW-SO-A", size = 5, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");
    }
}
module standoff_left() { translate([0, 0, 2 * ucz(1)]) rotate([0, 180, 0]) standoff(); }

module rack_side() { translate([0, -pull, lift]) { bar(); standoff(); standoff_left(); } }

if (part == "assembly") { rack_side(); rail(); }
else if (part == "bar")      { if (print) rotate([90, 0, 0]) bar(); else bar(); }
else if (part == "rail")     { if (print) translate([0, 0, wall_y]) rotate([-90, 0, 0]) rail(); else rail(); }
else if (part == "standoff") { if (print) rotate([90, 0, 0]) standoff(); else standoff(); }
else if (part == "clash_seated") intersection() { rack_side(); rail(); }
