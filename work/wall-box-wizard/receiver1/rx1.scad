// MoCA receiver box, concept 1 (Brian, 2026-10-31). Shelf box, lid on top. Second ScreenBeam ECB7250 lies flat on an
// adjustable sled; its Coax In is coupled straight to an F keystone coupler in the left wall by an F male-male barrel
// (no jumper). EchoGear 5-port gigabit switch in front of it; ScreenBeam Ethernet -> switch, switch -> front-wall
// Ethernet keystone. Both power cords leave through the back wall in the right-hand plug bay.
// PROPOSED - UNVALIDATED, concept only, not printed: switch size/ports, ScreenBeam port positions, coupler and barrel
// lengths, fit and strength are UNKNOWN. Lessons from the first box (concept15) are carried over: foot pockets, 0.5
// extra ScreenBeam clearance, room for the 44.5 mm power plug, straight vent slots, golden keystone, M3 heat-set inserts.
//
// Coordinates: outer box X 0..WO (left -> right), Y 0..DO (front -> back), Z 0..HO (floor -> top rim). Lid sits on top.
// part: "body" | "lid" | "sled" | "shims" | "devices" (context models, never printed) | "all" (assembled, lid lifted)
part="all";
lid_lift=40;   // "all" only: lid raised so the inside shows

use <../concept15/body15.scad>   // ks_gold_one(): golden keystone, ks_tight 0.2

$fn=40;
t=2.5; cr=6;                          // wall, vertical corner radius
insert_pilot=4.0; m3=3.4;

// ScreenBeam ECB7250 (Brian: 120 x 65 x 30 incl. rubber feet). Feet 13 dia, 2.25 proud, centres 8 in from the long
// edges and 16 in from the short ends; they drop into 16 x 2.6 pockets so the case sits on the sled.
SB=[120,65,30]; foot_h=2.25; sb_clr=0.5;
sb_feet=[for(x=[16,104],y=[8.5,56.5])[x,y]]; foot_d=16; foot_dp=2.6;
// Port positions. Coax In (Brian, 2026-10-31): centre 19 mm from the face it lies on when label side up; read as the
// label on the feet side, so 19 below the vent face (case 27.75 without feet). Across the end: centred, ASSUMED.
// Right end, from the first box's model (ASSUMED): power 24 and Ethernet 43 from the front long edge, mid-height.
coax_y=32.5; pwr_y=24; eth_y=43; coax_z=SB[2]-foot_h-19; port_z=(SB[2]-foot_h)/2;

// TP-Link TL-SG105 (Brian, 2026-10-31; replaces the EchoGear): 100 x 98 x 25 (retailer listings). Port face (LEDs are
// in the ports) out through the front wall, like Brian's downloaded "Switch Mount v2" rack bracket. Its fit is copied,
// not its mesh: sleeve 100.5 x 25.5 inside, 2 mm walls, 60 deep. Our window is 1.5 smaller all round so the switch
// stops against it, sliding in from the inside. Power jack position UNKNOWN.
SW=[100,98,25]; sl_in=[100.5,25.5]; sl_w=2; sl_d=60; win_lip=1.5;
// Power jack on the rear face (Brian's photo, 2026-10-31): scaled from the photo, ~21 from the switch's left side seen
// from the front, ~13.6 up. Straight plug assumed like the ScreenBeam's (35 out + bend): sw_plug of free space behind,
// cord turns left and leaves through a 10 mm hole in the left wall. A right-angle plug would let this shrink ~25.
sw_jack=[21,13.6]; sw_plug=45;

gap_l=22;      // inner left wall -> ScreenBeam left end: keystone coupler rear + male-male barrel (lengths UNKNOWN)
bay=60;        // ScreenBeam right end -> inner right wall: plugs (power 44.5 incl. tip) and the LAN patch to the keystone
boss_h=6; shim_nom=2; plate=4;
adj_x=5; adj_y=3;   // sled slot travel each way; height by shims (0..5 mm, nominal 2)

IW=gap_l+SB[0]+bay;
sw_y0=0; sb_y0=SW[1]+sw_plug;      // switch at the front wall, its plug space, then the ScreenBeam
ID=sb_y0+SB[1]+3;
IH=boss_h+shim_nom+plate+SB[2]-foot_h+6;
WO=IW+2*t; DO=ID+2*t; HO=IH+t;

// key positions (outer coordinates)
sbx0=t+gap_l; sbx1=sbx0+SB[0]; sby0=t+sb_y0;
plate_z=t+boss_h+shim_nom;           // sled plate bottom
case_z=plate_z+plate;                 // ScreenBeam case bottom (feet in pockets)
coax=[t, sby0+coax_y, case_z+coax_z]; // coax axis on the inner left wall face
swx0=t+38; swx1=swx0+SW[0]; swy0=t+sw_y0; swz0=t+sl_w;   // switch box (front face on the inner front wall)
slx0=swx0-(sl_in[0]-SW[0])/2;     // sleeve inside, X from
ks_lan=[t+IW-20, t+18];               // front keystone: X centre, Z of jack axis
pwr_holes=[[t+IW-30,t+16]];         // ScreenBeam power, back wall, 10 mm (barrel plug passes through)
sw_hole=[t+SW[1]+sw_plug/2+3, t+10]; // switch power, left wall (Y, Z)
ears=[for(x=[sbx0-7,sbx1+7],y=[sby0+8,sby0+SB[1]-8])[x,y]];

module rrect(x0,x1,y0,y1,r){hull()for(x=[x0+r,x1-r],y=[y0+r,y1-r])translate([x,y])circle(r=r);}
module slot2d(ax,ay,d){hull()for(sx=[-ax,ax],sy=[-ay,ay])translate([sx,sy])circle(d=d);}

// wall frames as in body15.scad: u to the right seen from outside, y inward, v up
module on_left(y,z){multmatrix([[0,1,0,0],[-1,0,0,y],[0,0,1,z],[0,0,0,1]])children();}
module on_front(x,z){multmatrix([[1,0,0,x],[0,1,0,0],[0,0,1,z],[0,0,0,1]])children();}
module ks_hole(){translate([-10.5,-0.01,-15])cube([21,4.02,33.5]);}

module body(){
 difference(){
  union(){
   difference(){
    linear_extrude(HO)rrect(0,WO,0,DO,cr);
    translate([0,0,t])linear_extrude(HO)rrect(t,WO-t,t,DO-t,cr-t);
   }
   for(e=ears)translate([e[0],e[1],t-0.01])cylinder(d=10,h=boss_h+0.01);         // sled bosses
   for(p=lid_posts())translate([p[0],p[1],0])cylinder(d=9,h=HO);                   // lid screw posts
  }
  for(e=ears)translate([e[0],e[1],t+boss_h-6.5])cylinder(d=insert_pilot,h=7);
  for(p=lid_posts())translate([p[0],p[1],HO-7])cylinder(d=insert_pilot,h=7.1);
  on_left(coax[1],coax[2])ks_hole();
  on_front(ks_lan[0],ks_lan[1])ks_hole();
  sw_window();
  for(p=pwr_holes)translate([p[0],DO+1,p[1]])rotate([90,0,0])cylinder(d=10,h=t+2);
  translate([-1,sw_hole[0],sw_hole[1]])rotate([0,90,0])cylinder(d=10,h=t+2);   // switch power cord, left wall
 }
 on_left(coax[1],coax[2])ks_gold_one(0,0);
 on_front(ks_lan[0],ks_lan[1])ks_gold_one(0,0);
 sw_sleeve();
}
function lid_posts()=[[t+3.5,t+3.5],[WO-t-3.5,t+3.5],[t+3.5,DO-t-3.5],[WO-t-3.5,DO-t-3.5]];

// switch sleeve on the front wall (fit from the downloaded bracket) and its window, 1.5 mm stop lip all round
slz0=swz0-(sl_in[1]-SW[2])/2;
module sw_sleeve(){difference(){
 translate([slx0-sl_w,t-0.01,t-0.01])cube([sl_in[0]+2*sl_w,sl_d+0.01,slz0-t+sl_in[1]+sl_w+0.01]);
 translate([slx0,t-1,slz0])cube([sl_in[0],sl_d+2,sl_in[1]]);
}}
module sw_window(){translate([slx0+win_lip,-1,slz0+win_lip])cube([sl_in[0]-2*win_lip,t+2,sl_in[1]-2*win_lip]);}

// Lid: flat 2.5 plate with a locating lip, four countersunk M3 into the post inserts, vent slots over both devices
module lid(){
 difference(){
  union(){
   linear_extrude(t)rrect(0,WO,0,DO,cr);
   translate([0,0,-3])linear_extrude(3.01)difference(){rrect(t+0.3,WO-t-0.3,t+0.3,DO-t-0.3,cr-t);
    rrect(t+1.9,WO-t-1.9,t+1.9,DO-t-1.9,cr-t);
    for(p=lid_posts())translate(p)circle(d=11);
    translate([-1,coax[1]-12])square([t+6,24]);}   // clear the coax keystone block
  }
  for(p=lid_posts())translate([p[0],p[1],-4]){cylinder(d=m3,h=10);translate([0,0,4+t-1.7])cylinder(d1=m3,d2=6.6,h=1.71);}
  for(x=[sbx0+12:5.5:sbx1-12])translate([x-1.25,sby0+10,-1])cube([2.5,SB[1]-20,t+2]);
  for(x=[swx0+8:5.5:swx1-8])translate([x-1.25,swy0+sl_d+4,-1])cube([2.5,SW[1]-sl_d-10,t+2]);
 }
}

// Sled: plate under the ScreenBeam with foot pockets, side lips, four ears with slots (X +-5, Y +-3) over the floor
// bosses. Fender or printed washers under the M3 heads. Height: shim rings under the ears.
module sled(){
 difference(){
  union(){
   translate([0,0,plate_z])linear_extrude(plate)union(){
    rrect(sbx0+1,sbx1-1,sby0-sb_clr/2-2,sby0+SB[1]+sb_clr/2+2,3);
    for(e=ears)translate(e)rrect(-8,8,-7,7,3);
    for(e=ears)hull(){translate(e)square([1,14],center=true);translate([e[0]<sbx0+60?sbx0+4:sbx1-4,e[1]])square([1,14],center=true);}
   }
   for(y=[sby0-sb_clr/2-2,sby0+SB[1]+sb_clr/2])translate([sbx0+15,y,case_z-0.01])cube([SB[0]-30,2,6]);   // side lips
  }
  for(e=ears)translate([e[0],e[1],plate_z-1])linear_extrude(plate+2)slot2d(adj_x,adj_y,m3);
  for(f=sb_feet)translate([sbx0+f[0],sby0+f[1],case_z-foot_dp])cylinder(d=foot_d,h=foot_dp+0.1,$fn=48);
 }
}
// shim rings (10 OD): 4 x 1 mm and 4 x 2 mm, plus 4 washers 14 x 14 x 2 for the slots; laid out for printing
module shims(){
 for(i=[0:3]){translate([i*13,0,0])difference(){cylinder(d=10,h=1);translate([0,0,-1])cylinder(d=m3,h=3);}
  translate([i*13,13,0])difference(){cylinder(d=10,h=2);translate([0,0,-1])cylinder(d=m3,h=4);}
  translate([i*17-7,26,0])difference(){translate([0,0,0])linear_extrude(2)rrect(0,14,0,14,2);translate([7,7,-1])cylinder(d=m3,h=4);}}
}

// context models (not printed)
module rod(a,b,d){hull(){translate(a)sphere(d=d,$fn=16);translate(b)sphere(d=d,$fn=16);}}
module devices(){
 color([0.12,0.12,0.13])translate([sbx0,sby0,case_z])cube([SB[0],SB[1],SB[2]-foot_h]);       // ScreenBeam
 color([0.1,0.1,0.1])for(f=sb_feet)translate([sbx0+f[0],sby0+f[1],case_z-foot_h])cylinder(d=13,h=foot_h);
 color([0.85,0.7,0.3])rotate([0,90,0])translate([-coax[2],coax[1],0]){                       // coax chain on the axis
  translate([0,0,-12])cylinder(d=9.5,h=t+26);           // keystone F coupler, ~12 behind the wall face (UNKNOWN)
  translate([0,0,t+12])cylinder(d=11,h=gap_l-14,$fn=6); // F male-male barrel (UNKNOWN length)
 }
 color("silver")translate([sbx1,sby0+pwr_y,case_z+port_z])rotate([0,90,0])cylinder(d=7.75,h=35);  // power plug
 color([0.15,0.15,0.15])rod([sbx1+35,sby0+pwr_y,case_z+port_z],[sbx1+45,DO-t-6,case_z+port_z],4);
 rod([sbx1+45,DO-t-6,case_z+port_z],[pwr_holes[0][0],DO+15,pwr_holes[0][1]],4);
 color([0.2,0.4,0.9])translate([sbx1,sby0+eth_y-6.5,case_z+port_z-6])cube([28,13,12]);               // RJ45 plug
 color([0.2,0.35,0.6])translate([swx0,swy0,swz0])cube([SW[0],SW[1],SW[2]]);                           // TL-SG105
 color([0.05,0.05,0.05])for(i=[0:4])translate([swx0+8+i*17,swy0-0.2,swz0+5])cube([14,1,12]);           // ports (positions ASSUMED)
 jk=[swx0+sw_jack[0],swy0+SW[1],swz0+sw_jack[1]];                                                   // switch power plug
 color("silver")translate(jk)rotate([-90,0,0])cylinder(d=7.75,h=35);
 color([0.15,0.15,0.15]){rod(jk+[0,35,0],[jk[0]-15,sw_hole[0],sw_hole[1]],4);rod([jk[0]-15,sw_hole[0],sw_hole[1]],[-15,sw_hole[0],sw_hole[1]],4);}
 // ScreenBeam LAN: right-angle out of the right end, along the bay to the back of the front keystone
 color([0.15,0.15,0.15])rod([sbx1+28,sby0+eth_y,case_z+port_z],[ks_lan[0],sby0-10,ks_lan[1]],6);
 rod([ks_lan[0],sby0-10,ks_lan[1]],[ks_lan[0],t+34,ks_lan[1]],6);
 color([0.2,0.4,0.9])translate([ks_lan[0]-8,t+4,ks_lan[1]-6])cube([16,30,12]);                        // patch plug in the LAN keystone
}

if(part=="body")body();
if(part=="lid")lid();
if(part=="lid_up")translate([0,0,HO+lid_lift])lid();   // viewer only
if(part=="sled")sled();
if(part=="shims")shims();
if(part=="devices")devices();
if(part=="all"){color([0.92,0.91,0.87])body();color([0.55,0.75,0.6])sled();devices();
 color([0.8,0.8,0.85,0.6])translate([0,0,HO+lid_lift])lid();
 echo(str("outer ",WO," x ",DO," x ",HO," (+ lid ",t,"); coax axis Y",coax[1]," Z",coax[2]));}
