// CBL-B/C/D/E (2026-10-31): companions to CBL-A. Same frame (X centred, Y=0 rear face of the rear posts, +Y rearward, Z=0 slot bottom).
//  B  exit chute   : a CBL-A module with a flared chute below it (bottom-rear cable exit). Goes on U1 (conflicts with the RW standoffs there).
//  C  strip ledge  : plate + web + ledge; a left/right pair carries a power strip / DC block across the rear (strip_w deep, <= ~200 long).
//  D  patch comb   : 1U blanking faceplate (44.4 x 252 x 4, four corner holes) with a comb along the bottom for front patch cords.
//  E  window comb  : plug-in comb for a CBL-A inner-wall window; splits the cords entering sideways into three lanes.
// Strip size and comb pitch are GUESSES (parameters). Fit, capacity, retention and strength UNKNOWN. Not printed.
include <CBL-A.scad>

// ---- B
chute_h=36; flare=6;
module chute(){
  z0=mid-mh/2;
  difference(){
    hull(){translate([u0,0,z0])cube([u1-u0,depth,0.01]);translate([u0-flare,0,z0-chute_h])cube([u1-u0+2*flare,depth+flare,0.01]);}
    hull(){translate([u0+wall,t_pl,z0+0.02])cube([u1-u0-2*wall,depth,0.01]);
           translate([u0-flare+wall,t_pl,z0-chute_h-0.02])cube([u1-u0+2*flare-2*wall,depth+flare,0.01]);}
  }
}
module partB(){union(){module_r();chute();}}

// ---- C
strip_w=50;            // strip depth (Y), UNKNOWN: measure the real strip / block
ledge_in=16; ledge_t=3.5; web=3; lip_h=10;
module partC_solid(){
  z0=mid-mh/2; ly=4+strip_w+4;
  difference(){
    union(){
      translate([u0,0,z0])cube([u1-u0,t_pl,mh]);                         // plate on the post
      translate([u0-web,0,z0])cube([web+0.01,ly,mh]);                    // web: stiffens the arm and stops the strip end
      translate([u0-ledge_in,0,z0])cube([ledge_in,ly,ledge_t]);          // ledge the strip rests on
    }
    for(dz=[-hole_dz,hole_dz])translate([hx,-1,mid+dz])rotate([-90,0,0])cylinder(d=m6_clear,h=t_pl+2);
    for(y=[0.6,4+strip_w+0.6])translate([u0-ledge_in+2,y,mid-mh/2-1])cube([ledge_in-web-4,strap_t,ledge_t+2]);  // strap slots either side of the strip
  }
}
module partC(){ // text is placed in world coordinates so it reads correctly on both sides
  z0=mid-mh/2;
  difference(){
    scale([s,1,1])partC_solid();
    translate([s*(u0-ledge_in/2),(4+strip_w+4)/2,z0+ledge_t-0.6])linear_extrude(1)
      text("CBL-C",size=2.6,font="Liberation Sans:style=Bold",halign="center",valign="center");
  }
}

// ---- D
pw=252; ph=44.4; pt=4; pr=2.5; fpitch=12; fw=4; fdepth=10; nf=8;
module partD2(){
  z0=(44.45-ph)/2;
  difference(){
    union(){
      translate([0,0,z0])rotate([90,0,0])linear_extrude(pt)offset(r=pr)offset(delta=-pr)translate([-pw/2,0])square([pw,ph]);   // plate, front face Y=-4
      // comb: base bar along the bottom with fingers, in front of the plate (towards -Y); 0.5 mm overlap into the plate
      translate([-100,-pt-fdepth,z0+4])cube([200,fdepth+0.5,3]);
      for(i=[-nf:nf])translate([i*fpitch-fw/2,-pt-fdepth,z0+4])cube([fw,fdepth*0.4,16]);
    }
    for(sx=[-1,1],dz=[-hole_dz,hole_dz])translate([sx*hx,1,mid+dz])rotate([90,0,0])cylinder(d=m6_clear,h=pt+2);
    translate([0,-pt+0.6,z0+ph-8])rotate([90,0,0])linear_extrude(1)
      text("CBL-D",size=4,font="Liberation Sans:style=Bold",halign="center",valign="center");   // 0.6 deep into the front face
  }
}

// ---- E
module partE_solid(){
  z0=mid-9.8; hgt=19.6; y0=6.2; y1=16.8; lane=8.2; rib=1.6;
  difference(){
    union(){
      translate([u0-20,y0,z0])cube([20+wall+3,y1-y0,hgt]);                // body through the window, 3 mm into the trough
      translate([u0-2,y0-1.7,mid-14])cube([2,y1-y0+3.4,28]);               // flange against the wall's outer face
    }
    // two cord lanes (8.2 high, 1.6 rib), open to the rack side, closed by a 1.6 mm web at the rear
    for(k=[0:1])translate([u0-21,y0+0.01,z0+0.8+k*(lane+rib)])cube([20+wall+3+1,y1-y0-1.6-0.01,lane]);
  }
}
module partE(){
  tx=(s>0)?u0-2+0.6:-(u0-2)-0.6;
  difference(){
    scale([s,1,1])partE_solid();
    translate([tx,(6.2+16.8)/2,mid+11.9])rotate(s>0?[90,0,-90]:[90,0,90])linear_extrude(1)
      text("CBL-E",size=2.4,font="Liberation Sans:style=Bold",halign="center",valign="center");
  }
}

if(part=="B")translate([0,0,uz*44.45])scale([s,1,1])partB();
if(part=="C")translate([0,0,uz*44.45])partC();
if(part=="D")translate([0,0,uz*44.45])partD2();
if(part=="E")translate([0,0,uz*44.45])partE();
