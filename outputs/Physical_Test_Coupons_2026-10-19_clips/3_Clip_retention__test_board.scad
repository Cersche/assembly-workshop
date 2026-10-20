// Stand-in for the board edge: 1.6 mm thick (board_t), spans the right-hand ledges and clip of the coupon tray.
// Same X/Y frame as the tray coupon; print flat. Real boards may differ: fit is UNKNOWN.
translate([30,12,0])cube([12.5,56,1.6]);
