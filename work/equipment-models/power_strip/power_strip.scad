// The rack's power strip as understood, 2026-11-03. Reference only, never printed.
// X across seen from the front (cord end at -X), Y up, Z out of the front. Back face Z=0, feet behind it.
$fn = 48;

// Listing photo
body = [254, 114.3, 27.94];
key_pitch = 162.05;
// Brian, measured
outlet_pitch = 50; top_to_plug = 8; foot_h = 0.8;
key_big = 9.6; key_slot = 5; key_len = 18;
lip = 2.75; floor_depth = 3.4; // he measured these in a hurry; 0.65 of room behind the lip is in doubt
// Keyholes centred on the strip's height: Brian trusts the listing over his 58
key_y = 0;
// GUESSES read off the listing photo: outlet face size, bottom row margin matching the top,
// middle row contents, feet, room around the slots behind the lip
outlet = [26, 28]; foot = [8, 22]; foot_inset = [10, 10];
under = [14, 24];

module keyhole_2d() {
    circle(d = key_big);
    hull() for (s = [-1, 1]) translate([0, s*(key_len - key_slot)/2]) circle(d = key_slot);
}

module outlet_cut(sideways = false) {
    rotate([0, 0, sideways ? 90 : 0]) translate([0, 0, body[2] - 0.6]) {
        linear_extrude(1) offset(3) square([outlet[0] - 6, outlet[1] - 6], center = true);
        translate([0, 0, -8]) {
            for (s = [-1, 1]) translate([s*6.35, 4, 0]) linear_extrude(9) square([2, s > 0 ? 6.5 : 8], center = true);
            translate([0, -7, 0]) cylinder(d = 5, h = 9);
        }
    }
}

difference() {
    linear_extrude(body[2]) offset(4) square([body[0] - 8, body[1] - 8], center = true);
    row_y = body[1]/2 - top_to_plug - outlet[1]/2;
    for (s = [-1, 1], i = [-2:2]) translate([i*outlet_pitch, s*row_y, 0]) outlet_cut();
    for (x = [-100, -50]) translate([x, 0, 0]) outlet_cut(true);
    // USB ports and switch, rough
    for (x = [25, 40]) translate([x, 0, body[2] - 8]) linear_extrude(9) square([7, 14], center = true);
    for (x = [55, 68]) translate([x, 0, body[2] - 8]) linear_extrude(9) square([12.5, 6], center = true);
    translate([108, 0, body[2] - 0.6]) linear_extrude(1) offset(5) square([8, 24], center = true);
    for (s = [-1, 1]) translate([s*key_pitch/2, key_y, 0]) {
        translate([0, 0, -1]) linear_extrude(lip + 1.01) keyhole_2d();
        translate([0, 0, lip]) linear_extrude(floor_depth - lip) offset(2) square([under[0] - 4, under[1] - 4], center = true);
    }
}
for (sx = [-1, 1], sy = [-1, 1])
    translate([sx*(body[0]/2 - foot_inset[0] - foot[0]/2), sy*(body[1]/2 - foot_inset[1] - foot[1]/2), -foot_h])
        linear_extrude(foot_h + 0.01) offset(3) square([foot[0] - 6, foot[1] - 6], center = true);
// Cord stub at the left end
translate([-body[0]/2 - 25, -30, body[2]/2]) rotate([0, 90, 0]) cylinder(d = 9, h = 25.5);
