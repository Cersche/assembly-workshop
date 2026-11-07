// TF-D DRAFT (2026-11-07, Brian: the fan must be screwed down): 4 pads under the CT200 155 x 155 holes with M3 inserts, M3 x 35 socket caps down through the fan, grille holes for the heads. TF-C source is frozen in outputs/Rack_Top_Fan_TF-C_2026-11-06/src.
// TF-C (2026-11-06: stock M6 x 8 button-head cross joints: insert bores in the rails, head recesses in the edges; 195 fan cavity; looks pass, Brian 2026-11-06: 45 deg chamfer, swirl grille; shadow groove dropped): rack top for a 200 mm exhaust fan, option B (Brian 2026-11-05).
// The fan sits fully recessed in the top's own 35 mm height (Brian: no fan body sticking out of the top):
// new front + rear top edges are hollowed on the inside into a cavity, the fan rests on ledges in them,
// and a 3 mm grille, flush with the rail tops, clamps it down. No panel: the grille is the top surface.
// Draft 3 (Brian picked B): the top is 15 taller (50 instead of 35) so there is a 15 mm air gap between the
// CM1000's top (Z 400.05, it fills slot 1) and the fan. That needs our own side rails; the stock handles go back on them.
// Frame = rack frame: X centred, Y 0 front .. 240 rear, Z 0 = bottom of slot 9, post tops Z 400.05.
// Joint values (plug, tongue, cross-holes) are read from the creator's meshes (docs/devices/lab-rax-top.md),
// not measured, and not copied: they are redrawn here as plain boxes. Fit and strength UNKNOWN.
include <workshop.scad>
include <BOSL2/std.scad>
part="assembly";         // edge_front | edge_rear | rail | rail_left | grille | fan | assembly
tag=undef; // Optional override; defaults belong to each physical part below.
$fn=64;

// --- stock interfaces (source values) ---
z_top=400.05;            // post tops / bottom of the edge body / top of slot 1 (U9)
z_stock=435.05;          // stock rail/edge top (reference only)
air_gap=15;              // Brian 2026-11-05: room between the modem top and the fan
z_lid=z_stock+air_gap;   // top of our rails and edges, Z 450.05
x_edge=141.12;           // edge half length (282.25 long)
plug_x=[127.12,133.98];  // plug + tongue column, each end
plug_y=[11.15,35]; plug_z=[380.2,z_top];      // drops into the post top pocket (post solid Y 0..11)
tongue_y=[35,54.85]; tongue_z=[z_top,423.9];  // slides into the side rail end pocket (Y 35..55, Z 400..424)
xhole_d=6.4; plug_hole=[22.5,390.05]; tongue_hole=[45,412.55]; // cross-holes along X, stock centres (source mesh)
xhead=[10.8,2];          // stock M6 x 8 button-head recess on the inner face of the plug and tongue (dia, depth)
xinsert=[7.6,139.48];    // stock M6 insert bore in the post/rail, facing the edge: dia, outer end X (1.5 skin left)
rail_in=110.98;          // inner face of the side rails (stock value, kept)
rail_out=140.98; rail_y=[35,205];             // stock rail envelope in X and Y
pocket_fit=[0.15,0.15,0.1];                   // tongue pocket room in X, Y, Z (stock rail pocket ~Y 35..55, Z 400..424)
groove=[136.28,139.78,405.5];                 // side panel groove from below, stock X 136.28..139.78 (depth approx.)
handle_hole=[124.73,[55,185]];                // stock handle screw positions (M6 inserts in the rail top)

// --- new design values (draft) ---
fan=[195,195,30]; fan_c=[0,120]; fan_fit=0.5; // CT200 frame 195 x 195 x 30 (Thermaltake drawing, not measured); 0.5 room each side
ledge_t=2;               // fan rests on ledges in the edges: Z 415.05..417.05
grille_t=3;              // grille Z 447.05..450.05, flush with the rail tops; it rests on the fan top
open_d=192;              // air opening under the blades (ledges cut back to it) and in the grille
front_wall=3;            // outer wall of each edge at the grille seat
grille_fit=0.3;          // grille to edge recess, each side
grille_x=rail_in-0.5;    // grille half width: 0.5 clear of the rail lip
m3_y=26; m3_x=[-105.5,105.5];                 // grille screws at the 4 corners, in solid edge beside the cavity
csk_d=7.0; csk_h=(csk_d-3.4)/2;               // M3 countersink, 90 deg, room around a 6.7 max head                // grille screws, M3 countersunk into M3 inserts in the edge walls
fan_hole=155/2;          // CT200 hole pattern 155 x 155 centred (Thermaltake drawing; holes "standard", ~4.3, Brian 2026-11-07)
pad_t=8; pad_d=12;       // TF-D: pad under each fan corner, Z 409.05..417.05, boss 12 OD (>= 9 for M3 x 3 x 5)
shcs_d=5.5; shcs_h=3; head_hole=shcs_d+2;     // M3 socket cap head (std 5.5 x 3) in a grille hole with 1 mm room all round
jack_x=85; jack_z=407.5; jack_d=8;            // DC panel jack in the rear edge's back face (model UNKNOWN), below the fan ledge
chamfer=15;              // looks: 45 deg chamfer on the outer top corner of each edge, like the stock edge's slope
seat_y=chamfer+2;        // grille seat starts here (2 mm land behind the chamfer)
hub_r=14; ring_r=62; n_blades=16; blade_w=2.4; sweep=70;   // swirl grille
cav_x=fan[0]/2+fan_fit;  // cavity half width
cav_y=fan_c[1]-fan[1]/2-fan_fit;              // cavity front face (Y 19.5)
z_fan=z_lid-grille_t-fan[2]; z_ledge=z_fan-ledge_t; z_grille=z_lid-grille_t;

module box(a,b){translate(a)cube(b-a);}

module edge(jack=false, label="TFE-D", coupon_insert=false){
  union(){ edge_body(jack,label,coupon_insert); fan_pads(jack); }
}
module edge_body(jack, label, coupon_insert){
  difference(){
    union(){
      translate([-x_edge,0,z_top]) cuboid([2*x_edge,35,z_lid-z_top],rounding=2,edges=[TOP+FRONT],anchor=FRONT+BOTTOM+LEFT);
      for(s=[-1,1]) mirror([s<0?1:0,0,0]){
        box([plug_x[0],plug_y[0],plug_z[0]],[plug_x[1],plug_y[1],plug_z[1]+0.01]);
        box([plug_x[0],tongue_y[0]-0.01,tongue_z[0]],[plug_x[1],tongue_y[1],tongue_z[1]]);
      }
    }
    // fan cavity, open to the inside, ledge left at z_ledge
    box([-cav_x,cav_y,z_fan],[cav_x,36,z_lid+1]);
    // below the ledge: open to the air gap under the fan
    box([-cav_x,cav_y,z_top-1],[cav_x,36,z_ledge]);
    // ledge cut back to the air opening
    translate([fan_c[0],fan_c[1],z_ledge-1]) cylinder(d=open_d,h=ledge_t+2);
    // grille seat
    box([-grille_x-grille_fit,seat_y,z_grille],[grille_x+grille_fit,36,z_lid+1]);
    // 45 deg chamfer on the outer top corner
    translate([-x_edge-1,0,0]) rotate([90,0,90]) linear_extrude(2*x_edge+2)
      polygon([[-1,z_lid-chamfer-1],[-1,z_lid+1],[chamfer+1,z_lid+1]]);
    // cross-holes
    // M6 x 8 button heads go in from inside the rack and thread into the post / rail inserts (Brian 2026-11-06, as stock)
    for(s=[-1,1]) mirror([s<0?1:0,0,0]) for(h=[plug_hole,tongue_hole]) translate([0,h[0],h[1]]) rotate([0,90,0]){
      translate([0,0,plug_x[0]-1]) cylinder(d=xhole_d,h=plug_x[1]-plug_x[0]+2);
      translate([0,0,plug_x[0]-1]) cylinder(d=xhead[0],h=xhead[1]+1);
    }
    // M3 inserts for the grille screws
    for(x=m3_x) translate([x,m3_y,z_grille]) mirror([0,0,1]) ws_insert_bore(ws_insert_m3,5);
    // ID on the inner face (Y 35) beside the cavity: mid-length is open air (the fan opening),
    // so it sits in solid wall between the cavity (X 100.5) and the plug/tongue column (X 127.12).
    if(label!="") inner_tag(is_undef(tag)?label:tag,119,435,3);
    // DC jack (rear edge only): hole through the back face, pocket beside the fan, open down into the rack
    if(jack){ translate([jack_x,-1,jack_z]) rotate([-90,0,0]) cylinder(d=jack_d,h=front_wall+2);
              box([jack_x-6,front_wall,z_top-1],[jack_x+6,36,z_ledge-1]); }
  }
}
// TF-D: pads under the two fan corners on this edge. They hang from the ledge and the cavity wall (Y 19.5)
// into the 15 mm air gap; M3 x 3 x 5 insert from the top, 3.4 hole below for the screw tip.
module fan_pads(jack){
  z0=z_fan-pad_t;
  difference(){
    for(x=[-fan_hole,fan_hole]) hull(){
      translate([x,fan_c[1]-fan_hole,z0]) cylinder(d=pad_d,h=pad_t);
      box([x-pad_d/2-2,cav_y-0.01,z0],[x+pad_d/2+2,cav_y+1,z_fan]);
    }
    for(x=[-fan_hole,fan_hole]) translate([x,fan_c[1]-fan_hole,0]){
      translate([0,0,z_fan]) mirror([0,0,1]) ws_insert_bore(ws_insert_m3);
      translate([0,0,z0-1]) cylinder(d=3.4,h=pad_t+2);
    }
    if(jack) box([jack_x-6,front_wall,z_top-1],[jack_x+6,36,z_ledge-1]);   // keep the DC jack pocket open
  }
}
module rail(label="TSR-B"){
  difference(){
    translate([rail_in,rail_y[0],z_top]) cuboid([rail_out-rail_in,rail_y[1]-rail_y[0],z_lid-z_top],rounding=2,edges=[TOP+RIGHT],anchor=FRONT+BOTTOM+LEFT);
    // tongue pockets at both ends, open at the end and the bottom (the rail drops onto the edge tongues)
    for(e=[0,1]) let(y0=e==0?rail_y[0]-1:240-tongue_y[1]-pocket_fit[1], y1=e==0?tongue_y[1]+pocket_fit[1]:rail_y[1]+1)
      box([plug_x[0]-pocket_fit[0],y0,z_top-1],[plug_x[1]+pocket_fit[0],y1,tongue_z[1]+pocket_fit[2]]);
    // inside of each pocket open to the rack, as on the stock rail, so the M6 screw goes in from inside
    for(e=[0,1]) let(y0=e==0?rail_y[0]-1:240-tongue_y[1]-pocket_fit[1], y1=e==0?tongue_y[1]+pocket_fit[1]:rail_y[1]+1)
      box([rail_in-1,y0,z_top-1],[plug_x[0],y1,tongue_z[1]+pocket_fit[2]]);
    // M6 heat-set insert (M6 x 5 x 8) facing the tongue, blind: 1.5 skin on the outer face as stock
    for(y=[tongue_hole[0],240-tongue_hole[0]]) translate([plug_x[1],y,tongue_hole[1]]) rotate([0,90,0]) cylinder(d=xinsert[0],h=xinsert[1]-plug_x[1]);
    // side panel groove from below
    box([groove[0],rail_y[0]-1,z_top-1],[groove[1],rail_y[1]+1,groove[2]]);
    // Inner side, clear of pockets, groove and handle bores.
    translate([rail_in-0.01,120,435]) rotate([90,0,90])
      linear_extrude(height=0.61) mirror([1,0,0]) text(is_undef(tag)?label:tag,size=4,halign="center",valign="center");
    // stock handles screw down into M6 inserts here
    for(y=handle_hole[1]) translate([handle_hole[0],y,z_lid]) mirror([0,0,1]) ws_insert_bore(ws_insert_m6,10);
  }
}
module rail_left(){ mirror([1,0,0]) rail(); }
module edge_rear(){ translate([0,240,0]) rotate([0,0,180]) edge(jack=true,label="TRE-D"); }

module grille(){
  y0=seat_y+grille_fit; y1=240-seat_y-grille_fit;
  difference(){
    translate([-grille_x,y0,z_grille]) cuboid([2*grille_x,y1-y0,grille_t],rounding=2,edges="Z",anchor=FRONT+BOTTOM+LEFT);
    grille_openings();
    translate([70,26,z_grille-0.01]) linear_extrude(height=0.61)
      text(is_undef(tag)?"TFG-B":tag,size=4,halign="center",valign="center");
    for(x=[-fan_hole,fan_hole],y=[fan_c[1]-fan_hole,fan_c[1]+fan_hole]) translate([x,y,z_grille-1]) cylinder(d=head_hole,h=grille_t+2);
    for(x=m3_x,y=[m3_y,240-m3_y]) translate([x,y,z_grille-0.01]){ cylinder(d=3.4,h=grille_t+1); translate([0,0,grille_t-csk_h+0.02]) cylinder(d1=3.4,d2=csk_d,h=csk_h); }
  }
}

module fan_dummy(){ translate([fan_c[0],fan_c[1],z_fan]) difference(){ translate([0,0,fan[2]/2]) cuboid(fan,rounding=8,edges="Z"); cylinder(d=open_d-4,h=3*fan[2],center=true);} }


// The same cutters drive the grille and the check-only cuts (32 vents + 8 screws + 4 fan-screw head holes).
module grille_openings(){
  translate([fan_c[0],fan_c[1],z_grille-1]) linear_extrude(grille_t+2) difference(){
    circle(d=open_d);
    circle(r=hub_r);
    difference(){ circle(r=ring_r+blade_w/2); circle(r=ring_r-blade_w/2); }   // one ring keeps fingers out and stiffens the blades
    for(i=[0:n_blades-1]) rotate(i*360/n_blades) blade_2d();
  }
}
module blade_2d(steps=14){
  for(k=[0:steps-1]) hull() for(t=[k/steps,(k+1)/steps])
    let(r=hub_r-1+t*(open_d/2+3-hub_r+1), a=t*sweep) translate([r*cos(a),r*sin(a)]) circle(d=blade_w,$fn=16);
}
module cuts(){
  grille_openings();
  for(x=m3_x,y=[m3_y,240-m3_y]) translate([x,y,z_grille-1]) cylinder(d=3.4,h=grille_t+2);
  for(x=[-fan_hole,fan_hole],y=[fan_c[1]-fan_hole,fan_c[1]+fan_hole]) translate([x,y,z_grille-1]) cylinder(d=head_hole,h=grille_t+2);
}
module inner_tag(label,x,z,size){
  translate([x,35.01,z]) rotate([90,0,0]) linear_extrude(height=0.61) mirror([1,0,0])
    text(label,size=size,halign="center",valign="center");
}
module coupon(){
  difference(){
    intersection(){edge(label="",coupon_insert=true); box([101,-1,plug_z[0]-1],[x_edge+1,56,z_lid+1]);}
    inner_tag(is_undef(tag)?"TFE-T2":tag,120,435,3);
  }
}
module rail_coupon(){
  difference(){
    intersection(){rail(label="");box([rail_in-1,35,z_top-1],[rail_out+1,75,z_lid+1]);}
    translate([rail_in-0.01,55,435]) rotate([90,0,90]) linear_extrude(height=0.61) mirror([1,0,0])
      text(is_undef(tag)?"TSR-T2":tag,size=3,halign="center",valign="center");
  }
}
// Head envelopes include 1 mm radial room. Cross-hole hardware remains UNKNOWN:
// no M6 cross-hole screw has been specified by Brian, so none is invented here.
module keepout(){
  // Countersunk heads sit flush in the countersink; keep the room above the grille open.
  for(x=m3_x,y=[m3_y,240-m3_y]) translate([x,y,z_lid]) rotate([90,0,0])
    ws_head_keepout(0,0,0,csk_d,6);
  // TF-D fan screws: M3 socket cap heads on the fan top, 1 mm room, 6 mm tool room above
  for(x=[-fan_hole,fan_hole],y=[fan_c[1]-fan_hole,fan_c[1]+fan_hole]) translate([x,y,z_grille]) cylinder(d=head_hole,h=grille_t+6);
  // M6 x 8 button heads at the cross joints (head 10.5 + 1 mm room), 6 mm of tool room inward from the inner face
  for(sx=[-1,1], h=[plug_hole,tongue_hole], y=[h[0],240-h[0]]) translate([sx>0?plug_x[0]-6:-plug_x[0],y,h[1]]) rotate([0,90,0]) cylinder(d=12.5,h=6);
}
// Same transform for a physical part and its check envelope. Edges lie on their flat
// front face (Y 0), diagonal on a 256 bed: tongues, ledge and cavity walls print upright;
// the two plugs stick out sideways 19.85 and need a small support each.
module edge_print_pose(){
  translate([128,128,0]) rotate([0,0,45]) translate([0,(plug_z[0]+z_lid)/2,0]) rotate([90,0,0]) children();
}
module rear_local(){translate([0,240,0]) rotate([0,0,180]) children();}
module rail_print_pose(){translate([0,0,rail_out]) rotate([0,90,0]) translate([0,-35,-z_top]) children();}
module grille_print_pose(){translate([grille_x,-front_wall-grille_fit,-z_grille]) children();}
if(part=="edge_front") edge();
if(part=="edge_rear") edge_rear();
if(part=="rail") rail();
if(part=="rail_left") rail_left();
if(part=="grille") grille();
if(part=="fan") fan_dummy();
if(part=="coupon") coupon();
if(part=="rail_coupon") rail_coupon();
if(part=="edge_front_print") edge_print_pose() edge();
if(part=="edge_rear_print") edge_print_pose() edge(jack=true,label="TRE-D");
if(part=="rail_print") rail_print_pose() rail();
if(part=="grille_print") grille_print_pose() grille();
if(part=="keepout") keepout();
if(part=="keepout_edge_front_print") edge_print_pose() keepout();
if(part=="keepout_edge_rear_print") edge_print_pose() rear_local() keepout();
if(part=="keepout_rail_print") rail_print_pose() keepout();
if(part=="keepout_grille_print") grille_print_pose() keepout();
if(part=="cuts") cuts();
if(part=="assembly"){ edge(); edge_rear(); rail(); rail_left(); grille(); %fan_dummy(); }
