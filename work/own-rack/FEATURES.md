# Own rack: feature list

The record for the own-rack orchestrator and the feature sessions. One row per feature Brian asks for. The orchestrator keeps it current; each feature session updates its own row when it finishes.

- Source: `work/own-rack/rack.scad` (one file; one feature session edits it at a time).
- Current draft: draft 5, viewer `work/mesh-viewer/OwnRack_draft5_wire.html`, private Artifact https://claude.ai/artifact/9uLPpx9xdJ1y3Dbp9zwqz5 (draft 4: `OwnRack_draft4.html`, https://claude.ai/artifact/UHywVEtYcY5PpsBBKk64sQ)
- Nothing printed. Fit and strength UNKNOWN throughout.

## Features

Status: asked / in progress / drafted (in the viewer, checked by the orchestrator) / needs more work / parked.

| # | Feature | What Brian asked for (his words) | Status | Session | Viewer | Open questions |
|---|---------|----------------------------------|--------|---------|--------|----------------|
| 1 | Integrated wire management | "lets add integrated wire management into the rack. im talking cable ties, routes, etc." (2026-11-11) | drafted (draft 5; orchestrator checked 2026-11-11: settled decisions unchanged in the file, pushed as 518ce56; waiting for Brian's markup) | wire-mgmt (2026-11-11) | `work/mesh-viewer/OwnRack_draft5_wire.html`, https://claude.ai/artifact/9uLPpx9xdJ1y3Dbp9zwqz5 | Tie width (5.5 x 2.6 slots assumed, for ties up to ~4.8 wide). Which rear corner takes power and which network. CT200 lead exit corner. Are 12 x 44 entry notches big enough, and are rear plates fitted on the lowest U. Is a top crossing wanted (none drawn: the fan fills the top). Tie fit, capacity, strength all UNKNOWN. |

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

- Fan cable route: drafted in draft 5 (side lane beside the fan, down a rear post, into the bottom trough); the CT200 lead's exit corner is still UNKNOWN.
- Cleat wall half.
- Side-panel and bezel clearances are unprinted guesses.
- 2.3 mm wall beside the bracket end-screw recess.
