# MoCA box: ScreenBeam cradle rev B (2026-10-27)

Replaces the cradle in `../MoCA_box_and_porch.3mf`. Nothing else changes: same four back-wall bosses, same M3 screws and
inserts, same Velcro strap.

Why (Brian, after the first print): the braided jumper was about an inch short of the ScreenBeam's Coax In, and the
cradle couldn't slide lower because its keystone-side shelf pad hit the Ethernet keystone. Also, the ScreenBeam's
rubber feet (13 mm across, 2.25 mm proud) held it off the plate.

| Change | Rev A | Rev B |
|---|---|---|
| ScreenBeam height | shelf at Z62 (box floor = 0) | shelf at Z37, 25 mm lower (the ±6 mm slot travel is still there) |
| Sideways | ScreenBeam X17.5..82.5 | X14.5..79.5, 3 mm away from the keystone |
| Keystone-side pad | ran 3 mm past the ScreenBeam edge (to X85.5) | ends 2 mm inside it (X77.5), 8 mm further from the keystone |
| Power-side pad | 21.5 wide | 16 wide, trimmed on the inner face for power-plug relief (Brian) |
| ScreenBeam clearance | lips tight on the device | +0.5 mm: side lips 0.25 further out each side, front lips 0.5 further from the plate (`sb_clr`, Brian: tight squeeze) |
| Feet | none | four pockets, 16 across x 2.6 deep |
| Plate | 97 x 102 | 97 x 131 (extended down to reach the lower shelf) |
| Strap slots | Z100..124 | Z85..109, moved with the ScreenBeam and clear of the screw slots |

`MoCA_cradle_revB.3mf` / `.stl`: one part, back face down, 97 x 131 x 37.5 mm, closed mesh, support-free (same pad
gussets as rev A). Source: `cradle15()` in `work/wall-box-wizard/concept15/c15.scad` (`sb_dx`, `sb_dz`, `sb_feet`),
export `-D pick=4` on `porch15.scad`.

PROPOSED - UNVALIDATED. Brian said to assume everything fits: room for the Ethernet and power plugs below the lowered
ScreenBeam, and keystone clearance, were NOT checked against real parts. The foot positions come from ruler photos
(±1 mm). Fit and strength are UNKNOWN.
