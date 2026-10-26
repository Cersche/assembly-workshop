// Concept 7 (Brian's arrangement photo, 2026-10-26): ScreenBeam standing, coax end down; splitter low on its left,
// OUTs up, IN down straight into a bottom-wall keystone; modem coax and Ethernet keystones on the right wall;
// power plug straight up, over the top to the left wall. Box inner 200 x 70 x 225 (outer ~205 x 75 x 230).
// Scratch concept only; splitter and adapter sizes are photo estimates / UNKNOWN.
color([0.92,0.91,0.87])import("body.stl");
module run(p,d=6.8)for(i=[0:len(p)-2])hull(){translate(p[i])sphere(d=d,$fn=14);translate(p[i+1])sphere(d=d,$fn=14);}
module rod(a,b,c="silver")color(c)hull(){translate(a)sphere(d=9.5,$fn=20);translate(b)sphere(d=9.5,$fn=20);}
module slot(l)hull(){translate([-l/2,0])circle(d=3.4,$fn=16);translate([l/2,0])circle(d=3.4,$fn=16);}
module ycyl(p,d,h)translate(p)rotate([-90,0,0])cylinder(d=d,h=h,$fn=32);
W=205; // outer width

// keystones: bottom (coax IN), right wall (coax to modem, Ethernet to switch)
color([0.95,0.95,0.95]){translate([26.5,42,2.5])cube([16,17,14]);translate([W-16.5,27,93])cube([14,16,17]);}
color([0.2,0.4,0.9])translate([W-16.5,27,168])cube([14,16,17]);

// Splitter on the back wall (photo estimates): back face Y=59 on slotted standoffs, body 39 (X) x 23 (Z) x 17,
// port axis Y=50, OUTs up 23 apart, IN down; ears at opposite corners, ground block on the OUT side.
sx=34.5; sz=55; ay=50; by=59;
EARS=[[sx-24,sz+6.5],[sx+24,sz-6.5]];
color([0.55,0.75,0.6])for(e=EARS)difference(){ycyl([e[0],by,e[1]],11,70-by);
 translate([e[0],by-1,e[1]])rotate([-90,0,0])linear_extrude(15)slot(5);}
color("silver"){
 translate([sx-19.5,ay,sz-11.5])cube([39,9,23]);
 translate([sx-19,ay-8,sz-11])cube([38,8,22]);
 for(e=EARS)difference(){hull(){ycyl([e[0],ay,e[1]],10,9);ycyl([e[0]+(e[0]<sx?8:-8),ay,e[1]],10,9);}
  ycyl([e[0],ay-1,e[1]],5,11);}
 translate([sx+15.5,ay-8,sz+11.5])cube([4,17,6]);
}
color("gold"){rod([sx,ay,sz-11.5],[sx,ay,sz-23.5]);for(dx=[-11.5,11.5])rod([sx+dx,ay,sz+11.5],[sx+dx,ay,sz+23.5]);}
rod([sx,ay,sz-23.5],[sx,ay,16.5]);   // IN: F male-male barrel straight down into the bottom keystone (no cable)

// ScreenBeam standing (65 wide, 120 tall, 30 thick), vents towards the lid; cradle with slotted tabs behind it
SB=[72,34,40];
color([0.55,0.75,0.6])difference(){union(){translate([SB[0]+3,64,SB[2]+5])cube([59,4,110]);
  for(x=[SB[0]+6,SB[0]+59],z=[SB[2]+12,SB[2]+108])translate([x-8,64,z-8])cube([16,4,16]);}
 for(x=[SB[0]+6,SB[0]+59],z=[SB[2]+12,SB[2]+108])translate([x,63,z])rotate([-90,0,0])linear_extrude(6)if(z>100)slot(9);else rotate(90)slot(9);}
color([0.12,0.12,0.13])translate(SB)cube([65,30,120]);
color([0.3,0.3,0.32])translate([SB[0]+12,33.5,SB[2]+30])cube([41,1,60]);
cx=SB[0]+45; ex=SB[0]+22; px=SB[0]+38; py=49; top=SB[2]+120;
// Coax In: right-angle F under the end, leg turned towards the lid
rod([cx,py,SB[2]],[cx,py,SB[2]-12]);rod([cx,py,SB[2]-12],[cx,26,SB[2]-12]);
color([0.95,0.95,0.95]){
 run([[sx-11.5,ay,sz+24],[sx-11,46,92],[sx+5,30,112],[cx-25,24,112],[cx,22,92],[cx,22,45],[cx,26,SB[2]-12]]);   // OUT 1 -> ScreenBeam
 run([[sx+11.5,ay,sz+24],[sx+12,44,90],[sx+30,30,104],[cx+20,20,104],[W-30,26,102],[W-16.5,35,102]]);          // OUT 2 -> modem keystone
}
// Ethernet: right-angle plug on top, short patch across to the right keystone (in front of the power plug)
color([0.2,0.4,0.9])translate([ex-7,py-7,top])cube([14,14,20]);
color([0.15,0.15,0.15])run([[ex,py-7,top+14],[ex+10,30,top+17],[px+20,30,top+17],[W-16.5,35,177]],6);
// Power: 45 mm plug straight up, U over the top, back left to a 13 mm hole in the left wall with a clamp inside
color([0.85,0.2,0.2])translate([px,py,top])cylinder(d=10,h=45,$fn=24);
color([0.15,0.15,0.15])run([[px,py,top+45],[px-2,52,top+56],[px-15,56,top+59],[45,59,top+55],[2,60,205]],4);
color([0.55,0.75,0.6])translate([30,54,199])cube([12,8,12]);
