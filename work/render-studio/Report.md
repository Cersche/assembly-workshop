# Depth-tested rack rendering — 2026-10-18

**Subsequent correction:** the selected hybrid GUI was not preserved by the initial integration. It has now been restored and verified in the original normal tab; see `work/gui-render-repair/Report.md`. That report supersedes GUI-preservation statements below. The rendering tests and screenshots retain their historical scope.

Implemented in the runnable app at `outputs/Mechanical_Design_App/`. The original protected `rack-references/rack-scene.js` is byte-for-byte unchanged: SHA-256 `414214bcbf3f1f40ff7a6be0791741ec721cb3d9585cc4d148b1c68f7ff1c7d2`.

## Rendering changes

- New local `rack-references/rack-studio.js`, independently registered in the integrity manifest. All pre-existing manifest entries are unchanged. No external libraries, CDN requests, npm packages or Python dependencies were added.
- Rack source meshes, tray, faceplate, inserts and bolts render in one WebGL context with a shared depth buffer. Canvas 2D retains labels, not equipment surfaces or occlusion masks. Opaque geometry remains depth-tested regardless of submission order.
- Perspective orbit camera with a 32-degree vertical field of view; Front retains orthographic projection. Matching projection and ray math keep labels and mesh selection aligned. The source rack meshes and their recovered placements are retained.
- Rounded 251 x 43.5 mm faceplate, real stadium openings at the supplied mounting coordinates, perforated 176 x 140 mm tray with wall thickness and four hollow bosses. Twenty-eight vent openings remain after reserving solid floor beneath two boss-adjacent grid positions. These are authored preview meshes, not an adapter/STL revision or a new dimensional approval.
- Smooth button-head profiles, real recessed hex sockets, 6 mm shanks, and brass insert rings. The supplied 2.7 mm insert bore is treated as a diameter. Insert length, dome height/profile, slot radius/length, tray wall/floor thickness and boss dimensions include preview assumptions recovered from Track B or authored for visualization; they do not establish supplier identity, manufacturing support or physical approval. Knurl appearance is illustrative.
- Three directional studio lights, metallic/roughness material response, analytic softbox highlights, hemisphere fill, tone mapping and gamma correction. A cached 2048-square shadow pass uses 3 x 3 filtered comparisons, with depth dithering disabled and slope bias to avoid surface striping.
- Screen-space ambient occlusion uses twelve hemisphere samples and a cached camera-depth pass, limited to 1200 pixels across. The studio floor fades into the background instead of producing a hard horizon. Hardware curves have smooth normals; source rack topology remains intact.
- Studio quality / Fast preview toggles cast shadows and contact shading without saving or changing a rack document. Source buffers and repeated hardware geometry are cached. Context loss produces a visible message; the workspace recreates the renderer on context restoration. Resource disposal covers GPU buffers, programs, textures and depth targets. Context restoration was reviewed in code, not induced in browser acceptance.
- Saved artwork uses the existing assembly viewer's normalized placement/scale semantics and applies only on actual front-face triangles. Artwork alignment math was checked; an actual saved-image upload/reload was not exercised in this pass.

## Verification actually completed

- `test_studio.cjs`: 256 projection/matrix/ray comparisons over sampled 1-, 5-, 8- and 48-slot scenes, both cameras and multiple orbit angles. Mesh values/indices and specified extents checked. Rays pass through all four plate openings and all 28 vent centers. Surface picking, blocking, and saved artwork rectangle semantics checked.
- `test_assets.py`: 3 PASS. Original locked script and all prior manifest entries unchanged; new module delivery and script order valid; altered module bytes rejected.
- Existing `test_rack_references.py`: 3 PASS, including exact source coordinate/index fidelity for all 21 source components and tamper rejection.
- Existing `work/rack-scene/test_scene.cjs`: PASS. Rigid source instances, sampled stack sizes, original camera framing and source API remain compatible.
- Existing catalog and Phase7 frontend harnesses: PASS. No manufacturing builds or export actions ran.
- Browser GPU acceptance: 15 PASS; see `GPU_Checks.txt`. Synthetic upright/tray crossing pixel matches the upright-only render. Reversing opaque draw order does not change that result. Source-scene order checks pass at six angles, including rear, steep and underside views. Five angles have zero changed pixels; one has a single raster seam pixel. WebGL error checks pass, including shadows and ambient occlusion.
- Actual disposable workspace: Front/Perspective and Studio/Fast controls work; clicking the rendered faceplate selects Slot 3; no warning/error console entries observed. Checks use separate temporary data at port 8767, never active user data.
- 8 read-only HTTP checks PASS across normal port 8765 and disposable port 8767. Both deliver matching current assets. No normal-server restart or existing user-tab refresh was required/performed. See `HTTP_Checks.json`.
- Screenshots: `Studio_Render.jpg`, `Hardware_Detail.jpg`, `Workspace_Render.jpg`. The standalone study uses a disposable, illustrative Slot 3 allocation and preview colors. Submission timing displayed by the study is CPU submission time, not measured end-to-end GPU frame time or a benchmark guarantee.

## Scope and preservation

Before-edit source copies are in `before-app/`. Application edits are limited to the new renderer, its manifest entry, script loading in index.html and renderer/camera/picking/quality integration in workspace.js. No writes to normal-use data, rack history/artwork, hardware pins, immutable revisions/caches, source rack component meshes, manufacturing geometry, builds or exports were made by this work. Existing user drafts were not refreshed or saved. Normal and disposable servers were left running.

Brian confirms the reference faceplate physically fits the rack post holes perfectly. Preserve that specimen-specific confirmation. It does not certify the newly authored preview meshes, arbitrary equipment, load capacity or strength. Pi4 manufacturing limits and Phase7 closed-with-limitations status remain unchanged. No printing, purchases, uploads, publishing, deployment, push or rack-frame manufacturing work occurred.

The earlier verification blocker is resolved: the supported in-app browser can reach localhost in this resumed turn. No unsupported Windows browser automation or URL-policy bypass was used.

The one-shot integration scripts are implementation records, not startup commands. Do not rerun them against current sources. `refresh_manifest.py` is an explicit development registration step; the preview server no longer silently updates hashes on startup. Integrity checks must continue rejecting unregistered edits.
