// DRAFT: 1U faceplate, 8 golden keystones, stiffened (Brian 2026-11-12: printed 10-keystone panel too flimsy;
// only 8 keystones needed; 12 mm frame OK).
// Base = outputs/Faceplate_1U_10_Keystones_2026-10-22 (same plate and golden blocks; outer keystones about where
// they were, 27.5 pitch, so the webs between blocks grow from 0.5 to 6.5 mm).
// Added: a rear stiffening frame behind the plate, rib_d deep, X +-rib_x. It is a solid slab with one
// pocket per keystone (+-9.9 = the golden block's own deep side walls, Z = block window), so every
// keystone keeps its original shape and the jack opening behind it stays open.
// Fit and strength UNKNOWN. Released as KSP-A 2026-11-12 (unprinted).
include <workshop.scad>

part="panel";           // panel | cuts (check only: one solid per keystone pocket)
tag="KSP-A";             // ID, engraved 0.6 deep in the rear face of the bottom frame bar, centre
u=1;
ks_n=8; ks_pitch=27.5;  // 10 at 21.5 before
ks=[for(i=[0:ks_n-1])(i-(ks_n-1)/2)*ks_pitch];  // +-13.75, 41.25, 68.75, 96.25
rib_d=12;               // frame depth behind the plate (was 0; golden blocks reach about 6.3)
rib_x=110.1;            // frame half-width: 1 mm clear of the post flange edge at X 111.12
pocket_w=19.8;          // block's deep walls are X +-9.9; nothing new inside them
ks_z0=ws_plate_center(u)-15; ks_z1=ws_plate_center(u)+18.5;   // block window (unchanged)
ch=1;                   // rear edge chamfer

module pockets(){for(x=ks)translate([x-pocket_w/2,-0.02,ks_z0])cube([pocket_w,rib_d+1,ks_z1-ks_z0]);}

module frame(){
 difference(){
  // slab behind the plate, inside the plate outline, rear edges chamfered
  hull(){
   translate([-rib_x,-0.01,ws_plate_bottom()])cube([2*rib_x,rib_d-ch+0.01,ws_plate_h(u)]);
   translate([-rib_x+ch,0,ws_plate_bottom()+ch])cube([2*(rib_x-ch),rib_d,ws_plate_h(u)-2*ch]);
  }
  pockets();
  translate([0,rib_d-0.6,(ws_plate_bottom()+ks_z0)/2])rotate([90,0,180])linear_extrude(1)
   text(tag,size=4,font="Liberation Sans:style=Bold",halign="center",valign="center");
 }
}

if(part=="panel"){ ws_plate(u,ks); frame(); }
if(part=="cuts") pockets();
