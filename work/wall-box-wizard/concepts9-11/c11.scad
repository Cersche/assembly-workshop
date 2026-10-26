// Concept 11 "Splitter porch" (2026-10-26): fewest F joints. The splitter sits OUTSIDE under the box in a printed
// porch (back plate + clip-on front cover, open at both ends), so the incoming coax and the modem coax screw straight
// onto the splitter: no coax keystones, couplers or barrels. One RG6 jumper from the upper OUT goes up through a 14 mm
// hole into the box and up the right side to the ScreenBeam's coax on top. Box ~105 x 75 x 210 outer, porch ~45 mm
// below it. Power hole and Ethernet keystone in the box's bottom wall; their cables run out through the porch.
// Scratch concept only.
include <parts.scad>
color([0.92,0.91,0.87])import("c11_body.stl");
ks([70,22.75,2.5],[0.2,0.4,0.9]);
SB=[17.5,34,62];
screenbeam(SB);
// porch: back plate on the wall plane and a clip-on front cover (shown see-through)
color([0.55,0.75,0.6])translate([5,66,-45])cube([95,6.5,45]);
cover=true; if(cover)color([0.92,0.91,0.87,0.35]){translate([5,16,-45])cube([95,3,45]);translate([5,16,-48])cube([95,56.5,3]);}
splitter([52,57,-22],-90,1);
color([0.95,0.95,0.95]){
 run([[28.5,57,-22],[10,57,-22],[-25,57,-30]]);                        // incoming coax straight onto IN
 run([[75.5,57,-33.5],[100,57,-33.5],[130,57,-40]]);                   // lower OUT straight to the modem
 run([[75.5,57,-10.5],[86,55,-8],[93,52,3],[93,52,160],[93,40,192],[70,28,198],[49.5,49,194]]);   // upper OUT -> ScreenBeam
}
rod([37.5,49,182],[37.5,49,194]);rod([37.5,49,194],[49.5,49,194]);
plug45([44.5,49,62],[0,0,-1]);
color([0.15,0.15,0.15]){run([[44.5,49,17],[44.5,49,-6],[42,32,-15],[30,28,-28],[0,28,-30],[-25,28,-30]],4);
 run([[70,22.75,-3],[72,24,-20],[100,25,-28],[130,25,-30]],6);}
color([0.55,0.75,0.6])difference(){translate([37.5,42,4])cube([14,14,9]);translate([44.5,49,0])cylinder(d=4.5,h=20,$fn=16);}
rj45ra([60.5,49,55]);
color([0.15,0.15,0.15])run([[67.5,49,55],[70,30,45],[70,23,17]],6);
