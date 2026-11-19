# TL-SG108E one-piece basket: test-print ID SG8-H (2026-11-19)

RELEASED FOR PRINTING, UNPRINTED. [SG8-G](../TL-SG108E_Basket_SG8-G_2026-11-17/README.md) plus a full-width flat rear stop lip. SG8-G printed (Brian, 2026-11-19): the switch was easily pushed back and shifted about 3 mm. Likely cause: its only rear stop was ER6-H's two 45° corner wedges, which the switch's rounded rear corners ride up. Fit, click and strength UNKNOWN.

| File | What |
|---|---|
| `SG8-H_bracket+labels.3mf` | **Print this.** One object, two parts: bracket + UPLINK/WLAN inlay seated in its engraving (give the inlay a second colour), front face on the bed. Built by `src/pack_3mf.py`; checked: inlay inside the recess, no overlap. Also `Q:\Projects\assembly-workshop\outputs\Final_3MF\SG8-H_TL-SG108E_basket.3mf` |
| `SG8-H_2-parts-print-layout.3mf` | Release script layout, parts side by side, inlay NOT in its recess. Don't use for two-colour printing |
| `SG8-H_bracket.stl`, `SG8-H_inlay.stl` | Rack position (X centred, plate back Y 0, Z 0 slot bottom) |
| `release_report.md` | `tools/release_part.py`: 0 fails, 0 warnings (posts U7 both sides, 5 floor openings, inlay 10 letter bodies) |
| `src/` | `sg108e_basket.scad` + frozen `lib/workshop.scad`; OPENSCADPATH=src/lib |

## Changed from SG8-G
- **Rear stop lip:** flat, full pocket width (159), 3 tall above the floor, Y 97.3..102.3. Its front face is the proven SG8-M6-D/F stop position (ports flush). 3 tall so it prints as a small overhang with the part face down. Corner wedges kept.
- ID SG8-H on the collar top.

## Kept from SG8-G (everything else)
Pocket 159 x 26.35 (side play 0.5, top 1.35), switch centre X −21.5, KD-E detents at ±55 / 48.5, keystones X +78 / +99 (golden), UPLINK / WLAN labels 3.5, floor slots, body. 102.8 cm3.

## Checks (digital only)
Switch seated with its face flush: clear except the bump zones; path above the bumps: clear; switch 0.3 further back: hits the lip. Posts clear. Not sliced.

## Fit report to send back
ID (SG8-H); does the switch still go in fully and click; rear play now (mm); ports flush, proud or sunk; keystones; rack fit; walls and infill.
