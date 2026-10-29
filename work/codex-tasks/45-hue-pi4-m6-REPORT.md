# Task 45 — HP4-M6-A Hue + Pi 4 M6 rebuild

Completed 2026-10-28 in `D:/Projects/assembly-workshop`, the repository Brian named. Session-start pull: already up to date. No commit or push.

## Changes and screw height

Copied immutable wide-lane `ext.scad` to `outputs/Hue_Pi4_M6_2026-10-28/src/HP4-M6-A.scad`. Only joint geometry, ID calls/modules and associated comments changed. Reused the generator @m6 rounded 20 x 6 tabs, tongue foot, 4 mm coves and counterbore geometry; 14 mm bosses, 7.6 mm bores, 6.6 mm clearance, 11.5 x 3.5 counterbores and 2.5 mm head seats. Three joints retain X=-58/-12/29.5. Original tongue and slot retained. No front screw holes.

Single screw height is Z=32.225 mm (tray_z 8.225 + 24). The generator's +32 would put the boss top at 47.225 and rounded tab top at 50.225, above the 44.425 plate top. Lowering to +24 keeps the boss at 39.225 and tab at 42.225; no clipping. Boss depth 8 mm, pilot runs Y=-0.1..8.1, giving 8 mm of bore inside the boss. Nominal screw engagement 8-2.5-0.3=5.2 mm; usable thread engagement UNKNOWN.

No edge walls were added. Joint feet end at Y=14.3, ahead of the cradle's front posts, and the right tab ends at X=39.5, leaving 6.5 mm to the Pi footprint X=46. Pi position, inserts, openings, cable lane/ties, cradle transform/import/base cut, golden keystone and floor outline remain the baseline source verbatim. IDs: 0.6 mm rear plate engraving, X=-35/Z=8, and floor engraving behind the cradle, X=-35/Y=119. Neither touches functional features.

## Acceptance

| Check | Result |
|---|---|
| OpenSCAD.exe part renders | PASS; simple=yes; no invalid/empty-geometry warnings; 35 inherited assignment-override notices per render |
| Tray closure | PASS; 6,908 triangles, 3,446 vertices, 10,362 edges, 0 edges with incidence !=2, 0 winding inconsistencies, 1 connected shell |
| Plate closure | PASS; 4,884 triangles, 2,428 vertices, 7,326 edges, 0 edges with incidence !=2, 0 winding inconsistencies, 1 connected shell |
| Intersection | **contact only, 0 volume**; 628 contact triangles, every vertex exactly Y=0, without rounding |
| Rear geometry X | PASS; tray -82.5..102, plate -102.4..36.5, combined -102.4..102 within -104..104 |
| Source diff scope | PASS; removing only the four joint modules, added @m6/ID blocks/calls and joint hardware parameter change recovers the baseline text (apart from surrounding whitespace) |
| Protected assets | PASS; 184 SHA-256 file hashes unchanged, including baseline, CM1000/TL-SG108E outputs, generator, packer and data/normal-use |
| Protected git status | PASS; no changes under the prohibited paths; unrelated pre-existing untracked pages preserved |
| BOM | PASS; 3 rack M6 inserts + 3 M6 x 8 button-head screws, separate unchanged Pi board mounting note |
| 3MF | PASS; two descriptive, separate objects, triangle counts preserved, both minimum Z=0, nonoverlapping side-by-side layout via tools/plate_layout_stl.py |

Digital edge checks use exact parsed STL coordinates, no rounding/welding, and shared-edge connected components. Signed volumes: tray 87,394.43394 mm³, plate 44,082.83312 mm³. OpenSCAD's Volumes=2 per part includes the exterior region; the independently checked part has one connected boundary shell.

## Diff summary

Full unified diff: `work/hue-pi4-m6-45/source.diff`.

- Joint constants: boss 9→14, bore 4→7.6, clearance 3.4→6.6.
- Added @m6 joint modules; fixed jzx to [24], omitted edge walls, clip uses unchanged asymmetric tray bounds.
- Faceplate joint add/cut loops use the new single screw height; rear bores only.
- Replaced legacy tray tab/braces and screw cut with m6_tray_joint_add/cut; original tongue-slot cut unchanged.
- Added hp4_plate_id / hp4_tray_id cuts and their 0.6 mm engraving modules.
- All other baseline geometry/code preserved, including both devices, cradle, keystone, ports, tie slots and tray/plate outlines.

## Approved deviation and remaining limits

The original literal “intersection renders empty” criterion returned only zero-thickness Y=0 contact surfaces, including the unchanged floor front against the plate. The build initially blocked packing. Brian then explicitly directed: “Accept the zero-volume contact and pack the 3MF”, said the contact was intended as in the printed baseline, prohibited relief, and changed the failure criterion to real overlapping volume. The build now permits only an empty result or an intersection whose every vertex lies exactly on Y=0. Its result is **contact only, 0 volume**. No geometry was changed to hide contact. The contact result has OpenSCAD non-manifold warnings; the part renders do not. A supplementary attempt to intersect imported ASCII STLs hit CGAL assertion errors and was rejected as evidence; source-CGAL contact geometry is the check used.

One collinear ASCII triangle at the tray's cradle seam is identical to the original baseline STL. The plate has two collinear triangles across ID text bottom edges. These are explicitly counted in acceptance.json; all undirected edges are still shared twice, winding is consistent and each part has one shell. No mesh repair, coordinate rounding, cradle changes or hardware revisions were made. Render closure does not establish printed fit/strength; insert dimensions/retention, load, thread engagement, Pi mounting hardware, cable bend room and slicer behaviour remain UNKNOWN.

No cradle STL copied. No printing, physical testing, uploads, publishing, app/server start, edits to active data, baseline/other brackets/generator, commit or push. No Final_3MF copy: final acceptance of this revision is still Brian's review.

## Evidence and review

`outputs/Hue_Pi4_M6_2026-10-28/checks/` contains acceptance JSON, complete renders and contact source/log/mesh. `work/hue-pi4-m6-45/` contains source diff, protected before/after hashes and git status snapshots. The reproducible Python 3.10 standard-library builder validates before packing and never invokes the generator or changes the source.

Local viewers (not committed): `work/mesh-viewer/HP4-M6-A_assembled.html`, `HP4-M6-A_print-layout.html`, `HP4-M6-A_baseline.html`. SendUserFile is unavailable in this Codex session; the assembled viewer was queued in Codex's browser and direct local links are delivered instead. Viewer geometry is preview-only; no third-party media uploaded.
