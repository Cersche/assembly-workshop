// Lab Rax generic equipment tray + faceplate (wizard template).
// Faceplate derived from the Pi4 baseline; rack holes follow the four-corner layout of the user-supplied
// 1U blank plate (faceplate_mounting.json): EVERY rack unit gets 4 holes, never a single centre pair.
// The wizard appends override assignments at the end of this file.
// PROPOSED, UNVALIDATED: printed fit, strength and rack clearance are UNKNOWN.
$fn=48;
part="assembly";            // assembly, faceplate, tray, combined, rear_bracket
// Device envelope (mm). Origin of hole coordinates = device front-left corner, seen from above.
dev_w=85; dev_d=56; dev_h=20;
holes=[];                   // [[x,y],...] mounting hole centres
hole_d=2.7;                 // device mounting hole diameter
device_mount="inserts";     // inserts, pegs, clips, straps
standoff=6;                 // device lift above tray floor
insert_pilot=3.2;           // pilot for heat-set insert (inserts mode)
board_t=1.6;                // board/flange thickness (pegs, clips)
joint="screw";              // screw, snap, single
u=1;                        // faceplate height in rack units
keystones=[];               // [x,...] keystone centres on faceplate (X=0 centre)
ks_w=14.5; ks_h=16;         // standard keystone opening
ports=[];                   // [[x,z,w,h,r],...] faceplate cut-outs, z from plate bottom, r=corner radius
front_gap=12;               // device front to faceplate rear face
margin=8;                   // tray border around device
rear_support=false;         // heavy/deep equipment: tray runs to the rear posts and screws to a rear bracket
coupon=[];                  // test coupon: [x0,x1,ymax] keeps only that slice of the part

// 4 mm plate (owner default 2026-10-18). Corner radius is limited by the four-corner holes:
// the reference holes sit 1.6 mm from the top/bottom edge, so larger corners would cut into them.
plate_w=252; plate_t=4; plate_r=2.5; plate_h=u*44.45-2.45;
hole_x=118.2625; hole_dz=15.902;   // each U: holes at its centre ±hole_dz (5.098 / 36.902 on a 1U plate)
rack_depth=240;             // Lab Rax frame depth (front of front posts to back of rear posts)
nudge=0;                    // render-repair only: tiny size offset applied when OpenSCAD 2021 emits a sliver
ks_front=2;                 // keystone clips need a thin wall: plate is pocketed from behind down to this
tray_t=3; tray_z=7;
tray_w=dev_w+2*margin; tray_d=rear_support?rack_depth:dev_d+front_gap+margin;
tray_x=-tray_w/2; tray_y=0;
dev_x=-dev_w/2; dev_y=front_gap; floor_top=tray_z+tray_t;
jx=min(40,tray_w/2-12); joint_x=[-jx,jx];
tongue_w=12; tongue_depth=7; tongue_h=3; tongue_z=tray_z+3.5;
slot_clear=0.3; boss_d=9; m3_clear=3.4; joint_pilot=4.0;  // 4.0 = the printed, well-fitting Pi4 trial

module capsule2d(len=10,diam=7){hull(){translate([-(len-diam)/2,0])circle(d=diam);translate([(len-diam)/2,0])circle(d=diam);}}
module rrect(w,h,r){rr=min(r,w/2-0.01,h/2-0.01);if(rr<=0)square([w,h],center=true);else offset(r=rr)square([w-2*rr,h-2*rr],center=true);}
// Mirror front-of-tray features to the rear (about the rack's mid-depth).
module to_rear(){translate([0,rack_depth/2,0])mirror([0,1,0])translate([0,-rack_depth/2,0])children();}

// Faceplate outline seen from the front: 2D X = rack X, 2D Y = height Z.
// rear=true cuts the larger keystone pocket; plain=true leaves out keystones/ports (rear bracket).
module plate2d(rear=false,plain=false){
 difference(){
  hull()for(sx=[-1,1],sz=[-1,1])translate([sx*(plate_w/2-plate_r),plate_h/2+sz*(plate_h/2-plate_r)])circle(r=plate_r+nudge);
  for(i=[0:u-1],dz=[-hole_dz,hole_dz],x=[-hole_x,hole_x])translate([x,i*44.45+21+dz])capsule2d();
  if(!plain){
   for(x=keystones)if(rear)translate([x,plate_h/2])square([ks_w+4+nudge,ks_h+6+nudge],center=true);
                   else translate([x,plate_h/2])square([ks_w,ks_h],center=true);
   for(p=ports)translate([p[0],p[1]])rrect(p[2],p[3],p[4]);
  }
 }
}
// Plate between y=y0 (front) and y0+t, built from the 2D outline (cleaner meshes than 3D cuts in OpenSCAD 2021).
module plate_layer(y0,t,rear=false,plain=false){translate([0,y0+t,0])rotate([90,0,0])linear_extrude(height=t)plate2d(rear,plain);}

module plate_joint_add(){
 if(joint=="screw"){
  for(x=joint_x)translate([x-tongue_w/2,0,tongue_z])cube([tongue_w,tongue_depth,tongue_h]);
  for(x=joint_x)translate([x,0,tray_z+14])rotate([-90,0,0])cylinder(d=boss_d,h=8);
 }
 if(joint=="snap") for(x=joint_x){
  // Cantilever arm under the tray floor; barb snaps up into a floor window.
  translate([x-4,0,tray_z-2])cube([8,16,2]);
  translate([x-4,12,tray_z])hull(){cube([8,4,0.01]);translate([0,3.4,0])cube([8,0.6,1.2]);}
 }
}
module plate_joint_cut(){if(joint=="screw")for(x=joint_x)translate([x,-0.1,tray_z+14])rotate([-90,0,0])cylinder(d=joint_pilot,h=8.2);}

module faceplate(){
 difference(){
  union(){
   // Front layer keeps the keystone opening; with keystones, the rear layer is pocketed so jacks grip ks_front.
   if(len(keystones)>0&&plate_t>ks_front){plate_layer(-plate_t,ks_front);plate_layer(-plate_t+ks_front,plate_t-ks_front,true);}
   else plate_layer(-plate_t,plate_t);
   plate_joint_add();
  }
  plate_joint_cut();
 }
}
// Plain plate on the rear posts (mirror of the faceplate, no openings) that the tray's rear end screws/snaps to.
module rear_bracket(){to_rear()difference(){union(){plate_layer(-plate_t,plate_t,false,true);plate_joint_add();}plate_joint_cut();}}

module device_features_add(){
 if(device_mount=="inserts")for(h=holes)translate([dev_x+h[0],dev_y+h[1],floor_top])cylinder(d=max(insert_pilot+3.5,7),h=standoff);
 if(device_mount=="pegs")for(h=holes)translate([dev_x+h[0],dev_y+h[1],floor_top]){
  cylinder(d=hole_d+3,h=standoff);
  translate([0,0,standoff])cylinder(d=hole_d-0.3,h=board_t+0.8);
  translate([0,0,standoff+board_t+0.8])cylinder(d1=hole_d-0.3,d2=hole_d-1,h=0.8);
 }
 if(device_mount=="clips"){
  // Support ledges at the four corners plus a flexing clip on each side.
  for(x=[dev_x-1,dev_x+dev_w-5],y=[dev_y-1,dev_y+dev_d-5])translate([x,y,floor_top])cube([6,6,standoff]);
  for(s=[-1,1])translate([s>0?dev_x+dev_w+0.2:dev_x-2.2,dev_y+dev_d/2-5,floor_top]){
   cube([2,10,standoff+board_t+2.5]);
   translate([s>0?-1.2:2,0,standoff+board_t+0.2])hull(){cube([1.2,10,1.6]);translate([s>0?1.2:0,0,1.6])cube([0.01,10,0.6]);}
  }
 }
}
module device_features_cut(){
 if(device_mount=="inserts")for(h=holes)translate([dev_x+h[0],dev_y+h[1],floor_top+0.01])cylinder(d=insert_pilot,h=standoff+0.1);
 if(device_mount=="straps")for(x=[dev_x-5.5,dev_x+dev_w+2.5],y=[dev_y+dev_d*0.25,dev_y+dev_d*0.75])
  translate([x,y-6,tray_z-0.1])cube([3,12,tray_t+0.2]);
}

module tray_joint_add(){
 if(joint=="screw"){
  for(x=joint_x) translate([x-9,0,tray_z+tray_t])cube([18,8,5]);
  for(x=joint_x)translate([x-7,8.3,tray_z+3])cube([14,3,19]);
  for(x=joint_x) for(side=[-1,1]) translate([x+side*6-1,0,0])
    hull(){translate([0,9,tray_z+2.7])cube([2,2,0.5]);
           translate([0,9,tray_z+8])cube([2,2,0.5]);
           translate([0,20,tray_z+2.7])cube([2,2,0.5]);}
 }
}
module tray_joint_cut(){
 if(joint=="screw"){
  for(x=joint_x)translate([x-(tongue_w+slot_clear)/2,-0.1,tongue_z-slot_clear/2])cube([tongue_w+slot_clear,tongue_depth+slot_clear,tongue_h+slot_clear]);
  for(x=joint_x)translate([x,11.4,tray_z+14])rotate([90,0,0])cylinder(d=m3_clear,h=12);
 }
 if(joint=="snap")for(x=joint_x)translate([x-4.3,14.8,tray_z-0.1])cube([8.6,1.6,tray_t+0.2]);
}

module tray(){
 difference(){
  union(){
   translate([tray_x,tray_y,tray_z])cube([tray_w,tray_d,tray_t]);
   tray_joint_add();
   if(rear_support)to_rear()tray_joint_add();
   device_features_add();
  }
  tray_joint_cut();
  if(rear_support)to_rear()tray_joint_cut();
  device_features_cut();
 }
}

module clip_coupon(){if(len(coupon)==3)intersection(){children();translate([coupon[0],-50,-50])cube([coupon[1]-coupon[0],coupon[2]+50,400]);}else children();}

clip_coupon(){
 if(part=="faceplate")faceplate();
 else if(part=="tray")tray();
 else if(part=="rear_bracket")rear_bracket();
 else if(part=="combined")union(){faceplate();translate([tray_x,-0.01,tray_z])cube([tray_w,0.02+0.01,tray_t]);tray();if(rear_support)rear_bracket();}
 else {color("steelblue")faceplate();color("silver")tray();if(rear_support)color("steelblue")rear_bracket();
  %translate([dev_x,dev_y,floor_top+(device_mount=="inserts"||device_mount=="pegs"||device_mount=="clips"?standoff:0)])cube([dev_w,dev_d,dev_h]);}
}

// ---- wizard overrides: 1_Keystone_and_corner_holes
dev_w=85.0;
dev_d=56.0;
dev_h=20.0;
hole_d=2.7;
standoff=6.0;
insert_pilot=3.2;
board_t=1.6;
u=1;
holes=[[3.5, 3.5], [61.5, 3.5], [3.5, 52.5], [61.5, 52.5]];
keystones=[100.0];
device_mount="inserts";
joint="screw";
rear_support=false;
coupon=[78.0, 127.0, 5.0];
ports=[];
