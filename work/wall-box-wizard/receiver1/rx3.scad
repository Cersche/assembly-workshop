// MoCA receiver box, concept 3 "bones" (Brian, 2026-10-31; replaces rx2's layout). Living-room shelf box, oblong, the
// LONG side is the back. Back wall: ETH1 + ETH2 as a pair at the left end, coax in the middle-right. Front wall: one
// Ethernet keystone at the right, under the switch's ports. Wiring: coax keystone -> short RG6 jumper -> ScreenBeam
// Coax In (Brian picked a jumper over the rigid right-angle chain); ScreenBeam LAN -> ETH1 -> Google Wifi WAN; Google
// Wifi LAN -> ETH2 -> inside patch -> front keystone -> 6 in patch -> TP-Link TL-SG105 sitting on the lid.
// Cosmetics come later (Brian). PROPOSED - UNVALIDATED, not printed: port positions, plug sizes, jumper bend, fit and
// strength UNKNOWN.
//
// Coordinates: X 0..WO (left -> right, seen from the front), Y 0..DO (front -> back), Z 0..HO (floor -> rim).
// part: "body" | "lid" | "cradle" | "devices" (context, never printed) | "lid_on" (viewer) | "all"
part="all";

use <../concept15/body15.scad>   // ks_gold_one(): golden keystone, ks_tight 0.2

$fn=40;
t=2.5; cr=6; insert_pilot=4.0; m3=3.4;

// ScreenBeam (Brian): 120 x 65 x 30 incl. feet (13 dia, 2.25 proud, centres 8 in from the long edges, 16 from the
// ends). Lies along X: LAN/power end at the left, Coax In end at the right. Port positions ASSUMED (first box's model):
// coax centred across, 19 below the vent face (Brian); power 24 and LAN 43 from the front long edge, mid-height.
SB=[120,65,30]; foot_h=2.25; sb_clr=0.5;
sb_feet=[for(x=[16,104],y=[8.5,56.5])[x,y]]; foot_d=16; foot_dp=2.6;
coax_y=32.5; coax_z=SB[2]-foot_h-19; pwr_y=24; eth_y=43; port_z=(SB[2]-foot_h)/2;

// TL-SG105 on the lid, right end, ports to the front (100 x 98 x 25, retailer listings; power jack on the rear).
SW=[100,98,25]; sw_clr=0.25;

bay=55;      // left: ScreenBeam power + LAN plugs (power 44.5 incl. tip)
rzone=42;    // right: jumper's right-angle on Coax In, front keystone plug room
bzone=35;    // behind the ScreenBeam: plug room for the back keystones, jumper and patch runs
boss_h=4; plate=4;

IW=bay+SB[0]+rzone; ID=3+SB[1]+3+bzone+2; IH=boss_h+plate+SB[2]-foot_h+6;
WO=IW+2*t; DO=ID+2*t; HO=IH+t;

sbx0=t+bay; sbx1=sbx0+SB[0]; sby0=t+3; sby1=sby0+SB[1];
plate_z=t+boss_h; case_z=plate_z+plate;
ks_z=t+17;                                   // all four keystones on one line (jack axis)
ks_eth1=t+20; ks_eth2=t+43;                  // back, left pair (X)
ks_coax=WO-70;                               // back, middle-right (X)
ks_front=WO-t-19;                            // front, right, under the switch's ports (X)
pwr_hole=[t+55, t+10];                       // ScreenBeam power, left wall (Y, Z), 10 mm (plug passes through)
ears=[for(x=[sbx0-7,sbx1+7],y=[sby0+10,sby1-10])[x,y]];

module rrect(x0,x1,y0,y1,r){hull()for(x=[x0+r,x1-r],y=[y0+r,y1-r])translate([x,y])circle(r=r);}
// wall frames as in body15.scad: u to the right seen from outside, y inward, v up
module on_front(x,z){multmatrix([[1,0,0,x],[0,1,0,0],[0,0,1,z],[0,0,0,1]])children();}
module on_back(x,z){multmatrix([[-1,0,0,x],[0,-1,0,DO],[0,0,1,z],[0,0,0,1]])children();}
module ks_hole(){translate([-10.5,-0.01,-15])cube([21,4.02,33.5]);}
module back_ks(){for(x=[ks_eth1,ks_eth2,ks_coax])on_back(x,ks_z)children();}
function lid_posts()=[[t+3.5,t+3.5],[WO-t-3.5,t+3.5],[t+3.5,DO-t-3.5],[WO-t-3.5,DO-t-3.5]];

module body(){
 difference(){
  union(){
   difference(){
    linear_extrude(HO)rrect(0,WO,0,DO,cr);
    translate([0,0,t])linear_extrude(HO)rrect(t,WO-t,t,DO-t,cr-t);
   }
   for(e=ears)translate([e[0],e[1],t-0.01])cylinder(d=10,h=boss_h+0.01);
   for(p=lid_posts())translate([p[0],p[1],0])cylinder(d=9,h=HO);
  }
  for(e=ears)translate([e[0],e[1],t+boss_h-5.7])cylinder(d=insert_pilot,h=6);
  for(p=lid_posts())translate([p[0],p[1],HO-7])cylinder(d=insert_pilot,h=7.1);
  back_ks()ks_hole();
  on_front(ks_front,ks_z)ks_hole();
  translate([-1,pwr_hole[0],pwr_hole[1]])rotate([0,90,0])cylinder(d=10,h=t+2);
 }
 back_ks()ks_gold_one(0,0);
 on_front(ks_front,ks_z)ks_gold_one(0,0);
}

// Lid: 2.5 plate, locating lip, four countersunk M3. Switch corner fence (4 tall) at the right end, ports to the front;
// vent slots over the part of the ScreenBeam the switch doesn't cover.
swx0=WO-6-SW[0]; swy0=(DO-SW[1])/2-2;
module lid(){
 difference(){
  union(){
   linear_extrude(t)rrect(0,WO,0,DO,cr);
   translate([0,0,-3])linear_extrude(3.01)difference(){rrect(t+0.3,WO-t-0.3,t+0.3,DO-t-0.3,cr-t);
    rrect(t+1.9,WO-t-1.9,t+1.9,DO-t-1.9,cr-t);
    for(p=lid_posts())translate(p)circle(d=11);}
   translate([0,0,t-0.01])linear_extrude(4)difference(){
    translate([swx0-sw_clr-1.6,swy0-sw_clr])square([SW[0]+2*sw_clr+3.2,SW[1]+2*sw_clr+1.6]);
    translate([swx0-sw_clr,swy0-sw_clr-1])square([SW[0]+2*sw_clr,SW[1]+2*sw_clr+1]);
    translate([swx0+15,swy0])square([SW[0]-30,SW[1]+5]);   // corner fences only
    translate([swx0-5,swy0+15])square([SW[0]+10,SW[1]-30]);
   }
  }
  for(p=lid_posts())translate([p[0],p[1],-4]){cylinder(d=m3,h=10);translate([0,0,4+t-1.7])cylinder(d1=m3,d2=6.6,h=1.71);}
  for(x=[sbx0-30:5.5:swx0-10])translate([x-1.25,sby0+8,-1])cube([2.5,SB[1]-16,t+2]);
 }
}

// Cradle: plate with foot pockets and side lips on four floor bosses (plain M3 holes: the jumper takes up any
// misalignment, so no adjustment slots or shims).
module cradle(){
 difference(){
  union(){
   translate([0,0,plate_z])linear_extrude(plate)union(){
    rrect(sbx0+1,sbx1-1,sby0-sb_clr/2-2,sby1+sb_clr/2+2,3);
    for(e=ears)translate(e)rrect(-7,7,-7,7,3);
    for(e=ears)hull(){translate(e)square([1,14],center=true);translate([e[0]<sbx0+60?sbx0+4:sbx1-4,e[1]])square([1,14],center=true);}
   }
   for(y=[sby0-sb_clr/2-2,sby1+sb_clr/2])translate([sbx0+15,y,case_z-0.01])cube([SB[0]-30,2,6]);
  }
  for(e=ears)translate([e[0],e[1],plate_z-1])cylinder(d=m3,h=plate+2);
  for(f=sb_feet)translate([sbx0+f[0],sby0+f[1],case_z-foot_dp])cylinder(d=foot_d,h=foot_dp+0.1,$fn=48);
 }
}

module rod(a,b,d){hull(){translate(a)sphere(d=d,$fn=16);translate(b)sphere(d=d,$fn=16);}}
module plug_in(x,z){color([0.2,0.4,0.9])translate([x-8,DO-t-34,z-6])cube([16,30,12]);}   // patch plug in a back keystone
module devices(){
 pz=case_z+port_z; cz=case_z+coax_z; kb=DO-t-34; kf=t+34;
 color([0.12,0.12,0.13])translate([sbx0,sby0,case_z])cube([SB[0],SB[1],SB[2]-foot_h]);
 color([0.1,0.1,0.1])for(f=sb_feet)translate([sbx0+f[0],sby0+f[1],case_z-foot_h])cylinder(d=13,h=foot_h);
 // power: straight out of the left end, U-turn, out the left wall
 color("silver")translate([sbx0,sby0+pwr_y,pz])rotate([0,-90,0])cylinder(d=7.75,h=35);
 color([0.15,0.15,0.15]){rod([sbx0-35,sby0+pwr_y,pz],[sbx0-42,pwr_hole[0],pz],4);rod([sbx0-42,pwr_hole[0],pz],[-15,pwr_hole[0],pwr_hole[1]],4);}
 // ScreenBeam LAN -> ETH1
 color([0.2,0.4,0.9])translate([sbx0-28,sby0+eth_y-6.5,pz-6])cube([28,13,12]);
 plug_in(ks_eth1,ks_z);plug_in(ks_eth2,ks_z);plug_in(ks_coax,ks_z);
 color([0.15,0.15,0.15]){rod([sbx0-28,sby0+eth_y,pz],[ks_eth1,kb-8,ks_z],6);
 // ETH2 -> along the back, round the right end -> front keystone
  rod([ks_eth2,kb,ks_z],[ks_eth2+10,kb-6,ks_z+8],6);rod([ks_eth2+10,kb-6,ks_z+8],[WO-t-12,kb-6,ks_z+8],6);
  rod([WO-t-12,kb-6,ks_z+8],[ks_front,kf,ks_z],6);}
 color([0.2,0.4,0.9])translate([ks_front-8,t+4,ks_z-6])cube([16,30,12]);
 // coax: right-angle F male on Coax In, short RG6 jumper round to the back of the coax keystone
 color("silver")translate([sbx1,sby0+coax_y,cz])rotate([0,90,0])cylinder(d=10,h=14);
 color([0.95,0.95,0.95]){rod([sbx1+10,sby0+coax_y,cz],[sbx1+10,sby1+12,cz+6],7);rod([sbx1+10,sby1+12,cz+6],[ks_coax,kb,ks_z],7);}
 // switch on the lid, ports to the front; 6 in patch down to the front keystone
 color([0.2,0.35,0.6])translate([swx0,swy0,HO+t])cube(SW);
 color([0.05,0.05,0.05])for(i=[0:4])translate([swx0+8+i*17,swy0-0.2,HO+t+5])cube([14,1,12]);
 color([0.85,0.85,0.85])rod([swx0+8+4*17+7,swy0-12,HO+t+11],[ks_front,-14,ks_z],5);
 // outside: coax in, ETH1 to / ETH2 from the Google Wifi
 color([0.95,0.95,0.95])for(x=[ks_eth1,ks_eth2,ks_coax])rod([x,DO+4,ks_z],[x,DO+40,ks_z-12],x==ks_coax?7:5);
}

if(part=="body")body();
if(part=="lid")lid();
if(part=="lid_on")translate([0,0,HO])lid();
if(part=="cradle")cradle();
if(part=="devices")devices();
if(part=="all"){color([0.92,0.91,0.87])body();color([0.55,0.75,0.6])cradle();devices();
 color([0.8,0.8,0.85,0.6])translate([0,0,HO])lid();
 echo(str("outer ",WO," x ",DO," x ",HO," (+ lid ",t,")"));}
