// NETGEAR CM1000 cable modem — envelope model (no manufacturer CAD found).
// Rack orientation (Brian, 2026-10-19): lights facing upward, so the LED side is +Y,
// the same as the bracket's light pipes.
// Units: mm. Orientation and origin match the bracket reference
// (reference/CM1000_1U_10in_bracket_body.stl): modem lying flat, off its stand.
//   X = length (side to side), Y = thickness (vertical, centered), Z = depth (front LED face at +Z).
//
// SOURCE STATUS
//   DERIVED from the pocket of Brian's bracket (Y:\CM1000_1U_10in.3mf), which Brian
//   reports fits very well. These are the cavity, so they are the modem plus fit clearance:
//     length 212.6 between rail floors; end channel 18.3 tall, 10.5 deep;
//     front nose profile (front_prof); max thickness 38.0, read where the pocket is widest.
//   body_d 136: retail 5.4 in (bracket 137.6 deep, consistent).
//     LED positions from the bracket's five shine-through light pipes.
//   Length excludes the stand (spec sheet 8.8 in = 223.5 includes it).
//   Rear port positions: scaled from NETGEAR's spec image (see port_from_top).
//   Rear-edge shape: ASSUMED.
// Visual/clearance stand-in only. Physical fit remains UNKNOWN.

include_bracket = false;  // overlay the local reference bracket (do not distribute)

body_l   = 212.6;
body_d   = 136.0;
front_z  = 68.6;          // modem front face, just inside faceplate (68.81)
max_t    = 38.0;
edge_t   = 18.3;

// half-thickness vs distance back from front face, sampled from the bracket pocket
front_prof = [[0, 0.6], [0.8, 1.1], [2.8, 3.9], [4.8, 6.6], [6.8, 9.4],
              [8.8, 12.1], [10.8, 14.9], [13.8, max_t / 2]];
rear_r   = 6;             // ASSUMED rear edge rounding

// half-thickness vs |x|, sampled from the end rails
end_prof = [[0, max_t / 2], [93, max_t / 2], [95, 16.0], [97, edge_t / 2], [body_l / 2, edge_t / 2]];

$fn = 48;

module yz_profile() {   // polygon in (z, y), extruded along X
    pts = concat(
        [for (p = front_prof) [front_z - p[0],  p[1]]],
        [[front_z - body_d + rear_r, max_t / 2], [front_z - body_d, max_t / 2 - rear_r],
         [front_z - body_d, -max_t / 2 + rear_r], [front_z - body_d + rear_r, -max_t / 2]],
        [for (i = [len(front_prof) - 1 : -1 : 0]) [front_z - front_prof[i][0], -front_prof[i][1]]]);
    polygon([for (p = pts) [p[1], p[0]]]);  // extrusion below maps polygon (u, v) -> (Y, Z)
}

module xy_profile() {   // polygon in (x, y), extruded along Z
    pts = concat(
        [for (p = end_prof) [p[0], p[1]]],
        [for (i = [len(end_prof) - 1 : -1 : 0]) [ end_prof[i][0], -end_prof[i][1]]],
        [for (p = end_prof) [-p[0], -p[1]]],
        [for (i = [len(end_prof) - 1 : -1 : 0]) [-end_prof[i][0],  end_prof[i][1]]]);
    polygon(pts);
}

module body() {
    intersection() {
        rotate([90, 0, 90]) translate([0, 0, -body_l / 2]) linear_extrude(body_l) yz_profile();
        translate([0, 0, front_z - body_d]) linear_extrude(body_d) xy_profile();
    }
}

module leds() {          // DERIVED: five status LEDs at the bracket's light-pipe positions (x, y = +8)
    for (x = [-23, -11.5, 0, 11.5, 23]) translate([x, 8, front_z - 6]) rotate([-35, 0, 0]) cylinder(d = 3, h = 0.6);
}

// Rear port order and spacing scaled from NETGEAR's "Technical Specs" image (rear view, upright,
// the case scaled to body_l = 212.6, excluding the stand). Distances are from the upright top tip.
// Which end of the flat-lying modem is "top" is ASSUMED (-X). Accuracy is about ±3 mm (image scaling).
port_from_top = [["reset", 43], ["lan", 70], ["cable", 119], ["switch", 152], ["dc", 165]];

module rear_ports() {
    rz = front_z - body_d;
    function px(name) = -body_l / 2 + [for (p = port_from_top) if (p[0] == name) p[1]][0];
    translate([px("reset"), 0, rz]) rotate([180, 0, 0]) cylinder(d = 3, h = 1);
    translate([px("lan") - 7, -8, rz - 1]) cube([14, 16, 1]);                     // RJ45 opening
    translate([px("cable"), 0, rz]) rotate([180, 0, 0]) cylinder(d = 9.5, h = 12); // F-connector
    translate([px("switch") - 2, -4, rz - 3]) cube([4, 8, 3]);                    // power switch
    translate([px("dc"), 0, rz]) rotate([180, 0, 0]) cylinder(d = 8, h = 2);      // DC jack 12 V 2.5 A
}

// Retention (Brian, 2026-10-19): the modem slides into the bracket's end-rail pockets, and one
// screw goes through the middle of the bracket into the modem. DERIVED from the bracket: a single
// horizontal slot through the LEFT (-X) rail wall at mid-depth, about 12 mm (Z) × 2.5 mm (Y),
// centered at Y ≈ +0.75, Z ≈ 0. The right rail has no hole. The screw size and the matching hole
// in the modem's end are UNKNOWN.
screw_slot = [-body_l / 2, 0.75, 0, 12, 2.5];   // x, y, z, length (Z), height (Y)

module screw_marker() {
    translate([screw_slot[0] - 4, screw_slot[1], screw_slot[2]]) rotate([0, 90, 0]) cylinder(d = 2.5, h = 8);
}

module cable_keepout() { // rear cable bend clearance (ASSUMED 60 mm)
    %translate([-body_l / 2, -max_t / 2, front_z - body_d - 60]) cube([body_l, max_t, 60]);
}

color("#1c1c1c") body();
color("#40ff40") leds();
color("#c0a050") rear_ports();
cable_keepout();
color("red") screw_marker();
if (include_bracket) %import("reference/CM1000_1U_10in_bracket_body.stl");
