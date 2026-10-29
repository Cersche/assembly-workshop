# CM6B — rev 3: packaging + rail-top fix

2026-10-28. **PROPOSED — UNVALIDATED. Fit, strength and retention UNKNOWN.**

The 3MF now has **three build items**: faceplate assembly (body + five light pipes + seven logo letters + two details), rail L, rail R. Each colour mesh is a component of the faceplate, with its own material property; coordinates use the same rigid faceplate placement. Unit is millimeter. No independently placed tiny colour objects. This follows CM6A's component hierarchy; CM6A has no slicer part metadata/material assignments to copy. Bambu/Orca import and filament mapping are **UNTESTED**.

The right rail's stripes were the old reference's engraved letter cuts captured in a side silhouette and extruded across the rail width. Replaced those notches with a straight numeric top edge; made both top outlines horizontal at Z=44.425. Cosmetic rounding setting remains zero; existing X/Z edge facets and CM6B-L/R ID engraving remain. Top strips around each ID measure Z=44.425000, flatness 0.000000 mm across 332 samples per rail, excluding the intentional letters and edge transitions. The unwanted right grooves were 0.475 mm below the corrected top. Ordinary top-level adjustment is at most 0.00405 mm. Changes are confined above Z=43.90662; the other contours and every fit setting are unchanged. 190 fit-feature ray comparisons per rail below Z=43.9 show 0.000000 mm boundary change. Rail bounds and length are unchanged.

`CM6B_source.scad` is self-contained primitive-only generator output; `CM6B_spec.json` stores numeric outlines. No remix meshes are imported into the generator. All 17 individual STLs were explicitly rebuilt with OpenSCAD.exe, closed and single-component. Normal artwork/printing scope is unchanged.

Plate 252 x 44.4 x 4 mm, four corner slots. Joints X=±104.4, Z=8.6/35.85; selected Ø7.6 pilot/Ø6.6 clearance. Rail Y=12.05..133.62, length 121.57 (setting 121.62, 0.05 separation). Bay dimensions/settings, pocket, retention slot, nose/bridge, all 14 colour shapes, and engraved IDs are retained. Task 44's known pocket discrepancy (2.015540 mm worst sampled boundary difference against CM6A) remains; rev 3 does not resolve or reclassify it.

Checks: 234 Python tests (2 skipped), 244 JavaScript tests passed. New tests verify component hierarchy, 14 independently assignable colour material properties, true positions within 0.001 mm, and rail-top flatness. Fourteen legacy source hashes unchanged; fresh HDT triangles match its preserved ID-free reference. For HDT and an ordinary tray, both packers produce byte-identical STL/3MF from identical mesh inputs with the same ZIP timestamp. Fresh OpenSCAD ASCII facet ordering differs between processes; triangle geometry remains identical. See `work/codex-tasks/46-cm6b-3mf-packaging-REPORT.md` and `validation/task46/`.

Final_3MF copy is byte-identical. SHA-256: `40c22e6198d4295cc73129f8e101d064b132e7be0272d5fffc7dbe44b2543b69`.

Physical fit/retention/strength, loads/sag, insert dimensions/compatibility/installation, screw seating/engagement/torque, access, usable rack depth, wall/process suitability, manufacturing accuracy, ID readability and printed colour/light performance remain UNKNOWN. Prior pocket/global surface fidelity gaps remain. Slicer behaviour UNTESTED. No printing, commit, push, normal-use data access or automatic build was performed. Local/private reference-derived work; do not redistribute.

Viewer: `work/mesh-viewer/CM6B_rev3.html` (uncommitted, preview only). Rev 2 delivery snapshot: `work/cm6b-46/before-cm6b/`. Older `validation/` files describe their dated task-44 state; new evidence is under `validation/task46/`.
