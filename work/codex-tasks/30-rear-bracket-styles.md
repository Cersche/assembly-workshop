# Task 30 · Rear bracket styles: more material, vents, a choice

Do this after task 29 (done).

Brian, 2026-10-20, looking at the task-29 rear bracket (SLV-D): "that rear bracket could probably use a little more meat on them. When adding vent holes, let's give some options. In the wizard we'll do this." SLV-D itself stays as is for his current test print.

Also relevant: the OptiPlex blows its exhaust out of the back. Its rear face has a large vent grille (see the Dell STEP model), so the rear bracket needs airflow as well as cable passage.

Standing rules in [README.md](README.md) apply. Fit, stiffness, airflow and strength stay UNKNOWN. Printing and exports are not authorized.

## Build

1. **Replace the boolean with a style.** Add a new spec key `rear_style`, a placement key next to `rear_openings`, with these values:

   | Style | What it is |
   |---|---|
   | `solid` | today's plain plate |
   | `open` | the task-29 windows, unchanged; equivalent to `rear_openings: true` |
   | `reinforced` | the same window layout as `open` but with more material (constants below), plus stiffening flanges on the **outer** face |
   | `slots` | mostly solid: one long cable slot above the bosses and one centre slot between them, 5 mm corner radius |
   | `vents` | a staggered grid of round vent holes over the free plate area, plus one centre cable slot between the bosses, plus the outer flanges |

   - **Compatibility:** `rear_openings: true` with no `rear_style` means `open`. Neither key means `solid`. Old sources stay byte-identical, as in task 29.
   - **Defaults:** new rear-supported items default to **`reinforced`**. Brian asked for more meat; say so in the report if you think another default is better.
2. **More material (PROPOSED named constants)**, for `reinforced` and the slot/vent styles:
   - joint margin 6 (was 4);
   - top/bottom bands 5 (was 3.5);
   - strip between the upper and lower windows 6 (was 4);
   - openings stop at X ±96.
3. **Outer flanges** (`reinforced`, `vents`):
   - 2.5 mm thick lips standing 8 mm out from the bracket's outer face (away from the tray, behind the rack);
   - along the top and bottom edges, and down both ends at X ±100.
   - They must stay inside X ±100 so they clear the rear posts. They must not touch the rack slots or the plate edge rounding.
   - Check they don't collide with anything the app models.
4. **Vent grid** (`vents`):
   - round holes, PROPOSED d 6 on a 9 mm staggered pitch;
   - only where the plate is free: outside the joint keep-out, the bands, the ears and the cable slot;
   - leave out partial holes.
   - Name the constants. Keep the mesh light enough to render quickly: count the holes and report it.
5. **Multi-U:** every style works for 1U–5U, with the same rules per U (repeat the joint keep-out conservatively, as task 29 does). Leave out any window or slot under 10 mm.
6. **Choice in Place on tray** (the wizard delegates tray choices there; if a wizard step does show rear support, add it there too):
   - replace the task-29 checkbox with a chip row: "Rear bracket: Solid · Open · Reinforced · Cable slots · Vents";
   - shown only when rear support is on;
   - each style gets a one-line hint ending "stiffness/airflow UNKNOWN";
   - the box sketch notes the style.
   - Update asset-manifest.json hashes.

## Tests

- Old specs (no key; `rear_openings` false or missing) give unchanged source.
- `rear_openings: true` with no style gives exactly the task-29 `open` source.
- For each style, on the OptiPlex sleeve rear-support spec and on a 2U inserts tray, analytical checks:
  - margins, bands and strip are at least the constants;
  - nothing cuts into the bosses, tongues or rack slots;
  - flanges stay within X ±100.
- `rear_style` is dropped when rear support is off; invalid values are rejected.
- No STL exports.

## May change

`equipment_tray.scad`, `equipment.py`, `tray-placement.js`, `equipment-wizard.js` (only if it shows rear support), `asset-manifest.json`, `test_*.py`, `js-tests/` (register new tests in `js-tests/run.js`). Nothing else; never data/normal-use, the coupon folders or third-party files.

## Checks and report

Run `run_checks.ps1` before and after. Write `work/codex-tasks/30-rear-bracket-styles-REPORT.md` with:
- files with SHA-256;
- each style's rule and constants;
- the OptiPlex numbers per style (windows, slots, vent count, flanges);
- check results;
- open questions.

Claude reviews it and renders every style for the OptiPlex afterwards (mesh closure, measured clearances), then shows Brian.
