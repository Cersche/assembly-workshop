# Final 3MF files (bracket overhaul, M6)

The latest accepted or current 3MF from each bracket session, copied here. The originals stay in their own output folders, which are the source of truth. Nothing here has been printed: fit and strength are UNKNOWN.

Print status (Brian, 2026-10-30): "accepted" means accepted to print, not proven. A file is proven only after Brian prints it and reports a fit; check docs/Fit_Findings.md.

| File | Bracket | Source folder |
|---|---|---|
| HDT-M6-A_drive_tray.3mf | HDD/SSD tray | Hard_Drive_Tray_M6_2026-10-28 |
| HDT-M6-A_drive_tray_color.3mf | HDD/SSD tray, color inlay | Hard_Drive_Tray_M6_2026-10-28 |
| CM6A_CM1000_M6_bracket_set.3mf | CM1000 modem (approved by Brian 2026-10-28: the printed baseline with only the M6 hardware changed; generated CM6B dropped) | CM1000_M6_2026-10-28 |
| SG8-M6-E_faceplate+label.3mf | TL-SG108E faceplate only, for the printed SG8-M6-D tray. **Unprinted.** Bosses cut back to clear the D tray lip (D plate + D tray clash: holes ~2 mm low). | TL-SG108E_M6_2026-10-28 |
| SG8-M6-D_TL-SG108E_M6_set.3mf | **Tray only now (printed); its faceplate clashes, use E.**  TL-SG108E switch. **Unprinted.** C + the proven 1.35 mm sleeve top clearance back (C printed 2026-10-30: did not fit; B/C had cut it to 0.35). Proven printed version: outputs/STL_Deliveries/2026-10-23_TL-SG108E_flush (M3) | TL-SG108E_M6_2026-10-28 |
| SCR5-H_screen_pi_hue_set.3mf | **Current screen unit (Brian 2026-10-31, ready to print).** 2U, measured Waveshare 5" screen flush in the plate (left/right cosmetic lips), rear frame on the 4 corner standoffs (M2.5 x 6), 3 wedge-pin buttons (DROP 0.45), SCR5-F Pi 4 + Hue tray behind (screwdriver trenches removed, one 25x10 cable slot right wall). DSI ~111 mm inside, stock 160 mm cable fits. 7 parts, 14,486/29,156 tags. Fit UNKNOWN | Screen_Pi_Hue_SCR5-H_2026-10-30 |
| SCR5-WP-A_wedge_pin_coupon.3mf | Test coupon ID SCR5-WP-A: wedge-pin buttons on the real screen, 3 pins (drop 0.35/0.45/0.55 = 1/2/3 dots). Print first or alongside to pick SCR5-H's DROP | Screen_WedgePin_Coupon_SCR5-WP-A_2026-10-30 |
| SCR5-F_screen_pi_hue_set.3mf | Superseded by SCR5-H (reference). 2U 5" screen (right) + Pi 4 (lower left) + Hue shelf + keystone, 30 mm deck fan + vents; four supportless parts (plate, clamp frame, floor+walls, Hue deck), rounded tray corners. Frees U5. Screen depth/preload as SCR5-B, still awaiting the screen | Screen_Pi_Hue_SCR5-F_2026-10-29 |
| SCR5-B_screen_plate_and_frame.3mf | 2U 5" screen plate (Waveshare 5inch DSI LCD (C)) + rear clamp frame, U4-U3. **Provisional (Brian 2026-10-29):** vendor dims, prepare for testing when the screen arrives (measure glass-front to PCB-rear at pad spots) | Screen_5in_SCR5-B_2026-10-29 |
| HP4-M6-B_Hue_Pi4_M6_set.3mf | **Default (Brian 2026-10-29).** Hue + Pi 4, Pi on the left for the 5" screen DSI ribbon, floor slot behind Pi | Hue_Pi4_M6-B_2026-10-28 |
| HP4-M6-A_Hue_Pi4_M6_set.3mf | Hue Bridge + Pi 4 + keystone (kept as alternative; Pi on the right) | Hue_Pi4_M6_2026-10-28 |
| MoCA_wall_cleat_set.3mf | MoCA box wall mount (accepted by Brian 2026-10-30): wall plate MOCA-WP-A (goes on the wall first, drilling template, anchor + stud holes) + French-cleat back plate MOCA-BC-A (replaces the keyhole back plate; M3 lock screw + insert). Not part of the rack | MoCA_Box_2026-10-27/wall_cleat_2026-10-30 |

SCR5-B and HP4-M6-A/B are kept for reference; the current rack layout uses SCR5-F at U4-U3 instead (U5 empty).

Each bracket session adds its finalized 3MF here, replaces the older version of the same bracket, and updates this table. Test coupons stay in their own folders.
