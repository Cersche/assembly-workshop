// CSB-B DRAFT (from printed CSB-A, which fits; adds tool windows) cable span bracket: front post to rear post, one side of the rack.
// Frame: X centred, Y=0 front face of front post, Y=240 rear face of rear post, Z=0 slot bottom. Drawn on the right (+X).
// Same part goes on the left turned 180 degrees about the vertical (part=="left"): the posts and this part both repeat under that turn.
// Post values come from the 4U post mesh (object_190), not measured. Fit, capacity and strength UNKNOWN.
include <workshop.scad>
part="bracket";          // bracket | left | keepout | demo_cables
soft=true;               // rounded outside corners, round finger tips (Brian picked B + C, 2026-11-05)
vented=true;             // floor slots
wall_windows=false;      // outer wall windows: they merged into one long slot; Brian closed them 2026-11-05
dropout=true;            // drop-out near each end: cables leave straight up or down in the outer lane (X 121..134.5), free beside the post-rail parts
do_y0=44; do_y1=62; do_x=121; do_r=3; do_lintel=8;  // CSB-B: drop-outs moved 4 away from the ends so the tool window takes a 30 mm key short arm (Brian). Outer wall kept as a bridge across the top of each drop-out
tag="CSB-B";             // test print ID, engraved 0.6 deep in the outer face of the outer wall, mid-length
tool_z=6;                // CSB-B: inner wall cut to 6 tall between each pad and its drop-out, so a 4 mm L-key reaches the screw (CSB-A: no driver access, Brian 2026-11-05)
key_a=0; key_s=30;       // demo_key short arm, tip to outside of bend                 // demo_key swing about the screw axis, degrees
hooks=false;             // catch under each finger tip (option D, not picked)
y_f=6; y_r=234;          // inner faces of the front and rear post flanges (mesh + 240 rack depth)
end_gap=0.3;             // gap at each end to the flange
x_in=110.5;              // inner edge: 0.6 inside the flange edge, leaves 2 of wall beside the 11.5 head recess
x_out=134.5;             // outer wall between the posts; side panel groove starts at X 136.42
x_pad=126.8;             // pad stops 0.32 short of the post side wall (X 127.12)
x_fil=124.2;             // post's inner corner fillet runs X 124.5..127.1, Y 6..8.8: clear it
y_bay0=36;               // past the post side wall (ends Y 35); mirrored at the rear
h=ws_plate_h(1); z0=ws_plate_bottom(); zm=ws_plate_center(1); ztop=z0+h;
floor_t=3; wall=2.5; pad_t=8;
low_wall=20;             // inner wall height between fingers: cables can leave sideways, tools can reach the screws
pitch=24; finger_w=10; drop_gap=8;   // fingers alternate from each wall, leaving an 8 gap to feed cables past
$fn=48;
yc=(y_f+y_r)/2;
function ry(y)=y_f+y_r-y;

module half2d(){ polygon([[x_in,yc],[x_in,y_f+end_gap+1.5],[x_in+1.5,y_f+end_gap],[x_fil,y_f+end_gap],[x_pad,y_f+end_gap+3.2],
    [x_pad,y_bay0-1],[x_out,y_bay0+6],[x_out,yc]]); }
module plan_raw(){ half2d(); translate([0,y_f+y_r])mirror([0,1])half2d(); }
rr= soft ? 3 : 0;
module plan2d(){ if(rr>0) offset(r=rr)offset(delta=-rr)plan_raw(); else plan_raw(); }
module cavity2d(){ intersection(){ offset(delta=-wall)plan2d(); translate([0,y_f+end_gap+pad_t])square([300,y_r-y_f-2*end_gap-2*pad_t]); } }
function wx(y)= y>=y_bay0+6 && y<=ry(y_bay0+6) ? x_out : x_out;
module finger_body(y,from_out){ // 45 deg underside: prints with no supports, floor on the bed
  L=x_out-x_in-wall-drop_gap; tip=from_out? x_out-wall-L : x_in+wall+L; sx=from_out?-1:1; root=from_out?x_out:x_in;
  translate([0,y+finger_w/2,0])rotate([90,0,0])linear_extrude(finger_w){
    polygon([[root,ztop],[tip,ztop],[tip,ztop-2],[root+sx*wall,ztop-2-L],[root,ztop-2-L]]);
    if(hooks) polygon([[tip,ztop-2+0.01],[tip-sx*2.2,ztop-2+0.01],[tip,ztop-4.2]]);  // catch: cable pushed past the gap stays behind it
  }
}
module finger(y,from_out){
  if(soft){ L=x_out-x_in-wall-drop_gap; tip=from_out? x_out-wall-L : x_in+wall+L;
    intersection(){ finger_body(y,from_out);
      translate([0,0,z0])linear_extrude(h)hull(){ translate([from_out?x_out:x_in-1,y-finger_w/2])square([0.01,finger_w]);
        translate([tip+(from_out?finger_w/2:-finger_w/2),y])circle(d=finger_w);} } }
  else finger_body(y,from_out);
}
module vents(){ // floor slots between the fingers and long windows in the outer wall
  for(i=[-3:2]) if(!(dropout && (i==-3||i==2))){ y=yc+(i+0.5)*pitch;
    translate([0,y,z0-1])linear_extrude(floor_t+2)hull(){for(x=[x_in+wall+4,x_out-wall-4])translate([x,0])circle(d=4);}
  }
  if(wall_windows) for(i=[-2:1]) translate([x_out-wall-1,yc+(i+0.5)*pitch,z0+floor_t+3])rotate([0,90,0])linear_extrude(wall+2)
    hull(){for(dy=[-(pitch-finger_w)/2-6,(pitch-finger_w)/2+6])translate([-5,dy])circle(d=8);}
}
module screw_end(y0,dir){ // dir=+1 front pad, -1 rear pad. Middle hole takes the M6 x 8; corners only get relief for faceplate screws
  a=dir>0?-90:90;
  translate([ws_hole_x,y0-dir,zm])rotate([a,0,0])cylinder(d=ws_m6_clear,h=pad_t+2);
  translate([ws_hole_x,y0+dir*ws_m6_web,zm])rotate([a,0,0])cylinder(d=ws_m6_head_d,h=pad_t,$fn=64);
  for(dz=[-ws_hole_dz,ws_hole_dz])translate([ws_hole_x,y0-dir,zm+dz])rotate([a,0,0])cylinder(d=9,h=4+1);
}
module bracket(){
  difference(){
    union(){
      difference(){
        translate([0,0,z0])linear_extrude(h)plan2d();
        translate([0,0,z0+floor_t])linear_extrude(h)cavity2d();
        // inner wall low between the finger risers
        for(i=[-4:3])translate([x_in-1,yc+i*pitch+(i==-4?-200:0)+finger_w/2,z0+low_wall])cube([wall+2,pitch-finger_w+(i==-4?200:0),h]);
        translate([x_in-1,yc+3*pitch+finger_w/2,z0+low_wall])cube([wall+2,y_r,h]);
      }
      for(i=[-3:3]) if(!(dropout && abs(i)==3)) finger(yc+i*pitch,abs(i)%2==1);
      // Brian 2026-11-05: a finger over each drop-out, from the full-height inner wall, holds cables as they turn down
      if(dropout) for(y=[(do_y0+do_y1)/2,ry((do_y0+do_y1)/2)]) finger(y,false);
      // inner wall stays full height beside each drop-out: it carries the bracket where the outer wall is cut
      if(dropout) for(m=[0,1]) intersection(){
        translate([0,0,z0])linear_extrude(h)plan2d();
        translate([0,m?ry(do_y1+8):do_y0,z0])cube([x_in+wall-0.01,do_y1-do_y0+8,h]); }
      // keep the pads whole
      for(y=[y_f+end_gap,y_r-end_gap-pad_t])intersection(){translate([0,0,z0])linear_extrude(h)plan2d();translate([0,y,0])cube([300,pad_t,100]);}
    }
    screw_end(y_f+end_gap,1);
    screw_end(y_r-end_gap,-1);
    if(vented) vents();
    for(y=[y_f+end_gap+pad_t-0.01, ry(do_y0-1)]) translate([x_in-1,y,z0+tool_z])cube([wall+2,do_y0-1-(y_f+end_gap+pad_t)+0.01,h]);  // tool windows
    translate([x_out-0.6,yc,zm])rotate([90,0,90])linear_extrude(1)text(tag,size=6,font="Liberation Sans:style=Bold",halign="center",valign="center");
    if(dropout) for(y=[do_y0,ry(do_y1)]) translate([0,0,z0-1])linear_extrude(h+1-do_lintel)offset(r=do_r)translate([do_x+do_r,y+do_r])square([40,do_y1-do_y0-2*do_r]);
  }
}
module keepout(){
  ws_m6_head_keepout(ws_hole_x,y_f+end_gap,zm,len=6);
  translate([0,240,0])mirror([0,1,0])ws_m6_head_keepout(ws_hole_x,y_f+end_gap,zm,len=6);
}
module left(){ translate([0,240,0])rotate([0,0,180])bracket(); }
if(part=="bracket")bracket();
if(part=="left")left();
if(part=="keepout")keepout();
if(part=="demo_cables"){ // scale only: 6 mm data, 8 mm power. Not a part
  for(c=[[116.5,10,6],[122.5,10,6],[128,10,8],[116.5,16,6],[122.5,16,6],[128,18,8]])
    translate([c[0],40,z0+floor_t+c[1]-5+c[2]/2])rotate([-90,0,0])cylinder(d=c[2],h=160);
}
if(part=="demo_key"){ // 4 mm hex L-key in the front screw, long arm into the rack. Not a part
  translate([ws_hole_x,0,zm])rotate([0,key_a,0])translate([-ws_hole_x,0,-zm]){
    translate([ws_hole_x,9.6,zm])rotate([-90,0,0])rotate([0,0,30])cylinder(d=4.62,h=key_s-2.3,$fn=6);
    translate([ws_hole_x+2.3,9.6+key_s-2.3,zm])rotate([0,-90,0])rotate([0,0,30])cylinder(d=4.62,h=70,$fn=6);
  }
}
