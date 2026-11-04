// ER6-H (2026-11-04): ER6-G with 3 long floor slots instead of hexes (Brian). ER6-G: ER6-F plus a keystone on each side of the plate. ER6-F: ER6-E with the rear stop 0.7 forward so the router face is flush with the plate front. Honeycomb floor, open top, sloped solid side walls.
// Brian's cue: a supplied picture of a similar open-top bracket. Dimensions and detents from ER6-D. Remix of Mixmeister's ER605 mount (MakerWorld, BY-NC-SA).
// PROPOSED, UNPRINTED. Fit and strength UNKNOWN. Prints standing on the plate's front face, no supports.
// Frame: X centred, plate back Y=0 (front Y=-4), Z=0 slot bottom. Router goes in from the front through the plate window.
id="ER6-H";
// ---- Faceplate: project standard (44.4/U, 252 wide, 4 thick, R2.5, four-corner slots), same code as equipment_tray.scad
u=1; rack_pitch=44.45; plate_gap=0.05; plate_w=252; plate_t=4; plate_r=2.5;
plate_h=u*rack_pitch-plate_gap; plate_center=u*rack_pitch/2; hole_x=118.2625; hole_dz=15.902;
// ---- Pocket: width and stop from the source, height 26.0 (Brian, ER6-D; case measured 26)
pk_w=158.7; pk_h=26; pk_end=97; wall=4;
// ---- Simplified body
collar_y=12;    // top wall stops here; the rest is open
side_rear=10;   // side wall height above the floor at the rear end; slopes up to the collar
stop_in=5;      // 45 deg rear stop on each side wall
root=4.5;       // plate-to-sleeve chamfer
corner_r=2;     // collar and floor outside corners
foot=0.4;       // first-layer relief at the window's front edge
// ---- Floor slots: run front to rear so each layer crosses only 3 openings; 6 mm ribs carry the load along the depth
slot_w=28; slot_rib=6; slot_y0=18; slot_apex=90; slot_ch=3;
// ---- Keyhole detents. Router (Brian): 158 x 101, keyhole round part dia 8, 17.25 from each side, 50 from the rear edge
case_w=158; key_c=17.25; key_rear=50; key_x=case_w/2-key_c; key_y=pk_end-key_rear;
arm_w=8; arm_t=1.8; arm_gap=1.2;     // KD-E arm section and gap
arm_root_y=14; arm_tip=key_y+4;
bump_w=5; bump_up=2; bump_flat=2;    // KD-E height, width and 45/60 deg faces; flat shortened to fit the dia 8 hole
// ---- Keystones: golden block, copied unchanged from SG8-M6-F (ks_tight 0.2 printed a perfect fit). Source: Goul, "10 inch shelf TP-Link SG108 Plus Keystone" (MakerWorld, BY-NC-SA).
keystones=[-99,99];
$fn=64;
out_w=pk_w+2*wall; out_h=pk_h+2*wall; rear=pk_end+stop_in;
pk_lo=plate_center-pk_h/2; pk_hi=plate_center+pk_h/2; fl_lo=pk_lo-wall; top=pk_hi+wall;

module along(y0,y1){translate([0,y1,0])rotate([90,0,0])linear_extrude(height=y1-y0)children();}
module capsule2d(len=10,diam=7){hull(){translate([-(len-diam)/2,0])circle(d=diam);translate([(len-diam)/2,0])circle(d=diam);}}
module rrect(w,h,r){offset(r=r)square([w-2*r,h-2*r],center=true);}
module plate2d(){difference(){
  hull()for(sx=[-1,1],sz=[-1,1])translate([sx*(plate_w/2-plate_r),plate_center+sz*(plate_h/2-plate_r)])circle(r=plate_r);
  for(i=[0:u-1],dz=[-hole_dz,hole_dz],x=[-hole_x,hole_x])translate([x,i*rack_pitch+rack_pitch/2+dz])capsule2d();
}}
module outer2d(extra=0){translate([0,plate_center])rrect(out_w+2*extra,out_h+2*extra,corner_r+extra);}
module pocket2d(extra=0){translate([0,plate_center])square([pk_w+2*extra,pk_h+2*extra],center=true);}
module root_chamfer(){hull(){along(-0.01,0)outer2d(root);along(root,root+0.01)outer2d(0);}}
module ears(){intersection(){
  for(s=[-1,1])scale([s,1,1])translate([0,0,fl_lo])linear_extrude(height=out_h)
    polygon([[pk_w/2+0.01,pk_end-0.01],[pk_w/2-stop_in,rear],[out_w/2,rear],[out_w/2,pk_end-0.01]]);
  along(pk_end-1,rear+1)outer2d(0);
}}
// Everything above this line goes: top wall behind the collar, side walls sloping down to the rear.
module top_cut(){translate([-out_w,0,0])rotate([90,0,90])linear_extrude(height=2*out_w)
  polygon([[collar_y,top+2],[collar_y,pk_hi],[rear,pk_lo+side_rear],[rear+2,pk_lo+side_rear],[rear+2,top+2]]);}
module floor_slots(){for(i=[-1,0,1])translate([i*(slot_w+slot_rib),0,fl_lo-1])linear_extrude(height=wall+1.01){w=slot_w/2;
  polygon([[-w+slot_ch,slot_y0],[w-slot_ch,slot_y0],[w,slot_y0+slot_ch],[w,slot_apex-w],[0,slot_apex],[-w,slot_apex-w],[-w,slot_y0+slot_ch]]);}}
// Slot around each arm, through the floor, pointed rear end so no bridge
module arm_slot(s){h=arm_w/2+arm_gap;translate([s*key_x,0,fl_lo-1])linear_extrude(height=wall+1.01)
  polygon([[-h,arm_root_y],[h,arm_root_y],[h,arm_tip+arm_gap],[0,arm_tip+arm_gap+h],[-h,arm_tip+arm_gap]]);}
module detent(s){translate([s*key_x,0,0]){
  translate([-arm_w/2,arm_root_y-1,pk_lo-arm_t])cube([arm_w,arm_tip-arm_root_y+1,arm_t]);
  y0=key_y-(bump_up+bump_flat+bump_up*tan(30))/2;
  translate([-bump_w/2,0,0])rotate([90,0,90])linear_extrude(height=bump_w)
    polygon([[y0-0.01,pk_lo-0.01],[y0+bump_up,pk_lo+bump_up],[y0+bump_up+bump_flat,pk_lo+bump_up],[y0+bump_up+bump_flat+bump_up*tan(30),pk_lo-0.01]]);
}}
// ID moved to the collar top; the plate back now has keystones where it was
module id_cut(){translate([0,8,top-0.6])linear_extrude(height=1)
  text(id,size=5,font="Liberation Sans:style=Bold",halign="center",valign="center");}
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


module bracket(){union(){detent(-1);detent(1);ks_golden();difference(){
  union(){
    along(-plate_t,0)plate2d();
    root_chamfer();
    difference(){union(){along(0,pk_end)outer2d(0);ears();}top_cut();}
  }
  along(-plate_t-1,pk_end+0.001)pocket2d(0);
  hull(){along(-plate_t-0.01,-plate_t)pocket2d(foot);along(-plate_t+foot,-plate_t+foot+0.01)pocket2d(0);}
  floor_slots();
  arm_slot(-1);arm_slot(1);
  ks_box_cut();
  id_cut();
}}}
bracket();
