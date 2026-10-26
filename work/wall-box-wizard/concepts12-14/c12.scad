// Concept 12 "Hanging porch" (2026-10-26): concept 11 with the splitter lying flat, back face UP, screwed to the
// underside of the box (slotted ears, inserts in a thickened bottom). Ports point left/right: incoming coax onto IN
// from the left, modem coax off the front OUT to the right; the back OUT takes a right-angle F straight up to the
// 14 mm hole and one jumper inside goes to the ScreenBeam. Shallow porch ~33 mm: back plate + floor + clip-on front
// cover, open at both ends. Scratch concept; splitter/adapter sizes are estimates / UNKNOWN.
include <parts.scad>
cover=true;
box_contents();
color([0.55,0.75,0.6]){translate([5,69,-33])cube([95,3.5,33]);translate([5,2,-33])cube([95,70.5,3]);}
if(cover)color([0.92,0.91,0.87,0.35])translate([5,2,-30])cube([95,3,30]);
splitter_hang([52.5,38,-11],2);
jumper_ra(-11);
color([0.95,0.95,0.95]){run([[29,38,-11],[5,38,-11],[-25,38,-16]]);run([[76,26.5,-11],[100,26.5,-11],[130,26.5,-16]]);}
color([0.15,0.15,0.15]){run([[15,49,-6],[13,58,-20],[0,62,-24],[-25,62,-26]],4);
 run([[90,22.75,-3],[92,16,-20],[100,12,-24],[130,12,-26]],6);}
