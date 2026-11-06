# MRT-H MoCA rack tray (2026-11-06)

PROPOSED, released for printing on Brian's direction. Fit, retention and strength are UNKNOWN. Source: `work/moca-rack-tray/MRT.scad` (copy in `src/`, library in `src/lib/`). Print file with everything, including the forming jigs: `outputs/Final_3MF/MRT-H_moca_tray_ramps_and_T5-T7_jigs.3mf` (14 objects). This folder's `MRT-H_11-parts-print-layout.3mf` holds just these 11 parts.

## Parts
| ID | Part | Print |
| --- | --- | --- |
| MRT-H | tray | floor down |
| MRT-E-P | faceplate, unchanged | front face down |
| MRT-C-L / MRT-C-R | rear shoes, unchanged | ear face down |
| MRT-H-C1 / C2 / C3 | channel covers (jumper, OUT2, IN) | flat |
| MRT-H-RIU / RID | IN ramp, up / down | on its side; needs support under the upper side wall and ear |
| MRT-H-ROU / ROD | OUT2 ramp, up / down | on its side; needs support under the upper side wall and ear |

Print only the ramp you'll use at each entrance (or both, to swap later).

## What changed from MRT-G (Brian's MRT-T4 report)
- Channel walls are 3 thick instead of 2. They grow outward, so the channel (10), lip gap (6.8), 60° lead-ins and all bend positions stay as printed on MRT-T4.
- Each wall has a 4 mm 45° fillet along its outside base, and the three bends each have 3 gussets. The cord/IN wall stays 2.
- Covers grow 1 mm a side and their pillars move out with the walls.
- Each rear coax entrance has a dock: the floor plus a 9-wide cheek with 2 M3 x 3 x 5 inserts (4.2 bore, 4 deep).
- A screw-on Up or Down ramp (R30) turns the coax vertical. Each ramp has cable-tie slot pairs at its entrance, middle and exit, and is held by 2 M3 countersunk screws.
  - Up stays inside its own 1U.
  - Down reaches about 22 below the slot, into the rear of the U below.
- Rear keystones were tried and dropped.

- Floor carried out under the splitter's rear ear boss, which sat half past the floor end since MRT-G (Brian, slicer, before printing).
- Floor outline rounded everywhere on the bed (outside corners r 3, inside corners filleted r 3; the front edge on the plate stays square), and the dock cheeks have r 2 corners, against warping (Brian).

Kept as printed: every MRT-G fit value (ScreenBeam pockets, splitter riser and bores, 48 straight at the splitter, 58 behind the right-angle F, lips, rib, M6 joint, shoes).

## Checks
0 failed, 10 warnings:
- 9 are countersinks the hole scan reads as bores.
- 1 tray insert bore reads 4.25; it is the same library bore as the other eleven.

Everything else:
- Posts at U2: clear.
- Keep-out: clear.
- Seven separate floor openings.
- No overlap with the ScreenBeam, splitter or cable mock-ups; the nearest cable gap is 0.42.
- Each ramp is 1.5 clear of its own coax path.

## UNKNOWN
- Lip insertion force.
- Whether there is room at the rear of the U above or below for the vertical runs.
- OUT2 has only 15 mm between its plan bend and its vertical bend.
- How hard the coax pushes on the ramps.
- M3 screw length.
- Jumper lengths.
- Fit and strength.

## Fit report to send back
- The ID on each part.
- Tray, plate and shoes: fit on the rack.
- Coax: in the thicker channels, and whether the walls still flex.
- Ramps: screw-on fit, whether the coax turns without fighting, which tie slots you used.
- Covers.
- Screw length used.
- Walls and infill.
