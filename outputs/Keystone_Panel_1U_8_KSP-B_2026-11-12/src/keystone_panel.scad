// DRAFT KSP-B: 1U faceplate, 8 golden keystones, stiffened, with engraved labels above the jacks.
// KSP-A (released 2026-11-12, outputs/Keystone_Panel_1U_8_KSP-A_2026-11-12) + labels (Brian 2026-11-12):
// keystones moved down ks_dz so the strip above them grows from 3.7 to 6.7 mm; icon + name engraved
// lbl_d deep in the front face. Icons are simple original glyphs, not the makers' logos.
// Base history: printed 10-keystone panel too flimsy; only 8 needed; 12 mm frame OK.
// Fit and strength UNKNOWN. Unprinted draft.
include <workshop.scad>

part="panel";           // panel | cuts (check only: one solid per keystone pocket)
tag="KSP-B";            // ID, engraved 0.6 deep in the rear face of the top frame bar, centre
u=1;
ks_n=8; ks_pitch=27.5;  // 10 at 21.5 before
ks=[for(i=[0:ks_n-1])(i-(ks_n-1)/2)*ks_pitch];  // +-13.75, 41.25, 68.75, 96.25
ks_dz=3;                // keystones 3 mm lower than KSP-A (bottom strip 7.2 -> 4.2, top 3.7 -> 6.7)
rib_d=12;               // frame depth behind the plate (golden blocks reach about 6.3)
rib_x=110.1;            // frame half-width: 1 mm clear of the post flange edge at X 111.12
pocket_w=19.8;          // block's deep walls are X +-9.9; nothing new inside them
ks_z0=ws_plate_center(u)-15-ks_dz; ks_z1=ws_plate_center(u)+18.5-ks_dz;   // block window
ch=1;                   // rear edge chamfer

// Labels, keystone 1 = leftmost seen from the front (X -96.25). "" = blank.
labels=[["",""],["bulb","Hue"],["coax","MoCA"],["berry","Pi LAN"],["panes","Win PC"],["desktop","OptiPlex"],["",""],["berry","Pi USB"]];
lbl_d=0.6;              // engraving depth in the front face
lbl_h=4.4;              // icon height
lbl_txt=3.0;            // text size
lbl_zc=(ks_z1+ws_plate_top(u))/2;   // strip centre
lbl_wmax=25.5;          // max label width (pitch 27.5)

module icon(k){
 s=lbl_h;
 if(k=="bulb"){ translate([0,s*0.62])circle(d=s*0.72,$fn=32); translate([-s*0.17,0])square([s*0.34,s*0.3]); }
 if(k=="coax"){ translate([0,s/2])difference(){circle(d=s,$fn=32);circle(d=s*0.62,$fn=32);} translate([0,s/2])circle(d=s*0.24,$fn=16); }
 if(k=="panes"){ g=s*0.14; c=(s-g)/2; for(i=[0,1],j=[0,1])translate([i*(c+g)-s/2,j*(c+g)])square([c,c]); }
 if(k=="desktop"){ translate([-s*0.6,s*0.3])difference(){square([s*1.2,s*0.7]);translate([s*0.14,s*0.14])square([s*0.92,s*0.42]);}
   translate([-s*0.08,s*0.12])square([s*0.16,s*0.2]); translate([-s*0.3,0])square([s*0.6,s*0.12]); }
 if(k=="berry"){ translate([0,s*0.36])for(p=[[0,0],[-1,0],[1,0],[-0.5,-0.85],[0.5,-0.85],[-0.5,0.85],[0.5,0.85]])translate(p*s*0.19)circle(d=s*0.3,$fn=16);
   for(m=[-1,1])translate([m*s*0.17,s*0.86])rotate(m*-30)scale([1,0.45])circle(d=s*0.38,$fn=16); }
}
function icon_w(k)= k=="desktop"?lbl_h*1.2:lbl_h;
function txt_w(t)=len(t)*lbl_txt*0.62;   // rough Liberation Sans Bold width, for centring only

// icon left, name right, centred as a group on x=0, clipped to lbl_wmax
module label2d(l){
 iw=icon_w(l[0]); gap=0.8; w=min(lbl_wmax,iw+gap+txt_w(l[1]));
 intersection(){
  translate([-w/2,0])union(){
   translate([iw/2,-lbl_h/2])icon(l[0]);
   translate([iw+gap,0])text(l[1],size=lbl_txt,font="Liberation Sans:style=Bold",halign="left",valign="center");
  }
  translate([-lbl_wmax/2,-lbl_h])square([lbl_wmax,2*lbl_h]);
 }
}
// rotate([90,0,0]): 2D x -> X, 2D y -> Z, extrusion toward -Y, readable from the front
module labels3d(){
 for(i=[0:len(ks)-1])if(labels[i][1]!="")
  translate([ks[i],-ws_plate_t+lbl_d,lbl_zc])rotate([90,0,0])linear_extrude(lbl_d+1)label2d(labels[i]);
}
module labels_part(){ intersection(){ labels3d(); translate([-130,-ws_plate_t,0])cube([260,lbl_d,50]); } }

module pockets(){for(x=ks)translate([x-pocket_w/2,-0.02,ks_z0])cube([pocket_w,rib_d+1,ks_z1-ks_z0]);}

module frame(){
 difference(){
  // slab behind the plate, inside the plate outline, rear edges chamfered
  hull(){
   translate([-rib_x,-0.01,ws_plate_bottom()])cube([2*rib_x,rib_d-ch+0.01,ws_plate_h(u)]);
   translate([-rib_x+ch,0,ws_plate_bottom()+ch])cube([2*(rib_x-ch),rib_d,ws_plate_h(u)-2*ch]);
  }
  pockets();
  translate([0,rib_d-0.6,(ks_z1+ws_plate_top(u))/2])rotate([90,0,180])linear_extrude(1)
   text(tag,size=3,font="Liberation Sans:style=Bold",halign="center",valign="center");
 }
}

// golden keystones from the library, moved down ks_dz (shapes unchanged)
module panel(){
 difference(){
  union(){
   difference(){
    rotate([90,0,0])linear_extrude(height=ws_plate_t)ws_plate2d(u);
    for(x=ks)translate([0,0,-ks_dz])ws_keystone_cut(x,u);
   }
   for(x=ks)translate([0,0,-ks_dz])ws_keystone(x,u);
   frame();
  }
  labels3d();
 }
}

if(part=="panel") panel();
if(part=="labels") labels_part();   // optional second-colour inlay that fills the engraving exactly
if(part=="cuts") pockets();
