// SCR5-J1 (Brian 2026-11-03): 4-port access panel. Pi on the screen's own standoffs, 2 x 2 golden keystones, Hue between the keystone rows.
// mm; X- left from the front, plate front Y 0, rear Y 4, Z 0 slot bottom. Screen position and H8 wedge pins unchanged from H11.
// PROPOSED, UNVALIDATED: not printed. Fit, snap, sag, heat and strength UNKNOWN. Jack/plug boxes and Pi connectors are not measured.
use <SCR5-H.scad>
use <SCR5-F_hp4lib.scad>
part="plate"; cradle_on=true;
ID="SCR5-J1";
$fn=48;
eps=0.02;
GCX=33; GCZ=41.5;
// Keystones: same golden block and ks_tight as H11, 21 wide x 33.5 tall. Post flange limit X -111.12.
KS=[for(x=[-100.35,-79.35],c=[16.5,68.8])[x,c]];
// M6 joints: all in the free strip right of the keystones. Inserts M6x5x8, bore 7.6, from behind; screws hidden from the front.
M6=[[-60,15],[-47,15],[-60,73],[-47,73]];
boss_end=14.6; tab_y=14.65; tab_t=6; cb_d=11.5; cb_deep=3.5; m6_clear=6.6; m6_bore=7.6; m6_deep=6.6;
tongue_x=[-60,-47]; tongue_w=12; tongue_z=38; tongue_h=3; tongue_y=19; slot_clear=0.3;
deck_z=28; deck_t=3; deck_top=deck_z+deck_t;
hue_cx=-54.4; hue_cy=82.2; hue_w=88; hue_d=88; hue_h=26; deck_y1=hue_cy+47.5; deck_x0=-105; deck_x1=-6; deck_r=6;
wall_x0=-66.7; wall_x1=-40.3; wall_top=79.7;
rib_x=[-89.85,-68,-36,-10]; rib_t=3; rib_y1=deck_y1-4;
// M3 countersunk down through the deck into M3x3x5 inserts in the underframe, bore 4.2 x 4 deep, boss 9.
DS=[[-89.85,50],[-89.85,rib_y1-4.5],[-68,40],[-68,rib_y1-4.5],[-36,30],[-36,rib_y1-4.5],[-10,42],[-10,rib_y1-4.5],[-53.5,24.5]];
// Pi: on the screen's four inner standoffs, USB-C edge up, USB/Ethernet to the right from the front. Published layout.
pi_x0=GCX-41.15; pi_y0=13.3; pi_z0=73.6;
PI_HOLES=[for(x=[GCX-37.65,GCX+20.35],z=[70.1,21.1])[x,z]];
module xz(y,d){translate([0,y+d,0])rotate([90,0,0])linear_extrude(d)children();}
module rr(w,h,r){hull()for(x=[-w/2+r,w/2-r],z=[-h/2+r,h/2-r])translate([x,z])circle(r=r);}
module cy(x,y,z,d,h){translate([x,y,z])rotate([-90,0,0])cylinder(d=d,h=h);}
module box(a,b){translate(a)cube(b-a);}
module slots(){for(x=[-118.2625,118.2625],z=[6.323,38.127,50.773,82.577])translate([x,z])hull()for(dx=[-1.5,1.5])translate([dx,0])circle(d=7);}
module block(x,c){translate([x+92.5,4.08,c-66])ks_golden();}
module plate(){union(){
 difference(){
  union(){
   xz(0,4)translate([0,44.4])rr(252,88.8,2.5);
   for(x=[GCX-68,GCX+68],z=[10,72])cy(x,3.9,z,9,9.4);
   for(q=M6)cy(q[0],3.9,q[1],14,boss_end-3.9);
   for(x=tongue_x)box([x-tongue_w/2,3.9,tongue_z],[x+tongue_w/2,tongue_y,tongue_z+tongue_h]);
   leaves();
  }
  xz(-.02,4.04)slots();
  window_cut();
  for(x=[45.5,35.5,25.5])box([GCX+x-1.7,-.02,GCZ+40.3],[GCX+x+1.7,16.3+.04,GCZ+44.7]);
  box([GCX+34.35,1.2,-1],[GCX+44.35,10,GCZ-38.6+1]);                    // screen's own panel ribbon, as H8
  for(x=[GCX-68,GCX+68],z=[10,72])cy(x,8.3,z,4.2,5.02);
  for(q=M6)cy(q[0],boss_end-m6_deep,q[1],m6_bore,m6_deep+.1);
  for(q=KS)box([q[0]-10.5,-.01,q[1]-15],[q[0]+10.5,4.01,q[1]+18.5]);
  xz(3.5,0.52)translate([-58,27])mirror([1,0])text(ID,size=5,halign="center",font="Liberation Sans:style=Bold");
 }
 for(q=KS)block(q[0],q[1]);
}}
// Rear frame: H8's outline and corner screws, opened for the Pi and its plugs.
module frame(){difference(){
 frame_blank();
 // ID on each of the 3 pieces: bottom bar, and J1 on both top pieces.
 xz(15.8,0.52){translate([GCX,6])mirror([1,0])text(ID,size=3,halign="center",font="Liberation Sans:style=Bold");
  for(x=[-13,48])translate([x,76.4])mirror([1,0])text("J1",size=2.4,halign="center",font="Liberation Sans:style=Bold");}
 dsi_keepout();
 difference(){ribbon_route();hull(){cyl_y(GCX-68,12.3,72,9.4,5);cyl_y(GCX-62,12.3,72,8.4,5);}}
 for(sx=[-1,1],sz=[-1,1])cyl_y(GCX+sx*56.45,13.28,GCZ+sz*34,2.8,3.04);
 for(x=[GCX-68,GCX+68],z=[10,72]){cyl_y(x,13.28,z,3.4,3.04);translate([x,14.8,z])rotate([-90,0,0])cylinder(d1=3.4,d2=6.4,h=1.52,$fn=32);}
 box([pi_x0-1,13,71.3],[pi_x0+86,17,75.5]);                  // Pi board and shells clear the top bar
 box([pi_x0+11.2-8,13,73],[pi_x0+11.2+8,17,81]);             // USB-C elbow gap
 box([GCX+58,13,14],[GCX+67,17,73]);                         // Pi USB/Ethernet plugs clear the right bar
}}
module deck_outline(){
 offset(r=deck_r)offset(delta=-deck_r)union(){
  translate([deck_x0,34.5])square([deck_x1-deck_x0,deck_y1-34.5]);
  translate([-69,tab_y])square([35.7,deck_y1-tab_y]);
  translate([-33.3-eps,16.7])square([deck_x1+33.3+eps,deck_y1-16.7]);
 }
 translate([-69,tab_y])square([deck_r+1,deck_r+1]);
 translate([-33.3-deck_r-1,tab_y])square([deck_r+1,deck_r+1]);
 translate([deck_x1-deck_r-1,16.7])square([deck_r+1,deck_r+1]);
 translate([-33.3-eps,16.7])square([deck_r+1,deck_r+1]);
}
module hue_cradle(){ // Brian's cradle corner posts read in place. Rear posts cut to 6 tall: the Hue tilts over them and slides out the back.
 translate([hue_cx,hue_cy,deck_top-3-0.045])intersection(){
  import("C:/Users/brian/Downloads/STL/Swanky Rottis.stl",convexity=6);
  union(){translate([-50,-50,3])cube([100,50,40]);translate([-50,0,3])cube([100,50,9.045]);}
 }
}
module deck(){difference(){
 union(){
  translate([0,0,deck_z])linear_extrude(deck_t)deck_outline();
  box([wall_x0,tab_y,deck_top-.1],[wall_x1,tab_y+tab_t,wall_top]);
  for(x=[-66.5,-53.5,-39.5])hull(){box([x-1.5,tab_y+tab_t-.1,deck_top-.1],[x+1.5,34,deck_top]);box([x-1.5,tab_y+tab_t-.1,deck_top-.1],[x+1.5,tab_y+tab_t,wall_top-6]);}
  if(cradle_on)hue_cradle();
 }
 for(q=M6)if(q[1]>deck_top){cy(q[0],tab_y-.1,q[1],m6_clear,tab_t+.2);cy(q[0],tab_y+tab_t-cb_deep,q[1],cb_d,cb_deep+.1);}
 for(x=tongue_x)box([x-(tongue_w+slot_clear)/2,tab_y-.1,tongue_z-slot_clear/2],[x+(tongue_w+slot_clear)/2,tongue_y+slot_clear,tongue_z+tongue_h+slot_clear/2]);
 for(q=DS){translate([q[0],q[1],deck_z-.1])cylinder(d=3.4,h=deck_t+.2);translate([q[0],q[1],deck_top-1.5])cylinder(d1=3.4,d2=6.4,h=1.51,$fn=32);}
 translate([-22,75,deck_z-.01])linear_extrude(.61)mirror([1,0])text(ID,size=4,halign="center",font="Liberation Sans:style=Bold");
}}
// Printed top face down. Carries the low M6 joints and the ribs between the lower cable lanes.
module underframe(){difference(){
 union(){
  box([wall_x0,tab_y,8.3],[wall_x1,tab_y+tab_t,deck_z]);
  box([-69.5,tab_y,16],[-34.5,tab_y+tab_t,deck_z]);
  for(x=rib_x)hull(){
   y0=(x==-68||x==-36)?tab_y+tab_t-.1:36;
   box([x-rib_t/2,y0,deck_z-3],[x+rib_t/2,rib_y1,deck_z]);
   box([x-rib_t/2,y0+(y0<30?2:8),12.5],[x+rib_t/2,rib_y1-12,deck_z]);
  }
  box([-89.85-rib_t/2,rib_y1-9,21],[-10+rib_t/2,rib_y1,deck_z]);     // rear cross bar, cables pass under it
  for(q=DS)translate([q[0],q[1],21])cylinder(d=9,h=deck_z-21);
 }
 for(q=M6)if(q[1]<deck_z){cy(q[0],tab_y-.1,q[1],m6_clear,tab_t+.2);cy(q[0],tab_y+tab_t-cb_deep,q[1],cb_d,cb_deep+.1);}
 for(q=DS){translate([q[0],q[1],20.9])cylinder(d=3.4,h=7.2);translate([q[0],q[1],deck_z-4])cylinder(d=4.2,h=4.1);}
 translate([-53.5,tab_y-.01,10])rotate([90,0,180])linear_extrude(.51)text(ID,size=3,halign="center",font="Liberation Sans:style=Bold");
}}
// Fan mount: tool-free as in H11. Snaps over the frame's top and bottom bars (about 0.2 per side, calculated). Fan on its rear face, facing the Pi's chip.
fan_c=[GCX-12.15,41.1]; fan_pitch=32;
module fan_mount(){difference(){
 union(){
  box([fan_c[0]-22,24.5,fan_c[1]-22],[fan_c[0]+22,29.5,fan_c[1]+22]);
  box([GCX+1,24.5,1],[GCX+6,29.5,82]);
  box([GCX+1,12,79.75],[GCX+6,29.5,82]);
  box([GCX+1,12,1],[GCX+6,29.5,3.25]);
  translate([GCX+1,0,0])rotate([90,0,90])linear_extrude(5)polygon([[12,79.75],[13.2,79.3],[13.2,79.75]]);
  translate([GCX+1,0,0])rotate([90,0,90])linear_extrude(5)polygon([[12,3.25],[13.2,3.7],[13.2,3.25]]);
 }
 cy(fan_c[0],24.4,fan_c[1],37,5.2);
 for(sx=[-1,1],sz=[-1,1])cy(fan_c[0]+sx*fan_pitch/2,25.5,fan_c[1]+sz*fan_pitch/2,4.2,4.1);
 translate([GCX+3.5,29.51,14])rotate([90,90,0])linear_extrude(.51)text(ID,size=2.6,halign="center",valign="center",font="Liberation Sans:style=Bold");
}}
// ---- references, not printed ----
module pi_at(){multmatrix([[1,0,0,pi_x0],[0,0,1,pi_y0],[0,-1,0,pi_z0],[0,0,0,1]])children();}
module pi(){pi_at(){
 box([0,0,0],[85,56,1.4]);
 for(y=[9,27])box([70,y-6.6,1.4],[87,y+6.6,17.4]);
 box([65,37.75,1.4],[87,53.75,14.9]);
 box([6.7,-1.5,1.4],[15.7,6,4.6]);for(x=[26,39.5])box([x-3.5,-1.5,1.4],[x+3.5,6.5,4.4]);box([51,0,1.4],[57,12,7.4]);
 box([7.1,50,1.4],[57.9,55,10]);box([2.5,19,1.4],[6.5,37,7]);box([43,19,1.4],[47,37,7]);
 box([22.5,25,1.4],[37.5,40,3.8]);box([-2.5,20,-1.4],[15,36,0]);
}}
module pi_screws(){for(q=PI_HOLES)cy(q[0],14.7,q[1],4.5,2.5);}
module pi_drivers(){for(q=PI_HOLES)cy(q[0],17.2,q[1],4,200);}
module screen_all(){dummy();for(q=PI_HOLES)cy(q[0],9.1,q[1],5.5,4.2);}
RIB=[[GCX-58,14.5],[GCX-58,20],[GCX-50,24.5],[GCX-40,24.5],[GCX-37.6,20.6]];
module ribbon(){for(i=[0:3])hull(){translate([RIB[i][0]-.2,RIB[i][1]-.2,38])cube([.4,.4,16]);translate([RIB[i+1][0]-.2,RIB[i+1][1]-.2,38])cube([.4,.4,16]);}}
module fan(){difference(){box([fan_c[0]-20,29.5,fan_c[1]-20],[fan_c[0]+20,39.5,fan_c[1]+20]);cy(fan_c[0],29.4,fan_c[1],37,10.2);}}
module hue(){translate([hue_cx,hue_cy,deck_top+.1]){linear_extrude(hue_h)offset(r=12)square([hue_w-24,hue_d-24],center=true);translate([0,0,hue_h-.1])cylinder(d=26,h=.7);}}
module jacks(){for(q=KS)box([q[0]-7.5,3,q[1]-10.5],[q[0]+7.5,34,q[1]+11]);}
module plugs(){for(q=KS)box([q[0]-5.8,34,q[1]-6.5],[q[0]+5.8,72,q[1]+6.5]);}
module cables(){for(q=KS)cy(q[0],72,q[1],6,90);}
module m6_heads(){for(q=M6)cy(q[0],tab_y+tab_t-cb_deep,q[1],10.5,3);}
module m6_tools(){for(q=M6)cy(q[0],tab_y+tab_t,q[1],5,110);}
module m3_tools(){for(q=DS)translate([q[0],q[1],deck_top])cylinder(d=5,h=26);}
module sd_path(){box([pi_x0-16,14.8,37],[pi_x0-3,160,54]);}
module usbc(){x=pi_x0+11.2;box([x-6,13,75.2],[x+6,20,85.5]);box([x-3,20,77.5],[x+3,80,83.5]);}
module pi_plugs(){for(y=[9,27])box([pi_x0+87,16.4,pi_z0-y-7],[pi_x0+87+36,29.4,pi_z0-y+7]);box([pi_x0+87,16.4,pi_z0-45.75-8],[pi_x0+87+38,29,pi_z0-45.75+8]);}
module pins(){for(i=[0:2])placed_pin(i);}
if(part=="plate")plate();
if(part=="frame")frame();
if(part=="deck")deck();
if(part=="underframe")underframe();
if(part=="fanmount")fan_mount();
if(part=="screen")screen_all();
if(part=="pi")pi();
if(part=="pi_screws")pi_screws();
if(part=="pi_drivers")pi_drivers();
if(part=="ribbon")ribbon();
if(part=="fan")fan();
if(part=="hue")hue();
if(part=="jacks")jacks();
if(part=="plugs")plugs();
if(part=="cables")cables();
if(part=="m6_heads")m6_heads();
if(part=="m6_tools")m6_tools();
if(part=="m3_tools")m3_tools();
if(part=="sd_path")sd_path();
if(part=="usbc")usbc();
if(part=="pi_plugs")pi_plugs();
if(part=="pins")pins();
hide=[];
function h(n)=len([for(q=hide)if(q==n)1])>0;
if(part=="all"){
 if(!h("plate"))color("#8a93a0")plate(); if(!h("frame"))color("#c8c8c8")frame(); if(!h("screen"))color("#23262b")screen_all();
 if(!h("pi")){color("#2e9e4f")pi();color("#333")pi_screws();} if(!h("ribbon"))color("#cc7a00")ribbon(); if(!h("fan")){color("#9b6fc4")fan();color("#b49ad6")fan_mount();}
 if(!h("hue"))color("#f0f0ea")hue(); if(!h("deck")){color("#4f81bd")deck();color("#2f5f96")underframe();}
 if(!h("post"))color("#d9d9d9"){translate([0,4,0])import("../../../work/rack-post-hex/assembled/post_left.stl",convexity=4);translate([0,4,0])import("../../../work/rack-post-hex/assembled/post_right.stl",convexity=4);}
 if(!h("ks")){color("#e0c040")jacks(); color("#7fb3d9")plugs(); color("#3b6ea5")cables();}
 if(!h("heads"))color("#222")m6_heads();
}
if(part=="pin1"||part=="pin2"||part=="pin3")pin(0.45,part=="pin1"?1:part=="pin2"?2:3);
