// CBL-A (2026-10-31): 1U rear cable lane module. Bolts to a REAR post (2 x M6 x 8 into the M6 inserts, from the trough side).
// Frame: X centred on the rack, Y=0 is the rear face of the rear post flange (+Y points away from the rack), Z=0 slot bottom.
// u = |X|; geometry is drawn for the right post (s=+1). Stack 1 module per U; 0.6 mm gaps between modules.
// Cross-section: plate on the flange, inner wall (rack side, with a cable window), outer wall, and a 45 deg hook lip on the outer
// wall (prints without supports with the plate on the bed). Lip is limited to the middle of the U so the screw heads stay reachable.
// Fit, cable capacity, retention and strength are UNKNOWN. Not printed.
s=1;                       // +1 right post, -1 left post
part="A";                  // set by -D; the other parts (src/CBL-BCDE.scad) include this file
uz=0;                      // U offset for viewing (the part is drawn in the U1 frame)
tag="CBL-A";               // test print ID (modelled into the outer wall)
label="";                  // optional second word ("DATA" / "PWR")
hx=118.2625; mid=22.225; hole_dz=15.902; mh=43.8;
half=14; u0=hx-half; u1=hx+half;     // 28 wide plate, centred on the hole column (as the creator's guide footprint)
t_pl=4; wall=2; depth=26;             // depth 26 stays inside the 30 mm wall-mount standoffs
m6_clear=6.6;
lip_len=9.26; lip_z=10;               // hook lip tip 9.26 over from the outer wall, Z mid +/- 10 (screw heads start at +/-10.15)
win_z=10; win_y1=17;                  // inner-wall cable window, Z mid +/- 10, Y 6..17 (wall stays whole above it, it carries the strap slot)
strap_w=16; strap_t=2.6; strap_y=19.5; // Velcro strap slot through both walls and the lip, Z mid +/- 8, crosses the trough at Y 19.5..22.1
rr=0.9;                               // rounded outside corners (max for a 2 mm wall)
$fn=48;

module section_outer(){
  offset(r=rr)offset(delta=-rr)union(){
    translate([u0,0])square([u1-u0,t_pl]);
    translate([u0,0])square([wall,depth]);
    translate([u1-wall,0])square([wall,depth]);
  }
}
module lip(){ // 45 deg underside, flat top at Y=depth
  polygon([[u1-wall,depth-lip_len],[u1-wall-lip_len,depth],[u1-wall,depth]]);
}
module body(){
  z0=mid-mh/2;
  translate([0,0,z0])linear_extrude(mh)section_outer();
  translate([0,0,mid-lip_z])linear_extrude(2*lip_z)lip();
}
module label_cut(){
  // engraved 0.6 deep into the outer face of the outer wall, reads upright when viewed from outside
  translate([u1-0.6,11,mid])rotate([90,0,90])linear_extrude(1)
    text(label==""?tag:str(tag," ",label),size=2.6,font="Liberation Sans:style=Bold",halign="center",valign="center");
}
module module_r(){
  difference(){
    body();
    for(dz=[-hole_dz,hole_dz])translate([hx,-1,mid+dz])rotate([-90,0,0])cylinder(d=m6_clear,h=t_pl+2);
    translate([u0-1,t_pl+2,mid-win_z])cube([wall+2,win_y1-t_pl-2,2*win_z]);   // cable window in the inner wall
    translate([u0-1,strap_y,mid-strap_w/2])cube([u1-u0+2,strap_t,strap_w]);    // strap slot, wall to wall
    label_cut();
  }
}
if(part=="A")translate([0,0,uz*44.45])scale([s,1,1])module_r();
