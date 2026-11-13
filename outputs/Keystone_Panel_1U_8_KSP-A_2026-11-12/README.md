# KSP-A: 1U keystone panel, 8 keystones, stiffened (2026-11-12)

Replaces the printed 10-keystone panel (`outputs/Faceplate_1U_10_Keystones_2026-10-22`), which Brian found too flimsy. ID **KSP-A** is engraved 0.6 mm deep on the rear face of the bottom frame bar, centre.

## What changed
- 8 keystones instead of 10 (Brian: only 8 needed), 27.5 mm pitch (X ±13.75, ±41.25, ±68.75, ±96.25). Webs between blocks grow from 0.5 to 6.5 mm.
- New 12 mm deep rear frame (Brian OK'd 12 mm) behind the plate, X ±110.1, full plate height, 1 mm rear chamfer, with one pocket per keystone (X ±9.9 around each block, Z = block window) so the space behind each jack stays open as before.

## Kept
- Plate 252 x 44.4 x 4, 2.5 mm corners, four-corner rack slots (44.4 standard).
- Golden keystone blocks, `ks_tight=0.2`, unchanged (from `lib/workshop.scad`).
- No screws or inserts: the panel mounts with the rack's own slot screws as before.

## Checks
`release_report.md`: 0 fails, 0 warnings. Real 4U posts placed at U7 (both sides): no overlap; the frame ends 1 mm short of the post flange edge (X 111.12, source value). The 8 pockets are separate.

## UNKNOWN
Printed fit of the frame against the posts, jack tilt-in clearance past the frame (frame starts at the block window edge, at least about 6 mm from a standard jack), stiffness and strength. Rendered with the pinned snapshot, now at `R:\Tools\OpenSCAD-snapshot\...`.

Print face down (front on the bed); the frame and engraving are then on top.
