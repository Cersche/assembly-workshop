# SCR5-H8: screen + Pi 4 + Hue, rev 8 (2026-10-31)

New revision folder; rev 7 (`outputs/Screen_Pi_Hue_SCR5-H7_2026-10-31/`) stays immutable. Test-print ID **SCR5-H8** on plate, frame, floor and deck. Fixes from Brian's rev 7 test fit (photos, 2026-10-31). Measurements are Brian's, taken from the BACK ("left" = front-view right).

## Changes from rev 7
- **Frame corner tab restored.** The Pi DSI ribbon corridor had cut away the upper corner tab (upper right seen from the back), leaving its plate insert unused. The tab now stays; the corridor runs beside it (frame now overlaps the old corridor keep-out by 108 mm3, all inside the tab where the plate boss already blocked it).
- **Pockets for the 2 unused Pi standoffs** on the screen PCB: 5.5 mm standoffs, 10 mm below the glass top, 40 and 98 mm from the glass left edge (from the back). 6.5 mm through-holes in the frame bar.
- **Screen panel ribbon pocket.** The screen's own flex wraps from the glass bottom edge back to the PCB underside, 17-25 mm from the left (from the back), ~4.5 below the glass. Pocket made generous: 16-26 mm (10 wide), from 1.2 mm behind the plate front back to Y 10, out through the plate's bottom edge. The front 1.2 mm skin stays, so it is hidden from the front (a dark slot may show through the 0.4 mm glass gap).

- **Deck screws moved (Brian's slicer review, 2026-11-01).** The 9 mm floor bosses overhung the floor edge at the inner step (-41,39) and along the rear (y 144 + 4.5 > 148); the rear corner screws sat under the Hue cradle's corner posts. New tray positions: (-39,41), (-12,42), (-96,119), (-55,143), (-15,119). The rear corners are now forward of the posts, so the deck's rear corners have no screw.
- **Screw wells through the cradle base.** The cradle's ~1.1 mm base slab covered the countersinks; each deck screw now has a 6.8 mm well straight up through it.
- **Third M6 tray joint (Brian, rev 7 test fit 2026-11-01).** The Pi tray sagged on its outer (USB-C) side: only two tabs, at X -71/-50. New third tab + plate M6 insert boss at X -88 (tab X -98..-78). Its screw has ~42 mm of straight access behind the head before the Hue cradle's front post (Y 60.5), so use a 4 mm hex L-key, not a long straight driver.

## Checks
- All 7 STLs one closed shell, 0 bad edges, 0 degenerate faces.
- Plate + frame vs the 2 standoffs (10 mm tall) and the ribbon wrap box (8 x 6.6 x 4.5): empty.
- Deck vs Hue 5096 mm3, same as rev 7. Other pairwise results in checks/pairwise_intersections.json.
- All 5 bosses lie inside the floor outline; the 5 head wells clear the cradle posts. Floor/deck vs Pi, fan, plate: 0.
- 3MF: 7 objects, 18244 vertex / 36704 triangle tags, no ns0.
- BOM change: +1 M6 x 8 button head and +1 M6x5x8 insert (3 total for the plate-to-tray joint).

## Notes / UNKNOWN
- The plate has only 2.5 mm below the window, so the ribbon (4.5 below the glass) hangs ~1.6 mm below this unit's slot bottom, behind the plate below. Check that nothing in the unit below sits at Y 2.5-9 at the top edge.
- The 1.2 x 2.5 mm front skin over the pocket is thin (10 mm long).
- BOM unchanged from rev 7. Fit, insert pull-out and strength UNKNOWN. Not printed.
