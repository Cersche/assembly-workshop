// SCR5 access panel concepts, not a revision. Pi on the screen's own 4 standoffs, Hue deck between the keystone rows.
// Coordinates as SCR5-H: X- left from front, plate front Y 0, rear Y 4, Z 0 slot bottom. Fit and strength UNKNOWN. Jack and plug boxes unmeasured.
use <../../outputs/Screen_Pi_Hue_SCR5-H11_2026-11-03/src/SCR5-H.scad>
use <../../outputs/Screen_Pi_Hue_SCR5-H11_2026-11-03/src/SCR5-F_hp4lib.scad>
opt="A"; part="all"; rail=false;
$fn=40;
L=-110.85;
RU=[16.5,68.8];                       // upright rows: blocks Z 1.5..35 and 53.8..87.3
RS=[12.9,33.9,54.9,75.9];             // sideways rows: blocks 21 tall
function gcx()=opt=="A"?33:opt=="B"||opt=="C"?38:opt=="S"?33:38.6;
function cols()=opt=="A"?[-100.35,-79.35,-58.35]:opt=="B"||opt=="C"?[-100.35,-79.35,-58.35,-37.35]:opt=="T"?[-33.35]:[];
function side_cols()=opt=="S"||opt=="T"?[-94.1,-60.6]:[];          // sideways block X centre
up=[for(x=cols(),c=opt=="C"?[RU[1]]:RU)[x,c]];
side=[for(x=side_cols(),c=RS)[x,c]];
function m6()=opt=="C"?[[-95,45],[-67,45],[-45,45]]:opt=="A"?[[-40,21.5],[-40,59],[-69,44.4]]:opt=="B"?[[-90,44.4],[-60,44.4]]:opt=="S"?[[-36,28],[-36,59]]:[[-33.35,44.4]];
function fbx()=opt=="C"?[[gcx()-68,46],[gcx()-68,10],[gcx()+68,10],[gcx()+68,72]]:opt=="A"||opt=="S"?[[gcx()-68,10],[gcx()-68,72],[gcx()+68,10],[gcx()+68,72]]:[[gcx()-68,44.4],[gcx()+68,10],[gcx()+68,72]];
GW=120.7; GCZ=41.5; D=gcx()-33;
module xz(y,d){translate([0,y+d,0])rotate([90,0,0])linear_extrude(d)children();}
module rr(w,h,r){hull()for(x=[-w/2+r,w/2-r],z=[-h/2+r,h/2-r])translate([x,z])circle(r=r);}
module cy(x,y,z,d,h){translate([x,y,z])rotate([-90,0,0])cylinder(d=d,h=h);}
module box(a,b){translate(a)cube(b-a);}
module slots(){for(x=[-118.2625,118.2625],z=[6.323,38.127,50.773,82.577])translate([x,z])hull()for(dx=[-1.5,1.5])translate([dx,0])circle(d=7);}
module block_up(x,c){translate([x+92.5,4.08,c-66])ks_golden();}
module block_side(x,c){translate([x,4.08,c])rotate([0,90,0])translate([92.5,0,-67.75])ks_golden();}
module cuts(){
 for(q=up)box([q[0]-10.5,-.01,q[1]-15],[q[0]+10.5,4.01,q[1]+18.5]);
 for(q=side)box([q[0]-16.75,-.01,q[1]-10.5],[q[0]+16.75,4.01,q[1]+10.5]);
}
module plate(){
 union(){
  difference(){
   union(){
    xz(0,4)translate([0,44.4])rr(252,88.8,2.5);
    for(q=fbx())cy(q[0],3.9,q[1],9,9.4);
    for(q=m6())cy(q[0],3.9,q[1],14,10.7);
    if(opt=="C")for(x=[-90,-60])box([x-6,3.9,7],[x+6,19,10]);
    if(opt=="A"||opt=="B")box([L,3.9,38],[opt=="A"?-46:-27,8,50.8]); // mid-height stiffening bar behind the label strip
   }
   xz(-.02,4.04)slots();
   translate([D,0,0])window_cut();
   for(x=[45.5,35.5,25.5])box([gcx()+x-1.7,-.02,GCZ+40.3],[gcx()+x+1.7,16.3,GCZ+44.7]);
   box([gcx()+34.35,1.2,-1],[gcx()+44.35,10,3.9]);
   for(q=fbx())cy(q[0],8.3,q[1],4.2,5.02);
   for(q=m6())cy(q[0],8,q[1],7.6,6.7);
   cuts();
  }
  for(q=up)block_up(q[0],q[1]);
  for(q=side)block_side(q[0],q[1]);
  translate([D,0,0])leaves();
 }
}
pi_x0=gcx()-41.15; pi_y0=13.3; pi_z0=73.6;
module pi_at(){multmatrix([[1,0,0,pi_x0],[0,0,1,pi_y0],[0,-1,0,pi_z0],[0,0,0,1]])children();}
module pi(){pi_at(){
 box([0,0,0],[85,56,1.4]);
 for(y=[9,27])box([70,y-6.6,1.4],[87,y+6.6,17.4]);
 box([65,37.75,1.4],[87,53.75,14.9]);
 box([6.7,-1.5,1.4],[15.7,6,4.6]);for(x=[26,39.5])box([x-3.5,-1.5,1.4],[x+3.5,6.5,4.4]);box([51,0,1.4],[57,12,7.4]);
 box([7.1,50,1.4],[57.9,55,10]);box([2.5,19,1.4],[6.5,37,7]);box([43,19,1.4],[47,37,7]);
 box([22.5,25,1.4],[37.5,40,3.8]);box([-2.5,20,-1.4],[15,36,0]);
}}
module pi_screws(){for(x=[gcx()-37.65,gcx()+20.35],z=[70.1,21.1])cy(x,14.7,z,4.5,2.5);}
module pi_drivers(){for(x=[gcx()-37.65,gcx()+20.35],z=[70.1,21.1])cy(x,17.2,z,4,200);}
module inner_so(){for(x=[gcx()-37.65,gcx()+20.35],z=[70.1,21.1])cy(x,9.1,z,5.5,4.2);}
module screen_all(){translate([D,0,0])dummy();inner_so();}
module frame_new(){
 difference(){
  translate([D,0,0])frame();
  box([pi_x0-1,13,71.3],[pi_x0+86,17,75.5]);                 // Pi board clears the top bar
  box([pi_x0+11.2-8,13,73],[pi_x0+11.2+8,17,81]);            // USB-C elbow gap
  box([gcx()+58,13,14],[gcx()+67,17,73]);                    // Pi USB/Ethernet plugs clear the right bar
  if(opt!="A"&&opt!="S")box([-60,13,opt=="C"?16:-1],[gcx()-64.7,17,90]);       // left bar and bosses come off, column 4 blocks are there
 }
 if(opt!="A"&&opt!="S"){box([gcx()-64.7,13.3,3.5],[gcx()-60.6,16.3,79.5]);hull(){cy(fbx()[0][0],13.3,opt=="C"?46:44.4,9,3);cy(gcx()-64,13.3,opt=="C"?46:44.4,7,3);}}
}
// flat DSI ribbon, 16 wide (50 mm cable from the screen's box assumed)
RIB=[[gcx()-58,14.5],[gcx()-58,20],[gcx()-50,24.5],[gcx()-40,24.5],[gcx()-37.6,20.6]];
module ribbon(){for(i=[0:3])hull(){translate([RIB[i][0]-.2,RIB[i][1]-.2,38])cube([.4,.4,16]);translate([RIB[i+1][0]-.2,RIB[i+1][1]-.2,38])cube([.4,.4,16]);}}
fan_c=[gcx()-12.15,41.1];
module fan(){difference(){box([fan_c[0]-20,29.5,fan_c[1]-20],[fan_c[0]+20,39.5,fan_c[1]+20]);cy(fan_c[0],29.4,fan_c[1],37,10.2);}}
module fan_mount(){difference(){union(){
  box([fan_c[0]-22,24.5,fan_c[1]-22],[fan_c[0]+22,29.5,fan_c[1]+22]);
  box([gcx()+1,24.5,1],[gcx()+6,29.5,82]);
  box([gcx()+1,13,79.75],[gcx()+6,29.5,82]);
  box([gcx()+1,13,1],[gcx()+6,29.5,3.2]);
 }
 cy(fan_c[0],24.4,fan_c[1],37,5.2);
}}
hue_cx=-54.4; hue_y0=opt=="C"?24.5:27; deck_z=opt=="C"?2:28; deck_t=3; deck_top=deck_z+deck_t;
hue_w=88; hue_d=88; hue_h=26;
module hue(){translate([hue_cx,hue_y0+hue_d/2,deck_top+.1]){linear_extrude(hue_h)offset(r=12)square([hue_w-24,hue_d-24],center=true);translate([0,0,hue_h-.1])cylinder(d=26,h=.7);}}
deck_y1=hue_y0+hue_d+4;
module tabs(){for(q=m6())difference(){
  hull(){cy(q[0],14.65,q[1],13.4,6);translate([q[0]-6.7,14.65,q[1]>deck_top?deck_top-.1:deck_z])cube([13.4,6,.2]);}
  cy(q[0],14,q[1],6.6,7.2);
  translate([q[0],17.5,q[1]])rotate([-90,0,0])cylinder(d=11.5,h=3.2);
}}
module deck_low(){difference(){   // one part: floor, side walls, front wall with 3 M6, full cradle
 union(){
  difference(){box([-105,14.65,2],[-3.9,116,5]);box([-37,14,1],[-3,16.7,6]);}
  box([-105,14.65,4.9],[-102,116,28]); box([-6.9,21,4.9],[-3.9,116,28]);
  box([-105,14.65,2],[-37,20.65,52]);
  translate([hue_cx,68.5,5-3-.045])intersection(){import("C:/Users/brian/Downloads/Swanky Rottis.stl",convexity=6);translate([-50,-50,3])cube([100,100,40]);}
 }
 for(q=m6()){cy(q[0],14,q[1],6.6,7.2);cy(q[0],17.15,q[1],11.5,3.6);}
 for(x=[-90,-60])box([x-6.15,14,6.85],[x+6.15,19.3,10.15]);
}}
module hue_lift(){translate([0,0,28])hue();}
module deck(){if(opt=="C")deck_low();else union(){
  difference(){box([-105,15,deck_z],[-8,deck_y1,deck_top]);box([-33.3,14,deck_z-1],[-7,16.7,deck_top+1]);}
  tabs();
  for(x=opt=="B"?[-89.85,-68.85,-47.85,-26.85]:[-89.85,-68.85,-47.85,-30])hull(){box([x-1.5,36,deck_z-.1],[x+1.5,deck_y1-2,deck_top-1]);box([x-1.5,44,12.5],[x+1.5,deck_y1-12,deck_z]);}  // ribs between the lower cable lanes
  box([-105,deck_y1-4,deck_top-.1],[-8,deck_y1,deck_top+5]);                                                                // rear stop rib
  if(rail)box([-112,44,deck_z],[-105,64,deck_top]);
}}
module rail_part(){difference(){box([-126.8,14.4,14],[-111.2,64,deck_z]);cy(-118.2625,10,22.225,6.6,8);translate([-118.2625,16,22.225])rotate([-90,0,0])cylinder(d=11.5,h=60);}}
module jacks(){for(q=up)box([q[0]-7.5,3,q[1]-10.5],[q[0]+7.5,34,q[1]+11]);for(q=side)box([q[0]-11,3,q[1]-7.5],[q[0]+10.5,34,q[1]+7.5]);}
module plugs(){for(q=up)box([q[0]-5.8,34,q[1]-6.5],[q[0]+5.8,72,q[1]+6.5]);for(q=side)box([q[0]-6.5,34,q[1]-5.8],[q[0]+6.5,72,q[1]+5.8]);}
module cables(){for(q=up)cy(q[0],72,q[1],6,90);for(q=side)cy(q[0],72,q[1],6,90);}
module m6_tools(){for(q=m6())cy(q[0],20.6,q[1],5,110);}
module m6_heads(){for(q=m6())cy(q[0],17.5,q[1],10.5,3);}
module sd_path(){box([pi_x0-16,14.8,37],[pi_x0-3,160,54]);}
module usbc_elbow(){x=pi_x0+11.2;box([x-6,13,75.2],[x+6,20,85.5]);box([x-3,20,77.5],[x+3,80,83.5]);}
module pi_plugs(){for(y=[9,27])box([pi_x0+87,16.4,pi_z0-y-7],[pi_x0+87+36,29.4,pi_z0-y+7]);box([pi_x0+87,16.4,pi_z0-45.75-8],[pi_x0+87+38,29,pi_z0-45.75+8]);}
module post_l(){translate([0,4,0])import("../rack-post-hex/assembled/post_left.stl",convexity=4);}
module post_r(){translate([0,4,0])import("../rack-post-hex/assembled/post_right.stl",convexity=4);}
module pins(){translate([D,0,0])for(i=[0:2])placed_pin(i);}
if(part=="plate")plate();
if(part=="frame")frame_new();
if(part=="screen")screen_all();
if(part=="pi")pi();
if(part=="pi_screws")pi_screws();
if(part=="pi_drivers")pi_drivers();
if(part=="ribbon")ribbon();
if(part=="fan")fan();
if(part=="fan_mount")fan_mount();
if(part=="hue")hue();
if(part=="deck")deck();
if(part=="hue_lift")hue_lift();
if(part=="rail")rail_part();
if(part=="jacks")jacks();
if(part=="plugs")plugs();
if(part=="cables")cables();
if(part=="m6_tools")m6_tools();
if(part=="m6_heads")m6_heads();
if(part=="sd_path")sd_path();
if(part=="usbc")usbc_elbow();
if(part=="pi_plugs")pi_plugs();
if(part=="post_l")post_l();
if(part=="post_r")post_r();
if(part=="pins")pins();
hide=[];
function h(n)=len([for(q=hide)if(q==n)1])>0;
if(part=="all"){
 if(!h("plate"))color("#8a93a0")plate(); if(!h("frame"))color("#c8c8c8")frame_new(); if(!h("screen"))color("#23262b")screen_all();
 if(!h("pi")){color("#2e9e4f")pi();color("#333")pi_screws();} if(!h("ribbon"))color("#cc7a00")ribbon(); if(!h("fan")){color("#9b6fc4")fan();color("#b49ad6")fan_mount();}
 if(!h("hue"))color("#f0f0ea")hue(); if(!h("deck"))color("#4f81bd")deck(); if(!h("post"))color("#d9d9d9"){post_l();post_r();}
 if(rail)color("#2f5f96")rail_part();
 if(!h("ks")){color("#e0c040")jacks(); color("#7fb3d9")plugs(); color("#3b6ea5")cables();}
 if(!h("heads"))color("#222")m6_heads();
}
