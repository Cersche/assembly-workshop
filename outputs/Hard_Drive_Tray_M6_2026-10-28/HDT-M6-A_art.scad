// HDT-M6-A faceplate artwork: database icon redrawn as vector shapes (smooth edges, no pixel grid).
// Brian's image: data/normal-use/artwork/8330262e...png (512 x 580 px). Parts: "faceplate_art" (plate with pocket), "art" (inlay).
// PROPOSED, UNVALIDATED: printed color result, fit and strength UNKNOWN.
include <HDT-M6-A.scad>
art_h=30; art_x=0; art_z=22.2; art_depth=0.6;  // icon height (mm), centre X/Z on the plate front, inlay depth
$fn=180;
W=512; H=580; rx=256; ry=75; cs=[75,225,365,505]; g=20; dot_r=11.5;
module ell(c){translate([W/2,c])scale([rx,ry])circle(r=1);}
module icon_px(){  // pixel coordinates, y down
 difference(){
  union(){
   ell(cs[0]);
   for(k=[1:3])difference(){
    union(){translate([0,cs[k-1]])square([W,cs[k]-cs[k-1]]);ell(cs[k]);}
    union(){ell(cs[k-1]+g);translate([-1,-1])square([W+2,cs[k-1]+g+1]);}
   }
  }
  for(k=[1:3],d=[[362,23],[410,13],[460,1]])translate([d[0],cs[k]+d[1]])circle(r=dot_r);
 }
}
module icon2d(){s=art_h/H;translate([art_x,art_z])scale([s,-s])translate([-W/2,-H/2])icon_px();}
module art3d(){translate([0,-plate_t+art_depth,0])rotate([90,0,0])linear_extrude(art_depth)icon2d();}
if(part=="faceplate_art")difference(){faceplate();translate([0,-0.001,0])art3d();}
if(part=="art")art3d();
if(part=="icon2d")icon2d();
