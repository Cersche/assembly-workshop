// Concept 14 "Open tray porch" (2026-10-26): the splitter SITS flat, back face DOWN, on slotted standoffs on an open
// tray under the box (screws go down into the tray, easy to reach). No cover and an open front: a wrench reaches every
// F nut without taking anything apart. Ports left/right as in 12; back OUT right-angle F up into the box. Tray ~27 mm.
// Scratch concept; splitter/adapter sizes are estimates / UNKNOWN.
include <parts.scad>
box_contents();
color([0.55,0.75,0.6]){translate([5,69,-27])cube([95,3.5,27]);translate([5,2,-27])cube([95,70.5,3]);
 translate([5,2,-24])cube([95,3,5]);}
splitter_sit([52.5,38,-12],3);
jumper_ra(-12);
color([0.95,0.95,0.95]){run([[29,38,-12],[5,38,-12],[-25,38,-16]]);run([[76,26.5,-12],[100,26.5,-12],[130,26.5,-16]]);}
color([0.15,0.15,0.15]){run([[15,49,-6],[13,60,-14],[0,63,-18],[-25,63,-20]],4);
 run([[90,22.75,-3],[93,12,-12],[100,10,-16],[130,10,-18]],6);}
