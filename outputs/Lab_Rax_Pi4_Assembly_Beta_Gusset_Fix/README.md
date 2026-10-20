# Lab Rax Pi4 Assembly Beta — gusset correction

This revision adds the four intended screw-ear gussets. It corrects the missing joint-position loop and lowers the gusset crests by 3 mm to clear the source's nominal PCB envelope. Original files in Downloads were not overwritten.

## Files

- `assembly_review.3mf`: two-part assembly at the intended relative coordinates, for fit inspection. This is a generic 3MF with no printer or filament settings. It is not a print layout: the tray bottom is 7 mm above the faceplate bottom.
- `tray.stl`: revised tray, with four gussets.
- `faceplate.stl`: regenerated faceplate; design unchanged.
- `pi4_assembly.scad`: editable revision source.

## Geometry checks

The tray remains 112 × 82 × 22 mm and the faceplate remains 252 × 11 × 42 mm. Socket geometry and screw axes are unchanged. Each screw ear has two 2 mm thick side gussets. All four gussets are present in the exported mesh.

The source's simplified PCB envelope is 85 × 56 × 1.6 mm, with its underside at Z=16 mm. The revised gussets have approximately 0.65 mm minimum vertical clearance beneath that envelope where their XY footprints overlap it. The board rests on the four standoff tops.

OpenSCAD solid-intersection checks found no penetration exceeding 0.001 mm between tray and faceplate, or between tray and nominal PCB. Initial zero-thickness intersections were confirmed as the intentional Y=0 faceplate/tray contact and Z=16 standoff/PCB contacts. Both STL exports rendered successfully; the assembled 3MF ZIP and XML structure were also validated.

The two 3.4 mm tray screw bores align with the two 4.2 mm faceplate insert pilots. Insert fit, screw length, screw head and driver access require the actual hardware dimensions. This revision does not select a heat-set insert.

The actual Pi connectors, components, cooler, cables and rack are not represented by the simple PCB envelope. Those clearances and physical printed fit remain unverified. No print has been started.


## Detailed Pi STEP check update
The complete Pi reference reveals approximately 0.05 mm interference between a USB connector metal feature and the right inner gusset. The previous nominal PCB-only clearance check does not establish complete Pi clearance. No further geometry change has been made. See ../Pi4_fit_inspection.md.
