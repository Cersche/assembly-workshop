// Concept 10 "Compact tower" (2026-10-26): smallest footprint, ~105 x 80 x 215 outer. Two layers: the splitter on its
// side on the back wall, the ScreenBeam standing in front of it on a cradle carried by four posts. Every opening in
// the bottom wall: coax keystones in the back row (straight under the splitter's right-angle + barrel chains, no
// cable), power hole and Ethernet keystone in the front row. ScreenBeam Ethernet/power end down (power plug straight
// out); one RG6 jumper from the upper OUT up the right side to the coax on top. Scratch concept only.
include <parts.scad>
color([0.92,0.91,0.87])import("c10_body.stl");
ks([22.5,58,2.5]);ks([82.5,58,2.5]);ks([85,22.75,2.5],[0.2,0.4,0.9]);
splitter([52.5,57,55],-90,9);
rod([29,57,55],[22.5,57,55]);rod([22.5,57,55],[22.5,57,16.5]);          // IN keystone -> IN
rod([76,57,43.5],[82.5,57,43.5]);rod([82.5,57,43.5],[82.5,57,16.5]);    // lower OUT -> modem keystone
SB=[20,10,62];
hide_sb=false; if(!hide_sb)screenbeam(SB);   // hide_sb=true shows the splitter layer behind it
color([0.55,0.75,0.6])for(x=[SB[0]+8,SB[0]+57],z=[SB[2]+40,SB[2]+108])translate([x,44,z])rotate([-90,0,0])cylinder(d=8,h=31,$fn=20);  // cradle posts
color([0.95,0.95,0.95])run([[76,57,66.5],[88,56,72],[93,54,90],[93,52,160],[93,40,192],[70,28,198],[52,25,194]]);
rod([40,25,182],[40,25,194]);rod([40,25,194],[52,25,194]);              // right-angle F on the coax (top)
plug45([47,25,62],[0,0,-1]);
color([0.15,0.15,0.15])run([[47,25,17],[47,25,-6]],4);
color([0.55,0.75,0.6])difference(){translate([40,18,4])cube([14,14,9]);translate([47,25,0])cylinder(d=4.5,h=20,$fn=16);}
rj45ra([63,25,55]);
color([0.15,0.15,0.15])run([[70,25,55],[80,24,50],[85,22,30],[85,22.75,17]],6);
