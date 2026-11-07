# TF-A release report

- Date 2026-11-06; source `rack_top_fan.scad`; renderer `OpenSCAD-2026.11.01-x86-64` with Manifold

## Keep-out
- keep-out keepout: 1524 mm3, 4 bodies

## Cuts cuts
- cuts cuts: 36 separate openings, none run together

## edge_front
- edge_front: closed solid, 1 body, 1980 triangles, volume 320661 mm3, size 282.24 x 54.85 x 69.85 mm
- edge_front: ID TFE-A is on the mesh, 5.7 mm3 of text at X 113.0..124.9, Y 34.4..35.0, Z 433.6..436.4; legibility not checked
- edge_front: 4 x dia 6.4 (X), depth about 6.75
- edge_front: 2 x dia 4.2 (Z), depth about 5.0
- edge_front: keep-out clear

## edge_rear
- edge_rear: closed solid, 1 body, 2550 triangles, volume 317738 mm3, size 282.24 x 54.85 x 69.85 mm
- edge_rear: ID TRE-A is on the mesh, 6.2 mm3 of text at X -125.2..-112.8, Y 205.0..205.6, Z 433.6..436.4; legibility not checked
- edge_rear: 1 x dia 8.0 (Y), depth about 3.0
- edge_rear: 4 x dia 6.4 (X), depth about 6.75
- edge_rear: 2 x dia 4.2 (Z), depth about 5.0
- edge_rear: keep-out clear

## rail
- rail: closed solid, 1 body, 3354 triangles, volume 242367 mm3, size 30.00 x 170.00 x 50.00 mm
- rail: ID TSR-A is on the mesh, 10.9 mm3 of text at X 111.0..111.6, Y 111.7..128.2, Z 433.0..437.0; legibility not checked
- rail: 2 x dia 7.6 (Z), depth about 10.0
- rail: 4 x dia 6.4 (X), depth about 6.75 to 16.0
- rail: keep-out clear

## grille
- grille: closed solid, 1 body, 5842 triangles, volume 65681 mm3, size 220.96 x 205.40 x 3.00 mm
- grille: ID TFG-A is on the mesh, 10.3 mm3 of text at X 61.8..78.3, Y 24.0..28.0, Z 447.0..447.6; legibility not checked
- grille: 4 x dia 6.73 (Z), depth about 0.25
- grille: 4 x dia 6.23 (Z), depth about 0.25
- grille: 4 x dia 5.73 (Z), depth about 0.25
- grille: 4 x dia 5.23 (Z), depth about 0.25
- grille: 4 x dia 4.73 (Z), depth about 0.25
- grille: 4 x dia 4.23 (Z), depth about 0.25
- WARN: grille: dia 4.23 is close to the M3 insert bore 4.2 but not on it
- grille: 4 x dia 3.73 (Z), depth about 0.25
- grille: 4 x dia 3.4 (Z), depth about 1.25
- grille: keep-out clear

## coupon
- coupon: closed solid, 1 body, 1050 triangles, volume 71148 mm3, size 40.12 x 54.85 x 69.85 mm
- coupon: ID TFE-T1 is on the mesh, 6.3 mm3 of text at X 113.1..127.0, Y 34.4..35.0, Z 433.6..436.4; legibility not checked
- coupon: 2 x dia 6.4 (X), depth about 7.0
- coupon: 1 x dia 4.2 (Z), depth about 5.0
- coupon: keep-out clear

## rail_coupon
- rail_coupon: closed solid, 1 body, 2506 triangles, volume 54580 mm3, size 30.00 x 40.00 x 50.00 mm
- rail_coupon: ID TSR-T1 is on the mesh, 6.7 mm3 of text at X 111.0..111.6, Y 47.9..62.2, Z 433.5..436.5; legibility not checked
- rail_coupon: 1 x dia 7.6 (Z), depth about 10.0
- rail_coupon: 2 x dia 6.4 (X), depth about 6.75 to 16.0
- rail_coupon: keep-out clear

## 3MF
- 3MF: 6 objects, 6 items, 8547 vertices, 17282 triangles, matching the STLs
- edge_front: turned x90 for printing in the 3MF; its STL keeps the design position
- edge_rear: turned x-90 for printing in the 3MF; its STL keeps the design position
- rail: turned y90 for printing in the 3MF; its STL keeps the design position
- coupon: turned x90 for printing in the 3MF; its STL keeps the design position
- rail_coupon: turned y90 for printing in the 3MF; its STL keeps the design position

## Source
- 1 source file(s) frozen in src/
- 33 library file(s) frozen in src/lib/; to re-render, set OPENSCADPATH to src/lib

## Result
- 0 failed, 1 warnings
- Digital checks only. The hole scan sees only fully surrounded round holes. Printed fit and strength: UNKNOWN.
