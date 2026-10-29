// SCR5-B, plate-anchored removable rear clamp. All dimensions mm.
// Vendor nominal; printed fit / preload / retention / strength UNKNOWN.
include <SCR5-B_config.scad>
$fn=48;
part="assembled";
eps=0.02;
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
 // Square seating rectangle plus outward overcuts: never an inward fillet.
 translate([0,centre_z])square([2*cx,2*ch],center=true);
 for(x=[-cx,cx],z=[centre_z-ch,centre_z+ch])translate([x,z])circle(r=pocket_relief_r);
}
module mouth(y,side,r,w,h,corner){
 // Eight-segment quarter-circle flare rounds the material at an opening's
 // front/rear mouth. This is source geometry, not an STL edge repair.
 // Loft one convex polyhedron instead of unioning dozens of thin hulls.
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
 // Accessible frame mouths and the pocket's rear edge are relieved on both
 // sides of the common Y=20 plane; the blind notch start is also rounded.
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
module plate(){difference(){union(){
 xz(-plate_t,plate_t)translate([0,centre_z])rr(plate_w,plate_h,plate_r);
 xz(0,pocket_depth)difference(){
  translate([0,centre_z])square([2*(cx+pocket_wall),2*(ch+pocket_wall)],center=true);
  cavity();
 }
 bosses();
 }
 xz(-plate_t-eps,plate_t+2*eps){aperture();rack_slots();}
 for(x=[-boss_x,boss_x],z=boss_z){
  xz(boss_end_y-insert_seat_depth,insert_seat_depth+eps)translate([x,z])circle(d=insert_pilot);
  translate([x,boss_end_y-insert_leadin,z])rotate([-90,0,0])cylinder(h=insert_leadin+eps,d1=insert_pilot,d2=insert_pilot+.4);
 }
 access();
}}
module pads(){for(x=[-pad_x,pad_x],z=[centre_z-pad_z_offset,centre_z+pad_z_offset])
 xz(pad_front_y,frame_front_y-pad_front_y+eps)translate([x,z])rr(pad_w,pad_h,pad_r);
}
module frame(engraved=true){difference(){union(){
 xz(frame_front_y,frame_t)difference(){
  translate([0,centre_z])rr(frame_outer_w,frame_outer_h,frame_outer_r);
  translate([0,centre_z])rr(frame_inner_w,frame_inner_h,frame_inner_r);
 }
 pads();
 }
 for(x=[-boss_x,boss_x],z=boss_z)xz(frame_front_y-eps,frame_t+2*eps)translate([x,z])circle(d=screw_clearance);
 access();
 if(engraved)xz(fy-id_depth,id_depth+eps)translate([id_x,id_z])rotate(5)offset(r=.08)
  text("SCR5-B",size=id_size,halign="center",valign="center",font="Liberation Sans:style=Bold");
}}
module screen(){ // Conservative union-of-outlines box, not a component model.
 translate([-glass_w/2,seat_y,centre_z-glass_h/2])cube([glass_w,total_depth,glass_h]);
 translate([pcb_reg_x-pcb_w/2,seat_y,centre_z+pcb_reg_z-pcb_h/2])cube([pcb_w,total_depth,pcb_h]);
}
module intended_contacts(){
 // Boss/wall rear Y=20 seats are boundary contacts; pads alone interfere.
 intersection(){pads();screen();}
}
if(part=="plate")plate();
else if(part=="frame")frame();
else if(part=="no_id")frame(false);
else if(part=="screen")screen();
else if(part=="plate_frame_intersection")intersection(){plate();frame();}
else if(part=="plate_screen_intersection")intersection(){plate();screen();}
else if(part=="frame_screen_intersection")intersection(){frame();screen();}
else if(part=="unintended")difference(){intersection(){frame();screen();}intended_contacts();}
else if(part=="intended")intended_contacts();
else if(part=="seating_clearance")intersection(){
 plate();
 union(){
  translate([-glass_w/2-glass_clear_left,.01,centre_z-glass_h/2-glass_clear_bottom])cube([glass_w+glass_clear_left+glass_clear_right,30,glass_h+glass_clear_top+glass_clear_bottom]);
  translate([pcb_reg_x-pcb_w/2-pcb_clear_x,.01,centre_z+pcb_reg_z-pcb_h/2-pcb_clear_z])cube([pcb_w+2*pcb_clear_x,30,pcb_h+2*pcb_clear_z]);
 }
}
else {color("slategray")plate();color("orange")frame();color([.1,.5,.3,.4])screen();}
