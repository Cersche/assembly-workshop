// PSB-A wall bracket for the power strip and the OptiPlex power brick. Unprinted.
// X across, Y up the wall, Z out of the wall; wall face is Z=0. Strip centre is the origin of the plate.
// Parts lie as they print: plate and cradle wall side down, hanger cap down, hoop on its side.
part = "plate"; // plate, hanger, cradle, hoop, strip_dummy, brick_dummy
$fn = 64;

// Brian's measurements, 2026-11-03
outlet_pitch = 50;
key_big = 9.6; key_slot = 5; key_len = 18;
brick = [155, 76.5, 24];
// From the listing photo
strip = [254, 114.3, 27.94];
key_pitch = 162.05;
// ASSUMED until measured: lip the hanger hooks behind, room behind the lip, foot height,
// keyholes level with the strip's middle, outlets centred across the strip
key_lip = 2; key_pocket = 3.5; strip_foot = 1.5;

neck_d = 4.6; cap_d = 9; cap_h = 3;
neck_h = key_lip + 0.6;
assert(cap_h <= key_pocket - 0.25, "hanger cap taller than the room behind the lip");
assert(cap_d <= key_big - 0.4 && neck_d <= key_slot - 0.3);
stud_y = key_len/2 - key_slot/2 + (key_slot - neck_d)/2; // neck resting at the top of the upper slot

plate_t = 5; boss_h = 2; boss_d = 12;
assert(boss_h > strip_foot);
sp_core = 26; sp_flange = 40; sp_channel = 14; sp_rim = 1.5;
lift_room = key_len/2 - key_slot/2 + 1.5; // strip goes on this far up, then drops onto the hangers
sp_y = strip[1]/2 + lift_room + sp_flange/2;
plate_w = 250; plate_r = 6;
plate_h = 2*(sp_y + sp_flange/2 + 4);
assert(plate_w <= 256 && plate_h <= 256);
assert(sp_flange < outlet_pitch);

insert_d = 4.2; insert_deep = 4; screw_pilot = 3.2;
screw_d = 3.4; csk_d = 6.4; csk_h = 1.9;
wall_d = 4.6; wall_head = 9.4; wall_csk = 2.6;

module rrect(w, h, r) { offset(r) square([w - 2*r, h - 2*r], center = true); }

// Core, 45 degree flange underside so it prints with no support, then a thin rim
module spool(base) {
    translate([0, 0, base]) {
        cylinder(d = sp_core, h = sp_channel);
        translate([0, 0, sp_channel]) cylinder(d1 = sp_core, d2 = sp_flange, h = (sp_flange - sp_core)/2);
        translate([0, 0, sp_channel + (sp_flange - sp_core)/2]) cylinder(d = sp_flange, h = sp_rim);
    }
}

module wall_hole(t) {
    translate([0, 0, -1]) cylinder(d = wall_d, h = t + 2);
    translate([0, 0, t - wall_csk]) cylinder(d1 = wall_d, d2 = wall_head, h = wall_csk + 0.01);
    translate([0, 0, t]) cylinder(d = wall_head, h = 3);
}

module insert_bore(top) {
    translate([0, 0, top - insert_deep]) cylinder(d = insert_d, h = insert_deep + 1);
    translate([0, 0, top - insert_deep - 1]) cylinder(d = screw_pilot, h = 1.01);
}

module id_text(s, size = 6, depth = 0.6, top = plate_t) {
    translate([0, 0, top - depth]) linear_extrude(depth + 1) text(s, size = size, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");
}

module plate() {
    difference() {
        union() {
            difference() {
                linear_extrude(plate_t) rrect(plate_w, plate_h, plate_r);
                // Openings behind the strip; a bar stays for the two hangers
                for (y = [[stud_y + 14, strip[1]/2 - 3], [-strip[1]/2 + 3, stud_y - 14]])
                    translate([-108, y[0], -1]) cube([216, y[1] - y[0], plate_t + 2]);
            }
            for (s = [-1, 1]) translate([s*key_pitch/2, stud_y, 0]) cylinder(d = boss_d, h = plate_t + boss_h);
            for (s = [-1, 1], i = [-2:2]) translate([i*outlet_pitch, s*sp_y, 0]) spool(plate_t);
        }
        for (s = [-1, 1]) translate([s*key_pitch/2, stud_y, 0]) insert_bore(plate_t + boss_h);
        for (s = [-1, 1], x = [-75, -25, 25, 75]) translate([x, s*(sp_y + 13), 0]) wall_hole(plate_t);
        translate([0, stud_y, 0]) id_text("PSB-A");
    }
}

// Goes through the wide part of the keyhole and carries the strip; an M3 countersunk screw clamps it down
module hanger() {
    difference() {
        union() {
            cylinder(d = cap_d, h = cap_h);
            cylinder(d = neck_d, h = cap_h + neck_h);
        }
        translate([0, 0, -1]) cylinder(d = screw_d, h = cap_h + neck_h + 2);
        translate([0, 0, -0.01]) cylinder(d1 = csk_d, d2 = screw_d, h = csk_h);
    }
}

br_clear = 0.5; hoop_w = 14; hoop_t = 4; hoop_foot = 14; cr_t = 6;
hoop_in_y = brick[1] + 2*br_clear; hoop_in_z = brick[2] + 0.5;
hoop_screw_y = hoop_in_y/2 + hoop_t + hoop_foot/2;
hoop_x = 45;
cr_w = brick[0] + 2*br_clear + 2*4 + 8;
cr_sp_y = -(hoop_screw_y + hoop_foot/2 + 2 + sp_flange/2);
cr_top = hoop_screw_y + hoop_foot/2 + 3;
cr_bot = cr_sp_y - sp_flange/2 - 6;
assert(cr_w <= 256 && cr_top - cr_bot <= 256);

module cradle() {
    stop_x = brick[0]/2 + br_clear;
    difference() {
        union() {
            difference() {
                translate([-cr_w/2, cr_bot, 0]) linear_extrude(cr_t)
                    translate([cr_w/2, (cr_top - cr_bot)/2]) rrect(cr_w, cr_top - cr_bot, plate_r);
                // Air behind the brick
                translate([-65, -28, -1]) cube([130, 56, cr_t + 2]);
            }
            // End stops, open in the middle for the cords
            for (sx = [-1, 1], sy = [-1, 1])
                translate([sx > 0 ? stop_x : -stop_x - 4, sy > 0 ? 12 : -brick[1]/2, 0]) cube([4, brick[1]/2 - 12, cr_t + 10]);
            for (s = [-1, 1]) translate([s*hoop_x, cr_sp_y, 0]) spool(cr_t);
        }
        for (sx = [-1, 1], sy = [-1, 1]) translate([sx*hoop_x, sy*hoop_screw_y, 0]) insert_bore(cr_t);
        for (x = [-78, 0, 78]) translate([x, cr_bot + 8, 0]) wall_hole(cr_t);
        for (s = [-1, 1]) translate([s*78, cr_top - 8, 0]) wall_hole(cr_t);
        translate([0, cr_top - 7, 0]) id_text("PSB-A", top = cr_t);
    }
}

// Printed on its side: the layers follow the U. Drawn as it prints, profile in XY, width in Z.
module hoop() {
    a = hoop_in_y/2; b = hoop_in_z; t = hoop_t; f = hoop_foot;
    difference() {
        linear_extrude(hoop_w) polygon([
            [-a - t - f, 0], [-a, 0], [-a, b], [a, b], [a, 0], [a + t + f, 0],
            [a + t + f, t], [a + t, t], [a + t, b + t], [-a - t, b + t], [-a - t, t], [-a - t - f, t]]);
        for (s = [-1, 1]) translate([s*(a + t + f/2), 0, hoop_w/2]) rotate([-90, 0, 0]) {
            translate([0, 0, -1]) cylinder(d = screw_d, h = t + 2);
            translate([0, 0, t - csk_h]) cylinder(d1 = screw_d, d2 = csk_d, h = csk_h + 0.01);
        }
        translate([0, b + t - 0.6, hoop_w/2]) rotate([-90, 0, 0]) linear_extrude(2)
            text("PSB-A", size = 6, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");
    }
}

// Viewer only, never printed: where the real things sit against the plate and cradle
module strip_dummy() {
    z = plate_t + boss_h;
    difference() {
        translate([-strip[0]/2, -strip[1]/2, z]) cube([strip[0], strip[1], strip[2]]);
        for (s = [-1, 1]) translate([s*key_pitch/2, 0, z - 1]) {
            cylinder(d = key_big, h = 4);
            hull() for (d = [-1, 1]) translate([0, d*(key_len - key_slot)/2, 0]) cylinder(d = key_slot, h = 4);
        }
    }
}
module brick_dummy() { translate([-brick[0]/2, -brick[1]/2, cr_t]) cube(brick); }

// Viewer only: everything where it goes, cradle to the right of the plate
asm_cr_x = plate_w/2 + cr_w/2 + 15;
if (part == "asm_hangers") for (s = [-1, 1])
    translate([s*key_pitch/2, stud_y, plate_t + boss_h + cap_h + neck_h]) rotate([180, 0, 0]) hanger();
if (part == "asm_cradle") translate([asm_cr_x, 0, 0]) cradle();
if (part == "asm_brick") translate([asm_cr_x, 0, 0]) brick_dummy();
if (part == "asm_hoops") for (s = [-1, 1])
    translate([asm_cr_x + s*hoop_x - hoop_w/2, 0, cr_t]) rotate([90, 0, 90]) hoop();

if (part == "plate") plate();
if (part == "hanger") hanger();
if (part == "cradle") cradle();
if (part == "hoop") hoop();
if (part == "strip_dummy") strip_dummy();
if (part == "brick_dummy") brick_dummy();
