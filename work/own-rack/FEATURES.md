# Own rack: feature list

The record for the own-rack orchestrator and the feature sessions. One row per feature Brian asks for. The orchestrator keeps it current; each feature session updates its own row when it finishes.

- Source: `work/own-rack/rack.scad` (one file; one feature session edits it at a time).
- Current draft: draft 4, viewer `work/mesh-viewer/OwnRack_draft4.html`, private Artifact https://claude.ai/artifact/UHywVEtYcY5PpsBBKk64sQ
- Nothing printed. Fit and strength UNKNOWN throughout.

## Features

Status: asked / in progress / drafted (in the viewer, checked by the orchestrator) / needs more work / parked.

| # | Feature | What Brian asked for (his words) | Status | Session | Viewer | Open questions |
|---|---------|----------------------------------|--------|---------|--------|----------------|
| | (none yet: Brian was asked for his list on 2026-11-11) | | | | | |

## Decisions a feature must not change

Unless Brian says so in chat. Check these in the file after every feature.

- **U standard (Lab Rax, exact):** 44.45 mm per U; holes at X ±118.2625, at each U centre and ±15.902; faceplate 252 x 44.4 x 4; depth 240; 9U. Bed 256 x 256.
- **Hardware:** M6 x 10 button heads into M6 x 5 x 8 heat-set inserts (7.6 bore). M3 x 35 approved for the fan mount only. No self-tapping into prints, no drilling prints. Ask before any new screw type.
- **Flush bezel:** post fronts step 4 mm forward beside the faceplates, 0.6 gap each side; the rear matches the front.
- **Look B:** 15 mm outer corners, accent strip down each post side, shadow lines at the post ends, caps over the top screw heads.
- **Posts:** 4U + 1U extension + 4U per corner, lap joint (tab in notch), one M6 from the post's rear face, hidden by the side panel tongue.
- **Corner brackets** top and bottom; arms meet mid-span; top and bottom panels drop into a pocket and tie them together. 0.3 mm gap between the top/bottom faceplate edges and the brackets (posts run 0.3 longer at each end; U positions unchanged).
- **Fan:** Thermaltake CT200 (195 x 195 x 30, holes 155 x 155; `docs/devices/fan-200mm.md`) does NOT stick out of the top. It hangs under a 6 mm top panel whose grille is flush with the rack top, on 4 x M3 x 35 from below into M3 inserts. Top brackets 38 tall so the fan stays above slot 1; bottom brackets 24. Plain bottom panel.
- **Side panels:** flush drop-in, two halves per side, vents in the bottom 2U of the lower halves.
- **Wall cleat:** rack half only (bar on the rear top brackets, 6 x M6, plus two ears to the rear posts' top holes, 2 x M6). The wall half comes later; don't ask what wall it mounts to.

## Known open items (not features yet)

- Fan cable route.
- Cleat wall half.
- Side-panel and bezel clearances are unprinted guesses.
- 2.3 mm wall beside the bracket end-screw recess.
