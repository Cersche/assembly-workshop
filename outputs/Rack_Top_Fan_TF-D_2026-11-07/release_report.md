# TF-D release report

- Date 2026-11-07; source `rack_top_fan.scad`; renderer `OpenSCAD-2026.11.01-x86-64` with Manifold

## Keep-out
- keep-out keepout: 8993 mm3, 16 bodies

## Cuts cuts
- cuts cuts: 40 separate openings, none run together

## edge_front
- edge_front: closed solid, 1 body, 4612 triangles, volume 350304 mm3, size 282.24 x 54.85 x 69.85 mm
- edge_front: ID TFE-D is on the mesh, 6.0 mm3 of text at X 113.1..125.0, Y 34.4..35.0, Z 433.6..436.4; legibility not checked
- edge_front: 4 x dia 10.8 (X), depth about 2.0
- edge_front: 4 x dia 6.4 (X), depth about 4.75
- edge_front: 4 x dia 4.2 (Z), depth about 4.0 to 5.0
- edge_front: 2 x dia 3.4 (Z), depth about 4.0
- edge_front: keep-out clear

## edge_rear
- edge_rear: closed solid, 1 body, 4920 triangles, volume 347953 mm3, size 282.24 x 54.85 x 69.85 mm
- edge_rear: ID TRE-D is on the mesh, 6.5 mm3 of text at X -125.3..-112.8, Y 205.0..205.6, Z 433.6..436.4; legibility not checked
- edge_rear: 4 x dia 10.8 (X), depth about 2.0
- edge_rear: 4 x dia 6.4 (X), depth about 4.75
- edge_rear: 4 x dia 4.2 (Z), depth about 4.0 to 5.0
- edge_rear: 2 x dia 3.4 (Z), depth about 4.0
- edge_rear: keep-out clear

## rail
- rail: closed solid, 1 body, 3248 triangles, volume 228030 mm3, size 30.00 x 170.00 x 50.00 mm
- rail: ID TSR-B is on the mesh, 11.7 mm3 of text at X 111.0..111.6, Y 112.0..128.2, Z 433.0..437.0; legibility not checked
- rail: 4 x dia 7.6 (X/Z), depth about 5.25 to 10.0
- WARN: rail: 2 M6 insert bore(s) dia 7.6 look shallower than 6.0 mm (about 5.25); confirm this is not a bore
- rail: keep-out clear

## grille
- grille: closed solid, 1 body, 7300 triangles, volume 65151 mm3, size 220.96 x 205.40 x 3.00 mm
- grille: ID TFG-B is on the mesh, 11.1 mm3 of text at X 61.8..78.0, Y 24.0..28.0, Z 447.0..447.6; legibility not checked
- grille: 4 x dia 7.5 (Z), depth about 3.0
- WARN: grille: dia 7.5 is close to the M6 insert bore 7.6 but not on it
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

## 3MF
- 3MF: 4 objects, 4 items, 9944 vertices, 20080 triangles, matching the STLs
- edge_front: turned x90 for printing in the 3MF; its STL keeps the design position
- edge_rear: turned x-90 for printing in the 3MF; its STL keeps the design position
- rail: turned y90 for printing in the 3MF; its STL keeps the design position

## Source
- 1 source file(s) frozen in src/
- 33 library file(s) frozen in src/lib/; to re-render, set OPENSCADPATH to src/lib

## Result
- 0 failed, 3 warnings
- Digital checks only. The hole scan sees only fully surrounded round holes. Printed fit and strength: UNKNOWN.
