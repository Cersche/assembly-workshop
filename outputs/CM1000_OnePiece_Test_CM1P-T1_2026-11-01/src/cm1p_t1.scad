// CM1P-T1: test slice for the one-piece CM1000 bracket. Press it onto the front of the modem from behind.
// Same pocket and channels as the planned one-piece part, at true spacing, only the ends plus two tie strips.
// Brian measured (2026-11-01): 212 tip to tip, 44.4 tall, 14 end wedge, 3 tall at the very front, 44.4 at 15 back, 136 deep.
// Assumed: end tip pointed and centred; nose a straight taper reaching full height 15 back.
// Frame: X across (254 plate), Y depth (plate front Y=0), Z height (0..44.45).
id = "CM1P-T1";

plate_h = 44.45;
mid = plate_h / 2;
rail_x = 16.77;            // outer face of the rails, unchanged: 220.46 across
block_x = 40;              // end blocks stop here
depth = 30;                // 14 of channel behind the pocket rim

// channel: x = tip_x + slope * |z - mid|
gap_x = 0.4;               // clearance across the width
tip_x = 127 - 212 / 2 - gap_x;
slope = 14 / 22.2;
over = 23.5;

// pocket: half height vs Y, modem nose + clearance
nose_k = (22.2 - 1.5) / 15;
floor_y = 1.6;             // front wall
floor_h = 2.2;             // modem front face half height 1.5 + 0.7 clearance
far_y = 20;

strip_h = 3.5;             // ties: along the outer faces, from the bed up, in the taper's spare room
strip_y = 13;

module channel(y0, y1)
    translate([0, y1, 0]) rotate([90, 0, 0]) linear_extrude(y1 - y0)
        polygon([[tip_x, mid], [tip_x + slope * over, mid + over], [block_x + 5, mid + over], [block_x + 5, mid - over], [tip_x + slope * over, mid - over]]);
module pocket_cut() intersection() {
    channel(floor_y, depth + 1);
    h = floor_h + nose_k * (far_y - floor_y);
    translate([0, 0, 0]) rotate([90, 0, 90]) linear_extrude(block_x + 6)
        polygon([[floor_y, mid - floor_h], [floor_y, mid + floor_h], [far_y, mid + h], [depth + 2, mid + h], [depth + 2, mid - h], [far_y, mid - h]]);
}
module end_block() difference() {
    translate([rail_x, 0, 0]) cube([block_x - rail_x, depth, plate_h]);
    pocket_cut();
}
module strip(z) translate([rail_x, 0, z]) cube([254 - 2 * rail_x, strip_y, strip_h]);

difference() {
    union() {
        end_block();
        translate([254, 0, 0]) mirror([1, 0, 0]) end_block();
        strip(0);
        strip(plate_h - strip_h);
    }
    translate([127, strip_y / 2, plate_h - 0.5]) linear_extrude(1)
        text(id, size = 5, font = "Liberation Sans:style=Bold", halign = "center", valign = "center");
}
