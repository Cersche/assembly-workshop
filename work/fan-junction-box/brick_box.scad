// Fan power box that snaps onto the GuanTing 12 V brick (DRAFT 2, viewer only, 2026-11-08).
// Holds 2x Wago 221-413 (12 V, GND) and the brick's screw-terminal socket tip; the brick's
// barrel plug enters through the bottom end wall. Zip-tie anchor outside for the cord bundle.
// Frame: strip face at Y=0 (prong block face), X across the brick width, Z up (Z=0 brick bottom).
// The brick is pushed into the cradle from the back; two side lips snap in behind its main
// back face, below the prong block. Fit, snap, grip, strength and heat are UNKNOWN.
include <workshop.scad>
$fn = 48;
part = "box"; // box | lid | brick | contents

// Brick (docs/devices/guanting-12v-brick.md): supplier 45 x 85, Brian's profile 2026-11-08
bw = 45; bh = 85;
body_d = 30;          // outer face to main back face
plinth = 6.25;        // prong block stands out from the main back (P)
plinth_h = 30;        // top edge to bottom of the prong block (Q)
round_r = 15;         // outer face curve at top and bottom (T)
cord_y = plinth + 7.75; // cord centre from the strip face (S from the main back)
cord_d = 4;           // UNKNOWN cord OD
prong_top = 15.5;
dd = plinth + body_d; // 36.25 overall
// Socket tip and plug
tip_len = 37.3; tip_barrel = 10; blk_h = 11.75; blk_w = 14.5;
blk_len = 16;         // UNKNOWN: green block length along the tip
plug_len = 35; plug_d = 9;
wago = [18.7, 18.6, 8.3];

cl = 0.3;             // cradle clearance per side (UNKNOWN fit)
t = 2.4;              // walls
lip_t = 2;            // snap lip thickness (Y)
lip_reach = 1.5;      // how far the lip reaches in behind the back face
lip_z = [3, bh - plinth_h - 3];
box_h = 14; lid_t = 2.4;

xo = bw/2 + cl + t;
y_lip0 = plinth - cl - lip_t;       // shell starts here
yf = dd + cl;                       // inside face of the box floor
yb = yf + t;                        // inside of the box
yt = yb + box_h;                    // lid seat
z0 = -cl - t; z1 = bh + cl + t;     // outer Z
zi0 = 0; zi1 = bh;                  // box inside Z range
boss_d = 9;
boss = [for (sx = [-1, 1], z = [zi0 + boss_d/2, zi1 - boss_d/2]) [sx*(xo - t - boss_d/2 + 0.5), z]];
bar_len = tip_len - blk_len;
wago_z1 = zi1 - boss_d - 0.5;
wago_z0 = wago_z1 - wago[1];
notch = [10, 6];
notch_z = (zi0 + tip_len + wago_z0)/2;

// Brick side profile, 2D: u = Y (from the strip), v = Z
module profile2d() {
    hull() {
        translate([plinth, 0]) square([1, bh]);
        translate([dd - round_r, round_r]) circle(r = round_r);
        translate([dd - round_r, bh - round_r]) circle(r = round_r);
    }
    translate([0, bh - plinth_h]) square([plinth + 1, plinth_h]);
}
module along_x(w) rotate([90, 0, 90]) linear_extrude(w, center = true) children();

module rrect(x0, x1, z0, z1, y0, y1, r = 2.5) {
    hull() for (x = [x0 + r, x1 - r], z = [z0 + r, z1 - r]) translate([x, y0, z]) rotate([-90, 0, 0]) cylinder(r = r, h = y1 - y0);
}

module box() {
    difference() {
        union() {
            intersection() {
                along_x(2*xo) offset(r = cl + t) profile2d();
                translate([-xo - 1, y_lip0, z0 - 1]) cube([2*xo + 2, 100, z1 - z0 + 2]);
            }
            rrect(-xo, xo, z0, z1, dd - 10, yt);
            zip_anchor();
        }
        // brick cavity
        along_x(bw + 2*cl) offset(r = cl) profile2d();
        // open back between the lips
        translate([-(bw/2 + cl - lip_reach), -1, z0 - 1]) cube([bw + 2*cl - 2*lip_reach, plinth + 1, z1 - z0 + 2]);
        // no lips outside lip_z (prong block zone, bottom corner)
        for (zz = [[z0 - 1, lip_z[0]], [lip_z[1], z1 + 1]]) translate([-xo - 1, -1, zz[0]]) cube([2*xo + 2, plinth - cl + 1, zz[1] - zz[0]]);
        // lip lead-in chamfers (brick enters from the back)
        for (sx = [-1, 1]) translate([sx*(bw/2 + cl - lip_reach), y_lip0, lip_z[0] - 1]) rotate([0, 0, sx > 0 ? 0 : 90])
            linear_extrude(lip_z[1] - lip_z[0] + 2) polygon([[0, 0], [lip_reach + 0.01, 0], [0, lip_reach]]);
        // cord slot in the bottom cap, open to the back
        translate([-(cord_d + 1)/2, -1, z0 - 1]) cube([cord_d + 1, cord_y + 1, t + cl + 2]);
        translate([0, cord_y, z0 - 1]) cylinder(d = cord_d + 1, h = t + cl + 2);
        // box interior
        rrect(-xo + t, xo - t, zi0, zi1, yb, yt + 1, 1);
        // plug hole through the bottom end wall
        translate([0, yb + tip_barrel/2 + 0.5, z0 - 1]) cylinder(d = plug_d + 0.6, h = -z0 + 2);
        // output cable notch, right wall
        translate([xo - t - 1, yt - notch[1], notch_z - notch[0]/2]) cube([t + 2, notch[1] + 1, notch[0]]);
    }
    // insert bosses (M3 x 3 x 5: 4.2 bore x 4 deep)
    for (b = boss) translate([b[0], yb - 0.01, b[1]]) difference() {
        rotate([-90, 0, 0]) cylinder(d = boss_d, h = box_h + 0.01);
        translate([0, box_h - 4 + 0.01, 0]) rotate([-90, 0, 0]) ws_insert_bore(ws_insert_m3);
    }
    // socket tip pocket: ribs either side of the barrel at the block's ends
    for (sx = [-1, 1]) {
        translate([sx > 0 ? tip_barrel/2 + 0.4 : -xo + t, yb - 0.01, zi0 + bar_len - 2])
            cube([xo - t - tip_barrel/2 - 0.4, 7, 2]);
        translate([sx > 0 ? 3.5 : -blk_w/2 - 1.5, yb - 0.01, zi0 + tip_len + 0.3]) cube([blk_w/2 + 1.5 - 3.5, 8, 2]);
    }
    // Wago stops: back rib and a centre divider
    translate([-wago[0] - 1.6, yb - 0.01, wago_z1]) cube([2*wago[0] + 3.2, 5, 1]);
    translate([-0.6, yb - 0.01, wago_z0]) cube([1.2, 5, wago[1]]);
}

module zip_anchor() {
    // bridge on the left outer wall of the box; zip tie runs along Z through it
    difference() {
        translate([-xo - 4.5, yb + 1, 18]) cube([4.5 + 0.01, 10, 8]);
        translate([-xo - 2.5, yb + 3, 17]) cube([2, 6, 10]);
    }
}

module lid() {
    difference() {
        rrect(-xo, xo, z0, z1, yt, yt + lid_t);
        for (b = boss) translate([b[0], yt - 1, b[1]]) rotate([-90, 0, 0]) {
            cylinder(d = 3.4, h = lid_t + 2);
            translate([0, 0, 1 + lid_t - 1.7]) cylinder(d1 = 3.4, d2 = 6.8, h = 1.7 + 0.01);
        }
    }
}

module brick() {
    along_x(bw) profile2d();
    for (sx = [-1, 1]) translate([sx*6.35 - 0.75, -16, bh - prong_top - 6]) cube([1.5, 16, 6]);
    translate([0, cord_y, -20]) cylinder(d = cord_d, h = 20);
}

module contents() {
    yb2 = yb + tip_barrel/2 + 0.5;
    translate([0, yb2, -plug_len + 8]) cylinder(d = plug_d, h = plug_len - 8);
    translate([0, yb2, zi0]) cylinder(d = tip_barrel, h = bar_len);
    translate([-blk_w/2, yb, zi0 + bar_len]) cube([blk_w, blk_h, blk_len]);
    for (sx = [-1, 1]) translate([sx > 0 ? 0.6 : -0.6 - wago[0], yb, wago_z0]) cube([wago[0], wago[2], wago[1]]);
}

if (part == "box") box();
if (part == "lid") lid();
if (part == "brick") brick();
if (part == "contents") contents();
