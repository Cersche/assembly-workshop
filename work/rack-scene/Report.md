# Actual rack mesh preview — 2026-10-18

Brian requested the rack in the main viewport look like his supplied enclosure, and asked to consult yesterday's GUI examples. Replaced the generic box frame with instances of the actual supplied meshes. This is a visual assembly, not a manufacturing rack adapter.

## Implemented

- Main viewport uses the exact component data already extracted from the supplied3MF sources: perforated posts, bottom/top front edges, side rails, feet, handles, bottom panel and top fan panel. Source triangle/vertex data stays unchanged. No OpenSCAD/CAD build, STL regeneration or new manufacturing output.
- Five-slot default has20 visible source component instances; Side panels enables the two actual5U panels (22 instances). Front and Perspective controls, mouse orbit, wheel zoom and keyboard orbit. Optional side panels are a view toggle, not a saved rack specification.
- Slots remain selectable over the actual front opening, with discreet U labels and contextual blue selection. Empty slots no longer draw pretend shelf faces. Occupancy is a planning highlight, not a mesh collision/fit calculation.
- For1–5 slots, the corresponding discrete source post/panel size is used. Taller layouts display stacks of source5U posts plus the remaining discrete size, matching the recovered stack concept. No post is stretched. These stacks are visual inference; their joints/fit remain UNKNOWN. The supplied extension is preserved in the component-reference viewer; no new extension configuration workflow is claimed.
- Existing optional width/depth/pitch values stay user data. They do not resize source meshes or become verified rack dimensions. No data schema or hardware/pin changes. Pi4 remains the only manufacturing adapter, sharing its current hardware project.
- New `rack-references/rack-scene.js` contains isolated source mapping, rigid visual poses, camera math and WebGL rendering. The existing integrity-checked reference routes serve it; its SHA-256 was added to the asset manifest. A page refresh loads it, without restarting the normal server.

## Earlier GUI discussion

Re-read the earlier pages of **Create Claude App Prompt**, `6ad39502-fa44-83e8-a1ce-5a357df4d02e`, including the actual GUI decision turns. `GUI_History_Evidence.json` preserves relevant returned turns. Confirmed choices include the Shapr3D/Tinkercad/Bambu Studio hybrid direction, three-panel layout, Dark Professional theme, Dark CAD Studio viewport, equipment picture cards, contextual Properties, inspection controls and overlays. Those visual/workflow choices guide the preview; earlier printer requirements do not supersede current STL-only scope.

Historical assistant responses containing examples/mockups are still returned as content-reference placeholders. No actual historical assistant mockup image was recovered in this read, so an exact screenshot match is not claimed. The supplied creator photos and full original app's frame placement routines provide the concrete rack-shape reference. The main viewport keeps the recovered dark studio rather than reverting to the legacy app's entire UI or cloud hooks.

Visual poses were transcribed from the recovered original's `bottomSlots`, `topSlots`, `levelSlots`, corner rotations and constants. They were isolated, not executed as historical application code. Source3MF plate transforms were not used as assembled rack poses. Source mesh fidelity and rigid-transform tests do not verify these inferred interfaces or strength.

## Verification

- Node scene tests PASS: rigid transforms only (no rescaling), discrete source stacks for1,3,5,6,8,9,48 slots, valid source mappings, complete framing, and pixel/GL camera alignment for front and perspective views. No export capability exists on the scene.
- Three Python reference tests PASS:21 exact source coordinate/index comparisons, integrity rejection and read-only routes.
- Seven existing rack document tests PASS with new temporary data under this work folder. Existing catalog and Phase7 frontend handler checks PASS. Existing individual-component viewer harness PASS. New module/workspace syntax PASS.
- Brian explicitly approved a fresh browser check. A separate server at8767 used newly created disposable data. Browser checks confirmed actual perforated/honeycomb frame rendering, front/perspective views,20 versus22 parts with the side-panel toggle, and slot3 selection/contextual Create assembly action. No console warnings/errors. No generate/import/export controls were invoked.
- `Rack_Mesh_Preview.png` is the real browser screenshot of the new preview in disposable data. It is not an old recovered mockup. `Protected_Data_Before.json` captures normal-use files; all6 hashes stayed unchanged during implementation and acceptance.

Brian's original browser tab contained an unsaved five-slot draft. It was not reloaded or saved as a test. A save/reload decision was requested only for activating the updated preview in that existing tab. Until then, preserve the draft; do not treat the old handoff's no-saved-rack observation as permission to clear it.

Phase7 remains CLOSED WITH LIMITATIONS. All rack installation, mating clearances, usable depth, M6 insert specification/installation, fit and strength remain UNKNOWN. No mounting work, parked research, printer integration, printing, purchases, upload, release packaging, publishing, deployment or push was performed. All creator assets remain local with unresolved redistribution rights.

## Normal-use activation

Brian subsequently explicitly approved saving the original five-slot draft and refreshing. Saved My Lab Rax (5 slots,0 assemblies), verified saved status after reload and visually confirmed the source-mesh preview in the normal8765 tab. The six pre-existing hardware/cache files remain unchanged. The new rack-workspace.json is now real user data to preserve. See Normal_Use_Activation.json and Normal_Use_Saved_Rack.png.
