// DRAFT (no ID yet): rack top for a 200 mm exhaust fan, option B (Brian 2026-11-05).
// New front + rear top edges with a square top (flat top grows from ~175 to 240 deep), a new panel that
// holds the fan, and a grille that clamps the fan down. Stock side rails and handles stay.
// Frame = rack frame: X centred, Y 0 front .. 240 rear, Z 0 = bottom of slot 9, post tops Z 400.05.
// Joint values (plug, tongue, cross-holes, ledges) are read from the creator's meshes (docs/devices/lab-rax-top.md),
// not measured, and not copied: they are redrawn here as plain boxes. Fit and strength UNKNOWN.
include <workshop.scad>
include <BOSL2/std.scad>
part="assembly";         // edge_front | edge_rear | panel | grille | fan | assembly
$fn=64;

// --- stock interfaces (source values) ---
z_top=400.05;            // post tops / bottom of the edge body
z_lid=435.05;            // top of rails and edges
x_edge=141.12;           // edge half length (282.25 long)
plug_x=[127.12,133.98];  // plug + tongue column, each end
plug_y=[11.15,35]; plug_z=[380.2,z_top];      // drops into the post top pocket (post solid Y 0..11)
tongue_y=[35,54.85]; tongue_z=[z_top,423.9];  // slides into the side rail end pocket (Y 35..55, Z 400..424)
xhole_d=6.4; plug_hole=[22.5,390.2]; tongue_hole=[45,416];  // cross-holes along X, centres approximate (UNKNOWN)
pnl_x=114.03; pnl_z=[430.05,433.05];          // stock panel half width and height in the rail ledge
handle_in=113.29;        // inner face of the stock handles

// --- new design values (draft) ---
fit=0.3;                 // panel to edge recess, each side
pnl_y=[14,226];          // new panel reaches over both new edges
seat_y=22;               // edge recess floor supports the panel from pnl_y[0] to here, then chamfers away for air
fan=[200,200,30]; fan_c=[0,120]; fan_fit=0.5;
open_d=192;              // air opening in the panel under the blades
rim_w=4; rim_h=6;        // locating rim around the fan on the panel top
post_x=105.5;  // rail lip over the panel starts X 110.98: post edge 110.25 post_y=[70,170]; post_d=9.5;    // grille posts beside the fan, M3 insert in the top
grille_t=3; grille_gap=0.3;                   // grille rests on the posts 0.3 above the fan top
m3_y=18; m3_x=[-60,60];  // panel screws into M3 inserts in the edge recess floor (front and rear)
jack_x=80; jack_z=415; jack_d=8; jack_wall=3;  // DC panel jack in the rear edge's back face (jack model UNKNOWN)
cable=[90,212,14,8];     // cable hole x,y,w,h under the fan's rear right corner

module box(a,b){translate(a)cube(b-a);}

module edge(jack=false){
  difference(){
    union(){
      // square body, 2 mm round along the outside top edge
      translate([-x_edge,0,z_top]) cuboid([2*x_edge,35,z_lid-z_top],rounding=2,edges=[TOP+FRONT],anchor=FRONT+BOTTOM+LEFT);
      for(s=[-1,1]) mirror([s<0?1:0,0,0]){
        box([plug_x[0],plug_y[0],plug_z[0]],[plug_x[1],plug_y[1],plug_z[1]+0.01]);
        box([plug_x[0],tongue_y[0]-0.01,tongue_z[0]],[plug_x[1],tongue_y[1],tongue_z[1]]);
      }
    }
    // panel recess, open to the inside
    box([-pnl_x-fit,pnl_y[0]-fit,pnl_z[0]],[pnl_x+fit,36,z_lid+1]);
    // air chamfer under the panel, inside the fan circle
    translate([0,0,0]) rotate([0,90,0]) linear_extrude(height=2*(plug_x[0]-1),center=true)
      polygon([[-pnl_z[0]-0.01,seat_y],[-pnl_z[0]-0.01,36],[-(pnl_z[0]-(36-seat_y)),36]]);
    // cross-holes
    for(s=[-1,1]) for(h=[plug_hole,tongue_hole]) translate([s*(plug_x[0]+plug_x[1])/2,h[0],h[1]]) rotate([0,90,0]) cylinder(d=xhole_d,h=10,center=true);
    // M3 inserts for the panel screws
    for(x=m3_x) translate([x,m3_y,pnl_z[0]]) mirror([0,0,1]) ws_insert_bore(ws_insert_m3,5);
    // DC jack (rear edge only): hole through the back face, pocket open to the inside below the panel
    if(jack){ translate([jack_x,-1,jack_z]) rotate([-90,0,0]) cylinder(d=jack_d,h=jack_wall+2);
              box([jack_x-9,jack_wall,jack_z-9],[jack_x+9,36,jack_z+9]); }
  }
}
module edge_rear(){ translate([0,240,0]) rotate([0,0,180]) edge(jack=true); }

module panel(){
  difference(){
    union(){
      box([-pnl_x,pnl_y[0],pnl_z[0]],[pnl_x,pnl_y[1],pnl_z[1]]);
      // locating rim, stays inside the handles
      difference(){
        translate([fan_c[0],fan_c[1],pnl_z[1]+rim_h/2]) cube([fan[0]+2*fan_fit+2*rim_w,fan[1]+2*fan_fit+2*rim_w,rim_h],center=true);
        translate([fan_c[0],fan_c[1],pnl_z[1]+rim_h/2]) cube([fan[0]+2*fan_fit,fan[1]+2*fan_fit,rim_h+1],center=true);
      }
      for(s=[-1,1],y=post_y) translate([s*post_x,y,pnl_z[1]]) cylinder(d=post_d,h=fan[2]+grille_gap);
    }
    translate([fan_c[0],fan_c[1],pnl_z[0]-1]) cylinder(d=open_d,h=10);
    box([cable[0]-cable[2]/2,cable[1]-cable[3]/2,pnl_z[0]-1],[cable[0]+cable[2]/2,cable[1]+cable[3]/2,pnl_z[1]+1]);
    for(x=m3_x,y=[m3_y,240-m3_y]) translate([x,y,pnl_z[0]-0.01]){ cylinder(d=3.4,h=5); translate([0,0,3-1.7+0.01]) cylinder(d1=3.4,d2=6.6,h=1.7); }
    for(s=[-1,1],y=post_y) translate([s*post_x,y,pnl_z[1]+fan[2]+grille_gap]) mirror([0,0,1]) ws_insert_bore(ws_insert_m3,5);
  }
}

module grille(){
  z0=pnl_z[1]+fan[2]+grille_gap;
  difference(){
    translate([0,fan_c[1],z0]) cuboid([2*(post_x+post_d/2),fan[1]+2*fan_fit+2*rim_w,grille_t],rounding=3,edges="Z",anchor=BOTTOM);
    difference(){
      translate([0,fan_c[1],z0-1]) cylinder(d=open_d,h=grille_t+2);
      // rings and spokes
      for(r=[30,55,80]) translate([0,fan_c[1],z0-1]) difference(){ cylinder(r=r+1.5,h=grille_t+2); cylinder(r=r-1.5,h=grille_t+2); }
      for(a=[0:45:135]) translate([0,fan_c[1],z0+grille_t/2]) rotate([0,0,a]) cube([open_d,3,grille_t+2],center=true);
      translate([0,fan_c[1],z0-1]) cylinder(r=14,h=grille_t+2);
    }
    for(s=[-1,1],y=post_y) translate([s*post_x,y,z0-0.01]){ cylinder(d=3.4,h=grille_t+1); translate([0,0,grille_t-1.7+0.02]) cylinder(d1=3.4,d2=6.6,h=1.7); }
  }
}

module fan_dummy(){ translate([fan_c[0],fan_c[1],pnl_z[1]]) difference(){ translate([0,0,fan[2]/2]) cuboid(fan,rounding=8,edges="Z"); cylinder(d=open_d,h=3*fan[2],center=true);} }

if(part=="edge_front") edge();
if(part=="edge_rear") edge_rear();
if(part=="panel") panel();
if(part=="grille") grille();
if(part=="fan") fan_dummy();
if(part=="assembly"){ edge(); edge_rear(); panel(); grille(); %fan_dummy(); }
