// CM1P-T6 ID text and hole labels, engraved 0.5 into the plate's top face (frame as cm1p_t6_freecad.py).
translate([127, 12, 43.95]) linear_extrude(1) text("CM1P-T6", size = 4, font = "Liberation Sans:style=Bold", halign = "center", valign = "center");
for (s = [["A", 75.25], ["B", 132.75]], i = [0 : 4]) translate([s[1] + i * 11.5, 5, 43.95]) linear_extrude(1) text(str(s[0], i + 1), size = 3.2, font = "Liberation Sans:style=Bold", halign = "center", valign = "center");
