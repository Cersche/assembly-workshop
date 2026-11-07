// Fan junction box: PLACEMENT CONCEPT only (2026-11-07). Not a part design; nothing here is for printing.
// Rack frame as rack_top_fan.scad: X centred, Y 0 front .. 240 rear, Z 0 = bottom of slot 9, post tops Z 400.05.
// Posts are simplified stand-ins from the 4U post card (flange Y 0..6 / 234..240, X 111.12..143, side wall to Y 35 / from 205).
// CM1000 = envelope (212.6 x 38 x 136, front at Y ~4) in slot 1. Wagos = datasheet sizes (Brian 2026-11-07: use datasheet).
part="box";   // posts | modem | box | wagos | socket | cable
$fn=32;
u=44.45; z_top=400.05; zc1=z_top-u/2;       // slot 1 (U9) centre 377.8
module post(){ // one right front post, Z from 400.05-4U to 400.05
  translate([111.12,0,z_top-4*u]) cube([143-111.12,6,4*u]);
  translate([127.12,0,z_top-4*u]) cube([143-127.12,35,4*u]);
}
if(part=="posts") for(s=[-1,1]) scale([s,1,1]){ post(); translate([0,240,0]) mirror([0,1,0]) post(); }
if(part=="modem") translate([-106.3,4,zc1-19]) cube([212.6,136,38]);

// COMPACT concept v2 (Brian: "HAS to be more compact"): only power is spliced. 2 x 221-413 (12 V bus, GND bus);
// ARGB 5 V / DATA / GND, PWM and TACH pass straight through unspliced. Brick socket adapter clips OUTSIDE the -X wall.
bx=[78,124]; by=[165,201]; bz=[365,383]; w=2;
if(part=="box") difference(){
  union(){
    translate([bx[0],by[0],bz[0]]) cube([bx[1]-bx[0],by[1]-by[0],bz[1]-bz[0]]);
    translate([108,by[1]-1,bz[0]]) cube([15,234-by[1]+1,bz[1]-bz[0]]);   // tab to the flange's front face (Y 234)
    translate([bx[0]-17,176,bz[0]]) difference(){ cube([17,19,13]); translate([-1,2,2]) cube([19,15,20]); } // open cradle for the socket adapter
  }
  translate([bx[0]+w,by[0]+w,bz[0]+w]) cube([bx[1]-bx[0]-2*w,by[1]-by[0]-2*w,30]);
  translate([118.26,226,zc1]) rotate([-90,0,0]) cylinder(d=6.6,h=20);    // M6 x 8 into an insert in the post's U9 middle hole
  translate([bx[0]-1,183,bz[0]+w]) cube([w+2,6,6]);                      // brick socket leads in
  translate([110,190,bz[0]-1]) cube([10,8,w+2]);                         // 6-core exit, down the rear post lane
  translate([110,168,bz[1]-w-1]) cube([12,9,w+2]);                       // CT200 leads in from the top
}
module wago(wd){ translate([0,0,bz[0]+w]) { cube([wd,18.6,8.3]); color("orange") translate([1,12,8.3]) cube([wd-2,4.6,1.5]); } }
if(part=="wagos") for(i=[0:1]) translate([bx[0]+w+1+i*20.7,by[1]-w-18.6,0]) wago(18.7);   // entries face -Y, 12+ mm of wire room in front
// screw-terminal DC socket adapter (approx. 38 long, 11.5 barrel + 15 x 15 terminal block), lying in the cradle, mouth facing -X
if(part=="socket") translate([bx[0]-40,185.5,bz[0]+2+7.5]) rotate([0,90,0]) { cylinder(d=11.5,h=18); translate([-7.5,-7.5,18]) cube([15,15,22]); }
// 6-core cable down the rear post lane to the Pi (slots 5-6), and CT200 leads up to the fan
if(part=="cable"){ translate([115,194,240]) cylinder(d=6,h=bz[0]-240); translate([116,172,bz[1]]) cylinder(d=5,h=z_top+15-bz[1]); }
