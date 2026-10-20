# Physical test kit — 2026-10-18

Generated at Brian's direction from the equipment wizard template (`equipment_tray.scad`). Each piece covers geometry that has **not** been printed before. Everything here is PROPOSED — UNVALIDATED until you print and check it. Hashes are in `manifest.json`; each piece's exact source is in its `__source.scad`.

## Print list (7 files)

| File | What it tests |
|---|---|
| `A_…__faceplate.stl` + `A_…__tray.stl` | **Main test.** New 4 mm faceplate with rounded corners, screw joint (4.0 mm insert hole, the size that worked on the Pi print), two keystone openings with rear pockets, Pi heat-set insert bosses |
| `B_…__faceplate.stl` + `B_…__tray.stl` | Snap-fit tabs joining the tray to the faceplate; printed pegs that the Pi pushes onto |
| `C_…__combined.stl` | Tray and faceplate as **one** print; snap clips holding the Pi by its edges |
| `D_…__tray.stl` | Strap / zip-tie slots (tray only; screws onto faceplate A) |
| `E_…__faceplate.stl` | 2U faceplate: rack slot spacing across two units, plus one keystone (faceplate only) |

Rack frame parts aren't included because your rack is already printed. They can be downloaded from the app (rack selected → "Download rack frame STLs").

## Hardware to have on hand
- Raspberry Pi 4 board
- For A: 2 × M3 heat-set inserts + 2 × M3 screws for the joint; 4 × small inserts for the Pi bosses (3.2 mm hole, sized for M2.5 inserts) + matching Pi screws
- 2–3 keystone jacks (any standard snap-in jack)
- Zip ties or a Velcro strap (for D)
- M6 bolts/inserts as you normally use for the rack mounting slots

## Checklist (write down pass / fail / notes for each)
1. **A faceplate in the rack:** do the slots line up with the rack holes in a 1U slot? Do the 4 mm thickness and rounded corners clear the neighbouring slots?
2. **A joint:** do the tray tongues slide into the faceplate? Do the M3 inserts go into the 4.0 mm holes cleanly, and does the screw pull the joint tight?
3. **A keystones:** does a jack snap in from the front and stay put? Is it too tight or too loose?
4. **A Pi bosses:** do the small inserts seat, and does the Pi line up with all 4 holes?
5. **B snap tabs:** does the tray click onto the faceplate arms, and can it come apart without breaking?
6. **B pegs:** does the Pi push onto the pegs and stay on? Do any pegs snap off?
7. **C single piece:** does it print cleanly in one go (it may need supports under the tray), and do the clips hold the Pi without cracking?
8. **D straps:** do zip ties thread through the slots and hold the Pi flat?
9. **E 2U plate:** do both pairs of slots line up with the rack holes across 2U?

Bring the notes back and I'll adjust the template (tolerances, thickness, clip strength) to match.

## Limits
These results will apply only to your printer, material and settings. Strength, long-term hold and screw torque remain UNKNOWN unless you specifically test them. Faceplate A was rendered with a 0.023 mm repair nudge (see manifest), far below what a printer can show.
