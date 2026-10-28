# MoCA box: porch rev 2 + new sleeve (2026-10-27)

Replaces the porch, bezel nut and sleeve in `../MoCA_box_and_porch.3mf`. The back plate, lid, cradle rev B
(`../cradle_revB/`) and nut sliders are unchanged and still fit (same joint blocks).

`MoCA_porch_rev2.3mf`: the three parts side by side, each its own object, flat on the bed; the same parts are also
here as single STLs. All three are closed meshes. Source: `work/wall-box-wizard/concept15/porch16.scad` (`-D pick=1` porch,
`pick=2` nut) and `body15.scad` (`sleeve()`, turned back edge down), at the commit that added this note.

| Part | Size on bed (mm) | Orientation | What changed |
|---|---|---|---|
| sleeve | 117 x 210 x 72.5 | back edge down (as before) | two porch screw bosses (M3 heat-set inserts) in the floor, 12 mm power hole at X20 Y54.5, left-wall power hole and PWR label removed |
| porch | 87.6 x 75 x 19.6 | floor down, open top up | sized to the calipered splitter; modem OUT outside; own two screws; power lobe with slit and two posts; IN / PWR / MODEM labels |
| bezel_nut | 13.9 x 13.9 x 2 | flat | 14 x 2 (was 21.5 x 3), thread bore 0.4 mm looser |

Hardware: 2 more M3 heat-set inserts (porch bosses), 2 M3 x 20 (porch), 2 M3 x 16 (splitter ears into the nut
sliders; replaces the M3 x 40). The rest is as in `../README.md`.

PROPOSED - UNVALIDATED. Not printed. Power plug size through the 12 mm hole, cord grip in the slit, printed thread,
room for the 45 mm power plug above the floor, fit and strength are UNKNOWN. No slicer settings are given or implied.
