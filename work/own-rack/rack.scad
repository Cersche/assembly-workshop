// Own rack system, DRAFT 3 concept (Brian 2026-11-11). Viewer only, unprinted; fit and strength UNKNOWN.
// Frame as the faceplate parts: X centred, Y=0 front face of the front post flange, Y=240 rear, Z=0 bottom of the lowest U.
// U standard kept from the Lab Rax posts: 44.45 per U, holes X +/-118.2625 at U centre and +/-15.902,
// flange Y 0..6 from X 111.12, side wall inner face X 127.12, post 35 deep, outer face X 141.12, depth 240.
// Hardware: M6 x 10 button head + M6 x 5 x 8 heat-set inserts. Fan: 4 x M3 x 40 countersunk (new length, ask Brian).
// Brian's picks 2026-11-09: look B, joint 1 (4U + 1U + 4U), fan on top under a rounded shroud, 0.3 bezel gap top and bottom,
// rack-side cleat only (wall half later).
include <workshop.scad>
part="all";
look="B";            // B: 15 mm corners, accent strips, shadow lines, screw caps.  A: 10 mm corners, plain
joint=1;             // 1: 4U + 1U extension + 4U.  2: 5U + 4U with a built-in tab
explode=0;
xoff=0;
rack_u=9;
bg=0.3;              // gap between the top/bottom faceplate edge and the corner brackets; U positions do not move
depth=240; xi=111.12; xw=127.12; xo=141.12; pd=35; ft=6;
r_out=look=="B"?15:10; r_in=4; H=24; r_top=5; pt=4; TABH=20; jx=134.12;
yf=-ws_plate_t;      // flush bezel: post front steps forward by the plate thickness
ZT=rack_u*ws_pitch;
end_xy=[[133.12,12],[133.12,27]];                     // M6 into each plain post end
pan_xy=[[30,13.6],[108,13.6],[119.2,60],[119.2,105]]; // M6 panel screws, per corner bracket
cleat_x=[25,65,105];                                  // M6 inserts in the rear top brackets' rear face
fan=[195,155,186];   // CT200: frame, hole square, opening (Thermaltake drawing; not measured)
// Brian 2026-11-11: the fan does NOT stick out. It hangs under the top panel, whose grille is flush with the rack top.
// The top brackets are taller (Ht) so the whole fan sits above the U stack: nothing enters slot 1.
ptt=6;               // top panel thickness: room for M3 inserts, M3 x 35 from below through the fan
Ht=ptt+30+2;         // top bracket height: panel + fan + 2 spare
$fn=64;

module mask2d(){hull(){translate([xo-r_out,yf+r_out])circle(r_out);translate([xo-0.6,pd-0.6])circle(0.6);translate([90,yf])square([1,pd-yf]);}}
module post2d(){intersection(){
  union(){
    offset(r=1.5)offset(delta=-1.5)offset(r=-r_in)offset(delta=r_in)union(){translate([xi,0])square([xo-xi,ft]);translate([xw,0])square([xo-xw,pd]);}
    translate([ws_plate_w/2+0.6,yf])square([xo-ws_plate_w/2-0.6,1-yf]);
  }
  mask2d();}}
module tab2d(){intersection(){post2d();translate([120,17.5])square([30,30]);}}
// joint screw, driven from the post's rear face; the side panel tongue hides the head
module jscrew_tab(z){translate([jx,0,z])rotate([-90,0,0]){translate([0,0,17])cylinder(d=ws_m6_clear,h=20);translate([0,0,21.5])cylinder(d=ws_m6_head_d,h=20);}}
module jscrew_ins(z){translate([jx,17.5,z])rotate([90,0,0])ws_insert_bore(ws_insert_m6,6.5);}
// post segment; top/bot: 0 plain end (runs bg past the U stack to meet the bracket), 1 tab, -1 notch
module seg(u,top=0,bot=0){h=u*ws_pitch;difference(){
  union(){linear_extrude(h)post2d();
    if(top==0)translate([0,0,h])linear_extrude(bg)post2d();
    if(bot==0)translate([0,0,-bg])linear_extrude(bg)post2d();
    if(top==1)translate([0,0,h])linear_extrude(TABH)tab2d();
    if(bot==1)translate([0,0,-TABH])linear_extrude(TABH)tab2d();}
  for(i=[0:u-1],dz=[-ws_hole_dz,0,ws_hole_dz])translate([ws_hole_x,ft,i*ws_pitch+ws_pitch/2+dz])rotate([90,0,0])ws_insert_bore(ws_insert_m6,ft+0.02);
  if(top==-1){translate([120,17.3,h-TABH-0.2])cube([30,30,TABH+1]);jscrew_ins(h-TABH/2);}
  if(bot==-1){translate([120,17.3,-1])cube([30,30,TABH+1.2]);jscrew_ins(TABH/2);}
  if(top==1)jscrew_tab(h+TABH/2);
  if(bot==1)jscrew_tab(-TABH/2);
  for(p=end_xy){if(top==0)translate([p[0],p[1],h+bg])mirror([0,0,1])ws_insert_bore(ws_insert_m6,7);if(bot==0)translate([p[0],p[1],-bg])ws_insert_bore(ws_insert_m6,7);}
  translate([136.92,30.9,-TABH-1])cube([2.4,5,h+2*TABH+2]);       // side panel groove
  if(look=="B"){
    translate([xo-1.2,12,-TABH-1])cube([2,8,h+2*TABH+2]);          // accent strip channel
    for(z=[0,h-0.5])translate([0,0,z])linear_extrude(0.5)intersection(){difference(){offset(delta=5)post2d();offset(delta=-1)post2d();}translate([127.5,-10])square([30,60]);}
  }
}}
module post_stack(){e=explode;
  if(joint==2){seg(5,top=1);translate([0,0,5*ws_pitch+e])seg(4,bot=-1);}
  else{seg(4,top=-1);translate([0,0,4*ws_pitch+e])seg(1,top=1,bot=1);translate([0,0,5*ws_pitch+2*e])seg(4,bot=-1);}}

// 2D shape with its top edge rounded
module puck(h,r,n=6){linear_extrude(h-r)children();
  for(i=[0:n-1])hull()for(a=[90*i/n,90*(i+1)/n])translate([0,0,h-r+r*sin(a)-(a>89?0.01:0)])linear_extrude(0.01)offset(delta=-r*(1-cos(a)))children();}
module corner2d(x0,y1){hull(){translate([xo-r_out,yf+r_out])circle(r_out);translate([x0,yf])square([1,y1-yf]);translate([xo-1,y1-1])square(1);}}
module panel2d(){hull()for(sx=[-1,1],y=[9.2+6,depth-9.2-6])translate([sx*(125-6),y])circle(6);}
module fan_holes(){for(sx=[-1,1],sy=[-1,1])translate([sx*fan[1]/2,sy*fan[1]/2,0])children();}
module panel(with_fan=false,t=pt){difference(){linear_extrude(t)panel2d();
  for(sx=[-1,1],p=pan_xy,y=[p[1],depth-p[1]])translate([sx*p[0],y,-1])cylinder(d=ws_m6_clear,h=t+2);
  if(with_fan)translate([0,depth/2,0]){translate([0,0,-1])cylinder(d=fan[2],h=t+2,$fn=128);
    fan_holes()ws_insert_bore(ws_insert_m3,5);}}                     // M3 inserts from below, 1 mm skin on top
  if(with_fan)translate([0,depth/2,t-3])linear_extrude(3){           // grille, flush with the top
    for(r=[31,62])difference(){circle(r+1.2);circle(r-1.2);}
    for(a=[45,135])rotate(a)square([fan[2]+2,2.4],center=true);}}
module fan_standin(){difference(){linear_extrude(30)offset(r=12)square(fan[0]-24,center=true);translate([0,0,-1])cylinder(d=fan[2],h=32,$fn=128);
  fan_holes()translate([0,0,-1])cylinder(d=4.3,h=32);}}
// corner bracket, drawn as the top front-right one, Z=0 on the post end. h tall, pocket for a panel t thick.
// cleat=true adds the rear-face inserts
module bracket(cleat=false,h=H,t=pt){difference(){
  union(){
    intersection(){puck(h,r_top)corner2d(113.12,depth/2+10);translate([0,-50,-1])cube([200,50+depth/2,h+2]);}
    intersection(){puck(h,r_top)corner2d(-10,21);translate([0,-50,-1])cube([200,200,h+2]);}
  }
  translate([0,0,h-t])linear_extrude(t+1)offset(delta=0.2)panel2d();
  for(p=end_xy)translate([p[0],p[1],0]){translate([0,0,-1])cylinder(d=ws_m6_clear,h=h+2);translate([0,0,4])cylinder(d=ws_m6_head_d,h=h);}   // M6 x 10: 4 web, 6 into the insert
  for(p=pan_xy)translate([p[0],p[1],h-t])mirror([0,0,1])ws_insert_bore(ws_insert_m6,7);
  if(cleat)for(x=cleat_x)translate([x,yf,h/2])rotate([-90,0,0])ws_insert_bore(ws_insert_m6,7);
}}
// flush side panel half: drops into the post grooves from above before the top brackets go on
module side_panel(lower){hz=ZT/2+bg;difference(){
  union(){translate([137.12,35.3,0])cube([4,169.4,hz]);translate([137.12,31.3,0])cube([2,177.4,hz]);}
  if(lower)for(y=[55:10:185])hull()for(z=[14,76])translate([130,y,z])rotate([0,90,0])cylinder(d=4,h=20,$fn=16);}}
// rack half of the wall cleat: bolts to the rear top brackets (4 x M6) and the rear posts' top holes (2 x M6).
// 45 deg hook along the bottom, pointing down at the wall side. The wall half comes later.
// The bar sits on the taller top brackets only, so it covers none of the rear U1 opening; two ears reach down to the posts.
cl_t=12; cz0=ZT-4; czt=ZT+bg+Ht-5; cl_w=252; ear_z=8*ws_pitch+ws_pitch/2+ws_hole_dz-9;
module m6_from_rear(web){rotate([-90,0,0]){translate([0,0,-1])cylinder(d=ws_m6_clear,h=40);translate([0,0,web])cylinder(d=ws_m6_head_d,h=40);}}
module cleat_rack(){difference(){
  union(){
    translate([-cl_w/2,0,0])rotate([90,0,90])linear_extrude(cl_w)polygon([[depth+4,cz0+cl_t],[depth+4+cl_t,cz0],[depth+4+cl_t,czt],[depth+4,czt]]);
    for(sx=[0,1])mirror([sx,0,0]){translate([111.6,depth,ear_z])cube([14.4,4.1,ZT-0.2-ear_z]);          // pads in the post bezel recess
      translate([111.6,depth+4,ear_z])cube([14.4,cl_t,cz0+cl_t-ear_z+1]);}                                // ears
  }
  for(sx=[-1,1])translate([sx*ws_hole_x,depth,8*ws_pitch+ws_pitch/2+ws_hole_dz])m6_from_rear(4);
  for(sx=[-1,1],x=cleat_x)translate([sx*x,depth+4,ZT+bg+Ht/2])m6_from_rear(4);
}}
module four(){for(sx=[0,1],sy=[0,1]){$rear=sy;mirror([sx,0,0])translate([0,sy*depth,0])mirror([0,sy,0])children();}}
function on(p)=part==p||part=="all";

translate([xoff,0,0]){
if(on("posts"))four()post_stack();
if(part=="joint")post_stack();
if(on("corner_brackets")){translate([0,0,ZT+bg])four()bracket($rear==1,Ht,ptt);mirror([0,0,1])translate([0,0,bg])four()bracket();}
if(on("top_fan_panel"))translate([0,0,ZT+bg+Ht-ptt])panel(true,ptt);
if(on("bottom_panel"))translate([0,0,-H-bg])panel();
if(on("side_panels"))for(sx=[0,1])mirror([sx,0,0]){translate([0,0,-bg])side_panel(true);translate([0,0,ZT/2])side_panel(false);}
if(on("fan_CT200_standin"))translate([0,depth/2,ZT+bg+Ht-ptt-30])fan_standin();
if(on("example_faceplates"))for(k=[0:2])translate([0,0,k*3*ws_pitch]){ws_plate(1);translate([0,0,ws_pitch])ws_plate(2);}
if(on("cleat_rack_half"))cleat_rack();
if(part=="accents"||(part=="all"&&look=="B")){
  four()translate([xo-1,12.2,-bg])cube([1,7.6,ZT+2*bg]);
  for(t=[0,1])mirror([0,0,t])translate([0,0,t?bg:ZT+bg])four()for(p=end_xy)translate([p[0],p[1],(t?H:Ht)-2])cylinder(d=11.2,h=2);}
}
