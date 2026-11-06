// DRAFT 2 (no ID yet): rack top for a 200 mm exhaust fan, option B (Brian 2026-11-05).
// The fan sits fully recessed in the top's own 35 mm height (Brian: no fan body sticking out of the top):
// new front + rear top edges are hollowed on the inside into a cavity, the fan rests on ledges in them,
// and a 3 mm grille, flush with the rail tops, clamps it down. No panel: the grille is the top surface.
// Stock side rails and handles stay.
// Frame = rack frame: X centred, Y 0 front .. 240 rear, Z 0 = bottom of slot 9, post tops Z 400.05.
// Joint values (plug, tongue, cross-holes) are read from the creator's meshes (docs/devices/lab-rax-top.md),
// not measured, and not copied: they are redrawn here as plain boxes. Fit and strength UNKNOWN.
include <workshop.scad>
include <BOSL2/std.scad>
part="assembly";         // edge_front | edge_rear | grille | fan | assembly
$fn=64;

// --- stock interfaces (source values) ---
z_top=400.05;            // post tops / bottom of the edge body / top of slot 1 (U9)
z_lid=435.05;            // top of rails and edges
x_edge=141.12;           // edge half length (282.25 long)
plug_x=[127.12,133.98];  // plug + tongue column, each end
plug_y=[11.15,35]; plug_z=[380.2,z_top];      // drops into the post top pocket (post solid Y 0..11)
tongue_y=[35,54.85]; tongue_z=[z_top,423.9];  // slides into the side rail end pocket (Y 35..55, Z 400..424)
xhole_d=6.4; plug_hole=[22.5,390.2]; tongue_hole=[45,416];  // cross-holes along X, centres approximate (UNKNOWN)
rail_in=110.98;          // inner face of the stock side rails (and their lip over the old panel seat)

// --- new design values (draft) ---
fan=[200,200,30]; fan_c=[0,120]; fan_fit=0.5; // CT200 frame from listings (UNKNOWN); 0.5 room each side
ledge_t=2;               // fan rests on ledges in the edges: Z 400.05..402.05
grille_t=3;              // grille Z 432.05..435.05, flush with the rail tops; it rests on the fan top
open_d=192;              // air opening under the blades (ledges cut back to it) and in the grille
front_wall=3;            // outer wall of each edge at the grille seat
grille_fit=0.3;          // grille to edge recess, each side
grille_x=rail_in-0.5;    // grille half width: 0.5 clear of the rail lip
m3_y=11; m3_x=[-95,-40,40,95];                // grille screws, M3 countersunk into M3 inserts in the edge walls
jack_x=106; jack_z=416; jack_d=8;             // DC panel jack in the rear edge's back face (model UNKNOWN), beside the fan
cav_x=fan[0]/2+fan_fit;  // cavity half width
cav_y=fan_c[1]-fan[1]/2-fan_fit;              // cavity front face (Y 19.5)
z_fan=z_top+ledge_t; z_grille=z_lid-grille_t;

module box(a,b){translate(a)cube(b-a);}

module edge(jack=false){
  difference(){
    union(){
      translate([-x_edge,0,z_top]) cuboid([2*x_edge,35,z_lid-z_top],rounding=2,edges=[TOP+FRONT],anchor=FRONT+BOTTOM+LEFT);
      for(s=[-1,1]) mirror([s<0?1:0,0,0]){
        box([plug_x[0],plug_y[0],plug_z[0]],[plug_x[1],plug_y[1],plug_z[1]+0.01]);
        box([plug_x[0],tongue_y[0]-0.01,tongue_z[0]],[plug_x[1],tongue_y[1],tongue_z[1]]);
      }
    }
    // fan cavity, open to the inside, ledge left underneath
    box([-cav_x,cav_y,z_fan],[cav_x,36,z_lid+1]);
    // ledge cut back to the air opening
    translate([fan_c[0],fan_c[1],z_top-1]) cylinder(d=open_d,h=ledge_t+2);
    // grille seat
    box([-grille_x-grille_fit,front_wall,z_grille],[grille_x+grille_fit,36,z_lid+1]);
    // cross-holes
    for(s=[-1,1]) for(h=[plug_hole,tongue_hole]) translate([s*(plug_x[0]+plug_x[1])/2,h[0],h[1]]) rotate([0,90,0]) cylinder(d=xhole_d,h=10,center=true);
    // M3 inserts for the grille screws
    for(x=m3_x) translate([x,m3_y,z_grille]) mirror([0,0,1]) ws_insert_bore(ws_insert_m3,5);
    // DC jack (rear edge only): hole through the back face, pocket beside the fan, open down into the rack
    if(jack){ translate([jack_x,-1,jack_z]) rotate([-90,0,0]) cylinder(d=jack_d,h=front_wall+2);
              box([jack_x-6,front_wall,z_top-1],[jack_x+4.5,36,jack_z+8]); }
  }
}
module edge_rear(){ translate([0,240,0]) rotate([0,0,180]) edge(jack=true); }

module grille(){
  y0=front_wall+grille_fit; y1=240-front_wall-grille_fit;
  difference(){
    translate([-grille_x,y0,z_grille]) cuboid([2*grille_x,y1-y0,grille_t],rounding=2,edges="Z",anchor=FRONT+BOTTOM+LEFT);
    difference(){
      translate([fan_c[0],fan_c[1],z_grille-1]) cylinder(d=open_d,h=grille_t+2);
      for(r=[30,55,80]) translate([fan_c[0],fan_c[1],z_grille-1]) difference(){ cylinder(r=r+1.5,h=grille_t+2); cylinder(r=r-1.5,h=grille_t+2); }
      for(a=[0:45:135]) translate([fan_c[0],fan_c[1],z_grille+grille_t/2]) rotate([0,0,a]) cube([open_d,3,grille_t+2],center=true);
      translate([fan_c[0],fan_c[1],z_grille-1]) cylinder(r=14,h=grille_t+2);
    }
    for(x=m3_x,y=[m3_y,240-m3_y]) translate([x,y,z_grille-0.01]){ cylinder(d=3.4,h=grille_t+1); translate([0,0,grille_t-1.7+0.02]) cylinder(d1=3.4,d2=6.6,h=1.7); }
  }
}

module fan_dummy(){ translate([fan_c[0],fan_c[1],z_fan]) difference(){ translate([0,0,fan[2]/2]) cuboid(fan,rounding=8,edges="Z"); cylinder(d=open_d-4,h=3*fan[2],center=true);} }

if(part=="edge_front") edge();
if(part=="edge_rear") edge_rear();
if(part=="grille") grille();
if(part=="fan") fan_dummy();
if(part=="assembly"){ edge(); edge_rear(); grille(); %fan_dummy(); }
