# Studio rendering in Assemble — 2026-10-18

Assemble now uses the rack tab's existing WebGL renderer for its actual inspection meshes. A new integrity-checked `rack-references/assembly-studio.js` adapter submits the loaded baseline/generated model parts, optional detailed Pi source and nominal hardware envelopes to that renderer. No rack-preview tray/faceplate substitutes are used. Model coordinates, indices, revisions and manufacturing exports are unchanged.

## Presentation and preserved controls

- Same directional studio lights, material response, analytic softbox reflections, hemisphere fill, tone mapping, antialiasing, filtered cast shadows and screen-space contact shading as the rack viewer. Plastic colors remain appearance-driven; hardware envelopes use steel/brass finishes and retain their reference/envelope labels.
- Perspective orbit for full assembly and joint focus; faceplate front remains orthographic. The camera frames the actual model silhouette and keeps visibility toggles from reframing the model. Joint focus, Top, Full assembly and Zoom remain available.
- A visual stage floor follows the inspection model's minimum Z and fades into the background. It is not part of the inspection/manufacturing model or exports.
- Shared depth testing for all displayed parts. Exact-mesh ray picking preserves click selection, cyan rim/tint, empty-space/Escape clearing and drag/keyboard orbit. The selection rim now accepts per-object bounds so it follows the actual inspection plate instead of assuming rack-preview dimensions.
- Local artwork retains the existing saved rectangle semantics and is textured only onto actual front-face triangles. Mounting holes remain open. Tested with an original synthetic PNG in disposable data; no user artwork was changed.
- Optional detailed Pi, visibility controls, independent assembly context, hardware envelopes and intentionally overlaid dashed guide axes remain. GPU buffers are reused and retired when model/visible reference meshes change. Hardware-envelope meshes are cached between input changes. Context-restoration logic recreates the studio renderer; context restoration was reviewed, not forced during acceptance.
- Existing software inspection remains a fallback when WebGL cannot be initialized or rendered. Its depth/selection and control suites still pass. GPU fallback error text is included when a rendering failure supplies an error. No new runtime libraries or external/CDN dependencies were added.

## Verification actually completed

- `test_adapter.cjs` PASS: exact-mesh bounds, frontmost source faceplate/tray/background picking, perspective/orthographic projection and fitted camera alignment; source input objects unchanged.
- `check_assets.py` PASS: both authored renderer modules match integrity checks; original `rack-scene.js` retains SHA-256 `414214bcbf3f1f40ff7a6be0791741ec721cb3d9585cc4d148b1c68f7ff1c7d2`; all other prior reference entries unchanged. Only the new adapter was added to the manifest.
- Existing viewer controls/model-switching, viewer depth, selection occlusion, appearance startup replay, combined Save and Phase7 frontend suites PASS. Existing rack geometry/camera suite PASS (256 comparisons).
- Nine assembly GPU checks PASS; recorded in `Assembly_GPU_Checks.txt`. Exact inspection triangle counts and source object identity preserved, reverse draw order yields zero changed seam pixels, front/hidden-part picking correct, detailed Pi uses the exact source mesh, no WebGL state errors, shadows/AO enabled, source coordinates/indices unchanged.
- All fifteen shared rack GPU checks PASS again after the shared shader extension.
- Disposable browser verified WebGL rendering, direct faceplate/tray selection, right-joint focus, Full assembly, Top, detailed Pi (133,734 submitted source triangles), and artwork fit/front projection. Front-view clicking preserves front mode. Only synthetic artwork and disposable data were saved. `Artwork_Front_GPU.jpg` records that preview.
- Normal tab had Save disabled and saved hardware status. Safely reloaded it, reopened existing Slot 1, confirmed `data-renderer=webgl`, and restored faceplate selection. No console warnings/errors observed. Screenshots: `Normal_Studio_Assemble.jpg`, `Normal_Studio_Selected.jpg`. Disposable test tab closed.

The current normal app is left open in Assemble with studio rendering. No backend restart, normal-use save, mesh generation/export, physical testing, remote upload, packaging or publication occurred. All fourteen normal-use files retain their pre-work hashes. Before-edit sources, prior test page, local fixture and evidence remain in this folder. This pass supersedes the earlier statement that Assemble still uses only the software orthographic renderer; its fallback remains available. Preview quality does not add physical approval or change any Phase7/manufacturing limits.
