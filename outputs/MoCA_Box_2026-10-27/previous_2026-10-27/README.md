# MoCA box + porch, concept 15 (2026-10-27)

`MoCA_box_and_porch.3mf`: every part once in its print orientation, flat face on the bed, laid out side by side
(the parts together are bigger than one bed: use the slicer's arrange / add plates). Built from
`work/wall-box-wizard/concept15/body15.scad` and `porch15.scad` at the commit that added this note.

| Part | Qty | Size on bed (mm) | Orientation |
|---|---|---|---|
| sleeve (4 walls, hinge, magnets, louvres, PWR/LAN labels) | 1 | 117 x 210 x 72.5 | back edge down |
| back_plate (keyholes, cradle bosses, alignment lip) | 1 | 105 x 210 x 10.5 | outer (wall) face down |
| lid (louvres, hinge knuckles, magnet pockets) | 1 | 116.4 x 210 x 9.1 | outer face down |
| porch (IN/MODEM labels) | 1 | 60.7 x 75 x 33 | floor down |
| cradle (ScreenBeam) | 1 | 97 x 102 x 37 | back face down |
| bezel_nut (printed 3/8-32 F thread) | 1 | 21.4 x 21.4 x 3 | flat |
| nut_slider | 2 | 14 x 12 x 6 | pocket down |

Designed support-free; the sleeve and back plate need a bed of at least ~210 mm in one direction.

Hardware (not in the file): 12 M3 heat-set inserts (6 sleeve joint blocks, 4 cradle bosses, 2 hinge sets), 6 countersunk M3 x ~8 (back plate), 2 M3 x ~30 (hinge), 2 M3 x 40 + 2 M3 nuts (porch/splitter),
4 disc magnets 6 x 1.6 mm (opposite poles facing), Velcro strap ~20 mm, Ethernet keystone, F right-angle,
F male-male barrel, braided jumper. Cradle screw sizes as in Scope.md.

PROPOSED - UNVALIDATED. Not printed. Fit, strength, hinge play, printed thread, magnet hold, screw lengths and every
splitter/ScreenBeam size (photo estimates) are UNKNOWN. No slicer settings are given or implied.
