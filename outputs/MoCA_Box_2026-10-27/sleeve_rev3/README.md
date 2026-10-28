# MoCA sleeve rev 3 + back plate rev 2 (2026-10-28)

Print `MoCA_sleeve_rev3_and_back_plate_rev2.3mf` (or the two STLs). Porch rev 2, lid, cradle rev B, nut and sliders are unchanged.

- **F hole is now a pill:** 14 mm wide, centres X78..X88 (was a 14 mm round at X88). The right-angle F leg didn't reach the round hole on Brian's print, so the hole now runs 10 mm back toward the splitter. Outer end unchanged.
- **Power hole is now a pill too:** 10 mm wide, centres X33.5..X43.5 (was a 10 mm round at X38.5), so the barrel plug can find the jack ±5 mm along X.
- **Fix: ear slots and porch bosses are back.** An edit on 2026-10-27 had turned `ear_adj=8` and `porch_boss_d/h` into comments, so the rev 2 sleeve file was built without the 26 mm nut-slider ear slots and without the 8 mm porch insert bosses. Rev 3 has both.
- **Bosses print without supports:** each porch boss has a 45 deg ramp on its +Y side (the bed side when the sleeve stands on its back edge).
- **Back plate rev 2:** its inner lip is notched (0.4 mm clear) around the back porch boss (X86 Y62), which overlapped it by 2.5 mm. Otherwise unchanged; outer face down on the bed.
- Sleeve print orientation as rev 2 (rotated -90 about X, back edge down).

UNKNOWN: where the leg actually lands, fit, strength. At the inner end of the pill, the coax coming up runs toward the cradle bottom (Z33, X72..77.5); the leg tip is about 2 mm below it.
