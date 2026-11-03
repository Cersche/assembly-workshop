// Exploration only, NOT a revision: Pi / Hue swap concepts around SCR5-H11. mm, plate frame (rear face Y 4). Claude 2026-11-03.
// opt: "S1" Pi on top, ports through the plate, keystone low. "S2" Pi on top turned round, ports to the rear, keystone stays.
//      "S3" Pi on top, ports through the plate, keystone on its side above them, deck 3.5 lower, two M6 right of the keystone.
//      "N" no swap, Hue on the deck moved forward and right. "C" = S1 with no keystone. "N2" no swap, no keystone, Hue forward, centred as H11. Fit, strength and sag UNKNOWN.
use <../../outputs/Screen_Pi_Hue_SCR5-H11_2026-11-03/src/SCR5-H.scad>
use <../../outputs/Screen_Pi_Hue_SCR5-H11_2026-11-03/src/SCR5-F_hp4lib.scad>
opt="S2"; part="floor";
$fn=40;
swap=opt!="N"&&opt!="N2";
s3=opt=="S3";
bar=opt=="S1"||opt=="C"||s3;       // M6 row on a cross bar above the Pi ports
ks=opt!="C"&&opt!="N2";         // C and N2: keystone omitted (Brian 2026-11-03), third M6 joint comes back
floor_z=swap?5.8:8.225; floor_top=floor_z+3;
deck_z=s3?37:40.5; deck_top=deck_z+3;
x0=-105; x1=opt=="N2"?-6:16.5; zone_x=-43;
hue_cx=opt=="N2"?-54.4:-34; hue_cy=swap?68.5:81.5;
rear=hue_cy+45;
right_y=opt=="N"?40:opt=="N2"?34:21;
pi_px=-102; pi_py=opt=="S2"?21:4;
pi_zb=bar?deck_top+4:opt=="S2"?49.5:17.225;  // S1 uses 4 mm standoffs to win height for the M6 row
joint_x=s3?[-64.5,-50]:ks?[-71,-50]:[-92,-71,-50]; jz=s3?75:bar?77.5:64.5;
tab_y0=12.3; tab_y1=18.3;
tab_base=bar?68:deck_top;
ks_x=opt=="S1"?-91.5:-92.5; ks_dz=opt=="S1"?-43:0;
rail_x=opt=="S1"?[-74,-60,-47]:[-88,-74,-60]; rail_y1=swap?20.5:28;
ledge_top=floor_z-0.15;
fan_y=opt=="S2"?60:46; fan_z=s3?53:bar?57:opt=="S2"?60:28.7;
ports=[[9,26.8,15,17.5],[27,26.8,15,17.5],[45.7,25.6,17.5,15]];
KSX=-91.75; KSZ=75;  // S3 keystone centre, turned on its side: window 33.5 wide x 21 tall
module outline(){offset(r=6)offset(delta=-6)union(){translate([x0,4])square([zone_x-x0,rear-4]);translate([zone_x-.01,right_y])square([x1-zone_x+.01,rear-right_y]);}
 translate([x0,4])square([6,6]);translate([zone_x-6,4])square([6,6]);}
module slab(z){translate([0,0,z])linear_extrude(3)outline();}
module box(a,b){translate(a)cube([b[0]-a[0],b[1]-a[1],b[2]-a[2]]);}
module plate(){difference(){union(){
  g_plate();
  for(x=joint_x){translate([x,4,jz])rotate([-90,0,0])cylinder(d=14,h=8);
   box([x-6,4,tab_base+0.5],[x+6,11,tab_base+3.5]);}
  intersection(){translate([-106.5,4,25])rotate([-90,0,0])cylinder(d=9,h=8);box([-110.85,3,0],[-90,13,60]);}
  box([x0,3.99,ledge_top-3],[-43,30,ledge_top]);
  for(x=[-103,-81,-67,-53,-44.5])hull(){box([x-1.5,3.99,.5],[x+1.5,4,ledge_top-3]);box([x-1.5,29,ledge_top-3.1],[x+1.5,30,ledge_top-3]);}
  for(x=rail_x){box([x-1.5,3.99,ledge_top-.01],[x+1.5,rail_y1,floor_top+1.775]);box([x-4,3.99,floor_top+.175],[x+4,rail_y1,floor_top+1.775]);}
 }
 for(x=joint_x)translate([x,3.9,jz])rotate([-90,0,0])cylinder(d=7.6,h=8.2);
 translate([-106.5,8,25])rotate([-90,0,0])cylinder(d=4.2,h=4.1);
 if(opt!="S2")for(p=ports)translate([pi_px+p[0]-p[2]/2,-.1,p[1]-17.225+pi_zb-p[3]/2])cube([p[2],4.2,p[3]]);
 if(s3)translate([KSX-16.75,-.02,KSZ-10.5])cube([33.5,4.1,21]);
 else if(ks)translate([ks_x-10.5,-.02,66+ks_dz-15])cube([21,4.1,33.5]);
 }
 if(s3)translate([KSX,4.08,KSZ])rotate([0,90,0])translate([92.5,0,-67.75])ks_golden();
 else if(ks)translate([ks_x+92.5,4.08,ks_dz])ks_golden();
}
module pilaster(){box([-111.5,12.3,floor_z],[-105+.01,21.3,deck_z]);}
module floor_part(){difference(){union(){
  slab(floor_z);
  if(swap){
   box([x0,12.3,floor_top-.01],[x0+3,rear,deck_z]);                      // outer wall, no window: nothing on this side needs a port
   box([-84.5,opt=="S1"?18:4.2,floor_top-.01],[-82,rear,deck_z]);        // lane wall left of the Hue, replaces the H11 inner wall
   box([x1-2.5,right_y+6,floor_top-.01],[x1,rear,deck_z]);               // right wall
   box([x0,rear-3,floor_top-.01],[-84.5,rear,deck_z]);                   // rear wall of the lane; Hue rear stays open
   hc();
  }else{
   box([x0,12.3,floor_top-.01],[x0+3,67,deck_z]);box([x0,90,floor_top-.01],[x0+3,rear,deck_z]);
   box([-46,4.2,floor_top-.01],[-43,92,deck_z]);
   box([x1-2.5,right_y+6,floor_top-.01],[x1,rear,deck_z]);box([x0,rear-3,floor_top-.01],[x1,rear,floor_top+4]);
   for(p=[[3.5,3.5],[61.5,3.5],[3.5,52.5],[61.5,52.5]])translate([pi_px+p[1],pi_py+85-p[0],floor_top])cylinder(d=7,h=6);
  }
  pilaster();
 }
 for(x=rail_x)box([x-1.8,3.9,floor_z-.1],[x+1.8,rail_y1+.4,floor_top+.1]);
 translate([-106.5,12,25])rotate([-90,0,0])cylinder(d=3.4,h=10);
 if(opt=="S1")box([ks_x-10.5,3.9,floor_z-.1],[ks_x+10.5,18,deck_z]);
 if(!swap)box([-46.1,33,21],[-42.9,41,deck_z+1]);
}}
module cradle_mesh(z,clipr){intersection(){translate([hue_cx,hue_cy,z-3-.045])intersection(){import("C:/Users/brian/Downloads/Swanky Rottis.stl",convexity=6);translate([-50,-50,3])cube([100,100,40]);}
  box([-200,0,-5],[200,clipr,120]);}}
// swap: cradle on the floor, rear posts removed so the Hue slides in from behind; front posts run on up and tie to the deck.
module hc(){cradle_mesh(floor_top,hue_cy+28);
 for(x=[hue_cx-44.5,hue_cx+44.5])translate([x,hue_cy-44.5,floor_top])cylinder(d=6,h=deck_z-floor_top);}
module tabs(){for(x=joint_x)difference(){union(){
  translate([0,tab_y1,0])rotate([90,0,0])linear_extrude(6)hull(){translate([x-10,tab_base-.01])square([20,1]);translate([x,jz])circle(d=20);}
  box([x-10,4.5,tab_base-.01],[x+10,tab_y1,tab_base+5]);}
 translate([x,tab_y1+.1,jz])rotate([90,0,0])cylinder(d=6.6,h=15);
 translate([x,tab_y1+.1,jz])rotate([90,0,0])cylinder(d=11.5,h=3.6);
 box([x-6.15,4,tab_base+.35],[x+6.15,11.15,tab_base+3.65]);}}
module deck_part(){difference(){union(){
  slab(deck_z);tabs();
  if(bar){  // side walls up to a cross bar that carries the M6 tabs; Pi ports pass under it
   box([x0,4.2,deck_top-.01],[x0+3,66,s3?63:78]);box([x0,90,deck_top-.01],[x0+3,rear,60]);
   box([-46,4.2,deck_top-.01],[-43,92,s3?68:78]);
   box([s3?-74.5:x0,tab_y0,s3?65:68],[-43,tab_y1,78]);
   if(s3)box([-74.5,tab_y1-.01,65],[-45.99,50,68]);  // roof over the Pi ties the bar to the right wall, below the screw line so a driver and the heads reach the M6s
  }
  if(opt=="S2"){
   box([x0,34,deck_top-.01],[x0+3,86,76]);        // short outer wall, fan mount clips to it
   box([-46,40,deck_top-.01],[-43,rear-3,58]);    // rib; HDMI and audio walled off, USB-C free
  }
  if(!swap)cradle_mesh(deck_top,rear);
 }
 if(bar)for(x=joint_x){translate([x,tab_y1+.1,jz])rotate([90,0,0])cylinder(d=6.6,h=15);translate([x,tab_y1+.1,jz])rotate([90,0,0])cylinder(d=11.5,h=3.6);}
 if(swap)translate([-33,hue_cy,deck_z-.1])cylinder(d=20,h=3.2);  // finger hole over the Hue button
 if(opt=="S1")box([ks_x-10.5,3.9,deck_z-.1],[ks_x+10.5,16,deck_top+.1]);
}
 if(opt=="S2")for(p=[[3.5,3.5],[61.5,3.5],[3.5,52.5],[61.5,52.5]])translate([pi_px+56-p[1],pi_py+p[0],deck_top])difference(){cylinder(d=7,h=6);cylinder(d=3.2,h=6.1);}
 if(bar)for(p=[[3.5,3.5],[61.5,3.5],[3.5,52.5],[61.5,52.5]])translate([pi_px+p[1],pi_py+85-p[0],deck_top])difference(){cylinder(d=7,h=4);cylinder(d=3.2,h=4.1);}
}
// Pi from the published board layout: board x 0..85 with USB at x=85, y 0..56 with USB-C/HDMI at y=0.
module pi(){zb=pi_zb;
 m=opt=="S2"?[[0,-1,0,pi_px+56],[1,0,0,pi_py],[0,0,1,zb],[0,0,0,1]]:[[0,1,0,pi_px],[-1,0,0,pi_py+85],[0,0,1,zb],[0,0,0,1]];
 multmatrix(m){
  box([0,0,0],[85,56,1.6]);
  for(y=[9,27])box([70,y-6.6,1.6],[87,y+6.6,17.6]);
  box([65,37.75,1.6],[87,53.75,15.1]);
  box([6.7,-1.5,1.6],[15.7,6,4.8]);for(x=[26,39.5])box([x-3.5,-1.5,1.6],[x+3.5,6.5,4.6]);box([51,0,1.6],[57,12,7.6]);
  box([7.1,50,1.6],[57.9,55,10.1]);box([2.5,19,1.6],[6.5,37,7.1]);box([43,19,1.6],[47,37,7.1]);
  box([22.5,25,1.6],[37.5,40,4]);box([-2.5,20,-1.4],[15,36,0]);
 }}
module hue(){z=swap?floor_top+.1:deck_top+.1;translate([hue_cx,hue_cy,z]){linear_extrude(26)offset(r=12)square([66.7,66.4],center=true);translate([0,0,25.9])cylinder(d=26,h=.7);}}
module fan(){box([x0-15,fan_y-20,fan_z-20],[x0-5,fan_y+20,fan_z+20]);}
module mount(){difference(){
 union(){z0=fan_z-23;z1=fan_z+23;box([x0-5,fan_y-22,z0],[x0-.1,fan_y+22,z1]);
  zl=swap?deck_z:floor_z;zt=s3?63:bar?78:opt=="S2"?76:deck_top;
  box([x0-.11,fan_y-14,z0],[x0+4,fan_y+22,zl-.1]);
  for(s=[-22,13])box([x0-.11,fan_y+s,zt+.1],[x0+2.7,fan_y+s+9,zt+2.5]);}
 translate([x0-5.1,fan_y,fan_z])rotate([0,90,0])cylinder(d=38,h=5.2);}}
module ks_path(){if(s3)box([KSX-11,4,KSZ-8],[KSX+11,38,KSZ+8]);else if(ks)translate([ks_x-6,0,60+ks_dz])cube([12,38,12]);}
RIB=s3?[[-24,18.5,44],[-38,24,44],[-46,34,48.5],[-58,60,49.5],[-74,85,49.5]]:opt=="S2"?[[-24,18.5,44],[-38,24,50],[-46,24,55],[-66,23,56],[-74,25.5,53]]:bar?[[-24,18.5,44],[-38,24,47],[-46,34,52],[-58,60,53],[-74,85,53]]:[[-24,18.5,44],[-40,28,44],[-40,34,33],[-44.5,41,30],[-74,89,22]];
module ribbon(){for(i=[0:len(RIB)-2])hull(){translate(RIB[i])sphere(r=.5,$fn=10);translate(RIB[i+1])sphere(r=.5,$fn=10);}}
if(part=="plate")plate();if(part=="floor")floor_part();if(part=="deck")deck_part();if(part=="pi")pi();if(part=="hue")hue();
if(part=="fan")fan();if(part=="mount")mount();if(part=="ks")ks_path();if(part=="ribbon")ribbon();
