# TP-Link ER605 one-piece bracket — test-print ID ER6-G (2026-11-04)

PROPOSED — UNPRINTED. Current design. [ER6-F](../ER605_Bracket_ER6-F_2026-11-04/README.md) plus a keystone on each side of the plate (Brian). Everything else, including install, as ER6-F and [ER6-E](../ER605_Bracket_ER6-E_2026-11-04/README.md). Router fit, flushness, detent click, rack fit and strength are UNKNOWN.

`ER6-G_ER605_bracket.3mf`, also in `outputs/Final_3MF/`: one object, front face on the bed, no supports. 252 x 44.4 x 106.08 mm, 101.7 cm3 solid volume.

## Keystones

Golden block, copied unchanged from SG8-M6-F's source, `ks_tight` 0.2 (printed a perfect fit, now the default). Source: Goul, "10 inch shelf TP-Link SG108 Plus Keystone" (MakerWorld, BY-NC-SA). Centres X ±99, block 21 wide (X 88.5..109.5), Z 7.225..40.725.

- 0.65 clear of the root chamfer on the inside, 3.76 clear of the rack slot on the outside. The block's outer edge is 1.6 inside the post's front flange (X 111.1, recorded number; not re-run against the post mesh).
- Mesh points of each opening lie on the SG8-M6-F opening (0.000 mm at a cut through the plate).
- Block front is 0.08 proud of the plate, as on the source and SG8-M6-F. So the block touches the bed first and the plate front starts 0.08 up.
- The block's own hook faces are past 45° (about 53 mm2 each), same as SG8-M6-F's; that block has printed fine face-down.
- Keystone jacks and cables are not modelled.

ID moved from the plate back to the collar top, because the keystones took its place. Its letters are 0.6 deep and hold the only other overhang, tiny.

## Checks (digital only)

`python src/pack_check.py . <SG8-M6-F_faceplate.stl> <source.stl>`: closed mesh; case box 25.98 tall with Ø8 holes, front at the plate front: clear; path from the front: clear apart from the bumps; plate matches SG8-M6-F within 0.12 mm; 3MF plain tags 2660 vertex / 5424 triangle. (The script's overhang total now counts the plate front, 0.08 off the bed; ignore it for this part.)
