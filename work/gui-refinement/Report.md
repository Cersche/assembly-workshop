# Selected hybrid GUI refinement — 2026-10-18

Brian selected **1C, 2C, 3A, 4A, 5A, 6A, 7A, 8A**. Decisions are recorded in Decisions.json. Navigation and slot actions were addressed first; the same pass integrated the selected save/appearance controls. Left grouping is provisional for Brian's review, as he requested.

## Implemented

- Hybrid studio: compact rack tree and collapsible inspector, preserving the dark rack-first studio and exact source-mesh enclosure preview. Hide/Show inspector expands the viewport. Racks & slots, Equipment and Hardware are independent collapsible left sections. Section headers and inspector tabs remain accessible while their panel scrolls. Slot rows were shortened.
- Click selects; ellipsis/right-click opens the shared slot actions menu. Actions expose contextual Setup/Appearance controls and restore a hidden inspector when needed. Existing keyboard context-menu and Escape behavior remains. Open rack/allocation editors must be applied or cancelled before switching away.
- Setup / Hardware / Appearance tabs replace the permanent property stack. Empty slots have Hardware disabled. A saved allocated slot can be opened from Setup or Hardware. New allocations remain drafts, require the header Save, and cannot silently save by opening Hardware.
- **One explicit Save button** in the header, also Ctrl/Cmd+S. `assembly_records.save_workspace` preflights the document/hardware and commits layout, appearance and the open independent hardware draft as one atomic JSON write. Invalid hardware, stale generation/revision or tampering reject the whole change. No intermediate layout-only commit. Legacy library/pins remain separate and immutable. Existing old-client routes remain protected.
- Saves serialize; newer edits remain unsaved while the receipt advances generation/revision, even if newer hardware text becomes invalid during the request. Failed input construction does not leave the UI locked. Check/export actions require explicit Save rather than silently committing pending drafts. No check/export/generation buttons were exercised in acceptance.
- Appearance uses eight named preset swatches plus native custom color pickers for rack, source component type and supported equipment/tray/faceplate previews. Artwork adds Fit & center and Center controls to the existing local chooser, size/position and removal. Preview-only; STL artwork is still deferred.
- Browser acceptance uncovered a startup timing issue: opening an instance before viewer initialization could miss its appearance event. The current appearance is now retained and replayed when the viewer initializes. A dedicated delayed-start test covers this; immediate reload/open was verified visually. Hardware envelopes also refresh after a combined Save.

## Actual activation and preservation

The normal tab had an unsaved rack appearance/layout draft. It was left intact while development used disposable data. Brian explicitly selected **Save current draft and refresh** (first `1`, then the structured reply). Saved the old page with its valid existing session before restarting the backend; then reloaded the same normal tab into the refined GUI. Brian's rack component colors were retained. My Lab Rax remains five slots/zero allocations.

Verified old PID19424 and its8765 listener before replacing it. **Normal PID25160** runs current app.py with `--existing-library --data data/normal-use --port8765`, six revisions/zero starter imports. No duplicate normal server was started. `After_Authorized_Draft_Save.json` captures all files after Brian's explicit save; all match after restart/read-only inspection. Six pre-existing library/cache files and four protected mechanical baseline files are unchanged. SQLite integrity is `ok`. The authorized rack save/history are preserved as user data; do not classify them as acceptance fixtures.

Before-app and before-guide files, authorized rack snapshot, decisions, verification and screenshots are in this folder. Most assets are untracked; Git alone is not a backup. Preserve rack-workspace.json, rack-history/, artwork/, library.sqlite3 and revisions/ together.

## Verification

- 37 targeted Python tests PASS: previous31 plus6 atomic-save tests. Fresh temporary data only; tabled source-generation/mounting tests excluded.
- Actual JavaScript save-controller tests PASS serialization, combined payloads, newer layout/hardware edits, invalid newer hardware, and editor/image guards. Viewer startup replay, existing viewer controls, catalog/Phase7 handlers and context/artwork depth tests PASS.
- Disposable8767 browser: collapsed inspector/context creation, tabs, explicit Save before opening a new record, combined hardware+colors save, image fit/center and persistence, rapid reload/open appearance restoration, and second-instance independence. No console warnings/errors. Normal8765 inspected read-only after the approved save/reload. Screenshots: Normal_Hybrid_Studio.png (actual user rack), Hybrid_Appearance.png (disposable image preview).
- Narrow breakpoint overrides were attempted, but the background tab continued reporting1280px, so narrow-width visual acceptance is **not claimed**. Desktop views were inspected at the browser's actual sizes.

## Continuing boundaries

No CAD build, manufacturing export, printing, purchasing, remote upload, release packaging, publishing, deployment or push. Pi4 remains the only manufacturing adapter; rack is layout/source-mesh context, with no frame STL or installed-equipment clearance engine. Physical dimensions/interfaces, M6 specification, usable depth, fit and strength remain UNKNOWN unless separately documented. Phase7 stays CLOSED WITH LIMITATIONS; mounting and niche research remain parked.

Next refinement is Brian's assessment of the left collapsible grouping and inspector flow. His choice2C is provisional; no new product decisions are required just to use the implemented pass.
