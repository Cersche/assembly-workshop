// CRN-A proposal: Lab Rax top front beam with an RGB-window crown (P2 HUB75 64x32).
// Beam-local coordinates = the creator's component_1_23 mesh: X along the rack, -Y = rack front,
// Z up; the beam sits at rack (0, 27.425, 407.625). The original ends (|x| >= END) are kept
// exactly from the source mesh, so both post joints stay original. The middle is new.
// PROPOSAL ONLY: panel numbers are nominal placeholders until Brian names the exact panel.
// Fit, strength and the panel's real dimensions are UNKNOWN. Not printed.

part = "beam";          // beam | cover | panel (placeholder, viewer only)
beam_stl = "beam_orig.stl";

B   = 27.425;           // half beam size (front face y = -B)
ZB  = -7.575;           // beam body bottom = top of slot U9 (rack z 400.05)
HY  = 7.58;             // beam body rear (hook rear face)
END = 111;              // original lattice ends here; |x| >= END is the original solid end block
W   = 112;              // crown half width (1 mm into the solid end block so the union fuses)
T   = 3;                // wall
CH  = 15;               // top corner chamfer (diagonal print fit)

// Panel: P2 64x32 nominal 128 x 64; depth UNKNOWN (placeholder 15)
PW = 128; PH = 64; PD = 15; C = 0.4;
PZ0 = ZB + T + C;                       // panel bottom
ZT  = PZ0 + PH + C + T;                 // crown top
FY  = -B;                               // front face
PY  = FY + T;                           // panel front face
RIB = PW/2 + C + 2.5;                   // inner face of the pocket side ribs = PW/2 + C

// roof seat groove of the original hook (the top panel's front edge sits here)
GY0 = 6.58; GZ0 = 22.72; GZ1 = 26.22; HOOKZ0 = 21.43; HOOKZ1 = 27.43;

module outline(o=0) {   // crown silhouette in XZ, offset inward by o
    polygon([[-W+o, ZB+o], [W-o, ZB+o], [W-o, ZT-CH], [W-CH, ZT-o], [-W+CH, ZT-o], [-W+o, ZT-CH]]);
}
module xz(y0, y1) { translate([0, y1, 0]) rotate([90, 0, 0]) linear_extrude(y1 - y0) children(); }

module middle() {
    difference() {
        union() {
            difference() {                                   // closed shell, rear open above the hook
                xz(FY, HY) outline();
                xz(FY + T, HY + 1) outline(T);
            }
            for (s = [-1, 1]) translate([s > 0 ? RIB - 2.5 : -RIB, FY, ZB]) cube([2.5, HY - FY, ZT - ZB - CH/2]);   // pocket side ribs
            translate([-W, HY - T, ZB]) cube([2*W, T, HOOKZ0 - ZB]);                                        // rear wall below the hook
            translate([-END, 3.5, HOOKZ0]) cube([2*END, HY - 3.5, HOOKZ1 - HOOKZ0]);                        // hook rail
            for (s = [-1, 1]) translate([s * (W - 6) - 6, HY - 6, ZB]) cube([12, 6, ZT - ZB - CH]);          // rear corner posts
        }
        // panel window and pocket
        translate([-PW/2, FY - 1, PZ0]) cube([PW, T + 2, PH]);
        translate([-PW/2 - C, PY, PZ0 - C]) cube([PW + 2*C, PD + 1, PH + 2*C]);
        // rear cable exit below the hook, between the ribs
        translate([-RIB + 2.5, HY - T - 1, ZB + T]) cube([2*RIB - 5, T + 2, HOOKZ0 - ZB - T]);
        // rib wire holes (status LEDs) low on each rib
        for (s = [-1, 1]) translate([s * (RIB - 1.25), 0, 2]) rotate([0, 90, 0]) cylinder(d = 8, h = 4, center = true, $fn = 24);
        // roof seat groove kept clear along the whole span
        translate([-W - 1, GY0, GZ0]) cube([2*W + 2, 3, GZ1 - GZ0]);
        // emblem recess (left, 40 x 40, 1 mm deep) and 3 status LED holes (right, 5 mm LEDs)
        translate([-(PW/2 + 28) - 20, FY - 1, (PZ0 + PH/2) - 20]) cube([40, 2, 40]);
        for (i = [0 : 2]) translate([PW/2 + 16 + i * 10, FY + T/2, PZ0 + PH/2 - 12]) rotate([90, 0, 0]) cylinder(d = 5.2, h = T + 2, center = true, $fn = 24);
        // rear cover screw pilots (M3 heat-set, nominal 4.0 bore) in the corner posts
        for (s = [-1, 1], z = [HOOKZ1 + 8, ZT - CH - 6]) translate([s * (W - 6), HY - 6, z]) rotate([-90, 0, 0]) cylinder(d = 4.0, h = 7, $fn = 24);
        // test-print ID on the floor underside (hidden when installed)
        translate([0, (FY + HY)/2, ZB - 0.01]) mirror([1, 0, 0]) linear_extrude(0.6) text("CRN-A", size = 8, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");
    }
}

module ends() {
    intersection() {
        import(beam_stl, convexity = 10);
        union() for (s = [-1, 1]) translate([s > 0 ? END : -150, -40, -40]) cube([150 - END, 80, 80]);
    }
}

module cover() {        // removable rear cover above the hook, 4 x M3 screws into the corner posts
    difference() {
        translate([-W + 1, HY, HOOKZ1 + 0.5]) cube([2*W - 2, 2.5, ZT - CH - HOOKZ1 - 0.5]);
        for (s = [-1, 1], z = [HOOKZ1 + 8, ZT - CH - 6]) translate([s * (W - 6), HY - 1, z]) rotate([-90, 0, 0]) cylinder(d = 3.4, h = 5, $fn = 24);
        translate([0, HY + 2.5 - 0.5, (HOOKZ1 + ZT - CH)/2]) rotate([-90, 0, 0]) linear_extrude(1) text("CRN-A-RC", size = 6, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");
    }
}

if (part == "beam") union() { ends(); middle(); }
if (part == "cover") cover();
if (part == "panel") translate([-PW/2, PY, PZ0]) cube([PW, PD, PH]);
