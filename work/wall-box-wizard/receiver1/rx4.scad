// MoCA receiver box, concept 4 "bones" (Brian, 2026-11-01; builds on rx3). One box for a cleaner look: the TP-Link
// TL-SG105 now lives INSIDE, on a removable shelf above the ScreenBeam ("stacked, compact"), ports out of a front
// window. Front wall, seen from the front: switch window at the left, Ethernet keystone to its right (Brian, 2026-11-01;
// 6 in jumper between them on the outside, to the nearest switch port). Back wall: ETH1 + ETH2 pair at the left end, coax middle-right with the ScreenBeam's power hole beside it,
// plus the switch's power hole. Wiring: coax keystone -> short RG6 jumper -> ScreenBeam Coax In; ScreenBeam LAN -> ETH1 ->
// Google Wifi WAN; Google Wifi LAN -> ETH2 -> inside patch -> front keystone -> 6 in jumper -> switch.
// Shelf drops in on wall ledges after the ScreenBeam; the lid's ribs clamp switch and shelf (no screws). Cosmetics come
// later (Brian). PROPOSED - UNVALIDATED, not printed: port positions, plug sizes, jumper bend, heat, fit and strength
// UNKNOWN.
//
// Coordinates: X 0..WO (left -> right, seen from the front), Y 0..DO (front -> back), Z 0..HO (floor -> rim).
// part: "body" | "base" (removable bottom) | "lid" | "shelf" | "cradle" | "devices" (context, never printed) | "lid_on" (viewer) | "all"
part="all";

use <../concept15/body15.scad>   // ks_gold_one(): golden keystone, ks_tight 0.2

$fn=40;
t=2.5; cr=12; er=2; insert_pilot=4.2; insert_d=4; m3=3.4;   // M3 x 3 x 5 heat-set insert: 4.2 bore, 4 deep

// ScreenBeam (Brian): 120 x 65 x 30 incl. feet (13 dia, 2.25 proud, centres 8 in from the long edges, 16 from the
// ends). Lies along X: LAN/power end at the left, Coax In end at the right. Coax In (Brian measured, 2026-11-01): centre
// 22 from the box-back long side (43 from the front), 15.25 up from the case bottom (feet not included). Power 24 and
// LAN 43 from the front long edge, mid-height: still ASSUMED (first box's model).
SB=[120,65,30]; foot_h=2.25; sb_clr=0.5;
sb_feet=[for(x=[16,104],y=[8.5,56.5])[x,y]]; foot_d=16; foot_dp=2.6;
coax_y=SB[1]-22; coax_z=15.25; pwr_y=24; eth_y=43; port_z=(SB[2]-foot_h)/2;

// TL-SG105 (100 x 98 x 25, retailer listings), ports to the front; fit copied from the supplied bracket (sleeve
// 100.5 x 25.5 -> 0.25 a side). Power jack on the rear (Brian measured, 2026-11-01): centre 12 from the switch's left
// side seen from the front (right side seen from the rear), 13 up from its bottom. Barrel plug 35.25 long overall, 8.5
// wide, sticks out 26 from the switch's back face: ends 7 short of the back wall (33 gap), cord straight out the 11 mm hole.
SW=[100,98,25]; sw_clr=0.25; sw_jack=[12,13]; sw_plug=[26,8.5]; sw_lip=1.5;

bay=55;      // left: ScreenBeam power + LAN plugs (power 44.5 incl. tip); front keystone above them
rzone=42;    // right: jumper's right-angle on Coax In
bzone=55;    // behind the ScreenBeam: back keystone plugs, jumper, patch runs; 30 behind the switch for its power plug (Brian: "a little longer", was 35); 58 -> 55 when the ScreenBeam moved back for cradle travel
travel=3; sb_front=3+travel;   // cradle adjusts +-travel in X and Y (Brian, 2026-11-01); ScreenBeam front gap leaves room for it
boss_h=4; plate=4; sh=2.5;   // cradle bosses, cradle plate, switch shelf

plate_z=t+boss_h; case_z=plate_z+plate;
shelf_z=case_z+SB[2]-foot_h+2;              // shelf underside, 2 above the ScreenBeam
sw_z=shelf_z+sh;                             // switch bottom
IW=bay+SB[0]+rzone; ID=sb_front+SB[1]+3+bzone+2; HO=sw_z+SW[2]+1.5;
WO=IW+2*t; DO=ID+2*t;

sbx0=t+bay; sbx1=sbx0+SB[0]; sby0=t+sb_front; sby1=sby0+SB[1];
ks_z=t+17;                                   // back keystones (jack axis)
ks_eth1=t+20; ks_eth2=t+43;                  // back, left pair (X)
ks_coax=sbx1+10;                             // back, right: in line with the right-angle F's free post (Brian, 2026-11-01; was WO-70)
ks_cz=case_z+coax_z;                         // coax keystone at the Coax In height, so the jumper runs straight back
swx0=t+41.5;                                 // switch left side (X), unchanged
ks_front=sbx1+10.5; ks_fz=40;                // front keystone right of the switch window, just past the ScreenBeam's right end, above its coax plug (Brian)
 swx1=swx0+SW[0]; swy0=t; // switch front face against the front wall
sl=[swx0-sw_clr-2, swx1+sw_clr+2];           // shelf X span
pwr_hole=[ks_coax-22, t+10];                 // ScreenBeam power, back wall beside the coax (X, Z), 10 mm (Brian: power comes in the back with the coax)
sw_pwr=[swx0+sw_jack[0], sw_z+sw_jack[1]];   // switch power, back wall (X, Z), 11 mm (plug passes through)
bl=[60, ks_coax-14];                         // back ledge X span (clear of the ETH2 and coax keystones)
pins=[75,125];                               // shelf locating pins into the back ledge (X)
ears=[for(x=[sbx0-11,sbx1+11],y=[sby0+10,sby1-10])[x,y]];   // cradle ears / base inserts; 22 pads end at the ScreenBeam's ends

// Test print ID (Brian's rule: every test print carries its ID), engraved 0.6 on hidden faces
print_id="RX4-B";
module id_text(){text(print_id,size=6,font="Liberation Sans:style=Bold",halign="center",valign="center");}
module rrect(x0,x1,y0,y1,r){hull()for(x=[x0+r,x1-r],y=[y0+r,y1-r])translate([x,y])circle(r=r);}
// wall frames as in body15.scad: u to the right seen from outside, y inward, v up
module on_front(x,z){multmatrix([[1,0,0,x],[0,1,0,0],[0,0,1,z],[0,0,0,1]])children();}
module on_back(x,z){multmatrix([[-1,0,0,x],[0,-1,0,DO],[0,0,1,z],[0,0,0,1]])children();}
module ks_hole(){translate([-10.5,-0.01,-15])cube([21,4.02,33.5]);}
module back_ks(){for(k=[[ks_eth1,ks_z],[ks_eth2,ks_z],[ks_coax,ks_cz]])on_back(k[0],k[1])children();}
// corner posts on the corner diagonal, 1.2 skin outside the 9 mm post (follows cr)
pc=cr-(cr-4.5-1.2)/sqrt(2);
function lid_posts()=[[pc,pc],[WO-pc,pc],[pc,DO-pc],[WO-pc,DO-pc]];
// outer plate (lid / base) with its outside edge rounded by er; rounded edge at the top, flip for the base
module rplate(h){hull(){linear_extrude(h-er)rrect(0,WO,0,DO,cr);
 for(a=[0:15:90])translate([0,0,h-er+er*sin(a)])linear_extrude(0.01)offset(delta=-(er-er*cos(a)))rrect(0,WO,0,DO,cr);}}
// 45-degree ledge on a wall: strip at the wall bottom, full depth at the top (prints without support)
module ledge(x0,x1,y0,d,dir){hull(){translate([x0,dir>0?y0:y0-0.01,shelf_z-d-0.01])cube([x1-x0,0.01,0.01]);
 translate([x0,dir>0?y0:y0-d,shelf_z-0.01])cube([x1-x0,d,0.01]);}}

// Side vents (Brian, 2026-11-01): vertical slots in both end walls (X = 0 and X = WO), round-ended so they print
// upright without support; clear of the rounded corners, the base lip below and the lid lip above.
vent_w=3; vent_z=[16,50]; vent_y=[28:6:DO-28];
module side_vents(){for(x=[-1,WO-t-1],y=vent_y)hull()for(z=vent_z)translate([x,y,z])rotate([0,90,0])cylinder(d=vent_w,h=t+2);}

// Body: open-bottom wall tube, Z t..HO; the removable base below it (Brian, 2026-11-01) and the lid on top screw into
// M3 inserts at both ends of the four corner posts.
module body(){
 difference(){
  union(){
   translate([0,0,t])linear_extrude(HO-t)difference(){rrect(0,WO,0,DO,cr);rrect(t,WO-t,t,DO-t,cr-t);}
   for(p=lid_posts())translate([p[0],p[1],t])cylinder(d=9,h=HO-t);
   ledge(sl[0],sl[1],t-0.01,2.5,1);          // front ledge: stops 0.5 short of the ScreenBeam (drops in past it)
   ledge(bl[0],bl[1],DO-t+0.01,5,-1);        // back ledge
  }
  for(p=lid_posts())translate([p[0],p[1],HO-insert_d])cylinder(d=insert_pilot,h=insert_d+0.1);
  for(p=lid_posts())translate([p[0],p[1],t-0.1])cylinder(d=insert_pilot,h=insert_d+0.1);
  back_ks()ks_hole();
  on_front(ks_front,ks_fz)ks_hole();
  translate([swx0+sw_lip,-1,sw_z+sw_lip])cube([SW[0]-2*sw_lip,t+2,SW[2]-2*sw_lip]);   // switch window, 1.5 lip
  translate([pwr_hole[0],DO+1,pwr_hole[1]])rotate([90,0,0])cylinder(d=10,h=t+2);
  translate([sw_pwr[0],DO+1,sw_pwr[1]])rotate([90,0,0])cylinder(d=11,h=t+2);
  translate([100,DO-t+0.6,t+7])rotate([90,0,0])linear_extrude(0.61)id_text();   // ID on the inside of the back wall
  side_vents();
 }
 for(x=pins)translate([x,DO-t-2.5,shelf_z-0.01])cylinder(d=3,h=2.4);   // shelf locating pins, up from the back ledge
 back_ks()ks_gold_one(0,0);
 on_front(ks_front,ks_fz)ks_gold_one(0,0);
}

// Shelf: 2.5 plate wall to wall over the ScreenBeam, side rails and a back stop for the switch, vent slots, two holes
// over the back ledge's pins (pins on the body so the shelf prints flat). Drops in after the ScreenBeam; the lid ribs
// hold it and the switch down.
module shelf(){
 difference(){
  union(){
   translate([sl[0],t+0.2,shelf_z])cube([sl[1]-sl[0],ID-0.4,sh]);
   for(x=[sl[0],swx1+sw_clr])translate([x,t+15,sw_z-0.01])cube([2,SW[1]-15+sw_clr,5]);
   translate([swx0+20,swy0+SW[1]+sw_clr,sw_z-0.01])cube([SW[0]-40,2,5]);
  }
  for(x=[swx0+12:6:swx1-12])translate([x-1.25,t+12,shelf_z-1])cube([2.5,SW[1]-24,sh+2]);
  for(x=pins)translate([x,DO-t-2.5,shelf_z-1])cylinder(d=3.4,h=sh+2);
  translate([95,118,sw_z-0.6])linear_extrude(1)id_text();
 }
}

// Lid: 2.5 plate, locating lip (cut where the switch meets the front wall), four countersunk M3, two ribs that clamp
// the switch (0.3 clearance), vent slots over the ScreenBeam's uncovered right part.
module lid(){
 difference(){
  union(){
   rplate(t);
   translate([0,0,-3])linear_extrude(3.01)difference(){rrect(t+0.3,WO-t-0.3,t+0.3,DO-t-0.3,cr-t);
    rrect(t+1.9,WO-t-1.9,t+1.9,DO-t-1.9,cr-t);
    for(p=lid_posts())translate(p)circle(d=11);
    translate([swx0-sw_clr-1,0])square([SW[0]+2*sw_clr+2,t+3]);}
   for(y=[swy0+25,swy0+SW[1]-25])translate([swx0+10,y-1,-1.2])cube([SW[0]-20,2,1.21]);
  }
  for(p=lid_posts())translate([p[0],p[1],-4]){cylinder(d=m3,h=10);translate([0,0,4+t-1.7])cylinder(d1=m3,d2=6.6,h=1.71);}
  translate([190,105,-0.01])mirror([1,0,0])linear_extrude(0.61)id_text();   // ID on the underside
  for(x=[sl[1]+6:5.5:sbx1+30])translate([x-1.25,sby0+8,-1])cube([2.5,SB[1]-16,t+2]);
 }
}

// Base: removable bottom, 2.5 plate with a 3 mm locating lip (notched at the corner posts and the back keystone frames),
// four countersunk M3 up into the post inserts, and the cradle's four insert bosses. ScreenBeam + cradle can be fitted
// on the base outside the box, then the body lowered over them.
module base(){
 difference(){
  union(){
   translate([0,0,t])mirror([0,0,1])rplate(t);
   translate([0,0,t-0.01])linear_extrude(3.01)difference(){rrect(t+0.3,WO-t-0.3,t+0.3,DO-t-0.3,cr-t);
    rrect(t+1.9,WO-t-1.9,t+1.9,DO-t-1.9,cr-t);
    for(p=lid_posts())translate(p)circle(d=11);
    for(x=[ks_eth1,ks_eth2,ks_coax])translate([x-12,DO-t-3])square([24,3]);}
   for(e=ears)translate([e[0],e[1],t-0.01])cylinder(d=10,h=boss_h+0.01);
  }
  for(e=ears)translate([e[0],e[1],t+boss_h-insert_d])cylinder(d=insert_pilot,h=insert_d+0.1);
  for(p=lid_posts())translate([p[0],p[1],-1]){cylinder(d=m3,h=t+2);translate([0,0,1-0.01])cylinder(d1=6.6,d2=m3,h=1.71);}
  translate([WO/2,DO/2,-0.01])mirror([1,0,0])linear_extrude(0.61)id_text();   // ID on the underside
 }
}

// Cradle: plate with foot pockets and side lips on four base bosses. Adjustable (Brian, 2026-11-01: "a little give"),
// +-travel in X and Y: each 22 mm ear pad (2 proud of the plate, outside the ScreenBeam's footprint) has a through slot
// over the fixed base insert and a flat-bottomed track 2.4 deep; a printed countersunk washer rides in the track, so the
// M3 countersunk head seats fully at any position and clamps 3.6 of pad.
pad_up=2; wash=[10,2.4]; wash_clr=0.4;
module cradle(){
 difference(){
  union(){
   translate([0,0,plate_z])linear_extrude(plate)union(){
    rrect(sbx0+1,sbx1-1,sby0-sb_clr/2-2,sby1+sb_clr/2+2,3);
    for(e=ears)hull(){translate(e)square([1,22],center=true);translate([e[0]<sbx0+60?sbx0+4:sbx1-4,e[1]])square([1,22],center=true);}
   }
   for(e=ears)translate([0,0,plate_z])linear_extrude(plate+pad_up)translate(e)rrect(-11,11,-11,11,3);
   for(y=[sby0-sb_clr/2-2,sby1+sb_clr/2])translate([sbx0+15,y,case_z-0.01])cube([SB[0]-30,2,6]);
  }
  for(e=ears){
   hull()for(dx=[-travel,travel],dy=[-travel,travel])translate([e[0]+dx,e[1]+dy,plate_z-1])cylinder(d=m3,h=plate+pad_up+2);
   hull()for(dx=[-travel,travel],dy=[-travel,travel])translate([e[0]+dx,e[1]+dy,case_z+pad_up-wash[1]])cylinder(d=wash[0]+wash_clr,h=wash[1]+1);
  }
  for(f=sb_feet)translate([sbx0+f[0],sby0+f[1],case_z-foot_dp])cylinder(d=foot_d,h=foot_dp+0.1,$fn=48);
  translate([(sbx0+sbx1)/2,sby0+SB[1]/2,plate_z-0.01])mirror([1,0,0])linear_extrude(0.61)id_text();   // ID on the underside
 }
}

// Printed slide washer for the cradle tracks: countersunk for the M3 head, which then sits flush with the pad top.
module washer(){difference(){cylinder(d=wash[0],h=wash[1]);translate([0,0,-1])cylinder(d=m3,h=wash[1]+2);
 translate([0,0,wash[1]-1.7])cylinder(d1=m3,d2=6.6,h=1.71);}}

module rod(a,b,d){hull(){translate(a)sphere(d=d,$fn=16);translate(b)sphere(d=d,$fn=16);}}
module plug_in(x,z){color([0.2,0.4,0.9])translate([x-8,DO-t-34,z-6])cube([16,30,12]);}   // patch plug in a back keystone
module devices(){
 pz=case_z+port_z; cz=case_z+coax_z; kb=DO-t-34; kf=t+34;
 color([0.12,0.12,0.13])translate([sbx0,sby0,case_z])cube([SB[0],SB[1],SB[2]-foot_h]);
 color([0.1,0.1,0.1])for(f=sb_feet)translate([sbx0+f[0],sby0+f[1],case_z-foot_h])cylinder(d=13,h=foot_h);
 // power: straight out of the left end, U-turn, back along the rear zone, out the back wall beside the coax
 color("silver")translate([sbx0,sby0+pwr_y,pz])rotate([0,-90,0])cylinder(d=7.75,h=35);
 color([0.15,0.15,0.15]){rod([sbx0-35,sby0+pwr_y,pz],[sbx0-42,sby0+pwr_y,pz],4);rod([sbx0-42,sby0+pwr_y,pz],[sbx0-42,sby1+6,pz],4);rod([sbx0-42,sby1+6,pz],[pwr_hole[0],DO-t-6,pwr_hole[1]],4);
  rod([pwr_hole[0],DO-t-6,pwr_hole[1]],[pwr_hole[0],DO+40,pwr_hole[1]-8],4);}
 // ScreenBeam LAN -> ETH1
 color([0.2,0.4,0.9])translate([sbx0-28,sby0+eth_y-6.5,pz-6])cube([28,13,12]);
 plug_in(ks_eth1,ks_z);plug_in(ks_eth2,ks_z);plug_in(ks_coax,ks_cz);
 color([0.15,0.15,0.15]){rod([sbx0-28,sby0+eth_y,pz],[ks_eth1,kb-8,ks_z],6);
 // ETH2 -> along the rear zone behind the ScreenBeam, then forward past its right end -> front keystone
  rod([ks_eth2,kb,ks_z],[ks_front,sby1+10,ks_fz],6);rod([ks_front,sby1+10,ks_fz],[ks_front,kf+4,ks_fz],6);}
 color([0.2,0.4,0.9])translate([ks_front-8,t+4,ks_fz-6])cube([16,30,12]);
 // coax: right-angle F male on Coax In, short RG6 jumper round to the back of the coax keystone
 color("silver")translate([sbx1,sby0+coax_y,cz])rotate([0,90,0])cylinder(d=10,h=14);
 color([0.95,0.95,0.95])rod([sbx1+10,sby0+coax_y,cz],[ks_coax,kb,ks_cz],7);
 // switch on the shelf, ports in the front window; power plug through the back wall
 color([0.2,0.35,0.6])translate([swx0,swy0,sw_z])cube(SW);
 color([0.05,0.05,0.05])for(i=[0:4])translate([swx0+8+i*17,swy0-0.2,sw_z+5])cube([14,1,12]);
 color("silver")translate([sw_pwr[0],swy0+SW[1]+sw_plug[0],sw_pwr[1]])rotate([90,0,0])cylinder(d=sw_plug[1],h=sw_plug[0]);
 color([0.15,0.15,0.15])rod([sw_pwr[0],swy0+SW[1]+sw_plug[0],sw_pwr[1]],[sw_pwr[0]+10,DO+40,sw_pwr[1]-30],4);
 // outside: 6 in jumper front keystone -> nearest switch port; coax in, ETH1 to / ETH2 from the Google Wifi
 color([0.85,0.85,0.85]){rod([ks_front,-14,ks_fz],[ks_front-12,-24,ks_fz-4],5);rod([ks_front-12,-24,ks_fz-4],[swx0+83,-12,sw_z+11],5);}
 color([0.95,0.95,0.95])for(k=[[ks_eth1,ks_z],[ks_eth2,ks_z],[ks_coax,ks_cz]])rod([k[0],DO+4,k[1]],[k[0],DO+40,k[1]-12],k[0]==ks_coax?7:5);
}

if(part=="body")body();
if(part=="lid")lid();
if(part=="base")base();
if(part=="lid_on")translate([0,0,HO])lid();
if(part=="shelf")shelf();
if(part=="cradle")cradle();
if(part=="washer")washer();
if(part=="washers")for(i=[0:3])translate([i*14,0,0])washer();   // print 4, flat side down
if(part=="washers_on")for(e=ears)translate([e[0],e[1],case_z+pad_up-wash[1]])washer();
if(part=="devices")devices();
if(part=="all"){color([0.92,0.91,0.87])body();color([0.75,0.72,0.66])base();color([0.55,0.75,0.6])cradle();color([0.9,0.6,0.3])for(e=ears)translate([e[0],e[1],case_z+pad_up-wash[1]])washer();color([0.6,0.7,0.85])shelf();devices();
 color([0.8,0.8,0.85,0.6])translate([0,0,HO])lid();
 echo(str("outer ",WO," x ",DO," x ",HO," (+ lid ",t,")"));}
