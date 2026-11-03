// CM1P-T5 ID text and hole numbers, engraved 0.5 into the plate's top face (frame as cm1p_t5_freecad.py). -D 'tag="A"'
tag = "A";
translate([127, 12, 43.95]) linear_extrude(1) text(str("CM1P-T5", tag), size = 4, font = "Liberation Sans:style=Bold", halign = "center", valign = "center");
for (i = [0 : 4]) translate([104 + i * 11.5, 5, 43.95]) linear_extrude(1) text(str(i + 1), size = 3.5, font = "Liberation Sans:style=Bold", halign = "center", valign = "center");
