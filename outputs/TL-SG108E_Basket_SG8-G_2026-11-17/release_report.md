# SG8-G release report

- Date 2026-11-17; source `sg108e_basket.scad`; renderer `OpenSCAD-2026.11.01-x86-64` with Manifold
- posts 7:both: 4 real post meshes placed for slot U7

## Cuts cuts
- cuts cuts: 5 separate openings, none run together

## bracket
- bracket: closed solid, 1 body, 8286 triangles, volume 100528 mm3, size 252.00 x 106.38 x 44.40 mm
- bracket: ID SG8-G is on the mesh, 27.4 mm3 of text at X -32.1..-11.1, Y 5.5..10.5, Z 38.8..39.4; legibility not checked
- bracket: no round holes found by the scan
- bracket: no overlap with post_front_right_U7; nearest gap 0.00 mm
- bracket: no overlap with post_rear_right_U7; nearest gap over 10 mm
- bracket: no overlap with post_front_left_U7; nearest gap 0.00 mm
- bracket: no overlap with post_rear_left_U7; nearest gap over 10 mm

## inlay
- inlay: closed solid, 10 body, 1332 triangles, volume 29 mm3, size 36.72 x 0.60 x 3.39 mm
- inlay: ID UPLINK is on the mesh, 16.1 mm3 of text at X 69.2..87.0, Y -4.0..-3.4, Z 2.1..5.5; legibility not checked
- inlay: no round holes found by the scan
- inlay: no overlap with post_front_right_U7; nearest gap 6.18 mm
- inlay: no overlap with post_rear_right_U7; nearest gap over 10 mm
- inlay: no overlap with post_front_left_U7; nearest gap over 10 mm
- inlay: no overlap with post_rear_left_U7; nearest gap over 10 mm

## 3MF
- 3MF: 2 objects, 2 items, 4801 vertices, 9618 triangles, matching the STLs
- bracket: turned x90 for printing in the 3MF; its STL keeps the design position
- inlay: turned x90 for printing in the 3MF; its STL keeps the design position

## Source
- 1 source file(s) frozen in src/
- 1 library file(s) frozen in src/lib/; to re-render, set OPENSCADPATH to src/lib

## Result
- 0 failed, 0 warnings
- Digital checks only. The hole scan sees only fully surrounded round holes. Printed fit and strength: UNKNOWN.
