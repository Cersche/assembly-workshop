// SCR5-A — INCOMPLETE CONCEPT REVIEW ONLY. No manufacturing approval.
// X viewed from front, Y rearward, Z above U3 bottom. All mm.
// Generated include is an exact projection of SCR5-A_parameters.json.
include <SCR5-A_config.scad>
$fn=48;
part="assembled"; // plate, frame, assembled, no_id, screen, intersection
eps=0.02;
aw=glass_w-lip_left-lip_right;
ah=glass_h-lip_bottom-lip_top;
ax=(lip_left-lip_right)/2;
az=centre_z+(lip_bottom-lip_top)/2;
cx=max(glass_w/2+max(glass_clear_left,glass_clear_right),abs(pcb_reg_x)+pcb_w/2+pcb_clear_x);
ch=max(glass_h/2+max(glass_clear_top,glass_clear_bottom),abs(pcb_reg_z)+pcb_h/2+pcb_clear_z);
fy=frame_front_y+frame_t;
br=insert_od/2+boss_wall;
assert(plate_h==88.8 && plate_w==252 && plate_t==4);
assert(insert_seat_depth<frame_t && id_depth<frame_t);
// Extrude an X/Z sketch from Y=start toward the rear.
module xz(start,depth){translate([0,start+depth,0])rotate([90,0,0])linear_extrude(depth)children();}
module rr(w,h,r){hull()for(x=[-w/2+r,w/2-r],z=[-h/2+r,h/2-r])translate([x,z])circle(r=r);}
module aperture(){translate([ax,az])rr(aw,ah,aperture_r);}
module rack_slots(){for(x=[-slot_x,slot_x],z=slot_z)translate([x,z])hull()for(dx=[-1.5,1.5])translate([dx,0])circle(d=7);}
module access(){
 // Smooth rounded opening silhouettes; no sharp internal square cut ends.
 xz(ribbon_cut_y,ribbon_depth)translate([ribbon_x,ribbon_z])rr(ribbon_width,20,ribbon_edge_r);
 xz(buttons_y,buttons_depth)translate([buttons_x,buttons_z])rr(buttons_width,buttons_height,buttons_edge_r);
}
module plate(){difference(){
 union(){
  xz(-plate_t,plate_t)translate([0,centre_z])rr(plate_w,plate_h,plate_r);
  xz(0,pocket_depth)difference(){
   translate([0,centre_z])square([2*(cx+pocket_wall),2*(ch+pocket_wall)],center=true);
   translate([0,centre_z])square([2*cx,2*ch],center=true);
  }
 }
 xz(-plate_t-eps,plate_t+2*eps){aperture();rack_slots();}
 access();
 // Side windows retain the frame hooks; closed rear shoulders remain.
 for(s=[-1,1],z=clip_z)translate([s*(cx+pocket_wall/2)-pocket_wall,clip_window_y,z-clip_window_h/2])cube([2*pocket_wall,clip_window_depth,clip_window_h]);
}}
// Angled, rounded lettering is an intentional source-level engraving profile;
// no STL vertices are repaired, moved or merged after rendering.
module id_cut(){xz(fy-id_depth,id_depth+eps)translate([id_x,id_z])rotate(5)offset(r=0.08)text("SCR5-A",size=id_size,halign="center",valign="center",font="Liberation Sans:style=Bold");}
module head_access(){
 // Counterbore-shaped clearance envelope, default 5.1 x 2.8.
 // At this concept's rear PCB plane it opens into free space, rather than
 // inventing a printed seat on an unmeasured/component-bearing PCB surface.
 for(x=[-hole_dx/2,hole_dx/2],z=[centre_z-hole_dz/2,centre_z+hole_dz/2]){
  xz(pcb_front_y+pcb_t,screw_head_h+head_clearance_h)
   translate([x+pcb_reg_x,z+pcb_reg_z])circle(d=screw_head_d+head_clearance_d);
  xz(pcb_front_y+pcb_t+screw_head_h,pocket_depth)
   translate([x+pcb_reg_x,z+pcb_reg_z])circle(d=tool_d);
 }
}
module frame(engraved=true){difference(){union(){
 xz(frame_front_y,frame_t)difference(){
  translate([0,centre_z])square([frame_outer_w,frame_outer_h],center=true);
  translate([0,centre_z])square([frame_inner_w,frame_inner_h],center=true);
 }
 for(x=[-hole_dx/2,hole_dx/2],z=[centre_z-hole_dz/2,centre_z+hole_dz/2])
  xz(frame_front_y,frame_t)translate([x+pcb_reg_x,z+pcb_reg_z])circle(r=br);
 // Four compliant side beams. Squeeze inward to remove; deflection is unvalidated.
 for(s=[-1,1],z=clip_z){
  translate([s*clip_x-clip_t/2,frame_front_y,z-clip_h/2])cube([clip_t,clip_end_y-frame_front_y,clip_h]);
  xz(frame_front_y,frame_t)translate([s*((frame_outer_w/2-0.5+clip_x+clip_t/2)/2),z])
   square([clip_x+clip_t/2-frame_outer_w/2+0.5,clip_h],center=true);
  // Wedge leading nose, flat rear bearing against pocket-window rear shoulder.
  translate([0,0,z-clip_h/2])linear_extrude(clip_h)polygon([
   [s*(clip_x-clip_t/2),clip_window_y],
   [s*(clip_x+clip_t/2+clip_hook),clip_end_y-0.5],
   [s*(clip_x+clip_t/2+clip_hook),clip_end_y],
   [s*(clip_x-clip_t/2),clip_end_y]]);
 }
 }
 for(x=[-hole_dx/2,hole_dx/2],z=[centre_z-hole_dz/2,centre_z+hole_dz/2]){
  xz(fy-insert_seat_depth,insert_seat_depth+eps)translate([x+pcb_reg_x,z+pcb_reg_z])circle(d=insert_pilot);
  // Rear lead-in chamfer; the nominal metal OD is independent of pilot.
  translate([x+pcb_reg_x,fy-insert_leadin,z+pcb_reg_z])rotate([-90,0,0])cylinder(h=insert_leadin+eps,d1=insert_pilot,d2=insert_pilot+0.4);
 }
 access();
 head_access();
 if(engraved)id_cut();
}}
module screen(){ // Nominal envelope only, never in the delivery package.
 color([0.12,0.12,0.14,0.45])translate([-glass_w/2,seat_y,centre_z-glass_h/2])cube([glass_w,glass_t,glass_h]);
 color([0.1,0.5,0.2,0.45])translate([pcb_reg_x-pcb_w/2,pcb_front_y,centre_z+pcb_reg_z-pcb_h/2])cube([pcb_w,pcb_t,pcb_h]);
 color([0.15,0.6,0.9,0.6])xz(seat_y-0.02,0.01)translate([active_offset_x,centre_z+active_offset_z])square([active_w,active_h],center=true);
}
module review_keepouts(){ // Provisional boxes [x,y,z,w,depth,height], NOT measured.
 for(k=[touch_keepout,fpc_keepout])color([0.9,0.15,0.25,0.45])translate([k[0],k[1],k[2]])cube([k[3],k[4],k[5]]);
}
if(part=="plate")plate();
else if(part=="frame")frame();
else if(part=="no_id")frame(false);
else if(part=="intersection")intersection(){plate();frame();}
else if(part=="screen")screen();
else {color("slategray")plate();color("orange")frame();screen();review_keepouts();}
