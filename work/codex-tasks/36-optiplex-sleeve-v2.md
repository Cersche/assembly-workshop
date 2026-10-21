# Task 36 · OptiPlex sleeve v2: height, foot grooves with click-in dip, cable opening, insert bosses

Brian printed SLV-A (faceplate + front 38 mm of the sleeve tray) on his real PC (badge: **OptiPlex 7060**; the STEP is the 7010) and reported on 2026-10-21. Standing rules in [README.md](README.md) apply. **SETTLED, don't change:** orientation (X is up + Rotate 90° once), the 44.4 mm faceplate on the front posts, the full 240 mm sleeve tray on rear support, the rear bracket on the rear posts, the 4 front M3 inserts and the 2 rear tongue screws. Fit, retention and strength stay UNKNOWN. No renders/exports/printing/commits/pushes; Claude renders and makes the coupon afterwards.

Brian's measurements and decisions (2026-10-21):
- The opening is about **0.5 mm too tight up and down**; the sides are fine (leave `sl_side=0.5`).
- Real feet stick out **2.75 mm** below the case (the STEP's 2.8 is right).
- Replace the foot pockets with **two smooth grooves** the feet slide along (like his working third-party bracket), ending in a **short sloped dip** so the PC clicks into place and doesn't slide out the front.
- The floor behind the PC needs a **simple cable opening** for the barrel plug and network cable only. Nothing fancy.
- **Not enough plastic around the 4 front heat-set holes** in the sleeve walls; he chose **outward bosses**.

All new behaviour sits behind new spec keys whose defaults reproduce today's output **byte-for-byte**. Old saved specs/revisions must not change.

## Build

Work in `equipment_tray.scad` (geometry), `equipment.py` (clean/validate/source), `tray-placement.js` (Place on tray controls + mirrored checks). Name every constant.

1. **Top play.** New key `sleeve_top` (mm, default 0.3 = today's `sl_top`; allowed 0.3..2). The OptiPlex coupon spec will use 0.8 plus the ride lift from item 2 (see there). Keep the existing 1U band assert and the lip-fits-in-U rule; report the resulting band above the opening.

2. **Foot grooves + click-in dip.** New key `feet_style`: `"pockets"` (default, today) or `"grooves"` (sleeve and flat mounts with feet only).
   - How it works: while sliding, the PC rides **on its feet** in the grooves with the case lifted by `sl_ride` (named constant, 0.5 mm). At the final position each foot drops into a dip and the case settles onto the floor top. That drop is the click.
   - **Groove:** one per foot track (feet that share an X range share a groove). Width = foot X extent + 2 × `foot_clearance`. Depth = `foot_h − sl_ride` below the floor top. It runs from the tray's front edge (Y = dev_y, flush with the faceplate's back) to the rear foot's final position, smooth, with no steps.
   - **Dip:** at every foot's final position (today's pocket box), deep enough that the case rests on the floor top (`foot_h + foot_extra_depth`, through the floor if needed, as pockets do today). Its **front and rear edges are 45° ramps** from the groove bottom, so the rear feet can cross the front dips on the way in (a mild bump) and the PC pulls out with a firm tug, no tool.
   - The lifted PC must clear the opening while sliding: with `feet_style="grooves"`, the opening height uses `sleeve_top + sl_ride`. So for the OptiPlex the opening is 36.0 + 0.8 + 0.5 = **37.3 mm** above the floor top. Report it.
   - **Floor under grooves:** groove bottom must keep ≥ `foot_min_floor` (0.8). The 3 mm floor leaves 0.75 under a 2.25 mm groove, so thicken the floor **downward only**, locally under each groove, to Z = 0 (the slot bottom; never below). Don't raise the floor top. If a groove still can't keep 0.8 mm, raise a clear error.
   - **Rear stop:** keep the tray's existing sleeve rear stop (`sl_stop_t` at `sl_rear`). It is the backstop the PC rests against, and the dips must line up with it. Don't add a second backstop on the rear bracket.

3. **Cable opening in the floor.** New key `rear_floor_opening` (bool, default false; only with `rear_support`). One rectangular through-opening in the floor between the sleeve rear stop and the rear joint uprights, centred on X, with 2 mm corner radius.
   - Keep ≥ 4 mm of floor to the rear stop, ≥ 3 mm to every rear tongue/upright/boss envelope (use the conservative `REAR_JOINT_HALF`-style envelopes from task 31), ≥ 5 mm to the sleeve walls, and no overlap with the strap slots or grooves.
   - For the OptiPlex, report the opening's exact X/Y. Expect roughly 60 × 30 mm.

4. **Outward insert bosses.** New key `insert_bosses` (bool, default false; sleeve + screw joint only). At each of the 4 front pilots:
   - Move the pilot outward so there's **≥ 2.0 mm** of plastic between the hole and the wall's inside face.
   - Add a round boss (axis along Y, from Y = 0 to 12 mm back) that leaves **≥ 3.0 mm** around the hole on the outside.
   - The boss must not reach inside the sleeve (clip it at the wall's inside face), below the floor bottom or above the lip top.
   - The faceplate's M3 clearance holes follow the new pilot X (they already derive from `sl_joints`).
   - Include the bosses in `tray_w` and in the Python/JS/SCAD 204 mm width checks. Report the new OptiPlex tray width (expect about 201–202 mm).

5. **Place on tray controls** (sleeve only, in the existing rear-support/rear-style area): "Top play (mm)", "Feet: Pockets / Grooves", "Cable opening in floor", "Stronger insert bosses". Short hints; fit and strength stay UNKNOWN in the wording. Mirror the validation in `tray-placement.js`.

## May change

`equipment_tray.scad`, `equipment.py`, `tray-placement.js`, `asset-manifest.json`, `test_*.py`, `js-tests/` (register new tests in `js-tests/run.js`). Nothing else: never data/normal-use, coupon folders, revisions or third-party files.

## Checks and report

- Run `run_checks.ps1` before and after.
- **Byte-identity:** every existing test fixture and the SLV-B / SLV-D / SLV-E specs must give identical cleaned specs and SCAD source with the new keys absent.
- **New tests (analytical, no render):** using the SLV-B OptiPlex spec plus `sleeve_top=0.8, feet_style="grooves", rear_floor_opening=true, insert_bosses=true`, check:
  - the groove depth/width, the ≥ 0.8 floor and the dip ramp angles;
  - the opening height (37.3) and the band above it;
  - the cable opening's clearances;
  - the boss wall thicknesses (≥ 2.0 inside, ≥ 3.0 outside) and the tray width ≤ 204;
  - error paths (feet too tall for grooves, a too-small floor for the opening).
- Write `work/codex-tasks/36-optiplex-sleeve-v2-REPORT.md` with files + SHA-256 before/after, the numbers above, commands actually run and open questions. Claude reviews it, renders it and makes the next coupon (front section with grooves/dip/bosses, unique ID).
