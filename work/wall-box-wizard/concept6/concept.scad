color([0.92,0.91,0.87])import("body.stl");
module run(p,d=6.8)for(i=[0:len(p)-2])hull(){translate(p[i])sphere(d=d,$fn=14);translate(p[i+1])sphere(d=d,$fn=14);}
module rod(a,b,c="silver")color(c)hull(){translate(a)sphere(d=9.5,$fn=20);translate(b)sphere(d=9.5,$fn=20);}
module slot(l)hull(){translate([-l/2,0])circle(d=3.4,$fn=16);translate([l/2,0])circle(d=3.4,$fn=16);}
module xcyl(p,d,h)translate(p)rotate([0,90,0])cylinder(d=d,h=h,$fn=32);
// keystone F couplers on the left wall: IN (top) and EXIT to the modem (bottom)
color([0.95,0.95,0.95]){translate([2.5,27,126])cube([14,16,17]);translate([2.5,39,22])cube([14,16,17]);}

// Bridgelink splitter from Brian's ruler photos (2026-10-26, estimates ~±1 mm): back face on the standoffs at X=17,
// body 39 (Y) x 23 (Z) x 17 thick (X: 9 base + 8 top box), F port axis 9 above the back (X=26), IN up centred,
// OUTs down 23 apart, ears at opposite corners (holes 48 apart in Y, 13 in Z), ground screw block by the upper-Y end.
sy=35; sz=81; bx=17; ax=bx+9;
EARS=[[sy-24,sz-6.5],[sy+24,sz+6.5]];
// slotted standoffs from the left wall up to the ear holes (M3 into inserts; slot lets the chain find its place)
color([0.55,0.75,0.6])for(e=EARS)difference(){xcyl([2.5,e[0],e[1]],11,bx-2.5);
 translate([1,e[0],e[1]])rotate([0,90,0])linear_extrude(bx)rotate(90)slot(5);}
color("silver"){
 translate([bx,sy-19.5,sz-11.5])cube([9,39,23]);
 translate([ax,sy-19,sz-11])cube([8,38,22]);
 for(e=EARS)difference(){hull(){xcyl([bx,e[0],e[1]],10,9);xcyl([bx,e[0]+(e[0]<sy?8:-8),e[1]],10,9);}
  xcyl([bx-1,e[0],e[1]],5,11);}
 translate([bx,sy+19.5,sz-11.5])cube([17,4,6]);
}
color("gold"){rod([ax,sy,sz+11.5],[ax,sy,sz+23.5]);for(dy=[-11.5,11.5])rod([ax,sy+dy,sz-11.5],[ax,sy+dy,sz-23.5]);}
rod([16.5,35,134.5],[ax,35,134.5]);rod([ax,35,134.5],[ax,35,sz+23.5]);          // IN: keystone -> right-angle -> down into splitter IN
rod([ax,sy+11.5,sz-23.5],[ax,sy+11.5,30.5]);rod([ax,sy+11.5,30.5],[16.5,sy+11.5,30.5]);  // EXIT: OUT 2 -> right-angle -> exit keystone

// ScreenBeam lying flat, cradle behind it (slotted tabs)
color([0.55,0.75,0.6])difference(){union(){translate([54,64,48])cube([116,4,69]);for(x=[62,162],z=[40,125])translate([x-8,64,z-8])cube([16,4,16]);}
 for(x=[62,162],z=[40,125])translate([x,63,z])rotate([-90,0,0])linear_extrude(6)if(z>100)slot(9);else rotate(90)slot(9);}
color([0.12,0.12,0.13])translate([52,34,50])cube([120,30,65]);
color([0.3,0.3,0.32])translate([82,33.5,65])cube([60,1,35]);
rod([42,49,70],[52,49,70]);rod([42,49,70],[42,49,58]);                // right-angle F on the ScreenBeam coax, pointing down
color([0.15,0.15,0.15])run([[ax,sy-11.5,sz-24],[ax+2,24,46],[40,40,44],[42,49,52]]);   // OUT 1 jumper -> ScreenBeam
// right end: Ethernet (right-angle) -> right keystone; power plug 45 mm straight out, U-turn, back left over the top, out the left wall
color([0.2,0.4,0.9])translate([172,41,94])cube([14,15,13]);
color([0.95,0.95,0.95])translate([218,40,85])cube([20,20,30]);
color([0.85,0.2,0.2])translate([172,49,72])rotate([0,90,0])cylinder(d=10,h=45,$fn=24);
color([0.15,0.15,0.15]){run([[186,48,100],[218,46,100]],6);
 run([[217,49,72],[226,50,76],[229,52,90],[222,56,128],[200,58,132],[60,59,132],[34,59,110],[5,59,102.5]],4);}
color([0.55,0.75,0.6])translate([36,55,104])cube([12,8,12]);   // strain-relief clamp
