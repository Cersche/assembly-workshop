// Lab Rax generic equipment tray + faceplate (wizard template).
// Faceplate derived from the Pi4 baseline; rack holes follow the four-corner layout of the user-supplied
// 1U blank plate (faceplate_mounting.json): EVERY rack unit gets 4 holes, never a single centre pair.
// The wizard appends override assignments at the end of this file.
// PROPOSED, UNVALIDATED: printed fit, strength and rack clearance are UNKNOWN.
$fn=48;
part="assembly";            // assembly, faceplate, tray, combined, rear_bracket
// Device envelope (mm). Origin of hole coordinates = device front-left corner, seen from above.
dev_w=85; dev_d=56; dev_h=20;
feet=[];                     // [[x,y,w,d,h],...] underside feet, device frame front-left origin
holes=[];                   // [[x,y],...] mounting hole centres
hole_d=2.7;                 // device mounting hole diameter
device_mount="inserts";     // inserts, pegs, clips, straps
standoff=6;                 // device lift above tray floor
insert_pilot=3.2;           // pilot for heat-set insert (inserts mode)
board_t=1.6;                // board/flange thickness (pegs, clips)
joint="screw";              // screw, single ("snap" retired 2026-10-19: too brittle; kept as history)
u=1;                        // faceplate height in rack units
keystones=[];               // [x,...] keystone centres on faceplate (X=0 centre)
// Keystone v2 (2026-10-19, now the fallback; see ks_style): re-modelled from measurements of Brian's reference keystone frame
// (14.5 x 16 opening was too narrow when printed). Opening 14.8 x 16.6 through the plate, plus a rear collar
// 19.8 x 27.85 reaching 9.2 mm behind the front face (bottom lip to 10.4) that carries the latch ramp and catches.
ks_w=14.8; ks_h=16.6;       // front opening
ks_ow=19.8; ks_ob=11.9; ks_ot=15.95; ks_od=9.2; ks_lip=10.4;  // collar width, below/above opening centre, depth
ports=[];                   // [[x,z,w,h,r],...] faceplate cut-outs, z from slot bottom, r=corner radius
front_gap=12;               // device front to faceplate rear face
margin=8;                   // tray border around device
dev_off_x=0;                // device left/right offset, mm from centred (+ = right, seen from the front)
dev_off_y=0;                // device front/back offset, mm added to front_gap (+ = toward the rear)
dev_rot=0;                  // device rotation seen from above: 0, 90, 180, 270 (90/270 swap width and depth)
rear_support=false;         // heavy/deep equipment: tray runs to the rear posts and screws to a rear bracket
coupon=[];                  // test coupon: [x0,x1,ymax] keeps only that slice of the part

// 4 mm plate (owner default 2026-10-18). Corner radius is limited by the four-corner holes:
// the reference holes sit 1.6 mm from the top/bottom edge, so larger corners would cut into them.
rack_pitch=44.45; plate_gap=0.05; legacy_slot_offset=1.225;
plate_bottom=plate_gap/2; plate_center=u*rack_pitch/2;
plate_w=252; plate_t=4; plate_r=2.5; plate_h=u*rack_pitch-plate_gap;
hole_x=118.2625; hole_dz=15.902;   // each U: holes at its centre ±hole_dz (6.323 / 38.127 above the slot bottom)
rack_depth=240;             // Lab Rax frame depth (front of front posts to back of rear posts)
nudge=0;                    // render-repair only: tiny size offset applied when OpenSCAD 2021 emits a sliver
sleeve=device_mount=="sleeve";
// PROPOSED sleeve defaults (mm); independent design, fit and strength UNKNOWN.
sl_side=0.5; sl_top=0.3; sl_wall=6; sl_lip_w=10; sl_lip_t=1.5; sl_band=1.5; sl_stop_t=4; sl_stop_h=6;
foot_clearance=0.5; foot_extra_depth=0.3; foot_min_floor=0.8; foot_lip_t=3.0;
tray_t=3; floor_z=(device_mount=="flat"||sleeve)?0.5:7+legacy_slot_offset; tray_z=floor_z; // @flat-floor
assert(dev_rot==0||dev_rot==90||dev_rot==180||dev_rot==270,"dev_rot must be 0, 90, 180 or 270");
// Device footprint on the tray after rotation; the tray stays centred and grows to keep the margin.
fp_w=(dev_rot==90||dev_rot==270)?dev_d:dev_w; fp_d=(dev_rot==90||dev_rot==270)?dev_w:dev_d;
rack_inner_w=208; side_clear=2; max_tray=rack_inner_w-2*side_clear; // PROPOSED nominal opening / side clearance
tray_w=2*(abs(dev_off_x)+fp_w/2+(sleeve?max(margin,sl_side+sl_wall):margin)); tray_d=rear_support?rack_depth:sleeve?-plate_t+fp_d+margin:dev_off_y+fp_d+front_gap+margin;
tray_x=-tray_w/2; tray_y=0;
 // @flat-begin
assert(device_mount!="flat"||front_gap+dev_off_y>=6.2,"Flat corner stops need a front gap of at least 6.2 mm");
assert(device_mount!="flat"||joint!="screw"||front_gap+dev_off_y>=11.5,"Flat device must clear the front screw joint (front gap >= 11.5 mm)");
assert(device_mount!="flat"||!rear_support||front_gap+dev_off_y+fp_d<=rack_depth-11.5,"Flat device must clear the rear screw joint (rear gap >= 11.5 mm)");
 // @flat-end
dev_x=-fp_w/2+dev_off_x; dev_y=sleeve?-plate_t:front_gap+dev_off_y; floor_top=tray_z+tray_t;
assert(tray_w<=max_tray,str("This tray is ",tray_w," mm wide but the rack opening allows ",max_tray," mm (",rack_inner_w," mm minus ",side_clear," mm each side). Try Rotate 90 degrees, or reduce dev_off_x."));
assert(sleeve||dev_y>=0,str("Device moved into the faceplate: dev_off_y must be at least ",-front_gap));
assert(!rear_support||dev_y+fp_d+margin<=rack_depth,"Device moved past the rear posts; reduce dev_off_y");
// Device-frame point [x,y] (front-left origin, unrotated) -> footprint offset from [dev_x,dev_y].
function dp(p)=dev_rot==90?[dev_d-p[1],p[0]]:dev_rot==180?[dev_w-p[0],dev_d-p[1]]:dev_rot==270?[p[1],dev_w-p[0]]:p;
foot_h=(device_mount=="flat"||sleeve)?max([0,for(f=feet)f[4]]):0; foot_depth=foot_h>0?foot_h+foot_extra_depth:0;
sl_half=fp_w/2+sl_side; sl_bottom=floor_top; sl_window_top=sl_bottom+dev_h-foot_h+sl_top;  // case rests on the floor top; feet hang in pockets foot_extra_depth deeper
sl_lip=sl_window_top+(foot_h>0?foot_lip_t:sl_lip_t)<=u*rack_pitch?(foot_h>0?foot_lip_t:sl_lip_t):0;
sl_rear=dev_y+fp_d;
sl_joints=[dev_off_x-sl_half-sl_wall/2,dev_off_x+sl_half+sl_wall/2];
sl_joint_z=[sl_bottom+3,sl_window_top-3];
assert(!sleeve||fp_d/4-plate_t-6>=8,"Sleeve depth must be at least 72 mm to keep strap slots clear of the front joint");
assert(!sleeve||sl_bottom-plate_bottom>=sl_band&&u*rack_pitch-plate_bottom-sl_window_top>=sl_band,str("Too tall for a flush window in ",u,"U; choose ",u+1,"U"));
assert(!sleeve||!rear_support||sl_rear+sl_stop_t<=rack_depth-11.5,"Sleeve rear stop must clear rear joint by 11.5 mm");
assert(!sleeve||joint!="screw"||sl_window_top-sl_bottom>=10,"Sleeve screw joint needs a window at least 10 mm tall");
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
  hull()for(sx=[-1,1],sz=[-1,1])translate([sx*(plate_w/2-plate_r),plate_center+sz*(plate_h/2-plate_r)])circle(r=plate_r+nudge);
  for(i=[0:u-1],dz=[-hole_dz,hole_dz],x=[-hole_x,hole_x])translate([x,i*rack_pitch+rack_pitch/2+dz])capsule2d();
  if(!plain){
   if(sleeve)translate([dev_off_x,(sl_bottom+sl_window_top)/2])square([2*sl_half,sl_window_top-sl_bottom],center=true);
   for(p=ports)translate([p[0],p[1]])rrect(p[2],p[3],p[4]);
  }
 }
}
// Plate between y=y0 (front) and y0+t, built from the 2D outline (cleaner meshes than 3D cuts in OpenSCAD 2021).
module plate_layer(y0,t,rear=false,plain=false){translate([0,y0+t,0])rotate([90,0,0])linear_extrude(height=t)plate2d(rear,plain);}

module plate_joint_add(rear=false){
 if(joint=="screw"&&(!sleeve||rear)){
  for(x=joint_x)translate([x-tongue_w/2,0,tongue_z])cube([tongue_w,tongue_depth,tongue_h]);
  for(x=joint_x)translate([x,0,tray_z+14])rotate([-90,0,0])cylinder(d=boss_d,h=8);
 }
 if(joint=="snap") for(x=joint_x){
  // Cantilever arm under the tray floor; barb snaps up into a floor window.
  translate([x-4,0,tray_z-2])cube([8,16,2]);
  // Barb v2: square catch face toward the plate, ramp falling toward the rear so the tray, slid in
  // from the rear, cams the arm down until its window drops over the barb.
  translate([x-4,12,tray_z])hull(){cube([8,0.6,1.2]);cube([8,2.4,0.01]);}
 }
}
// Keystone collar behind the plate, and the jack-shaped cut through plate + collar.
// Profile in (d = depth behind front face, z from opening centre); X width is ks_w throughout.
module ks_collar(){for(x=keystones)translate([x-ks_ow/2,-plate_t,plate_center]){
 translate([0,0,-ks_ob])cube([ks_ow,ks_od,ks_ob+ks_ot]);
 translate([0,0,-ks_ob])cube([ks_ow,ks_lip,ks_ob-ks_h/2]);
}}
module ks_cut(){for(x=keystones)translate([x-ks_w/2,-plate_t,plate_center])rotate([90,0,90])linear_extrude(height=ks_w)
 polygon([[-1,-ks_h/2],[5.8,-ks_h/2],[5.8,-9.9],[9.2,-9.9],[9.2,-ks_h/2],[11,-ks_h/2],[11,11.6],[8.2,11.6],
          [8.2,ks_ot+1],[7.2,ks_ot+1],[7.2,13.6],[0.6,ks_h/2],[-1,ks_h/2]]);}
// Golden keystone (Brian, 2026-10-19): exact cross-sections of the keystone on Brian's SG108 faceplate, which fits
// perfectly in practice. Source: "10 inch shelf TP-Link SG108 Plus Keystone" by Goul (MakerWorld remix, BY-NC-SA),
// local/personal use only, never redistributed. Each band: [X from opening centre, width, polygons in source (Y, Z)]
// with source Y running down the plate (opening centre Y=25.09) and Z = depth (keystone face 0, plate back 4.08).
// The block replaces the plate within 21 x 33.5 mm around each keystone; front face sits 0.08 proud like the source.
ks_style="golden";          // golden (SG108 copy) or v2 (own measured rebuild, kept as fallback)
// Brian, 2026-10-19: the golden v3 print fit left/right well but had ~0.4 mm play up/down. ks_tight moves the
// bottom (hook-side) edge of the opening, its hook groove and lip up by this much; the latch side is unchanged.
ks_tight=0.2;  // Brian, 2026-10-19: v5 coupon (0.2) printed a perfect fit; v4 (0.4) was too tight.
KS_GOLD=[
  [-10.50,0.60,[[[45.500,4.080],[45.500,0.080],[38.691,0.080],[38.691,0.000],[7.251,0.000],[7.251,0.080],[1.000,0.080],[1.000,4.080],[1.071,4.080]]]],
  [-9.90,0.98,[[[9.143,4.080],[9.143,6.600],[9.205,7.147],[9.207,7.160],[9.226,7.216],[9.395,7.692],[9.679,8.145],[9.697,8.169],[10.075,8.546],[10.099,8.565],[10.551,8.848],[11.083,9.036],[11.643,9.100],[13.493,9.100],[14.293,9.900],[33.393,9.900],[33.893,10.400],[34.493,10.400],[35.054,10.336],[35.586,10.148],[36.038,9.865],[36.062,9.846],[36.439,9.469],[36.458,9.445],[36.742,8.992],[36.753,8.965],[36.930,8.460],[36.993,7.900],[36.993,4.080],[45.500,4.080],[45.500,0.080],[38.691,0.080],[38.691,0.000],[7.251,0.000],[7.251,0.080],[1.000,0.080],[1.000,4.080],[1.014,4.080]]]],
  [-8.92,1.52,[[[7.551,4.080],[7.551,2.250],[9.143,2.250],[9.143,6.600],[9.209,7.169],[9.367,7.620],[9.404,7.709],[9.658,8.114],[9.716,8.190],[9.755,8.229],[10.054,8.527],[10.130,8.586],[10.534,8.840],[10.623,8.876],[11.074,9.034],[11.643,9.100],[13.493,9.100],[14.293,9.900],[33.393,9.900],[33.893,10.400],[34.493,10.400],[35.063,10.334],[35.514,10.176],[35.603,10.140],[36.006,9.886],[36.083,9.827],[36.420,9.490],[36.479,9.414],[36.719,9.030],[36.737,9.000],[36.770,8.920],[36.927,8.469],[36.993,7.900],[36.993,2.250],[38.551,2.250],[38.551,4.080],[45.500,4.080],[45.500,0.080],[38.691,0.080],[38.691,0.000],[7.251,0.000],[7.251,0.080],[1.000,0.080],[1.000,4.080],[1.044,4.080]]]],
  [-7.40,14.80,[[[7.551,4.080],[7.551,2.250],[9.143,2.250],[9.143,6.600],[9.175,6.878],[9.229,7.247],[9.478,7.850],[9.876,8.368],[10.393,8.765],[10.996,9.015],[11.365,9.069],[11.643,9.100],[13.493,9.100],[13.493,8.100],[11.493,8.100],[11.493,7.200],[16.793,0.500],[16.793,0.000],[7.251,0.000],[7.251,0.080],[1.000,0.080],[1.000,4.080],[1.025,4.080]],[[45.500,4.080],[45.500,0.080],[38.691,0.080],[38.691,0.000],[33.393,0.000],[33.393,5.800],[34.993,5.800],[34.993,8.400],[33.393,8.400],[33.393,9.900],[33.893,10.400],[34.493,10.400],[34.771,10.369],[35.140,10.315],[35.743,10.065],[36.200,9.715],[36.261,9.668],[36.658,9.150],[36.908,8.547],[36.962,8.178],[36.993,7.900],[36.993,2.250],[38.551,2.250],[38.551,4.080],[42.555,4.080]]]],
  [7.40,2.50,[[[45.500,4.080],[45.500,0.080],[38.691,0.080],[38.691,0.000],[7.251,0.000],[7.251,0.080],[1.000,0.080],[1.000,4.080],[7.551,4.080],[7.551,2.250],[9.143,2.250],[9.143,6.600],[9.209,7.168],[9.370,7.630],[9.402,7.705],[9.662,8.120],[9.712,8.185],[9.927,8.400],[10.059,8.531],[10.124,8.582],[10.538,8.841],[10.614,8.873],[11.075,9.034],[11.643,9.100],[13.493,9.100],[14.293,9.900],[33.393,9.900],[33.893,10.400],[34.493,10.400],[35.062,10.335],[35.523,10.172],[35.599,10.141],[36.013,9.882],[36.078,9.831],[36.425,9.486],[36.474,9.420],[36.735,9.005],[36.767,8.930],[36.928,8.467],[36.993,7.900],[36.993,2.250],[38.551,2.250],[38.551,4.080],[42.599,4.080]]]],
  [9.90,0.60,[[[45.500,4.080],[45.500,0.080],[38.691,0.080],[38.691,0.000],[7.251,0.000],[7.251,0.080],[1.000,0.080],[1.000,4.080],[7.551,4.080],[7.551,2.250],[38.551,2.250],[38.551,4.080],[42.635,4.080]]]]
];
// Depths are shifted by -0.08 before polygon() and the 0.08 is added back in the 3D transform: OpenSCAD 2021 snaps 2D
// points to a 1/65536 mm grid, which put the plate-flush faces (Z 0.08 / 4.08) 0.0000134 mm off the plate and left a
// non-manifold sliver edge. Shifted, those faces sit at exactly 0 and 4.0 (on the grid); the shape is unchanged.
// The block is cut 0.1 mm oversize in height, then clipped in rack coordinates by the same box as ks_box_cut, so its
// top/bottom faces are the very same numbers as the plate opening (the transform alone landed them a hair off).
module ks_golden(){for(x=keystones)intersection(){
 translate([x,0,plate_center])multmatrix([[1,0,0,0],[0,0,1,-4],[0,-1,0,25.09],[0,0,0,1]])intersection(){
  union()for(b=KS_GOLD)translate([b[0],0,0])rotate([90,0,90])linear_extrude(height=b[1])for(pg=b[2])
   translate([b[1]>10&&min([for(q=pg)q[0]])>30?-ks_tight:0,0])polygon([for(q=pg)[q[0],q[1]-0.08]]);  // opening band, hook side
  translate([-10.5,25.09-18.6,-0.09])cube([21,33.7,10.42]);
 }
 translate([x-10.5,-plate_t-1,plate_center-15])cube([21,plate_t+16,33.5]);
}}
module ks_box_cut(){for(x=keystones)translate([x-10.5,-plate_t-0.01,plate_center-15])cube([21,plate_t+0.02,33.5]);}
module plate_joint_cut(rear=false){if(joint=="screw"&&(!sleeve||rear))for(x=joint_x)translate([x,-0.1,tray_z+14])rotate([-90,0,0])cylinder(d=joint_pilot,h=8.2);}

module faceplate(){
 union(){
  difference(){
   union(){
    plate_layer(-plate_t,plate_t);
    if(ks_style=="v2")ks_collar();
    plate_joint_add();
   }
   plate_joint_cut();
   if(sleeve&&joint=="screw")for(x=sl_joints,z=sl_joint_z)translate([x,-plate_t-0.1,z])rotate([-90,0,0])cylinder(d=m3_clear,h=plate_t+0.2);
   if(ks_style=="v2")ks_cut(); else ks_box_cut();
  }
  if(ks_style!="v2")ks_golden();
 }
}
// Plain plate on the rear posts (mirror of the faceplate, no openings) that the tray's rear end screws/snaps to.
module rear_bracket(){to_rear()difference(){union(){plate_layer(-plate_t,plate_t,false,true);plate_joint_add(true);}plate_joint_cut(true);}}

module device_features_add(){
 wall_add();
 sleeve_v2_add();
 if(sleeve){
  for(side=[-1,1]){
   x=side<0?dev_off_x-sl_half-sl_wall:dev_off_x+sl_half;
   translate([x,0,floor_top])cube([sl_wall,sl_rear,sl_window_top-floor_top]);
   if(sl_lip>0)translate([side<0?x:dev_off_x+sl_half-min(sl_lip_w,sl_half),0,sl_window_top])cube([sl_wall+min(sl_lip_w,sl_half),sl_rear,sl_lip]);
  }
  translate([dev_x,sl_rear,floor_top])cube([fp_w,sl_stop_t,min(sl_stop_h,dev_h-foot_h)]);
 }

 // @flat-begin
 if(device_mount=="flat"){
  // Corner stops outside the footprint, with 0.2 mm nominal clearance. Retention UNKNOWN.
  for(x=[dev_x-6.2,dev_x+fp_w+0.2],y=[dev_y,dev_y+fp_d-min(6,fp_d)])
   translate([x,y,floor_top])cube([6,min(6,fp_d),min(6,dev_h-foot_h)]);
  for(x=[dev_x,dev_x+fp_w-min(6,fp_w)],y=[dev_y-6.2,dev_y+fp_d+0.2])
   translate([x,y,floor_top])cube([min(6,fp_w),6,min(6,dev_h-foot_h)]);
 }
 // @flat-end
 if(device_mount=="inserts")for(h=[for(q=holes)dp(q)])translate([dev_x+h[0],dev_y+h[1],floor_top])cylinder(d=max(insert_pilot+3.5,7),h=standoff);
 if(device_mount=="pegs")for(h=[for(q=holes)dp(q)])translate([dev_x+h[0],dev_y+h[1],floor_top]){
  cylinder(d=hole_d+3,h=standoff);
  translate([0,0,standoff])cylinder(d=hole_d-0.3,h=board_t+0.8);
  translate([0,0,standoff+board_t+0.8])cylinder(d1=hole_d-0.3,d2=hole_d-1,h=0.8);
 }
 if(device_mount=="clips"){
  // Support ledges at the four corners plus a flexing clip on each side.
  for(x=[dev_x-1,dev_x+fp_w-5],y=[dev_y-1,dev_y+fp_d-5])translate([x,y,floor_top])cube([6,6,standoff]);
  for(s=[-1,1])translate([s>0?dev_x+fp_w+0.2:dev_x-2.2,dev_y+fp_d/2-5,floor_top]){
   cube([2,10,standoff+board_t+2.5]);
   translate([s>0?-1.2:2,0,standoff+board_t+0.2])hull(){cube([1.2,10,1.6]);translate([s>0?1.2:0,0,1.6])cube([0.01,10,0.6]);}
  }
 }
}
module device_features_cut(){
 if(sleeve&&joint=="screw")for(x=sl_joints,z=sl_joint_z)translate([x,-0.1,z])rotate([-90,0,0])cylinder(d=joint_pilot,h=8.1);
 // Strap access through each wall at quarter-depth, clear of the front/rear joints.
 if(sleeve)for(side=[-1,1],y=[dev_y+fp_d*0.25,dev_y+fp_d*0.75])
  translate([side<0?dev_off_x-sl_half-sl_wall-0.1:dev_off_x+sl_half-0.1,y-6,floor_top-0.1])cube([sl_wall+0.2,12,3.1]);

 if(device_mount=="inserts")for(h=[for(q=holes)dp(q)])translate([dev_x+h[0],dev_y+h[1],floor_top+0.01])cylinder(d=insert_pilot,h=standoff+0.1);
 if(device_mount=="straps"||device_mount=="flat"||sleeve)for(x=[dev_x-5.5,dev_x+fp_w+2.5],y=[dev_y+fp_d*0.25,dev_y+fp_d*0.75])
  translate([x,y-6,tray_z-0.1])cube([3,12,tray_t+0.2]);
 // Blind pockets retain at least foot_min_floor; taller feet pass through the floor by design.
 if(foot_h>0&&(device_mount=="flat"||sleeve))for(f=feet){corners=[dp([f[0],f[1]]),dp([f[0]+f[2],f[1]]),dp([f[0],f[1]+f[3]]),dp([f[0]+f[2],f[1]+f[3]])];x0=dev_x+min([for(p=corners)p[0]])-foot_clearance;x1=dev_x+max([for(p=corners)p[0]])+foot_clearance;y0=dev_y+min([for(p=corners)p[1]])-foot_clearance;y1=dev_y+max([for(p=corners)p[1]])+foot_clearance;deep=f[4]+foot_extra_depth;
  translate([x0,y0,deep>tray_t-foot_min_floor?tray_z-0.1:floor_top-deep])cube([x1-x0,y1-y0,deep>tray_t-foot_min_floor?tray_t+0.2:deep+0.02]);}
}

// @wall-begin
wall_open=["rear"]; wall_clear=0.5; wall_t=2; wall_h=min(12,dev_h-2);
function wall_spans(l,opened,notch)=opened?(l<30?[]:[[-2.5,9.5,wall_h],[l-9.5,l+2.5,wall_h]]):notch&&l>=40?[[-2.5,l/2-10,wall_h],[l/2-10,l/2+10,min(4,wall_h)],[l/2+10,l+2.5,wall_h]]:[[-2.5,l+2.5,wall_h]];
function wall_local()=[for(side=["front","rear","left","right"])let(hz=side=="front"||side=="rear",l=hz?dev_w:dev_d,c=side=="front"||side=="left"?-2.5:(hz?dev_d:dev_w)+.5)for(a=wall_spans(l,len([for(o=wall_open)if(o==side)o])>0,!hz))hz?[a[0],c,a[1],c+2,a[2]]:[c,a[0],c+2,a[1],a[2]]];
function wall_rects()=[for(q=wall_local())let(a=dp([q[0],q[1]]),b=dp([q[2],q[3]]))[dev_x+min(a[0],b[0]),dev_y+min(a[1],b[1]),dev_x+max(a[0],b[0]),dev_y+max(a[1],b[1]),q[4]]];
module wall_add(){if(device_mount=="wall")for(q=wall_rects())translate([q[0],q[1],floor_top-.01])cube([q[2]-q[0],q[3]-q[1],q[4]+.01]);}
assert(device_mount!="wall"||(is_list(wall_open)&&len(wall_open)>0&&len([for(s=["front","rear","left","right"])if(len([for(o=wall_open)if(o==s)o])>0)s])<4&&len([for(s=wall_open)if(s!="front"&&s!="rear"&&s!="left"&&s!="right")s])==0),"Open sides must leave at least one open and one closed");
assert(device_mount!="wall"||dev_h>2,"A wall needs a device taller than 2 mm");
assert(device_mount!="wall"||len([for(q=wall_rects())if(q[1]<0||(joint=="screw"&&len([for(x=joint_x)if(q[0]<x+9&&q[2]>x-9&&(q[1]<11.3&&q[3]>0||q[1]<22&&q[3]>9&&len([for(side=[-1,1])if(q[0]<x+side*6+1&&q[2]>x+side*6-1)side])>0))x])>0))q])==0,"The wall would hit the faceplate joint; set the device back or move it sideways.");
// @wall-end

module tray_joint_add(rear=false){
 if(joint=="screw"&&(!sleeve||rear)){
  for(x=joint_x) translate([x-9,0,tray_z+tray_t])cube([18,8,5]);
  for(x=joint_x)translate([x-7,8.3,tray_z+3])cube([14,3,19]);
  for(x=joint_x) for(side=[-1,1]) translate([x+side*6-1,0,0])
    hull(){translate([0,9,tray_z+2.7])cube([2,2,0.5]);
           translate([0,9,tray_z+8])cube([2,2,0.5]);
           translate([0,(device_mount=="flat"||sleeve)?9.5:20,tray_z+2.7])cube([2,2,0.5]);}
 }
}
module tray_joint_cut(rear=false){
 if(joint=="screw"&&(!sleeve||rear)){
  for(x=joint_x)translate([x-(tongue_w+slot_clear)/2,-0.1,tongue_z-slot_clear/2])cube([tongue_w+slot_clear,tongue_depth+slot_clear,tongue_h+slot_clear]);
  for(x=joint_x)translate([x,11.4,tray_z+14])rotate([90,0,0])cylinder(d=m3_clear,h=12);
 }
 if(joint=="snap")for(x=joint_x)translate([x-4.3,11.6,tray_z-0.1])cube([8.6,3.2,tray_t+0.2]);
}

module tray(){
 difference(){
  union(){
   translate([tray_x,tray_y,tray_z])cube([tray_w,tray_d,tray_t]);
   tray_joint_add();
   if(rear_support)to_rear()tray_joint_add(true);
   device_features_add();
  }
  tray_joint_cut();
  if(rear_support)to_rear()tray_joint_cut(true);
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
  %translate([dev_x,dev_y,floor_top+(device_mount=="inserts"||device_mount=="pegs"||device_mount=="clips"?standoff:0)-foot_h])cube([fp_w,fp_d,dev_h]);}
}

// ---- wizard overrides: Hue Bridge test
dev_w=90.7;
dev_d=90.4;
dev_h=25.4;
hole_d=2.7;
standoff=6.0;
insert_pilot=3.2;
board_t=1.6;
u=1;
holes=[];
keystones=[];
device_mount="wall";
joint="screw";
rear_support=false;
coupon=[];
wall_open=["rear"];
dev_off_y=13.0;
ports=[];
