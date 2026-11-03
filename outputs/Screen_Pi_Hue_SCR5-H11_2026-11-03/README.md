# SCR5-H11: screen + Pi 4 + Hue, rev 11 (2026-11-03)

New revision folder; H8, H9 and H10 stay as they are. Test-print ID **SCR5-H11** on plate, floor, deck and fan mount. Frame and wedge pins are H8's, unchanged, and keep their H8 ID. **Not printed.** Fit, snap retention, strength and how much sag this removes are UNKNOWN.

Everything from H10 is kept: clear keystone, 2 M6 joints + low M3 joint, inner and outer walls keyed into the deck, Hue 10 forward, tray 10 shorter. See [H10's README](../Screen_Pi_Hue_SCR5-H10_2026-11-03/README.md) and [H9's](../Screen_Pi_Hue_SCR5-H9_2026-11-03/README.md).

## Changes from H10 (Brian, 2026-11-03)
- **Fan mount is its own part, no tools to take on or off.** `SCR5-H11_fanmount.stl`: a 5 thick frame, Y 24..68, Z 5.2..49.2, with the same 40 x 10 fan position and 4 M3x3x5 inserts (4.2 x 4 deep, from the fan side). The fan columns and deck notches are gone from the tray, so the tray works with no fan at all.
- **How it clips on:** the bottom lip hooks under the floor edge, two keys in the lip drop into two grooves under the floor (they stop it sliding along the wall), then two top lips clip over the deck edge. Rough interference over the deck edge is about 0.2 mm, calculated from the geometry. Pry the top out to remove it.
- **Longer ledge:** 26 long (was 8), X -105..-43, with 5 tapered ribs underneath, down to Z 0.5.
- **T-rails instead of screws:** 3 rails on the ledge at X -88, -74 and -60, 24 long, with an 8 wide top. They run through open-front slots in the floor, so the tray slides on from behind and the floor is held top and bottom: 0.15 clearance under it, 0.175 over it, 0.3 per side at the rail stems. The rails stop 4.5 short of the floor vents.

## Assembly order
1. Deck on the floor, with the Pi and ribbon in place.
2. Slide the tray straight onto the plate: T-rails, Pi ports and M6 tongues all engage along the same direction.
3. M6 screws (4 mm L-key), then the low M3 x 10 screw (2 mm L-key, with the fan mount off).
4. Fan on the mount, then clip the mount on.

## BOM change from H10
None; the 4 fan inserts move to the fan mount. Confirm fan screw length on hand (about M3 x 14 countersunk).

## Still to check
- **Clip fit:** the most uncertain part of this revision. Could be too tight, or loose enough to rattle with the fan running.
- **Rail slide:** clearances are calculated, not printed. Rail tops sit at Z 11.4..13, under the Pi board (Z 17.2); parts on the Pi's underside aren't modelled beyond its box.
- **Print:** the plate now stands 30 tall face down (was 13.3), with the ledge and thin rail tops as tall fins. Check that in the slicer, and watch the print time.
- From H9 and H10: only USB-C used on the Pi's side (the mount reaches 1 mm into the USB-C window), ribbon twist and reach, keystone cable bend, low M3 strength.

## Checks (digital only)
- Plate, floor, deck, fan mount: one closed shell, 0 bad edges, 0 degenerate faces.
- Intersections (`checks/pairwise.json`), all 0: every H10 pair, plus fan mount vs floor, deck, plate, fan, Pi, Hue and left post. Exceptions as in H10: deck vs Hue 5,097 mm3 (inherited box-vs-cradle overlap) and straight M6 driver lines vs the Hue box (hence the L-key).
- The clip-on and slide-on motions were not simulated; only the final positions were checked.
- 3MF: 8 objects, 19,252 vertex / 38,704 triangle tags, no ns0.

## Rebuild
`python src/SCR5-H11_build.py`, then `python src/SCR5-H11_finish.py`. Needs OpenSCAD and the local Hue cradle `C:/Users/brian/Downloads/Swanky Rottis.stl`.
