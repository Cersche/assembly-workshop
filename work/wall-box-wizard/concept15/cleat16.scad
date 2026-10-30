// MoCA box wall plate + French-cleat back plate (Brian, 2026-10-30: "a new back panel that mates with a template that
// we first put on the wall"; picked French cleat, wall plate holes for anchors AND a stud). PROPOSED - UNVALIDATED:
// fit, cleat hold, lock screw, anchor/stud load and strength are UNKNOWN until printed and tested.
//
// The wall plate goes on the wall first (it is also the drilling template: same 105 x 210 outline as the box back).
// The box's new back plate has a pocket cut through its outer face; lift the box ~9 mm, push it to the wall so the
// wall cleat enters the pocket, drop it: the 45 deg roof pulls the box onto the plate. One M3 lock screw from inside
// the box (above the ScreenBeam, through the lid opening) into an insert in the cleat stops it lifting off.
// Replaces back_plate() only; sleeve, lid, cradle and porch are unchanged (the old keyhole back plate still fits).
//
// Box frame as body15.scad: X 0..105, Z 0..210, back outer face at Y=db (72.5), wall at Y=db+wp_t. s = depth into the
// box from the back outer face. pick: 1 back plate, 2 wall plate, 0 both seated (plus 3 = sleeve ghost for checks).
include <body15.scad>
part="none"; mount_style="none";   // no keyholes on the new back plate
pick=0;

wc_c=8;             // cleat depth (s 0..8)
wc_zh=193;          // cleat tip top (at s=wc_c); roof/cleat top is z = wc_zh-wc_c+s (45 deg, down towards the wall)
wc_zb=171;          // cleat bottom (flat)
wc_x=[17,88];       // cleat length
wc_lift=9;          // lift room under the cleat in the pocket (needs > wc_c to unhook)
wc_clr=0.5;         // pocket depth beyond the cleat tip
wc_side=0.6;        // pocket side clearance (sets left-right play)
wp_t=3;             // wall plate thickness (box stands this far off the wall)
band_t=10.5;        // back plate thickness at the cleat band (from the outer face)
band_x=[12,93]; band_z=[wc_zb-wc_lift-3,wc_zh+3];   // clear of the cradle top (Z158 at +6 travel) and top joint blocks
lock=[38,186];      // lock screw X, Z: M3 heat-set insert in the cleat face, M3 x 8-10 from inside the box
wall_holes=[[24,178],[81,178],[52.5,178],[15,15],[90,15],[52.5,15]];   // anchors: 4 outer; stud: 2 on the centre line
hole_d=4.5; csk_d=9;   // #8 / 4 mm countersunk wood screws (sizes UNKNOWN until Brian picks screws/anchors)
win=[15,90,30,160];    // wall plate window (material saver, lets wall marks show)
id_wall="MOCA-WP-A"; id_back="MOCA-BC-A";

module yz_prism(x0,x1,pts)translate([x0,0,0])rotate([90,0,90])linear_extrude(x1-x0)polygon(pts);   // 2D (Y,Z), along X
module cleat()yz_prism(wc_x[0],wc_x[1],[[db,wc_zb],[db,wc_zh-wc_c],[db-wc_c,wc_zh],[db-wc_c,wc_zb]]);
module pocket(){s1=wc_c+wc_clr;
 yz_prism(wc_x[0]-wc_side,wc_x[1]+wc_side,[[db+1,wc_zb-wc_lift],[db+1,wc_zh-wc_c-1],[db-s1,wc_zh-wc_c+s1],[db-s1,wc_zb-wc_lift]]);}
module engrave(x,y,z,s,size)translate([x,y+0.6,z])rotate([90,0,0])linear_extrude(1)
 text(s,size=size,font=art_font,halign="center",valign="center");

module cleat_back(){difference(){
 union(){back_plate();translate([band_x[0],db-band_t,band_z[0]])cube([band_x[1]-band_x[0],band_t-0.01,band_z[1]-band_z[0]]);}
 pocket();
 translate([lock[0],db-band_t-0.1,lock[1]])rotate([-90,0,0])linear_extrude(band_t)hull()for(dz=[-1.5,1.5])translate([0,dz])circle(d=m3_clear,$fn=24);
 engrave(wo/2,di,45,id_back,5);
}}

module wall_plate(){difference(){
 union(){rbox(0,wo,db,db+wp_t,0,ho,corner_r);cleat();}
 rbox(win[0],win[1],db-1,db+wp_t+1,win[2],win[3],6);
 for(h=wall_holes)let(f=h[1]>wc_zb?db-wc_c:db)translate([h[0],f-0.01,h[1]])rotate([-90,0,0]){
  cylinder(d=hole_d,h=wc_c+wp_t+1,$fn=32);cylinder(d1=csk_d,d2=hole_d,h=(csk_d-hole_d)/2,$fn=32);}
 translate([lock[0],db-wc_c-0.01,lock[1]])rotate([-90,0,0])cylinder(d=insert_pilot,h=insert_depth,$fn=24);
 // level / centre marks: V notches on the edges at the hole heights and on the centre line
 for(z=[15,178],x=[0,wo])translate([x,db-1,z])rotate([-90,0,0])linear_extrude(wp_t+2)polygon([[0,-2],[x==0?2:-2,0],[0,2]]);
 for(z=[0,ho])translate([wo/2,db-1,z])rotate([-90,0,0])linear_extrude(wp_t+2)polygon([[-2,0],[0,z==0?-2:2],[2,0]]);
 engrave(wo/2,db,24,id_wall,4);
 engrave(wo/2,db,202,"TOP",5);
}}

if(pick==1)cleat_back();
else if(pick==2)wall_plate();
else if(pick==0||pick==3){cleat_back();color([0.6,0.7,0.9])wall_plate();if(pick==3)%sleeve();}
