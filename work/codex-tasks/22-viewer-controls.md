# Task 22 · Bambu-style controls for every 3D viewer

Brian (2026-10-20, equipment-wizard beta): the 3D viewer controls are "awful". Every 3D view in the app should use the same mouse controls as Bambu Studio's defaults, from ONE shared module instead of separate code in each viewer. See the IDEAS.md Inbox line dated 2026-10-20.

Standing rules in [README.md](README.md) apply (no commits/pushes; Claude reviews, checks in the browser and commits).

## Viewers today

| Viewer | Where | Keep working |
| --- | --- | --- |
| Rack view | workspace.js ~1347-1366 (`rackCanvas` wheel / pointerdown / move / up / cancel; yaw, pitch, zoom 0.5-2.5) | A drag over 4 px switches to 3D perspective (`perspectiveCamera`, `setViewButtons('3d')`); a click without a drag still selects a slot; the existing 3D / Front / Rear buttons. |
| Mesh viewer | viewer.js ~197-206 (`canvas` pointer handlers; `frontMode`, yaw, pitch) | A click without a drag still picks a point (port fine-tuning). |
| Wizard model view, step 1, and the wizard 3D preview | equipment-wizard.js `drawModel` ~114-140 (`view.yaw/pitch/zoom`) | The floor drawn first (`under:true`). |

Check tray-placement.js too: its SVG device drag is 2D placement, not a camera, so leave it alone unless it also has a 3D camera.

## Target controls

Check the current Bambu Studio keyboard and mouse reference first (its wiki or the in-app shortcut list) and write in the report what you found and where. Expected:

- Left-drag: orbit.
- Right-drag and middle-drag: pan.
- Scroll wheel: zoom toward the point under the cursor (not the center).
- One-click view presets suited to each viewer (top, front, iso…) and a "fit view" key or button (Bambu: `Z`). Number keys 0-6 for views if Bambu uses them, active only while the pointer is over or focus is on that canvas, never while typing in a field.
- No browser context menu on the canvases. Touch/pen: one-finger drag orbits, two-finger pinch zooms, if easy.
- Keep the small drag threshold so clicks still select/pick.

## Build

- New file `viewer-controls.js` (plain JS, no libraries) exporting one helper, e.g. `attachViewerControls(canvas, {getView, setView, redraw, onClick, presets, fit})`. Each viewer keeps its own camera math and calls the helper for input.
- Load it in index.html before workspace.js (scripts load in the line-168 `<script>` list).
- Pan needs a camera target/offset in each viewer; add it where missing. Zoom-to-cursor needs the screen point to stay fixed while zooming.
- Optional, only if it does not make drawing slower: reduce the remaining clipping in the shared canvas painter (sorted triangles, no depth buffer). If it is not a quick win, leave it and say so in the report.
- Add `viewer-controls.js` to asset-manifest.json and update the sha256 of every changed front-end file. The hash is computed with CRLF normalized to LF (a test checks this).
- Add a JS test in js-tests/ for the pure parts (button → action mapping, zoom-to-cursor math keeps the cursor point fixed, drag threshold) and register it in js-tests/run.js the same way as the others.

## May change

viewer-controls.js (new), workspace.js, viewer.js, equipment-wizard.js, index.html, asset-manifest.json, js-tests/ (new test + run.js), IDEAS.md (update the 2026-10-20 viewer-controls line to say what's left). Nothing else.

## Checks

Run before and after and report exact results:

```
powershell -NoProfile -ExecutionPolicy Bypass -File outputs\Mechanical_Design_App\run_checks.ps1
```

Do not start or stop servers. Claude checks it in the browser afterwards.

## Report

work/codex-tasks/22-viewer-controls-REPORT.md: files changed with before/after SHA-256, what Bambu's controls are and the source, any differences from them, check results, open questions.
