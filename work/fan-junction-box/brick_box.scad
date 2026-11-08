// Fan power box that slides onto the GuanTing 12 V brick (DRAFT, viewer only, 2026-11-08).
// Holds 2x Wago 221-413 (12 V, GND) and the brick's screw-terminal socket tip; the brick's
// barrel plug enters through the bottom end wall. Zip-tie anchor outside for the cord bundle.
// Frame: brick prong face at Y=0 (against the strip), X across the brick width, Z along its
// height (Z=0 bottom, prongs near the top). Fit, grip, strength and heat are UNKNOWN.
// Render: snapshot openscad --backend=manifold -D 'part="box"' etc.
include <workshop.scad>
$fn = 48;
part = "box"; // box | lid | brick | contents

// Brick, measured by Brian 2026-11-08 (A..K on brick_measure.svg)
bw = 44; bh = 87; bd = 31;     // A width, B height, C depth
prong_top = 15.5;               // E top edge to prongs
cord_d = 4;                     // UNKNOWN (cord OD), D: leaves the left side, centred
// Socket tip and plug
tip_len = 37.3; tip_barrel = 10; blk_h = 11.75; blk_w = 14.5;  // F, G, H, I
blk_len = 16;                   // UNKNOWN: green block length along the tip
plug_len = 35; plug_d = 9;      // J, K
// Wago 221-413, datasheet
wago = [18.7, 18.6, 8.3];       // width (levers), depth (entry to back), height

cl = 0.3;      // sleeve clearance per side (UNKNOWN fit)
t = 2.4;       // walls
grip = 0.5;    // grip ridge height (0.2 interference)
back_gap = 1.5;// sleeve edges stay this far off the strip face
box_h = 14;    // inside height of the box
lid_t = 2.4;

xo = bw/2 + cl + t;                 // outer half width
yf = bd + cl;                       // inner face of box floor
yb = yf + t;                        // box floor top (inside of box)
yt = yb + box_h;                    // box rim (lid seat)
zt = bh + cl + t;                   // outer top
zi0 = t; zi1 = bh + cl;             // box inside Z range
boss_d = 9;
boss = [for (sx = [-1, 1], z = [zi0 + boss_d/2, zi1 - boss_d/2]) [sx*(xo - t - boss_d/2 + 0.5), z]];
bar_len = tip_len - blk_len;
wago_z1 = zi1 - boss_d - 0.5;       // Wago backs
wago_z0 = wago_z1 - wago[1];        // Wago entries face -Z
notch = [10, 6];                    // output cable notch in the right wall (Z length, depth)
notch_z = (zi0 + bar_len + blk_len + wago_z0)/2;

module rrect(x0, x1, z0, z1, y0, y1, r = 2.5) {
    hull() for (x = [x0 + r, x1 - r], z = [z0 + r, z1 - r]) translate([x, y0, z]) rotate([-90, 0, 0]) cylinder(r = r, h = y1 - y0);
}

module box() {
    difference() {
        union() {
            // sleeve + box shell in one block
            rrect(-xo, xo, 0, zt, back_gap, yt);
            zip_anchor();
        }
        // brick cavity (open back, open bottom)
        translate([-bw/2 - cl, -1, -1]) cube([bw + 2*cl, yf + 1, bh + cl + 1]);
        // box interior
        rrect(-xo + t, xo - t, zi0, zi1, yb, yt + 1, 1);
        // cord slot in the left side wall, open at the bottom
        translate([-xo - 1, bd/2, bh/2]) rotate([0, 90, 0]) cylinder(d = cord_d + 2, h = t + 2);
        translate([-xo - 1, bd/2 - (cord_d + 2)/2, -1]) cube([t + 2, cord_d + 2, bh/2 + 1]);
        // plug hole through the bottom end wall
        translate([0, yb + tip_barrel/2 + 0.5, -1]) cylinder(d = plug_d + 0.6, h = t + 2);
        // output cable notch, right wall
        translate([xo - t - 1, yt - notch[1], notch_z - notch[0]/2]) cube([t + 2, notch[1] + 1, notch[0]]);
    }
    // grip ridges on the sleeve side walls near the back edge
    for (sx = [-1, 1]) translate([sx*(bw/2 + cl) - (sx > 0 ? grip : 0), back_gap + 3, 25]) cube([grip, 1.2, 40]);
    // insert bosses (M3 x 3 x 5: 4.2 bore x 4 deep)
    for (b = boss) translate([b[0], yb - 0.01, b[1]]) difference() {
        rotate([-90, 0, 0]) cylinder(d = boss_d, h = box_h + 0.01);
        translate([0, box_h - 4 + 0.01, 0]) rotate([-90, 0, 0]) ws_insert_bore(ws_insert_m3);
    }
    // socket tip pocket: ribs either side of the barrel at the block's ends
    for (sx = [-1, 1]) {
        translate([sx > 0 ? tip_barrel/2 + 0.4 : -xo + t, yb - 0.01, zi0 + bar_len - 2])
            cube([xo - t - tip_barrel/2 - 0.4 - (sx > 0 ? 0 : 0), 7, 2]);
        translate([sx > 0 ? 3.5 : -blk_w/2 - 1.5, yb - 0.01, zi0 + tip_len + 0.3]) cube([blk_w/2 + 1.5 - 3.5, 8, 2]);
    }
    // Wago stops: back rib and a centre divider
    translate([-2*wago[0]/2 - 1.6, yb - 0.01, wago_z1]) cube([2*wago[0] + 3.2, 5, 0.01 + (zi1 - boss_d) - wago_z1 + 0.5]);
    translate([-0.6, yb - 0.01, wago_z0]) cube([1.2, 5, wago[1]]);
}

module zip_anchor() {
    // bridge on the left outer wall; zip tie runs along Z through it
    difference() {
        translate([-xo - 4.5, yb + 1, 18]) cube([4.5 + 0.01, 10, 8]);
        translate([-xo - 2.5, yb + 3, 17]) cube([2, 6, 10]);
    }
}

module lid() {
    difference() {
        rrect(-xo, xo, 0, zt, yt, yt + lid_t);
        for (b = boss) translate([b[0], yt - 1, b[1]]) rotate([-90, 0, 0]) {
            cylinder(d = 3.4, h = lid_t + 2);
            translate([0, 0, 1 + lid_t - 1.7]) cylinder(d1 = 3.4, d2 = 6.8, h = 1.7 + 0.01);
        }
    }
}

module brick() {
    translate([-bw/2, 0, 0]) rrect(0, bw, 0, bh, 0, bd, 4);
    for (sx = [-1, 1]) translate([sx*6.35 - 0.75, -16, bh - prong_top - 6]) cube([1.5, 16, 6]);
    translate([-bw/2, bd/2, bh/2]) rotate([0, -90, 0]) cylinder(d = cord_d, h = 20);
}

module contents() {
    yb2 = yb + tip_barrel/2 + 0.5;
    // plug body (outside, below the box) and socket tip
    translate([0, yb2, -plug_len + 8]) cylinder(d = plug_d, h = plug_len - 8);
    translate([0, yb2, zi0]) cylinder(d = tip_barrel, h = bar_len);
    translate([-blk_w/2, yb, zi0 + bar_len]) cube([blk_w, blk_h, blk_len]);
    // Wagos, entries facing -Z
    for (sx = [-1, 1]) translate([sx > 0 ? 0.6 : -0.6 - wago[0], yb, wago_z0]) cube([wago[0], wago[2], wago[1]]);
}

if (part == "box") box();
if (part == "lid") lid();
if (part == "brick") brick();
if (part == "contents") contents();
