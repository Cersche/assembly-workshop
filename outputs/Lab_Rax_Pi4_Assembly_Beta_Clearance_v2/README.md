# Pi4 tray clearance revision 2

All four gusset crests are 1 mm lower than the previous gusset-fix revision. No other design dimensions were changed. The faceplate, alignment pockets, screw bores, mounting-hole pattern, PCB height and tray envelope are unchanged.

Validation:
- OpenSCAD exported simple tray and faceplate solids. Every STL edge is shared by two triangles.
- The previously clashing USB connected solid clears the right inner gusset even after shifting that USB solid down 0.5 mm. This checks 0.5 mm vertical clearance at that feature, not a global minimum Euclidean distance.
- Direct triangle clipping of the complete Pi mesh against all four gussets finds no intersection after lowering the Pi 0.5 mm. The ear envelopes and the 48-sided standoff envelopes also have no triangle intersection, excluding intentional PCB contact by 0.001 mm. The floor and socket rails are separated from the Pi by their coordinate bounds.
- The whole-Pi CGAL solid check was inconclusive because the imported Pi has non-manifold edges; its empty output is not counted as a pass. The targeted USB solid check and direct triangle checks above provide the clearance evidence.
- The nominal PCB and the tray/faceplate solid-interference checks also pass, excluding their intentional contact surfaces by 0.001 mm.

Fit geometry retained: PCB hole pattern 58 x 49 mm; two tongue pockets with 0.15 mm nominal side/vertical clearance per side and 0.2 mm tip clearance; joint screw axes at X=+/-40, Z=21 along Y; 0.3 mm gap from plate bosses to tray ears. Tray floor and faceplate are perpendicular in model space.

Files:
- tray.stl: updated tray.
- faceplate.stl: unchanged matching faceplate.
- pi4_assembly.scad: editable source for this revision.
- assembly_review.3mf: tray and faceplate at assembled coordinates, geometry only.
- Pi4_fit_REFERENCE_ONLY.3mf: assembly with aligned detailed Pi mesh for inspection only. Do not print the Pi reference.
- verification.json: render and intersection logs.

Bambu Studio has not been updated during this file-only revision. Ask for desktop-session permission before loading these files there. Geometry-only 3MFs have no printer configuration, so Bambu may report that it is loading geometry only. The detailed Pi model may generate non-manifold warnings; it is a reference, not a printable part.

These checks establish clearance for the supplied tessellated Pi reference. Cables, heatsinks, actual fasteners/inserts, rack engagement, insertion path, printed tolerances and strength under load remain untested. Nothing was printed.
