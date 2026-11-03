# SCR5-H9: screen + Pi 4 + Hue, rev 9 (2026-11-03)

New revision folder; H8 (`outputs/Screen_Pi_Hue_SCR5-H8_2026-10-31/`) stays immutable. Test-print ID **SCR5-H9** on plate, floor and deck. Frame and wedge pins are H8's, unchanged, and keep their H8 ID. **Not printed.** Fit, strength and how much sag this removes are UNKNOWN.

Why: Brian reported the tray sagging (2026-11-03). H8's tray joined the plate through a section with no walls: at the fan hole only two 10 mm x 3 mm deck strips carried the rear of the tray, and the floor wasn't tied to the plate at all.

## Changes from H8
- **Fan moved off the deck (Brian's choice).** Same 40 x 10 12 V fan, now upright on the outside of the outer wall, blowing across the Pi. Centre Y 46, Z 28.7 (plate-front coordinates), X -120..-110. The deck hole and its 4 screw holes are gone.
- **Two fan columns** printed from the bed on the floor part, X -110..-102, 9 wide, up to Z 49.2. Each takes 2 M3x3x5 inserts (4.2 bore, 4 deep, from the fan side). They pass through notches in the deck edge, which also stops the deck sliding on the floor.
- **Grille in the outer wall** where the fan blows: Z 12.7..39 only, because the fan (40) is taller than the floor-to-deck gap (29), so part of its outlet is blocked. 3 vertical bars tie the floor to the deck there.
- **Outer wall**, X -105..-102, from the plate to Y 67, then a **USB-C window** Y 67..90, then the existing rear wall. The tray is 3 mm wider on this side so the wall clears the Pi.
- **Inner wall**, X -46..-43, from the plate to Y 92, along the Pi. **Open-top ribbon slot** Y 33..41, from Z 21 up.
- **Wall tops key into the deck:** 1.5 wide x 1.5 tall tongues in 2.0 x 1.8 deep grooves in the deck underside, so floor and deck work as one box.
- **Plate ledge:** 3 thick, 8 deep, X -105..-43, 0.15 under the floor. The floor sits on it, and pushes on the plate when the tray tries to droop.
- **Hue + cradle 10 forward, tray 10 shorter** (rear now Y 142). Back where the Hue was before the 40 mm fan. Right-wall vents and cable slot moved with it.
- **Deck screws:** now 7. The 3 rear ones moved 10 forward with the cradle; new ones at the inner wall's rear end and on a small outside pad at the front corner (X -112 at its widest). Front-left tray corner is now square so the outer wall butts the plate.

## Kept unchanged (`docs/Fit_Findings.md`)
Screen window 121.5 x 78.0, frame, wedge pins, Pi position and port openings, keystone, Hue cradle shape, 3 M6 tray joints and tongue clearance, insert bores, rack slots. The parked top-of-glass clearance is still parked.

## Assumptions to check
- **Only USB-C is used on the Pi's side.** The outer wall and grille now cover HDMI and audio. USB-C position comes from the published Pi layout, not a measurement.
- **Ribbon:** the slot and route are modelled on a 1 mm centreline; a real flat ribbon's twist and reach are UNKNOWN. Lay it in the slot before the deck goes on.
- **Fan screws:** about M3 x 14 countersunk (10 fan + insert). Confirm the length on hand.
- **Rack clearance:** not checked against the post mesh in this build. Everything stays inside the space SG8-M6-F's post rails were clash-checked in (X to 125, Y from 6.2 behind the plate), up to Z 49.2 vs that rail's 44; the post wall is solid mid-post.
- M6 screws: about 32 of straight room behind the heads now (42 in H8), so still a 4 mm hex L-key.

## BOM change from H8
7 deck M3 countersunk + 7 M3x3x5 inserts (was 5 + 5). 4 fan M3 countersunk + 4 M3x3x5 inserts (fan previously had no inserts). 3 M6 joints unchanged.

## Print
Reprint plate, floor and deck. Frame and pins: H8 files. Floor on its bottom face, deck on its underside, plate face down; no supports intended, but the fan column undersides above the rotor cut are short overhangs (about 37 to 57 degrees from flat), so check them in the slicer.

## Checks (digital only)
- Plate, floor, deck: one closed shell, 0 bad edges, 0 degenerate faces. Frame carried over.
- Intersections (`checks/pairwise.json`): floor/deck vs plate, frame, Pi, fan, ribbon, screen dummy and screw heads, floor vs Hue, fan vs plate and Pi, floor vs deck: all 0. Deck vs Hue 5,097 mm3 (same inherited box-vs-cradle overlap as H8, 5,096). The M6 straight-driver lines still hit the cradle post and Hue box, as in H8, hence the L-key.
- 3MF: 7 objects, 18,949 vertex / 38,122 triangle tags, no ns0.
- Calculated bending stiffness through the old fan-hole position: H8 45 mm4 (deck strips only), H9 about 174,000 mm4 if floor, walls and deck act fully as one box. That is a best case: real joints give less, and the plate and M6 tabs are not included. It doesn't predict the sag.

## Rebuild
`python src/SCR5-H9_build.py`, then `python src/SCR5-H9_finish.py`. Needs OpenSCAD and the local Hue cradle `C:/Users/brian/Downloads/Swanky Rottis.stl`.
