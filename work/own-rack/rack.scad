// Own rack system, DRAFT concept (Brian 2026-11-09). Viewer only, unprinted; fit and strength UNKNOWN.
// Frame as the faceplate parts: X centred, Y=0 front face of the front post flange, Y=240 rear, Z=0 bottom of U1.
// Interface kept from the Lab Rax posts: flange Y 0..6 from X 111.12, side wall inner face X 127.12,
// post 35 deep, outer face X 141.12, holes X +/-118.2625 at U centre and +/-15.902, depth 240.
include <workshop.scad>
part="all";
rack_u=9; seg_u=3;
bezel=true;          // post front steps 4 forward beside the faceplates, so plates sit flush in a rounded frame
depth=240; xi=111.12; xw=127.12; xo=141.12; pd=35; ft=6;
r_out=10; r_in=4; H=24; r_top=5; pt=4;
yf=bezel?-ws_plate_t:0;
ZT=rack_u*ws_pitch;
end_xy=[[133.12,12],[133.12,27]];                 // M6 into each post end
pan_xy=[[30,15.5],[95,15.5],[119.2,60],[119.2,105]]; // M6 panel screws, per corner bracket
$fn=64;

module mask2d(){hull(){translate([xo-r_out,yf+r_out])circle(r_out);translate([xo-5,pd-5])circle(5);translate([90,yf])square([1,pd-yf]);}}
module post2d(){intersection(){
  union(){
    offset(r=1.5)offset(delta=-1.5)offset(r=-r_in)offset(delta=r_in)union(){translate([xi,0])square([xo-xi,ft]);translate([xw,0])square([xo-xw,pd]);}
    if(bezel)translate([ws_plate_w/2+0.6,yf])square([xo-ws_plate_w/2-0.6,1-yf]);
  }
  mask2d();}}
module post(u){difference(){
  linear_extrude(u*ws_pitch)post2d();
  for(i=[0:u-1],dz=[-ws_hole_dz,0,ws_hole_dz])translate([ws_hole_x,ft,i*ws_pitch+ws_pitch/2+dz])rotate([90,0,0])ws_insert_bore(ws_insert_m6,ft+0.02);
  for(p=end_xy){translate([p[0],p[1],0])ws_insert_bore(ws_insert_m6,7);translate([p[0],p[1],u*ws_pitch])mirror([0,0,1])ws_insert_bore(ws_insert_m6,7);}
}}

// 2D shape with its top edge rounded
module puck(h,r,n=6){linear_extrude(h-r)children();
  for(i=[0:n-1])hull()for(a=[90*i/n,90*(i+1)/n])translate([0,0,h-r+r*sin(a)-(a>89?0.01:0)])linear_extrude(0.01)offset(delta=-r*(1-cos(a)))children();}
module corner2d(x0,y1){hull(){translate([xo-r_out,yf+r_out])circle(r_out);translate([x0,yf])square([1,y1-yf]);translate([xo-1,y1-1])square(1);}}
module panel2d(){hull()for(sx=[-1,1],y=[9.2+6,depth-9.2-6])translate([sx*(125-6),y])circle(6);}
module panel(){difference(){linear_extrude(pt)panel2d();
  for(sx=[-1,1],p=pan_xy,y=[p[1],depth-p[1]])translate([sx*p[0],y,-1])cylinder(d=ws_m6_clear,h=pt+2);}}
// top front-right corner bracket, Z=0 on the post end
module bracket(){difference(){
  union(){
    intersection(){puck(H,r_top)corner2d(113.12,depth/2+10);translate([0,-50,-1])cube([200,50+depth/2,H+2]);}
    intersection(){puck(H,r_top)corner2d(-10,22);translate([0,-50,-1])cube([200,200,H+2]);}
  }
  translate([0,0,H-pt])linear_extrude(pt+1)offset(delta=0.2)panel2d();
  for(p=end_xy)translate([p[0],p[1],0]){translate([0,0,-1])cylinder(d=ws_m6_clear,h=H+2);translate([0,0,5])cylinder(d=ws_m6_head_d,h=H);}
  for(p=pan_xy)translate([p[0],p[1],H-pt])mirror([0,0,1])ws_insert_bore(ws_insert_m6,7);
}}
module four(){for(sx=[0,1],sy=[0,1])mirror([sx,0,0])translate([0,sy*depth,0])mirror([0,sy,0])children();}
module ends(){translate([0,0,ZT])children();mirror([0,0,1])children();}

if(part=="posts"||part=="all")four()for(k=[0:rack_u/seg_u-1])translate([0,0,k*seg_u*ws_pitch])post(seg_u);
if(part=="corner_brackets"||part=="all")ends()four()bracket();
if(part=="top_bottom_panels"||part=="all")ends()translate([0,0,H-pt])panel();
if(part=="example_faceplates"||part=="all")for(k=[0:2])translate([0,0,k*3*ws_pitch]){ws_plate(1);translate([0,0,ws_pitch])ws_plate(2);}
