# TF-B release report

- Date 2026-11-06; source `rack_top_fan.scad`; renderer `OpenSCAD-2026.11.01-x86-64` with Manifold

## Keep-out
- keep-out keepout: 1524 mm3, 4 bodies

## edge_front
- edge_front: closed solid, 1 body, 2396 triangles, volume 346198 mm3, size 282.24 x 54.85 x 69.85 mm
- edge_front: ID TFE-B is on the mesh, 6.1 mm3 of text at X 113.2..124.9, Y 34.4..35.0, Z 433.6..436.4; legibility not checked
- edge_front: 4 x dia 6.4 (X), depth about 6.75
- edge_front: 2 x dia 4.2 (Z), depth about 5.0
- edge_front: keep-out clear

## edge_rear
- edge_rear: closed solid, 1 body, 2966 triangles, volume 342855 mm3, size 282.24 x 54.85 x 69.85 mm
- edge_rear: ID TRE-B is on the mesh, 6.7 mm3 of text at X -125.2..-113.0, Y 205.0..205.6, Z 433.6..436.4; legibility not checked
- edge_rear: 1 x dia 8.0 (Y), depth about 3.0
- edge_rear: 4 x dia 6.4 (X), depth about 6.75
- edge_rear: 2 x dia 4.2 (Z), depth about 5.0
- edge_rear: keep-out clear

## 3MF
- 3MF: 2 objects, 2 items, 2667 vertices, 5362 triangles, matching the STLs
- edge_front: turned x90 for printing in the 3MF; its STL keeps the design position
- edge_rear: turned x-90 for printing in the 3MF; its STL keeps the design position

## Source
- 1 source file(s) frozen in src/
- 33 library file(s) frozen in src/lib/; to re-render, set OPENSCADPATH to src/lib

## Result
- 0 failed, 0 warnings
- Digital checks only. The hole scan sees only fully surrounded round holes. Printed fit and strength: UNKNOWN.
