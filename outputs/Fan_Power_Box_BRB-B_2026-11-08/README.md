# Fan power box BRB-B (2026-11-08)

A two-piece box on the GuanTing 12 V 2 A brick (device card `docs/devices/guanting-12v-brick.md`). Replaces BRB-A, whose sleeve BRB-B-S printed too short in height to go on (width good). **Only change:** brick height now 87 (Brian's measurement; BRB-A used the supplier's 85) and 0.5 clearance per end, so the cavity is **88** tall (Brian). Box and lid grow 2.4 taller with it. Everything else is as in BRB-A, including the proven 0.3 width clearance. Source: `work/fan-junction-box/brick_box.scad` (frozen copy in `src/`). Design history: `work/fan-junction-box/Spec.md`.

Print file: `outputs/Final_3MF/BRB-B_fan_power_box_sleeve_box_lid.3mf` (same as `BRB-B_3-parts-print-layout.3mf`).

| Part | ID on part | Where | Print orientation in the 3MF |
| --- | --- | --- | --- |
| Sleeve (snaps onto the brick) | BRB-B-S | right side, reads along the height | lip/back side down |
| Junction box (Wagos + socket tip) | BRB-B-B | left side | floor (dovetail groove) down |
| Lid | BRB-B-L | outer face | outer face down |

## What it does
- The sleeve grips only the brick's flat faces: 45 wide, 30 from the main back face to the label face, with lips behind the main back running Z 18 to 67. Its curves get 4 mm extra room (`loose`). Clearance on the side flats is 0.3 (width fit good on BRB-A-S); in height 0.5 per end (cavity 88, unprinted). The cord boot exits through a slot in the bottom.
- The sleeve has zip-tie slot pairs centred on its left, right and top faces, for the ~25 x 85 cord bundle. The slots are 5 x 1.8, 10 apart and flush with the face. Each pair joins through a 1.4 deep groove on the inside, so the tie runs between a 1.0 bridge and the brick.
- The junction box holds 2x Wago 221-413 and the screw-terminal socket tip; the brick's barrel plug enters through its bottom end wall. Wire it first, then slide it down from the top onto the dovetail rail on the sleeve's front plate until it stops. Rail: 12 at the plate, 16 at its face, 2.5 tall. Groove clearance 0.25 per face.
- Lock: one M3 countersunk screw from inside the box, between the top lid bosses, into an M3 x 3 x 5 heat-set insert in the rail top (4.2 x 4 bore plus 3.2 tip clearance). M3 x 8 assumed.
- Lid: 4x M3 countersunk screws into M3 x 3 x 5 inserts in the box corners. The output cable notch is in the box's right wall.

## Hardware
- 5x M3 x 3 x 5 heat-set inserts: 4 in the box corners, 1 in the sleeve rail.
- 5x M3 countersunk screws: 4 for the lid (about M3 x 4–6), 1 lock screw (M3 x 8 assumed). Lengths on hand are UNKNOWN.

## Checks (release_report.md)
0 failed, 3 warnings, all kept on purpose:
- The sleeve's 3.2 x 2.5 hole is screw-tip clearance under the rail insert, not an M2.5 bore.
- The box's dia 4.23 and the lid's dia 4.25 are slices of the countersinks, not bores.

No overlap with the brick (sleeve nearest gap 0.30). Screw-head keep-outs are clear: the Wago back rib now has a gap in the middle for the lock screw head. Draft checks: sleeve/brick and sleeve/contents are empty; box/sleeve, box/contents and lid/box only touch faces.

## UNKNOWN
Sleeve fit and snap, grip, dovetail slide fit, zip-tie threading and bridge strength, insert fit, screw lengths, heat. The print orientations are suggestions. Digital checks only.
