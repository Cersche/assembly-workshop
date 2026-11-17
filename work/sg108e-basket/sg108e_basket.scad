// TL-SG108E one-piece basket, DRAFT (2026-11-17, Brian): the ER605 ER6-H basket system for the SG108E,
// replacing the SG8-M6-F tray + post rails + faceplate. Second keystone on the right; switch moved left to make room.
// DRAFT: no ID, unprinted. Fit and strength UNKNOWN. The basket system itself (ER6-H) is also unprinted.
// Prints standing on the plate's front face, no supports (as ER6-H).
// Frame: X centred, plate back Y=0 (front Y=-4), Z=0 slot bottom. Switch goes in from the front through the window.
include <workshop.scad>
part="bracket";   // bracket | inlay | switch  (no screws except the 4 rack screws)
id="";            // drafts carry no ID; set at release
// ---- Switch fit: the SG8-M6-D/F pocket, printed and fits well (Brian 2026-10-31). Kept exactly.
dev_w=158; dev_d=100; dev_h=25;         // TL-SG108E (SG8-M6-F wizard values)
side_play=0.5; sleeve_top=1.35;          // proven; not the 0.8 library default
set_back=1.3;                            // switch front 1.3 behind the plate front: ports flush (Fit_Findings 2026-10-28)
dev_cx=-21.5;                            // was -15 on SG8-M6-F: 6.5 left so two keystones fit on the right
pk_w=dev_w+2*side_play; pk_h=dev_h+sleeve_top; dev_y0=-ws_plate_t+set_back; pk_end=dev_y0+dev_d;   // rear stop at 100 deep, as proven
// ---- Keystones: golden block (settled), two on the right. Blocks 21 wide, touching at X 88.5; outer edge 109.5 (post flange from 111.1).
keystones=[78,99];
labels=[["UPLINK",78,3.8,3.5],["WLAN",99,3.8,3.5]];   // WLAN = upstairs WLAN (Brian 2026-11-17). 3.5 (was 4.5): at 4.5 the two labels were ~1 mm apart
label_depth=0.6;
// ---- Basket body: ER6-H values
wall=4; collar_y=12; side_rear=10; stop_in=5; root=4.5; corner_r=2; foot=0.4;
// ---- Floor slots: ER6-H pattern, narrowed (23 instead of 28) to stay 9 mm clear of the detent slots
slot_w=23; slot_rib=6; slot_y0=18; slot_apex=90; slot_ch=3;
// ---- Keyhole detents: SG8-M6-F (KD-E) bump and arm, ER6-H-style arm in a floor slot
key_dx=55; key_y=dev_y0+48.5;            // keyholes ±55 from the switch centre, 48.5 from its front (SG8-M6-F)
arm_w=8; arm_t=1.8; arm_gap=1.2; arm_l=26; arm_tip=key_y+5; arm_root_y=arm_tip-arm_l;
bump_w=5; bump_up=2; bump_flat=4;        // KD-E: 2 high, 4 flat, 45 deg front, 60 deg rear
$fn=64;
pc=ws_plate_center(); out_w=pk_w+2*wall; out_h=pk_h+2*wall; rear=pk_end+stop_in;
pk_lo=pc-pk_h/2; pk_hi=pc+pk_h/2; fl_lo=pk_lo-wall; top=pk_hi+wall;

module along(y0,y1){translate([0,y1,0])rotate([90,0,0])linear_extrude(height=y1-y0)children();}
module rrect(w,h,r){offset(r=r)square([w-2*r,h-2*r],center=true);}
module outer2d(extra=0){translate([dev_cx,pc])rrect(out_w+2*extra,out_h+2*extra,corner_r+extra);}
module pocket2d(extra=0){translate([dev_cx,pc])square([pk_w+2*extra,pk_h+2*extra],center=true);}
module root_chamfer(){hull(){along(-0.01,0)outer2d(root);along(root,root+0.01)outer2d(0);}}
module ears(){translate([dev_cx,0,0])intersection(){
  for(s=[-1,1])scale([s,1,1])translate([0,0,fl_lo])linear_extrude(height=out_h)
    polygon([[pk_w/2+0.01,pk_end-0.01],[pk_w/2-stop_in,rear],[out_w/2,rear],[out_w/2,pk_end-0.01]]);
  translate([-dev_cx,0,0])along(pk_end-1,rear+1)outer2d(0);
}}
module top_cut(){translate([-200,0,0])rotate([90,0,90])linear_extrude(height=400)
  polygon([[collar_y,top+2],[collar_y,pk_hi],[rear,pk_lo+side_rear],[rear+2,pk_lo+side_rear],[rear+2,top+2]]);}
module floor_slots(){for(i=[-1,0,1])translate([dev_cx+i*(slot_w+slot_rib),0,fl_lo-1])linear_extrude(height=wall+1.01){w=slot_w/2;
  polygon([[-w+slot_ch,slot_y0],[w-slot_ch,slot_y0],[w,slot_y0+slot_ch],[w,slot_apex-w],[0,slot_apex],[-w,slot_apex-w],[-w,slot_y0+slot_ch]]);}}
module arm_slot(s){h=arm_w/2+arm_gap;translate([dev_cx+s*key_dx,0,fl_lo-1])linear_extrude(height=wall+1.01)
  polygon([[-h,arm_root_y],[h,arm_root_y],[h,arm_tip+arm_gap],[0,arm_tip+arm_gap+h],[-h,arm_tip+arm_gap]]);}
module detent(s){translate([dev_cx+s*key_dx,0,0]){
  translate([-arm_w/2,arm_root_y-1,pk_lo-arm_t])cube([arm_w,arm_tip-arm_root_y+1,arm_t]);
  y0=key_y-bump_flat/2-bump_up;
  translate([-bump_w/2,0,0])rotate([90,0,90])linear_extrude(height=bump_w)
    polygon([[y0-0.01,pk_lo-0.01],[y0+bump_up,pk_lo+bump_up],[y0+bump_up+bump_flat,pk_lo+bump_up],[y0+bump_up+bump_flat+bump_up*tan(30),pk_lo-0.01]]);
}}
module label2d(l){translate([l[1],l[2]])text(l[0],size=l[3],font="Liberation Sans:style=Bold",halign="center",valign="center");}
module label_cut(){for(l=labels)translate([0,-ws_plate_t+label_depth,0])rotate([90,0,0])linear_extrude(height=label_depth+0.1)mirror([0,0,0])label2d(l);}
module inlay(){for(l=labels)translate([0,-ws_plate_t+label_depth,0])rotate([90,0,0])linear_extrude(height=label_depth)label2d(l);}
module id_cut(){if(id!="")translate([dev_cx,8,top-0.6])linear_extrude(height=1)
  text(id,size=5,font="Liberation Sans:style=Bold",halign="center",valign="center");}

module bracket(){union(){detent(-1);detent(1);difference(){
  union(){
    rotate([90,0,0])linear_extrude(height=ws_plate_t)ws_plate2d();   // window and keystone boxes cut below, keystones added after
    root_chamfer();
    difference(){union(){along(0,pk_end)outer2d(0);ears();}top_cut();}
  }
  along(-ws_plate_t-1,pk_end+0.001)pocket2d(0);
  hull(){along(-ws_plate_t-0.01,-ws_plate_t)pocket2d(foot);along(-ws_plate_t+foot,-ws_plate_t+foot+0.01)pocket2d(0);}
  floor_slots();
  arm_slot(-1);arm_slot(1);
  for(x=keystones)ws_keystone_cut(x);
  label_cut();
  id_cut();
}
for(x=keystones)ws_keystone(x);
}}
// Switch mock: nominal box seated on the floor, front set back 1.3
module switch(){translate([dev_cx-dev_w/2,dev_y0,pk_lo])cube([dev_w,dev_d,dev_h]);}
if(part=="bracket")bracket();
if(part=="inlay")inlay();
if(part=="switch")switch();
