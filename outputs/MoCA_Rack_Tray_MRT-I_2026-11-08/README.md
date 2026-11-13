# MRT-I MoCA rack tray (2026-11-08)

PROPOSED, released for printing at Brian's direction. Fit, retention and strength are UNKNOWN.

- **Source:** `work/moca-rack-tray/MRT.scad`. A copy is in `src/` and the library is in `src/lib/`.
- **Print file:** `outputs/Final_3MF/MRT-I_moca_tray_sled_covers_washers.3mf`. It has 5 objects, the same as this folder's `MRT-I_5-parts-print-layout.3mf`.
- **Check:** `release_report.md` shows 0 failed and 4 warnings. The warnings are the 3.4/4.15/4.25 screw-clearance and countersink holes sitting near the 4.2 insert bore, the same kind MRT-H had.
  - Posts at U2 are clear, and the ScreenBeam, splitter and cables are clear.
  - The 0.00 gaps are devices resting on the floor and on the sled.
  - All 24 cuts are separate: 17 vent slots plus the 7 earlier openings.

## Print new
| ID | Part | Print |
| --- | --- | --- |
| MRT-I | tray | floor down; turn slicer supports off, the strap-groove combs are modelled (3 bodies) |
| MRT-I-C2 | OUT2 channel cover | flat |
| MRT-I-C3 | IN channel cover | flat |
| MRT-I-S | splitter sled | flat, plate down |
| IW (x2) | sled clamp washers | flat |

## Reuse from MRT-H (unchanged, no reprint)
- **Faceplate:** MRT-E-P.
- **Jumper cover:** MRT-H-C1.
- **Rear shoes:** MRT-C-L / MRT-C-R, with the MRT-H wall tips. They work well (Brian, 2026-11-07).
- **Ramps:** MRT-H-RIU/RID/ROU/ROD.

## What changed from MRT-H (Brian's MRT-H print report, `docs/Fit_Findings.md`)
- **Splitter mount:**
  - The splitter, with its riser, bosses and inserts, moved 4 to the rear, away from the ScreenBeam.
  - The ear bosses stand 7 above the riser (12.5 above the floor), because the real ears sit 7 above the case's resting face. The inserts are at the new top.
- **IN channel:** moved 9 to the rear.
- **OUT2 channel:** moved 6.75 to the rear. The ramp stays in place, which leaves 8.25 of straight before it.
- **Jumper channel:** unchanged.
- **Lips:** dropped from every channel and the rear rib, because the covers hold the cables. Covers C2/C3 follow the moved channels.
- **Splitter sled MRT-I-S:** a 5.5 plate in the riser's place carries the ear bosses and their M3 inserts.
  - It locks to the tray with 2 M3 countersunk screws through the IW washers, into M3 x 3 x 5 inserts flush in the floor.
  - The lock holes are 11 across, so the sled adjusts about ±4 in any direction, and turns a little, to meet the real ears.
- **Zip-tie fallback:** moved onto the sled. It has a 2-wide slot down each side of the body and 3 grooves underneath.
- **Ground screw:** an 8-long block at the front, OUT half, next to the front ear. Its head, ring terminal and driver path are kept clear. No ground-lead route is needed (Brian).
- **Vents:** two floor fields of 4-wide slots on a 7 pitch, running front to back, because the tray sits low in the rack.
  - Left field: 10 slots.
  - Right field: 7 slots.

## Kept as printed
These are the proven MRT-H values:
- Channel width 10, walls 3 with fillets and gussets, and bend radii.
- Dock cheeks and inserts.
- ScreenBeam cradle and feet pockets.
- Strap grooves and combs.
- Rounded bed corners.
- Tray 218 wide (2.12 a side to the posts).
- Rear shoes and wall tips.

## Hardware
- **M3 x 3 x 5 inserts, 4.2 bore:**
  - 2 in the sled bosses.
  - 2 in the floor for the sled locks.
  - The covers and docks as in MRT-H.
- **Sled lock screws:** 2 M3 countersunk. The stack is washer 2.5 + sled 5.5 + insert, so M3 x 10 is the likely length; UNKNOWN until fitted.
- **Splitter ears:** 2 M3 screws into the sled bosses.

## UNKNOWN
- Fit and strength.
- Whether the sled clamp holds without creep.
- Stiffness of the 12.5-tall bosses.
- Ground screw head size (7 x 3 assumed).
- Lock screw length.
- Comb removal force.

## Fit report to send back
- ID on each part (MRT-I, MRT-I-C2, MRT-I-C3, MRT-I-S, IW).
- **Splitter:** do the ears line up with the sled bosses after adjusting? Does the sled lock firmly? What screw length did you use?
- **Channels:** does the IN coax drop into its channel without a fight? Same for OUT2. Do the ramps still meet them?
- **Covers C2/C3:** do they seat on their pillars?
- **Ground:** is the ground screw reachable with the ring terminal on?
- **Fit:** fits or not; where it's tight or loose, and by how much if measured.
- **Print settings:** walls and infill.
