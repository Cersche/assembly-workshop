// Fan junction box DRAFT (2026-11-07): receiver (JBR) on the right rear post + Wago case (JBC) + lid.
// Viewer-only draft per work/fan-junction-box/Spec.md. Nothing released or printed. No IDs modelled yet (drafts get none).
// Frame = rack frame of rack_top_fan.scad: X centred, Y 0 front .. 240 rear, Z 0 = bottom of slot 9,
// post tops / slot 1 top Z 400.05. Right rear post: flange X 111.12..143, Y 234..240; side wall X 127.12..143
// from Y 205; inner fillet X 124.5..127.1, Y 231.2..234 (source mesh values, docs/devices/lab-rax-4u-post.md).
// Fit, strength, cleat play, insert fit and wire retention are UNKNOWN.
include <workshop.scad>
include <BOSL2/std.scad>
part="assembly";   // receiver | case | lid | keepout | wagos | assembly
$fn=48;

// ---- post interface (source values, not measured)
y_post=234; x_flange=111.12; hole=[118.26,377.8];   // U9 middle hole: X, Z (7.6 insert bore in the post, insert present UNKNOWN)
x_fillet=124.5; y_fillet=231.2; x_side=127.12;

// ---- clearances (draft guesses; dovetail fit UNKNOWN until a coupon prints)
c_dt=0.3;      // dovetail cleat to channel, each flank and at the tip
c_face=0.3;    // case back to receiver front, lip to receiver bottom
c_post=0.3;    // receiver to the flange edge
// ---- Wago 221-413 (datasheet, Brian 2026-11-07: use it): W across levers x D entry to back x H lever closed
wago=[18.7,18.6,8.3]; wago_fit=0.4; wago_gap=1.6;
side_room=2;   // draft 4 (Brian): room between the outer Wagos and the side walls for the outer wires
wire_room=16;  // draft 4: 12 + 4 for the floor tie anchor behind the slot

// ---- case (Z chosen so the receiver covers the M6 head recess, Z 372.05..383.55, with ~2 mm left each side)
wall=2; floor_t=2; inner_h=12; lid_t=2.5;
zc0=366; zc_lid=zc0+floor_t+inner_h; zc1=zc_lid+lid_t;           // 366 / 380 / 382.5
cx1=124.0; cy1=223.0;          // +X side (post side wall X 127.12) and case back stay put; growth goes to -X and the front
cx0=cx1-(2*wall+2*wago[0]+wago_gap+2*wago_fit+2*side_room);     // 76.4
cy0=cy1-(2*wall+wire_room+wago[1]+wago_fit);                    // 184.0
r_bed=3;                                                         // rounded bed corners (Brian, 2026-11-05)

// ---- receiver
yr0=cy1+c_face;               // receiver front face 223.3
web=ws_m6_web; head_d=ws_m6_head_d; head_room=4.3;               // button head ~3.3 high + 1 mm
yf=y_post-web-head_room;      // dovetail channel floor 227.2 (same depth as the head counterbore bottom)
dt_x=102; dt_m=10; dt_ang=30; // channel centre X, mouth width, flank undercut
dt_hm=dt_m/2; dt_hf=dt_hm+(yf-yr0)*tan(dt_ang);                 // half widths at mouth / floor
zr0=zc0+3.7+c_face;           // receiver bottom 370 (lip is 3.7 thick)
z_stop=zc1;                   // channel closed above the cleat top: the top stop
zr1=z_stop+3;                 // receiver top 385.5
rx0=92; rx_right=126.5; rx_fil=124.2; ry_leg=239.5;             // outline
lock=[dt_x,234.5];            // M3 lock screw axis X, Y (vertical)
ear=[85.5,226.3];             // third lid screw on a back ear, clear of the receiver (X >= 92)
// draft 3 (Brian 2026-11-07): front lid screws moved onto outside ears so the Wago wire path to the front is completely clear
lid_screws=[[cx0+4.5,cy0+wall-4.5],[cx1-4.5,cy0+wall-4.5],ear];
module ears2d(){ for(p=lid_screws) hull(){ translate(p) circle(d=9); translate([p[0]-4.5,p[1]<cy0+10?cy0+1:cy1-3]) square([9,1]); } }

module box(a,b){translate(a)cube(b-a);}
module rbox2(a,b,r=r_bed){translate(a)offset(r=r)offset(delta=-r)square(b-a);}

// dovetail channel (2D in XY): mouth at yr0, floor at yf; extended 1 mm out the front
module dt_channel2d(){polygon([[dt_x-dt_hm+tan(dt_ang),yr0-1],[dt_x+dt_hm-tan(dt_ang),yr0-1],[dt_x+dt_hf,yf],[dt_x-dt_hf,yf]]);}
// matching cleat: channel offset in by c_dt on flanks and tip, rooted in the case back
module dt_cleat2d(){
  function h(y)=dt_hm+(y-yr0)*tan(dt_ang)-c_dt/cos(dt_ang);
  yt=yf-c_dt; y0=cy1-0.5;
  polygon([[dt_x-h(y0),y0],[dt_x+h(y0),y0],[dt_x+h(yt),yt],[dt_x-h(yt),yt]]);
}

module receiver(){
  difference(){
    translate([0,0,zr0]) linear_extrude(zr1-zr0) offset(r=1)offset(delta=-1) union(){
      rbox2([rx0,yr0],[x_flange-c_post,ry_leg]);                // block beside the flange edge, to the rack rear
      rbox2([x_flange-4,yr0],[rx_right,y_fillet-0.2],1.5);      // plate on the flange front, clear of the fillet

      translate([x_flange-4,yr0]) square([rx_fil-x_flange+4,y_post-yr0]);
    }
    // dovetail channel, open at the bottom, closed at z_stop
    translate([0,0,zr0-1]) linear_extrude(z_stop-zr0+1) dt_channel2d();
    // M6 x 8 button head: clearance + head counterbore from the front face (hidden behind the case when mounted)
    translate([hole[0],yr0-1,hole[1]]) rotate([-90,0,0]){ cylinder(d=ws_m6_clear,h=y_post-yr0+2); cylinder(d=head_d,h=yf-yr0+1+head_room);}
    // M3 x 3 x 5 insert for the lock screw, up from the bottom (7 deep: room for an M3 x 10)
    translate([lock[0],lock[1],zr0]) ws_insert_bore(ws_insert_m3,7);
  }
}
module receiver_keepout(){ ws_m6_head_keepout(hole[0],yf,hole[1],len=head_room+web,web=0); }

module case_body(){
  difference(){
    union(){
      translate([0,0,zc0]) linear_extrude(zc_lid-zc0) union(){
        rbox2([cx0,cy0],[cx1,cy1]);
        ears2d();  // back ear for a lid screw
      }
      // dovetail cleat on the back, case bottom to the top stop
      translate([0,0,zc0]) linear_extrude(z_stop-zc0) dt_cleat2d();
      // lock lip under the receiver bottom
      translate([0,0,zc0]) linear_extrude(3.7) rbox2([lock[0]-6,cy1-2],[lock[0]+6,ry_leg],2);
      // (draft 2, Brian 2026-11-07: no socket cradle. The DC socket stays down at the power strip with the brick;
      //  a new 12 V pair runs up the rack and enters through the floor slot beside the outgoing bundle.)
    }
    // inside
    translate([0,0,zc0+floor_t]) linear_extrude(20) difference(){
      offset(r=1)offset(delta=-1) translate([cx0+wall,cy0+wall]) square([cx1-cx0-2*wall,cy1-cy0-2*wall]);
    }
    // lid screw inserts
    for(p=lid_screws) translate([p[0],p[1],zc_lid]) mirror([0,0,1]) ws_insert_bore(ws_insert_m3,7);
    // M3 countersunk lock screw up through the lip
    translate([lock[0],lock[1],zc0-0.01]){ cylinder(d=3.4,h=10); cylinder(d1=7,d2=3.4,h=1.8); }
    // floor slot in the wire room: 12 V pair up from the power strip + 6-conductor bundle down to the Pi
    translate([103,cy0+wall+5,zc0-1]) linear_extrude(floor_t+2) hull(){ for(x=[-6.5,6.5]) translate([x,0]) circle(d=7); }
  }
  // low fences so the Wagos stay at the back (1.2 high, below the wire entries: entry height ASSUMED)
  for(i=[0:1]) translate([cx0+wall+side_room+wago_fit/2+i*(wago[0]+wago_gap)+2,wago_y-1.2,zc0+floor_t-0.01]) cube([wago[0]-4,1.2,1.2]);
  // zip tie anchor (Brian, draft 4): bridge on the floor between the slot and the Wagos; the tie runs through it along X
  // and over the wires crossing it, so a pull on the bundle stops here, not at the Wagos. Tie up to 4 wide x 1.5 thick assumed.
  translate([0,0,zc0+floor_t-0.01]) tie_bridge(103,tie_y,12);
}
tie_y=cy1-wall-wago_fit/2-wago[1]-1.2-3.0;                                                 // bridge centre Y, in front of the fences
module tie_bridge(x,y,len){ difference(){ translate([x-len/2,y-3,0]) cube([len,6,3.7]); translate([x-len/2-1,y-2.25,0]) cube([len+2,4.5,2.2]); } }
wago_y=cy1-wall-wago_fit/2-wago[1];                                  // Wago fronts (entries) at Y 202.0

module lid(){
  difference(){
    translate([0,0,zc_lid]) linear_extrude(lid_t) union(){
      rbox2([cx0,cy0],[cx1,cy1]);
      ears2d();
    }
    for(p=lid_screws) translate([p[0],p[1],zc_lid-0.01]){ cylinder(d=3.4,h=5); translate([0,0,lid_t-1.8+0.02]) cylinder(d1=3.4,d2=7,h=1.8); }
    // CT200 leads drop in at the back (notch open to the back edge, closed by nothing: leads lay in)
    translate([0,0,zc_lid-1]) linear_extrude(lid_t+2) hull(){ translate([113,cy1-6]) circle(d=8); translate([109,cy1+1]) square([8,1]); }
  }
  // zip tie anchor on the lid top in front of the notch: tie the CT200 leads down before they drop in (Brian, draft 4)
  translate([0,0,zc1-0.01]) tie_bridge(113,cy1-16,12);
}

module wagos(){ for(i=[0:1]) translate([cx0+wall+side_room+wago_fit/2+i*(wago[0]+wago_gap),wago_y,zc0+floor_t]) cube(wago); }
module keepout(){ receiver_keepout(); for(p=lid_screws) translate([p[0],p[1],zc1]) cylinder(d=7+2,h=3); }

if(part=="receiver") receiver();
if(part=="case") case_body();
if(part=="lid") lid();
if(part=="wagos") wagos();
if(part=="keepout") keepout();
if(part=="assembly"){ receiver(); case_body(); lid(); color("orange") wagos(); }
