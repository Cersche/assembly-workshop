// ER6-A (2026-11-04): TP-Link ER605 one-piece 1U bracket, print-friendly remix of Mixmeister's
// "TP-Link ER605 Omada 10-inch rack mount" (MakerWorld, BY-NC-SA). Rebuilt from scratch from its measured dimensions.
// PROPOSED, UNPRINTED. Fit and strength UNKNOWN. Prints standing on the plate's front face, no supports.
// Frame: X centred, plate back Y=0 (front Y=-4), Z=0 slot bottom. Router goes in from the front through the plate window.
id="ER6-A";
// ---- Faceplate: project standard (44.4/U, 252 wide, 4 thick, R2.5, four-corner slots), same code as equipment_tray.scad
u=1; rack_pitch=44.45; plate_gap=0.05; plate_w=252; plate_t=4; plate_r=2.5;
plate_h=u*rack_pitch-plate_gap; plate_center=u*rack_pitch/2; hole_x=118.2625; hole_dz=15.902;
// ---- Pocket and walls: kept from the source
pk_w=158.7; pk_h=25.7; pk_end=97.7;  // Y of the rear stop start; 101.7 from the plate front, so a 101 deep router ends about flush
wall=4; arm_x=69.35;                 // bottom wall opening half width
open_y=12.8; open_r=20;              // bottom opening front edge and corner radius (source about R21)
// ---- Print-friendly changes
stop_in=5;      // 45 deg rear stop, reaches in as far as the source's bar
root=5;         // plate-to-sleeve chamfer (source 3)
corner_r=2;     // sleeve outside corners along the print axis (source square)
foot=0.4;       // first-layer relief at the window's front edge
hex_flat=22; hex_pitch=26; hex_s=5;  // stretched hexes: 22 wide, 45 deg roofs. Source 30 deg roofs (too flat), about 40 holes, 2 struts, half hexes at the edges
hex_rows=3; hex_cols=6; hex_cy=49.5; hex_strut=4;
hex_py=hex_flat/2-(hex_pitch/2-hex_flat/2)+2*hex_s+hex_strut*sqrt(2);  // row pitch for a 4 mm strut along the 45 deg edges
win_hh=8.5; win_y0=8; win_y1=92;     // side window, pointed ends
$fn=64;
out_w=pk_w+2*wall; out_h=pk_h+2*wall; rear=pk_end+stop_in;
pk_lo=plate_center-pk_h/2; pk_hi=plate_center+pk_h/2;

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
// Rear ears: side wall carries on past the tube and turns in at 45 deg, so the stop needs no bridge.
module ear2d(){polygon([[pk_w/2,pk_end-0.01],[pk_w/2-stop_in,rear],[out_w/2,rear],[out_w/2,pk_end-0.01]]);}
module ears(){intersection(){
  for(s=[-1,1])scale([s,1,1])translate([0,0,plate_center-out_h/2])linear_extrude(height=out_h)ear2d();
  along(pk_end-1,rear+1)outer2d(0);
}}
// Bottom wall opening, open to the rear (as the source)
module bottom_open(){translate([0,0,pk_lo-wall-1])linear_extrude(height=wall+1.01)
  offset(r=open_r)offset(delta=-open_r)polygon([[-arm_x,open_y],[arm_x,open_y],[arm_x,rear+40],[-arm_x,rear+40]]);}
// Top wall hexes: whole hexes only, stretched so every roof is 45 deg
module top_hexes(){for(r=[0:hex_rows-1]){n=r%2==0?hex_cols:hex_cols-1;
  for(c=[0:n-1])translate([(c-(n-1)/2)*hex_pitch,hex_cy+(r-(hex_rows-1)/2)*hex_py,pk_hi-0.01])
    linear_extrude(height=wall+1){w=hex_flat/2;polygon([[w,-hex_s],[w,hex_s],[0,hex_s+w],[-w,hex_s],[-w,-hex_s],[0,-hex_s-w]]);}}}
module side_window(){c=plate_center;
  translate([-out_w,0,0])rotate([90,0,90])linear_extrude(height=2*out_w)
    polygon([[win_y0,c],[win_y0+win_hh,c+win_hh],[win_y1-win_hh,c+win_hh],[win_y1,c],[win_y1-win_hh,c-win_hh],[win_y0+win_hh,c-win_hh]]);}
module side_windows(){difference(){side_window();translate([-pk_w/2,-5,-5])cube([pk_w,200,100]);}}
module id_cut(){translate([99,0,0])along(-0.6,0.01)translate([0,plate_center])mirror([1,0])
  text(id,size=5,font="Liberation Sans:style=Bold",halign="center",valign="center");}

module bracket(){difference(){
  union(){
    along(-plate_t,0)plate2d();
    root_chamfer();
    along(0,pk_end)outer2d(0);
    ears();
  }
  // Pocket through the plate and tube
  along(-plate_t-1,pk_end+0.001)pocket2d(0);
  // 45 deg relief at the bed so first-layer squish can't pinch the router on its way in
  hull(){along(-plate_t-0.01,-plate_t)pocket2d(foot);along(-plate_t+foot,-plate_t+foot+0.01)pocket2d(0);}
  bottom_open();
  top_hexes();
  side_windows();
  id_cut();
}}
bracket();
