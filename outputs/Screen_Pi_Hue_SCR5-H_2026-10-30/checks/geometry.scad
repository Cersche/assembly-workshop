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
// DSI measured W=5.0; deliberately retain G conservative 8 mm envelope plus 3 mm clearance.
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
module g_plate(){difference(){union(){
  difference(){xz(0,PT)translate([0,PH/2])rr(PW,PH,2.5);window_cut();}
  for(x=BX,z=BZ)cyl_y(x,3.9,z,8,SEAT-3.9);
  leaves(); lips();
 }
 xz(-0.02,4.04)rack_slots();
 for(x=BTN_X)translate([GCX+x-HOLE[0]/2,-0.02,GCZ+HOLE[1]])cube([HOLE[0],SEAT+FT+0.04,HOLE[2]-HOLE[1]]);
 // Printed-in screw pilots (no heat-set OD assumption): nominal M2.5, fit UNKNOWN.
 for(x=BX,z=BZ)cyl_y(x,SEAT-6,z,2.1,6.02);
 // Rear engraving, 0.5 deep, left field.
 xz(3.5,0.52)translate([-75,40])mirror([1,0])text("SCR5-H",size=6,halign="center",font="Liberation Sans:style=Bold");
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
module frame(){difference(){frame_blank();
 xz(SEAT+FT-0.5,0.52)translate([GCX+62,41])rotate(90)mirror([1,0])text("SCR5-H",size=2.5,halign="center",font="Liberation Sans:style=Bold");dsi_keepout();ribbon_route();
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
// PCB centred under glass CONFIRMED; metal-frame top/bottom extent remains UNKNOWN.
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
module dsi(){translate([DSI[0],DSI[1],DSI[2]])cube([5.0,DSI[4],DSI[5]]);}
module touch(){translate([GCX-10,9.1,GCZ-5])cube([20,2,10]);} // lateral extent unmeasured
module dummy(){glass();lcd();pcb();standoffs();buttons();dsi();touch();}

// H: G front unchanged except ID and F interfaces. F rear datum Y=0 -> H plate rear Y=4.
use <D:/Projects/assembly-workshop/outputs/Screen_Pi_Hue_SCR5-H_2026-10-30/src/SCR5-H_tray.scad>
use <D:/Projects/assembly-workshop/outputs/Screen_Pi_Hue_SCR5-H_2026-10-30/src/SCR5-F_hp4lib.scad>
TRAY_DY=4;
module f_at(){translate([0,TRAY_DY,0])children();}
module plate(){
 union(){
  difference(){union(){g_plate();f_at()joint_plate_add();}
   f_at()joint_plate_cut();
   // All three Pi ports clear the G screen/window/frame; retain F dimensions.
   xz(-0.02,4.04)for(p=[[-93,26.8,15,17.5,1],[-75,26.8,15,17.5,1],[-56.3,25.6,17.5,15,1]])
    translate([p[0],p[1]])rrect2(p[2],p[3],p[4]);
   f_at()ks_box_cut();
  }
  f_at()translate([0,0.08,0])ks_golden();
 }
}
module h_floor(){difference(){f_at()floor_part();frame_access_clearance();}}
module h_deck(){difference(){f_at()deck_part();frame_access_clearance();}}
module h_pi(){f_at()pi();}
module h_hue(){f_at()hue();}
module h_fan(){f_at()fan();}
module pi_dsi(){translate([-82,83,18.825])cube([16,4,3.175]);} // inherited approximate endpoint, not measured hardware
module h_joint_tools(){f_at()joint_tools();}
// G pin travel is 2*DROP+0.5, cap face stops against plate front Y=0.
module pin_stroke(i){
 s=2*DROP+0.5;
 translate([GCX+BTN_X[i],0,GCZ])union(){
  translate([-1.5,0,0])rotate([90,0,90])linear_extrude(3)
   minkowski(){polygon([[-s-0.02,40.5],[10.2,40.5],[10.2,41.0],[11.5,41.0],[11.5+2*DROP,41.0-DROP],[15,41.0-DROP],[15,44.5],[-s-0.02,44.5]]);square([s,0.00001]);}
  translate([-2.5,-s-1.5,39.6])cube([5,1.5+s,5.8]);
 }
}
// Local access channels: diameter 6 (0.25 mm radial clearance to the 5.5 mm tool).
// Channels in the thin floor are open upward. Rear-wall roof is a short <=6 mm bridge.
module frame_access_clearance(){for(q=concat([for(x=BX,z=BZ)[x,z]],[for(sx=[-1,1],sz=[-1,1])[GCX+sx*SO[0],GCZ+sz*SO[1]]]))cyl_y(q[0],SEAT+FT,q[1],6,180);}
module screw_heads(){for(q=concat([for(x=BX,z=BZ)[x,z]],[for(sx=[-1,1],sz=[-1,1])[GCX+sx*SO[0],GCZ+sz*SO[1]]]))cyl_y(q[0],SEAT+FT,q[1],4.5,2.5);}
module screw_drivers(){for(q=concat([for(x=BX,z=BZ)[x,z]],[for(sx=[-1,1],sz=[-1,1])[GCX+sx*SO[0],GCZ+sz*SO[1]]]))cyl_y(q[0],SEAT+FT+2.5,q[1],5.5,160);}
// Route centreline. Pi DSI endpoint is inherited approximate F location, not a new measurement.
RIBBON_POINTS=[[-24,14.5,44],[-40,24,44],[-40,32,33],[-74,85,22]];
module ribbon_path(){for(i=[0:len(RIBBON_POINTS)-2])hull()for(j=[i,i+1])translate(RIBBON_POINTS[j])sphere(r=0.5,$fn=12);}
module assembly(){plate();frame();h_floor();h_deck();for(i=[0:2])placed_pin(i);}
module reference(){assembly();dummy();h_pi();h_hue();h_fan();}
