// Lab Rax Pi4 two-piece joint prototype. Conceptual joint geometry; rack engagement unverified.
$fn=48;
part="assembly"; // assembly, faceplate, tray
plate_w=252; plate_h=42; plate_t=3;
tray_w=112; tray_d=82; tray_t=3;
// Tray extends rearward (+Y); board connectors point toward +X (rack right).
// Plate centered at X=0, front at Y=-3, bottom Z=0.
tray_x=-tray_w/2; tray_y=0; tray_z=7;
// Two alignment tongues on faceplate; matching slots on tray front edge.
// Joint uses two horizontal M3 screws inserted from rear through tray tabs into plate bosses.
// Fastener engagement is conceptual: thread inserts and tolerances require testing.
joint_x=[-40,40]; tongue_w=12; tongue_depth=7; tongue_h=3; tongue_z=tray_z+3.5;
slot_clear=0.3; boss_d=9; m3_clear=3.4; insert_pilot=4.2;
module capsule2d(len=10,diam=7){hull(){translate([-(len-diam)/2,0])circle(d=diam);translate([(len-diam)/2,0])circle(d=diam);}}
module faceplate(){
 difference(){
  union(){
   translate([-plate_w/2,-plate_t,0]) cube([plate_w,plate_t,plate_h]);
   // Faceplate alignment tongues projecting rearward
   for(x=joint_x)translate([x-tongue_w/2,0,tongue_z])cube([tongue_w,tongue_depth,tongue_h]);
   // Rear insert bosses, threaded insert pilot axes along Y
   for(x=joint_x)translate([x,0,tray_z+14])rotate([-90,0,0])cylinder(d=boss_d,h=8);
  }
  // 1U creator slots, vertical center +1.9722 relative to source midpoint
  for(x=[-118.2625,118.2625])translate([x,-plate_t-0.1,plate_h/2+1.9722])rotate([-90,0,0])linear_extrude(height=plate_t+0.2) capsule2d();
  for(x=joint_x)translate([x,-0.1,tray_z+14])rotate([-90,0,0])cylinder(d=insert_pilot,h=8.2);
 }
}
module tray(){
 difference(){
  union(){
   translate([tray_x,tray_y,tray_z])cube([tray_w,tray_d,tray_t]);
   for(x=joint_x) translate([x-9,0,tray_z+tray_t])cube([18,8,5]);
   // Vertical screw ears on tray, rear-accessible fasteners
   for(x=joint_x)translate([x-7,8.3,tray_z+3])cube([14,3,19]);
   // Four side gussets tie both upright ears into the tray floor.
   // Lowered crest clears the nominal PCB underside (Z=16), including at Y=13.
   for(x=joint_x) for(side=[-1,1]) translate([x+side*6-1,0,0])
     hull(){translate([0,9,tray_z+2.7])cube([2,2,0.5]);
            translate([0,9,tray_z+9])cube([2,2,0.5]);
            translate([0,20,tray_z+2.7])cube([2,2,0.5]);}
   // PCB bosses, 58x49 pitch, nominal offsets remain provisional
   for(dx=[0,58],dy=[0,49])translate([tray_x+12+3.5+dx,tray_y+13+3.5+dy,tray_z+tray_t])cylinder(d=7,h=6);
  }
  // Reinforced front joint rail: pockets are enclosed vertically and laterally.
  // Tongue sockets at front edge
  for(x=joint_x)translate([x-(tongue_w+slot_clear)/2,-0.1,tongue_z-slot_clear/2])cube([tongue_w+slot_clear,tongue_depth+slot_clear,tongue_h+slot_clear]);
  // Screw clearance along Y from rear face of ears into plate bosses
  for(x=joint_x)translate([x,11.4,tray_z+14])rotate([90,0,0])cylinder(d=m3_clear,h=12);
  for(dx=[0,58],dy=[0,49])translate([tray_x+12+3.5+dx,tray_y+13+3.5+dy,tray_z-0.1])cylinder(d=2.8,h=9.2);
  for(x=[tray_x+19:11:tray_x+96],y=[tray_y+12:11:tray_y+70])
   if(min([for(dx=[0,58],dy=[0,49])norm([x-(tray_x+15.5+dx),y-(tray_y+16.5+dy)])])>8)
    translate([x,y,tray_z-0.1])cylinder(d=5,h=tray_t+0.2);
 }
}
intersection(){tray(); translate([tray_x+12,tray_y+13,16.001])cube([85,56,1.6]);}