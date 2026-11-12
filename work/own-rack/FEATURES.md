# Own rack: feature list

The record for the own-rack orchestrator and the feature sessions. One row per feature Brian asks for. The orchestrator keeps it current; each feature session updates its own row when it finishes.

- Source: `work/own-rack/rack.scad` (one file; one feature session edits it at a time).
- Current draft: draft 5, viewer `work/mesh-viewer/OwnRack_draft5_wire.html`, private Artifact https://claude.ai/artifact/9uLPpx9xdJ1y3Dbp9zwqz5 (draft 4: `OwnRack_draft4.html`, https://claude.ai/artifact/UHywVEtYcY5PpsBBKk64sQ)
- Nothing printed. Fit and strength UNKNOWN throughout.

## Features

Status: asked / in progress / drafted (in the viewer, checked by the orchestrator) / needs more work / parked.

| # | Feature | What Brian asked for (his words) | Status | Session | Viewer | Open questions |
|---|---------|----------------------------------|--------|---------|--------|----------------|
| 1 | Integrated wire management | "lets add integrated wire management into the rack. im talking cable ties, routes, etc." (2026-11-11) | drafted (draft 5; orchestrator checked 2026-11-11: settled decisions unchanged in the file, pushed as 518ce56; waiting for Brian's markup) | wire-mgmt (2026-11-11) | `work/mesh-viewer/OwnRack_draft5_wire.html`, https://claude.ai/artifact/9uLPpx9xdJ1y3Dbp9zwqz5 | Answered by Brian 2026-11-12: ties are 4.8 mm or narrower; power on the left facing the front (-X), network on the right (+X); tie points stay on both sides for the CT200 lead; the 44 x 12 entry notch is fine; no top crossing. Still UNKNOWN until printed: tie fit, capacity, strength. |
| 2 | Fine tune the rack shape | "open a new session to fine tune the rack shape. there are some changes i'd like to make" (2026-11-12, relayed by the wire-mgmt session) | asked (session proposed; it asks Brian for the changes first) | shape-tune | | What the changes are: Brian has not said yet. |

### Wire features a later change must keep (draft 5)

- A 45 degree tie tunnel per U at each post's inside rear corner (5.5 x 2.6 slot, moved 8 mm off the U centre beside a lap joint).
- Two tie tunnels on the inner edge of each bracket side arm.
- 11 tie stations with underside recesses in the bottom panel (5 across the rear, 3 down each side).
- The 20 mm cable trough under the lowest U.
- Entry notches in the rear bottom brackets (X 46..90, 12 deep).
- Power on the left facing the front (-X), network on the right (+X); no top crossing.

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
