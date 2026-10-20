# Sidebar Hardware library slimming — 2026-10-19

Brian approved the plan. UI layout only; no data, pin, import, save, geometry or export behavior changed. Originals in originals/ (index.html unchanged in the end).

- workspace.js (after the cards move into #hardwarePane): section renamed "Hardware library"; one-line hint pointing to the inspector Hardware tab for per-slot choices; size coverage relabelled ("M3 · 3 screws / 3 inserts") and empty sizes hidden behind a "N sizes awaiting parts" toggle (MutationObserver re-applies after app.js re-renders coverage); catalog-pack and import cards moved into a collapsed "Add or import parts" group. Element IDs unchanged.
- workspace.css: appended rules for the above and hid the duplicate inner "Hardware library" heading.
- Dimension/property filters were already collapsed by default.

Verified in browser pane against normal 8765 server (reload only, nothing saved): only M3 visible, toggle shows 13 → all 14 → back, 6 part rows, section height ~1880 → ~920 px. Screenshot: Sidebar_Hardware_Library.jpg. Not exercised: importing a pack/records (not clicked).

Also this session: rack-references/asset-manifest.json regained its assembly-studio.js entry (dropped ~2026-10-18 20:04; file hash unchanged d67896c4…7608), restoring the assembly inspection renderer; old manifest at work/equipment-list/originals/asset-manifest.json.
