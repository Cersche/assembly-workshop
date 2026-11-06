# MRT-G MoCA rack tray (2026-11-06)

PROPOSED, UNPRINTED as a full tray. Fit, retention, heat and strength are UNKNOWN. Source: `work/moca-rack-tray/MRT.scad` (snapshot, `--backend=manifold`). Holds the ScreenBeam ECB7250 and the Bridgelink 2-way splitter in one 1U slot.

Print file: `MRT-G_7-parts-print-layout.3mf` (copy in `outputs/Final_3MF/MRT-G_moca_rack_tray_set.3mf`), 7 objects:

| Object | ID on part | Changed from MRT-F? | Print orientation |
|---|---|---|---|
| tray | MRT-G | yes | floor down |
| plate | MRT-E-P | no (byte-identical render) | front face down (x90) |
| cover_j | MRT-G-C1 | yes | flat, as modelled |
| cover_o | MRT-G-C2 | moved with the OUT2 bend | flat |
| cover_i | MRT-G-C3 | moved with the IN bend | flat |
| shoe_left / shoe_right | MRT-C-L / MRT-C-R | no | ear face down (x-90), chosen at this release |

## What changed (from Brian's MRT-T1 print, docs/Fit_Findings.md 2026-11-06)
- Straight coax at the splitter: the cable starts to curve 48 from the body face (crimp ends 33). Splitter moved +19.5 in X so the IN bend stays; OUT2 bend moved out; jumper channel walls start 48 from the body.
- Jumper off the ScreenBeam right-angle F: crimp ends 44 and the curve starts 58 behind the port centre line. The jumper bend moved back 19, and the splitter with it (OUT1 on Y 137).
- Floor carried back under the OUT2 bend to the rear bar. Right floor window moved forward between jumper and ScreenBeam (32 x 24). Tray ID moved clear of the IN bend.
- Coax lips (IN, OUT2, rear rib notches): 60 deg lead-in on top, 5.5 tall, so the cable cams in. The flat-top T1 lips took enough force to nearly damage the coax. Gap 6.8 and the 45 deg underside kept as printed. Rear rib 18 -> 22 tall to fit it.
- Jumper lips removed (Brian): the jumper hangs between two ports above the floor; the connectors and cover C1 hold it.

## Kept as printed or as before
Channel width 10, lip gap 6.8, bend R30, splitter riser 5.5 and M3 insert bosses, ScreenBeam foot pockets (hold well, Brian) and Velcro slots, cord lips, plate, hidden M6 joint, shoes, tray width (2.12 to each front post).

## Checks (release_report.md)
0 failed, 3 warnings: the cover countersinks read as a 4.15 bore; no insert there, harmless. Keep-out clear (M6 recesses, driver paths, shoe heads). 7 floor openings stay separate. No overlap with the real posts at U2, the ScreenBeam, splitter or cable mock-up (nearest cable gap 1.03 to the tray, 2.13 to C1). 3MF: 7 objects, 23493 vertex / 47460 triangle tags, all closed. The shoes' slotted M6 holes don't show in the round-hole scan.

## UNKNOWN
New lip lead-in: insertion force and hold. Jumper lengths (until installed). ScreenBeam coax port height 15.25 (not calipered). M3 cover screw length on hand, cover retention, M6 joint and inserts, shoe ramp seating, heat, strength. Rack slot not chosen (U2 and U4 free in the saved layout; checked at U2).

## Fit report to send back
ID on each part; fits or not; where tight or loose and by how much; how hard the coax goes past the new lips and whether it stays in; splitter and ScreenBeam seating; covers and screw length used; jumper lengths once installed; walls and infill.
