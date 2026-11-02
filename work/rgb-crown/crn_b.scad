// CRN-B proposal (Brian 2026-10-30, option 1): keep the stock Lab Rax top front beam shape;
// the P2 64x32 panel sits at the beam's 45 deg slope in a separate tray screwed onto the face.
// Beam-local coordinates = creator mesh component_1_23 (-Y = rack front, Z up); the stock face
// is the plane z = y + FC. Local tray frame: X along the beam, S up the slope, N out of the face.
// PROPOSAL ONLY: panel numbers are placeholders until Brian names the panel. Fit, strength UNKNOWN.

part = "tray";          // tray | bezel | panel (placeholder) | screws (viewer only)

FC = 21.864;            // stock face plane z = y + FC (measured, logo is flush paint)
ZB = -7.575;            // beam bottom (rack z 400.05, top of U9)
PW = 128; PH = 64; PD = 15; C = 0.4;    // panel nominal; depth UNKNOWN (placeholder)
T = 3; WALL = 3;
S0 = 2;                 // tray bottom edge up the slope (stays above the beam bottom)
IW = PW + 2*C; IH = PH + 2*C;           // pocket
OW = IW + 2*WALL; OH = IH + 2*WALL;
TN = T + PD + C;        // tray height out of the face (panel front flush with the rim)
BZ = 2;                 // bezel ring thickness
LIP = 0.6;              // bezel overlap onto the panel edge
SPINE_S = 25;           // solid 10 mm spine of the stock plate (measured): tray screws go here
SCREW_X = [-56, -20, 20, 56];
EAR_S = [S0 + 12, S0 + OH - 12];
CAB = [80, 13];         // cable exit (w, h) in the tray back where the tray overhangs the beam top

r = 1 / sqrt(2);
O = [0, ZB - FC, ZB];   // face plane point at the beam bottom (S = 0)
module frame() multmatrix([[1, 0, 0, O[0]], [0, r, -r, O[1]], [0, r, r, O[2]], [0, 0, 0, 1]]) children();

module tray() {
    difference() {
        union() {
            translate([-OW/2, S0, 0]) cube([OW, OH, TN]);
            for (sx = [-1, 1], s = EAR_S) translate([sx * (OW/2 + 4), s, 0]) cylinder(d = 10, h = TN, $fn = 32);
        }
        translate([-IW/2, S0 + WALL, T]) cube([IW, IH, TN]);
        // cable exit through the back plate, above the beam top (opens over the roof)
        translate([-CAB[0]/2, S0 + OH - WALL - CAB[1] - 1, -1]) cube([CAB[0], CAB[1], T + 2]);
        // 4 x M3 countersunk screws into heat-set inserts melted into the stock beam spine
        for (x = SCREW_X) translate([x, SPINE_S, -1]) {
            cylinder(d = 3.4, h = T + 2, $fn = 24);
            translate([0, 0, T + 1 - 1.7]) cylinder(d1 = 3.4, d2 = 6.4, h = 1.71, $fn = 24);
        }
        // bezel screws: M3 heat-set pilots in the side ears
        for (sx = [-1, 1], s = EAR_S) translate([sx * (OW/2 + 4), s, TN - 6]) cylinder(d = 4.0, h = 7, $fn = 24);
        // test-print ID on the back (hidden against the beam)
        translate([0, S0 + 12, -0.01]) mirror([1, 0, 0]) linear_extrude(0.6) text("CRN-B", size = 7, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");
    }
}

module bezel() {
    difference() {
        union() {
            translate([-OW/2, S0, TN]) cube([OW, OH, BZ]);
            for (sx = [-1, 1], s = EAR_S) translate([sx * (OW/2 + 4), s, TN]) cylinder(d = 10, h = BZ, $fn = 32);
        }
        translate([-IW/2 - C + LIP, S0 + WALL + C + LIP, TN - 1]) cube([PW - 2*LIP, PH - 2*LIP, BZ + 2]);
        for (sx = [-1, 1], s = EAR_S) translate([sx * (OW/2 + 4), s, TN - 1]) cylinder(d = 3.4, h = BZ + 2, $fn = 24);
        translate([0, S0 + 1.5, TN - 0.01]) mirror([1, 0, 0]) linear_extrude(0.5) text("CRN-B-BZ", size = 2, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");
    }
}

frame() {
    if (part == "tray") tray();
    if (part == "bezel") bezel();
    if (part == "panel") translate([-PW/2, S0 + WALL + C, T]) cube([PW, PH, PD]);
    if (part == "screws") for (x = SCREW_X) translate([x, SPINE_S, -8]) cylinder(d = 3, h = 8 + T, $fn = 16);
}
