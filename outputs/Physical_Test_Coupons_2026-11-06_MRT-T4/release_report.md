# MRT-T4 release report

- Date 2026-11-06; source `MRT.scad`; renderer `OpenSCAD-2026.11.01-x86-64` with Manifold

## jig
- jig: closed solid, 1 body, 15918 triangles, volume 91784 mm3, size 218.00 x 203.00 x 22.00 mm
- jig: ID MRT-T4 is on the mesh, 44.6 mm3 of text at X -10.0..19.5, Y 184.1..189.9, Z 1.4..2.0; legibility not checked
- jig: 2 x dia 16.01 (Z), depth about 2.5
- jig: 2 x dia 16.0 (Z), depth about 2.5
- jig: 12 x dia 4.2 (Z), depth about 4.0
- jig: 10 x dia 3.4 (Z), depth about 12.0
- jig: no overlap with dev_screenbeam.stl; nearest gap 0.25 mm
- jig: no overlap with dev_splitter.stl; nearest gap 2.00 mm
- jig: no overlap with dev_cables.stl; nearest gap 0.43 mm

## 3MF
- 3MF: 1 objects, 1 items, 7745 vertices, 15918 triangles, matching the STLs

## Source
- 1 source file(s) frozen in src/
- 1 library file(s) frozen in src/lib/; to re-render, set OPENSCADPATH to src/lib

## Result
- 0 failed, 0 warnings
- Digital checks only. The hole scan sees only fully surrounded round holes. Printed fit and strength: UNKNOWN.
