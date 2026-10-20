# Workflow audit — 2026-10-18

Brian authorized exercising the app and identifying gaps. Acceptance used a fresh disposable library/rack directory on port8767; the saved normal-use rack and hardware were not test fixtures. No source geometry was generated, rendered through CAD, printed, imported or exported.

## Fixed

1. **Allocations could be added but could not be corrected.** Occupied-slot Properties now provides Edit slot allocation (move/resize) and Release slots. Release has an explicit session Undo slot release action. Edits reject overlap and out-of-range values; undo refuses restoration if a later edit occupies that space or the rack has been shrunk. Hardware projects and meshes are untouched. These remain logical reservations, not installed geometry transforms. Every change is a draft until Save layout.
2. **A second save could start while the first was pending.** A new edit re-enabled the button during a save. The actual handler now serializes requests, keeps newer edits dirty, and advances their generation from the completed snapshot. Saving is blocked while a rack/allocation editor has uncommitted fields. Allocation creation/edit commits resolve the current rack object rather than mutating a stale object retained across a save.
3. **Old success feedback remained after new unsaved edits.** Rack creation/settings now reports that the layout was updated in the draft and needs saving. The selection summary also resets correctly when changing racks.

`rack-references/rack-layout.js` isolates and tests logical allocation edits; it is integrity-listed and loaded before workspace.js. No rack document schema, SQLite schema, hardware pins, existing revisions, cache or manufacturing adapter was changed. Existing normal-server handlers serve the new assets; activation requires only page refresh.

## Browser checks actually performed

- Select an empty slot, reserve two slots, transition into Pi4 assembly inspection, and return to the actual source-mesh rack. No build control was used.
- Reject shrinking the rack past an occupied slot; reject a new allocation overlapping the saved allocation.
- Move the reservation from slots2–3 to4–5; reject out-of-range edits; release it; undo release; save and reload. The updated allocation persisted.
- Create a second named eight-slot rack with UNKNOWN dimensions; preserve both named layouts after reload. The viewport uses source component stacks; their physical mating remains unverified.
- Inspect Review and Prepare. Rack installation, dimensions, fit and strength remain visibly UNKNOWN; Prepare states that exports exclude the rack and slot positions. Generate/export controls were not invoked.
- Search the Keyboard Shortcuts dialog for save; Escape closes it. Verify corrected draft feedback after editing rack settings.
- No browser console warnings/errors. `Allocation_Controls.png` shows the tested new Properties actions in disposable data.

The normal8765 tab was observed only to check whether activation was safe. It had an open, unconfirmed slot5 allocation wizard even though the saved-layout header was clean. It was **not refreshed, saved, cancelled or otherwise altered**. Finish that interaction before refreshing to load the fixes. A clean saved-layout indicator does not mean all open form fields are committed.

## Automated checks

- New logical action tests PASS: move/resize validation, release/restore, shrink/conflict protection during undo. Actual workspace save-handler tests PASS for serialization, edits during an in-flight save, uncommitted-editor guards and clean successful save.
- Existing7 rack document tests and3 full-source-reference/integrity tests PASS in newly created project-local temporary data.
- Source-mesh scene transform/framing tests, existing catalog/Phase7 frontend handlers and all21 individual reference-viewer selections PASS. No mounting-specific test or historical renderer was run.
- Normal-use preservation hashes are recorded separately in Verification.json; this includes the real rack-workspace.json as user data.

## Remaining gaps, in recommended order

| Priority | Gap | Why it matters / next bounded step |
| --- | --- | --- |
| 1 | Independent assembly records per slot | Every allocation still refers to one shared Pi4 hardware project. Create a versioned assembly-instance model with explicit pins/revisions and an export identity per instance before expanding device breadth. Existing saved pins must be preserved. |
| 2 | Installed equipment preview and exact rack interfaces | The rack shows logical highlights; Pi4 is inspected separately in assembly coordinates. Establish source-linked visual transforms and interface/clearance evidence before claiming installed collision or fit support. Physical fit/strength remain UNKNOWN. |
| 3 | Explicit rack component/stack configuration | Taller racks use inferred5U-plus-remainder post stacks. The supplied1U extension is inspectable but not selectable in a stack editor. Add explicit source component choices and provenance; do not infer physical approval from the preview. |
| 4 | More equipment and geometry adapters | Equipment library currently offers Pi4 only. There are no general tray, faceplate or bracket adapters, arbitrary CAD editing or automatic equipment ingestion. Catalog hardware breadth does not provide those geometries. |
| 5 | Recovery and workspace management | Saves preserve JSON history, but the app lacks a history/recovery browser, persisted active-rack selection, rack archive action and automatic unsaved-draft recovery. Current release undo is session-only; saved history remains preserved on disk. |
| 6 | Rack-frame manufacturing export | No supported rack-frame STL adapter exists. Exact source/mesh matching, supported configuration rules, audited transforms and export integrity must precede it. Preview pose tests do not meet that gate. |

These are software/product gaps, not grounds to reopen Phase7, parked research or tabled mounting. No printer/slicer integration is required. Any later printing or physical testing remains separately directed. Creator assets remain local; redistribution rights remain unresolved.
