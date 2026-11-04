// SCR5-F, 2U (U4-U3) screen + Pi 4 + Hue Bridge + keystone unit. All dimensions mm. Claude, 2026-10-29.
// Brian: Pi lower left (USB/Ethernet through the plate), Hue on a shelf top left reaching behind the screen,
// keystone top left, screen on the right; M6 tray joints; U5 freed.
// Screen retention = SCR5-B (task 49) unchanged, translated by scx. Pi openings = HP4-M6-B unchanged, same X.
// Golden keystone and Hue cradle come from SCR5-F_hp4lib.scad (copy of HP4-M6-B.scad + overrides).
// Coordinates: X negative = left from the front, plate rear Y=0, Y+ into the rack, Z up from the U3 slot bottom.
// SCR5-D (Brian, 2026-10-29) = SCR5-C + Pi cooling: 30 x 30 x 7 5V fan on the deck over the Pi blowing down,
// vent slots in the floor under the Pi and in the right wall behind the screen.
// SCR5-E (Brian, 2026-10-29) = SCR5-D split for printing: floor+walls and deck print flat without supports and
// screw together with M2.5 inserts; deck front moved back to Y 36 so the DSI ribbon drop gap is ~10 mm.
// SCR5-F (Brian, 2026-10-29) = SCR5-E with rounded tray corners (r 6) against warping: floor and deck outline,
// walls follow the curves. Front corners at the plate stay square except the far left one (the joint tab needs
// the deck under it); a deck pad now carries the right tab to X -36. Front-right deck screw moved into the corner arc centre (-12, 42).
// SCR5-H9 (Brian 2026-11-03, tray sag): fan off the deck to the outer side, side walls make the front a box and key into
// the deck, floor sits on a plate ledge, Hue 10 forward, tray 10 shorter, tray 3 wider on the outer side.
// SCR5-H10 (Brian 2026-11-03): the X -88 M6 tab and boss from rev 8 blocked the keystone opening. Removed; third joint is now
// one M3 low on the outer side, plate boss into a pilaster on the floor part, so the tray is fastened top and bottom.
// SCR5-H11 (Brian 2026-11-03): fan mount is a separate add-on part that clips on the floor and deck edges; columns and deck notches gone.
// Plate ledge longer, with T-rails the floor slides under, so the floor is held to the ledge without screws.
// PROPOSED, UNVALIDATED: not printed. Fit, preload, shelf strength, ribbon reach, heat and access UNKNOWN.
include <SCR5-F_screen_config.scad>
use <SCR5-F_hp4lib.scad>
$fn=48;
part="assembled";
eps=0.02;
scx=33;                                   // screen centre X: pocket X -35.75..101.75
// Tray: floor (Pi) and shelf deck (Hue), joined to the plate at deck level by two HP4-style M6 joints.
floor_z=8.225; floor_t=3; floor_top=floor_z+floor_t;  // same floor height as HP4-M6-B, so its Pi openings line up
deck_z=40.5; deck_t=3; deck_top=deck_z+deck_t;       // >= 3 mm over the Pi envelope top (37.225)
tray_x0=-105; tray_x1=-6; tray_d=138; pi_zone_x1=-43; rear_zone_y=36;  // behind the screen the tray starts at Y 32
// Pi 4 exactly where HP4-M6-B has it: footprint X -102..-46, Y 0..85, rotated 270 (USB/Ethernet to the plate).
pi_x0=-102; pi_w=56; pi_d=85; pi_h=20; pi_standoff=6; pi_pilot=3.2;
pi_holes=[[3.5,81.5],[3.5,23.5],[52.5,81.5],[52.5,23.5]];
pi_ports=[[-93.0,26.8,15.0,17.5,1.0],[-75.0,26.8,15.0,17.5,1.0],[-56.3,25.6,17.5,15.0,1.0]];
// Hue Bridge v2 envelope in Brian's cradle (cradle posts 95 x 95; centre set in the lib overrides).
hue_cx=-54.4; hue_cy=93;  // rev 9: Hue back at 93, the fan left the deck
hue_w=90.7; hue_d=90.4; hue_h=30.7;
// M6 joints (HP4-M6-B geometry, base moved from the floor to the deck).
joint_x=[-71,-50];  // rev 10: rev 8's X -88 tab sat in the keystone opening
// rev 10 low joint: M3x3x5 insert in a plate boss, M3 x 10 countersunk from behind through the pilaster. Post flange ends X -111.12 (Y<6.2).
low_x=-106.5; low_z=25; low_boss_d=9; low_clip_x=-110.85; low_bore=4.2; low_deep=4; low_clear=3.4; low_seat_y=14; low_head_d=6.4; low_well_d=6.8; low_well_y=23.2;
pil_y0=8.3; pil_y1=17.3;
jz=24; tab_w=20; up_t=6; tab_foot_h=5; fil_r=4; cb_d=11.5; cb_depth=3.5;
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
 intersection(){translate([low_x,0,low_z])rotate([-90,0,0])cylinder(d=low_boss_d,h=8);translate([low_clip_x,-1,0])cube([20,10,60]);}
}
module joint_plate_cut(){
 for(x=joint_x)translate([x,-0.1,deck_z+jz])rotate([-90,0,0])cylinder(d=m6_pilot,h=8.2);
 translate([low_x,8-low_deep,low_z])rotate([-90,0,0])cylinder(d=low_bore,h=low_deep+0.1);
}
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
  text("SCR5-H11",size=id_size,halign="center",valign="center",font="Liberation Sans:style=Bold");
}}
// ID on the floor top behind the screen (the cradle covers the whole deck).
// Floor/deck footprint: full depth over the Pi zone, from Y 32 behind the screen (frame + screw heads end at Y 26.5).
corner_r=6;
module outline_sharp(){
 translate([tray_x0,0])square([pi_zone_x1-tray_x0,tray_d]);
 translate([pi_zone_x1-eps,rear_zone_y])square([tray_x1-pi_zone_x1+eps,tray_d-rear_zone_y]);
}
// Opening (erode, then round dilate) rounds every convex corner; the corner at (pi_zone_x1, 0) is put back square.
module outline(){
 offset(r=corner_r)offset(delta=-corner_r)outline_sharp();
 translate([pi_zone_x1-corner_r,0])square([corner_r,corner_r]);
 translate([tray_x0,0])square([corner_r,corner_r]);  // rev 9: outer wall butts the plate square
}
// Deck pad under the right M6 tab (tab + fillet reach X -36; the Pi-zone deck ends at X -44). Brian, 2026-10-29.
tab_pad_x1=-36; tab_pad_y=16;
module deck_tab_pad(){translate([0,0,deck_z])linear_extrude(deck_t)hull(){
 translate([pi_zone_x1-eps,0])square([1,tab_pad_y]);
 translate([tab_pad_x1-0.5,0])square([0.5,1]);
 translate([tab_pad_x1-3,tab_pad_y-3])circle(r=3);
}}
module ring(t){difference(){outline();offset(r=-t)outline();}}
module footprint(z,t){translate([0,0,z])linear_extrude(t)outline();}
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
// rev 9 walls. Outer: X -105..-102, plate to Y 63, window Y 63..86 for the Pi USB-C (centre Y ~74 from the published Pi layout, not measured).
// Inner: X -46..-43, plate to Y 88, open-top ribbon slot Y 29..37 from Z 21. Tongues on the wall tops key into deck-underside grooves.
wall_y0=8.3; wall_front_y1=63; wall_rear_y=86; inner_x=-46; inner_y1=88;
rib_slot_y=[29,37]; rib_slot_z=21;
key_inset=0.75; key_w=1.5; key_h=1.5; key_clear=0.25; groove_depth=1.8;
wall_keys=[[tray_x0,wall_y0,wall_front_y1],[inner_x,0,inner_y1]];
// Deck screws: M2.5 inserts (4 x 3.5 OD) from the top of wall bosses, M2.5 x 7 down through the deck.
// rev 8 (Brian slicer review 2026-11-01): 9 mm bosses overhung the floor edge at (-41,39) and the rear row (y 144+4.5 > 148);
// rear corner screws sat under the Hue cradle corner posts (posts start y 123.3 tray). Moved: front-left in from the step,
// rear middle 1 mm forward, rear corners forward of the posts.
deck_screws=[[-39,41],[-12,42],[-96,109],[-55,133],[-15,109],[-40,90],[-107.5,12.8]]; deck_boss_d=9; deck_pilot=4.2; deck_pilot_depth=5; deck_hole_d=3.4; // rev 7: M3x3x5 inserts, M3 countersunk
module supports(){
 // Rear wall (open-top cable notch, no bridge), right wall behind the screen, left wall behind the Pi, corner post.
 difference(){
  translate([0,0,floor_top-eps])linear_extrude(wall_h+eps)
   intersection(){ring(3);translate([tray_x0-1,tray_d-corner_r])square([tray_x1-tray_x0+2,corner_r+1]);}
  translate([-90,tray_d-3.1,floor_top+4])cube([28,3.2,wall_h]);
  translate([-48,tray_d-3.1,floor_top+4])cube([26,3.2,wall_h]);
 }
 translate([0,0,floor_top-eps])linear_extrude(wall_h+eps){
  intersection(){ring(2.5);translate([tray_x1-6,rear_zone_y+corner_r])square([7,tray_d-rear_zone_y-corner_r+1]);}
  intersection(){ring(3);translate([tray_x0-1,wall_rear_y])square([7,tray_d-wall_rear_y+1]);}
  translate([tray_x0,wall_y0])square([3,wall_front_y1-wall_y0]);   // rev 10: starts behind the plate's low boss
  translate([inner_x,0])square([3,inner_y1]);        // rev 9: inner wall along the Pi
 }
 translate([pi_zone_x1,rear_zone_y,floor_top-eps])cube([6,6,wall_h+eps]);
 for(q=deck_screws)translate([q[0],q[1],floor_top-eps])cylinder(d=deck_boss_d,h=wall_h+eps);
 for(k=wall_keys)translate([k[0]+key_inset,k[1],deck_z-eps])cube([key_w,k[2]-k[1],key_h+eps]);
 translate([-111.5,pil_y0,floor_z])cube([6.5+eps,pil_y1-pil_y0,deck_z-floor_z]);  // rev 10: pilaster, low joint and deck screw
}
function pi_hole(h)=[pi_x0+h[0],h[1]];
// Pi cooling. rev 9: 40 x 10 12 V fan moved off the deck, upright on the outer wall blowing +X across the Pi.
// rev 11: the fan screws into M3x3x5 inserts (4.2 x 4 deep) in an add-on mount, printed fan face down, no supports.
// Bottom lip hooks under the floor, keys in floor grooves locate it along the wall, top lips clip over the deck edge.
fan_s=40; fan_t=10; fan_cy=42; fan_cz=28.7; fan_hole_d=38; fan_pitch=32; fan_stand=5; col_w=9; col_top=49.2;
insert_bore=4.2; insert_deep=4;
grille_z0=12.7; grille_z1=39; grille_bars=[-9.5,0,9.5]; grille_bar_w=3;
fan_hole_y=[fan_cy-fan_pitch/2,fan_cy+fan_pitch/2];
mount_y0=20; mount_y1=64; mount_z0=5.2; mount_z1=49.2; mount_gap=0.1;
lip_y0=28; lip_x=5; lip_clear=0.1; top_lip_x=2.7; top_lip_t=2.4; top_lip_y=[[20,29],[55,64]];
key_y=[34,58]; key_w=4; key_up=1.4; key_groove_w=4.4; key_groove_up=1.5;
module fan_rotor(x,l){translate([x,fan_cy,fan_cz])rotate([0,90,0])cylinder(d=fan_hole_d,h=l);}
module fan_mount(){difference(){
 union(){
  translate([tray_x0-fan_stand,mount_y0,mount_z0])cube([fan_stand-mount_gap,mount_y1-mount_y0,mount_z1-mount_z0]);
  translate([tray_x0-mount_gap-eps,lip_y0,mount_z0])cube([lip_x+mount_gap+eps,mount_y1-lip_y0,floor_z-lip_clear-mount_z0]);
  for(y=key_y)translate([tray_x0-mount_gap-eps,y-key_w/2,floor_z-lip_clear-eps])cube([lip_x+mount_gap+eps,key_w,key_up+lip_clear+eps]);
  for(s=top_lip_y)translate([tray_x0-mount_gap-eps,s[0],deck_top+lip_clear])cube([top_lip_x+eps,s[1]-s[0],top_lip_t]);
 }
 fan_rotor(tray_x0-fan_stand-0.1,fan_stand+0.1-mount_gap+eps);
 for(y=fan_hole_y,z=[fan_cz-fan_pitch/2,fan_cz+fan_pitch/2])translate([tray_x0-fan_stand-0.1,y,z])rotate([0,90,0])cylinder(d=insert_bore,h=insert_deep+0.1);
 translate([tray_x0-fan_stand-0.01,fan_cy,mount_z0+0.6])rotate([90,0,90])linear_extrude(0.5)text("SCR5-H11",size=2.4,halign="center",font="Liberation Sans:style=Bold");
}}
module fan_mount_grooves(){for(y=key_y)translate([tray_x0-0.1,y-key_groove_w/2,floor_z-0.1])cube([lip_x+0.3,key_groove_w,key_groove_up+0.1]);}
// rev 11: open-front slots for the plate's T-rails; the floor slides under the rail tops as the tray goes on.
rail_x=[-88,-74,-60]; rail_y=24; rail_stem=3; rail_slot=3.6;
module rail_slots(){for(x=rail_x)translate([x-rail_slot/2,-0.1,floor_z-0.1])cube([rail_slot,rail_y+0.4,floor_t+0.2]);}
module fan_grille_cut(){difference(){
 intersection(){fan_rotor(tray_x0-0.1,3.2);translate([tray_x0-0.2,fan_cy-20,grille_z0])cube([3.4,40,grille_z1-grille_z0]);}
 for(d=grille_bars)translate([tray_x0-0.3,fan_cy+d-grille_bar_w/2,0])cube([3.6,grille_bar_w,60]);
}}
// rev 9: pad outside the outer wall under the front deck screw.
module screw_pad(z,t){translate([0,0,z])linear_extrude(t)hull(){translate([-107.5,12.8])circle(d=deck_boss_d);translate([tray_x0,pil_y0])square([0.5,pil_y1-pil_y0]);}}
floor_vent_x=[for(i=[0:6])-92+6*i]; floor_vent_y=[30,75]; vent_w=3;   // 7 slots 3 x 45 between the Pi standoffs
wall_vent_y=[for(i=[0:11])46+8*i]; wall_vent_w=4; wall_vent_z=[floor_top+4.5,deck_z-4.5];  // 12 slots 4 x 20.3
module floor_cooling_cut(){
 for(x=floor_vent_x)hull()for(y=floor_vent_y)translate([x,y,floor_z-0.1])cylinder(d=vent_w,h=floor_t+0.2);
 // SCR5-H rev 4 (Brian 2026-10-31): one 25 x 10 cable slot low at the rear of the right wall; vents behind Y 106 dropped.
 for(y=wall_vent_y)if(y<96)hull()for(z=wall_vent_z)translate([tray_x1-2.6,y,z])rotate([0,90,0])cylinder(d=wall_vent_w,h=2.7);
 hull()for(y=[107,127])translate([tray_x1-2.6,y,floor_top+8])rotate([0,90,0])cylinder(d=10,h=2.7,$fn=40);
}
module fan(){translate([tray_x0-fan_stand-fan_t,fan_cy-fan_s/2,fan_cz-fan_s/2])cube([fan_t,fan_s,fan_s]);}
module floor_part(engraved=true){
 difference(){
  union(){
   footprint(floor_z,floor_t);
   screw_pad(floor_z,floor_t);
   supports();
   for(h=pi_holes)translate([pi_x0+h[0],h[1],floor_top-eps])cylinder(d=7,h=pi_standoff+eps);
  }
  for(h=pi_holes)translate([pi_x0+h[0],h[1],floor_top+0.01])cylinder(d=pi_pilot,h=pi_standoff+0.1);
  for(q=deck_screws)translate([q[0],q[1],deck_z-deck_pilot_depth])cylinder(d=deck_pilot,h=deck_pilot_depth+0.1);
  floor_cooling_cut();
  fan_grille_cut();
  fan_mount_grooves();
  rail_slots();
  // rev 10: low joint screw through the pilaster, head well reaches back along the wall so the screw can be started with the fan mount off.
  translate([low_x,pil_y0-0.1,low_z])rotate([-90,0,0])cylinder(d=low_clear,h=low_seat_y-pil_y0+0.2);
  translate([low_x,low_seat_y,low_z])rotate([-90,0,0])cylinder(d1=low_clear,d2=low_head_d,h=1.5,$fn=32);
  translate([low_x,low_seat_y+1.49,low_z])rotate([-90,0,0])cylinder(d=low_well_d,h=low_well_y-low_seat_y-1.49,$fn=32);
  translate([inner_x-0.1,rib_slot_y[0],rib_slot_z])cube([3.2,rib_slot_y[1]-rib_slot_y[0],wall_h+5]);
  if(engraved)translate([-25,110,floor_top-0.6])linear_extrude(0.61)
   text("SCR5-H11",size=4,font="Liberation Sans:style=Bold",halign="center");
 }
}
module deck_part(engraved=true){
 difference(){
  union(){
   footprint(deck_z,deck_t);
   screw_pad(deck_z,deck_t);
   deck_tab_pad();
   joint_tabs();
   intersection(){cradle();translate([-200,-50,0])cube([400,50+tray_d,200]);}  // rev 6: cradle clipped at the deck rear edge
  }
  joint_tab_cut();
  // rev 9: grooves for the wall tongues.
  for(k=wall_keys)translate([k[0]+key_inset-key_clear,k[1]-0.1,deck_z-0.1])cube([key_w+2*key_clear,k[2]-k[1]+0.4,groove_depth+0.1]);
  for(q=deck_screws)translate([q[0],q[1],deck_z-0.1])cylinder(d=deck_hole_d,h=deck_t+0.2);
  // rev 6: rear screws now sit under the Hue -> 90 deg countersink for flush M2.5 flat heads
  for(q=deck_screws)translate([q[0],q[1],deck_top-1.5])cylinder(d1=3.4,d2=6.4,h=1.51,$fn=32);
  // rev 8: the cradle base slab (~1.1 mm) covered the countersinks; open a 6.8 mm head/driver well straight up through it.
  for(q=deck_screws)translate([q[0],q[1],deck_top-0.01])cylinder(d=6.8,h=20,$fn=32);
  // ID on the deck underside (bed face), mirrored so it reads from below.
  if(engraved)translate([-25,100,deck_z-0.01])linear_extrude(0.61)mirror([1,0])
   text("SCR5-H11",size=4,font="Liberation Sans:style=Bold",halign="center");
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

