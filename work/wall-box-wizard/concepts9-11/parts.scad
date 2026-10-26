// Shared concept parts (scratch). Splitter and adapter sizes are photo estimates / UNKNOWN.
module run(p,d=6.8)for(i=[0:len(p)-2])hull(){translate(p[i])sphere(d=d,$fn=14);translate(p[i+1])sphere(d=d,$fn=14);}
module rod(a,b,c="silver")color(c)hull(){translate(a)sphere(d=9.5,$fn=20);translate(b)sphere(d=9.5,$fn=20);}
module slot(l)hull(){translate([-l/2,0])circle(d=3.4,$fn=16);translate([l/2,0])circle(d=3.4,$fn=16);}
module ycyl(p,d,h)translate(p)rotate([-90,0,0])cylinder(d=d,h=h,$fn=32);
module ks(p,c=[0.95,0.95,0.95])color(c)translate(p-[8,8.5,0])cube([16,17,14]);   // keystone coupler rear, p = centre on the floor

// Bridgelink splitter, local frame: length along x (39), width along z (23), IN points +z at x=0, OUTs point -z at
// x=+-11.5, port axis y=0, back face y=+9 (towards the mounting plate), standoffs from y=9 to y=9+sd.
// rot = rotation about Y: 0 IN up, 180 IN down, 90 IN to +X, -90 IN to -X.
module splitter(p,rot,sd){translate(p)rotate([0,rot,0]){
 EARS=[[-24,-6.5],[24,6.5]];
 color([0.55,0.75,0.6])for(e=EARS)difference(){ycyl([e[0],9,e[1]],11,sd);translate([e[0],8,e[1]])rotate([-90,0,0])linear_extrude(sd+2)slot(5);}
 color("silver"){translate([-19.5,0,-11.5])cube([39,9,23]);translate([-19,-8,-11])cube([38,8,22]);
  for(e=EARS)difference(){hull(){ycyl([e[0],0,e[1]],10,9);ycyl([e[0]-sign(e[0])*8,0,e[1]],10,9);}ycyl([e[0],-1,e[1]],5,11);}
  translate([15.5,-8,-17.5])cube([4,17,6]);}
 color("gold"){rod([0,0,11.5],[0,0,23.5]);for(x=[-11.5,11.5])rod([x,0,-11.5],[x,0,-23.5]);}
}}

// ScreenBeam ECB7250 (120 x 65 x 30), vents towards the lid (-Y). flat=true: 120 along X; else 65 along X, 120 along Z.
// Cradle with four slotted tabs behind it, plate thickness 4.
module screenbeam(SB,flat=false){L=flat?[120,30,65]:[65,30,120];
 color([0.55,0.75,0.6])difference(){union(){translate([SB[0]+3,SB[1]+30,SB[2]+5])cube([L[0]-6,4,L[2]-10]);
   for(x=[SB[0]+6,SB[0]+L[0]-6],z=[SB[2]+12,SB[2]+L[2]-12])translate([x-8,SB[1]+30,z-8])cube([16,4,16]);}
  for(x=[SB[0]+6,SB[0]+L[0]-6],z=[SB[2]+12,SB[2]+L[2]-12])translate([x,SB[1]+29,z])rotate([-90,0,0])linear_extrude(6)slot(7);}
 color([0.12,0.12,0.13])translate(SB)cube(L);
 color([0.3,0.3,0.32])translate(flat?[SB[0]+30,SB[1]-0.5,SB[2]+12]:[SB[0]+12,SB[1]-0.5,SB[2]+30])cube(flat?[60,1,41]:[41,1,60]);
}
module plug45(a,dir)color([0.85,0.2,0.2])hull(){translate(a)sphere(d=10,$fn=20);translate(a+45*dir)sphere(d=10,$fn=20);}
module rj45ra(c)color([0.2,0.4,0.9])translate(c-[7,7,7])cube([14,14,14]);
