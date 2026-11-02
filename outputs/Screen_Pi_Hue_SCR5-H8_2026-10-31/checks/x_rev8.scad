include <geometry.scad>
GCX=33;GCZ=41.5;GW=120.7;GH=77.2;
intersection(){union(){plate();frame();}
 union(){
  for(d=[40,98])translate([GCX+GW/2-d,9.1,GCZ+GH/2-10])rotate([-90,0,0])cylinder(d=5.5,h=10,$fn=32); // unused Pi standoffs, 10 tall
  translate([GCX+GW/2-25,2.5,GCZ-GH/2-4.5])cube([8,9.1-2.5,4.5]); // panel ribbon wrap
 }}
