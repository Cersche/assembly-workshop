# SG8-M6-D — TP-Link TL-SG108E 1U bracket, M6 hardware (2026-10-30)

Test-print ID **SG8-M6-D** is engraved (0.6 mm) on the back of the faceplate between the screw bosses and on the outside of the left sleeve wall.
M6 redesign of the printed baseline `outputs/STL_Deliveries/2026-10-23_TL-SG108E_flush/` (kept unchanged). **Not printed. Fit and strength UNKNOWN.**

| File | What |
|---|---|
| `SG8-M6-D_TL-SG108E_M6_set.3mf` | Tray + faceplate side by side; faceplate object = faceplate + UPLINK label inlay |
| `SG8-M6-D_tray.stl`, `SG8-M6-D_faceplate.stl`, `SG8-M6-D_UPLINK-label-inlay.stl` | Separate parts (closed meshes, 0 open edges) |
| `src/SG8-M6-D_build.py` | Build: `python src/SG8-M6-D_build.py <out_dir>` (app generator + patch, as the baseline) |
| `src/SG8-M6-D.scad` | Exact generated source; `src/label_3mf.py` packs the 3MF |

**D vs C (Brian, 2026-10-30: printed C did not fit):** B had cut the sleeve top clearance from the proven 1.35 mm (2026-10-23 flush print, fit acceptable) to 0.35 mm, reading Brian's "~1 mm spare above the switch in the opening" as a sleeve change. D puts `sleeve_top` back to 1.35 (sleeve inside height 26.35 = switch 25 + 1.35, same as the print that fit). The hidden-screw bosses/uprights follow the sleeve top as before. Everything else is C. `previous_SG8-M6-C/` is C. Not printed.

**Fit numbers vs the proven 2026-10-23 print:** device 158 x 100 x 25, offset X -15, sleeve side play 0.5, sleeve top 1.35, keyholes 48.5 behind port face / 110 apart, keystone +88: all **same**. Changed on purpose: switch 1.3 mm further back (Brian: it stood 1.3 proud), M3 → M6 hidden screws, rounded tray corners.

**BOM:** 2 × rack M6 heat-set insert + 2 × M6 x 8 button-head screw. That's all.

**B vs A (Brian's fit report on the printed 2026-10-23 version, 2026-10-28):** the switch stood ~1.3 mm proud of the plate front and had ~1 mm spare clearance at the top of the opening. B sets the switch 1.3 mm back (rear stop and keyhole detents move with it) and cut the sleeve inside height to 25.35 mm (sleeve_top 0.35; wrong, undone in D). The lower window top let the bosses grow to 12 mm. `previous_SG8-M6-A/` is the unprinted A.

**C vs B (Brian, 2026-10-29: tray prints warp, sharp corners don't help):** the tray footprint corners are rounded through the full height: rear corners R 20 (clear of the switch corner; the rear-stop ends and wall rear ends follow the curve), front corners R 5 (the side walls stand only 1.5 mm in from the floor edge, so a ~1.4 mm sliver goes from each wall's outer front foot; the screws, not that corner, locate the tray). Everything else is identical to B; the faceplate differs only in its engraved ID. `previous_SG8-M6-B/` is B. Warping reduction is UNKNOWN until printed.

What changed vs the baseline (everything else is identical to the baseline):
- The two hidden M3 screws became M6. Faceplate bosses: 7.6 mm bore (rack post insert hole), 7 mm deep, 12 mm across (~2.2 mm wall), top clipped flush with the plate top, centred Z 38.4 (was 39.65), X −92.5 / +62.5.
- Sleeve uprights: 16 wide (was 12), 6 thick, 6.6 mm clearance hole + 11.5 × 3.5 mm head counterbore (open where it runs out of the upright), 2.5 mm under the head, so the M6 x 8 reaches ~5.2 mm into the insert.
- Kept: hidden screws (none through the front), keyhole detents (2 mm bump, 6.5 mm floor), rear stop, flush ports, keystone at +88, UPLINK inlay. Faceplate: only the four corner rack slots.

Why not the generator's `m6_joint` option: it supports non-sleeve trays only; this bracket is a sleeve with hidden screws, so the baseline's patch approach was kept.

UNKNOWN: insert OD/length (thin 1.8 mm boss wall may bulge on insertion), boss/upright strength, fit, detent behaviour as before.
