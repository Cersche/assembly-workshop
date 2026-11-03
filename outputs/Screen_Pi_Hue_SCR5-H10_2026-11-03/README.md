# SCR5-H10: screen + Pi 4 + Hue, rev 10 (2026-11-03)

New revision folder; H8 and H9 stay as they are, but **don't print either: their third M6 joint blocks the keystone opening.** Test-print ID **SCR5-H10** on plate, floor and deck. Frame and wedge pins are H8's, unchanged, and keep their H8 ID. **Not printed.** Fit, strength and how much sag this removes are UNKNOWN.

Everything from H9 is kept: side fan, inner and outer walls keyed into the deck, plate ledge, Hue 10 forward, tray 10 shorter. See [H9's README](../Screen_Pi_Hue_SCR5-H9_2026-11-03/README.md).

## Changes from H9
- **X -88 M6 tab and plate boss removed.** Added in H8, they sat inside the keystone opening (X -92.5). The keystone is clear behind the plate again, and the plate is back to 2 M6 joints at X -71 and -50.
- **New third joint, low on the outer side (Brian).** M3 at X -106.5, Z 25: a plate boss (9 OD, clipped at X -110.85 to clear the post flange, M3x3x5 insert bore 4.2 x 4 deep) and a screw from behind through a pilaster on the floor part. The top M6 joints and this low one now fasten the tray at top and bottom.
- **M3 instead of M6 here (Brian's OK, 2026-11-03):** only about 9 mm of width is free between the Pi's USB opening and the post flange.
- **Pilaster:** X -112..-102, Y 8.3..17.3 (plate-rear frame), floor to deck. The front deck screw moved 0.8 back onto it.
- **Outer wall now starts 8.3 behind the plate** so the boss can pass; the floor still butts the plate there.
- **Head well:** a 6.8 mm well behind the screw head runs to Y 23.2, thinning the outer wall to 1.1 mm over a 6.8 tall, 7.7 long patch and removing the thin bit of the front fan column at that height.

## Assembly order
Fit the low screw **before the fan**: M3 x 10 countersunk, put in through the gap where the fan goes, tightened with a 2 mm L-key. M6 screws: 4 mm L-key as before. The ribbon goes in its slot before the deck goes on.

## BOM change from H9
M6 joints 2 (was 3). +1 M3 x 10 countersunk and +1 M3x3x5 insert for the low joint. 7 deck and 4 fan M3 pairs unchanged. Confirm lengths on hand.

## Still to check
- Keystone: a 12 x 12 straight path 30 back from the plate rear is clear, but the jack and cable size are not measured here. With the Hue forward, the cradle is about 51 behind the plate rear on the keystone's line (61 in H7), so check the cable bend.
- The H9 list still applies: only USB-C used on the Pi's side, ribbon twist and reach, fan screw length, column overhangs in the slicer.
- The low joint's single M3 and its small boss: pull-out and strength UNKNOWN.

## Checks (digital only)
- Plate, floor, deck: one closed shell, 0 bad edges, 0 degenerate faces.
- Intersections (`checks/pairwise.json`): floor/deck vs plate, frame, Pi, fan, ribbon, screen dummy and screw heads, floor vs Hue, fan vs plate and Pi, floor vs deck: all 0.
- **New this revision:** plate, floor and deck vs the keystone path: 0. Plate, floor, deck and fan vs the left rack post mesh (the hex-groove 4U concept copy, `work/rack-post-hex/assembled/post_left.stl`, used as the stand-in for the post shape): 0.
- Deck vs Hue 5,097 mm3, the same inherited box-vs-cradle overlap. Straight M6 driver lines now clear the deck but still cross the Hue box, hence the L-key.

## Rebuild
`python src/SCR5-H10_build.py`, then `python src/SCR5-H10_finish.py`. Needs OpenSCAD and the local Hue cradle `C:/Users/brian/Downloads/Swanky Rottis.stl`.
