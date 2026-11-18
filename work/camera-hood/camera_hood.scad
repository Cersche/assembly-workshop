// Window camera hood for a TP-Link Tapo C211 — clip-on, two halves. DRAFT 1.
// Unprinted, no ID yet. Every camera/window number below is a stand-in until Brian measures.
// Frame (use orientation): Z up, the camera hangs upside down, Z=0 is the base face against
// the bracket, the pan axis is the Z axis, the glass is toward +Y, the window frame is at +X.
// Idea: the hood clamps around the camera's fixed base (two collars), encloses the whole
// pan/tilt sweep (the camera may still sweep at power-up), and is open only at the front,
// where a flange seals to the glass with foam tape. Halves split at X=0 and snap together.
// Print: each half stands upright as used (floor on the bed, seam face vertical); roof and
// lips are 45 degrees or steeper, so no supports.

part = "assembly";   // assembly | scene | camera | glass | bracket | left | right | print

/* ---------- camera (stand-in, Tapo spec 86.5 x 85 x 117.7) ---------- */
cam_base_d   = 86.6;   // round fixed base, against the bracket
cam_base_h   = 12;     // bracket face to where the turning body starts
cam_body_d   = 80;     // widest turning part (body/ball)
cam_h        = 117.7;  // bracket face to bottom of the ball
ball_d       = 80;
lens_d       = 30;
lens_proud   = 2;      // lens front beyond the ball surface
lens_z       = -cam_h + ball_d/2;   // lens centre height (level aim)
cable_ang    = 180;    // direction the cable leaves the base, deg from +X (180 = left, 270 = room)
cable_w      = 7;      // cable plug/cord width through the collar notch
cable_depth  = 8;      // notch depth from the collar top

/* ---------- window (stand-in) ---------- */
glass_gap    = 15;     // lens front to glass
pane_w       = 140;    // visible glass width
cam_x        = 0;      // camera axis from pane centre (+ = toward the frame)
frame_w      = 30;     // right frame strip width
frame_proud  = 20;     // frame face out from the glass
glass_t      = 4;

/* ---------- hood ---------- */
clear        = 6;      // gap around the full pan/tilt sweep
wall         = 2.4;
floor_t      = 2.4;
collar_h     = 8;      // collar height around the base
collar_top   = 2;      // collar top stays this far below the bracket face
collar_fit   = -0.3;   // collar bore minus base diameter (negative = grips)
flange_w     = 10;     // foam flange width beyond the hood outline
flange_t     = 3;
seam_gap     = 0.2;    // total gap between the halves
tongue_t     = 1.2;    // light-seal liner on the right half, overlapping the seam inside
tongue_w     = 4;
snap_len     = 12;     // snap arm length across the seam (rear wall)
snap_h       = 10;
snap_t       = 1.6;
snap_gap     = 0.2;
snap_win     = 4;      // window in the arm the bump clicks into
snap_bump    = 1.0;    // bump catch depth
print_gap    = 15;     // gap between halves on the bed

$fn = 96;

/* ---------- derived ---------- */
sweep_r   = max(cam_body_d/2, ball_d/2 + lens_proud, cam_base_d/2 - 2);
R         = sweep_r + clear;                    // inner radius of the rear
glass_y   = ball_d/2 + lens_proud + glass_gap;  // glass plane
r_ci      = cam_base_d/2 + collar_fit/2;        // collar bore radius
cw        = wall * sqrt(2);                     // collar wall (gives ~wall normal to the 45 deg roof)
r_co      = r_ci + cw;
z_ct      = -collar_top;
z_cb      = z_ct - collar_h;                    // collar bottom
z_fi      = -cam_h - clear;                     // floor inside
z_f       = z_fi - floor_t;                     // floor underside (bed)
z_ri      = z_cb - (sqrt(R*R + glass_y*glass_y) - r_ci);              // roof meets inner walls
z_ro      = z_cb - (sqrt(pow(R+wall,2) + glass_y*glass_y) - r_co);    // roof meets outer walls
ys        = -(R + wall);                        // rear outer wall
snap_z    = [z_f + 22, z_ro - 14];

echo(str("HOOD inner R=", R, " glass_y=", glass_y, " floor=", z_f, " outer width=",
         2*(R+wall), " flange width=", 2*(R+wall+flange_w), " height=", z_ct - z_f));

/* ---------- shapes ---------- */
module outline(r, y_front) { circle(r); translate([-r, 0]) square([2*r, y_front]); }

module outer_body() {
    hull() {
        translate([0, 0, z_cb]) cylinder(r = r_co, h = 0.01);
        translate([0, 0, z_f]) linear_extrude(z_ro - z_f) outline(R + wall, glass_y);
    }
    translate([0, 0, z_cb]) cylinder(r = r_co, h = collar_h);
}

module cavity(shrink = 0) {
    hull() {
        translate([0, 0, z_cb]) cylinder(r = r_ci - shrink, h = 0.01);
        translate([0, 0, z_fi + shrink])
            linear_extrude(z_ri - z_fi - shrink) outline(R - shrink, glass_y + 0.5);
    }
}

module section_at_glass() {     // 2D (x, z) section of a solid at the flange plane
    projection(cut = true) translate([0, 0, glass_y - 0.05]) rotate([-90, 0, 0]) children();
}

module flange() {
    translate([0, glass_y, 0]) rotate([90, 0, 0]) linear_extrude(flange_t)
    intersection() {
        difference() {
            offset(r = flange_w) section_at_glass() outer_body();
            intersection() {
                section_at_glass() cavity();
                translate([-500, z_f + flange_w]) square(1000);
            }
        }
        translate([-500, z_f]) square(1000);       // nothing below the bed
    }
}

module cable_notch() {
    rotate([0, 0, cable_ang]) translate([0, -cable_w/2, z_ct - cable_depth])
        cube([r_co + 1, cable_w, cable_depth + 1]);
}

module shell() {
    difference() {
        outer_body();
        cavity();
        translate([0, 0, z_cb - 1]) cylinder(r = r_ci, h = collar_h + 2);
        translate([-500, glass_y, -500]) cube(1000);   // open front
        cable_notch();
    }
    flange();   // added after the cavity cut so its bottom bar spans the opening
}

module half_space_x(sign) {     // sign -1: x <= -seam_gap/2, +1: x >= seam_gap/2
    translate([sign > 0 ? seam_gap/2 : -1000 - seam_gap/2, -500, -500]) cube([1000, 1000, 1000]);
}

// Light-seal liner: right half, inside the left half's wall along the seam, 45 deg bottom.
module liner() {
    intersection() {
        union() {
            difference() { cavity(); cavity(tongue_t); }
            intersection() {    // bonds into the right wall (overlap, not a shared face)
                difference() { cavity(-0.6); cavity(tongue_t); }
                translate([-seam_gap/2, -500, -500]) cube([2, 1000, 1000]);
            }
        }
        translate([-tongue_w - seam_gap/2, -500, z_fi]) cube([tongue_w + seam_gap/2 + 1.5, 1000, z_cb - 0.5 - z_fi]);
        translate([0, 0, z_fi]) rotate([0, 45, 0]) translate([-500, -500, 0]) cube(1000);
        translate([-500, -500, -500]) cube([1000, glass_y - flange_t + 500, 1000]);
    }
}

// Snap arm (right half) reaching across the rear seam over the left half's wall.
module snap_arm(zc) {
    y1 = ys - snap_gap; y0 = y1 - snap_t;
    difference() {
        union() {
            translate([0.5, y0, zc - snap_h/2 - snap_len]) cube([3, ys + 1.5 - y0, snap_h + snap_len]);   // root on the wall
            // arm plate, bottom edge rises 45 deg toward the tip (printable)
            translate([0, y1, 0]) rotate([90, 0, 0]) linear_extrude(snap_t)
                polygon([[2, zc - snap_h/2 - snap_len + 2], [2, zc + snap_h/2],
                         [-snap_len, zc + snap_h/2], [-snap_len, zc - snap_h/2]]);
        }
        translate([-snap_len + 2, y0 - 1, zc - snap_h/2 + 2]) cube([snap_win, snap_t + 2, snap_h - 4]);
    }
}

// Bump on the left half's wall that clicks into the arm window: ramp faces the seam.
module snap_bump(zc) {
    y1 = ys - snap_gap; y0 = y1 - snap_t;
    x_catch = -snap_len + 2 + 0.3; x_ramp = -snap_len + 2 + snap_win - 0.3;
    intersection() {
        translate([0, 0, zc - snap_h/2 + 2.3]) linear_extrude(snap_h - 4.6)
            polygon([[x_catch, ys + 2], [x_catch, y0 + 0.2], [x_catch + 1, y0 + 0.2],
                     [x_ramp, y1 - (snap_t - snap_bump) + 0.0], [x_ramp, ys + 2]]);
        translate([0, ys + 2, zc - snap_h/2 + 2.3]) rotate([-45, 0, 0]) translate([-500, -500, 0]) cube(1000);
    }
}

module hood_left()  { intersection() { shell(); half_space_x(-1); } for (z = snap_z) snap_bump(z); }
module hood_right() { intersection() { shell(); half_space_x(1); } liner(); for (z = snap_z) snap_arm(z); }

/* ---------- stand-ins ---------- */
module camera() {
    color("white") {
        translate([0, 0, -cam_base_h]) cylinder(d = cam_base_d, h = cam_base_h);
        translate([0, 0, lens_z]) cylinder(d = cam_body_d, h = -cam_base_h - lens_z);
        translate([0, 0, lens_z]) sphere(d = ball_d);
    }
    color("black") translate([0, ball_d/2 - 6, lens_z]) rotate([-90, 0, 0]) cylinder(d = lens_d, h = 6 + lens_proud);
}
module glass() {
    x_r = pane_w/2 - cam_x;
    color("lightblue", 0.4) translate([-pane_w/2 - cam_x, glass_y, -220]) cube([pane_w, glass_t, 280]);
    color("saddlebrown") translate([x_r, glass_y - frame_proud, -220]) cube([frame_w, frame_proud + glass_t, 280]);
}
module bracket() {
    x_r = pane_w/2 - cam_x; yf = glass_y - frame_proud;
    color("dimgray") {
        hull() { cylinder(d = 30, h = 3); translate([x_r, yf - 23, 0]) cube([frame_w, 20, 3]); }
        translate([x_r, yf - 3, -40]) cube([frame_w, 3, 43]);
    }
}

if (part == "assembly") { hood_left(); hood_right(); camera(); glass(); bracket(); }
if (part == "scene")    { camera(); glass(); bracket(); }
if (part == "camera")   camera();
if (part == "glass")    glass();
if (part == "bracket")  bracket();
if (part == "left")     hood_left();
if (part == "right")    hood_right();
if (part == "print") {   // both halves upright, seam faces up-and-apart, floor on the bed
    translate([-print_gap/2, 0, -z_f]) hood_left();
    translate([ print_gap/2, 0, -z_f]) hood_right();
}
