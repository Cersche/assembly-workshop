# Fit findings log

One place for every printed-fit result, because prints are slow and fit tests end up spread across different parts and days.
Add a row for each printed piece (what was tight or loose, by how much, what changed). Specimen-specific: a result applies
to that part, material and printer only; fit stays UNKNOWN elsewhere.

## Pattern so far: sleeves are too tight top to bottom

Two different sleeves came out about **0.5 mm too tight in height**, with the sides fine. The app's default sleeve top
clearance is `sleeve_top = 0.3` mm (`equipment_tray.scad`, `SLEEVE_TOP_DEFAULT` in `equipment.py`).
Raising the default (e.g. to 0.8) is **not decided**; until then, set `sleeve_top: 0.8` on new sleeves.

| Date | Part | Result | Change |
| --- | --- | --- | --- |
| 2026-10-21 | OptiPlex sleeve SLV-A | ~0.5 mm too tight up/down, sides fine | Sleeve v2 redesign (task 36) |
| 2026-10-22 | TL-SG108E sleeve, first delivery (`2026-10-22_TL-SG108E`) | Too tight top to bottom | Hidden-screw version uses `sleeve_top: 0.8` (+0.5 mm), unprinted |
| 2026-10-23 | TL-SG108E (Brian printed; version not confirmed, hidden-screw build sets it 17 mm back) | Ports not flush with the rack front; rear retention needed | `2026-10-23_TL-SG108E_flush`: measured depth 100 mm, ports flush, rear stop, keyhole spring detents (0.6 mm bumps), `sleeve_top` 0.8, unprinted |

| 2026-10-23 | KD-D keyhole-detent coupon (3 mm bump, 3 mm floor) | Locks very nicely; arm sticks out the bottom when bent | KD-E + tray: 6.5 mm floor, arm over a pocket, unprinted |

## Other fit results (see HANDOFF.md for details)

| Date | Part | Result |
| --- | --- | --- |
| 2026-10-18 | Clearance v2 tray/faceplate (two-hole) | Fit good |
| 2026-10-19 | Golden keystone v5, `ks_tight=0.2` | Perfect; now the default |
| 2026-10-20 | FP44 plate-height coupons | Perfect; 44.4 mm/U is the standard |
| 2026-10-20 | SLV-A OptiPlex sleeve | Slid in, feet in pockets (later: 0.5 mm tight in height, above) |
| 2026-10-27 | MoCA box first print: sleeve rev A, cradle rev A | Sleeve had no porch screw slots (fixed in rev B). Cradle: ScreenBeam feet (13 mm, 2.25 proud) hold it off the plate; keystone-side pad hits the keystone, so the jumper is ~1 in short of Coax In (cradle rev B) |
| 2026-10-28 | CM1000 bracket: faceplate + rails v2 (screw access bays) | Fits (Brian) |
| 2026-10-28 | TL-SG108E `2026-10-23_TL-SG108E_flush` | Printed and tested; fit acceptable (Brian) |
| 2026-10-27 | MoCA porch15 + printed bezel nut | Fits, but nut too tall (above the rim), too thick and too tight; empty corner past the OUTs and closed modem side get in the way (porch rev 2, porch16.scad). Splitter calipered |

- 2026-10-28 TL-SG108E flush (2026-10-23 print): switch face ~1.3 mm proud of the faceplate; ~1 mm spare clearance above the switch in the opening (Brian: 1 mm is already forgiving). Fixed in SG8-M6-B.
