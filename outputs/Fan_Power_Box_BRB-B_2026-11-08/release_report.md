# BRB-B release report

- Date 2026-11-08; source `brick_box.scad`; renderer `OpenSCAD-2026.11.01-x86-64` with Manifold

## Keep-out
- keep-out keepout: 1822 mm3, 5 bodies

## sleeve
- sleeve: closed solid, 1 body, 4794 triangles, volume 37747 mm3, size 50.40 x 37.50 x 92.80 mm
- sleeve: ID BRB-B-S is on the mesh, 25.2 mm3 of text at X -25.2..25.2, Y 5.9..27.5, Z 5.9..87.5; legibility not checked
- sleeve: 1 x dia 5.31 (X), depth about 0.25
- sleeve: 1 x dia 4.2 (Y), depth about 4.0
- sleeve: 1 x dia 3.2 (Y), depth about 2.5
- WARN: sleeve: 1 M2.5 insert bore(s) dia 3.2 look shallower than 5.0 mm (about 2.5); confirm this is not a bore
- sleeve: 1 x dia 1.56 (X), depth about 0.25
- sleeve: keep-out clear

## box
- box: closed solid, 1 body, 4992 triangles, volume 28488 mm3, size 50.40 x 18.00 x 92.80 mm
- box: ID BRB-B-B is on the mesh, 26.2 mm3 of text at X -25.2..20.5, Y 43.0..57.0, Z 32.0..78.6; legibility not checked
- box: 1 x dia 9.6 (Z), depth about 3.0
- box: 1 x dia 6.73 (Y), depth about 0.25
- box: 1 x dia 6.23 (Y), depth about 0.25
- box: 1 x dia 5.73 (Y), depth about 0.25
- box: 1 x dia 5.23 (Y), depth about 0.25
- box: 1 x dia 4.73 (Y), depth about 0.25
- box: 1 x dia 4.23 (Y), depth about 0.25
- WARN: box: dia 4.23 is close to the M3 insert bore 4.2 but not on it
- box: 4 x dia 4.2 (Y), depth about 4.0
- box: 1 x dia 3.73 (Y), depth about 0.25
- box: 1 x dia 3.4 (Y), depth about 0.75
- box: keep-out clear

## lid
- lid: closed solid, 1 body, 3036 triangles, volume 10958 mm3, size 50.40 x 2.40 x 92.80 mm
- lid: ID BRB-B-L is on the mesh, 23.7 mm3 of text at X -11.4..11.2, Y 58.8..59.3, Z 41.6..45.4; legibility not checked
- lid: 4 x dia 6.73 (Y), depth about 0.25
- lid: 4 x dia 6.24 (Y), depth about 0.25
- lid: 4 x dia 5.74 (Y), depth about 0.25
- lid: 4 x dia 5.24 (Y), depth about 0.25
- lid: 4 x dia 4.74 (Y), depth about 0.25
- lid: 4 x dia 4.25 (Y), depth about 0.25
- WARN: lid: dia 4.25 is close to the M3 insert bore 4.2 but not on it
- lid: 4 x dia 3.75 (Y), depth about 0.25
- lid: 4 x dia 3.4 (Y), depth about 0.75
- lid: 1 x dia 1.56 (Y), depth about 0.25
- lid: keep-out clear

## 3MF
- 3MF: 3 objects, 3 items, 6387 vertices, 12822 triangles, matching the STLs
- sleeve: turned x90 for printing in the 3MF; its STL keeps the design position
- box: turned x90 for printing in the 3MF; its STL keeps the design position
- lid: turned x-90 for printing in the 3MF; its STL keeps the design position

## Source
- 1 source file(s) frozen in src/
- 1 library file(s) frozen in src/lib/; to re-render, set OPENSCADPATH to src/lib

## Result
- 0 failed, 3 warnings
- Digital checks only. The hole scan sees only fully surrounded round holes. Printed fit and strength: UNKNOWN.
