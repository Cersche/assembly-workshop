// SCR5-G; mm; FRONT view: X right, Z up, Y into rack. Glass/plate front Y=0.
// Measured values: work/screen-5in/Dimensions.md. Physical fit/strength UNKNOWN.
part="plate";
DROP=0.45; // coupon winner can be substituted here; all three pins use this DROP
LIP=0.8; LIP_ON=true;
LIP_EDGES=[true,true,false,false]; // left,right,bottom,top; Brian: side lips only, cosmetic
FRAME_STEP=1.5; // measured glass-edge inset to metal LCD frame, left/right only
SHIM=0; // moves rear frame seat and plate-boss mating face back
$fn=48;
GCX=33; GCZ=41.5; PW=252; PH=88.8; PT=4;
GW=120.7; GH=77.2; CLEAR=0.2; WW=GW+2*CLEAR; WH=GH+2*CLEAR;
SEAT=13.3+SHIM; FT=3;
SO=[56.45,34]; BTN_X=[45.5,35.5,25.5];
PCB_TOP=38; GAP=0.10; LEAF_T=0.8;
HOLE=[3.4,40.3,44.7];
BX=[GCX-68,GCX+68]; BZ=[10,72];
// DSI connector X extent is unmeasured: conservative assumed 8 mm inward from PCB edge.
DSI=[GCX-60.5,9.1,GCZ-38+30,8,5.25,21];
module xz(y,d){translate([0,y+d,0])rotate([90,0,0])linear_extrude(d)children();}
// rr/rack_slots copied from SCR5-F; same exact slot centres, outline shifted -0.05 Z to centre 44.4.
module rr(w,h,r){hull()for(x=[-w/2+r,w/2-r],z=[-h/2+r,h/2-r])translate([x,z])circle(r=r);}
module rack_slots(){for(x=[-118.2625,118.2625],z=[6.323,38.127,50.773,82.577])translate([x,z])hull()for(dx=[-1.5,1.5])translate([dx,0])circle(d=7);}
module cyl_y(x,y,z,d,h){translate([x,y,z])rotate([-90,0,0])cylinder(d=d,h=h);}
module window_cut(){
  xz(-0.02,4.04)translate([GCX,GCZ])square([WW,WH],center=true);
  // 0.3 x 45-degree chamfer, square corners, front only.
  translate([GCX,0.3,GCZ])rotate([90,0,0])
    linear_extrude(height=0.3,scale=[(WW+0.6)/WW,(WH+0.6)/WH])square([WW,WH],center=true);
}
module lips(){
  // Cosmetic side ledges only; rear frame/standoffs set depth and retain the screen.
  if(LIP_ON)for(i=[0:3])if(LIP_EDGES[i]){
    if(i<2)translate([GCX+(i==0?-WW/2:WW/2-LIP),2.5,GCZ-GH/2+4])cube([LIP,0.8,GH-8]);
    else translate([GCX-GW/2+4,2.5,GCZ+(i==2?-WH/2:WH/2-LIP)])cube([GW-8,0.8,LIP]);
  }
}
// Leaf/nub/bump geometry copied from SCR5-WP-A, translated to this glass centre.
module leaves(){for(x=BTN_X)translate([GCX+x-1.5,0,GCZ]){
  translate([0,0,PCB_TOP+GAP+0.9+0.1])cube([3,11.8,LEAF_T]);
  translate([0,10.2,PCB_TOP+GAP])cube([3,1.4,1.0+LEAF_T/2]);
  translate([0,10.4,PCB_TOP+GAP+1.0+LEAF_T])cube([3,1.0,0.9]);
}}
module plate(){difference(){union(){
  difference(){xz(0,PT)translate([0,PH/2])rr(PW,PH,2.5);window_cut();}
  for(x=BX,z=BZ)cyl_y(x,3.9,z,8,SEAT-3.9);
  leaves(); lips();
 }
 xz(-0.02,4.04)rack_slots();
 for(x=BTN_X)translate([GCX+x-HOLE[0]/2,-0.02,GCZ+HOLE[1]])cube([HOLE[0],SEAT+FT+0.04,HOLE[2]-HOLE[1]]);
 // Printed-in screw pilots (no heat-set OD assumption): nominal M2.5, fit UNKNOWN.
 for(x=BX,z=BZ)cyl_y(x,SEAT-6,z,2.1,6.02);
 // Rear engraving, 0.5 deep, left field.
 xz(3.5,0.52)translate([-75,40])mirror([1,0])text("SCR5-G",size=6,halign="center",font="Liberation Sans:style=Bold");
}}
module frame_blank(){
  // C-shaped perimeter; no material across the board centre / touch FPC.
  xz(SEAT,FT)translate([GCX,GCZ])difference(){square([132,76],center=true);square([116,60],center=true);}
  for(sx=[-1,1],sz=[-1,1])cyl_y(GCX+sx*SO[0],SEAT,GCZ+sz*SO[1],9,FT);
  for(x=BX,z=BZ)hull(){cyl_y(x,SEAT,z,8,FT);cyl_y(GCX+(x<GCX?-62:62),SEAT,z,8,FT);}
}
module dsi_keepout(){translate([DSI[0]-3,DSI[1]-3,DSI[2]-3])cube([DSI[3]+6,DSI[4]+6,DSI[5]+6]);}
module ribbon_route(){
  // Open left/up corridor 18 mm wide; extends past top of plate.
  translate([GCX-84,6.1,GCZ-11])cube([18,24,65]);
  translate([GCX-84,6.1,GCZ-11])cube([32,24,27]);
}
module frame(){difference(){frame_blank();dsi_keepout();ribbon_route();
 for(sx=[-1,1],sz=[-1,1])cyl_y(GCX+sx*SO[0],SEAT-0.02,GCZ+sz*SO[1],2.8,FT+0.04);
 for(x=BX,z=BZ)cyl_y(x,SEAT-0.02,z,2.8,FT+0.04);
}}
// Pin polygon/cap/notch/dot design copied unchanged from SCR5-WP-A.
module pin(d,dots){s=2*d+0.5;difference(){union(){
 translate([-1.5,0,0])rotate([90,0,90])linear_extrude(3)polygon([
 [-s-0.02,40.5],[10.2,40.5],[10.2,41.0],[11.5,41.0],[11.5+2*d,41.0-d],[15,41.0-d],[15,44.5],[-s-0.02,44.5]]);
 translate([-2.5,-s-1.5,39.6])cube([5,1.5,5.8]);
 }for(i=[0:dots-1])translate([(i-(dots-1)/2)*1.4,-s-1.5-0.01,43.5])rotate([-90,0,0])cylinder(d=0.9,h=0.4);}}
module placed_pin(i){translate([GCX+BTN_X[i],0,GCZ])pin(DROP,i+1);}
// Measured layers: cover glass 0.9 + second glass 1.6, metal frame 3.0,
// open gap 2.0, PCB 1.6. Metal frame inset ~1.5 at LEFT/RIGHT only.
// PCB centred under glass and full metal-frame top/bottom extent remain UNKNOWN.
module glass(){translate([GCX-GW/2,0,GCZ-GH/2])cube([GW,2.5,GH]);}
module lcd(){
  translate([GCX-GW/2+FRAME_STEP,2.5,GCZ-GH/2])cube([GW-2*FRAME_STEP,3.0,GH]);
}
module pcb(){translate([GCX-60.5,7.5,GCZ-38])cube([121,1.6,76]);}
module standoffs(){for(sx=[-1,1],sz=[-1,1])difference(){cyl_y(GCX+sx*SO[0],9.1,GCZ+sz*SO[1],5.5,4.2);cyl_y(GCX+sx*SO[0],9.08,GCZ+sz*SO[1],2.5,4.24);}}
module buttons(){for(x=BTN_X){
 translate([GCX+x-3.5,9.1,GCZ+38-3.4])cube([7,3.6,2.4]);
 translate([GCX+x-1.5,9.1,GCZ+37])cube([3,3.6,1]);
}}
module dsi(){translate([DSI[0],DSI[1],DSI[2]])cube([DSI[3],DSI[4],DSI[5]]);}
module touch(){translate([GCX-10,9.1,GCZ-5])cube([20,2,10]);} // lateral extent unmeasured
module dummy(){glass();lcd();pcb();standoffs();buttons();dsi();touch();}
module assembly(){color("gray")plate();color("orange")frame();for(i=[0:2])color("cyan")placed_pin(i);color([0.2,0.3,0.4,0.4])dummy();}
if(part=="plate")plate();else if(part=="frame")frame();
else if(part=="pin1"||part=="pin2"||part=="pin3")pin(DROP,part=="pin1"?1:part=="pin2"?2:3);
else if(part=="assembly")assembly();else if(part=="dummy")dummy();
