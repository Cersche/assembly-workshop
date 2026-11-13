# KSP-B release report

- Date 2026-11-12; source `keystone_panel.scad`; renderer `OpenSCAD-2026.11.01-x86-64` with Manifold
- posts 7:both: 4 real post meshes placed for slot U7

## Cuts cuts
- cuts cuts: 8 separate openings, none run together

## panel
- panel: closed solid, 1 body, 10768 triangles, volume 98082 mm3, size 252.00 x 16.08 x 44.40 mm
- panel: ID KSP-B is on the mesh, 9.9 mm3 of text at X -31.4..51.2, Y -0.0..12.0, Z 7.3..42.5; legibility not checked
- panel: 1 x dia 4.4 (Y), depth about 0.75
- panel: 2 x dia 2.36 (Y), depth about 0.25
- panel: no overlap with post_front_right_U7; nearest gap 0.00 mm
- panel: no overlap with post_rear_right_U7; nearest gap over 10 mm
- panel: no overlap with post_front_left_U7; nearest gap 0.00 mm
- panel: no overlap with post_rear_left_U7; nearest gap over 10 mm

## 3MF
- 3MF: 1 objects, 1 items, 5350 vertices, 10768 triangles, matching the STLs

## Source
- 1 source file(s) frozen in src/
- 1 library file(s) frozen in src/lib/; to re-render, set OPENSCADPATH to src/lib

## Result
- 0 failed, 0 warnings
- Digital checks only. The hole scan sees only fully surrounded round holes. Printed fit and strength: UNKNOWN.
