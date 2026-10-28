# SG8-M6-A — TP-Link TL-SG108E 1U bracket, M6 hardware (2026-10-28)

Test-print ID **SG8-M6-A** is engraved (0.6 mm) on the back of the faceplate between the screw bosses and on the outside of the left sleeve wall.
M6 redesign of the printed baseline `outputs/STL_Deliveries/2026-10-23_TL-SG108E_flush/` (kept unchanged). **Not printed. Fit and strength UNKNOWN.**

| File | What |
|---|---|
| `SG8-M6-A_TL-SG108E_M6_set.3mf` | Tray + faceplate side by side; faceplate object = faceplate + UPLINK label inlay |
| `SG8-M6-A_tray.stl`, `SG8-M6-A_faceplate.stl`, `SG8-M6-A_UPLINK-label-inlay.stl` | Separate parts (closed meshes, 0 open edges) |
| `src/SG8-M6-A_build.py` | Build: `python src/SG8-M6-A_build.py <out_dir>` (app generator + patch, as the baseline) |
| `src/SG8-M6-A.scad` | Exact generated source; `src/label_3mf.py` packs the 3MF |

**BOM:** 2 × rack M6 heat-set insert + 2 × M6 x 8 button-head screw. That's all.

What changed (everything else is identical to the baseline):
- The two hidden M3 screws became M6. Faceplate bosses: 7.6 mm bore (rack post insert hole), 7 mm deep, 11.2 mm across (the most the 11 mm above the switch window allows; ~1.8 mm wall), top clipped flush with the plate top, centred Z 38.8 (was 39.65), X −92.5 / +62.5.
- Sleeve uprights: 16 wide (was 12), 6 thick, 6.6 mm clearance hole + 11.5 × 3.5 mm head counterbore (open where it runs out of the upright), 2.5 mm under the head, so the M6 x 8 reaches ~5.2 mm into the insert.
- Kept: hidden screws (none through the front), keyhole detents (2 mm bump, 6.5 mm floor), rear stop, flush ports, keystone at +88, UPLINK inlay. Faceplate: only the four corner rack slots.

Why not the generator's `m6_joint` option: it supports non-sleeve trays only; this bracket is a sleeve with hidden screws, so the baseline's patch approach was kept.

UNKNOWN: insert OD/length (thin 1.8 mm boss wall may bulge on insertion), boss/upright strength, fit, detent behaviour as before.
