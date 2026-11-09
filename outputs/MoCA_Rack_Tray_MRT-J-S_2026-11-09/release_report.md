# MRT-J-S release report

- Date 2026-11-09; source `MRT.scad`; renderer `OpenSCAD-2026.11.01-x86-64` with Manifold
- posts 2:both: 4 real post meshes placed for slot U2

## Keep-out
- keep-out keepout: 14898 mm3, 11 bodies

## sled
- sled: closed solid, 1 body, 5076 triangles, volume 13393 mm3, size 39.49 x 92.36 x 12.50 mm
- sled: ID MRT-J-S is on the mesh, 16.2 mm3 of text at X -4.9..14.0, Y 156.3..159.7, Z 8.9..9.5; legibility not checked
- sled: 1 x dia 11.09 (Z), depth about 5.5
- sled: 1 x dia 11.0 (Z), depth about 5.5
- sled: 2 x dia 4.2 (Z), depth about 4.0
- sled: no overlap with dev_screenbeam.stl; nearest gap over 10 mm
- sled: no overlap with dev_splitter.stl; nearest gap 0.00 mm
- sled: no overlap with dev_cables.stl; nearest gap 6.73 mm
- sled: no overlap with post_front_right_U2; nearest gap over 10 mm
- sled: no overlap with post_rear_right_U2; nearest gap over 10 mm
- sled: no overlap with post_front_left_U2; nearest gap over 10 mm
- sled: no overlap with post_rear_left_U2; nearest gap over 10 mm
- sled: keep-out clear

## 3MF
- 3MF: 1 objects, 1 items, 2532 vertices, 5076 triangles, matching the STLs

## Source
- 1 source file(s) frozen in src/
- 1 library file(s) frozen in src/lib/; to re-render, set OPENSCADPATH to src/lib

## Result
- 0 failed, 0 warnings
- Digital checks only. The hole scan sees only fully surrounded round holes. Printed fit and strength: UNKNOWN.
