// Assembly Workshop shared parts. Copied from proven sources; printed fit is specific to those specimens,
// and strength is UNKNOWN. Checked against the built parts by tools/test_workshop_lib.py.
// Use: include <workshop.scad>   (tools/release_part.py sets the library path and freezes these files)
// Frame: X centred, plate back Y=0, plate front Y=-ws_plate_t, Z=0 slot bottom.

// ---- Rack and faceplate (44.4 mm standard, Brian 2026-10-20; four-corner slots settled 2026-10-18)
ws_pitch=44.45; ws_plate_gap=0.05; ws_plate_w=252; ws_plate_t=4; ws_plate_r=2.5;
ws_hole_x=118.2625; ws_hole_dz=15.902; ws_slot_len=10; ws_slot_d=7;
function ws_plate_h(u=1)=u*ws_pitch-ws_plate_gap;
function ws_plate_bottom()=ws_plate_gap/2;
function ws_plate_top(u=1)=ws_plate_bottom()+ws_plate_h(u);
function ws_plate_center(u=1)=u*ws_pitch/2;

// ---- Fasteners (Brian's standard, 2026-10-31): [bore, minimum depth]. Fit stays UNKNOWN until a print proves it.
ws_insert_m6=[7.6,6]; ws_insert_m3=[4.2,4]; ws_insert_m25=[3.2,5];
ws_m6_clear=6.6; ws_m6_head_d=11.5; ws_m6_web=2.5;  // SG8-C1 printed: M6 x 8 button head recess good

// ---- Fit values proven on Brian's prints. Specimen-specific starting points: check docs/Fit_Findings.md for the part.
ws_fit_sleeve_top=0.8;       // new sleeves: printed about 0.5 tight at the old 0.3
ws_fit_runner_ledge=1.1;     // OPX-F post rails, good fit 2026-11-04
ws_fit_runner_outer=1.25;
ws_fit_runner_hold=1.35;
ws_fit_runner_side=1.1;

module ws_slot2d(){hull(){for(s=[-1,1])translate([s*(ws_slot_len-ws_slot_d)/2,0])circle(d=ws_slot_d);}}

// Plate outline seen from the front: 2D X = rack X, 2D Y = height Z. Children are 2D cut-outs.
module ws_plate2d(u=1){
 difference(){
  hull()for(sx=[-1,1],sz=[-1,1])translate([sx*(ws_plate_w/2-ws_plate_r),ws_plate_center(u)+sz*(ws_plate_h(u)/2-ws_plate_r)])circle(r=ws_plate_r);
  for(i=[0:u-1],dz=[-ws_hole_dz,ws_hole_dz],x=[-ws_hole_x,ws_hole_x])translate([x,i*ws_pitch+ws_pitch/2+dz])ws_slot2d();
  children();
 }
}

// Solid faceplate with any golden keystones at X positions. Children are 2D cut-outs.
module ws_plate(u=1,keystones=[],$fn=48){
 union(){
  difference(){
   rotate([90,0,0])linear_extrude(height=ws_plate_t)ws_plate2d(u){if($children>0)children();}
   for(x=keystones)ws_keystone_cut(x,u);
  }
  for(x=keystones)ws_keystone(x,u);
 }
}

// Golden keystone (Brian 2026-10-19, ks_tight 0.2 printed perfect; settled, do not tweak without Brian).
// Cross-sections from "10 inch shelf TP-Link SG108 Plus Keystone" by Goul (MakerWorld remix, BY-NC-SA):
// local and personal use only, never redistributed.
ws_ks_tight=0.2;
ws_ks_gold=[
  [-10.50,0.60,[[[45.500,4.080],[45.500,0.080],[38.691,0.080],[38.691,0.000],[7.251,0.000],[7.251,0.080],[1.000,0.080],[1.000,4.080],[1.071,4.080]]]],
  [-9.90,0.98,[[[9.143,4.080],[9.143,6.600],[9.205,7.147],[9.207,7.160],[9.226,7.216],[9.395,7.692],[9.679,8.145],[9.697,8.169],[10.075,8.546],[10.099,8.565],[10.551,8.848],[11.083,9.036],[11.643,9.100],[13.493,9.100],[14.293,9.900],[33.393,9.900],[33.893,10.400],[34.493,10.400],[35.054,10.336],[35.586,10.148],[36.038,9.865],[36.062,9.846],[36.439,9.469],[36.458,9.445],[36.742,8.992],[36.753,8.965],[36.930,8.460],[36.993,7.900],[36.993,4.080],[45.500,4.080],[45.500,0.080],[38.691,0.080],[38.691,0.000],[7.251,0.000],[7.251,0.080],[1.000,0.080],[1.000,4.080],[1.014,4.080]]]],
  [-8.92,1.52,[[[7.551,4.080],[7.551,2.250],[9.143,2.250],[9.143,6.600],[9.209,7.169],[9.367,7.620],[9.404,7.709],[9.658,8.114],[9.716,8.190],[9.755,8.229],[10.054,8.527],[10.130,8.586],[10.534,8.840],[10.623,8.876],[11.074,9.034],[11.643,9.100],[13.493,9.100],[14.293,9.900],[33.393,9.900],[33.893,10.400],[34.493,10.400],[35.063,10.334],[35.514,10.176],[35.603,10.140],[36.006,9.886],[36.083,9.827],[36.420,9.490],[36.479,9.414],[36.719,9.030],[36.737,9.000],[36.770,8.920],[36.927,8.469],[36.993,7.900],[36.993,2.250],[38.551,2.250],[38.551,4.080],[45.500,4.080],[45.500,0.080],[38.691,0.080],[38.691,0.000],[7.251,0.000],[7.251,0.080],[1.000,0.080],[1.000,4.080],[1.044,4.080]]]],
  [-7.40,14.80,[[[7.551,4.080],[7.551,2.250],[9.143,2.250],[9.143,6.600],[9.175,6.878],[9.229,7.247],[9.478,7.850],[9.876,8.368],[10.393,8.765],[10.996,9.015],[11.365,9.069],[11.643,9.100],[13.493,9.100],[13.493,8.100],[11.493,8.100],[11.493,7.200],[16.793,0.500],[16.793,0.000],[7.251,0.000],[7.251,0.080],[1.000,0.080],[1.000,4.080],[1.025,4.080]],[[45.500,4.080],[45.500,0.080],[38.691,0.080],[38.691,0.000],[33.393,0.000],[33.393,5.800],[34.993,5.800],[34.993,8.400],[33.393,8.400],[33.393,9.900],[33.893,10.400],[34.493,10.400],[34.771,10.369],[35.140,10.315],[35.743,10.065],[36.200,9.715],[36.261,9.668],[36.658,9.150],[36.908,8.547],[36.962,8.178],[36.993,7.900],[36.993,2.250],[38.551,2.250],[38.551,4.080],[42.555,4.080]]]],
  [7.40,2.50,[[[45.500,4.080],[45.500,0.080],[38.691,0.080],[38.691,0.000],[7.251,0.000],[7.251,0.080],[1.000,0.080],[1.000,4.080],[7.551,4.080],[7.551,2.250],[9.143,2.250],[9.143,6.600],[9.209,7.168],[9.370,7.630],[9.402,7.705],[9.662,8.120],[9.712,8.185],[9.927,8.400],[10.059,8.531],[10.124,8.582],[10.538,8.841],[10.614,8.873],[11.075,9.034],[11.643,9.100],[13.493,9.100],[14.293,9.900],[33.393,9.900],[33.893,10.400],[34.493,10.400],[35.062,10.335],[35.523,10.172],[35.599,10.141],[36.013,9.882],[36.078,9.831],[36.425,9.486],[36.474,9.420],[36.735,9.005],[36.767,8.930],[36.928,8.467],[36.993,7.900],[36.993,2.250],[38.551,2.250],[38.551,4.080],[42.599,4.080]]]],
  [9.90,0.60,[[[45.500,4.080],[45.500,0.080],[38.691,0.080],[38.691,0.000],[7.251,0.000],[7.251,0.080],[1.000,0.080],[1.000,4.080],[7.551,4.080],[7.551,2.250],[38.551,2.250],[38.551,4.080],[42.635,4.080]]]]
];
module ws_keystone_cut(x,u=1){translate([x-10.5,-ws_plate_t-0.01,ws_plate_center(u)-15])cube([21,ws_plate_t+0.02,33.5]);}
module ws_keystone(x,u=1){intersection(){
 translate([x,0,ws_plate_center(u)])multmatrix([[1,0,0,0],[0,0,1,-4],[0,-1,0,25.09],[0,0,0,1]])intersection(){
  union()for(b=ws_ks_gold)translate([b[0],0,0])rotate([90,0,90])linear_extrude(height=b[1])for(pg=b[2])
   translate([b[1]>10&&min([for(q=pg)q[0]])>30?-ws_ks_tight:0,0])polygon([for(q=pg)[q[0],q[1]-0.08]]);
  translate([-10.5,25.09-18.6,-0.09])cube([21,33.7,10.42]);
 }
 translate([x-10.5,-ws_plate_t-1,ws_plate_center(u)-15])cube([21,ws_plate_t+16,33.5]);
}}

// Round bore along +Z from the origin. spec is one of ws_insert_*.
module ws_insert_bore(spec,depth=0,$fn=64){translate([0,0,-0.01])cylinder(d=spec[0],h=(depth>0?depth:spec[1])+0.01);}

// Hidden M6 joint, plate side: boss behind the plate at X,Z, 8 long with a 1 mm front floor, clipped at the plate top.
module ws_m6_plate_boss(x,z,u=1,d=12,h=8,$fn=64){intersection(){
 translate([x,0,z])rotate([-90,0,0])difference(){cylinder(d=d,h=h);translate([0,0,1])cylinder(d=ws_insert_m6[0],h=h);}
 translate([x-d,-0.1,0])cube([2*d,h+0.2,ws_plate_top(u)]);
}}

// Hidden M6 joint, tray side: clearance hole and head recess along +Y, starting at Y=y0. Subtract from the upright.
module ws_m6_screw_cut(x,y0,z,len=6,web=ws_m6_web){
 translate([x,y0-0.1,z])rotate([-90,0,0])cylinder(d=ws_m6_clear,h=len+0.2,$fn=48);
 translate([x,y0+web,z])rotate([-90,0,0])cylinder(d=ws_m6_head_d,h=len,$fn=64);
}
