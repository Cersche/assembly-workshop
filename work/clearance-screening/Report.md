# Equipment clearance screening (option A) — 2026-10-19

Brian chose A: basic envelope warning, screening only. Physical fit stays UNKNOWN.

- New outputs/Mechanical_Design_App/clearance.js (`WorkshopClearance.screen`). Wizard equipment only; Pi 4 is shown as REFERENCE (its own baseline, not screened).
  - Height: 10 mm tray floor + standoff (0 for straps) + device height vs span × pitch (same stack the wizard enforces).
  - Width: device width + 16 mm tray sides vs rack `width_mm` (the app's "internal width").
  - Depth: 12 mm faceplate offset + device depth vs rack `depth_mm` ("usable depth").
  - Unspecified rack numbers → UNKNOWN; allocation smaller than the equipment's designed U → OVER.
  - "Tight" thresholds (3 / 5 / 10 mm) are screening assumptions, not tolerances.
- Shown in the 03 Review stage per allocation (OK / TIGHT / OVER / UNKNOWN / REFERENCE). Refreshes when the equipment library loads.
- Wiring: app.py serves /clearance.js (server restart needed); index.html loads it; equipment-wizard.js exposes `equipmentLibraryItems()` and fires `equipment-library`.
- Tests: 2 new Node tests (js-tests/run.js). Python 38/38, JS 11/11.
- Browser (disposable :8767, hand-written test library in the scratch copy only — no OpenSCAD build): switch = SCREENED OK; 200 mm amp = OVER on width (216 of 208 mm). Expected 400s for the fake items' missing meshes. Screenshot Review_Screening.jpg.

Finding (not changed): the wizard accepts device widths up to 230 mm, but tray width + 16 mm exceeds the 208 mm nominal internal width above ~192 mm. Worth a decision whether the wizard should warn or cap.

## Wizard warning (Brian: warn, never block — 2026-10-19)
The wizard now shows a non-blocking 'Heads up' on the Device and Generate steps when tray width or device depth is tight/over against the selected rack (nominal 208 × 240 mm if none). Next, Save and Generate stay enabled. Height keeps its existing server-side rule. Verified on disposable :8767 (200 mm width → warning, Next enabled; shown again on Generate step; no console errors). Screenshot Wizard_Warning.jpg.

