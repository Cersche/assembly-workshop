// Own rack system, DRAFT 6 concept (Brian 2026-11-12): draft 5 reshaped as a "rounded cube" with Lab Rax style frame joints.
// Viewer only, unprinted; fit and strength UNKNOWN.
// Draft 6: the top and bottom are each a front edge, a rear edge and two side rails (as the Lab Rax frame, without its 45 deg face).
// Each edge has a plug down into each post end (vertical tongue) and a tongue into each side rail (horizontal tongue),
// each held by one M6 x 10 driven from inside the rack. Every outer edge of the rack has the same 15 mm radius.
// Frame as the faceplate parts: X centred, Y=0 front face of the front post flange, Y=240 rear, Z=0 bottom of the lowest U.
// U standard kept from the Lab Rax posts: 44.45 per U, holes X +/-118.2625 at U centre and +/-15.902,
// flange Y 0..6 from X 111.12, side wall inner face X 127.12, post 35 deep, outer face X 141.12, depth 240.
// Hardware: M6 x 10 button head + M6 x 5 x 8 heat-set inserts. Fan: 4 x M3 x 35 from below into M3 inserts (Brian OK 2026-11-11).
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
r_out=look=="B"?15:10; r_in=4; H=24; pt=4; TABH=20; jx=134.12;
yf=-ws_plate_t;      // flush bezel: post front steps forward by the plate thickness
ZT=rack_u*ws_pitch;
pan_e=[[30,13.6],[108,13.6]];                         // M6 panel screws into each edge, per half
pan_r=[[119.2,68],[119.2,105]];                       // M6 panel screws into each rail, per end
pan_xy=concat(pan_e,pan_r);
cleat_x=[25,65,105];                                  // M6 inserts in the rear top edge's rear face
R=r_out;             // rounded cube: the top and bottom edges get the same radius as the upright corners
plug=[6,24,20];      // vertical tongue into the post end: thickness X, length Y, drop Z (Lab Rax: 6.86 x 23.85 x 19.85)
plug_y=11;           // post pocket starts here; it is open to the inside and to the rear, as on the Lab Rax post
plug_sy=25;          // plug screw: between the accent channel (Y 12..20) and the side panel groove (Y 30.9)
tng=[6,20,16];       // horizontal tongue into the side rail, on the rail's inside face: thickness X, length Y, height Z
jc=0.2;              // joint clearance (unprinted guess)
fan=[195,155,186];   // CT200: frame, hole square, opening (Thermaltake drawing; not measured)
// Brian 2026-11-11: the fan does NOT stick out. It hangs under the top panel, whose grille is flush with the rack top.
// The top brackets are taller (Ht) so the whole fan sits above the U stack: nothing enters slot 1.
ptt=6;               // top panel thickness: room for M3 inserts, M3 x 35 from below through the fan
Ht=ptt+30+2;         // top bracket height: panel + fan + 2 spare
// Wire management (draft 5). Tie slot 5.5 x 2.6, the size already used on Brian's rear-lane bar: for ties up to
// about 4.8 wide (ASSUMPTION, unprinted). Every tie point is a tunnel modeled into a rack part: no add-on parts, no screws.
tie=[5.5,2.6]; tie_a=6.5;   // tie_a: where the 45 deg tunnel meets each face, measured from the edge (3.3 bridge left at the edge)
tie_by=[62,100];             // tie tunnels along each side rail (Y from each post face); moved clear of the rail tongue
ent=[46,90,12];              // cable entry notch in the rear bottom brackets: X from, X to, depth
floor_x=[-80,-40,0,40,80]; floor_y=[70,120,170];   // tie stations in the bottom panel (rear row, side rows)
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
  // pocket for the edge's plug, and the M6 insert its screw goes into (driven from inside the rack)
  if(top==0){translate([xw-1,plug_y,h+bg-plug[2]-jc])cube([plug[0]+1,pd,plug[2]+1]);translate([xw+plug[0],plug_sy,h+bg-plug[2]/2])rotate([0,90,0])ws_insert_bore(ws_insert_m6,6.5);}
  if(bot==0){translate([xw-1,plug_y,-bg-1])cube([plug[0]+1,pd,plug[2]+jc+1]);translate([xw+plug[0],plug_sy,-bg+plug[2]/2])rotate([0,90,0])ws_insert_bore(ws_insert_m6,6.5);}
  translate([136.92,30.9,-TABH-1])cube([2.4,5,h+2*TABH+2]);       // side panel groove
  // tie tunnel round the inside rear corner, one per U; moved 8 away from a lap-joint notch or a plug pocket
  for(i=[0:u-1])translate([xw+tie_a/2,pd-tie_a/2,i*ws_pitch+ws_pitch/2+(top!=1&&i==u-1?-8:0)+(bot!=1&&i==0?8:0)])rotate([0,0,-45])cube([tie[1],14,tie[0]],center=true);
  if(look=="B"){
    translate([xo-1.2,12,-TABH-1])cube([2,8,h+2*TABH+2]);          // accent strip channel
    for(z=[0,h-0.5])translate([0,0,z])linear_extrude(0.5)intersection(){difference(){offset(delta=5)post2d();offset(delta=-1)post2d();}translate([127.5,-10])square([30,60]);}
  }
}}
module post_stack(){e=explode;
  if(joint==2){seg(5,top=1);translate([0,0,5*ws_pitch+e])seg(4,bot=-1);}
  else{seg(4,top=-1);translate([0,0,4*ws_pitch+e])seg(1,top=1,bot=1);translate([0,0,5*ws_pitch+2*e])seg(4,bot=-1);}}

module panel2d(){hull()for(sx=[-1,1],y=[9.2+6,depth-9.2-6])translate([sx*(125-6),y])circle(6);}
module fan_holes(){for(sx=[-1,1],sy=[-1,1])translate([sx*fan[1]/2,sy*fan[1]/2,0])children();}
// tie station through the bottom panel: two slots s apart and a band recess underneath so the tie sits flush
module floor_tie(s=16){for(d=[-s/2,s/2])translate([0,d,0])cube([tie[0],tie[1],20],center=true);
  translate([0,0,0.6-0.01])cube([6,s+tie[1],1.2],center=true);}
module panel(with_fan=false,t=pt,ties=false){difference(){linear_extrude(t)panel2d();
  if(ties){for(x=floor_x)translate([x,205,0])floor_tie();                 // rear crossing, cables run left-right
    for(sx=[-1,1],y=floor_y)translate([sx*98,y,0])rotate(90)floor_tie();}  // side runs, cables run front-back
  for(sx=[-1,1],p=pan_xy,y=[p[1],depth-p[1]])translate([sx*p[0],y,-1])cylinder(d=ws_m6_clear,h=t+2);
  if(with_fan)translate([0,depth/2,0]){translate([0,0,-1])cylinder(d=fan[2],h=t+2,$fn=128);
    fan_holes()ws_insert_bore(ws_insert_m3,5);}}                     // M3 inserts from below, 1 mm skin on top
  if(with_fan)translate([0,depth/2,t-3])linear_extrude(3){           // grille, flush with the top
    for(r=[31,62])difference(){circle(r+1.2);circle(r-1.2);}
    for(a=[45,135])rotate(a)square([fan[2]+2,2.4],center=true);}}
module fan_standin(){difference(){linear_extrude(30)offset(r=12)square(fan[0]-24,center=true);translate([0,0,-1])cylinder(d=fan[2],h=32,$fn=128);
  fan_holes()translate([0,0,-1])cylinder(d=4.3,h=32);}}
// rounded cube mask in a frame part's own coordinates (Z=0 on the post end, h = the rack's outer face)
module rbox(h){hull()for(sx=[-1,1],y=[yf+R,depth-yf-R],z=[-600,h-R])translate([sx*(xo-R),y,z])sphere(R);}
// M6 x 10 through a 6 mm tongue, driven along +X from the tongue's inside face: 2 recess, 4 web, 6 into the insert
module tscrew(){rotate([0,90,0]){translate([0,0,-1])cylinder(d=ws_m6_clear,h=12);translate([0,0,-10])cylinder(d=ws_m6_head_d,h=12);}}
module ymir(){children();translate([0,depth,0])mirror([0,1,0])children();}
module xmir(){children();mirror([1,0,0])children();}
// front edge (the rear one is its mirror), full width, drawn as the top one: Z=0 on the post ends. h tall, pocket for a panel t thick.
// The beam is 21 deep so the fan clears it; the ends are post-deep and carry the plug and the tongue.
module edge(h,t,cleat=false,entry=false){difference(){
  union(){
    intersection(){linear_extrude(h)offset(r=-3)offset(delta=3){translate([-xo,yf])square([2*xo,21-yf]);xmir()translate([113.12,yf])square([xo-113.12,pd-yf]);}rbox(h);}
    xmir(){translate([xw,plug_y+jc,-plug[2]])cube([plug[0]-jc,plug[1]-jc,plug[2]+1]);     // plug down into the post
      translate([113.12,pd-1,0])cube([tng[0],tng[1]+1,tng[2]]);}                           // tongue back into the rail
  }
  translate([0,0,h-t])linear_extrude(t+1)offset(delta=0.2)panel2d();
  xmir(){translate([xw,plug_sy,-plug[2]/2])tscrew();translate([113.12,pd+tng[1]/2,tng[2]/2])tscrew();
    for(p=pan_e)translate([p[0],p[1],h-t])mirror([0,0,1])ws_insert_bore(ws_insert_m6,7);
    if(cleat)for(x=cleat_x)translate([x,yf,h/2])rotate([-90,0,0])ws_insert_bore(ws_insert_m6,7);
    // cable entry notch, open towards the U stack so a cord of any plug size can be laid in
    if(entry)hull(){translate([ent[0],yf-1,-5])cube([ent[1]-ent[0],30,1]);for(x=[ent[0]+4,ent[1]-4])translate([x,yf-1,ent[2]-4])rotate([-90,0,0])cylinder(r=4,h=30);}}
}}
// side rail between the front and rear edges, drawn as the top right one. It drops onto the two tongues.
module rail(h,t){difference(){
  intersection(){translate([113.12,pd+jc,0])cube([xo-113.12,depth-2*pd-2*jc,h]);rbox(h);}
  translate([0,0,h-t])linear_extrude(t+1)offset(delta=0.2)panel2d();
  ymir(){translate([113.12-1,pd,-1])cube([tng[0]+jc+1,tng[1]+jc,tng[2]+jc+1]);                       // rebate for the tongue
    translate([113.12+tng[0]+jc,pd+tng[1]/2,tng[2]/2])rotate([0,90,0])ws_insert_bore(ws_insert_m6,6.5);
    for(p=pan_r)translate([p[0],p[1],h-t])mirror([0,0,1])ws_insert_bore(ws_insert_m6,7);
    // tie tunnels round the rail's inner edge on the U-stack side
    for(y=tie_by)translate([113.12+tie_a/2,y,tie_a/2])rotate([0,-45,0])cube([tie[1],tie[0],14],center=true);}
}}
// flush side panel half: drops into the post grooves from above before the top brackets go on
module side_panel(lower){hz=ZT/2+bg;difference(){
  union(){translate([137.12,35.3,0])cube([4,169.4,hz]);translate([137.12,31.3,0])cube([2,177.4,hz]);}
  if(lower)for(y=[55:10:185])hull()for(z=[14,76])translate([130,y,z])rotate([0,90,0])cylinder(d=4,h=20,$fn=16);}}
// rack half of the wall cleat: bolts to the rear top brackets (4 x M6) and the rear posts' top holes (2 x M6).
// 45 deg hook along the bottom, pointing down at the wall side. The wall half comes later.
// The bar sits on the taller top brackets only, so it covers none of the rear U1 opening; two ears reach down to the posts.
cl_t=12; cz0=ZT-4; czt=ZT+bg+Ht-12;   // the bar stops where the rounded top edge starts
 cl_w=252; ear_z=8*ws_pitch+ws_pitch/2+ws_hole_dz-9;
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
module ends(){for(sy=[0,1]){$rear=sy;translate([0,sy*depth,0])mirror([0,sy,0])children();}}
function on(p)=part==p||part=="all";

translate([xoff,0,0]){
if(on("posts"))four()post_stack();
if(part=="joint")post_stack();
if(on("frame_edges")){translate([0,0,ZT+bg])ends()edge(Ht,ptt,cleat=$rear==1);mirror([0,0,1])translate([0,0,bg])ends()edge(H,pt,entry=$rear==1);}
if(on("frame_rails"))xmir(){translate([0,0,ZT+bg])rail(Ht,ptt);mirror([0,0,1])translate([0,0,bg])rail(H,pt);}
if(part=="one_edge")edge(Ht,ptt,cleat=true);     // bed-fit check only
if(part=="one_rail")rail(Ht,ptt);
if(part=="frame_joint"){translate([0,-explode,explode])edge(Ht,ptt);translate([0,0,2*explode])rail(Ht,ptt);translate([0,0,-4*ws_pitch-bg])seg(4,bot=-1);}
if(on("top_fan_panel"))translate([0,0,ZT+bg+Ht-ptt])panel(true,ptt);
if(on("bottom_panel"))translate([0,0,-H-bg])panel(ties=true);
if(on("side_panels"))for(sx=[0,1])mirror([sx,0,0]){translate([0,0,-bg])side_panel(true);translate([0,0,ZT/2])side_panel(false);}
if(on("fan_CT200_standin"))translate([0,depth/2,ZT+bg+Ht-ptt-30])fan_standin();
if(on("example_faceplates"))for(k=[0:2])translate([0,0,k*3*ws_pitch]){ws_plate(1);translate([0,0,ws_pitch])ws_plate(2);}
if(on("cleat_rack_half"))cleat_rack();
if(part=="accents"||(part=="all"&&look=="B")){
  four()translate([xo-1,12.2,-bg])cube([1,7.6,ZT+2*bg]);}   // draft 6: no screw caps, the frame screws are inside the rack
}
// preview only, never printed: where cables are meant to run (fan lead, a trunk, the bottom crossing)
module run(pts,d=5){for(i=[0:len(pts)-2])hull(){translate(pts[i])sphere(d=d,$fn=16);translate(pts[i+1])sphere(d=d,$fn=16);}}
// Brian 2026-11-12: power on the left facing the rack front (-X), network on the right (+X); no top crossing.
if(part=="wire_routes_preview")translate([xoff,0,0])mirror([1,0,0]){
  run([[104,30,ZT+12],[106,200,ZT+10],[120,216,ZT-8],[120,216,6],[104,205,-12],[68,215,-10],[68,250,-7]],4);   // CT200 lead, power side
  run([[-120,216,300],[-120,216,6],[-104,205,-12],[-68,215,-10],[-68,250,-7]],7);                            // network trunk, network side
  run([[-80,205,-15],[80,205,-15]],7);}                                                                      // bottom crossing
