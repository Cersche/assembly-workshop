// Concept 9 "Landscape" (2026-10-26): wide and short like a NID box, ~220 x 75 x 150 outer. ScreenBeam lying flat
// (original orientation: coax left end, Ethernet/power right end). Every opening in the bottom wall. All coax links
// rigid, no coax jumper: splitter (IN right, OUTs left) -> upper OUT: right-angle + barrel + right-angle into the
// ScreenBeam's coax; lower OUT: right-angle + barrel to the modem keystone; IN: right-angle + barrel to the IN keystone.
// Power plug 45 mm straight out the right end, one gentle 90 deg bend down to its hole. Scratch concept only.
include <parts.scad>
color([0.92,0.91,0.87])import("c9_body.stl");
ks([18,50,2.5]);ks([78,50,2.5]);ks([160,25,2.5],[0.2,0.4,0.9]);
splitter([48,50,42],90,11);
rod([24.5,50,53.5],[18,50,53.5]);rod([18,50,53.5],[18,50,107]);rod([18,50,107],[30,49,107]);   // upper OUT -> ScreenBeam coax
rod([24.5,50,30.5],[18,50,30.5]);rod([18,50,30.5],[18,50,16.5]);                              // lower OUT -> modem keystone
rod([71.5,50,42],[78,50,42]);rod([78,50,42],[78,50,16.5]);                                    // IN keystone -> IN
screenbeam([30,34,75],true);
plug45([150,49,95],[1,0,0]);
color([0.15,0.15,0.15])run([[195,49,95],[203,49,90],[205,49,75],[205,49,-6]],4);
color([0.55,0.75,0.6])difference(){translate([198,42,4])cube([14,14,9]);translate([205,49,0])cylinder(d=4.5,h=20,$fn=16);}
rj45ra([157,49,120]);
color([0.15,0.15,0.15])run([[157,42,120],[160,28,112],[160,25,60],[160,25,17]],6);
