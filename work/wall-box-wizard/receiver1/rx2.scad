// MoCA receiver box, concept 2 "bones" (Brian, 2026-10-31; replaces rx1.scad's layout). Living-room shelf box, oblong,
// lid on top. ScreenBeam ECB7250 lies flat, long axis front-back, Coax In at the back: coupled straight to a keystone F
// coupler in the back wall by an F male-male barrel (no jumper), lined up by the adjustable sled. Back wall (Brian,
// 2026-10-31): coax, then ETH1 = ScreenBeam LAN out to the Google Wifi WAN, then ETH2 = Google Wifi LAN back in, patched
// inside to the one front Ethernet keystone. The TP-Link
// TL-SG105 sits on the lid in a low fence, ports to the front, so a 6 in (152 mm) patch reaches the front keystone.
// Cosmetics come later (Brian). PROPOSED - UNVALIDATED, not printed: port positions, coupler/barrel lengths, plug
// sizes, fit and strength UNKNOWN.
//
// Coordinates: X 0..WO (left -> right, seen from the front), Y 0..DO (front -> back), Z 0..HO (floor -> rim).
// part: "body" | "lid" | "sled" | "shims" | "devices" (context, never printed) | "lid_up" (viewer) | "all"
part="all";
lid_lift=40;

use <../concept15/body15.scad>   // ks_gold_one(): golden keystone, ks_tight 0.2

$fn=40;
t=2.5; cr=6; insert_pilot=4.0; m3=3.4;

// ScreenBeam (Brian): 120 x 65 x 30 incl. feet (13 dia, 2.25 proud, centres 8 in from the long edges, 16 from the ends).
// Here X = 65 across, Y = 120 long (coax end at the back), Z = 30.
SB=[65,120,30]; foot_h=2.25; sb_clr=0.5;
sb_feet=[for(x=[8.5,56.5],y=[16,104])[x,y]]; foot_d=16; foot_dp=2.6;
// Coax In (Brian, 2026-10-31): 19 below the vent face (label taken to be on the feet side); centred across, ASSUMED.
// Front end, from the first box's model (ASSUMED): power 24 and LAN 43 from the left long edge, case mid-height.
coax_x=32.5; coax_z=SB[2]-foot_h-19; pwr_x=24; eth_x=43; port_z=(SB[2]-foot_h)/2;

// TL-SG105 on the lid: 100 x 98 x 25 (retailer listings), ports on the front face, power jack on the rear (Brian's
// photo). Fence clearance as the downloaded bracket's sleeve (100.5 inside).
SW=[100,98,25]; sw_clr=0.25;

gap_b=22;   // ScreenBeam back end -> inner back wall: coupler rear + barrel (UNKNOWN lengths)
bay=60;     // inner front wall -> ScreenBeam front end: power plug (44.5 incl. tip) + LAN patch + front keystone
side=56;    // right of the ScreenBeam: two back Ethernet keystones side by side, two patches and the power cord
boss_h=6; shim_nom=2; plate=4; adj_y=5; adj_x=3;

IW=3+SB[0]+side+1;  ID=bay+SB[1]+gap_b;  IH=boss_h+shim_nom+plate+SB[2]-foot_h+6;
WO=IW+2*t; DO=ID+2*t; HO=IH+t;

sbx0=t+3; sbx1=sbx0+SB[0]; sby0=t+bay; sby1=sby0+SB[1];
plate_z=t+boss_h+shim_nom; case_z=plate_z+plate;
coax=[sbx0+coax_x, case_z+coax_z];          // back keystone, X and Z of the axis
ks_back=[sbx1+13, coax[1]];                 // ETH1: ScreenBeam LAN -> Google Wifi WAN
ks_back2=[sbx1+36, coax[1]];                // ETH2: Google Wifi LAN -> front keystone
ks_front=[sbx1+30, t+18];               // front Ethernet keystone
pwr_hole=[DO-t-45, t+12];                   // ScreenBeam power, right wall near the back (Y, Z), 10 mm
ears=[for(x=[sbx0+8,sbx1-8],y=[sby0-7,sby1+7])[x,y]];

module rrect(x0,x1,y0,y1,r){hull()for(x=[x0+r,x1-r],y=[y0+r,y1-r])translate([x,y])circle(r=r);}
module slot2d(ax,ay,d){hull()for(sx=[-ax,ax],sy=[-ay,ay])translate([sx,sy])circle(d=d);}
// wall frames as in body15.scad: u to the right seen from outside, y inward, v up
module on_front(x,z){multmatrix([[1,0,0,x],[0,1,0,0],[0,0,1,z],[0,0,0,1]])children();}
module on_back(x,z){multmatrix([[-1,0,0,x],[0,-1,0,DO],[0,0,1,z],[0,0,0,1]])children();}
module ks_hole(){translate([-10.5,-0.01,-15])cube([21,4.02,33.5]);}
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
  for(e=ears)translate([e[0],e[1],t+boss_h-6.5])cylinder(d=insert_pilot,h=7);
  for(p=lid_posts())translate([p[0],p[1],HO-7])cylinder(d=insert_pilot,h=7.1);
  on_back(coax[0],coax[1])ks_hole();
  on_back(ks_back[0],ks_back[1])ks_hole();
  on_back(ks_back2[0],ks_back2[1])ks_hole();
  on_front(ks_front[0],ks_front[1])ks_hole();
  translate([WO-t-1,pwr_hole[0],pwr_hole[1]])rotate([0,90,0])cylinder(d=10,h=t+2);
 }
 on_back(coax[0],coax[1])ks_gold_one(0,0);
 on_back(ks_back[0],ks_back[1])ks_gold_one(0,0);
 on_back(ks_back2[0],ks_back2[1])ks_gold_one(0,0);
 on_front(ks_front[0],ks_front[1])ks_gold_one(0,0);
}

// Lid: 2.5 plate, locating lip, four countersunk M3. Switch fence (4 tall, ports to the front, open there) at the
// front; vent slots behind the switch, over the back of the ScreenBeam.
swx0=(WO-SW[0])/2; swy0=6;
module lid(){
 difference(){
  union(){
   linear_extrude(t)rrect(0,WO,0,DO,cr);
   translate([0,0,-3])linear_extrude(3.01)difference(){rrect(t+0.3,WO-t-0.3,t+0.3,DO-t-0.3,cr-t);
    rrect(t+1.9,WO-t-1.9,t+1.9,DO-t-1.9,cr-t);
    for(p=lid_posts())translate(p)circle(d=11);
    translate([coax[0]-12,DO-t-6])square([24,8]);translate([ks_back[0]-12,DO-t-6])square([47,8]);}   // clear keystones
   translate([0,0,t-0.01])linear_extrude(4)difference(){
    translate([swx0-sw_clr-1.6,swy0-sw_clr])square([SW[0]+2*sw_clr+3.2,SW[1]+2*sw_clr+1.6]);
    translate([swx0-sw_clr,swy0-sw_clr-1])square([SW[0]+2*sw_clr,SW[1]+2*sw_clr+1]);
    translate([swx0+15,swy0])square([SW[0]-30,SW[1]+5]);   // corner fences only
    translate([swx0-5,swy0+15])square([SW[0]+10,SW[1]-30]);
   }
  }
  for(p=lid_posts())translate([p[0],p[1],-4]){cylinder(d=m3,h=10);translate([0,0,4+t-1.7])cylinder(d1=m3,d2=6.6,h=1.71);}
  for(y=[swy0+SW[1]+8:5.5:DO-14])translate([sbx0+8,y-1.25,-1])cube([SB[0]-16,2.5,t+2]);
 }
}

// Sled: as rx1 turned 90 deg. Ears slot +-5 front-back (onto the coupler) and +-3 across; height by shim rings.
module sled(){
 difference(){
  union(){
   translate([0,0,plate_z])linear_extrude(plate)union(){
    rrect(sbx0-sb_clr/2-2,sbx1+sb_clr/2+2,sby0+1,sby1-1,3);
    for(e=ears)translate(e)rrect(-7,7,-8,8,3);
    for(e=ears)hull(){translate(e)square([14,1],center=true);translate([e[0],e[1]<sby0+60?sby0+4:sby1-4])square([14,1],center=true);}
   }
   for(x=[sbx0-sb_clr/2-2,sbx1+sb_clr/2])translate([x,sby0+15,case_z-0.01])cube([2,SB[1]-30,6]);   // side lips
  }
  for(e=ears)translate([e[0],e[1],plate_z-1])linear_extrude(plate+2)slot2d(adj_x,adj_y,m3);
  for(f=sb_feet)translate([sbx0+f[0],sby0+f[1],case_z-foot_dp])cylinder(d=foot_d,h=foot_dp+0.1,$fn=48);
 }
}
module shims(){
 for(i=[0:3]){translate([i*13,0,0])difference(){cylinder(d=10,h=1);translate([0,0,-1])cylinder(d=m3,h=3);}
  translate([i*13,13,0])difference(){cylinder(d=10,h=2);translate([0,0,-1])cylinder(d=m3,h=4);}
  translate([i*17-7,26,0])difference(){linear_extrude(2)rrect(0,14,0,14,2);translate([7,7,-1])cylinder(d=m3,h=4);}}
}

module rod(a,b,d){hull(){translate(a)sphere(d=d,$fn=16);translate(b)sphere(d=d,$fn=16);}}
module devices(){
 color([0.12,0.12,0.13])translate([sbx0,sby0,case_z])cube([SB[0],SB[1],SB[2]-foot_h]);
 color([0.1,0.1,0.1])for(f=sb_feet)translate([sbx0+f[0],sby0+f[1],case_z-foot_h])cylinder(d=13,h=foot_h);
 color([0.85,0.7,0.3])translate([coax[0],DO+12,coax[1]])rotate([90,0,0]){cylinder(d=9.5,h=t+26);   // coupler (UNKNOWN)
  translate([0,0,t+24])cylinder(d=11,h=gap_b-14,$fn=6);}                                          // M-M barrel (UNKNOWN)
 pz=case_z+port_z;
 color("silver")translate([sbx0+pwr_x,sby0,pz])rotate([90,0,0])cylinder(d=7.75,h=35);             // ScreenBeam power
 color([0.15,0.15,0.15]){rod([sbx0+pwr_x,sby0-35,pz],[sbx0+pwr_x+6,sby0-44,pz],4);
  rod([sbx0+pwr_x+6,sby0-44,pz],[sbx1+8,sby0-44,t+12],4);rod([sbx1+8,sby0-44,t+12],[sbx1+8,pwr_hole[0],t+12],4);
  rod([sbx1+8,pwr_hole[0],t+12],[WO+15,pwr_hole[0],pwr_hole[1]],4);}
 color([0.2,0.4,0.9])translate([sbx0+eth_x-6.5,sby0-28,pz-6])cube([13,28,12]);                    // RJ45 at the ScreenBeam
 color([0.15,0.15,0.15]){                                                                          // inside patches
  rod([sbx0+eth_x,sby0-28,pz],[sbx1+8,sby0-20,t+14],6);rod([sbx1+8,sby0-20,t+14],[sbx1+8,DO-t-45,t+14],6);   // ScreenBeam LAN
  rod([sbx1+8,DO-t-45,t+14],[ks_back[0],DO-t-34,ks_back[1]],6);                                              //  -> ETH1
  rod([ks_back2[0],DO-t-34,ks_back2[1]],[WO-t-8,DO-t-50,t+30],6);rod([WO-t-8,DO-t-50,t+30],[WO-t-8,t+45,t+30],6);  // ETH2
  rod([WO-t-8,t+45,t+30],[ks_front[0],t+34,ks_front[1]],6);}                                                 //  -> front
 color([0.2,0.4,0.9]){translate([ks_front[0]-8,t+4,ks_front[1]-6])cube([16,30,12]);
  for(k=[ks_back,ks_back2])translate([k[0]-8,DO-t-34,k[1]-6])cube([16,30,12]);}
 color([0.95,0.95,0.95])for(k=[ks_back,ks_back2])rod([k[0],DO+4,k[1]],[k[0],DO+40,k[1]-15],5);     // to/from the Google Wifi
 // switch on the lid, ports to the front; 6 in patch from a port down to the front keystone
 color([0.2,0.35,0.6])translate([swx0,swy0,HO+t])cube(SW);
 color([0.05,0.05,0.05])for(i=[0:4])translate([swx0+8+i*17,swy0-0.2,HO+t+5])cube([14,1,12]);
 color([0.85,0.85,0.85])rod([swx0+8+4*17+7,swy0-12,HO+t+11],[ks_front[0],-14,ks_front[1]],5);
}

if(part=="body")body();
if(part=="lid")lid();
if(part=="lid_up")translate([0,0,HO+lid_lift])lid();
if(part=="sled")sled();
if(part=="shims")shims();
if(part=="devices")devices();
if(part=="all"){color([0.92,0.91,0.87])body();color([0.55,0.75,0.6])sled();devices();
 color([0.8,0.8,0.85,0.6])translate([0,0,HO])lid();
 echo(str("outer ",WO," x ",DO," x ",HO," (+ lid ",t,"); coax axis X",coax[0]," Z",coax[1]));}
