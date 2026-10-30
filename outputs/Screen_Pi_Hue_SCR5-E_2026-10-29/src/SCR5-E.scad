// SCR5-E, 2U (U4-U3) screen + Pi 4 + Hue Bridge + keystone unit. All dimensions mm. Claude, 2026-10-29.
// Brian: Pi lower left (USB/Ethernet through the plate), Hue on a shelf top left reaching behind the screen,
// keystone top left, screen on the right; M6 tray joints; U5 freed.
// Screen retention = SCR5-B (task 49) unchanged, translated by scx. Pi openings = HP4-M6-B unchanged, same X.
// Golden keystone and Hue cradle come from SCR5-E_hp4lib.scad (copy of HP4-M6-B.scad + overrides).
// Coordinates: X negative = left from the front, plate rear Y=0, Y+ into the rack, Z up from the U3 slot bottom.
// SCR5-E (Brian, 2026-10-29) = SCR5-C + Pi cooling: 30 x 30 x 7 5V fan on the deck over the Pi blowing down,
// vent slots in the floor under the Pi and in the right wall behind the screen.
// SCR5-E (Brian, 2026-10-29) = SCR5-D split for printing: floor+walls and deck print flat without supports and
// screw together with M2.5 inserts; deck front moved back to Y 36 so the DSI ribbon drop gap is ~10 mm.
// PROPOSED, UNVALIDATED: not printed. Fit, preload, shelf strength, ribbon reach, heat and access UNKNOWN.
include <SCR5-E_screen_config.scad>
use <SCR5-E_hp4lib.scad>
$fn=48;
part="assembled";
eps=0.02;
scx=33;                                   // screen centre X: pocket X -35.75..101.75
// Tray: floor (Pi) and shelf deck (Hue), joined to the plate at deck level by two HP4-style M6 joints.
floor_z=8.225; floor_t=3; floor_top=floor_z+floor_t;  // same floor height as HP4-M6-B, so its Pi openings line up
deck_z=40.5; deck_t=3; deck_top=deck_z+deck_t;       // >= 3 mm over the Pi envelope top (37.225)
tray_x0=-102; tray_x1=-6; tray_d=148; pi_zone_x1=-44; rear_zone_y=36;  // behind the screen the tray starts at Y 32
// Pi 4 exactly where HP4-M6-B has it: footprint X -102..-46, Y 0..85, rotated 270 (USB/Ethernet to the plate).
pi_x0=-102; pi_w=56; pi_d=85; pi_h=20; pi_standoff=6; pi_pilot=3.2;
pi_holes=[[3.5,81.5],[3.5,23.5],[52.5,81.5],[52.5,23.5]];
pi_ports=[[-93.0,26.8,15.0,17.5,1.0],[-75.0,26.8,15.0,17.5,1.0],[-56.3,25.6,17.5,15.0,1.0]];
// Hue Bridge v2 envelope in Brian's cradle (cradle posts 95 x 95; centre set in the lib overrides).
hue_cx=-54.4; hue_cy=93; hue_w=90.7; hue_d=90.4; hue_h=30.7;
// M6 joints (HP4-M6-B geometry, base moved from the floor to the deck).
joint_x=[-71,-50]; jz=24; tab_w=20; up_t=6; tab_foot_h=5; fil_r=4; cb_d=11.5; cb_depth=3.5;
m6_clear=6.6; m6_pilot=7.6; m6_boss_d=14; tongue_w=12; tongue_depth=7; tongue_h=3; slot_clear=0.3;

cx=pocket_half_x; ch=pocket_half_z;
aw=glass_w-lip_left-lip_right; ah=glass_h-lip_bottom-lip_top;
ax=(lip_left-lip_right)/2; az=centre_z+(lip_bottom-lip_top)/2;
br=insert_od/2+boss_wall;
fy=frame_front_y+frame_t;
pad_front_y=seat_y+total_depth-preload;
module xz(start,depth){translate([0,start+depth,0])rotate([90,0,0])linear_extrude(depth)children();}
module rr(w,h,r){hull()for(x=[-w/2+r,w/2-r],z=[-h/2+r,h/2-r])translate([x,z])circle(r=r);}
module aperture(){translate([ax,az])rr(aw,ah,aperture_r);}
module rack_slots(){for(x=[-slot_x,slot_x],z=slot_z)translate([x,z])hull()for(dx=[-1.5,1.5])translate([dx,0])circle(d=7);}
module cavity(){
 translate([0,centre_z])square([2*cx,2*ch],center=true);
 for(x=[-cx,cx],z=[centre_z-ch,centre_z+ch])translate([x,z])circle(r=pocket_relief_r);
}
module mouth(y,side,r,w,h,corner){
 n=52;
 points=[for(j=[0:8],q=[0:3],i=[0:12])let(
  d=r*j/8,growth=r-sqrt(r*r-(r-d)*(r-d)),a=q*90+i*7.5,
  xx=(q==0||q==3?1:-1)*(w/2-corner),
  zz=(q<2?1:-1)*(h/2-corner))
  [xx+(corner+growth)*cos(a),y+side*d,zz+(corner+growth)*sin(a)]];
 rawfaces=concat([[for(i=[0:n-1])i]],[[for(i=[n-1:-1:0])8*n+i]],
  [for(j=[0:7],i=[0:n-1])[j*n+i,(j+1)*n+i,(j+1)*n+(i+1)%n,j*n+(i+1)%n]]);
 polyhedron(points,side==1?rawfaces:[for(f=rawfaces)[for(i=[len(f)-1:-1:0])f[i]]],convexity=10);
}
module opening(y,depth,x,z,w,h,r,mr){
 xz(y,depth)translate([x,z])rr(w,h,r);
 for(yy=[y,frame_front_y,frame_front_y+frame_t])
  translate([x,0,z]){
   mouth(yy,1,mr,w,h,r);
   if(yy!=y)mouth(yy,-1,mr,w,h,r);
  }
}
module access(){
 opening(ribbon_cut_y,ribbon_depth,ribbon_x,ribbon_z,ribbon_width,ribbon_height,ribbon_edge_r,ribbon_mouth_r);
 opening(buttons_y,buttons_depth,buttons_x,buttons_z,buttons_width,buttons_height,buttons_edge_r,buttons_mouth_r);
}
module bosses(){for(x=[-boss_x,boss_x],z=boss_z)xz(0,boss_end_y)translate([x,z])circle(r=br);}
module screen_pocket_add(){
 xz(0,pocket_depth)difference(){
  translate([0,centre_z])square([2*(cx+pocket_wall),2*(ch+pocket_wall)],center=true);
  cavity();
 }
 bosses();
}
module screen_plate_cut(){
 xz(-plate_t-eps,plate_t+2*eps)aperture();
 for(x=[-boss_x,boss_x],z=boss_z){
  xz(boss_end_y-insert_seat_depth,insert_seat_depth+eps)translate([x,z])circle(d=insert_pilot);
  translate([x,boss_end_y-insert_leadin,z])rotate([-90,0,0])cylinder(h=insert_leadin+eps,d1=insert_pilot,d2=insert_pilot+.4);
 }
 access();
}
module rrect2(w,h,r){offset(r=r)square([w-2*r,h-2*r],center=true);}
module joint_plate_add(){
 for(x=joint_x){
  translate([x-tongue_w/2,0,deck_z+3.5])cube([tongue_w,tongue_depth,tongue_h]);
  translate([x,0,deck_z+jz])rotate([-90,0,0])cylinder(d=m6_boss_d,h=8);
 }
}
module joint_plate_cut(){for(x=joint_x)translate([x,-0.1,deck_z+jz])rotate([-90,0,0])cylinder(d=m6_pilot,h=8.2);}
module plate(){
 union(){
  difference(){
   union(){
    xz(-plate_t,plate_t)translate([0,centre_z])rr(plate_w,plate_h,plate_r);
    translate([scx,0,0])screen_pocket_add();
    joint_plate_add();
   }
   xz(-plate_t-eps,plate_t+2*eps){rack_slots();for(p=pi_ports)translate([p[0],p[1]])rrect2(p[2],p[3],p[4]);}
   translate([scx,0,0])screen_plate_cut();
   joint_plate_cut();
   ks_box_cut();
  }
  ks_golden();
 }
}
module pads(){for(x=[-pad_x,pad_x],z=[centre_z-pad_z_offset,centre_z+pad_z_offset])
 xz(pad_front_y,frame_front_y-pad_front_y+eps)translate([x,z])rr(pad_w,pad_h,pad_r);
}
module frame(engraved=true){translate([scx,0,0])difference(){union(){
 xz(frame_front_y,frame_t)difference(){
  translate([0,centre_z])rr(frame_outer_w,frame_outer_h,frame_outer_r);
  translate([0,centre_z])rr(frame_inner_w,frame_inner_h,frame_inner_r);
 }
 pads();
 }
 for(x=[-boss_x,boss_x],z=boss_z)xz(frame_front_y-eps,frame_t+2*eps)translate([x,z])circle(d=screw_clearance);
 access();
 if(engraved)xz(fy-id_depth,id_depth+eps)translate([id_x,id_z])rotate(5)offset(r=.08)
  text("SCR5-E",size=id_size,halign="center",valign="center",font="Liberation Sans:style=Bold");
}}
// ID on the floor top behind the screen (the cradle covers the whole deck).
// Floor/deck footprint: full depth over the Pi zone, from Y 32 behind the screen (frame + screw heads end at Y 26.5).
module footprint(z,t){
 translate([tray_x0,0,z])cube([pi_zone_x1-tray_x0,tray_d,t]);
 translate([pi_zone_x1-eps,rear_zone_y,z])cube([tray_x1-pi_zone_x1+eps,tray_d-rear_zone_y,t]);
}
module joint_tabs(){
 ft=deck_top;
 for(x=joint_x){
  translate([0,8.3+up_t,0])rotate([90,0,0])linear_extrude(up_t)hull(){translate([x-tab_w/2,ft-0.01])square([tab_w,1]);translate([x,deck_z+jz])circle(d=tab_w);}
  hull(){translate([x-tab_w/2,0,ft-0.01])cube([tab_w,8.3+up_t,1]);translate([x-tab_w/2,8.3,ft-0.01])cube([tab_w,0.01,tab_foot_h]);
        translate([x-tab_w/2,1.5,ft+tab_foot_h-1.5])rotate([0,90,0])cylinder(r=1.5,h=tab_w);translate([x-tab_w/2,0,ft-0.01])cube([tab_w,0.01,tab_foot_h-1.5]);}
  for(sd=[-1,1])translate([x+sd*tab_w/2-(sd<0?fil_r:0),8.3,ft-0.01])difference(){cube([fil_r,up_t,fil_r]);translate([sd<0?0:fil_r,-0.1,fil_r])rotate([-90,0,0])cylinder(r=fil_r,h=up_t+0.2);}
 }
}
module joint_tab_cut(){for(x=joint_x){
 translate([x,8.3+up_t+0.1,deck_z+jz])rotate([90,0,0])cylinder(d=m6_clear,h=up_t+9);
 translate([x,8.3+up_t+0.1,deck_z+jz])rotate([90,0,0])cylinder(d=cb_d,h=cb_depth+0.1);
 translate([x-(tongue_w+slot_clear)/2,-0.1,deck_z+3.5-slot_clear/2])cube([tongue_w+slot_clear,tongue_depth+slot_clear,tongue_h+slot_clear]);
}}
wall_h=deck_z-floor_top;
// Deck screws: M2.5 inserts (4 x 3.5 OD) from the top of wall bosses, M2.5 x 7 down through the deck.
deck_screws=[[-41,39],[-10,40],[-96,144],[-55,144],[-15,144]]; deck_boss_d=8; deck_pilot=3.4; deck_pilot_depth=6; deck_hole_d=2.9;
module supports(){
 // Rear wall (open-top cable notch, no bridge), right wall behind the screen, left wall behind the Pi, corner post.
 difference(){
  translate([tray_x0,tray_d-3,floor_top-eps])cube([tray_x1-tray_x0,3,wall_h+eps]);
  translate([-90,tray_d-3.1,floor_top+4])cube([28,3.2,wall_h]);
  translate([-48,tray_d-3.1,floor_top+4])cube([26,3.2,wall_h]);
 }
 translate([tray_x1-2.5,rear_zone_y,floor_top-eps])cube([2.5,tray_d-rear_zone_y,wall_h+eps]);
 translate([tray_x0,92,floor_top-eps])cube([3,tray_d-92,wall_h+eps]);
 translate([pi_zone_x1,rear_zone_y,floor_top-eps])cube([6,6,wall_h+eps]);
 for(q=deck_screws)translate([q[0],q[1],floor_top-eps])cylinder(d=deck_boss_d,h=wall_h+eps);
}
function pi_hole(h)=[pi_x0+h[0],h[1]];
// Pi cooling (SCR5-E). Fan in front of the Hue cradle (Hue front Y 45.5), clear of the M6 tabs (Y <= 14.3).
fan_s=30; fan_t=7; fan_cx=-74; fan_cy=30; fan_hole_d=28; fan_pitch=24; fan_screw_d=3.4;
floor_vent_x=[for(i=[0:6])-92+6*i]; floor_vent_y=[30,75]; vent_w=3;   // 7 slots 3 x 45 between the Pi standoffs
wall_vent_y=[for(i=[0:11])40+8*i]; wall_vent_w=4; wall_vent_z=[floor_top+4.5,deck_z-4.5];  // 12 slots 4 x 20.3
module deck_cooling_cut(){
 translate([fan_cx,fan_cy,deck_z-0.1])cylinder(d=fan_hole_d,h=deck_t+0.2);
 for(sx=[-1,1],sy=[-1,1])translate([fan_cx+sx*fan_pitch/2,fan_cy+sy*fan_pitch/2,deck_z-0.1])cylinder(d=fan_screw_d,h=deck_t+0.2);
}
module floor_cooling_cut(){
 for(x=floor_vent_x)hull()for(y=floor_vent_y)translate([x,y,floor_z-0.1])cylinder(d=vent_w,h=floor_t+0.2);
 for(y=wall_vent_y)hull()for(z=wall_vent_z)translate([tray_x1-2.6,y,z])rotate([0,90,0])cylinder(d=wall_vent_w,h=2.7);
}
module fan(){translate([fan_cx-fan_s/2,fan_cy-fan_s/2,deck_top])cube([fan_s,fan_s,fan_t]);}
module floor_part(engraved=true){
 difference(){
  union(){
   footprint(floor_z,floor_t);
   supports();
   for(h=pi_holes)translate([pi_x0+h[0],h[1],floor_top-eps])cylinder(d=7,h=pi_standoff+eps);
  }
  for(h=pi_holes)translate([pi_x0+h[0],h[1],floor_top+0.01])cylinder(d=pi_pilot,h=pi_standoff+0.1);
  for(q=deck_screws)translate([q[0],q[1],deck_z-deck_pilot_depth])cylinder(d=deck_pilot,h=deck_pilot_depth+0.1);
  floor_cooling_cut();
  if(engraved)translate([-25,110,floor_top-0.6])linear_extrude(0.61)
   text("SCR5-E",size=4,font="Liberation Sans:style=Bold",halign="center");
 }
}
module deck_part(engraved=true){
 difference(){
  union(){
   footprint(deck_z,deck_t);
   joint_tabs();
   cradle();
  }
  joint_tab_cut();
  deck_cooling_cut();
  for(q=deck_screws)translate([q[0],q[1],deck_z-0.1])cylinder(d=deck_hole_d,h=deck_t+0.2);
  // ID on the deck underside (bed face), mirrored so it reads from below.
  if(engraved)translate([-25,100,deck_z-0.01])linear_extrude(0.61)mirror([1,0])
   text("SCR5-E",size=4,font="Liberation Sans:style=Bold",halign="center");
 }
}
module tray(engraved=true){floor_part(engraved);deck_part(engraved);}
module screen(){translate([scx,0,0]){
 translate([-glass_w/2,seat_y,centre_z-glass_h/2])cube([glass_w,total_depth,glass_h]);
 translate([pcb_reg_x-pcb_w/2,seat_y,centre_z+pcb_reg_z-pcb_h/2])cube([pcb_w,total_depth,pcb_h]);
}}
module pi(){translate([pi_x0,0,floor_top+pi_standoff])cube([pi_w,pi_d,pi_h]);}
module hue(){translate([hue_cx-hue_w/2,hue_cy-hue_d/2,deck_top])cube([hue_w,hue_d,hue_h]);}
// Screw head + driver envelope behind each frame screw, straight back to the tray rear.
module tools(){translate([scx,0,0])for(x=[-boss_x,boss_x],z=boss_z)translate([x,fy,z])rotate([-90,0,0])cylinder(d=tool_d,h=tray_d-fy+20);}
module joint_tools(){for(x=joint_x)translate([x,8.3+up_t,deck_z+jz])rotate([-90,0,0])cylinder(d=cb_d,h=tray_d);}

if(part=="plate")plate();
else if(part=="frame")frame();
else if(part=="tray")tray();
else if(part=="floor")floor_part();
else if(part=="deck")deck_part();
else if(part=="floor_deck")intersection(){floor_part();deck_part();}
else if(part=="tray_no_id")tray(false);
else if(part=="plate_tray")intersection(){plate();tray();}
else if(part=="plate_frame")intersection(){plate();frame();}
else if(part=="tray_frame")intersection(){tray();frame();}
else if(part=="tray_screen")intersection(){tray();screen();}
else if(part=="plate_screen")intersection(){plate();screen();}
else if(part=="tray_pi")intersection(){tray();pi();}
else if(part=="plate_pi")intersection(){plate();pi();}
else if(part=="tray_hue")intersection(){tray();hue();}
else if(part=="pi_hue")intersection(){pi();hue();}
else if(part=="screen_hue")intersection(){screen();hue();}
else if(part=="tray_tools")intersection(){tray();tools();}
else if(part=="tray_fan")intersection(){tray();fan();}
else if(part=="fan_hue")intersection(){fan();hue();}
else if(part=="plate_fan")intersection(){plate();fan();}
else if(part=="hue_tools")intersection(){hue();tools();}
else if(part=="tray_joint_tools")intersection(){tray();joint_tools();}
else {color("slategray")plate();color("orange")frame();color("silver")tray();
 %screen();%pi();%hue();%fan();}
