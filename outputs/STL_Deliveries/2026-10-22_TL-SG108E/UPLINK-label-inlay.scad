// Fills the 0.6 mm UPLINK engraving exactly (same text call as label_cut), front face Y=-4.
plate_t=4; $fn=48;
intersection(){
 translate([88,-plate_t-0.1,3.8])rotate([90,0,0])mirror([0,0,1])linear_extrude(height=0.7)text("UPLINK",size=4.5,font="Liberation Sans:style=Bold",halign="center",valign="center");
 translate([-200,-plate_t,-10])cube([400,0.6,100]);
}
