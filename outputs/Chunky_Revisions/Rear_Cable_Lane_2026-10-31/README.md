# Rear cable management set CBL-A..E (Claude, 2026-10-31)

Brian: data lane LEFT, power lane RIGHT (as seen from the rear), exit bottom-rear. All parts bolt to the rack posts with M6 x 8 button heads into the M6 heat-set inserts (2 per U at hole pitch +/-15.902 about the U centre, X +/-118.2625). Not printed; fit, capacity, retention, strength and insert engagement UNKNOWN.

| ID | Part | Where | Notes |
|---|---|---|---|
| CBL-A | 1U lane module (R = PWR, L = DATA) | rear posts, U2-U8 | trough 24 x 22, 45 deg hook lip, side window, 16 mm Velcro strap slot through both walls |
| CBL-B | exit chute (A module + flared chute 36 mm) | rear posts, U1 | conflicts with the RW wall-mount standoffs at U1 |
| CBL-C | power strip / DC block ledge pair | rear posts, one U (shown at U2) | ledge 16 mm, web stops the strip end; `strip_w` = 50 is a GUESS, strip must be <= ~200 long; strap slots both sides |
| CBL-D | 1U blanking panel with patch comb | front, any empty U | standard 252 x 44.4 x 4 plate, four corner holes O6.6; comb 17 fingers, 12 mm pitch, 10 mm deep; pitch is a GUESS |
| CBL-E | window comb (R/L) | pushes into the CBL-A inner-wall window | two 8.2 mm cord lanes; friction fit only, no retention yet |

Sources: `src/CBL-A.scad` (`part`, `s`, `uz`, `tag`, `label` via -D), `src/CBL-BCDE.scad` (includes A), `src/pack_3mf.py`, `src/check_mesh.py`. Print file: `CBL-A-E_cable_management_set.3mf` (9 objects). STLs in this folder are installed-orientation. `src/placeholder_strip.scad` is a viewer-only stand-in, not a part.

Open: the U9/U1 rear insert holes are used by the RW wall mount; CBL-B and the lane need U1, so choose one or the other. Clash check against the 4U post mesh not run yet.
