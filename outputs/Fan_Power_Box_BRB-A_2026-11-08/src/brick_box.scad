// Fan power box on the GuanTing 12 V brick (BRB-A, released for Brian's print 2026-11-08; was draft 6). Two pieces (Brian):
// the SLEEVE snaps onto the brick; the junction BOX (2x Wago 221-413 + the brick's screw-terminal
// socket tip, wired first) slides down onto a dovetail rail on the sleeve and is locked by one M3
// countersunk screw into an M3 heat-set insert in the rail. The brick's barrel plug enters through
// the box's bottom end wall. Zip-tie slot pairs centred on the sleeve's left, right and top faces.
// Frame: strip face at Y=0 (prong block face), X across the brick width, Z up (Z=0 brick bottom).
// The brick is pushed into the cradle from the back; two side lips snap in behind its main
// back face, below the prong block. Fit, snap, grip, strength and heat are UNKNOWN.
include <workshop.scad>
$fn = 48;
part = "box"; // sleeve | box | lid | brick | contents | measure | keepout

// Brick (docs/devices/guanting-12v-brick.md): supplier 45 x 85, Brian's profile 2026-11-08
bw = 45; bh = 85;
body_d = 30;          // outer face to main back face
plinth = 6.25;        // prong block stands out from the main back (P)
plinth_h = 30;        // top edge to bottom of the prong block (Q)
plinth_top = 10;      // prong block starts 10 below the top edge (Brian, viewer check)
plan_r = 10;          // label-face side edges, seen from above (Brian, viewer check)
round_r = 15;         // outer face curve at the bottom: 15 up the face x 15 along the bottom
top_rz = 18; top_ry = 15; // top curve: 18 down the face x 15 along the top (Brian, 3D measure page)
front_r = 16;         // corner radius seen from the label face
plinth_w = 29;        // prong block width, centred; its outer corners r 4 seen from above
plinth_r = 4;
cord_y = plinth + 7.75; // cord centre from the strip face (S from the main back)
cord_d = 4;           // cord OD (measured)
boot_d = 10; boot_len = 13; // strain-relief boot at the brick bottom
prong_top = 15.5;
dd = plinth + body_d; // 36.25 overall
// Socket tip and plug
tip_len = 37.3; tip_barrel = 10; blk_h = 11.75; blk_w = 14.5;
blk_len = 13.55;      // green block length along the tip (measured)
plug_len = 35; plug_d = 9;
wago = [18.7, 18.6, 8.3];

cl = 0.3;             // cradle clearance per side on the main flats (UNKNOWN fit)
loose = 4;            // cavity curves use radii 4 smaller, so grip comes from the flats, not the curves
t = 2.4;              // walls
lip_t = 2;            // snap lip thickness (Y)
lip_reach = 1.5;      // how far the lip reaches in behind the back face
lip_z = [front_r + 2, bh - front_r - 2]; // straight part of the sides; ribs are cosmetic
box_h = 14; lid_t = 2.4;
// Zip-tie slots (Brian, draft 4): a slot pair in the middle of the left, right and top faces
tie_w = 5;            // slot length (fits ties up to ~4.8 wide)
tie_t = 1.8;          // slot width / tunnel height (ties ~1.2 thick)
tie_gap = 10;         // slot centre to centre
tie_groove = 1.4;     // flush slots (Brian, draft 6): the tunnel is a groove in the cavity side, the brick closes it

xo = bw/2 + cl + t;
y_lip0 = plinth - cl - lip_t;       // shell starts here
yf = dd + cl;                       // sleeve: inside face of its front plate
ys = yf + t;                        // sleeve front plate outer face = split face
// Dovetail rail (on the sleeve, along Z) and the box floor groove; box slides down from the top
rail_h = 2.5; rail_base = 12; rail_top = 16; // rail narrow at the plate, wide at its face
dv_cl = 0.25;                       // groove clearance per face (UNKNOWN fit)
box_floor = 4;                      // box floor; groove 2.75 deep leaves 1.25
yb = ys + box_floor;                // inside of the box
yt = yb + box_h;                    // lid seat
z0 = -cl - t; z1 = bh + cl + t;     // outer Z
zi0 = 0; zi1 = bh;                  // box inside Z range
boss_d = 9;
boss = [for (sx = [-1, 1], z = [zi0 + boss_d/2, zi1 - boss_d/2]) [sx*(xo - t - boss_d/2 + 0.5), z]];
bar_len = tip_len - blk_len;
rail_z0 = z0 + 4;                   // rail bottom = box stop (box floor closed below the groove)
lock_z = zi1 - boss_d/2;            // lock screw between the two top lid bosses, above the Wagos
wago_z1 = zi1 - boss_d - 0.5;
wago_z0 = wago_z1 - wago[1];
notch = [10, 6];
notch_z = (zi0 + tip_len + wago_z0)/2;

// Brick side profile, 2D: u = Y (from the strip), v = Z
module profile2d(k = 0) {   // body only, no prong block; k shrinks the curve radii
    hull() {
        translate([plinth, 0]) square([1, bh]);
        translate([dd - round_r + k, round_r - k]) circle(r = round_r - k);
        translate([dd - top_ry + k, bh - top_rz + k]) scale([top_ry - k, top_rz - k]) circle(r = 1, $fn = 64);
    }
}
// Front view outline (X, Z), r 16 corners
module front2d(k = 0) {
    r = front_r - k;
    hull() for (x = [-bw/2 + r, bw/2 - r], z = [r, bh - r]) translate([x, z]) circle(r = r);
}
module along_x(w) rotate([90, 0, 90]) linear_extrude(w, center = true) children();
module along_y(y0, y1) translate([0, y1, 0]) rotate([90, 0, 0]) linear_extrude(y1 - y0) children();
// Plan view (X, Y): r 10 where the sides meet the label face, square at the back
module plan2d(k = 0) {
    r = plan_r - k;
    hull() {
        translate([-bw/2, plinth]) square([bw, 1]);
        for (x = [-bw/2 + r, bw/2 - r]) translate([x, dd - r]) circle(r = r);
    }
}
// Brick body grown by off: side profile x front outline x plan outline
module body3d(off, k = 0) intersection() {
    along_x(bw + 2*off + 2) offset(r = off) profile2d(k);
    along_y(-30, dd + off + 1) offset(r = off) front2d(k);
    translate([0, 0, -off - 1]) linear_extrude(bh + 2*off + 2) offset(r = off) union() { plan2d(k); translate([-bw/2, -30]) square([bw, plinth + 31]); }
}

module rrect(x0, x1, z0, z1, y0, y1, r = 2.5) {
    hull() for (x = [x0 + r, x1 - r], z = [z0 + r, z1 - r]) translate([x, y0, z]) rotate([-90, 0, 0]) cylinder(r = r, h = y1 - y0);
}

module rail2d(c = 0) offset(delta = c) polygon([[-rail_base/2, ys - 1], [rail_base/2, ys - 1], [rail_base/2, ys], [rail_top/2, ys + rail_h], [-rail_top/2, ys + rail_h], [-rail_base/2, ys]]);

// Part IDs engraved 0.6 deep. m = rows of [text x, text y, outward] in the brick frame.
module id_cut(id, pos, m) translate(pos) multmatrix([[m[0][0], m[0][1], m[0][2], 0], [m[1][0], m[1][1], m[1][2], 0], [m[2][0], m[2][1], m[2][2], 0]])
    translate([0, 0, -0.6]) linear_extrude(2) text(id, size = 4, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");

module sleeve() {
    difference() {
        union() {
            intersection() {
                body3d(cl + t, loose);
                translate([-xo - 1, y_lip0, z0 - 1]) cube([2*xo + 2, 100, z1 - z0 + 2]);
            }
            rrect(-xo, xo, z0, z1, dd - 10, ys, 6);
            // dovetail rail
            translate([0, 0, rail_z0]) linear_extrude(z1 - rail_z0) rail2d();
        }
        // brick cavity
        body3d(cl, loose);
        // open back between the lips
        translate([-(bw/2 + cl - lip_reach), -1, z0 - 1]) cube([bw + 2*cl - 2*lip_reach, plinth + 1, z1 - z0 + 2]);
        // no lips outside lip_z (prong block zone, bottom corner)
        for (zz = [[z0 - 1, lip_z[0]], [lip_z[1], z1 + 1]]) translate([-xo - 1, -1, zz[0]]) cube([2*xo + 2, plinth - cl + 1, zz[1] - zz[0]]);
        // lip lead-in chamfers (brick enters from the back)
        for (sx = [-1, 1]) translate([sx*(bw/2 + cl - lip_reach), y_lip0, lip_z[0] - 1]) rotate([0, 0, sx > 0 ? 0 : 90])
            linear_extrude(lip_z[1] - lip_z[0] + 2) polygon([[0, 0], [lip_reach + 0.01, 0], [0, lip_reach]]);
        // cord slot in the bottom cap, open to the back
        translate([-(boot_d + 1)/2, -1, z0 - 1]) cube([boot_d + 1, cord_y + 1, t + cl + 2]);
        translate([0, cord_y, z0 - 1]) cylinder(d = boot_d + 1, h = t + cl + 2);
        tie_faces() tie_cut();
        id_cut("BRB-A-S", [xo, y_mid, 26], [[0, 0, 1], [0, -1, 0], [1, 0, 0]]); // right face, reads along Z
        // lock screw insert in the rail (M3 x 3 x 5: 4.2 x 4) + screw tip clearance
        translate([0, ys + rail_h + 0.01, lock_z]) rotate([90, 0, 0]) { ws_insert_bore(ws_insert_m3); cylinder(d = 3.2, h = 6.5); }
    }
}

module box() {
    difference() {
        rrect(-xo, xo, z0, z1, ys, yt, 6);
        // dovetail groove, open at the top, closed below rail_z0 (stop)
        translate([0, 0, rail_z0 - dv_cl]) linear_extrude(z1 - rail_z0 + dv_cl + 1) rail2d(dv_cl);
        // box interior
        rrect(-xo + t, xo - t, zi0, zi1, yb, yt + 1, 3.6);
        // plug hole through the bottom end wall
        translate([0, yb + tip_barrel/2 + 0.5, z0 - 1]) cylinder(d = plug_d + 0.6, h = -z0 + 2);
        // output cable notch, right wall
        translate([xo - t - 1, yt - notch[1], notch_z - notch[0]/2]) cube([t + 2, notch[1] + 1, notch[0]]);
        id_cut("BRB-A-B", [-xo, (ys + yt)/2, bh/2], [[0, 0, -1], [0, 1, 0], [1, 0, 0]]); // left face
    }
    // insert bosses for the lid (M3 x 3 x 5: 4.2 bore x 4 deep)
    for (b = boss) translate([b[0], yb - 0.01, b[1]]) difference() {
        rotate([-90, 0, 0]) cylinder(d = boss_d, h = box_h + 0.01);
        translate([0, box_h - 4 + 0.01, 0]) rotate([-90, 0, 0]) ws_insert_bore(ws_insert_m3);
    }
    // lock screw boss: M3 countersunk from inside the box into the rail insert (M3 x 8 assumed)
    translate([0, yb - 0.01, lock_z]) difference() {
        rotate([-90, 0, 0]) cylinder(d = boss_d, h = 2.4);
        translate([0, -box_floor - 1, 0]) rotate([-90, 0, 0]) cylinder(d = 3.4, h = 10);
        translate([0, 2.4 - 1.7 + 0.02, 0]) rotate([-90, 0, 0]) cylinder(d1 = 3.4, d2 = 6.8, h = 1.7);
    }
    // socket tip pocket: ribs either side of the barrel at the block's ends
    for (sx = [-1, 1]) {
        translate([sx > 0 ? tip_barrel/2 + 0.4 : -xo + t, yb - 0.01, zi0 + bar_len - 2])
            cube([xo - t - tip_barrel/2 - 0.4, 7, 2]);
        translate([sx > 0 ? 3.5 : -blk_w/2 - 1.5, yb - 0.01, zi0 + tip_len + 0.3]) cube([blk_w/2 + 1.5 - 3.5, 8, 2]);
    }
    // Wago stops: back rib (gap in the middle keeps the lock screw head clear) and a centre divider
    for (sx = [-1, 1]) translate([sx > 0 ? 5 : -wago[0] - 1.6, yb - 0.01, wago_z1]) cube([wago[0] + 1.6 - 5, 5, 1]);
    translate([-0.6, yb - 0.01, wago_z0]) cube([1.2, 5, wago[1]]);
}

// Zip-tie slots, local frame: u = along the slot spacing, v = along the slot, w = outward (outer face at w = 0)
y_mid = (y_lip0 + ys)/2;             // centre of the sleeve's side/top faces
module tie_faces() {
    translate([xo, y_mid, bh/2]) multmatrix([[0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]]) children();   // right
    translate([-xo, y_mid, bh/2]) multmatrix([[0, 0, -1, 0], [1, 0, 0, 0], [0, 1, 0, 0]]) children(); // left
    translate([0, y_mid, z1]) multmatrix([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 0]]) children();     // top
}
module tie_cut() {
    // two flush slots through the wall into a groove on the cavity side; the tie passes between
    // the groove roof (t - tie_groove = 1.0 bridge) and the brick (+ cl)
    translate([-tie_gap/2 - tie_t/2, -tie_w/2, -t - 1]) cube([tie_gap + tie_t, tie_w, tie_groove + 1]);
    for (u = [-1, 1]) translate([u*tie_gap/2 - tie_t/2, -tie_w/2, -t - 1]) cube([tie_t, tie_w, t + 2]);
}

module lid() {
    difference() {
        rrect(-xo, xo, z0, z1, yt, yt + lid_t, 6);
        for (b = boss) translate([b[0], yt - 1, b[1]]) rotate([-90, 0, 0]) {
            cylinder(d = 3.4, h = lid_t + 2);
            translate([0, 0, 1 + lid_t - 1.7]) cylinder(d1 = 3.4, d2 = 6.8, h = 1.7 + 0.01);
        }
        id_cut("BRB-A-L", [0, yt + lid_t, bh/2], [[-1, 0, 0], [0, 0, 1], [0, 1, 0]]);
    }
}

module brick() {
    body3d(0);
    // prong block: 29 wide, r 4 outer corners seen from above, clipped by the front outline
    intersection() {
        hull() for (x = [-plinth_w/2 + plinth_r, plinth_w/2 - plinth_r]) {
            translate([x, plinth_r, bh - plinth_h]) cylinder(r = plinth_r, h = plinth_h - plinth_top);
            translate([x - plinth_r, plinth, bh - plinth_h]) cube([2*plinth_r, 1, plinth_h - plinth_top]);
        }
        along_y(-1, plinth + 2) front2d();
    }
    // US blades (NEMA 1-15, standard): 12.7 apart, 6.35 tall, 1.5 thick, 16 long
    for (sx = [-1, 1]) translate([sx*6.35 - 0.75, -16, bh - prong_top - 6.35]) cube([1.5, 16, 6.35]);
    translate([0, cord_y, -boot_len]) cylinder(d1 = 6, d2 = boot_d, h = boot_len);
    translate([0, cord_y, -boot_len - 20]) cylinder(d = cord_d, h = 20);
}

module contents() {
    yb2 = yb + tip_barrel/2 + 0.5;
    translate([0, yb2, -plug_len + 8]) cylinder(d = plug_d, h = plug_len - 8);
    translate([0, yb2, zi0]) cylinder(d = tip_barrel, h = bar_len);
    translate([-blk_w/2, yb, zi0 + bar_len]) cube([blk_w, blk_h, blk_len]);
    for (sx = [-1, 1]) translate([sx > 0 ? 0.6 : -0.6 - wago[0], yb, wago_z0]) cube([wago[0], wago[2], wago[1]]);
}

if (part == "sleeve") sleeve();
// Screw head room (check only): lock screw head inside the box, lid screw heads outside the lid
if (part == "keepout") {
    ws_head_keepout(0, yb + 2.4, lock_z, 6.8);
    for (b = boss) ws_head_keepout(b[0], yt + lid_t, b[1], 6.8);
}
if (part == "box") box();
if (part == "lid") lid();
if (part == "brick") brick();
if (part == "contents") contents();
// Measuring stand-in: brick plus the socket tip laid beside it (tip axis along Z at X=60)
if (part == "measure") {
    brick();
    translate([60, 0, 0]) {
        cylinder(d = tip_barrel, h = bar_len);
        translate([-blk_w/2, -blk_h/2, bar_len]) cube([blk_w, blk_h, blk_len]);
    }
}
