# SCR5-J5: J4 tray with the Hue cradle loosened (2026-11-05)

Brian's fit notes on the printed SCR5-J4: the Hue cradle is too tight. J5 changes only the tray (deck); plate, front frame, rear frame, fan mount and wedge pins stay J4 / H8. Test-print ID **SCR5-J5** on the tray underside. J4 stays as it was. **Not printed.** Hue fit, hold, sag and strength UNKNOWN.

## What changed from J4
- Each of the 4 cradle corner posts (Brian's `Swanky Rottis.stl`, read in place) moves **0.4 out in X**, so the gap is **0.8 wider** side to side.
- The two front posts move **0.8 forward**, so the gap is **0.8 longer** front to back. The rear posts stay put: they already sit on the tray's rear edge (Y 116).
- Everything else on the tray is J4.

## Print
`SCR5-J5_tray.3mf` (also in `outputs/Final_3MF/`), one object, upright as J4. Reprint only the tray.

## Checks (digital only)
- Tray: one closed shell, 0 bad edges, 0 degenerate faces, bounds as J4 (rear edge still Y 116).
- `checks/pairwise.json`, 152 pairs: identical to J4 except the Hue against the tray (ghost Hue box overlaps the posts less: 2197.9 → 1318.7 mm³; removal poses 0 and 1 also smaller). The ghost Hue is a rounded 88 x 88 box, not the real shape, so these numbers don't prove the fit.
- 3MF: 1 object, 2,922 vertex / 5,852 triangle tags, no ns0.
- Other parts were rebuilt only as references in `checks/ref_J4_*.stl`.

## Rebuild
`python src/SCR5-J5_build.py`, then `python src/SCR5-J5_finish.py`. OpenSCAD 2021.01 (same as J4), trimesh, numpy and `C:/Users/brian/Downloads/STL/Swanky Rottis.stl`. `cradle_loose` in `src/SCR5-J5.scad` sets the shift.
