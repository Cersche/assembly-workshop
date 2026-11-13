// OPTION B (Brian 2026-11-07: use more vertical space, stack the Wagos). Copied from option A (draft 6, fan_junction_box.scad,
// commit 80fbd8f), which stays unchanged. B: the two 221-413 sit one on top of the other in a loose pocket against the -X wall,
// entries +X into the same post-side wire lane and corner exit; the case is ~20 mm shorter in Y and grows DOWN (top, lid,
// TF-C clearance unchanged). Receiver is the same design, taller because it follows the case bottom (longer dovetail).
// B draft 2 (Brian 2026-11-07, picked B): the fan's own leads won't reach the Pi, so they get extended IN the box. CT200 4-pin
// plugs into a 4-pin PWM extension (cut: 12 V/GND into the Wagos, PWM/TACH on to the Pi); CT200 3-pin ARGB plugs into an uncut
// 3-pin extension. Both mated pairs lie stacked in one pocket in a front bay (end stops so they can't vibrate apart, lid on
// top). Fan leads lay in through a lid notch at the -X edge, so the pairs run +X and the extension wires go straight back down
// the lane to the Wagos and the corner exit (no U-turn). Mated-pair sizes are TYPICAL, not measured (UNKNOWN).
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
side_room=2;   // draft 4 (Brian): room beside the outer Wagos for the outer wires
wire_room=16;  // draft 4: wire room in front of the entries
// draft 6 (Brian 2026-11-07): wires leave straight down beside the right rear post, parallel to it. The Wagos turn 90 deg:
// stacked along Y against the -X wall, entries facing +X into a full-depth wire lane on the post side; exit hole in the
// lane's rear corner, under the CT200 lead notch, so every wire enters and leaves at the right rear corner.

// ---- case (Z chosen so the receiver covers the M6 head recess, Z 372.05..383.55, with ~2 mm left each side)
wall=2; floor_t=2; lid_t=2.5; stack_fit=0.6;                       // B: vertical play over the two stacked Wagos
inner_h=2*wago[2]+stack_fit;                                     // 17.2 (A: 12)
zc_lid=380; zc0=zc_lid-floor_t-inner_h; zc1=zc_lid+lid_t;        // 360.8 / 380 / 382.5: top unchanged, grows down
cx1=124.0; cy1=223.0;          // +X side (post side wall X 127.12) and case back stay put; growth goes to -X and the front
// B draft 2: connector bay in front of the Wagos. Mated pair (fan plug + extension plug) L x W x H, TYPICAL 2.54 mm fan/ARGB
// housings, UNKNOWN until Brian measures (diagram work/fan-junction-box/pair_measure.svg)
pair=[26,11.5,7.5]; pk_len=pair[0]+2.5; pk_w=pair[1]+1.0; stop_t=1.6; pw_t=1.6;
drop=7.5;      // lead drop-in room at the -X end under the lid notch
end_room=5.5;  // extension wires turn from the pocket's +X end back into the lane
cx0=cx1-(2*wall+drop+2*stop_t+pk_len+end_room);                  // 75.3 (B1 85.0)
wy0=cy1-(2*wall+wago[0]+wago_fit+2*side_room);                   // 195.9 Wago pocket front partition (B1 case front)
cy0=wy0-pw_t-pk_w-wall;                                          // 179.8 (A 175.2)
px0=cx0+wall+drop+stop_t; px1=px0+pk_len; pcy=cy0+wall+pk_w/2;  // pocket X 86.4..114.9, centre Y 188.05
wago_x1=cx0+wall+wago_fit/2+wago[1];                             // Wago entry faces X 96.1 (lane now ~26 wide)
exit_x=116; exit_y=[209,216]; exit_d=8;                          // exit hole X 112..120, Y 205..220 (inner walls X 122, Y 221)
r_bed=3;                                                         // rounded bed corners (Brian, 2026-11-05)

// ---- receiver
yr0=cy1+c_face;               // receiver front face 223.3
web=ws_m6_web; head_d=ws_m6_head_d; head_room=4.3;               // button head ~3.3 high + 1 mm
yf=y_post-web-head_room;      // dovetail channel floor 227.2 (same depth as the head counterbore bottom)
dt_x=102; dt_m=10; dt_ang=30; // channel centre X, mouth width, flank undercut
dt_hm=dt_m/2; dt_hf=dt_hm+(yf-yr0)*tan(dt_ang);                 // half widths at mouth / floor
zr0=zc0+3.7+c_face;           // receiver bottom 364.8 (A: 370) (lip is 3.7 thick)
z_stop=zc1;                   // channel closed above the cleat top: the top stop
zr1=z_stop+3;                 // receiver top 385.5
rx0=92; rx_right=126.5; rx_fil=124.2; ry_leg=239.5;             // outline
lock=[dt_x,234.5];            // M3 lock screw axis X, Y (vertical)
ear=[87.0,226.3];             // third lid screw on a back ear, clear of the receiver (X >= 92)
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
    // draft 6: exit hole in the lane's rear corner, 12 V pair up from the power strip + 6-conductor bundle down to the Pi,
    // both running straight down beside the post (X 116 is 11 inside the post side wall X 127.12)
    translate([exit_x,0,zc0-1]) linear_extrude(floor_t+2) hull(){ for(y=exit_y) translate([0,y]) circle(d=exit_d); }
    // flush zip tie notches (draft 5 style) either side of the lane just in front of the exit: tie the bundle before it drops
    for(x=[exit_x-4,exit_x+4]) translate([x-1,tie_y-2.25,zc0-1]) cube([2,4.5,floor_t+2]);
  }
  // B draft 2: inner walls. Partition in front of the Wagos; pocket back wall; end stops at both pocket ends (corner tabs,
  // 7.5 mm open in the middle for the wires, narrower than the housings so the mated pair can't slide apart)
  hz=[zc0+floor_t-0.01,zc_lid];
  box([cx0+wall-0.01,wy0,hz[0]],[wago_x1+1.2,wy0+wall,hz[1]]);
  box([px0-stop_t,wy0-pw_t,hz[0]],[px1+stop_t,wy0+0.01,hz[1]]);
  for(x=[px0-stop_t,px1]) for(y=[[cy0+wall-0.01,pcy-3.75],[pcy+3.75,wy0-pw_t+0.01]]) box([x,y[0],hz[0]],[x+stop_t,y[1],hz[1]]);
  // low fence so the lower Wago stays at the back (1.2 high, below the wire entries: entry height ASSUMED)
  translate([wago_x1,wago_y0+2,zc0+floor_t-0.01]) cube([1.2,wago[0]-4,1.2]);
  // B: full-height stop ribs on both side walls at the entry face, in the side room (wires enter mid-face): keep the upper Wago back too
  for(y=[wy0+wall-0.01,cy1-wall-1.5+0.01]) translate([wago_x1,y,zc0+floor_t-0.01]) cube([1.2,1.5,inner_h]);
}
tie_y=exit_y[0]-exit_d/2-4;                                                                // tie notch centre Y 201
module tie_bridge(x,y,len){ difference(){ translate([x-len/2,y-3,0]) cube([len,6,3.7]); translate([x-len/2-1,y-2.25,0]) cube([len+2,4.5,2.2]); } }
wago_y0=wy0+wall+side_room+wago_fit/2;                               // first Wago's low-Y side

module lid(){
  difference(){
    translate([0,0,zc_lid]) linear_extrude(lid_t) union(){
      rbox2([cx0,cy0],[cx1,cy1]);
      ears2d();
    }
    for(p=lid_screws) translate([p[0],p[1],zc_lid-0.01]){ cylinder(d=3.4,h=5); translate([0,0,lid_t-1.8+0.02]) cylinder(d1=3.4,d2=7,h=1.8); }
    // B draft 2: CT200 leads lay in at the -X edge, over the drop room in front of the pocket's -X end (A/B1: back notch)
    translate([0,0,zc_lid-1]) linear_extrude(lid_t+2) hull(){ translate([cx0+wall+drop/2,pcy]) circle(d=7); translate([cx0-1,pcy-3.5]) square([1,7]); }
  }
  // zip tie anchor on the lid top in front of the notch: tie the CT200 leads down before they drop in (Brian, draft 4)
  // B draft 2: moved beside the new notch, tie runs along Y: leads drape over the lid edge, get tied, drop into the notch
  translate([cx0+wall+drop+8,pcy,zc1-0.01]) rotate(90) tie_bridge(0,0,12);
}

// B: stacked, lower on the floor, upper resting on it, both loose (lid off and lift the upper one out to rewire; lever-open height UNKNOWN)
module wagos(){ for(i=[0:1]) translate([wago_x1-wago[1],wago_y0,zc0+floor_t+i*wago[2]]) cube([wago[1],wago[0],wago[2]]); }  // entries at +X
// B draft 2: the two mated pairs (typical size), 4-pin PWM below, 3-pin ARGB on top
module pairs(){ for(i=[0:1]) translate([px0+1.25,pcy-pair[1]/2,zc0+floor_t+i*pair[2]]) cube(pair); }
module keepout(){ receiver_keepout(); for(p=lid_screws) translate([p[0],p[1],zc1]) cylinder(d=7+2,h=3); }

if(part=="receiver") receiver();
if(part=="case") case_body();
if(part=="lid") lid();
if(part=="wagos") wagos();
if(part=="keepout") keepout();
if(part=="pairs") pairs();
if(part=="assembly"){ receiver(); case_body(); lid(); color("orange") wagos(); color("black") pairs(); }
