# TP-Link ER605 one-piece bracket — test-print ID ER6-A (2026-11-04)

PROPOSED — UNPRINTED. Print-friendly remix of Mixmeister's "TP-Link ER605 Omada 10-inch rack mount" (MakerWorld, BY-NC-SA), no-keystone version. Rebuilt from scratch in OpenSCAD from that part's measured dimensions; no source mesh is inside. Router fit, rack fit and strength are UNKNOWN. Router size is not measured: the pocket is the source's.

## Print

`ER6-A_ER605_bracket.3mf`, also in `outputs/Final_3MF/`: one object, front face on the bed, no supports. 252 x 44.4 x 106.7 mm, 96.6 cm3 solid volume. `ER6-A_ER605_bracket.stl` is the same part in rack position.

## Install

Four rack screws in the plate. Router slides in from the front through the plate window until its rear corners meet the two stops. No other hardware. Nothing holds the router forward except friction, same as the source.

## Kept from the source

Pocket 158.7 wide x 25.7 tall, 101.7 from plate front to rear stop (router ends about flush with a 101 deep case). 4 mm walls. Bottom wall open to the rear, 14 wide arms (X ±69.35..83.35), opening starts Y 12.8. Rear open for the power lead.

## Faceplate standard (changed from the source's 254 x 44.5)

252 wide, 44.4 per U, 4 thick, R2.5 corners, four 10 x 7 slots at X ±118.2625, Z 6.323 / 38.127. Same code as `equipment_tray.scad`. Compared with the SG8-M6-F faceplate mesh: same outer bounds, ears and slots match within 0.12 mm (circle facet differences).

## What changed for printing

| Feature | Source | ER6-A | Why |
|---|---|---|---|
| Rear stop | 5 x 5 bars bridging 25.7 mm, near the top of a 107 tall print | 45° wedge turning in from each side wall, same 5 reach | No bridge. Router's rear corners stop on the wedge line |
| Top wall vents | About 40 hexes, 2 mm struts, half hexes at the edges, roofs 30° off flat | 17 whole hexes, 22 wide, 4 mm struts, 45° roofs | Roofs self-support; fewer retractions; no slivers |
| Side windows | Flat 8 wide top | Pointed 45° ends, 17 tall | No bridge |
| Plate-to-sleeve root | 3 mm chamfer | 5 mm chamfer | More layer area where a face-down print is weakest. Adds no overhang |
| Sleeve outer corners | Square | R2 | Cleaner corners, less corner lift |
| Window front edge | Square | 0.4 at 45° | First-layer squish can't pinch the router on the way in |

Faces steeper than 45° off the bed: source 2948 mm2, ER6-A none (a 0.01 mm modelling step at each wedge start, 0.57 mm2 in all, is too small to print).

## Checks (digital only)

`python src/pack_check.py . <SG8-M6-F_faceplate.stl> <source.stl>`: closed mesh; 158 x 101 x 25 box flush with the plate front and on its way in from the front clears the bracket; 3MF plain tags 1854 vertex / 3800 triangle. Sleeve plus root reaches X ±88.35; post inner faces are at X ±111 and beyond by the recorded numbers (not re-run against the post mesh).

## UNKNOWN

Router's real size, corner radius, foot height and foot positions (feet may land on the arms); how far the rounded rear corners run into the wedges (router may sit slightly proud); whether friction holds it when unplugging cables; layer strength at the root; any neighbour-U clash with cables. Slicer settings not tried.
