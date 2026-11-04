// ER6-F (2026-11-04): ER6-E with the rear stop 0.7 forward so the router face is flush with the plate front. Honeycomb floor, open top, sloped solid side walls.
// Brian's cue: a supplied picture of a similar open-top bracket. Dimensions and detents from ER6-D. Remix of Mixmeister's ER605 mount (MakerWorld, BY-NC-SA).
// PROPOSED, UNPRINTED. Fit and strength UNKNOWN. Prints standing on the plate's front face, no supports.
// Frame: X centred, plate back Y=0 (front Y=-4), Z=0 slot bottom. Router goes in from the front through the plate window.
id="ER6-F";
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
// ---- Floor honeycomb: whole hexes, 45 deg roofs, 4 mm struts
hex_w=16; hex_pitch=20; hex_s=3; hex_strut=4; hex_rows=4; hex_cols=5; hex_cy=53;
hex_py=hex_w/2-(hex_pitch/2-hex_w/2)+2*hex_s+hex_strut*sqrt(2);
// ---- Keyhole detents. Router (Brian): 158 x 101, keyhole round part dia 8, 17.25 from each side, 50 from the rear edge
case_w=158; key_c=17.25; key_rear=50; key_x=case_w/2-key_c; key_y=pk_end-key_rear;
arm_w=8; arm_t=1.8; arm_gap=1.2;     // KD-E arm section and gap
arm_root_y=14; arm_tip=key_y+4;
bump_w=5; bump_up=2; bump_flat=2;    // KD-E height, width and 45/60 deg faces; flat shortened to fit the dia 8 hole
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
module hex2d(){w=hex_w/2;polygon([[w,-hex_s],[w,hex_s],[0,hex_s+w],[-w,hex_s],[-w,-hex_s],[0,-hex_s-w]]);}
module floor_hexes(){for(r=[0:hex_rows-1]){n=r%2==0?hex_cols:hex_cols-1;
  for(c=[0:n-1])translate([(c-(n-1)/2)*hex_pitch,hex_cy+(r-(hex_rows-1)/2)*hex_py,fl_lo-1])
    linear_extrude(height=wall+1.01)hex2d();}}
// Slot around each arm, through the floor, pointed rear end so no bridge
module arm_slot(s){h=arm_w/2+arm_gap;translate([s*key_x,0,fl_lo-1])linear_extrude(height=wall+1.01)
  polygon([[-h,arm_root_y],[h,arm_root_y],[h,arm_tip+arm_gap],[0,arm_tip+arm_gap+h],[-h,arm_tip+arm_gap]]);}
module detent(s){translate([s*key_x,0,0]){
  translate([-arm_w/2,arm_root_y-1,pk_lo-arm_t])cube([arm_w,arm_tip-arm_root_y+1,arm_t]);
  y0=key_y-(bump_up+bump_flat+bump_up*tan(30))/2;
  translate([-bump_w/2,0,0])rotate([90,0,90])linear_extrude(height=bump_w)
    polygon([[y0-0.01,pk_lo-0.01],[y0+bump_up,pk_lo+bump_up],[y0+bump_up+bump_flat,pk_lo+bump_up],[y0+bump_up+bump_flat+bump_up*tan(30),pk_lo-0.01]]);
}}
module id_cut(){translate([99,0,0])along(-0.6,0.01)translate([0,plate_center])mirror([1,0])
  text(id,size=5,font="Liberation Sans:style=Bold",halign="center",valign="center");}

module bracket(){union(){detent(-1);detent(1);difference(){
  union(){
    along(-plate_t,0)plate2d();
    root_chamfer();
    difference(){union(){along(0,pk_end)outer2d(0);ears();}top_cut();}
  }
  along(-plate_t-1,pk_end+0.001)pocket2d(0);
  hull(){along(-plate_t-0.01,-plate_t)pocket2d(foot);along(-plate_t+foot,-plate_t+foot+0.01)pocket2d(0);}
  floor_hexes();
  arm_slot(-1);arm_slot(1);
  id_cut();
}}}
bracket();
