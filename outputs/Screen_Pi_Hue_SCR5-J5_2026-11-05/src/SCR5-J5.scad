// SCR5-J5 (Brian 2026-11-05): J4 with the Hue cradle loosened (J4 printed: cradle too tight). Each corner post moves 0.4 out in X; the two front posts move 0.8 forward (rear posts already sit on the deck rear edge). Only the tray changes and carries ID SCR5-J5; all other parts are J4.
// SCR5-J4 (Brian 2026-11-03): J3 with the front frame's top band as wide as its bottom band (7.2 flat face), notched around the 3 wedge pin caps. J3 was J2 with a separate front frame and the top glass gap tightened. J2 was: 3-port access panel. Pi on the screen's own standoffs, 3 golden keystones across the top, Hue low and forward on a one-piece tray.
// mm; X- left from the front, plate front Y 0, rear Y 4, Z 0 slot bottom. Screen position and H8 wedge pins unchanged from H11.
// PROPOSED, UNVALIDATED: not printed. Fit, snap, sag, heat and strength UNKNOWN. Jack/plug boxes and Pi connectors are not measured.
use <SCR5-H.scad>
use <SCR5-F_hp4lib.scad>
part="plate"; cradle_on=true;
ID="SCR5-J4"; DECK_ID="SCR5-J5"; cradle_loose=0.4;
$fn=48;
eps=0.02;
GCX=33; GCZ=41.5;
// Keystones: same golden block and ks_tight as H11, 21 wide x 33.5 tall, one row. Blocks Z 53.8..87.3. Post flange limit X -111.12.
KS=[for(x=[-100.35,-79.35,-58.35])[x,68.8]];
// M6 joints: one row under the keystones. Inserts M6x5x8, bore 7.6, from behind; screws hidden from the front.
M6=[[-95,45],[-71,45],[-47,45]];
boss_end=14.6; tab_y=14.65; tab_t=6; cb_d=11.5; cb_deep=3.5; m6_clear=6.6; m6_bore=7.6; m6_deep=6.6;
// Low on the plate: 2 tongues carry the weight, their pads take the wall's push toward the plate. The M6 row only has to pull.
tongue_x=[-90,-60]; tongue_w=12; tongue_z=7; tongue_h=3; tongue_y=19; slot_clear=0.3; pad_z0=3; pad_z1=14;
deck_z=2; deck_t=3; deck_top=deck_z+deck_t;
hue_cx=-54.4; hue_cy=68.5; hue_w=88; hue_d=88; hue_h=26; deck_y1=116; deck_x0=-105; deck_x1=-7; deck_r=6;
wall_x1=-40.3; wall_top=52; side_top=28; rside_x0=-10; rside_y0=21; notch_x=-41; notch_y=16.7;
// Pi: on the screen's four inner standoffs, USB-C edge up, USB/Ethernet to the right from the front. Published layout.
pi_x0=GCX-41.15; pi_y0=13.3; pi_z0=73.6;
PI_HOLES=[for(x=[GCX-37.65,GCX+20.35],z=[70.1,21.1])[x,z]];
module xz(y,d){translate([0,y+d,0])rotate([90,0,0])linear_extrude(d)children();}
module rr(w,h,r){hull()for(x=[-w/2+r,w/2-r],z=[-h/2+r,h/2-r])translate([x,z])circle(r=r);}
module cy(x,y,z,d,h){translate([x,y,z])rotate([-90,0,0])cylinder(d=d,h=h);}
module box(a,b){translate(a)cube(b-a);}
module slots(){for(x=[-118.2625,118.2625],z=[6.323,38.127,50.773,82.577])translate([x,z])hull()for(dx=[-1.5,1.5])translate([dx,0])circle(d=7);}
module block(x,c){translate([x+92.5,4.08,c-66])ks_golden();}
// Front frame: Brian's borders from the glass edge (2026-11-03): left 6, right 6, top 3, bottom 8. Glass X -27.35..93.35, Z 2.9..80.1.
LIT=[-21.35,87.35,10.9,77.1]; REVEAL=1.5; BZ_T=1.5; BZ_REL=0.2; BZ_OUT=[-32.25,98.25,0.9,87.1]; // top 87.1: flat face above the bevel = 7.2, same as the bottom
CAP_X=[58.5,68.5,78.5]; CAP_NOTCH_HW=2.9; CAP_NOTCH_Z=80.7; // pin caps X +-2.5, Z 81.1..86.9; 0.4 clear each side and below, open at the top
// Hooks, 2 per side, all hidden behind the frame: hook on 2.2 high, then the frame drops and its feet catch the plate's rear face. Nothing flexes.
HK_Z=[20,45]; HK_W=8; HK_FOOT=2; HK_DROP=2.2; HK_YEND=5.7; HK_X=[[-30.95,-28.95],[94.95,96.95]];
HOLE_X=[[-31.35,-28.75],[94.75,97.35]];
module win(){ // as J2's window_cut, top glass gap 0.2 instead of 0.4
 box([GCX-60.75,-.02,2.5],[GCX+60.75,4.02,80.3]);
 hull(){box([GCX-60.75,.3,2.5],[GCX+60.75,.31,80.3]);box([GCX-61.05,-.01,2.2],[GCX+61.05,0,80.6]);}
}
module hook_holes(){for(q=HOLE_X,z=HK_Z)box([q[0],-.02,z],[q[1],4.02,z+HK_W+HK_DROP+.2]);}
module frust(y0,y1,g0,g1){hull(){box([LIT[0]-g0,y0,LIT[2]-g0],[LIT[1]+g0,y0+.01,LIT[3]+g0]);box([LIT[0]-g1,y1-.01,LIT[2]-g1],[LIT[1]+g1,y1,LIT[3]+g1]);}}
module bezel(){union(){
 difference(){
  box([BZ_OUT[0],-BZ_T,BZ_OUT[2]],[BZ_OUT[1],0,BZ_OUT[3]]);
  frust(-BZ_REL,-BZ_T-.1,REVEAL,REVEAL+BZ_T-BZ_REL+.1);       // 45 degree bevel, even dark edge around the picture
  box([LIT[0]-REVEAL,-BZ_REL-.01,LIT[2]-REVEAL],[LIT[1]+REVEAL,.01,LIT[3]+REVEAL]);
  box([-28,-BZ_REL,2.3],[94,.01,80.4]);                       // never presses on the glass
  for(x=CAP_X)box([x-CAP_NOTCH_HW,-BZ_T-.1,CAP_NOTCH_Z],[x+CAP_NOTCH_HW,.01,BZ_OUT[3]+.1]);   // the 3 buttons stay reachable
  xz(-BZ_REL-.5,.51)translate([GCX,4.2])mirror([1,0])text(ID,size=3,halign="center",font="Liberation Sans:style=Bold");
 }
 for(q=HK_X,z=HK_Z){
  box([q[0],-.01,z+.05],[q[1],HK_YEND,z+.05+HK_W]);
  // foot catches the plate's rear face; its ramp pulls the frame tight as it drops
  translate([q[0],0,0])rotate([90,0,90])linear_extrude(q[1]-q[0])polygon([[4.1,z+.05],[4.6,z+.05-HK_FOOT],[HK_YEND,z+.05-HK_FOOT],[HK_YEND,z+.06]]);
 }
}}
module plate(){union(){
 difference(){
  union(){
   xz(0,4)translate([0,44.4])rr(252,88.8,2.5);
   for(x=[GCX-68,GCX+68],z=[10,72])cy(x,3.9,z,9,9.4);
   for(q=M6)cy(q[0],3.9,q[1],14,boss_end-3.9);
   for(x=tongue_x){box([x-tongue_w/2,3.9,tongue_z],[x+tongue_w/2,tongue_y,tongue_z+tongue_h]);box([x-tongue_w/2,3.9,pad_z0],[x+tongue_w/2,boss_end,pad_z1]);}
   leaves();
  }
  xz(-.02,4.04)slots();
  win();
  hook_holes();
  for(x=[45.5,35.5,25.5])box([GCX+x-1.7,-.02,GCZ+40.3],[GCX+x+1.7,16.3+.04,GCZ+44.7]);
  box([GCX+34.35,1.2,-1],[GCX+44.35,10,GCZ-38.6+1]);                    // screen's own panel ribbon, as H8
  for(x=[GCX-68,GCX+68],z=[10,72])cy(x,8.3,z,4.2,5.02);
  for(q=M6)cy(q[0],boss_end-m6_deep,q[1],m6_bore,m6_deep+.1);
  for(q=KS)box([q[0]-10.5,-.01,q[1]-15],[q[0]+10.5,4.01,q[1]+18.5]);
  xz(3.5,0.52)translate([-75,27])mirror([1,0])text(ID,size=5,halign="center",font="Liberation Sans:style=Bold");
 }
 for(q=KS)block(q[0],q[1]);
}}
// Rear frame: H8's outline and corner screws, opened for the Pi and its plugs.
module frame(){difference(){
 frame_blank();
 // ID on each of the 3 pieces: bottom bar, and J2 on both top pieces.
 xz(15.8,0.52){translate([GCX,6])mirror([1,0])text(ID,size=3,halign="center",font="Liberation Sans:style=Bold");
  for(x=[-13,48])translate([x,76.4])mirror([1,0])text("J4",size=2.4,halign="center",font="Liberation Sans:style=Bold");}
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
  translate([deck_x0,tab_y])square([notch_x-deck_x0,deck_y1-tab_y]);
  translate([deck_x0,notch_y])square([deck_x1-deck_x0,deck_y1-notch_y]);
 }
 translate([deck_x0,tab_y])square([deck_r+1,deck_r+1]);
 translate([notch_x-deck_r-1,tab_y])square([deck_r+1,deck_r+1]);
 translate([deck_x1-deck_r-1,notch_y])square([deck_r+1,deck_r+1]);
}
module hue_cradle(){ // Brian's cradle posts, full height, read in place. J5: each post moved outward (cradle_loose).
 for(sx=[-1,1],sy=[-1,1])
  translate([hue_cx+sx*cradle_loose,hue_cy+(sy<0?-2*cradle_loose:0),deck_top-3-0.045])intersection(){
   import("C:/Users/brian/Downloads/STL/Swanky Rottis.stl",convexity=6);
   translate([sx<0?-50:0,sy<0?-50:0,3])cube([50,50,40]);
  }
}
// One printed part: floor, side walls, front wall with the 3 M6 and the 2 tongue slots, cradle posts.
module deck(){difference(){
 union(){
  translate([0,0,deck_z])linear_extrude(deck_t)deck_outline();
  box([deck_x0,tab_y,deck_top-.1],[deck_x0+3,deck_y1-deck_r,side_top]);
  box([rside_x0,rside_y0,deck_top-.1],[deck_x1,deck_y1-deck_r,side_top]);
  box([deck_x0,tab_y,deck_z],[wall_x1,tab_y+tab_t,wall_top]);
  if(cradle_on)hue_cradle();
 }
 for(q=M6){cy(q[0],tab_y-.1,q[1],m6_clear,tab_t+.2);cy(q[0],tab_y+tab_t-cb_deep,q[1],cb_d,cb_deep+.1);}
 for(x=tongue_x)box([x-(tongue_w+slot_clear)/2,tab_y-.1,tongue_z-slot_clear/2],[x+(tongue_w+slot_clear)/2,tongue_y+slot_clear,tongue_z+tongue_h+slot_clear/2]);
 translate([-54,105,deck_z-.01])linear_extrude(.61)mirror([1,0])text(DECK_ID,size=4,halign="center",font="Liberation Sans:style=Bold");
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
// Taking the Hue out, front bottom edge as reference: lift, tip the rear up, ease back and up, then level and slide out.
POSE=[[0,20,0],[0,20,6],[10,23,6],[40,28.5,0],[100,28.5,0]];
module hue_pose(i){p=POSE[i];y=hue_cy-hue_d/2;z=deck_top+.1;translate([0,y+p[0],z+p[1]])rotate([p[2],0,0])translate([0,-y,-z])hue();}
module jacks(){for(q=KS)box([q[0]-7.5,3,q[1]-10.5],[q[0]+7.5,34,q[1]+11]);}
module plugs(){for(q=KS)box([q[0]-5.8,34,q[1]-6.5],[q[0]+5.8,72,q[1]+6.5]);}
module cables(){for(q=KS)cy(q[0],72,q[1],6,90);}
module m6_heads(){for(q=M6)cy(q[0],tab_y+tab_t-cb_deep,q[1],10.5,3);}
module m6_tools(){for(q=M6)cy(q[0],tab_y+tab_t,q[1],5,110);}
module sd_path(){box([pi_x0-16,14.8,37],[pi_x0-3,160,54]);}
module usbc(){x=pi_x0+11.2;box([x-6,13,75.2],[x+6,20,85.5]);box([x-3,20,77.5],[x+3,80,83.5]);}
module pi_plugs(){for(y=[9,27])box([pi_x0+87,16.4,pi_z0-y-7],[pi_x0+87+36,29.4,pi_z0-y+7]);box([pi_x0+87,16.4,pi_z0-45.75-8],[pi_x0+87+38,29,pi_z0-45.75+8]);}
module pins(){for(i=[0:2])placed_pin(i);}
if(part=="plate")plate();
if(part=="frame")frame();
if(part=="bezel")bezel();
if(part=="deck")deck();
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
for(i=[0:4])if(part==str("hue_pose",i))hue_pose(i);
if(part=="sd_path")sd_path();
if(part=="usbc")usbc();
if(part=="pi_plugs")pi_plugs();
if(part=="pins")pins();
hide=[];
function h(n)=len([for(q=hide)if(q==n)1])>0;
if(part=="all"){
 if(!h("plate"))color("#8a93a0")plate(); if(!h("frame"))color("#c8c8c8")frame(); if(!h("bezel"))color("#9aa3b0")bezel(); if(!h("screen"))color("#23262b")screen_all();
 if(!h("pi")){color("#2e9e4f")pi();color("#333")pi_screws();} if(!h("ribbon"))color("#cc7a00")ribbon(); if(!h("fan")){color("#9b6fc4")fan();color("#b49ad6")fan_mount();}
 if(!h("hue"))color("#f0f0ea")hue(); if(!h("deck"))color("#4f81bd")deck();
 if(!h("post"))color("#d9d9d9"){translate([0,4,0])import("../../../work/rack-post-hex/assembled/post_left.stl",convexity=4);translate([0,4,0])import("../../../work/rack-post-hex/assembled/post_right.stl",convexity=4);}
 if(!h("ks")){color("#e0c040")jacks(); color("#7fb3d9")plugs(); color("#3b6ea5")cables();}
 if(!h("heads"))color("#222")m6_heads();
 if(!h("pins"))color("#3fb8a8")pins();
}
if(part=="pin1"||part=="pin2"||part=="pin3")pin(0.45,part=="pin1"?1:part=="pin2"?2:3);
