// MRT-C (2026-11-04): MRT-B with the rear braces replaced (Brian picked option A): the tray side walls reach back to small shoes on the rear posts.
// One piece: 1U faceplate + floor + side walls. Carries the ScreenBeam ECB7250 and the Bridgelink 2-way splitter.
// PROPOSED, MOCK-UP, UNPRINTED. Fit, heat, retention and strength are UNKNOWN. Plug lengths and cable diameters ASSUMED.
// Frame: x = 0..220 left to right seen from the front (rack X = x-110), y = 0 at the plate back, + to the rear,
// z = 0 at the slot bottom. Prints floor down, no supports.
// part: tray, shoe_left, shoe_right, screenbeam, splitter, cables
part="tray";
id="MRT-C";
$fn=64;

// ---- Faceplate: project standard (44.4/U, 252 wide, 4 thick, R2.5, four-corner slots)
u=1; rack_pitch=44.45; plate_gap=0.05; plate_w=252; plate_t=4; plate_r=2.5;
plate_h=u*rack_pitch-plate_gap; plate_center=u*rack_pitch/2; hole_x=118.2625; hole_dz=15.902;

// ---- Tray. Post flange inner faces are at rack X +-111.12 (4U post mesh), so 218 wide leaves 2.12 a side.
tx0=1; tx1=219; depth=172; tray_end_y=172; fl_z=0.025; fl_top=4; side_t=2.5; wall_top=24; wall_t=2; chan=10;
// ---- Retention lips: 45 deg underside, so they print without supports. The cable presses past from above.
lip_p=3.2; lip_pl=4.5;

// ---- ScreenBeam (Brian): 120 x 65 x 30 incl. feet; feet 2.25 proud, pockets as the receiver cradle. Coax end at the right.
SB=[120,65,30]; foot_h=2.25; foot_d=16; foot_dp=2.6; pad=2; sb_clr=0.5;
sbx0=70; sby0=6; case_z=fl_top+pad;
sb_feet=[for(x=[16,104],y=[8.5,56.5])[sbx0+x,sby0+y]];
coax_p=[sbx0+SB[0],sby0+SB[1]-22,case_z+15.25];
port_z=case_z+(SB[2]-foot_h)/2; lan_y=sby0+24; pwr_y=sby0+43;
lan_end=32; pwr_end=25;     // ASSUMED plug ends: LAN 38 long, power 45 long

// ---- Splitter (Brian's calipers, porch16.scad). Back face up on a 5.5 riser, IN to -x, OUTs to +x.
sp_l=38.75; sp_w=23; sp_base=7.5; sp_h=15.9; sp_axis=7.5; sp_out=22; sp_in_end=18.5; sp_port=13; sp_port_d=9.5;
sp_ear_l=48.5; sp_ear_s=14; sp_ear_hole=5; sp_ear_d=10; sp_ear_t=9;
riser=5.5; sp_z=fl_top+riser; xc=95; out1_y=118; yc=out1_y+sp_out/2; y0=yc-sp_l/2; in_y=y0+sp_in_end; out2_y=out1_y+sp_out;
axis_z=sp_z+sp_axis; x_in=xc-sp_w/2; x_out=xc+sp_w/2;
ears=[[xc+sp_ear_s/2,yc+sp_ear_l/2],[xc-sp_ear_s/2,yc-sp_ear_l/2]];
ins_d=4.2; ins_dp=4; boss_d=9.5;   // M3 x 3 x 5 insert standard

// ---- Channel centrelines, all bends R30
R=30; ra_reach=18.6; ra_tip=38.2;
ra_x=coax_p[0]+ra_reach; ra_tip_y=coax_p[1]+ra_tip;
c_jump=[ra_x-R,ra_tip_y+0.8];                 // jumper bend, angle 0..90; ends on y = out1_y
conn=26;                                      // ASSUMED straight F connector length past the port tip
c_out2=[x_out+sp_port+conn-13+2.5,out2_y+R];          // modem OUT bend, angle -90..0
c_in=[x_in-sp_port-2.5-conn+13,in_y+R];       // coax IN bend, angle 180..270
split_wall=c_in[0]-R-chan/2;                  // left channel inner face

module along(y0,y1){translate([0,y1,0])rotate([90,0,0])linear_extrude(height=y1-y0)children();}
module capsule2d(len=10,diam=7){hull(){translate([-(len-diam)/2,0])circle(d=diam);translate([(len-diam)/2,0])circle(d=diam);}}
module rr(x0,x1,y0,y1,r){translate([x0+r,y0+r])offset(r=r)square([x1-x0-2*r,y1-y0-2*r]);}
module plate2d(){difference(){
  hull()for(sx=[-1,1],sz=[-1,1])translate([sx*(plate_w/2-plate_r),plate_center+sz*(plate_h/2-plate_r)])circle(r=plate_r);
  for(dz=[-hole_dz,hole_dz],x=[-hole_x,hole_x])translate([x,rack_pitch/2+dz])capsule2d();
}}

// ---- Curved walls: inner and outer wall of one channel bend
module arc_wall(c,a0,da){translate([c[0],c[1],fl_top-0.01])rotate(a0)rotate_extrude(angle=da){
  translate([R-chan/2-wall_t,0])square([wall_t,wall_top-fl_top+0.01]);
  translate([R+chan/2,0])square([wall_t,wall_top-fl_top+0.01]);
}}
module wall_x(y,x0,x1){translate([x0,y,fl_top-0.01])cube([x1-x0,wall_t,wall_top-fl_top+0.01]);}
module wall_y(x,y0,y1){translate([x,y0,fl_top-0.01])cube([wall_t,y1-y0,wall_top-fl_top+0.01]);}

// ---- Lips. d = +1 points toward +r (or +x/+y), d = -1 the other way; face = the wall face it grows from.
module lip_prof(face,d,p){u=wall_top-p-0.5;polygon([[face-d*0.4,u],[face,u],[face+d*p,u+p],[face+d*p,wall_top],[face-d*0.4,wall_top]]);}
module arc_lip(c,a0,da,inner){translate([c[0],c[1],0])rotate(a0)rotate_extrude(angle=da)
  if(inner)lip_prof(R-chan/2,1,lip_p);else lip_prof(R+chan/2,-1,lip_p);}
module lip_y(face,d,p,y0,y1){translate([0,y1,0])rotate([90,0,0])linear_extrude(height=y1-y0)lip_prof(face,d,p);}
module lip_x(face,d,p,x0,x1){translate([x0,0,0])rotate([90,0,90])linear_extrude(height=x1-x0)lip_prof(face,d,p);}

// ---- Cable-tie slots: a pair across the channel; the tie goes down one, under the floor, up the other and around the cable.
module tie(p,ang,half){translate([p[0],p[1],fl_z-1])rotate(ang)for(s=[-1,1])translate([0,s*half,0])linear_extrude(fl_top-fl_z+1.5)
  offset(r=0.9)square([3.4,0.2],center=true);}
function on_arc(c,a)=[c[0]+R*cos(a),c[1]+R*sin(a)];

groove_tie=1.6; groove_strap=2;
module tie_groove(p,ang,half){translate([p[0],p[1],fl_z-1])rotate(ang)linear_extrude(1+groove_tie)offset(r=0.9)square([3.4,2*half],center=true);}
module strap_slot(x,y){translate([x-9,y,fl_z-1])cube([18,2.5,8.5]);}   // 16 mm Velcro, same as the rear cable lane

// ---- Rear support. The side walls run on to Y 220 and tie across with a low bar the cables pass over. Each wall tip has a 45 deg underside and
// seats on the ramp of a shoe bolted to the back of the rear post (2 M6 x 8, existing corner inserts, as the OptiPlex rear channels).
// No screw at the tip, so the plate alone sets the tray front to back. Vertical ear slots give +-1: tray home, raise the shoe until the tip just sits, tighten.
rack_depth=240; x_mid=110; ext_y0=166; wy=208; tip=220; bar_y0=198; bar_y1=206; flange_w=5.5;
seat_gap=0.15; side_gap=0.4; cap_gap=0.4; top_rise=2.5;
b_z0=1.1; b_z1=43.35; ear_t=4; ear_out=126; ear_slot=1; m6_clear=6.6;
s_x0=-0.9; s_x1=3.9; s_chk=tx0-side_gap; s_y0=wy-1; s_block=tip+1; cap_y0=212; chk_top=31;
function ramp_z(y)=y-wy+fl_z-seat_gap;
function cap_z(x)=wall_top+(x-tx0)+cap_gap;
module mir(m){if(m==1)translate([2*x_mid,0,0])mirror([1,0,0])children();else children();}
module rear_wall(){
  // wall carried on, underside rising at 45 deg over the last 12
  translate([tx0,0,0])rotate([90,0,90])linear_extrude(side_t)polygon([[ext_y0,fl_z],[wy,fl_z],[tip,tip-wy+fl_z],[tip,wall_top],[ext_y0,wall_top]]);
  // sloped top at the tip, the hold-down bears on it
  translate([0,tip,0])rotate([90,0,0])linear_extrude(tip-bar_y1)polygon([[tx0,wall_top-0.01],[tx0+side_t,wall_top-0.01],[tx0+side_t,wall_top+top_rise],[tx0,wall_top]]);
  // floor flange along the wall
  translate([tx0+side_t-0.01,ext_y0,fl_z])cube([flange_w,bar_y1-ext_y0,fl_top-fl_z]);
}
module shoe(tag){difference(){union(){
  translate([s_x0,s_block,b_z0])cube([s_x1-s_x0,rack_depth+ear_t-s_block,b_z1-b_z0]);
  translate([x_mid,rack_depth+ear_t,0])rotate([90,0,0])linear_extrude(ear_t)hull(){
    for(z=[b_z0+plate_r,b_z1-plate_r])translate([-ear_out+plate_r,z])circle(r=plate_r);
    translate([s_x0-x_mid,b_z0])square([0.01,b_z1-b_z0]);}
  // cheek outside the wall, lead-in at its front
  translate([0,0,b_z0])linear_extrude(chk_top-b_z0)polygon([[s_x0,s_y0],[s_chk-0.8,s_y0],[s_chk,s_y0+2],[s_chk,s_block+0.01],[s_x0,s_block+0.01]]);
  // ramp under the tip
  translate([s_chk-0.01,0,0])rotate([90,0,90])linear_extrude(s_x1-s_chk+0.01)polygon([[wy+b_z0-fl_z+seat_gap,b_z0],[s_block+0.01,ramp_z(s_block+0.01)],[s_block+0.01,b_z0]]);
  // hold-down over the tip, 45 deg underside
  translate([0,s_block+0.01,0])rotate([90,0,0])linear_extrude(s_block+0.01-cap_y0)polygon([[s_chk-0.01,cap_z(s_chk)],[s_x1,cap_z(s_x1)],[s_x1,chk_top],[s_chk-0.01,chk_top]]);
 }
 for(dz=[-hole_dz,hole_dz])translate([x_mid-hole_x,rack_depth-1,rack_pitch/2+dz])rotate([-90,0,0])hull()for(k=[-1,1])translate([0,k*ear_slot,0])cylinder(d=m6_clear,h=ear_t+2);
 translate([x_mid-hole_x,rack_depth+ear_t-0.6,rack_pitch/2])rotate([90,0,180])rotate([0,0,90])linear_extrude(1)text(tag,size=3,font="Liberation Sans:style=Bold",halign="center",valign="center");
}}
module tray(){difference(){
  union(){
    // plate, with the rack holes; tray parts run behind it
    translate([110,0,0])along(-plate_t,0)plate2d();
    // floor
    translate([0,0,fl_z])linear_extrude(fl_top-fl_z)union(){rr(tx0,tx1,0,depth,4);translate([tx0,0])square([tx1-tx0,10]);}
    // side walls, tied into the plate by a chamfer
    for(x=[tx0,tx1-side_t])translate([x,0,fl_z])cube([side_t,depth-4,wall_top-fl_z]);
    for(s=[0,1])translate([s==0?tx0+side_t-0.01:tx1-side_t-6.01,0,fl_top-0.01])
      linear_extrude(wall_top-fl_top+0.01)polygon(s==0?[[0,0],[6,0],[0,6]]:[[0,0],[6,0],[6,6]]);
    // floor-to-plate chamfer across the width
    translate([tx0,0,0])rotate([90,0,90])linear_extrude(tx1-tx0)polygon([[-0.01,fl_top-0.01],[5,fl_top-0.01],[-0.01,fl_top+5]]);
    for(m=[0,1])mir(m)rear_wall();
    translate([tx0,bar_y0,fl_z])cube([tx1-tx0,bar_y1-bar_y0,fl_top-fl_z]);
    // ScreenBeam: foot pads and long-side fences
    for(f=sb_feet)translate([f[0],f[1],fl_top-0.01])cylinder(d=22,h=pad+0.01);
    for(y=[sby0-sb_clr/2-2,sby0+SB[1]+sb_clr/2])translate([sbx0+15,y,fl_top-0.01])cube([SB[0]-30,2,pad+6]);
    // splitter riser and ear bosses
    translate([xc-sp_w/2+2,y0+2,fl_top-0.01])cube([sp_w-4,sp_l-4,riser+0.01]);
    for(e=ears)translate([e[0],e[1],fl_top-0.01])cylinder(d=boss_d,h=riser+0.01);
    // jumper channel
    arc_wall(c_jump,0,90);
    wall_x(c_jump[1]+R+chan/2,c_jump[0]-34,c_jump[0]+0.01);
    wall_x(c_jump[1]+R-chan/2-wall_t,c_jump[0]-34,c_jump[0]+0.01);
    arc_lip(c_jump,38,18,true); arc_lip(c_jump,60,18,false);
    lip_x(c_jump[1]+R-chan/2,1,lip_p,c_jump[0]-14,c_jump[0]-4);
    lip_x(c_jump[1]+R+chan/2,-1,lip_p,c_jump[0]-30,c_jump[0]-20);
    // modem OUT channel
    arc_wall(c_out2,-90,90);
    wall_y(c_out2[0]+R-chan/2-wall_t,c_out2[1]-0.01,depth);
    wall_y(c_out2[0]+R+chan/2,c_out2[1]-0.01,depth);
    arc_lip(c_out2,-82,18,true); arc_lip(c_out2,-60,18,false); arc_lip(c_out2,-26,18,true);
    // coax IN channel
    arc_wall(c_in,180,90);
    wall_y(c_in[0]-R-chan/2-wall_t,c_in[1]-0.01,depth);
    wall_y(c_in[0]-R+chan/2,c_in[1]-0.01,depth);
    arc_lip(c_in,244,18,true); arc_lip(c_in,222,18,false); arc_lip(c_in,188,18,true);
    // power + LAN channel: long inner wall, tray side wall on the other side
    wall_y(split_wall-wall_t,70,c_in[1]);
    lip_y(tx0+side_t,1,lip_pl,82,92); lip_y(split_wall-wall_t,-1,lip_pl,102,112);
    lip_y(tx0+side_t,1,lip_pl,122,132); lip_y(split_wall-wall_t,-1,lip_pl,142,152);
  }
  // ScreenBeam foot pockets
  for(f=sb_feet)translate([f[0],f[1],case_z-foot_dp])cylinder(d=foot_d,h=foot_dp+pad);
  // Velcro strap slots around the ScreenBeam
  for(x=[sbx0+30,sbx0+90]){strap_slot(x,0.8);strap_slot(x,sby0+SB[1]+sb_clr/2+2.3);}
  // insert bores in the splitter bosses
  for(e=ears)translate([e[0],e[1],sp_z-ins_dp])cylinder(d=ins_d,h=ins_dp+1);
  // cable-tie slots
  tie(on_arc(c_jump,28),28+90,3.5); tie(on_arc(c_out2,-38),-38+90,3.5); tie(on_arc(c_in,206),206+90,3.5);
  tie([(tx0+side_t+split_wall-wall_t)/2,100],90,5.5); tie([(tx0+side_t+split_wall-wall_t)/2,138],90,5.5);
  // tie slots in the rear bar for the cords and both coax runs
  for(x=[11,c_in[0]-R,c_out2[0]+R]){tie([x,(bar_y0+bar_y1)/2],90,5.5);tie_groove([x,(bar_y0+bar_y1)/2],90,5.5);}
  // floor windows
  translate([0,0,fl_z-1])linear_extrude(fl_top-fl_z+1.01){
    rr(sbx0+30,sbx0+90,sby0+13,sby0+52,6);
    rr(32,sbx0+60,78,99,6);
    rr(178,212,134,165,6);
  }
  // Grooves under the floor: ties and straps pass under without reaching the slot below
  tie_groove(on_arc(c_jump,28),28+90,3.5); tie_groove(on_arc(c_out2,-38),-38+90,3.5); tie_groove(on_arc(c_in,206),206+90,3.5);
  tie_groove([(tx0+side_t+split_wall-wall_t)/2,100],90,5.5); tie_groove([(tx0+side_t+split_wall-wall_t)/2,138],90,5.5);
  for(x=[sbx0+30,sbx0+90])translate([x-9,0.8,fl_z-1])cube([18,sby0+SB[1]+sb_clr/2+2.3+2.5-0.8,1+groove_strap]);
  // ID on the floor top, open area left of the splitter
  translate([66,160,fl_top-0.6])linear_extrude(1)text(id,size=5,font="Liberation Sans:style=Bold",halign="center",valign="center");
}}

// ---- Context models
module screenbeam(){
  translate([sbx0,sby0,case_z])cube([SB[0],SB[1],SB[2]-foot_h]);
  for(f=sb_feet)translate([f[0],f[1],case_z-foot_h])cylinder(d=13,h=foot_h+0.01);
  translate([coax_p[0]-0.01,coax_p[1],coax_p[2]])rotate([0,90,0])cylinder(d=9.5,h=11);
}
module splitter(){
  translate([x_in,y0,sp_z])cube([sp_w,sp_l,sp_h]);
  for(y=[out1_y,out2_y])translate([x_out-0.01,y,axis_z])rotate([0,90,0])cylinder(d=sp_port_d,h=sp_port);
  translate([x_in+0.01,in_y,axis_z])rotate([0,-90,0])cylinder(d=sp_port_d,h=sp_port);
  for(e=ears)translate([e[0],e[1],sp_z])difference(){
    union(){cylinder(d=sp_ear_d,h=sp_ear_t);hull(){cylinder(d=sp_ear_d,h=sp_ear_t);translate([xc-e[0],yc-e[1],0])cylinder(d=sp_ear_d,h=sp_ear_t);}}
    translate([0,0,-1])cylinder(d=sp_ear_hole,h=sp_ear_t+2);
  }
}
module rod(a,b,d){hull(){translate(a)sphere(d=d,$fn=24);translate(b)sphere(d=d,$fn=24);}}
module run(pts,d){for(i=[0:len(pts)-2])rod(pts[i],pts[i+1],d);}
function arc_pts(c,a0,a1,z0,z1,n=8)=[for(i=[0:n])let(t=i/n,a=a0+(a1-a0)*t)[c[0]+R*cos(a),c[1]+R*sin(a),z0+(z1-z0)*t]];
coax_d=7; rest=fl_top+coax_d/2+1;
module cables(){
  // right-angle F on the ScreenBeam (Brian's reach and tip numbers)
  rod(coax_p,[ra_x,coax_p[1],coax_p[2]],12); rod([ra_x,coax_p[1],coax_p[2]],[ra_x,ra_tip_y-6,coax_p[2]],12);
  // jumper: right-angle F, bend, straight into OUT1
  run(concat([[ra_x,ra_tip_y-6,coax_p[2]]],arc_pts(c_jump,0,90,coax_p[2]-3,rest+3),[[x_out+sp_port+conn-13,out1_y,axis_z]]),coax_d);
  // modem coax out of OUT2, IN coax into IN, each with an F connector at the port
  run(concat([[x_out+sp_port,out2_y,axis_z]],arc_pts(c_out2,-90,0,rest+4,rest),[[c_out2[0]+R,245,rest]]),coax_d);
  run(concat([[x_in-sp_port,in_y,axis_z]],arc_pts(c_in,270,180,rest+4,rest),[[c_in[0]-R,245,rest]]),coax_d);
  for(p=[[x_out+sp_port-1,out1_y],[x_out+sp_port-1,out2_y]])translate([p[0],p[1],axis_z])rotate([0,90,0])cylinder(d=11.5,h=13);
  translate([x_in-sp_port+1,in_y,axis_z])rotate([0,-90,0])cylinder(d=11.5,h=13);
  // power plug and cord (ASSUMED 45 long, 5 cord), LAN plug and cord (ASSUMED 38 long, 6 cord)
  translate([pwr_end,pwr_y-6,port_z-6])cube([sbx0-pwr_end,12,12]);
  translate([lan_end,lan_y-8,port_z-7])cube([sbx0-lan_end,16,14]);
  rp=11; lp=24; cx=(tx0+side_t+split_wall-wall_t)/2;
  run(concat([for(i=[0:6])let(a=90-i*15)[pwr_end-rp*sin(90-a),pwr_y+rp-rp*cos(90-a),port_z-i*1.8]],[[pwr_end-rp,pwr_y+rp+20,fl_top+4],[pwr_end-rp,245,fl_top+4]]),5);
  run(concat([for(i=[0:6])let(a=90-i*15)[lan_end-lp*sin(90-a),lan_y+lp-lp*cos(90-a),port_z-i*1.6]],[[lan_end-lp,lan_y+lp+20,fl_top+4],[lan_end-lp,245,fl_top+4]]),6);
}
if(part=="tray")tray();
if(part=="shoe_left")shoe("MRT-C-L");
if(part=="shoe_right")mir(1)shoe("MRT-C-R");
if(part=="screenbeam")screenbeam();
if(part=="splitter")splitter();
if(part=="cables")cables();
if(part=="clash_devices")intersection(){tray();union(){screenbeam();splitter();}}
if(part=="clash_cables")intersection(){tray();cables();}
