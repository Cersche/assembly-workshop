// Concept 13 "Drop-through porch" (2026-10-26): same flat hanging splitter as 12, but every cable leaves DOWN
// through slots in the porch floor (slots open to the front so a cable with its connector on slips in). IN and the
// modem OUT each take a right-angle F pointing down; the back OUT goes up into the box as in 12. Porch ~48 mm.
// Two more F joints than 12, but nothing sticks out sideways. Scratch concept; sizes estimates / UNKNOWN.
include <parts.scad>
cover=true;
box_contents();
color([0.55,0.75,0.6]){translate([5,69,-48])cube([95,3.5,48]);
 difference(){translate([5,2,-48])cube([95,70.5,3]);
  for(s=[[17,42],[88,30],[8,63],[95,12]])translate([s[0]-4.5,0,-50])cube([9,s[1]+2,6]);}}
if(cover)color([0.92,0.91,0.87,0.35])translate([5,2,-45])cube([95,3,45]);
splitter_hang([52.5,38,-11],2);
jumper_ra(-11);
rod([29,38,-11],[17,38,-11]);rod([17,38,-11],[17,38,-23]);
rod([76,26.5,-11],[88,26.5,-11]);rod([88,26.5,-11],[88,26.5,-23]);
color([0.95,0.95,0.95]){run([[17,38,-23],[17,38,-62],[14,30,-95]]);run([[88,26.5,-23],[88,26.5,-62],[91,20,-95]]);}
color([0.15,0.15,0.15]){run([[15,49,-6],[9,58,-20],[8,61,-62],[6,55,-95]],4);
 run([[90,22.75,-3],[93,13,-12],[95,8,-30],[95,8,-62],[97,12,-95]],6);}
