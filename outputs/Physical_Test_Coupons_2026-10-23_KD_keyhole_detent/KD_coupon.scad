// KD keyhole-detent coupons (Brian, 2026-10-23). One detent of the TL-SG108E tray (build.py in
// outputs/STL_Deliveries/2026-10-23_TL-SG108E_flush) on a small floor piece, with the rear stop at the real distance.
// Test: set the switch (ports away from the wall) on the coupon, keyhole side down, slide it back until it touches the
// wall; the bump should drop into one keyhole's round part. Fit/retention/strength UNKNOWN; specimen-specific.
id="KD-A"; bump_up=0.6;            // KD-A 0.6, KD-B 0.8, KD-C 1.0 mm above the floor
tray_t=3; arm_w=8; arm_t=1.8; arm_l=26; arm_gap=1.2; bump_w=5; bump_flat=4;
key_y=44.5;                        // keyhole centre (48.5 behind the port face, which sits at Y=-4)
stop_y=96; stop_t=4; stop_h=8;     // rear stop face at 96 (switch depth 100)
w=34; y0=10;                       // coupon width / front edge
arm_end=key_y+5; arm_root=arm_end-arm_l;
bump_base=arm_t; bump_top=tray_t+bump_up; bump_hh=bump_top-bump_base;
difference(){
 union(){
  translate([-w/2,y0,0])cube([w,stop_y+stop_t-y0,tray_t]);
  translate([-w/2,stop_y,0])cube([w,stop_t,tray_t+stop_h]);
 }
 difference(){translate([-arm_w/2-arm_gap,arm_root,-0.1])cube([arm_w+2*arm_gap,arm_l+arm_gap,tray_t+0.2]);
  translate([-arm_w/2,arm_root-0.1,-0.2])cube([arm_w,arm_l+0.1,tray_t+0.4]);}
 translate([-arm_w/2-0.01,arm_root+3,bump_base])cube([arm_w+0.02,arm_l-3+0.01,tray_t]);
 // ID engraved 0.6 mm into the floor top, in front of the arm
 translate([0,y0+5,tray_t-0.6])linear_extrude(1)text(id,size=5,font="Liberation Sans:style=Bold",halign="center",valign="center");
 translate([0,stop_y-4,tray_t-0.6])linear_extrude(1)text(str(bump_up),size=4,font="Liberation Sans:style=Bold",halign="center",valign="center");
}
translate([-bump_w/2,0,0])rotate([90,0,90])linear_extrude(height=bump_w)
 polygon([[key_y-bump_flat/2-bump_hh,bump_base],[key_y-bump_flat/2,bump_top],[key_y+bump_flat/2,bump_top],[key_y+bump_flat/2+bump_hh*tan(30),bump_base]]);
