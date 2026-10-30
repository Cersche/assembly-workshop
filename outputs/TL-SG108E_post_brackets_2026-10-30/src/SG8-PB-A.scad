// SG8-PB-A (2026-10-30): post brackets that hang the printed SG8-M6-D tray from the back of the front rack posts.
// Frame = faceplate/slot frame: X centred, plate back Y=0, Z=0 slot bottom, U centre Z=22.225.
// Post (Lab Rax 1U, measured from the source mesh): front flange Y 0..6 for |X| >= 111.1, middle hole (unused by the
// faceplate) Ø7.6 at X ±118.2625, Z 22.225; side flange outboard at |X| 134.1..139.6. M6 insert assumed in that hole.
// Tray (D, unchanged): uprights 16 x 6 at X -92.5 / 62.5, Y 8.3..14.3, hole Ø6.6 at Z 38.425 (head counterbore at the rear);
// sleeve wall + lip top Z 34.85 under each upright. B plate bosses must be cut off: this block takes their place.
// Block: Y 0.3..8.0, Z 35.15..44.2, 5.0 mm pilot (M6 threads straight into it; no room for an insert above the lip).
// Post pad: Y 6..12, M6 x 8 from behind, 11.5 counterbore leaving 2.5 under the head (~5.5 into the post hole).
// Fit, strength, insert presence in the middle hole: UNKNOWN.
part="left";            // left | right | both
id="SG8-PB-A";
hs_z=38.425; hole_z=22.225; post_x=118.2625; post_in=111.1;
y0=0.3; yb=8.0; zb=35.15; ztop=44.2; pad_y=[6.2,12]; pad_z=[11,33.5];
web_in=104;             // inner edge of the post web (tray is |X| <= 102 / 72)
pilot=5.0; clear=6.6; cb=11.5; web=2.5;
$fn=48;
module pad(s){ // s=+1 right, -1 left
 difference(){
  translate([s>0?web_in:-125,pad_y[0],pad_z[0]])cube([125-web_in,pad_y[1]-pad_y[0],pad_z[1]-pad_z[0]]);
  translate([s*post_x,pad_y[0]-0.1,hole_z])rotate([-90,0,0])cylinder(d=clear,h=10);
  translate([s*post_x,pad_y[0]+web,hole_z])rotate([-90,0,0])cylinder(d=cb,h=10);
  translate([s*post_x,pad_y[1]-0.6,pad_z[0]+3.2])rotate([-90,0,0])linear_extrude(1)mirror([s>0?0:1,0,0])
   text(id,size=3,font="Liberation Sans:style=Bold",halign="center",valign="center");
 }}
module web(s,z0){translate([s>0?web_in:-post_in+0.3,y0,z0])cube([post_in-0.3-web_in,pad_y[1]-y0,ztop-z0]);}
module block(x0,x1){difference(){translate([x0,y0,zb])cube([x1-x0,yb-y0,ztop-zb]);}}
module bore(x){translate([x,y0-0.1,hs_z])rotate([-90,0,0])cylinder(d=pilot,h=10);}
module left(){difference(){union(){pad(-1);web(-1,pad_z[0]);block(-post_in+0.3,-84.5);}bore(-92.5);}}
// Right: keystone block on the plate back sits at X 78..98, Y 0..8, Z 10.3..38.2, so the right bracket is a frame around it:
// low beam under it (Z 0.6..6.6), column between tray and keystone (X 72.4..77.6), top beam above it (Z 41..44.2).
module right(){difference(){union(){pad(1);web(1,0.6);block(54.5,77.6);
  translate([72.4,y0,0.6])cube([77.6-72.4,yb-y0,ztop-0.6]);
  translate([72.4,y0,0.6])cube([web_in-72.4+0.01,pad_y[1]-y0,6]);
  translate([72.4,y0,41])cube([web_in-72.4+0.01,pad_y[1]-y0,ztop-41]);}bore(62.5);}}
if(part=="left")left(); else if(part=="right")right(); else {left();right();}
