// SCR5-WP-A — wedge-pin button test coupon for the Waveshare 5" DSI LCD (C).
// Frame: FRONT view of the screen. X right, Z up, Y back; glass front Y=0, glass centred on X=0,Z=0.
// Measured 2026-10-30 (work/screen-5in/Dimensions.md). PCB assumed centred under the glass (UNKNOWN).
part = "body";            // body | pin1 | pin2 | pin3 | assembly
$fn = 40;
PCB_TOP   = 38.0;          // PCB top edge (76/2)
GLASS_TOP = 38.6;          // 77.2/2
SEAT      = 13.3;          // glass front -> standoff top (calipers)
SO        = [56.45, 34];   // corner standoff centre (112.9 x 68)
PLG_Y     = 10.9;          // plunger centre depth (PCB back 9.1 + 3.6/2)
BTN_X     = [45.5, 35.5, 25.5];   // power, bright+, bright- (15/25/35 from rear-view left = front-view right)
DROP      = [0.35, 0.45, 0.55];   // stem drop per pin variant (1/2/3 dots)
GAP       = 0.10;          // nub to plunger at rest
BAR_T = 3; STUB_T = 4; ZB = GLASS_TOP + 0.8; ZT = 48;
HOLE = [3.4, 40.3, 44.7];  // pin guide: width, z0, z1
LEAF_T = 0.8;
module body() {
  difference() {
    union() {
      translate([-61, 0, ZB]) cube([122, STUB_T, ZT-ZB]);                 // front stub (faceplate stand-in)
      translate([-61, 0, ZT-2]) cube([122, SEAT+BAR_T, 2]);               // roof
      translate([-61, SEAT, 36]) cube([122, BAR_T, ZT-36]);               // rear bar
      for (s=[-1,1]) translate([s*SO[0], SEAT, SO[1]]) rotate([-90,0,0]) cylinder(r=4.5, h=BAR_T);   // screw pads
      for (x=[-61,-57,18,50,57]) translate([x, 0, ZB]) cube([x==-61||x==57?4:2, SEAT, ZT-ZB]); // walls
      for (x=BTN_X) translate([x-1.5, 0, 0]) {                            // leaf springs from the stub
        translate([0, 0, PCB_TOP+GAP+0.9+0.1]) cube([3, 11.8, LEAF_T]);
        translate([0, 10.2, PCB_TOP+GAP]) cube([3, 1.4, 1.0+LEAF_T/2]);   // nub onto the plunger
        translate([0, 10.4, PCB_TOP+GAP+1.0+LEAF_T]) cube([3, 1.0, 0.9]); // bump under the pin ramp
      }
    }
    for (s=[-1,1]) translate([s*SO[0], SEAT-1, SO[1]]) rotate([-90,0,0]) cylinder(d=2.8, h=BAR_T+2);
    for (x=BTN_X) translate([x-HOLE[0]/2, -1, HOLE[1]]) cube([HOLE[0], SEAT+BAR_T+2, HOLE[2]-HOLE[1]]);
  }
  translate([-25, 8, ZT-0.01]) linear_extrude(0.6) text("SCR5-WP-A", size=4.5, halign="center", valign="center", font="Liberation Sans:style=Bold");
}
// one pin, rest position, centred on X=0; drop d, stroke s = 2d + 0.5 (0.1 lead-in + 0.4 dwell = hard stop)
module pin(d, dots) {
  s = 2*d + 0.5;
  difference() {
    union() {
      translate([-1.5, 0, 0]) rotate([90,0,90]) linear_extrude(3) polygon([
        [-s,40.5],[10.2,40.5],[10.2,41.0],[11.5,41.0],[11.5+2*d,41.0-d],[15,41.0-d],[15,44.5],[-s,44.5]]);
      translate([-2.5, -s-1.5, 39.6]) cube([5, 1.5, 5.8]);                 // finger cap; its back face is the hard stop
    }
    for (i=[0:dots-1]) translate([(i-(dots-1)/2)*1.4, -s-1.5-0.01, 43.5]) rotate([-90,0,0]) cylinder(d=0.9, h=0.4);
  }
}
if (part=="body") body();
else if (part=="assembly") { body(); for (i=[0:2]) translate([BTN_X[i],0,0]) pin(DROP[i], i+1); }
else { i = part=="pin1"?0:part=="pin2"?1:2; pin(DROP[i], i+1); }
