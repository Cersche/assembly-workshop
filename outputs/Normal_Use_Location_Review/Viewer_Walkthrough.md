# Viewer refinement and visual walkthrough — 2026-10-18

Replaced whole-triangle average-depth painting with per-pixel interpolated depth testing in viewer.js. Crossing tray/faceplate surfaces now occlude correctly. Full-model camera framing fits projected bounds with a margin at default zoom; joint focus retains its deliberate close-up. No mesh coordinates, SCAD, STL, hardware records or validation rules changed.

Verified in the authorized browser session: full assembly, top view, right joint close-up and full reset; selected M3x8 screw inspector shows revision/source fields; saved screw/insert and pilot4 values visible; draft comparison reports both selections match saved selections. Six library records remain loaded. Matching revision download stays disabled with no generated proposal in this session. No Save, Import, Generate or source/package export clicked. The previously documented legacy-cache limitation remains.

Checks PASS: Node viewer behavior; crossing-surface pixel tests (order independence, winding, degeneracy and viewport clipping); post-walkthrough complete SHA-256 equality of both original Beta0.8 and normal-use data against the setup manifest (all six files unchanged). No browser console audit or new STL-generation acceptance is claimed. Screenshot: Refined_Viewer.png.

App left available at http://127.0.0.1:8765 using data/normal-use with --existing-library. Server was started for this walkthrough; no automatic starter import. Browser remains on full assembly. No build, pack import, printing or mounting reassessment. Phase7 remains closed with limitations.

Observed wording follow-up: the library caption still says starter records load at startup even though normal-use launcher explicitly skips that import. No data behavior issue observed; wording can be clarified separately.
