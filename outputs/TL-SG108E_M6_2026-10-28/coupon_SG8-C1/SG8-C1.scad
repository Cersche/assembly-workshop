// SG8-C1: coupon of the SG8-M6-B left hidden-screw joint (X -104..-80, Y <= 24). ID engraved 0.4 mm.
part="tray";
module t(){linear_extrude(1)text("SG8-C1",size=3,font="Liberation Sans:style=Bold",halign="center",valign="center");}
if(part=="tray")difference(){import("raw_tray.stl");translate([-100.5-0.6+0.4,13,16])rotate([90,0,-90])t();}
else difference(){import("raw_faceplate.stl");translate([-92,-4-0.6+0.4,38.4])rotate([90,0,0])mirror([0,0,1])t();}
