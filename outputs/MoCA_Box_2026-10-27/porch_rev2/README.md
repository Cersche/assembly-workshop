# MoCA box: porch rev 2 + new sleeve (2026-10-27)

Replaces the porch, bezel nut and sleeve in `../MoCA_box_and_porch.3mf`. The back plate, lid, cradle rev B
(`../cradle_revB/`) and nut sliders are unchanged and still fit (same joint blocks).

`MoCA_porch_rev2.3mf`: the three parts side by side, each its own object, flat on the bed; the same parts are also
here as single STLs. All three are closed meshes. Source: `work/wall-box-wizard/concept15/porch16.scad` (`-D pick=1` porch,
`pick=2` nut) and `body15.scad` (`sleeve()`, turned back edge down), at the commit that added this note.

| Part | Size on bed (mm) | Orientation | What changed |
|---|---|---|---|
| sleeve | 117 x 210 x 72.5 | back edge down (as before) | 2026-10-28: power plug comes straight down through a 10 mm floor hole under the ScreenBeam jack (X38.5 Y43; plug 7.75 dia, 35 below the jack); ear slots and right-angle F hole 8 mm forward (splitter moved so the IN coax clears the plug); three porch screw bosses (X18 Y42, X78 Y5, X86 Y62); Ethernet keystone + LAN label up the right wall at Z121.5 Y22, between the louvre sets; left-wall power hole and PWR label removed |
| porch | 87.6 x 75.6 x 19.6 | floor down, open top up | sized to the calipered splitter; modem OUT outside; 2026-10-28: splitter 8 mm forward, power lobe reaches forward over the plug (0.4 off the bezel nut), front-right lug for the third screw, MODEM label on the front face; step wall between the OUT posts moved 0.5 and thinned to 1.6 (2026-10-28, 1 mm off the right-angle nut, nut size assumed); IN post slot 11 wide (was 10); own two screws; power lobe with slit and two posts; IN / PWR / MODEM labels |
| bezel_nut | 13.9 x 13.9 x 2 | flat | 14 x 2 (was 21.5 x 3), thread bore 0.4 mm looser |

Hardware: 3 more M3 heat-set inserts (porch bosses), 3 M3 x 20 (porch), 2 M3 x 16 (splitter ears into the nut
sliders; replaces the M3 x 40). The rest is as in `../README.md`.

PROPOSED - UNVALIDATED. Not printed. Power plug size through the 12 mm hole, cord grip in the slit, printed thread,
room for the 45 mm power plug above the floor, fit and strength are UNKNOWN. No slicer settings are given or implied.
