// CM1P-T2: second test slice for the one-piece CM1000 bracket. T1 was too tight and its thin strips bowed as the blocks levered apart.
// Changes from T1: flat channel floor for the modem's flat end strip, 1.5 clearance across the width (was 0.4),
// 1.2 on the nose (was 0.7). Same open frame as T1: this print only proves the fit (Brian).
// Brian measured: 212 across the flat ends, 44.4 tall, 14 end wedge, 3 tall at the very front, 44.4 at 15 back.
// ASSUMED: nose a straight taper; flat strip width unmeasured.
// Frame: X across (254 plate), Y depth (plate front Y=0), Z height (0..44.45).
id = "CM1P-T2";

plate_h = 44.45;
mid = plate_h / 2;
rail_x = 16.77;            // outer face of the rails, unchanged: 220.46 across
block_x = 40;
depth = 30;

gap_x = 1.5;               // clearance across the width: deliberately loose, T1 had to be REALLY forced on; measure the play and dial in
flat_w = 8;                // channel floor; modem's flat end strip looks narrower (by eye), extra is safe
tip_x = 127 - 212 / 2 - gap_x;
slope = 14 / (22.2 - flat_w / 2);
over = 23.5;

nose_k = (22.2 - 1.5) / 15;
floor_y = 1.6;             // front wall
floor_h = 2.7;             // modem front face half height 1.5 + 1.2 clearance
far_y = 20;

strip_h = 3.5;
strip_y = 13;

module channel(y0, y1)
    translate([0, y1, 0]) rotate([90, 0, 0]) linear_extrude(y1 - y0)
        polygon([[tip_x, mid - flat_w / 2], [tip_x, mid + flat_w / 2],
                 [tip_x + slope * (over - flat_w / 2), mid + over], [block_x + 5, mid + over],
                 [block_x + 5, mid - over], [tip_x + slope * (over - flat_w / 2), mid - over]]);
module pocket_cut() intersection() {
    channel(floor_y, depth + 1);
    h = floor_h + nose_k * (far_y - floor_y);
    rotate([90, 0, 90]) linear_extrude(block_x + 6)
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
