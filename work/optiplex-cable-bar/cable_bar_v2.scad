// DRAFT (2026-11-11) copied from OPX-G for the rear cable bar: variant D (slide rail, chosen by Brian; E and F are in git history). The OPX-G part list below is unchanged.
// OPX-G: new rear channels only, with a cable pass-through window in each web (Brian, 2026-11-04). Used with the printed OPX-D sleeve and printed OPX-F rails (good fit, Brian), whose modules are unchanged here and keep their IDs. Unprinted; fit and strength UNKNOWN.
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
rail_loose=1.0;                                 // OPX-F: channel moved 1.0 outward on each rail vs OPX-D, adds 1.0 on the ledge, outer wall and hold-down (OPX-E was 0.5)
rl_in=103+rail_loose-0.5; rl_wall=111; rl_out=126.9; rl_z0=0.5; rl_z1=44; rl_y0=6.2; rl_y0b=11.8; rl_blk=38; rl_y1=60; rail_r=3;
mid_z=rack_pitch/2; m6_clear=6.6; m6_head=11.5; web=2.5; relief_d=9; relief_l=10;
stop_y=pc_rear+0.8; stop_w=5;                       // rear stop face: 0.8 behind the seated case, before a foot can climb its ramp
// Cable window through the web, behind the rear stop and ahead of the gusset. Front end is a 45 degree peak so it prints ear-down without support.
win_y0=180; win_y1=194; win_y2=212; win_z0=8.2; win_z1=36.2; win_r=3;
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
module channel_profile(){translate([rail_loose,0])polygon([[ru1-1,rz_bot-cl_bear-1],[rb,rz_bot+rb-ru1-cl_bear],[rb+cl,rz_bot+rb-ru1-cl_bear],[rb+cl,rz_mid+cl*0.4],[ru1-1,rz_mid+cl*1.4+rb-ru1+1]]);}
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
// D (2026-11-11, Brian: more room where the cables meet the bar): window runs back to Y 234 above the rail, both faces
// rounded over 2 mm, and the gusset gets a matching pocket so cables leave the window straight to the side.
wD_rear=234; wD_low=15.2; wch=1; wD_ramp0=204;   // ramp from Z 8.2 at Y 204 up to Z 15.2 at the rail's front end (219)
wD_rc=8;                                          // radius on the window's inside (concave) corners
// One smooth outline (Brian, 2026-11-11: the stepped version looked horrid): every corner rounded, 1 mm edge break on
// both faces, and the gusset cut to the same outline 1 mm larger.
module windowD2d(){offset(r=win_r)offset(delta=-win_r)offset(r=-wD_rc)offset(delta=wD_rc)
 polygon([[win_y0,(win_z0+win_z1)/2],[win_y1,win_z0],[wD_ramp0,win_z0],[dt_y0,wD_low],[wD_rear,wD_low],[wD_rear,win_z1],[win_y1,win_z1]]);}
module xslab(x0,t){rotate([90,0,90])translate([0,0,x0])linear_extrude(t)children();}
module window_cut(){
 if(variant=="D"){
  xslab(win-0.5,wall+1)windowD2d();
  // 45 deg edge break that follows the outline (hull() would fill the ramp's hollow and shave the wall under it)
  minkowski(){xslab(win-0.5,0.5)windowD2d();rotate([0,90,0])cylinder(h=wch,r1=wch,r2=0,$fn=12);}
  minkowski(){xslab(win+wall,0.5)windowD2d();rotate([0,-90,0])cylinder(h=wch,r1=wch,r2=0,$fn=12);}
  xslab(win+wall-0.01,ear_web-win-wall+1)offset(r=3)windowD2d();           // gusset cut to the window outline, 3 clear
  translate([win+wall-0.01,rack_depth-gusset_d-1,z0-1])cube([ear_web-win-wall+1,222-(rack_depth-gusset_d-1),z1-z0+2]);   // blunt gusset start at Y 222, no thin tip
 } else xslab(win-0.5,wall+1)cable_window2d();
}
module cable_window2d(){offset(r=win_r)offset(delta=-win_r)polygon([[win_y0,(win_z0+win_z1)/2],[win_y1,win_z0],[win_y2,win_z0],[win_y2,win_z1],[win_y1,win_z1]]);}
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
  window_cut();
  // lead-in for the PC's rear end: floor, roof and web flare over the first lead_l mm
  rotate([90,0,90])translate([0,0,win-ledge-1])linear_extrude(ledge+1){
   polygon([[ch_y0-1,ledge_top-lead],[ch_y0,ledge_top-lead],[ch_y0+lead_l,ledge_top],[ch_y0-1,ledge_top]]);
   polygon([[ch_y0-1,roof_low+lead],[ch_y0,roof_low+lead],[ch_y0+lead_l,roof_low],[ch_y0-1,roof_low]]);
  }
  translate([0,0,-1])linear_extrude(50)polygon([[win-0.01,ch_y0-1],[win+lead,ch_y0-1],[win+lead,ch_y0],[win,ch_y0+lead_l],[win-0.01,ch_y0+lead_l]]);
 }
}
module rear_id(s,t){multmatrix([[-1,0,0,s*106],[0,0,1,rack_depth+plate_t],[0,1,0,22.2]])translate([0,0,-id_d])linear_extrude(id_d+0.1)rotate(90)text(t,size=3.5,font=font,halign="center",valign="center");}
module rear(s,t){difference(){union(){channel(s);scale([s,1,1])bar_mount();}rear_id(s,t);}}
variant="D";   // D, or G for the OPX-G channels as designed

// ================= rear cable bar, bracket variants (drawn for the right side) =================
bz=3.6;                       // bar bottom, 0.3 above the floor ledge (3.3)
by0=214; by1=236;             // trough: 42 behind the PC's rear (171.7) for plugs
bend=80;                      // body ends / end blocks start
cb=0.3;                       // sliding clearance
end_top=14.6;                   // end blocks stay low: cables from the window pass over them into the trough
module along_x(x0,x1){translate([x0,0,0])rotate([90,0,90])linear_extrude(x1-x0)children();}
// Zip-tie slots (Brian, 2026-11-11), 5.5 x 2.6 for ties up to about 4.8 wide. At each station a tie can wrap the
// floor/wall corner of either lane (front wall or back lip slot + floor slot next to the divider), and up the front
// wall two more slots hold a stacked bundle against it. Ties pass under the bar: 3.6 clear below it.
tie_w=5.5; tie_t=2.6; band_w=6; tie_d=1.2; tie_x=[-68,-45,-15,15,45,68];
module tie_slots(){for(x=tie_x){
 for(z=abs(x)<=52?[8.2,15.5,23.5]:[8.2])translate([x-tie_w/2,by0-1,z])cube([tie_w,5,tie_t]);      // front wall
 translate([x-tie_w/2,by1-4,7.6])cube([tie_w,5,tie_t]);                                           // back lip
 for(y=[221.2,226.2])translate([x-tie_w/2,y,bz-1])cube([tie_w,tie_t,5]);                           // floor, beside the divider
 // band recesses (Brian, 2026-11-11): tie_d deep, so the band sits flush on the front face, under the floor and on the back lip
 translate([x-band_w/2,by0-1,bz-1])cube([band_w,1+tie_d,(abs(x)<=52?23.5:8.2)+tie_t-(bz-1)]);       // front face, up to the top slot
 translate([x-band_w/2,by0-1,bz-1])cube([band_w,by1-by0+2,1+tie_d]);                                 // underside, front to back
 translate([x-band_w/2,by1-tie_d,bz-1])cube([band_w,tie_d+1,7.6+tie_t-(bz-1)]);                       // back face of the lip
}}
 // Walls with every exposed edge rounded (Brian, 2026-11-11): top, slope and the corners between them. The part below
// the bed is cut off, so the faces stay flat down to the bed; the wall ends run into the end blocks.
module round_wall(y,t,h,xf,r){intersection(){
 minkowski(){translate([0,y+t-r,0])rotate([90,0,0])linear_extrude(t-2*r)offset(delta=-r)
   polygon([[-82,bz-3],[82,bz-3],[82,bz+3],[xf,h],[-xf,h],[-82,bz+3]]);sphere(r=r,$fn=16);}
 translate([-200,y-1,bz])cube([400,t+2,50]);}}
module troughD(){difference(){union(){
 along_x(-bend-0.01,bend+0.01)translate([by0,bz])square([by1-by0,3]);
 round_wall(by0,3,30,52,1.4);     // front wall full height inside X +-52, slopes to the floor at the end blocks
 round_wall(224,2,22,58,0.9);     // divider
 round_wall(by1-3,3,13,82,1.4);   // back lip
 } tie_slots();}}

// D: dovetail rail on each web's inner face. The bar slides on from the rear: the rail enters the open front of the
// bar's groove, the groove's closed rear end stops on the rail's rear end (Y 240), and a spring leaf in the groove's
// inner wall clicks its nub into a dimple in the rail's tip face. Pull firmly to remove (grip UNKNOWN).
dt_tip=win-4;                                                   // 87.75: rail tip face, 4 proud of the web
dt=[[win+0.01,7.1],[dt_tip,5.6],[dt_tip,12.6],[win+0.01,11.1]];   // lowered 2026-11-11 so the end block can drop to 14.6     // x,z: wider at the tip
nub_on=true;   // false: bar without the nub, for the slide-in sweep check
dt_y0=219; dt_y1=rack_depth;                                    // rail Y 219..240
nub_y=dt_y0+3; nub=1.2; dimple=1.4;                             // click position, nub height, dimple depth
leaf_t=1.5; leaf_gap=2.5; leaf_y1=238; leaf_z0=6.2; leaf_z1=11.8;   // cantilever rooted at Y 238, 5 mm ahead of the block's rear face
blk_y0=by0-3; blk_y1=dt_y1+cb+3; blk_r=2;                       // end block Y 211..243.3
module D_mount(){difference(){
  translate([0,dt_y1,0])rotate([90,0,0])linear_extrude(dt_y1-dt_y0)polygon(dt);
  translate([dt_tip,nub_y,9.1])rotate([0,90,0])cylinder(d=3.2,h=2*dimple,center=true);          // dimple for the nub
  // 1 mm lead-ins on the rail's rear (entry) end: tip face and top/bottom edges
  translate([0,dt_y1+0.01,0])rotate([90,0,0])linear_extrude(1.2,scale=1)difference(){square([200,30]);offset(delta=-1)polygon(dt);}
 }}
module D_end(){
 x1=win-cb;                                                       // 91.45
 difference(){
  hull(){translate([0,0,bz])linear_extrude(end_top-bz-2)offset(r=blk_r)offset(delta=-blk_r)translate([bend,blk_y0])square([x1-bend,blk_y1-blk_y0]);
        translate([0,0,end_top-0.01])linear_extrude(0.01)offset(r=blk_r)offset(delta=-blk_r-2)translate([bend,blk_y0])square([x1-bend,blk_y1-blk_y0]);}   // top edges chamfered 2
  translate([0,dt_y1+cb,0])rotate([90,0,0])linear_extrude(dt_y1+cb-blk_y0+1)offset(delta=cb)polygon(dt);   // groove: open in front, closed at the rear
  translate([0,blk_y0+1.5,0])rotate([90,0,0])linear_extrude(1.6)offset(delta=1+cb)polygon(dt);  // entry chamfer in front
  // free the spring leaf: slot behind it and slits above and below
  lx0=dt_tip-cb-leaf_t;
  translate([lx0-leaf_gap,blk_y0-1,leaf_z0-0.6])cube([leaf_gap,leaf_y1-blk_y0+1,leaf_z1-leaf_z0+1.2]);
  for(z=[leaf_z0-0.6,leaf_z1])translate([lx0-0.01,blk_y0-1,z])cube([leaf_t+0.02,leaf_y1-blk_y0+1,0.6]);
 }
 // nub on the leaf's free end, facing the rail
 if(nub_on)translate([dt_tip-cb,nub_y,9.1])scale([nub/1.5,1,1])sphere(d=3,$fn=24);
}
module bar_mount(){if(variant=="D")D_mount();}
module bar(){
 if(variant=="D"){troughD();D_end();mirror([1,0,0])D_end();}

}

// ---- PC dummy (from Brian's measurements; rear add-ons read off his photos, approximate)
module pc(){
 x0=-pc_w/2; yc=pc_front+bz_t; z=floor_top;
 translate([x0,yc,z])cube([pc_w,pc_rear-yc,pc_h]);
 translate([x0,pc_front,z])cube([bz_w,bz_t+0.01,bz_h]);
 for(f=[[15,17.3],[162.5,17.3],[15,148],[162.5,148]])translate([x0+f[0],pc_front+f[1],z-2.8])cube([5,20,2.81]);
 for(a=[[13,4,4,14],[30,16,4,12],[70,14,11,10],[94,11,10,12]])translate([x0+a[0],pc_rear-0.01,z+14])cube([a[1],a[2],a[3]]);
}

if(part=="bar")bar();
else if(part=="sweep")for(dy=[0:2:40])translate([0,dy,0])bar();   // bar positions while sliding in from the rear
else if(part=="front")front();
else if(part=="rear_left")rear(-1,"OPX-G-L");
else if(part=="rear_right")rear(1,"OPX-G-R");
else if(part=="pc")pc();
else if(part=="rail_left")rail(-1,"OPX-F-RL");
else if(part=="rail_right")rail(1,"OPX-F-RR");
else if(part=="print_front")translate([0,0,plate_t])rotate([90,0,0])front();
else if(part=="print_rear_left")translate([0,0,rack_depth+plate_t])rotate([-90,0,0])rear(-1,"OPX-G-L");
else if(part=="print_rear_right")translate([0,0,rack_depth+plate_t])rotate([-90,0,0])rear(1,"OPX-G-R");
else{color("steelblue")front();color("orange"){rear(-1,"OPX-G-L");rear(1,"OPX-G-R");}color("gold"){rail(-1,"OPX-F-RL");rail(1,"OPX-F-RR");}color("dimgray")pc();}
