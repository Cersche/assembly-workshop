# CM1000 bracket CM6C — test-print ID CM6C (2026-11-01)

PROPOSED — UNPRINTED. Fit, strength and insert retention UNKNOWN.

Replaces CM6A, which Brian printed: the modem only went in by force and pushed the rail rear ends out to 228 mm across (design 220.46). CM6A stays untouched in `outputs/CM1000_M6_2026-10-28/`. Remix of noyoustupid / Jsmaz3 (CC BY-NC-SA): personal use, keep local/private, never redistribute. Brian approved changing the channel shape (2026-11-01), an exception to "baseline + M6 hardware only".

## Cause

The modem's end wedge is blunter than the baseline channel. Brian measured the modem at 44.5 tall with a 12 mm end wedge; the channel had a 14.2 mm wedge over about 40 mm. The spread of 3.8 mm per side matches the calculated overlap. Tip-to-tip width was not measured: tip position x20.38 is worked back from the 228 mm spread.

## Print file

`CM6C_CM1000_M6_bracket_set.3mf`: three objects, same layout and colour parts as CM6A. IDs CM6C-F / -L / -R are engraved 0.5 mm into each part. Single STLs use the rack frame: `CM6C_faceplate.stl` (body only), `CM6C_rail_l.stl`, `CM6C_rail_r.stl`.

Hardware unchanged: 4 M6 x 5 x 8 inserts, 4 M6 x 8 button heads, 4 rack screws.

## Changes from CM6A

| | CM6A | CM6C |
|---|---|---|
| Channel surface | baseline, 36° | x = 20.0 + 0.539 x distance from mid-height (0.38 clear of the modem wedge) |
| Wall at the channel tip | 3.9 | 3.2 |
| Insert/joint position | x22.6/231.4, z8.6/35.85 | x22.2/231.8, z5.6/38.85 |
| Rail lips | past x34 | end at x32 |
| Screw bays, Y20..54 | 12 tall, across the whole rail; on the right rail a hairline strip was left by mistake | head-sized notch, open at the outer side and the top or bottom face (head within 0.35 of it); both rails mirror exactly |
| Rail in the bays | web z14.6..29.85 only | web z11.6..32.85 plus a bar along the channel, 4.3 wide and 7.95 tall, flange to rail |

The faceplate pocket's nose taper is kept, plus 0.1 in the widened ends. Width across the rails stays 220.46.

## Checks run (digital only)

`python check_fit.py` from `src/`:
- All three STLs closed; 3MF has 25401 vertex and 50854 triangle tags.
- 0.38 clear of the modem wedge at every sampled plane, Y10 to Y130.
- Pilot wall to the nearest surface 1.63 (the outer side face); about 2.15 to the channel by calculation. Flange wall around the 6.6 hole 2.13.

## Still open

- Thinnest insert wall is 1.63 on the outer side: an installing insert may bulge there.
- Pocket rear rim stays about 41 tall against the modem's 44.5. This only clears if the modem's nose follows the pocket taper, which is not measured. If CM6C still stops short, look here first.
- Rail strength with open bays is UNKNOWN. CM6A rails that were spread may be damaged; reprint all three parts.

## Rebuild (PC)

From `src/` (uses CM6A's `src/orig/` baseline meshes, read only), OpenSCAD.exe on `cm1000_cm6c.scad` with `-D part="id_F"` (→ `id_F.stl`), `"rail_l"`, `"rail_r"` (→ `../CM6C_rail_*.stl`), then:
`"C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('faceplate_freecad.py').read())"`, then `python pack.py`.
