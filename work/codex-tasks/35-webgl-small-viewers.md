# Task 35 · WebGL for the small 3D previews (wizard + Place on tray)

Brian wants nicer 3D previews. Claude's diagnosis (2026-10-20, disposable data on port 8799, RTX 3080):

- **Rack view and mesh viewer are already WebGL** (`rack-studio.js` `Renderer`: depth buffer, shadows, ambient occlusion; the mesh viewer uses it through `assembly-studio.js` with the canvas painter as fallback). Rack view: 141,326 triangles, 34 parts, ~7–8 ms per frame at 1200×800 with shadows+AO on. Not the problem.
- **The rough one is `window.EquipmentPainter`** (`equipment-wizard.js` `paint`, used by the wizard view and the Place on tray "Live 3D preview"). It is a 2D-canvas painter: every frame it re-projects every triangle in JS, sorts them by average depth and fills them one by one. No depth buffer (overlapping parts clip through each other), flat one-light shading, each triangle stroked to hide seams. Measured: 5k tris 10.6 ms, 20k tris 41.5 ms, 80k tris 452 ms per frame. An imported STEP/STL device easily makes it stutter.

Standing rules in [README.md](README.md) apply. Preview only: no change to any STL, SCAD source, spec or saved data. Fit and strength stay UNKNOWN. No new libraries and nothing loaded from the internet; reuse the WebGL code already in `rack-studio.js`.

## Build

1. **WebGL path for EquipmentPainter.** Keep `EquipmentPainter.draw(cv,view)` / `bind` / `parseStl` signatures. Inside, draw `view.sets` (flat `[x,y,z…]` triangle lists, `color`, `alpha`, `under`) with WebGL: depth test on, opaque sets first, then translucent sets (depth write off, sorted back-to-front by set centre). Same camera maths as today (`P` in `paint`: yaw/pitch/zoom/pan/cen/span, same screen result), so `ViewerControls` and the Iso/Top/Front/Fit buttons behave identically. Prefer reusing `LabRaxStudio.Renderer` (or a small shared helper extracted from it) rather than a second shader stack. Lighting: the same hemisphere + key light look as the rack view; shadows/AO optional and only on High.
2. **Buffers uploaded once.** Upload each set to a GPU buffer when the set array changes (cache by set object / a version counter); orbiting must not re-upload or re-parse. Face normals computed at upload. One WebGL context per canvas, reused; release it when the window closes (no leaked contexts after opening/closing Place on tray 20 times).
3. **Optional edge lines** (feature edges, angle > 30°) as a thin dark overlay, on by default at High, off at Low. Computed once at upload.
4. **Switch and fallback.** Keep the current 2D painter untouched as `paint2d`. Choose WebGL unless: WebGL is unavailable, the context is lost, a localStorage preference `assemblyWorkshop.previewRenderer` = `canvas` (wrapped in try/catch like `render-quality.js`), or a frame-budget fallback (below). On fallback show a one-line note under the preview ("Simple preview — WebGL unavailable"). Context lost → fall back immediately, try WebGL again on restore.
5. **Frame-time budget.** Draw only on demand (requestAnimationFrame when something changed; nothing while idle — no render loop). Measure each draw; if the median of the last 10 WebGL draws exceeds **16 ms**, drop to the next lower quality (High→Medium→Low pixel ratio); if Low still exceeds 33 ms, use the 2D painter for that window. Expose `EquipmentPainter.stats` = `{renderer:'webgl'|'canvas', triangles, lastMs, medianMs}` for tests and review.
6. **Quality slider still works**: `RenderQuality.pixelRatio`/`cell` keep their meaning (Low merges points, High higher resolution). Medium must not look worse than today.

## May change

`equipment-wizard.js`, `rack-studio.js` (extract a shared helper only; rack view output must stay pixel-identical — check with a before/after readPixels hash on the same scene), `tray-placement.js` (only the fallback note / dispose hook), `render-quality.js` (if needed), `asset-manifest.json`, `js-tests/` (register in `js-tests/run.js`). Nothing else; never data/normal-use, coupon folders or third-party meshes.

## Tests

- Camera parity: for a few yaw/pitch/zoom/pan values, the WebGL projection of known points equals the 2D painter's `P` within 0.5 px.
- Switch logic: unavailable WebGL / pref `canvas` / lost context / over-budget medians each pick the right renderer (pure function, no GPU needed in node).
- Upload caching: redrawing with the same sets uploads nothing new.
- Edge extraction: a cube gives 12 edges; a flat subdivided square gives 4.

## Checks and report

Run `run_checks.ps1` before and after. Then in the browser on **disposable data** (temporary `--data` folder, spare port; never data/normal-use, never stop Brian's app on 8765): open Place on tray with the example device and with a large imported STL (≥ 80k triangles), orbit for 5 s, record `EquipmentPainter.stats` (median ms, triangles) at Low/Medium/High for both renderers, and confirm the standoffs/device no longer clip through the tray. Write `work/codex-tasks/35-webgl-small-viewers-REPORT.md` with files + SHA-256, the timings table, the rack-view pixel-hash result, screenshots before/after, and open questions. Claude reviews in the browser.
