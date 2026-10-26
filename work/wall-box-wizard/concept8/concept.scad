// Concept 8 (Brian, 2026-10-26: "route everything through the bottom"): every opening in the bottom wall
// (coax IN, coax to modem, power hole, Ethernet). ScreenBeam standing with Ethernet/power end DOWN, so the 45 mm power
// plug points straight at its hole: no U-turn. Splitter on its side, ports left/right; IN and modem OUT reach their
// keystones through right-angle F + barrel (no cable); one RG6 jumper from the other OUT up to the ScreenBeam's coax
// on top. Box inner 185 x 70 x 210 (outer ~190 x 75 x 215). Scratch concept; splitter/adapter sizes are estimates/UNKNOWN.
color([0.92,0.91,0.87])import("body.stl");
module run(p,d=6.8)for(i=[0:len(p)-2])hull(){translate(p[i])sphere(d=d,$fn=14);translate(p[i+1])sphere(d=d,$fn=14);}
module rod(a,b,c="silver")color(c)hull(){translate(a)sphere(d=9.5,$fn=20);translate(b)sphere(d=9.5,$fn=20);}
module slot(l)hull(){translate([-l/2,0])circle(d=3.4,$fn=16);translate([l/2,0])circle(d=3.4,$fn=16);}
module ycyl(p,d,h)translate(p)rotate([-90,0,0])cylinder(d=d,h=h,$fn=32);

// bottom-wall keystones: coax IN (X15), coax to modem (X75), Ethernet (X170); power hole at X119
color([0.95,0.95,0.95]){translate([7,42,2.5])cube([16,17,14]);translate([67,42,2.5])cube([16,17,14]);}
color([0.2,0.4,0.9])translate([162,41,2.5])cube([16,17,14]);

// Splitter on the back wall, turned on its side: body 23 (X) x 39 (Z) x 17, port axis Y=50, IN points left,
// OUTs point right 23 apart; ears at opposite corners on slotted standoffs; ground block top right.
sx=45; sz=60; ay=50; by=59;
EARS=[[sx-6.5,sz+24],[sx+6.5,sz-24]];
color([0.55,0.75,0.6])for(e=EARS)difference(){ycyl([e[0],by,e[1]],11,70-by);
 translate([e[0],by-1,e[1]])rotate([-90,0,0])linear_extrude(15)slot(5);}
color("silver"){
 translate([sx-11.5,ay,sz-19.5])cube([23,9,39]);
 translate([sx-11,ay-8,sz-19])cube([22,8,38]);
 for(e=EARS)difference(){hull(){ycyl([e[0],ay,e[1]],10,9);ycyl([e[0],ay,e[1]+(e[1]<sz?8:-8)],10,9);}
  ycyl([e[0],ay-1,e[1]],5,11);}
 translate([sx+11.5,ay-8,sz+15.5])cube([6,17,4]);
}
color("gold"){rod([sx-11.5,ay,sz],[sx-23.5,ay,sz]);for(dz=[-11.5,11.5])rod([sx+11.5,ay,sz+dz],[sx+23.5,ay,sz+dz]);}
rod([sx-23.5,ay,sz],[15,ay,sz]);rod([15,ay,sz],[15,ay,16.5]);                          // IN: right-angle F + barrel down to the IN keystone
rod([sx+23.5,ay,sz-11.5],[75,ay,sz-11.5]);rod([75,ay,sz-11.5],[75,ay,16.5]);           // lower OUT: right-angle F + barrel down to the modem keystone

// ScreenBeam standing, Ethernet/power end DOWN, coax end up, vents towards the lid; slotted cradle behind it
SB=[92,34,62];
color([0.55,0.75,0.6])difference(){union(){translate([SB[0]+3,64,SB[2]+5])cube([59,4,110]);
  for(x=[SB[0]+6,SB[0]+59],z=[SB[2]+12,SB[2]+108])translate([x-8,64,z-8])cube([16,4,16]);}
 for(x=[SB[0]+6,SB[0]+59],z=[SB[2]+12,SB[2]+108])translate([x,63,z])rotate([-90,0,0])linear_extrude(6)if(z>100)slot(9);else rotate(90)slot(9);}
color([0.12,0.12,0.13])translate(SB)cube([65,30,120]);
color([0.3,0.3,0.32])translate([SB[0]+12,33.5,SB[2]+30])cube([41,1,60]);
px=SB[0]+27; ex=SB[0]+43; cx=SB[0]+20; py=49; top=SB[2]+120;
// Power: 45 mm plug straight down, cable straight out of the 13 mm hole, clamp just inside
color([0.85,0.2,0.2])translate([px,py,SB[2]-45])cylinder(d=10,h=45,$fn=24);
color([0.15,0.15,0.15])run([[px,py,SB[2]-45],[px,py,-6]],4);
color([0.55,0.75,0.6])difference(){translate([px-7,py-7,4])cube([14,14,9]);translate([px,py,0])cylinder(d=4.5,h=20,$fn=16);}
// Ethernet: right-angle plug turning right, short patch down into the Ethernet keystone
color([0.2,0.4,0.9])translate([ex-7,py-7,SB[2]-20])cube([14,14,20]);
color([0.15,0.15,0.15])run([[ex+7,py,SB[2]-12],[ex+20,46,SB[2]-14],[166,48,38],[170,49,18]],6);
// Coax In on top: right-angle F, leg to the left; upper OUT -> one RG6 jumper up between the splitter and ScreenBeam
rod([cx,py,top],[cx,py,top+12]);rod([cx,py,top+12],[cx-12,py,top+12]);
color([0.95,0.95,0.95])run([[sx+23.5,ay,sz+11.5],[78,46,sz+16],[84,30,sz+35],[84,26,150],[88,30,top+4],[cx-12,py,top+12]]);
