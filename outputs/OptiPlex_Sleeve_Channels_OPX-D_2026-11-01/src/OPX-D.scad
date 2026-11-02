// OPX-D (2026-11-01): OPX-C plus front post rails (SG8-M6-F pattern) and a middle screw in each rear ear, for the PC's weight (Brian). Test print, unprinted; fit and strength UNKNOWN.
// The stops on the channels catch the case's rear corners.
// Own geometry; ideas credited to Psychobob (one-piece flush shelf, scooped floor/roof) and scubaroboto (rear C-channel, ear gusset).
// Frame as the app: X centred (- = left seen from the front), plate back Y=0, Z=0 slot bottom, rear post back Y=240.
// Kept from printed SLV-F: plate 252 x 44.4 x 4, four-corner slots, window +-91.75 x Z 3.5..40.8, foot tracks and click-in dips.
// PC (Brian, 2026-11-01): 182.5 wide, 178 deep incl. the bezel, 36 tall; bezel left-aligned, 122.5 x 23 from the bottom, 2.3 proud.
part="assembly";   // assembly, front, rear_left, rear_right, rail_left, rail_right, pc, print_front, print_rear_left, print_rear_right
$fn=48;

rack_pitch=44.45; plate_w=252; plate_t=4; plate_r=2.5; plate_h=44.4; plate_bottom=0.025;
hole_x=118.2625; hole_dz=15.902; rack_depth=240;
pc_w=182.5; pc_d=178; pc_h=36; bz_w=122.5; bz_h=23; bz_t=2.3;
win=91.75; floor_top=3.5; win_top=40.8;       // SLV-F window
pc_front=-plate_t-bz_t;                       // bezel face; the case front is flush with the plate face
pc_rear=pc_front+pc_d;                        // 171.7
z0=0.2; z1=44.2;                              // sleeve and channel body inside the slot
wall=4; ear_web=109;                          // gussets stop short of the post flange (u 111.1)

sleeve_d=65;
// Feet measured by Brian 2026-11-01: 5 x 20 x 2.8 tall, 15 from each side, front pair 15 from the case front (17.3 from the bezel face), rear pair 10 from the rear.
groove_z=1.2; foot_stop_y=pc_front+17.3-0.5; dip_y1=foot_stop_y+21; ramp=1.3;  // SLV-F depths; 21 long dip (20 mm foot + 0.5 each end) ending in a solid forward stop
tracks=[[-76.75,-70.75],[70.75,76.75]];
ch_y0=pc_rear-41;                             // channels start 41 mm ahead of the PC's rear
ledge=12; ledge_rear=6; ledge_top=3.3; roof_low=41.0; lead=1.5; lead_l=6;
taper_y0=pc_rear+6; taper_y1=taper_y0+14;     // grip narrows behind the case so cables have room
gusset_d=25; front_gusset=102.6;              // front gusset stops short of the rail
// Post rail, numbers from SG8-M6-F. u = |X|. Front post: flange Y 0..6 from u 111.1, 4U side wall at u 127.12, inner fillet to Y 11.3. Middle hole u 118.2625, Z 22.225.
ru1=102; rb=107.5; rz_bot=1.5; rz_mid=9; ri=103.5; run_tip=8;   // sleeve runner profile
cl_bear=0.1; cl=0.25;
rl_in=103; rl_wall=111; rl_out=126.9; rl_z0=0.5; rl_z1=44; rl_y0=6.2; rl_y0b=11.8; rl_blk=38; rl_y1=60; rail_r=3;
mid_z=rack_pitch/2; m6_clear=6.6; m6_head=11.5; web=2.5; relief_d=9; relief_l=10;
stop_y=pc_rear+0.8; stop_w=5;                       // rear stop face: 0.8 behind the seated case, before a foot can climb its ramp
id_d=0.6; font="Liberation Sans:style=Bold";

module capsule2d(len=10,diam=7){hull(){translate([-(len-diam)/2,0])circle(d=diam);translate([(len-diam)/2,0])circle(d=diam);}}
module plate_outline(){hull()for(sx=[-1,1],sz=[-1,1])translate([sx*(plate_w/2-plate_r),plate_bottom+plate_h/2+sz*(plate_h/2-plate_r)])circle(r=plate_r);}
module slots2d(){for(dz=[-hole_dz,hole_dz],x=[-hole_x,hole_x])translate([x,rack_pitch/2+dz])capsule2d();}

// ---- front sleeve
// Scoop, seen from above: open at the rear, narrowing toward the plate (Psychobob's idea, our numbers). Keeps both foot tracks.
module scoop2d(){offset(r=8)offset(delta=-8)polygon([[-34,10],[34,10],[46,38],[62,sleeve_d+20],[-62,sleeve_d+20],[-46,38]]);}
module sleeve_body(){
 for(s=[-1,1]) scale([s,1,1]){
  translate([win,0,z0])cube([wall,sleeve_d,z1-z0]);
  translate([0,0,z0])linear_extrude(z1-z0)polygon([[win+wall-0.01,-0.01],[front_gusset,-0.01],[win+wall-0.01,gusset_d]]);
 }
 difference(){
  union(){
   translate([-win-0.01,0,z0])cube([2*win+0.02,sleeve_d,floor_top-z0]);
   translate([-win-0.01,0,win_top])cube([2*win+0.02,sleeve_d,z1-win_top]);
  }
  translate([0,0,-1])linear_extrude(50)scoop2d();
 }
}
// Foot track from the sleeve rear to a solid stop; dip with a ramp on its rear side only (click-in), through the floor as in SLV-F.
module track_cuts(){
 for(t=tracks)translate([t[0],0,0]){
  translate([0,dip_y1+ramp-0.01,groove_z])cube([t[1]-t[0],sleeve_d-dip_y1-ramp+1,floor_top-groove_z+0.1]);
  rotate([90,0,90])linear_extrude(t[1]-t[0])polygon([[foot_stop_y,-0.1],[dip_y1,-0.1],[dip_y1+ramp,groove_z],[dip_y1+ramp,floor_top+0.1],[foot_stop_y,floor_top+0.1]]);
 }
}
module front_plate(){rotate([90,0,0])linear_extrude(plate_t)difference(){plate_outline();slots2d();translate([-win,floor_top])square([2*win,win_top-floor_top]);}}
module front_id(){translate([104.5,-4,22.2])rotate([90,0,0])translate([0,0,-id_d])linear_extrude(id_d+0.1)rotate(90)text("OPX-D-FRONT",size=3.5,font=font,halign="center",valign="center");}
module along_y(y0,y1){translate([0,y1,0])rotate([90,0,0])linear_extrude(height=y1-y0)children();}
// Runner on each sleeve wall; its rear end narrows over run_tip mm so it finds the rail.
module runner_profile(){polygon([[win+wall-0.01,rl_z0],[ru1,rl_z0],[ru1,rz_bot],[rb,rz_bot+rb-ru1],[rb,rz_mid],[ri,rz_mid+rb-ri],[win+wall-0.01,rz_mid+rb-ri]]);}
module runner(s){scale([s,1,1])intersection(){
 along_y(0,sleeve_d)runner_profile();
 translate([0,0,-1])linear_extrude(50)polygon([[0,0],[rb+1,0],[rb+1,sleeve_d-run_tip],[rb-2,sleeve_d],[0,sleeve_d]]);
}}
module front(){difference(){union(){front_plate();difference(){sleeve_body();track_cuts();}runner(-1);runner(1);}front_id();}}

// ---- post rail (drawn for the right side)
module channel_profile(){polygon([[ru1-1,rz_bot-cl_bear-1],[rb,rz_bot+rb-ru1-cl_bear],[rb+cl,rz_bot+rb-ru1-cl_bear],[rb+cl,rz_mid+cl*0.4],[ru1-1,rz_mid+cl*1.4+rb-ru1+1]]);}
module rail_round(){translate([0,0,-1])linear_extrude(100)offset(r=rail_r)offset(delta=-rail_r)
 polygon([[rl_in,rl_y0],[125,rl_y0],[125,rl_y0b],[rl_out,rl_y0b],[rl_out,rl_blk],[rl_wall,rl_blk],[rl_wall,rl_y1],[rl_in,rl_y1]]);}
module rail(s,t){scale([s,1,1])intersection(){rail_round();difference(){
 translate([rl_in,rl_y0,rl_z0])cube([rl_out-rl_in,rl_y1-rl_y0,rl_z1-rl_z0]);
 along_y(rl_y0-1,rl_y1+1)channel_profile();
 translate([hole_x,rl_y0-0.1,mid_z])rotate([-90,0,0])cylinder(d=m6_clear,h=web+0.2);                  // M6 x 8 from behind into the post's middle hole
 translate([hole_x,rl_y0+web,mid_z])rotate([-90,0,0])cylinder(d=m6_head,h=rl_blk);                    // head pocket, open to the rear
 for(dz=[-hole_dz,hole_dz])translate([hole_x,rl_y0-0.1,mid_z+dz])rotate([-90,0,0])cylinder(d=relief_d,h=relief_l); // plate screw tips
 translate([rl_in+0.6,35,28])rotate([90,0,-90])linear_extrude(1)mirror([s<0?1:0,0])text(t,size=4.5,font=font,halign="center",valign="center");
}}}

// ---- rear channel (drawn for the right side, s=+1; left is mirrored)
module ledge_plan(){polygon([[win+0.01,ch_y0],[win-ledge,ch_y0],[win-ledge,taper_y0],[win-ledge_rear,taper_y1],[win-ledge_rear,rack_depth],[win+0.01,rack_depth]]);}
module channel(s){
 scale([s,1,1])difference(){
  union(){
   translate([win,ch_y0,z0])cube([wall,rack_depth-ch_y0,z1-z0]);
   // Rear stop; its back face slopes so it prints ear-down without support.
   translate([0,0,z0])linear_extrude(z1-z0)polygon([[win+0.01,stop_y],[win-stop_w,stop_y],[win-stop_w,stop_y+1],[win+0.01,stop_y+1+stop_w]]);
   translate([0,0,z0])linear_extrude(floor_top-z0-0.2)ledge_plan();
   translate([0,0,roof_low])linear_extrude(z1-roof_low)ledge_plan();
   translate([0,0,z0])linear_extrude(z1-z0)polygon([[win+wall-0.01,rack_depth+0.01],[ear_web,rack_depth+0.01],[win+wall-0.01,rack_depth-gusset_d]]);
   translate([0,rack_depth+plate_t,0])rotate([90,0,0])linear_extrude(plate_t)difference(){
    intersection(){plate_outline();translate([win,-1])square([plate_w/2-win+1,50]);}
    slots2d();
    translate([hole_x,rack_pitch/2])capsule2d();   // middle screw: M6 x 8 into the rear post's middle hole
   }
  }
  // lead-in for the PC's rear end: floor, roof and web flare over the first lead_l mm
  rotate([90,0,90])translate([0,0,win-ledge-1])linear_extrude(ledge+1){
   polygon([[ch_y0-1,ledge_top-lead],[ch_y0,ledge_top-lead],[ch_y0+lead_l,ledge_top],[ch_y0-1,ledge_top]]);
   polygon([[ch_y0-1,roof_low+lead],[ch_y0,roof_low+lead],[ch_y0+lead_l,roof_low],[ch_y0-1,roof_low]]);
  }
  translate([0,0,-1])linear_extrude(50)polygon([[win-0.01,ch_y0-1],[win+lead,ch_y0-1],[win+lead,ch_y0],[win,ch_y0+lead_l],[win-0.01,ch_y0+lead_l]]);
 }
}
module rear_id(s,t){multmatrix([[-1,0,0,s*106],[0,0,1,rack_depth+plate_t],[0,1,0,22.2]])translate([0,0,-id_d])linear_extrude(id_d+0.1)rotate(90)text(t,size=3.5,font=font,halign="center",valign="center");}
module rear(s,t){difference(){channel(s);rear_id(s,t);}}

// ---- PC dummy (from Brian's measurements; rear add-ons read off his photos, approximate)
module pc(){
 x0=-pc_w/2; yc=pc_front+bz_t; z=floor_top;
 translate([x0,yc,z])cube([pc_w,pc_rear-yc,pc_h]);
 translate([x0,pc_front,z])cube([bz_w,bz_t+0.01,bz_h]);
 for(f=[[15,17.3],[162.5,17.3],[15,148],[162.5,148]])translate([x0+f[0],pc_front+f[1],z-2.8])cube([5,20,2.81]);
 for(a=[[13,4,4,14],[30,16,4,12],[70,14,11,10],[94,11,10,12]])translate([x0+a[0],pc_rear-0.01,z+14])cube([a[1],a[2],a[3]]);
}

if(part=="front")front();
else if(part=="rear_left")rear(-1,"OPX-D-L");
else if(part=="rear_right")rear(1,"OPX-D-R");
else if(part=="pc")pc();
else if(part=="rail_left")rail(-1,"OPX-D-RL");
else if(part=="rail_right")rail(1,"OPX-D-RR");
else if(part=="print_front")translate([0,0,plate_t])rotate([90,0,0])front();
else if(part=="print_rear_left")translate([0,0,rack_depth+plate_t])rotate([-90,0,0])rear(-1,"OPX-D-L");
else if(part=="print_rear_right")translate([0,0,rack_depth+plate_t])rotate([-90,0,0])rear(1,"OPX-D-R");
else{color("steelblue")front();color("orange"){rear(-1,"OPX-D-L");rear(1,"OPX-D-R");}color("gold"){rail(-1,"OPX-D-RL");rail(1,"OPX-D-RR");}color("dimgray")pc();}
