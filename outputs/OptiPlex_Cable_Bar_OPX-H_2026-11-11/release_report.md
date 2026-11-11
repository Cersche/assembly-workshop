# OPX-H release report

- Date 2026-11-11; source `OPX-H.scad`; renderer `OpenSCAD-2026.11.01-x86-64` with Manifold
- posts 1:both: 4 real post meshes placed for slot U1

## Keep-out
- keep-out keepout: 5995 mm3, 6 bodies

## Cuts cuts
- cuts cuts: 34 separate openings, none run together

## rear_left
- rear_left: closed solid, 1 body, 3092 triangles, volume 30557 mm3, size 46.25 x 113.30 x 44.40 mm
- rear_left: ID OPX-H-L is on the mesh, 15.3 mm3 of text at X -107.7..-91.8, Y 193.2..244.0, Z 7.2..37.0; legibility not checked
- rear_left: 1 x dia 3.2 (X), depth about 1.5
- WARN: rear_left: 1 M2.5 insert bore(s) dia 3.2 look shallower than 5.0 mm (about 1.5); confirm this is not a bore
- rear_left: no overlap with ref_pc.stl; nearest gap 0.20 mm
- rear_left: no overlap with post_front_right_U1; nearest gap over 10 mm
- rear_left: no overlap with post_rear_right_U1; nearest gap over 10 mm
- rear_left: no overlap with post_front_left_U1; nearest gap over 10 mm
- rear_left: no overlap with post_rear_left_U1; nearest gap 0.00 mm
- rear_left: keep-out clear

## rear_right
- rear_right: closed solid, 1 body, 3308 triangles, volume 30555 mm3, size 46.25 x 113.30 x 44.40 mm
- rear_right: ID OPX-H-R is on the mesh, 17.0 mm3 of text at X 91.8..107.7, Y 192.9..244.0, Z 7.2..36.8; legibility not checked
- rear_right: 1 x dia 3.2 (X), depth about 1.5
- WARN: rear_right: 1 M2.5 insert bore(s) dia 3.2 look shallower than 5.0 mm (about 1.5); confirm this is not a bore
- rear_right: no overlap with ref_pc.stl; nearest gap 0.20 mm
- rear_right: no overlap with post_front_right_U1; nearest gap over 10 mm
- rear_right: no overlap with post_rear_right_U1; nearest gap 0.00 mm
- rear_right: no overlap with post_front_left_U1; nearest gap over 10 mm
- rear_right: no overlap with post_rear_left_U1; nearest gap over 10 mm
- rear_right: keep-out clear

## bar
- bar: closed solid, 1 body, 6048 triangles, volume 28588 mm3, size 182.90 x 32.30 x 26.37 mm
- bar: ID OPX-H-BAR is on the mesh, 17.5 mm3 of text at X -87.2..80.2, Y 215.2..238.9, Z 12.4..30.0; legibility not checked
- bar: no round holes found by the scan
- bar: no overlap with ref_pc.stl; nearest gap over 10 mm
- bar: no overlap with post_front_right_U1; nearest gap over 10 mm
- bar: no overlap with post_rear_right_U1; nearest gap over 10 mm
- bar: no overlap with post_front_left_U1; nearest gap over 10 mm
- bar: no overlap with post_rear_left_U1; nearest gap over 10 mm
- bar: keep-out clear

## 3MF
- 3MF: 3 objects, 3 items, 6134 vertices, 12448 triangles, matching the STLs
- rear_left: turned x270 for printing in the 3MF; its STL keeps the design position
- rear_right: turned x270 for printing in the 3MF; its STL keeps the design position

## Source
- 1 source file(s) frozen in src/

## Result
- 0 failed, 2 warnings
- Digital checks only. The hole scan sees only fully surrounded round holes. Printed fit and strength: UNKNOWN.
