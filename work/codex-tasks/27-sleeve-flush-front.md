# Task 27 · "Sleeve" mount with a flush front window, tested on rear-post support

Do this after tasks 25 (44.4 mm plate, Z=0 = slot bottom) and 26 (204 mm width limit).

Brian, 2026-10-20 (OptiPlex beta): "sleeve option is definitely the way to go. This is also a heavier item, so it could be a good test case for the rear post supported tray." Reference: a third-party OptiPlex bracket that Brian says fits his rack. It is studied in `work/optiplex-bracket-study/Report.md`; read that report. The bracket's files are third-party: never open, copy or redistribute them; use only the numbers in the report.

Bracket summary:
- 1U sleeve, 201 mm outside, 9 mm side walls, 183 × 37 mm inside (0.25 mm per side: "a tight squeeze").
- 3.7 mm floor and roof ledges, 15.5 mm wide, running the full depth.
- A front window equal to the inside, so the PC front is flush with the panel and the power button and front USB are open.
- Open rear. Front ears only.

Our design must stand on its own. The bracket's fit does not transfer to it; fit, retention and strength stay UNKNOWN. Printing is not authorized.

Standing rules in [README.md](README.md) apply.

## Build

1. **New mount `sleeve`** ("Sleeve: boxed in, front flush (PCs, boxes)") beside inserts / pegs / clips / straps / flat.
   - No standoffs, no holes needed.
   - The device sits on the tray floor, with the same floor rule as `flat` after task 25.
   - Two side walls run along the device's full depth. The roof is a lip along the top of each wall, reaching inward over the device's top edges, if it fits the height budget (point 3). If it doesn't fit, build the walls only and say so in a one-line note in Place on tray.
   - Add a rear stop (a low bar or corner blocks behind the device) so the device stops flush when slid in from the front. The front is open because you insert it there.
   - Keep the strap slots from `flat` so it can also be strapped.
   - Lightening windows in the walls are optional. Add them only if you can show they don't weaken the joint areas; explain your choice.
2. **Parameters**, each a named constant with a short comment saying it is a PROPOSED default:
   - side clearance 0.5 mm per side;
   - top clearance 0.3 mm;
   - wall thickness (your choice, at least 4 mm; the outside width must still pass the task 26 limit);
   - lip width about 10 mm;
   - minimum lip thickness 1.5 mm;
   - minimum plate band above and below the window 1.5 mm.

   State in the report which numbers come from the bracket study and which you chose.
3. **Height budget** (Z=0 = slot bottom after task 25): floor bottom ≥ 0.5, and the device top + top clearance + lip must stay ≤ `u*44.45`.
   - OptiPlex check: 182.5 × 194.5 × 38.8 (the STEP size includes feet; Brian hasn't said yet whether his are removed). It must build as 1U with walls.
   - Report the lip and window band you get for it.
4. **Flush front** (always on for `sleeve`):
   - The faceplate gets a window the size of the device front plus the side and top clearances.
   - The device front sits flush with the plate front, so the device passes through the plate.
   - The plate keeps a band of at least the minimum above and below the window. If it can't, block with a plain message ("Too tall for a flush window in 1U; choose 2U").
   - The rack slots, the 2.5 mm corners and the keystone rules stay. Keystones and front port cut-outs are not allowed inside the window; ports outside it still work.
   - Entered front openings that fall inside the window are dropped with a note, since the window already exposes them.
5. **Joint:** the bottom-centre screw tongues and bosses would sit in the window, so move the joint for `sleeve`.
   - Join the plate to the front ends of the side walls (and/or the floor strip under the window), outside the window.
   - Reuse the proven parts: M3, `m3_clear 3.4`, `joint_pilot 4.0` heat-set pilot (the printed, well-fitting Pi4 trial value).
   - `single` (one-piece print) must also work for `sleeve`.
   - Explain the joint in the report.
6. **Rear-post support:**
   - `sleeve` with `rear_support=true` must build: the tray runs to the rear posts and screws to the rear bracket (screw joint only, as today).
   - The walls stop behind the device. Check that the rear stop and the device clear the rear joint (≥ 11.5 mm, as for flat).
   - The OptiPlex sleeve on rear support is the reference test case.
7. **Wizard:** add `sleeve` to the mount choices (Place on tray, and the "Tray default mount" from task 24), with a short hint line.
   - The live box sketches and the exact preview show the walls, lips, window and rear stop.
   - Python and JS share the same rules (height, width including walls, window bands, joint clearances).
8. Update asset-manifest.json hashes for changed front-end files.

## Tests

- OptiPlex sleeve 1U, `dev_rot` as needed so 182.5 is across:
  - validates;
  - outside width ≤ 204;
  - window size equals device front + clearances;
  - bands ≥ 1.5 mm or a clear rejection;
  - joint outside the window.
- The same with `rear_support=true` validates and keeps ≥ 11.5 mm rear clearance.
- `single` + sleeve validates; `single` + rear support is still rejected.
- A device too tall for the window bands in 1U is rejected with the message.
- Existing mounts are unchanged by this task.
- No STL exports. Run render tests only where the existing tests already do so in a temp folder.

## May change

`equipment_tray.scad`, `equipment.py`, `equipment-wizard.js`, `tray-placement.js`, `port-openings.js`, `port_openings.py` (only if the opening rules need the window), `cable-ports.js` (only if the lift/front face moves), `asset-manifest.json`, `test_*.py`, `js-tests/`. Nothing else; never data/normal-use or the third-party bracket files.

## Checks and report

Run `run_checks.ps1` before and after. Write `work/codex-tasks/27-sleeve-flush-front-REPORT.md` with:
- files with SHA-256;
- every new parameter and its value and source;
- the OptiPlex numbers (outside width, wall, lip, window, bands, joint position, rear clearance);
- what holds the device;
- check results;
- open questions.

Claude browser-checks with the OptiPlex STEP afterwards. A clearance coupon (with a test print ID) can follow if Brian wants one.
